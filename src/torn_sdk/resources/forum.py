from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.forum import Forum

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.forum import GeneratedForumResourceMixin


class ForumResource(GeneratedForumResourceMixin, Resource[Forum]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.forum)


ResourceRegistry.register("forum", ForumResource)
