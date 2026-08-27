"""
Endpoint specification module
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from pydantic import BaseModel

# Justification: Types should be PascalCase
# pylint: disable=invalid-name
ModelT = TypeVar("ModelT", bound=BaseModel)

Extractor = Callable[[Any], Any]

# pylint: enable=invalid-name


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
