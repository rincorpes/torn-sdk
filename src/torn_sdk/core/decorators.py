from __future__ import annotations

from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    ParamSpec,
    Protocol,
    TypeVar,
    cast,
    get_type_hints,
)

from pydantic import BaseModel

from .endpoint import EndpointSpec
from .parser import ResponseParser

ParamsT = ParamSpec("ParamsT")
ReturnT = TypeVar("ReturnT", bound=BaseModel)


class EndpointResource(Protocol):
    def _call_endpoint(
        self,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any: ...


def _build_endpoint_spec(
    func: Callable[..., Any],
    *,
    method: str | None,
    extract: str | None,
    extract_path: tuple[str, ...] | None,
    extractor: Callable[[Any], Any] | None,
    extract_default: bool,
) -> EndpointSpec:
    sdk_method_name = func.__name__
    wrapper_method_name = method or f"get_{sdk_method_name}"

    model = cast(
        type[BaseModel],
        get_type_hints(func)["return"],
    )

    extract_key = extract

    if (
        extract_key is None
        and extract_path is None
        and extractor is None
        and extract_default
    ):
        extract_key = sdk_method_name

    return EndpointSpec(
        method=wrapper_method_name,
        model=model,
        extract_key=extract_key,
        extract_path=extract_path,
        extractor=extractor,
    )


def endpoint(
    *,
    method: str | None = None,
    extract: str | None = None,
    extract_path: tuple[str, ...] | None = None,
    extractor: Callable[[Any], Any] | None = None,
    extract_default: bool = True,
) -> Callable[
    [Callable[ParamsT, ReturnT]],
    Callable[ParamsT, ReturnT],
]:
    def decorator(
        func: Callable[ParamsT, ReturnT],
    ) -> Callable[ParamsT, ReturnT]:
        spec = _build_endpoint_spec(
            func,
            method=method,
            extract=extract,
            extract_path=extract_path,
            extractor=extractor,
            extract_default=extract_default,
        )

        @wraps(func)
        def wrapped(
            self: EndpointResource,
            *args: Any,
            **kwargs: Any,
        ) -> ReturnT:
            response = self._call_endpoint(
                spec.method,
                *args,
                **kwargs,
            )

            return cast(
                ReturnT,
                ResponseParser.parse(response, spec),
            )

        return cast(Callable[ParamsT, ReturnT], wrapped)

    return decorator


def async_endpoint(
    *,
    method: str | None = None,
    extract: str | None = None,
    extract_path: tuple[str, ...] | None = None,
    extractor: Callable[[Any], Any] | None = None,
    extract_default: bool = True,
) -> Callable[
    [Callable[ParamsT, Awaitable[ReturnT]]],
    Callable[ParamsT, Awaitable[ReturnT]],
]:
    def decorator(
        func: Callable[ParamsT, Awaitable[ReturnT]],
    ) -> Callable[ParamsT, Awaitable[ReturnT]]:
        spec = _build_endpoint_spec(
            func,
            method=method,
            extract=extract,
            extract_path=extract_path,
            extractor=extractor,
            extract_default=extract_default,
        )

        @wraps(func)
        async def wrapped(
            self: EndpointResource,
            *args: Any,
            **kwargs: Any,
        ) -> ReturnT:
            response = await cast(
                Awaitable[Any],
                self._call_endpoint(
                    spec.method,
                    *args,
                    **kwargs,
                ),
            )

            return cast(
                ReturnT,
                ResponseParser.parse(response, spec),
            )

        return cast(
            Callable[ParamsT, Awaitable[ReturnT]],
            wrapped,
        )

    return decorator
