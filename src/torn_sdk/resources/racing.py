from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.racing import Racing

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.racing import GeneratedRacingResourceMixin


class RacingResource(GeneratedRacingResourceMixin, Resource[Racing]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.racing)


ResourceRegistry.register('racing', RacingResource)
