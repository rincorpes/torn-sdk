from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.faction import Faction

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.faction import GeneratedFactionResourceMixin


class FactionResource(GeneratedFactionResourceMixin, Resource[Faction]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.faction)


ResourceRegistry.register("faction", FactionResource)
