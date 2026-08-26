"""
Torn SDK Base resource classes and registry
"""

from __future__ import annotations

from abc import ABC
from typing import Any, Callable, Generic, TypeVar, cast

from onomasticon import ImplementationRegistry  # pylint: disable=import-error

# Justification: Types should be PascalCase
# pylint: disable=invalid-name
WrapperT = TypeVar("WrapperT")


class BaseResource(ABC, Generic[WrapperT]):
    def __init__(self, wrapper: WrapperT) -> None:
        self._wrapper = wrapper

    def call_endpoint(
        self,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        wrapper_call = cast(
            Callable[..., Any],
            getattr(self._wrapper, method),
        )
        return wrapper_call(*args, **kwargs)


class Resource(BaseResource[WrapperT]): ...


class AsyncResource(BaseResource[WrapperT]): ...


class ResourceRegistry(ImplementationRegistry[Resource]):
    implementation_base = Resource


class AsyncResourceRegistry(ImplementationRegistry[AsyncResource]):
    implementation_base = AsyncResource
