from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.torn import Torn

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.torn import GeneratedTornResourceMixin


class TornResource(GeneratedTornResourceMixin, Resource[Torn]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.torn)


ResourceRegistry.register('torn', TornResource)
