from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)

Extractor = Callable[[Any], Any]


@dataclass(frozen=True, slots=True)
class EndpointSpec(Generic[ModelT]):
    method: str
    model: type[ModelT]
    extract_key: str | None = None
    extract_path: tuple[str, ...] | None = None
    extractor: Extractor | None = None
