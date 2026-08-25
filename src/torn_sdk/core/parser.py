from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

from .endpoint import EndpointSpec
from .extraction import PayloadExtractor

ModelT = TypeVar("ModelT", bound=BaseModel)


class ResponseParser:

    @staticmethod
    def parse(
        response: Any,
        spec: EndpointSpec[ModelT],
    ) -> ModelT:
        payload = PayloadExtractor.extract(response, spec)
        return spec.model.model_validate(payload)
