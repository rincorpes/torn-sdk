# Parameters and filters

Torn SDK's public method signatures are generated from two sources:

```text
Torn OpenAPI
+
TornAPIWrapper
```

OpenAPI describes the Torn API contract.

TornAPIWrapper determines how that contract is actually exposed through Python.

This distinction matters because wrapper-friendly Python names are sometimes different from the raw Torn API parameter.

For example, an API parameter such as:

```text
filters
```

may be represented by TornAPIWrapper as a more descriptive Python parameter.

Torn SDK follows the Python-facing TornAPIWrapper name while retaining the OpenAPI type information.

## IDs

Endpoints that support both the authenticated entity and a specific entity commonly use an optional ID:

```python
current = torn.user.basic()

other = torn.user.basic(
    user_id=123456,
)
```

For another resource this may instead be:

```python
faction_id=...
item_id=...
listing_id=...
```

The goal is to avoid a large number of ambiguous parameters all named simply `id`.

## Python keywords

Some Torn parameters are Python keywords.

Those are normalized:

```python
from_=1234567890
```

instead of the invalid:

```python
from=1234567890
```

## Defaults

The SDK preserves Torn/OpenAPI defaults where they can be represented safely.

For example, limits, sorting direction, or `striptags` values may already have defaults in the Python signature.

Do not assume all Torn endpoints have the same limit or sorting behavior.

Your editor's method signature is the best source for the SDK-facing call.

The official Torn API documentation remains the source of truth for the API's actual behavior.

## Typed values

Where Torn exposes a finite set of valid values, the generator creates Python literal types.

This improves autocomplete and helps type checkers identify invalid calls before they reach Torn.
