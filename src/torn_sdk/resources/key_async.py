from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.key import Key

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.key_async import (
    GeneratedAsyncKeyResourceMixin,
)


class AsyncKeyResource(GeneratedAsyncKeyResourceMixin, AsyncResource[Key]):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.key)


AsyncResourceRegistry.register("key", AsyncKeyResource)
