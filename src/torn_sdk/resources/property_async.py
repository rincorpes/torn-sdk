from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.property import Property

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.property_async import (
    GeneratedAsyncPropertyResourceMixin,
)


class AsyncPropertyResource(
    GeneratedAsyncPropertyResourceMixin, AsyncResource[Property]
):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.property)


AsyncResourceRegistry.register("property", AsyncPropertyResource)
