"""
Endpoint specification module
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)

Extractor = Callable[[Any], Any]


@dataclass(frozen=True, slots=True)
class EndpointSpec(Generic[ModelT]):
    """
    Endpoint spec class

    Attributes:
        method (str): method name
        model (type[ModelT]): Model class
        extract_key (str | None): The key to extract
        extract_path (tuple[str, ...] | None): For recursive extraction
        extractor (Extractor): Custom extraction function
    """

    method: str
    model: type[ModelT]
    extract_key: str | None = None
    extract_path: tuple[str, ...] | None = None
    extractor: Extractor | None = None
