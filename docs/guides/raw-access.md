# Raw TornAPIWrapper access

Torn SDK is designed to make the typed interface the normal application API.

It intentionally keeps TornAPIWrapper available as an escape hatch.

```python
from torn_sdk import TornClient

torn = TornClient("your-api-key")

response = torn.raw.user.get_cooldowns()
```

Use `raw` when:

* TornAPIWrapper supports something not yet represented by Torn SDK
* Torn has just changed an endpoint
* you need the original wrapper response
* you are debugging the typed parsing layer

Prefer:

```python
torn.user.cooldowns()
```

for normal application code.

Prefer:

```python
torn.raw.user.get_cooldowns()
```

when you explicitly need TornAPIWrapper behavior.

Raw access is not deprecated or considered a failure.

It is an intentional interoperability boundary between the two projects.
