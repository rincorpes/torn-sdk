"""
Endpoint decorators
"""

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

# Justification: Types should be PascalCase
# pylint: disable=invalid-name
ParamsT = ParamSpec("ParamsT")
ReturnT = TypeVar("ReturnT", bound=BaseModel)
# pylint: enable=invalid-name


class EndpointResource(Protocol):
    """
    Endpoint resource protocol for typed access without circular dependency
    """

    def call_endpoint(
        self,
        method: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Executes the method from the API transport

        Attrs:
            method (str): Name of the method to execute
            *args: List of positional arguments for the method
            **kwargs: Keyword arguments for the method
        """


# Justification: Endpoint spec builder by default should accept multiple arguments
# pylint: disable=too-many-arguments
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


# pylint: enable=too-many-arguments


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
    """
    Synchronous endpoint decorator

    Attrs:
        method (str | None): Class method name
        extract (str | None): key to extract from raw result
        extract_path (tuple[str, ...]): For recursive extraction
        extractor (Callable[[Any], Any]): Custom extraction function
        extract_default (bool): Returns the data as it is.

    Returns:
        Callable[[Callable[ParamsT, ReturnT]],Callable[ParamsT, ReturnT],]:
            The Client method
    """

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
            response = self.call_endpoint(
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
    """
    Asynchronous endpoint decorator

    Attrs:
        method (str | None): Class method name
        extract (str | None): key to extract from raw result
        extract_path (tuple[str, ...]): For recursive extraction
        extractor (Callable[[Any], Any]): Custom extraction function
        extract_default (bool): Returns the data as it is.

    Returns:
        Callable[[Callable[ParamsT, Awaitable[ReturnT]]],Callable[ParamsT, Awaitable[ReturnT]],]:
            The Client method
    """

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
                self.call_endpoint(
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
