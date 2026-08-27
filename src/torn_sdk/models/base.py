"""Base Pydantic models used by all generated Torn API response types."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, RootModel


class TornModel(BaseModel):
    """Base model for generated Torn API object responses.

    Extra response fields are retained to keep clients resilient to additive API
    changes while preserving explicit types for documented fields.
    """

    model_config = ConfigDict(
        extra="allow",
    )


ItemT = TypeVar("ItemT", bound=TornModel)


class TornListModel(
    RootModel[list[ItemT]],
    Generic[ItemT],
):
    """Base model for Torn API responses whose root value is a list.

    Attributes:
        items: The generated model instances contained in the response.
    """

    @property
    def items(self) -> list[ItemT]:
        """Return the list held by Pydantic's root model."""
        return self.root
