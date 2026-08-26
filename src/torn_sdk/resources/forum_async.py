from __future__ import annotations

from TornAPIWrapper import TornAPIWrapperAsync
from TornAPIWrapper.endpoints_async.forum import Forum

from torn_sdk.core.resource import AsyncResource, AsyncResourceRegistry
from torn_sdk.resources._generated.forum_async import (
    GeneratedAsyncForumResourceMixin,
)


class AsyncForumResource(
    GeneratedAsyncForumResourceMixin, AsyncResource[Forum]
):
    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper.forum)


AsyncResourceRegistry.register("forum", AsyncForumResource)
