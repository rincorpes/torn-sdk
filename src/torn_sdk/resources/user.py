from __future__ import annotations

from TornAPIWrapper import TornAPIWrapper
from TornAPIWrapper.endpoints.user import User

from torn_sdk.core.resource import Resource, ResourceRegistry
from torn_sdk.resources._generated.user import GeneratedUserResourceMixin


class UserResource(GeneratedUserResourceMixin, Resource[User]):
    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper.user)


ResourceRegistry.register("user", UserResource)
