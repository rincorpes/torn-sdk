from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.property import Property

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.property import GeneratedPropertyResourceMixin


class PropertyResource(GeneratedPropertyResourceMixin, Resource[Property]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.property)


ResourceRegistry.register('property', PropertyResource)
