"""Limen commands that generate Torn SDK sources, mocks, and contract tests."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from limen.argument_type import ArgumentType
from limen.base_command import BaseCommand
from limen.registry import CommandRegistry

from torn_sdk.codegen.common import (
    CodegenError,
    OpenAPIDocument,
    PythonNames,
    ReviewRequired,
)
from torn_sdk.codegen.mock import (
    TornMockGenerator,
    TornMockGeneratorRunContext,
)
from torn_sdk.codegen.sdk import TornSDKGenerator
from torn_sdk.codegen.tests import TornTestGenerator


def _tags(values: list[str] | None) -> set[str] | None:
    if not values:
        return None
    return {PythonNames.snake(value) for value in values}


def _print_changes(
    *,
    root: Path,
    changes,
    show_unchanged: bool,
) -> None:
    statuses = {
        "create": "CREATE",
        "update": "UPDATE",
        "unchanged": "OK",
        "remove": "REMOVE",
        "scaffold": "SCAFFOLD",
    }

    for change in sorted(changes, key=lambda item: str(item.path)):
        if change.status == "unchanged" and not show_unchanged:
            continue

        try:
            display = change.path.relative_to(root)
        except ValueError:
            display = change.path

        print(
            f"{statuses.get(change.status, change.status.upper()):8} {display}"
        )


@dataclass(frozen=True)
class BaseGenerateInput:
    """Shared parsed options for every Torn SDK generation command."""

    openapi: Path
    tags: set[str] | None
    strict: bool
    skip_wrapper_check: bool
    report: bool
    report_file: Path | None
    check: bool

    @classmethod
    def _base_values(cls, values: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "openapi": Path(str(values.get("openapi") or "openapi.json")),
            "tags": _tags(values.get("tag")),
            "strict": bool(values.get("strict")),
            "skip_wrapper_check": bool(values.get("skip_wrapper_check")),
            "report": bool(values.get("report")),
            "report_file": (
                Path(str(values["report_file"]))
                if values.get("report_file")
                else None
            ),
            "check": bool(values.get("check")),
        }


@dataclass(frozen=True)
class GenerateSDKInput(BaseGenerateInput):
    """Parsed options for typed SDK source generation."""

    sdk_root: Path
    dry_run: bool
    prune: bool
    scaffold_resources: bool

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any]) -> "GenerateSDKInput":
        """Create typed SDK-generation input from Limen command values."""
        return cls(
            **cls._base_values(values),
            sdk_root=Path(str(values.get("sdk_root") or "src/torn_sdk")),
            dry_run=bool(values.get("dry_run")),
            prune=bool(values.get("prune")),
            scaffold_resources=bool(values.get("scaffold_resources")),
        )


@dataclass(frozen=True)
class GenerateMockInput(BaseGenerateInput):
    """Parsed options for network-free TornAPIWrapper mock generation."""

    output: Path

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any]) -> "GenerateMockInput":
        """Create mock-generation input from Limen command values."""
        return cls(
            **cls._base_values(values),
            output=Path(
                str(
                    values.get("output")
                    or "tests/generated/mock_torn_api_wrapper.py"
                )
            ),
        )


@dataclass(frozen=True)
class GenerateTestsInput(BaseGenerateInput):
    """Parsed options for generated pytest contract tests."""

    sdk_root: Path
    test_root: Path
    mock_module: str
    dry_run: bool
    prune: bool

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any]) -> "GenerateTestsInput":
        """Create test-generation input from Limen command values."""
        return cls(
            **cls._base_values(values),
            sdk_root=Path(str(values.get("sdk_root") or "src/torn_sdk")),
            test_root=Path(str(values.get("test_root") or "tests/generated")),
            mock_module=str(
                values.get("mock_module")
                or "tests.generated.mock_torn_api_wrapper"
            ),
            dry_run=bool(values.get("dry_run")),
            prune=bool(values.get("prune")),
        )


class GenerateSDKOperation:
    """Generate typed SDK models, resources, clients, and reports."""

    def execute(self, input_data: GenerateSDKInput) -> int:
        """Run SDK generation and return a CLI-compatible exit status."""
        document = OpenAPIDocument.load(input_data.openapi)
        generator = TornSDKGenerator(
            document,
            input_data.sdk_root,
            check=input_data.check,
            dry_run=input_data.dry_run,
            prune=input_data.prune,
            scaffold_resources=input_data.scaffold_resources,
            strict=input_data.strict,
            skip_wrapper_check=input_data.skip_wrapper_check,
        )

        try:
            plan, files = generator.generate(input_data.tags)
        except ReviewRequired as exc:
            print(f"REVIEW REQUIRED: {exc}", file=sys.stderr)
            return 2
        except CodegenError as exc:
            print(f"CODEGEN ERROR: {exc}", file=sys.stderr)
            return 3

        print(
            f"Torn OpenAPI {document.version} "
            f"({document.source_hash[:12]}) -> {input_data.sdk_root}"
        )

        report_content = None
        if input_data.report or input_data.report_file:
            report_content = generator.reports.render(plan)

        if input_data.report and report_content is not None:
            print()
            print(report_content, end="")

        if input_data.report_file and report_content is not None:
            exported = generator.report_exporter.export(
                input_data.report_file,
                report_content,
            )
            print(f"REPORT   {exported}")

        _print_changes(
            root=input_data.sdk_root,
            changes=files.changes,
            show_unchanged=input_data.report,
        )

        endpoint_count = sum(len(tag.endpoints) for tag in plan.tags)
        changed_count = sum(
            change.status != "unchanged" for change in files.changes
        )
        print(
            f"\n{len(plan.tags)} tag(s), {endpoint_count} endpoint(s), "
            f"{changed_count} file change(s)."
        )

        for warning in plan.warnings:
            print(f"WARNING: {warning}", file=sys.stderr)

        return 1 if input_data.check and files.dirty else 0


class GenerateMockOperation:
    """Generate the OpenAPI-backed TornAPIWrapper test double."""

    def execute(self, input_data: GenerateMockInput) -> int:
        """Run mock generation and return a CLI-compatible exit status."""
        try:
            document = OpenAPIDocument.load(input_data.openapi)
            generator = TornMockGenerator(
                document,
                wrapper_check=not input_data.skip_wrapper_check,
                strict=input_data.strict,
            )
            return generator.run(
                context=TornMockGeneratorRunContext(
                    output=input_data.output,
                    selected_tags=input_data.tags,
                    report=input_data.report,
                    report_file=input_data.report_file,
                    check=input_data.check,
                )
            )
        except ReviewRequired as exc:
            print(f"REVIEW REQUIRED: {exc}", file=sys.stderr)
            return 2
        except CodegenError as exc:
            print(f"CODEGEN ERROR: {exc}", file=sys.stderr)
            return 3


class GenerateTestsOperation:
    """Generate pytest contracts for the current typed SDK surface."""

    def execute(self, input_data: GenerateTestsInput) -> int:
        """Run test generation and return a CLI-compatible exit status."""
        try:
            document = OpenAPIDocument.load(input_data.openapi)
            generator = TornTestGenerator(
                document,
                sdk_root=input_data.sdk_root,
                test_root=input_data.test_root,
                mock_module=input_data.mock_module,
                strict=input_data.strict,
                skip_wrapper_check=input_data.skip_wrapper_check,
                check=input_data.check,
                dry_run=input_data.dry_run,
                prune=input_data.prune,
            )
            plan, files = generator.generate(input_data.tags)
        except ReviewRequired as exc:
            print(f"REVIEW REQUIRED: {exc}", file=sys.stderr)
            return 2
        except CodegenError as exc:
            print(f"CODEGEN ERROR: {exc}", file=sys.stderr)
            return 3

        report_content = None
        if input_data.report or input_data.report_file:
            report_content = generator.reports.render(plan)

        if input_data.report and report_content is not None:
            print(report_content, end="")

        if input_data.report_file and report_content is not None:
            exported = generator.report_exporter.export(
                input_data.report_file,
                report_content,
            )
            print(f"REPORT   {exported}")

        _print_changes(
            root=input_data.test_root,
            changes=files.changes,
            show_unchanged=input_data.report,
        )

        case_count = sum(len(tag.cases) for tag in plan.tags)
        changed_count = sum(
            change.status != "unchanged" for change in files.changes
        )
        print(
            f"\n{len(plan.tags)} tag(s), {case_count} route case(s), "
            f"{changed_count} file change(s)."
        )

        for warning in plan.warnings:
            print(f"WARNING: {warning}", file=sys.stderr)

        return 1 if input_data.check and files.dirty else 0


COMMON_ARGS = [
    ArgumentType(
        name="openapi",
        data_type=str,
        default="openapi.json",
        help_text="Path to Torn openapi.json.",
    ),
    ArgumentType(
        name="tag",
        data_type=str,
        nargs="+",
        default=None,
        help_text="Limit generation to one or more tags.",
    ),
    ArgumentType(
        name="strict",
        data_type=bool,
        help_text="Fail instead of skipping unsupported/ambiguous operations.",
    ),
    ArgumentType(
        name="skip_wrapper_check",
        data_type=bool,
        help_text="Skip TornAPIWrapper compatibility inspection.",
    ),
    ArgumentType(
        name="report",
        data_type=bool,
        help_text="Print a generation report.",
    ),
    ArgumentType(
        name="report_file",
        data_type=str,
        default=None,
        help_text="Write the generation report to a file.",
    ),
    ArgumentType(
        name="check",
        data_type=bool,
        help_text="Do not write; fail if generated output is stale.",
    ),
]


@CommandRegistry.implementation("generate")
class GenerateCommand(BaseCommand):
    """Parent command for all Torn SDK generation workflows."""

    is_group = True
    summary = "Generate SDK artifacts, mocks, or tests."


class BaseGenerateCommand(BaseCommand):
    """Abstract base configuration for generation subcommands."""

    abstract = True
    parent = "generate"


@CommandRegistry.implementation("generate_sdk")
class GenerateSDKCommand(BaseGenerateCommand):
    """Expose the typed SDK generator as ``torn-sdk generate sdk``."""

    abstract = False
    name = "sdk"
    summary = "Generate typed SDK models, resources, clients, and exports."
    input_class = GenerateSDKInput
    operation_class = GenerateSDKOperation
    args = [
        *COMMON_ARGS,
        ArgumentType(
            name="sdk_root",
            data_type=str,
            default="src/torn_sdk",
            help_text="Root Torn SDK package directory.",
        ),
        ArgumentType(
            name="dry_run",
            data_type=bool,
            help_text="Report intended writes without changing files.",
        ),
        ArgumentType(
            name="prune",
            data_type=bool,
            help_text="Remove stale machine-generated files.",
        ),
        ArgumentType(
            name="scaffold_resources",
            data_type=bool,
            help_text="Create missing thin public resource modules.",
        ),
    ]


@CommandRegistry.implementation("generate_mock")
class GenerateMockCommand(BaseGenerateCommand):
    """Expose mock generation as ``torn-sdk generate mock``."""

    abstract = False
    name = "mock"
    summary = "Generate the OpenAPI-backed TornAPIWrapper mock client."
    input_class = GenerateMockInput
    operation_class = GenerateMockOperation
    args = [
        *COMMON_ARGS,
        ArgumentType(
            name="output",
            data_type=str,
            default="tests/generated/mock_torn_api_wrapper.py",
            help_text="Generated mock module path.",
        ),
    ]


@CommandRegistry.implementation("generate_tests")
class GenerateTestsCommand(BaseGenerateCommand):
    """Expose test generation as ``torn-sdk generate tests``."""

    abstract = False
    name = "tests"
    summary = "Generate pytest contract tests against the generated mock."
    input_class = GenerateTestsInput
    operation_class = GenerateTestsOperation
    args = [
        *COMMON_ARGS,
        ArgumentType(
            name="sdk_root",
            data_type=str,
            default="src/torn_sdk",
            help_text="Root Torn SDK package directory.",
        ),
        ArgumentType(
            name="test_root",
            data_type=str,
            default="tests/generated",
            help_text="Directory for generated pytest modules.",
        ),
        ArgumentType(
            name="mock_module",
            data_type=str,
            default="tests.generated.mock_torn_api_wrapper",
            help_text="Import path of the generated mock module.",
        ),
        ArgumentType(
            name="dry_run",
            data_type=bool,
            help_text="Report intended writes without changing files.",
        ),
        ArgumentType(
            name="prune",
            data_type=bool,
            help_text="Remove stale generated test files.",
        ),
    ]
