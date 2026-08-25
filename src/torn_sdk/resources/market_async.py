from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.market import Market

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.market_async import GeneratedAsyncMarketResourceMixin


class AsyncMarketResource(GeneratedAsyncMarketResourceMixin, AsyncResource[Market]):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.market)


AsyncResourceRegistry.register('market', AsyncMarketResource)
