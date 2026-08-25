from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.torn import Torn

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.torn_async import GeneratedAsyncTornResourceMixin


class AsyncTornResource(GeneratedAsyncTornResourceMixin, AsyncResource[Torn]):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.torn)


AsyncResourceRegistry.register('torn', AsyncTornResource)
