from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.user import User

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.user_async import (
    GeneratedAsyncUserResourceMixin,
)


class AsyncUserResource(GeneratedAsyncUserResourceMixin, AsyncResource[User]):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.user)


AsyncResourceRegistry.register("user", AsyncUserResource)
