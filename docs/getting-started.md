# Getting started

## Installation

Torn SDK requires Python 3.13 or newer.

```bash
python -m pip install torn-sdk
```

You will also need a Torn API key.

The API key's access level determines which Torn endpoints you can use.

## Create a client

```python
from torn_sdk import TornClient

torn = TornClient("your-api-key")
```

Resources are grouped by Torn API domain:

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

## Make your first request

```python
profile = torn.user.basic()

print(profile.name)
print(profile.level)
```

Unlike a lower-level API wrapper, `profile` is a Pydantic model.

That means editors and type checkers know which attributes are expected on the response.

## Query another player

Where Torn supports an ID-based variant, the corresponding resource method exposes it:

```python
profile = torn.user.basic(user_id=123456)
```

The same method can therefore represent both:

```text
current authenticated user
specific user
```

when Torn and TornAPIWrapper support both forms.

## Inspect the result

Pydantic APIs are available on response models:

```python
data = profile.model_dump()
json_data = profile.model_dump_json()
```

## Next

Read [Sync client](guides/sync.md), [Parameters and filters](guides/parameters-and-filters.md), and [Response models](concepts/models.md).
