# Response models

Torn SDK converts supported Torn API responses into Pydantic models.

Most object responses derive from `TornModel`.

```python
profile = torn.user.basic()

print(profile.name)
```

You can use normal Pydantic functionality:

```python
profile.model_dump()
profile.model_dump_json()
```

## Forward compatibility

`TornModel` allows additional fields.

This means Torn can add a response field without immediately causing every existing SDK version to reject the response.

Known fields remain typed while new fields can still pass through until the SDK is regenerated.

## List responses

Some Torn endpoints return a list as the root response.

Those models derive from `TornListModel`.

They provide:

```python
response.root
```

and the convenience property:

```python
response.items
```

Example:

```python
records = torn.user.racingrecords()

for record in records.items:
    print(record)
```

## Generated models

Files marked:

```text
AUTO-GENERATED
```

must not be edited manually.

If a model is incorrect, fix the OpenAPI interpretation, generator behavior, or explicit Torn override and regenerate.
