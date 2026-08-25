from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, RootModel


class TornModel(BaseModel):
    """Base model for Torn API object responses."""

    model_config = ConfigDict(
        extra="allow",
    )


ItemT = TypeVar("ItemT", bound=TornModel)


class TornListModel(
    RootModel[list[ItemT]],
    Generic[ItemT],
):
    """Base model for Torn API responses whose root value is a list."""

    @property
    def items(self) -> list[ItemT]:
        return self.root
