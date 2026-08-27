"""Shared OpenAPI, naming, file-output, and reporting utilities for generators."""

from __future__ import annotations

import hashlib
import json
import keyword
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_URL = "https://www.torn.com/swagger/openapi.json"
MISSING = object()


class CodegenError(RuntimeError):
    """Base error for all Torn SDK code-generation workflows."""


class ReviewRequired(CodegenError):
    """Raised when a contract cannot be translated safely without review."""


class MergeConflict(ReviewRequired):
    """Raised when multiple OpenAPI operations cannot become one SDK method."""


class WrapperUnsupported(ReviewRequired):
    """Raised when TornAPIWrapper cannot safely service an OpenAPI operation."""


class PythonNames:
    """Centralized OpenAPI -> Python naming policy."""

    _splitter = re.compile(r"[^0-9A-Za-z]+")
    _camel_boundary_1 = re.compile(r"(.)([A-Z][a-z]+)")
    _camel_boundary_2 = re.compile(r"([a-z0-9])([A-Z])")

    @classmethod
    def snake(cls, value: str) -> str:
        """Normalize arbitrary text into a snake_case Python name.

        Args:
            value: Source text to normalize.

        Returns:
            A valid, nonempty snake_case name.
        """
        value = value.strip().replace("-", "_")
        value = cls._camel_boundary_1.sub(r"\1_\2", value)
        value = cls._camel_boundary_2.sub(r"\1_\2", value)
        value = cls._splitter.sub("_", value)
        value = re.sub(r"_+", "_", value).strip("_").lower()
        return value or "value"

    @classmethod
    def pascal(cls, value: str) -> str:
        """Normalize arbitrary text into a PascalCase Python name.

        Args:
            value: Source text to normalize.

        Returns:
            A valid, nonempty PascalCase name.
        """
        parts = [part for part in cls.snake(value).split("_") if part]
        return (
            "".join(part[:1].upper() + part[1:] for part in parts) or "Value"
        )

    @classmethod
    def identifier(cls, value: str) -> tuple[str, str | None]:
        """Return a safe Python identifier and any required original alias.

        Args:
            value: OpenAPI name to convert.

        Returns:
            The Python identifier and the original name when an alias is needed.
        """
        original = value
        if value.startswith("_"):
            value = value.lstrip("_") or "value"
        value = cls.snake(value)
        if value[:1].isdigit():
            value = f"value_{value}"
        if keyword.iskeyword(value):
            value = f"{value}_"
        return value, original if value != original else None

    @classmethod
    def path_parameter(cls, name: str, tag: str) -> tuple[str, str | None]:
        """Return a Python-safe name for an OpenAPI path parameter.

        Args:
            name: OpenAPI path parameter name.
            tag: Resource tag used to disambiguate generic ``id`` parameters.

        Returns:
            The Python identifier and any required original alias.
        """
        snake = cls.snake(name)
        if snake == "id":
            return f"{cls.snake(tag)}_id", name
        return cls.identifier(name)

    @classmethod
    def enum_alias(cls, source_name: str) -> str:
        """Return the preferred Python alias name for an enum schema.

        Args:
            source_name: OpenAPI component name for the enum schema.

        Returns:
            The derived Python type-alias name.
        """
        name = source_name
        if name.startswith("Api"):
            name = name[3:]
        if name.endswith("Enum"):
            name = name[:-4]
        if name.endswith("Type"):
            return name
        return f"{name}Type"


