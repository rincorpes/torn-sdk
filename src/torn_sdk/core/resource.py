from __future__ import annotations

from abc import ABC
from typing import Any, Callable, Generic, TypeVar, cast

from onomasticon import ImplementationRegistry

WrapperT = TypeVar("WrapperT")


class BaseResource(ABC, Generic[WrapperT]):
    def __init__(self, wrapper: WrapperT) -> None:
        self._wrapper = wrapper

    def _call_endpoint(
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
