# Torn SDK for Python

**A typed, ergonomic Python client for the [Torn API](https://www.torn.com/api.html).**

Torn SDK turns Torn's OpenAPI surface into discoverable Python resources,
typed response models, and matching synchronous and asynchronous clients. It is
built for applications that want the convenience of an SDK without giving up
access to the underlying `TornAPIWrapper` when an endpoint needs something
more direct.

```python
from torn_sdk import TornClient

client = TornClient("your-api-key")
cooldowns = client.user.cooldowns()

print(cooldowns.drug)
print(cooldowns.booster)
```

## Why Torn SDK?

- **Typed API responses** for better editor support and earlier feedback.
- **Resource-oriented clients** for Torn domains including `user`, `faction`,
  `company`, `market`, `racing`, `forum`, `property`, `key`, and `torn`.
- **Sync and async support** with the same resource layout.
- **Raw escape hatch** when you need direct `TornAPIWrapper` access.
- **OpenAPI-driven generation** to keep the SDK, test doubles, and contract
  tests aligned with the published API.

## Requirements

- Python 3.13 or newer
- A valid Torn API key with the permissions required by the endpoints you use

## Install

Install the package from a local checkout while the package is under active
development:

```bash
python -m pip install -e .
```

Or, with Poetry:

```bash
poetry install
```

## Quick Start

Create a client with your Torn API key, then call methods on a resource.
Response types are generated from the OpenAPI specification.

```python
from torn_sdk import TornClient

client = TornClient("your-api-key", request_timeout=15)

profile = client.user.profile()
print(profile.name)

faction = client.faction.basic()
print(faction.name)
```

Available top-level resources are:

```python
client.user
client.faction
client.company
client.market
client.racing
client.forum
client.property
client.key
client.torn
```

Endpoint availability and required API-key permissions are defined by Torn.
Use the Torn API documentation to determine which key access level an endpoint
requires.

## Async Usage

`AsyncTornClient` mirrors the synchronous client. It supports `async with` and
closes its underlying HTTP resources automatically.

```python
import asyncio

from torn_sdk import AsyncTornClient


async def main() -> None:
    async with AsyncTornClient("your-api-key") as client:
        cooldowns = await client.user.cooldowns()
        print(cooldowns.drug)


asyncio.run(main())
```

## Raw API Access

The typed SDK is the preferred interface, but the wrapper remains available
through `raw` for endpoints or options not yet represented in the generated
surface.

```python
from torn_sdk import TornClient

client = TornClient("your-api-key")
response = client.raw.user.get_cooldowns()
```

Raw responses follow `TornAPIWrapper` semantics. Treat this interface as lower
level than the typed resource methods.

## Regenerating the SDK

The repository contains a developer CLI named `torn-sdk`. It generates typed
models, resource mixins, clients, exports, a network-free mock wrapper, and
pytest contract tests from an OpenAPI document.

Download or provide `openapi.json`, then run:

```bash
torn-sdk generate sdk \
  --openapi openapi.json \
  --sdk-root src/torn_sdk \
  --scaffold-resources \
  --report-file .local/reports/sdk.txt
```

Useful companion commands:

```bash
# Generate a deterministic TornAPIWrapper test double.
torn-sdk generate mock --openapi openapi.json

# Generate contract tests against that mock.
torn-sdk generate tests --openapi openapi.json --sdk-root src/torn_sdk

# Check whether generated output is current without writing files.
torn-sdk generate sdk --openapi openapi.json --sdk-root src/torn_sdk --check
```

Use `--tag user faction` to limit generation to specific OpenAPI tags. Add
`--strict` to fail when an operation cannot be safely represented, rather than
skipping it with a warning.

Generated files include an `AUTO-GENERATED` header. Do not edit them manually;
make the change in the generator or the OpenAPI input and regenerate instead.

## Development

Run the test suite from this directory:

```bash
pytest
```

The generated contract tests run against a local mock, so they do not make
live Torn API requests. Keep changes focused, regenerate affected artifacts,
and run tests before opening a pull request.

## Project Status

Torn SDK is actively developed alongside the evolving Torn OpenAPI
specification. The generated surface is broad, but Torn can add or adjust
endpoints at any time. If an endpoint is missing or ambiguous, use `raw` as a
temporary bridge and open an issue with the relevant OpenAPI detail.

## License

See [LICENSE](LICENSE).
