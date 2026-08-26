# Error handling

Torn SDK does not introduce a separate API error hierarchy.

API errors and wrapper-level failures come from TornAPIWrapper.

This is intentional.

TornAPIWrapper already owns Torn API communication, so defining a second error system inside Torn SDK would duplicate behavior and make applications harder to reason about.

## Torn API errors

TornAPIWrapper exposes an `APIError` base class and specific subclasses for Torn API error responses.

An application can therefore handle API failures at different levels:

```python
from TornAPIWrapper.errors import APIError

try:
    profile = torn.user.basic()
except APIError as exc:
    print(exc)
```

Or catch a more specific error when your application needs different behavior:

```python
from TornAPIWrapper.errors import (
    InvalidKey,
    PermissionDenied,
    RateLimit,
)

try:
    profile = torn.user.basic()
except InvalidKey:
    ...
except PermissionDenied:
    ...
except RateLimit:
    ...
```

## Validation errors

There is another category of failure that belongs to Torn SDK itself: response validation.

SDK responses are parsed into Pydantic models.

If Torn returns data incompatible with the generated OpenAPI model, Pydantic may raise a validation error.

That is useful information.

It can indicate:

* Torn changed a response
* the OpenAPI specification changed
* the SDK generator modeled something incorrectly
* a generated model is stale

If you encounter one of these consistently, please open an SDK issue with the endpoint and sanitized response shape.

Never include your API key in an issue.
