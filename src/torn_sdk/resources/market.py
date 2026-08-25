from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.market import Market

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.market import GeneratedMarketResourceMixin


class MarketResource(GeneratedMarketResourceMixin, Resource[Market]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.market)


ResourceRegistry.register('market', MarketResource)
