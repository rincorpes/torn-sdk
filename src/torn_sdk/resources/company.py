from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.company import Company

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.company import GeneratedCompanyResourceMixin


class CompanyResource(GeneratedCompanyResourceMixin, Resource[Company]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.company)


ResourceRegistry.register("company", CompanyResource)
