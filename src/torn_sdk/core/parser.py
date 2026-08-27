"""Parse Torn API payloads into the generated Pydantic response models."""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from .endpoint import EndpointSpec
from .extraction import PayloadExtractor

# Justification: Types should be PascalCase
# pylint: disable=invalid-name
ModelT = TypeVar("ModelT", bound=BaseModel)

# pylint: enable=invalid-name


class ResponseParser:
    """Convert extracted API payloads into the model required by an endpoint."""

    @staticmethod
    def parse(
        response: Any,
        spec: EndpointSpec[ModelT],
    ) -> ModelT:
        """Extract an endpoint payload and validate it as the target model.

        Args:
            response: Raw payload returned by TornAPIWrapper.
            spec: Endpoint extraction and model-validation contract.

        Returns:
            The validated generated response model.
        """
        payload = PayloadExtractor.extract(response, spec)
        return spec.model.model_validate(payload)
