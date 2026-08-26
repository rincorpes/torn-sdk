from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.company import Company

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.company_async import (
    GeneratedAsyncCompanyResourceMixin,
)


class AsyncCompanyResource(
    GeneratedAsyncCompanyResourceMixin, AsyncResource[Company]
):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.company)


AsyncResourceRegistry.register("company", AsyncCompanyResource)
