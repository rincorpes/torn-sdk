# Asynchronous client

Use `AsyncTornClient` when your application already runs an asyncio event loop or needs to perform concurrent I/O.

```python
import asyncio

from torn_sdk import AsyncTornClient


async def main() -> None:
    async with AsyncTornClient("your-api-key") as torn:
        profile = await torn.user.basic()
        print(profile.name)


asyncio.run(main())
```

The async client mirrors the sync client:

```text
TornClient.user
AsyncTornClient.user

TornClient.faction
AsyncTornClient.faction
```

and so on.

The response models are the same.

Only the request execution is asynchronous.

## Prefer the context manager

Use:

```python
async with AsyncTornClient(...) as torn:
    ...
```

when possible.

This ensures TornAPIWrapper's underlying asynchronous HTTP resources are closed.

If you manage the client manually:

```python
torn = AsyncTornClient("your-api-key")

try:
    profile = await torn.user.basic()
finally:
    await torn.close()
```
