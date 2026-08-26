# Synchronous client

`TornClient` is the standard client for synchronous applications.

```python
from torn_sdk import TornClient

torn = TornClient("your-api-key")
```

Use its resource namespaces to make requests:

```python
profile = torn.user.profile()
faction = torn.faction.basic()
stocks = torn.torn.stocks()
```

Resource methods return typed Pydantic models.

## Request timeout

A request timeout can be configured when creating the client:

```python
torn = TornClient(
    "your-api-key",
    request_timeout=15,
)
```

The value is passed to TornAPIWrapper.

## Reusing a client

Create one client and reuse it across related requests rather than constructing a new client for every endpoint call.

```python
torn = TornClient("your-api-key")

profile = torn.user.basic()
cooldowns = torn.user.cooldowns()
money = torn.user.money()
```

This also keeps application code organized around a single Torn API dependency.
