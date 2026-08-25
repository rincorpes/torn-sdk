from __future__ import annotations

from typing import Any

from .endpoint import EndpointSpec


class PayloadExtractor:
    @staticmethod
    def extract(response: Any, spec: EndpointSpec) -> Any:
        if spec.extractor:
            return spec.extractor(response)

        if spec.extract_path is not None:
            value = response
            for key in spec.extract_path:
                value = PayloadExtractor._get_value(value, key, spec)

            return value

        if spec.extract_key is not None:
            return PayloadExtractor._get_value(
                response,
                spec.extract_key,
                spec,
            )

        return response

    @staticmethod
    def _get_value(
        value: Any,
        key: str,
        spec: EndpointSpec,
    ) -> Any:
        if not isinstance(value, dict):
            raise TypeError(
                f"Cannot extract {key!r} for {spec.method!r}: "
                f"expected a dictionary, got {type(value).__name__}."
            )

        try:
            return value[key]
        except KeyError as error:
            available_keys = ", ".join(repr(item) for item in value)
            raise KeyError(
                f"Response for {spec.method!r} has no {key!r} payload key. "
                f"Available keys: {available_keys or '(none)'}."
            ) from error
