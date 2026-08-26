from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.racing import Racing

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.racing_async import (
    GeneratedAsyncRacingResourceMixin,
)


class AsyncRacingResource(
    GeneratedAsyncRacingResourceMixin, AsyncResource[Racing]
):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.racing)


AsyncResourceRegistry.register("racing", AsyncRacingResource)
