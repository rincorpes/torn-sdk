from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.faction import Faction

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.faction_async import (
    GeneratedAsyncFactionResourceMixin,
)


class AsyncFactionResource(
    GeneratedAsyncFactionResourceMixin, AsyncResource[Faction]
):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.faction)


AsyncResourceRegistry.register("faction", AsyncFactionResource)
