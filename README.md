# Torn SDK for Python

A typed, resource-oriented Python SDK for the Torn API v2, built on top of **[TornAPIWrapper](https://github.com/cxdzc/TornAPIWrapper)**.

Torn SDK adds generated Pydantic models, typed endpoint signatures, editor autocomplete, resource-oriented clients, and OpenAPI-driven tooling while leaving HTTP transport and Torn API communication to TornAPIWrapper.

```python
from torn_sdk import TornClient

torn = TornClient("your-api-key")

profile = torn.user.basic()

print(profile.name)
print(profile.level)
```

## Why Torn SDK?

**TornAPIWrapper** already does the difficult work of communicating with the Torn API.

Torn SDK builds another layer on top of it for applications where developer experience and strong response types matter.

With Torn SDK you get:

* typed Pydantic response models
* IDE autocomplete for endpoints, parameters, and responses
* synchronous and asynchronous clients with the same API
* resource-oriented access such as `client.user`, `client.faction`, and `client.market`
* generated Python types for Torn enums and response structures
* direct access to **TornAPIWrapper** whenever you need the lower-level API
* OpenAPI-driven generation
* network-free OpenAPI mocks
* generated contract tests

The goal is not to replace **TornAPIWrapper**.

The projects solve different parts of the same problem:

```text
Your application
      │
      ▼
   Torn SDK
 typed resources
 Pydantic models
 autocomplete
      │
      ▼
TornAPIWrapper
 HTTP transport
 API parameters
 API errors
 sync / async
      │
      ▼
  Torn API v2
```

Improvements to **TornAPIWrapper** directly benefit Torn SDK.

## Requirements

* Python 3.13+
* A Torn API key with the permissions required by the endpoints you use

## Installation

```bash
python -m pip install torn-sdk
```

## Quick start

Create a client and use one of the Torn resource namespaces.

```python
from torn_sdk import TornClient

torn = TornClient("your-api-key")

user = torn.user.basic()

print(user.name)
print(user.level)
```

Many endpoints can also target another Torn entity when the API supports it:

```python
user = torn.user.basic(user_id=123456)

print(user.name)
```

Your editor can inspect the method signature and response model without requiring you to manually inspect dictionaries returned by the API.

## Resources

The client currently exposes the Torn API through these top-level resources:

```python
torn.user
torn.faction
torn.company
torn.market
torn.racing
torn.forum
torn.property
torn.key
torn.torn
```

Each resource contains the endpoints available through the current Torn OpenAPI specification and supported by TornAPIWrapper.

For example:

```python
profile = torn.user.profile()
faction = torn.faction.basic()
stocks = torn.torn.stocks()
market = torn.market.itemmarket(item_id=1)
```

Endpoint availability, API-key access levels, and returned data are ultimately controlled by Torn.

## Typed responses

Responses are Pydantic models rather than unstructured dictionaries.

```python
profile = torn.user.basic()

print(profile.name)
print(profile.level)

data = profile.model_dump()
```

Object responses inherit from `TornModel`.

List-root responses use `TornListModel` and expose the underlying list through both `root` and the convenience `items` property.

```python
records = torn.user.racingrecords()

for record in records.items:
    print(record)
```

Torn models allow additional fields so newly added API fields do not immediately break existing SDK versions.

## Async client

`AsyncTornClient` mirrors the synchronous resource layout.

```python
import asyncio

from torn_sdk import AsyncTornClient


async def main() -> None:
    async with AsyncTornClient("your-api-key") as torn:
        profile = await torn.user.basic()
        print(profile.name)


asyncio.run(main())
```

Using the client as an async context manager ensures the underlying TornAPIWrapper resources are closed correctly.

## Parameters and filters

SDK methods expose typed parameters based on Torn's OpenAPI specification while remaining compatible with TornAPIWrapper's Python API.

For example, your editor can show:

```python
results = torn.user.attacks(
    limit=100,
    sort="DESC",
)
```

Where **TornAPIWrapper** provides a Python-friendly name for an API parameter, Torn SDK follows the wrapper-facing name rather than leaking the raw query parameter into the public SDK.

Python keywords are also normalized where necessary, such as:

```python
from_=...
```

See `docs/guides/parameters-and-filters.md` for more details.

## Error handling

Torn SDK intentionally does not create a second competing API error hierarchy.

API and transport errors come from **TornAPIWrapper**.

This means applications already familiar with **TornAPIWrapper** can use the same error-handling strategy while gaining typed SDK responses.

See `docs/guides/errors.md`.

## Raw TornAPIWrapper access

Not every application needs to stay inside the typed surface all the time.

The underlying wrapper remains available through `raw`:

```python
from torn_sdk import TornClient

torn = TornClient("your-api-key")

response = torn.raw.user.get_cooldowns()
```

Use the typed resources as the normal application interface and `raw` as an escape hatch when:

* Torn adds something before the SDK has generated support for it
* **TornAPIWrapper** exposes functionality not yet modeled by the SDK
* you explicitly want the original dictionary response

## Documentation

The Sphinx documentation covers setup, typed sync and async clients, raw
wrapper access, models, code generation, and testing. Its API reference is
generated from `src/torn_sdk` whenever the docs are built, so route signatures
stay aligned with the SDK.

Build it locally with:

```bash
python -m pip install -e ".[docs]"
make -C docs html
```

Open `docs/_build/html/index.html` after the build. The source pages live in
[`docs/`](docs/).

## OpenAPI-driven development

A large part of Torn SDK is generated from Torn's OpenAPI specification.

The developer CLI currently provides three generation workflows:

```bash
torn-sdk generate sdk
torn-sdk generate mock
torn-sdk generate tests
```

These produce:

```text
OpenAPI
   │
   ├── typed models and resources
   ├── TornAPIWrapper-compatible mock
   └── pytest contract tests
```

Generated files contain an `AUTO-GENERATED` header and should not be edited manually.

If a generated model or endpoint is wrong, fix the generator, compatibility layer, or override responsible for it and regenerate.

## Testing

The generated contract tests do not make live requests to Torn.

They exercise:

```text
Torn SDK
   ↓
real TornAPIWrapper endpoint
   ↓
real TornAPIWrapper parameter handling
   ↓
mock request boundary
   ↓
OpenAPI-generated response
   ↓
Pydantic model
```

Run the suite with:

```bash
python -m pytest
```

Using `python -m pytest` is recommended so the test suite runs with the Python interpreter from your active environment.

## TornAPIWrapper

Torn SDK exists because TornAPIWrapper already provides a strong foundation for Torn API applications.

TornAPIWrapper remains responsible for low-level API communication, endpoint implementations, parameter handling, asynchronous transport, and API errors.

Torn SDK intentionally builds on that work rather than duplicating it.

If an issue belongs to the underlying Torn API request implementation, it may belong in TornAPIWrapper.

If it concerns generated models, SDK typing, resource ergonomics, parsing, code generation, or SDK tooling, it belongs here.

## Project status

Torn SDK is young and under active development.

The Torn API evolves continuously, so there may occasionally be a difference between:

```text
Torn OpenAPI
TornAPIWrapper
Torn SDK
```

The generator detects many of these differences and skips operations it cannot represent safely instead of guessing.

Bug reports and examples of real Torn applications are especially welcome.

## Contributing

Contributions are welcome.

Please read `[CONTRIBUTING.md](CONTRIBUTING.md)` before opening a pull request, particularly if your change affects generated models or resources.

## License

[MIT.](LICENSE)
