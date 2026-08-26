from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.key import Key

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.key import GeneratedKeyResourceMixin


class KeyResource(GeneratedKeyResourceMixin, Resource[Key]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.key)


ResourceRegistry.register("key", KeyResource)
