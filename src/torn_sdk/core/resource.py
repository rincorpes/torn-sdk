"""Base resource adapters and implementation registries for Torn SDK."""

from __future__ import annotations

from abc import ABC
from typing import Any, Callable, Generic, TypeVar, cast

from onomasticon import ImplementationRegistry  # pylint: disable=import-error

# Justification: Types should be PascalCase
# pylint: disable=invalid-name
WrapperT = TypeVar("WrapperT")


class BaseResource(ABC, Generic[WrapperT]):
    """Base adapter that delegates SDK endpoint calls to TornAPIWrapper."""

    def __init__(self, wrapper: WrapperT) -> None:
        """Create a resource bound to one TornAPIWrapper endpoint namespace."""
        self._wrapper = wrapper

    def call_endpoint(
        self,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Call a named method on the wrapped TornAPIWrapper namespace.

        Args:
            method: Wrapper method to invoke.
            *args: Positional arguments forwarded to the wrapper method.
            **kwargs: Keyword arguments forwarded to the wrapper method.

        Returns:
            The unparsed wrapper response.
        """
        wrapper_call = cast(
            Callable[..., Any],
            getattr(self._wrapper, method),
        )
        return wrapper_call(*args, **kwargs)


class Resource(BaseResource[WrapperT]):
    """Synchronous resource base class."""


class AsyncResource(BaseResource[WrapperT]):
    """Asynchronous resource base class."""


class ResourceRegistry(ImplementationRegistry[Resource]):
    """Registry of synchronous public SDK resources."""

    implementation_base = Resource


class AsyncResourceRegistry(ImplementationRegistry[AsyncResource]):
    """Registry of asynchronous public SDK resources."""

    implementation_base = AsyncResource
