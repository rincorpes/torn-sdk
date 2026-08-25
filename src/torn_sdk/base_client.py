from __future__ import annotations

from typing import Any, Generic, TypeVar

WrapperT = TypeVar("WrapperT")
RawT = TypeVar("RawT")


class BaseTornClient(Generic[WrapperT, RawT]):
    raw: RawT

    def __init__(
        self,
        wrapper: WrapperT,
        raw: RawT,
    ) -> None:
        self._wrapper = wrapper
        self.raw = raw

    def _load_resources(
        self,
        implementations: dict[str, type[Any]],
    ) -> None:
        for name, resource_type in implementations.items():
            if hasattr(self, name):
                continue

            setattr(
                self,
                name,
                resource_type(self._wrapper),
            )