class OpenAPIDocument:
    """Loaded Torn OpenAPI document shared by every generator."""

    def __init__(self, data: dict[str, Any], source: Path) -> None:
        self.data = data
        self.source = source

    @classmethod
    def download(
        cls,
        *,
        url: str = SCHEMA_URL,
        user_agent: str = "torn-sdk-codegen/0.1.0",
    ) -> dict[str, Any]:
        """Download the Torn OpenAPI document as a JSON object.

        Args:
            url: OpenAPI document URL.
            user_agent: HTTP User-Agent header sent with the request.

        Returns:
            The decoded OpenAPI document.

        Raises:
            CodegenError: If the downloaded JSON root is not an object.
        """
        request = urllib.request.Request(
            url,
            headers={"User-Agent": user_agent},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.load(response)
        if not isinstance(data, dict):
            raise CodegenError("Downloaded OpenAPI root must be a JSON object")
        return data

    @classmethod
    def load(
        cls,
        path: Path,
        *,
        download_if_missing: bool = True,
    ) -> "OpenAPIDocument":
        """Load an OpenAPI document from disk, downloading it if needed.

        Args:
            path: Local OpenAPI JSON path.
            download_if_missing: Whether a missing document may be downloaded.

        Returns:
            The loaded OpenAPI document wrapper.

        Raises:
            CodegenError: If the document cannot be loaded or is invalid.
        """
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise CodegenError(
                    f"Unable to load OpenAPI document {path}: {exc}"
                ) from exc
            if not isinstance(data, dict):
                raise CodegenError("OpenAPI root must be a JSON object")
            return cls(data, path)

        if not download_if_missing:
            raise CodegenError(f"OpenAPI document does not exist: {path}")

        data = cls.download()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return cls(data, path)

    @property
    def paths(self) -> Mapping[str, Any]:
        """Return the OpenAPI paths collection.

        Returns:
            Mapping of path templates to OpenAPI path items.
        """
        return self.data.get("paths", {})

    @property
    def schemas(self) -> Mapping[str, Any]:
        """Return the OpenAPI component schemas collection.

        Returns:
            Mapping of component schema names to schema definitions.
        """
        return self.data.get("components", {}).get("schemas", {})

    @property
    def parameters(self) -> Mapping[str, Any]:
        """Return the OpenAPI component parameters collection.

        Returns:
            Mapping of component parameter names to definitions.
        """
        return self.data.get("components", {}).get("parameters", {})

    @property
    def version(self) -> str:
        """Return the declared OpenAPI version string.

        Returns:
            Document version, or ``"unknown"`` when absent.
        """
        return str(self.data.get("info", {}).get("version", "unknown"))

    @property
    def source_hash(self) -> str:
        """Return a stable hash of the loaded OpenAPI document.

        Returns:
            SHA-256 digest of the canonicalized document JSON.
        """
        payload = json.dumps(self.data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class RefResolver:
    """Local OpenAPI reference resolver with OpenAPI 3.1 sibling support."""

    def __init__(self, document: OpenAPIDocument) -> None:
        self.document = document

    def resolve_ref(self, ref: str) -> Any:
        """Resolve an internal OpenAPI JSON pointer reference.

        Args:
            ref: Internal JSON pointer beginning with ``#/``.

        Returns:
            The referenced document value.

        Raises:
            ReviewRequired: If the reference is external or cannot be resolved.
        """
        if not ref.startswith("#/"):
            raise ReviewRequired(f"External $ref is unsupported: {ref}")

        current: Any = self.document.data
        for token in ref[2:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            try:
                current = current[token]
            except (KeyError, TypeError) as exc:
                raise ReviewRequired(f"Unable to resolve $ref {ref}") from exc
        return current

    def resolve(self, node: Any) -> Any:
        """Resolve a `$ref` node and merge any OpenAPI 3.1 sibling fields.

        Args:
            node: OpenAPI node that may contain a ``$ref``.

        Returns:
            The original node or its resolved, sibling-merged value.

        Raises:
            ReviewRequired: If a contained reference cannot be resolved.
        """
        if not isinstance(node, dict) or "$ref" not in node:
            return node

        resolved = self.resolve_ref(str(node["$ref"]))
        if not isinstance(resolved, dict):
            return resolved

        siblings = {key: value for key, value in node.items() if key != "$ref"}
        if not siblings:
            return resolved

        merged = dict(resolved)
        merged.update(siblings)
        return merged

    @staticmethod
    def ref_name(node: Any) -> str | None:
        """Return the component name referenced by a `$ref` node.

        Args:
            node: OpenAPI node to inspect.

        Returns:
            The referenced component name, if present.
        """
        if isinstance(node, dict) and isinstance(node.get("$ref"), str):
            return node["$ref"].rsplit("/", 1)[-1]
        return None


class SchemaExampleFactory:
    """Build deterministic JSON-compatible examples from OpenAPI schemas."""

    def __init__(
        self,
        refs: RefResolver,
        *,
        max_depth: int = 40,
    ) -> None:
        self.refs = refs
        self.max_depth = max_depth
        self.warnings: list[str] = []

    def build(
        self,
        schema: Any,
        *,
        name_hint: str,
        depth: int = 0,
        ref_stack: tuple[str, ...] = (),
    ) -> Any:
        """Build a deterministic example value for an OpenAPI schema node.

        Args:
            schema: Schema or reference node to sample.
            name_hint: Contextual name used for generated scalar values.
            depth: Current recursive traversal depth.
            ref_stack: References currently being resolved.

        Returns:
            A JSON-compatible example value.
        """
        if depth > self.max_depth:
            self.warnings.append(
                f"maximum schema depth exceeded at {name_hint}; using null"
            )
            return None

        if not isinstance(schema, Mapping):
            return None

        if "$ref" in schema:
            ref = str(schema["$ref"])
            ref_name = ref.rsplit("/", 1)[-1]
            if ref in ref_stack:
                resolved = self.refs.resolve(schema)
                if self._nullable(resolved):
                    return None
                self.warnings.append(
                    f"recursive schema {ref_name} at {name_hint}; using empty object"
                )
                return {}
            return self.build(
                self.refs.resolve(schema),
                name_hint=ref_name,
                depth=depth + 1,
                ref_stack=(*ref_stack, ref),
            )

        if "example" in schema:
            return schema["example"]

        examples = schema.get("examples")
        if isinstance(examples, list) and examples:
            return examples[0]

        if "const" in schema:
            return schema["const"]

        if "default" in schema and schema["default"] is not None:
            return schema["default"]

        enum = schema.get("enum")
        if isinstance(enum, list) and enum:
            non_null = [value for value in enum if value is not None]
            return non_null[0] if non_null else None

        if "allOf" in schema:
            return self._all_of(schema["allOf"], name_hint, depth, ref_stack)

        if "oneOf" in schema:
            return self._first_branch(
                schema["oneOf"], name_hint, depth, ref_stack
            )

        if "anyOf" in schema:
            return self._first_branch(
                schema["anyOf"], name_hint, depth, ref_stack
            )

        schema_type = schema.get("type")
        if isinstance(schema_type, list):
            non_null = [item for item in schema_type if item != "null"]
            if not non_null:
                return None
            clone = dict(schema)
            clone["type"] = non_null[0]
            return self.build(
                clone,
                name_hint=name_hint,
                depth=depth + 1,
                ref_stack=ref_stack,
            )

        if schema_type == "null":
            return None

        if schema_type == "object" or "properties" in schema:
            return self._object(schema, name_hint, depth, ref_stack)

        if schema_type == "array":
            try:
                count = max(1, int(schema.get("minItems", 0) or 0))
            except (TypeError, ValueError):
                count = 1
            count = min(count, 3)
            return [
                self.build(
                    schema.get("items", {}),
                    name_hint=f"{name_hint}_item",
                    depth=depth + 1,
                    ref_stack=ref_stack,
                )
                for _ in range(count)
            ]

        if schema_type == "integer":
            return self._integer(schema)
        if schema_type == "number":
            return float(self._integer(schema))
        if schema_type == "boolean":
            return True
        if schema_type in {"string", None}:
            return self._string(schema, name_hint)

        self.warnings.append(
            f"unsupported schema type {schema_type!r} at {name_hint}; using null"
        )
        return None

    def _object(
        self,
        schema: Mapping[str, Any],
        name_hint: str,
        depth: int,
        ref_stack: tuple[str, ...],
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}
        properties = schema.get("properties", {})
        if isinstance(properties, Mapping):
            for name, child in properties.items():
                result[str(name)] = self.build(
                    child,
                    name_hint=f"{name_hint}_{name}",
                    depth=depth + 1,
                    ref_stack=ref_stack,
                )

        additional = schema.get("additionalProperties")
        if not result and isinstance(additional, Mapping):
            result["key"] = self.build(
                additional,
                name_hint=f"{name_hint}_value",
                depth=depth + 1,
                ref_stack=ref_stack,
            )
        return result

    def _all_of(
        self,
        branches: Any,
        name_hint: str,
        depth: int,
        ref_stack: tuple[str, ...],
    ) -> Any:
        if not isinstance(branches, list):
            return None
        values = [
            self.build(
                branch,
                name_hint=name_hint,
                depth=depth + 1,
                ref_stack=ref_stack,
            )
            for branch in branches
        ]
        if all(isinstance(value, dict) for value in values):
            merged: dict[str, Any] = {}
            for value in values:
                merged.update(value)
            return merged
        return next((value for value in values if value is not None), None)

    def _first_branch(
        self,
        branches: Any,
        name_hint: str,
        depth: int,
        ref_stack: tuple[str, ...],
    ) -> Any:
        if not isinstance(branches, list):
            return None
        for branch in branches:
            resolved = self.refs.resolve(branch)
            if (
                isinstance(resolved, Mapping)
                and resolved.get("type") == "null"
            ):
                continue
            return self.build(
                branch,
                name_hint=name_hint,
                depth=depth + 1,
                ref_stack=ref_stack,
            )
        return None

    @staticmethod
    def _nullable(schema: Any) -> bool:
        if not isinstance(schema, Mapping):
            return False
        schema_type = schema.get("type")
        if schema_type == "null":
            return True
        if isinstance(schema_type, list) and "null" in schema_type:
            return True
        for key in ("oneOf", "anyOf"):
            branches = schema.get(key)
            if isinstance(branches, list):
                if any(
                    isinstance(branch, Mapping)
                    and branch.get("type") == "null"
                    for branch in branches
                ):
                    return True
        return False

    @staticmethod
    def _integer(schema: Mapping[str, Any]) -> int:
        minimum = schema.get("minimum")
        if isinstance(minimum, (int, float)):
            return int(minimum)
        exclusive = schema.get("exclusiveMinimum")
        if isinstance(exclusive, (int, float)):
            return int(exclusive) + 1
        maximum = schema.get("maximum")
        if isinstance(maximum, (int, float)) and maximum < 1:
            return int(maximum)
        return 1

    @staticmethod
    def _string(schema: Mapping[str, Any], name_hint: str) -> str:
        fmt = schema.get("format")
        formats = {
            "date-time": "2026-01-01T00:00:00Z",
            "date": "2026-01-01",
            "time": "00:00:00",
            "uuid": "00000000-0000-4000-8000-000000000000",
            "email": "mock@example.test",
            "ipv4": "127.0.0.1",
            "ipv6": "::1",
            "uri": "https://example.test/",
            "url": "https://example.test/",
        }
        if fmt in formats:
            return formats[fmt]

        lowered = name_hint.lower()
        if "url" in lowered or "link" in lowered:
            return "https://example.test/"
        if "email" in lowered:
            return "mock@example.test"
        if "name" in lowered:
            return "Mock"
        if "description" in lowered or "text" in lowered:
            return "Mock value"

        try:
            length = max(1, int(schema.get("minLength", 1) or 1))
        except (TypeError, ValueError):
            length = 1
        return "x" * min(length, 32)


@dataclass(frozen=True)
class FileChange:
    """Describe one generated file operation.

    Attributes:
        path: Absolute path of the affected file.
        status: Planned operation, such as ``"create"`` or ``"unchanged"``.
    """

    path: Path
    status: str


class GeneratedFileManager:
    """Deterministic write/check/prune helper shared by generators."""

    GENERATED_MARKER = "AUTO-GENERATED"

    def __init__(
        self,
        root: Path,
        *,
        check: bool = False,
        dry_run: bool = False,
        prune: bool = False,
    ) -> None:
        self.root = root
        self.check = check
        self.dry_run = dry_run
        self.prune = prune
        self.expected: set[Path] = set()
        self.changes: list[FileChange] = []

    @property
    def dirty(self) -> bool:
        """Return whether any tracked file change is not unchanged.

        Returns:
            ``True`` when generation would alter or remove a file.
        """
        return any(change.status != "unchanged" for change in self.changes)

    def emit(self, relative: Path, content: str) -> None:
        """Create or update a generated file tracked by this manager.

        Args:
            relative: File path relative to the managed root.
            content: Complete generated file content.
        """
        path = self.root / relative
        self.expected.add(path)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            self.changes.append(FileChange(path, "unchanged"))
            return

        status = "update" if path.exists() else "create"
        self.changes.append(FileChange(path, status))
        if self.check or self.dry_run:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def scaffold(self, relative: Path, content: str) -> None:
        """Create a file only when it does not already exist.

        Args:
            relative: File path relative to the managed root.
            content: Initial file content.
        """
        path = self.root / relative
        self.expected.add(path)
        if path.exists():
            self.changes.append(FileChange(path, "unchanged"))
            return
        self.changes.append(FileChange(path, "scaffold"))
        if self.check or self.dry_run:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def find_stale(self, roots: Iterable[Path]) -> None:
        """Mark generated Python files under the given roots as stale.

        Args:
            roots: Relative directories to search for generated Python files.
        """
        for relative_root in roots:
            absolute = self.root / relative_root
            if not absolute.exists():
                continue
            for path in absolute.rglob("*.py"):
                if path in self.expected:
                    continue
                self._mark_stale(path)

    def find_stale_paths(self, paths: Iterable[Path]) -> None:
        """Mark specific generated paths as stale when they were not emitted.

        Args:
            paths: Relative generated file paths to inspect.
        """
        for relative in paths:
            path = self.root / relative
            if path.exists() and path not in self.expected:
                self._mark_stale(path)

    def _mark_stale(self, path: Path) -> None:
        try:
            head = path.read_text(encoding="utf-8")[:256]
        except OSError:
            return
        if self.GENERATED_MARKER not in head:
            return
        self.changes.append(FileChange(path, "remove"))
        if self.prune and not self.check and not self.dry_run:
            path.unlink()


class ReportExporter:
    """Write generation reports to user-selected paths."""

    def export(self, path: Path, content: str) -> Path:
        """Write a report file and return its final path.

        Args:
            path: Destination report path.
            content: Report text to write.

        Returns:
            The destination path.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path


def normalize_tags(tags: Sequence[str] | None) -> set[str] | None:
    """Normalize optional tag filters into snake_case tag names.

    Args:
        tags: Optional raw resource tag filters.

    Returns:
        Normalized tags, or ``None`` when no filter was provided.
    """
    if not tags:
        return None
    return {PythonNames.snake(tag) for tag in tags}
