from __future__ import annotations

from builtins import property as builtin_property
from typing import Generic, Protocol, TypeVar

from TornAPIWrapper import TornAPIWrapper, TornAPIWrapperAsync
from TornAPIWrapper.endpoints.company import Company
from TornAPIWrapper.endpoints.faction import Faction
from TornAPIWrapper.endpoints.forum import Forum
from TornAPIWrapper.endpoints.key import Key
from TornAPIWrapper.endpoints.market import Market
from TornAPIWrapper.endpoints.property import Property
from TornAPIWrapper.endpoints.racing import Racing
from TornAPIWrapper.endpoints.torn import Torn
from TornAPIWrapper.endpoints.user import User
from TornAPIWrapper.endpoints_async.company import Company as AsyncCompany
from TornAPIWrapper.endpoints_async.faction import Faction as AsyncFaction
from TornAPIWrapper.endpoints_async.forum import Forum as AsyncForum
from TornAPIWrapper.endpoints_async.key import Key as AsyncKey
from TornAPIWrapper.endpoints_async.market import Market as AsyncMarket
from TornAPIWrapper.endpoints_async.property import Property as AsyncProperty
from TornAPIWrapper.endpoints_async.racing import Racing as AsyncRacing
from TornAPIWrapper.endpoints_async.torn import Torn as AsyncTorn
from TornAPIWrapper.endpoints_async.user import User as AsyncUser

UserT = TypeVar("UserT", covariant=True)
FactionT = TypeVar("FactionT", covariant=True)
CompanyT = TypeVar("CompanyT", covariant=True)
MarketT = TypeVar("MarketT", covariant=True)
RacingT = TypeVar("RacingT", covariant=True)
ForumT = TypeVar("ForumT", covariant=True)
PropertyT = TypeVar("PropertyT", covariant=True)
KeyT = TypeVar("KeyT", covariant=True)
TornT = TypeVar("TornT", covariant=True)


class NamespaceWrapper(
    Protocol[
        UserT,
        FactionT,
        CompanyT,
        MarketT,
        RacingT,
        ForumT,
        PropertyT,
        KeyT,
        TornT,
    ],
):
    @builtin_property
    def user(self) -> UserT: ...

    @builtin_property
    def faction(self) -> FactionT: ...

    @builtin_property
    def company(self) -> CompanyT: ...

    @builtin_property
    def market(self) -> MarketT: ...

    @builtin_property
    def racing(self) -> RacingT: ...

    @builtin_property
    def forum(self) -> ForumT: ...

    @builtin_property
    def property(self) -> PropertyT: ...

    @builtin_property
    def key(self) -> KeyT: ...

    @builtin_property
    def torn(self) -> TornT: ...


class BaseNamespace(
    Generic[
        UserT,
        FactionT,
        CompanyT,
        MarketT,
        RacingT,
        ForumT,
        PropertyT,
        KeyT,
        TornT,
    ],
):
    def __init__(
        self,
        wrapper: NamespaceWrapper[
            UserT,
            FactionT,
            CompanyT,
            MarketT,
            RacingT,
            ForumT,
            PropertyT,
            KeyT,
            TornT,
        ],
    ) -> None:
        self._wrapper = wrapper

    @builtin_property
    def user(self) -> UserT:
        return self._wrapper.user

    @builtin_property
    def faction(self) -> FactionT:
        return self._wrapper.faction

    @builtin_property
    def company(self) -> CompanyT:
        return self._wrapper.company

    @builtin_property
    def market(self) -> MarketT:
        return self._wrapper.market

    @builtin_property
    def racing(self) -> RacingT:
        return self._wrapper.racing

    @builtin_property
    def forum(self) -> ForumT:
        return self._wrapper.forum

    @builtin_property
    def property(self) -> PropertyT:
        return self._wrapper.property

    @builtin_property
    def key(self) -> KeyT:
        return self._wrapper.key

    @builtin_property
    def torn(self) -> TornT:
        return self._wrapper.torn


class RawNamespace(
    BaseNamespace[
        User, Faction, Company, Market, Racing, Forum, Property, Key, Torn
    ]
):
    """Typed access to the underlying synchronous TornAPIWrapper resources."""

    def __init__(self, wrapper: TornAPIWrapper) -> None:
        super().__init__(wrapper)


class AsyncRawNamespace(
    BaseNamespace[
        AsyncUser,
        AsyncFaction,
        AsyncCompany,
        AsyncMarket,
        AsyncRacing,
        AsyncForum,
        AsyncProperty,
        AsyncKey,
        AsyncTorn,
    ],
):
    """Typed access to the asynchronous TornAPIWrapper resources."""

    def __init__(self, wrapper: TornAPIWrapperAsync) -> None:
        super().__init__(wrapper)
