# Code generation

Torn SDK has three generation workflows.

## SDK

```bash
torn-sdk generate sdk \
    --openapi openapi.json \
    --sdk-root src/torn_sdk \
    --scaffold-resources
```

This generates:

```text
models
generated resource mixins
resource exports
clients
shared literal types
```

## Mock

```bash
torn-sdk generate mock \
    --openapi openapi.json
```

The generated mock subclasses TornAPIWrapper but replaces the network request boundary.

It still exercises TornAPIWrapper's real endpoint methods and parameter conversion.

## Tests

```bash
torn-sdk generate tests \
    --openapi openapi.json \
    --sdk-root src/torn_sdk
```

Tests are generated only for endpoint variants supported by both:

```text
SDK generation plan
AND
mock/TornAPIWrapper plan
```

This prevents the test suite from pretending unsupported wrapper functionality exists.

## Generated files

Never directly edit files containing:

```text
AUTO-GENERATED
```

Make changes at the generator or override level and regenerate.

## Updating TornAPIWrapper

The SDK generator inspects TornAPIWrapper's synchronous and asynchronous
endpoint methods. Updating TornAPIWrapper can therefore change the generated
SDK surface even when the OpenAPI document is unchanged.

Use the same Python version as the generated-artifact CI job when updating the
wrapper. First inspect the installed and available versions:

```bash
python -c "from importlib.metadata import version; print(version('tornapiwrapper'))"
python -m pip index versions tornapiwrapper
```

Update the TornAPIWrapper requirement in `pyproject.toml`, refresh the lock
file, and recreate the development environment. Pin an exact wrapper version
when CI installs with `pip install` instead of consuming `poetry.lock`.

Then regenerate dependent artifacts in this order:

```bash
torn-sdk generate sdk \
    --openapi openapi.json \
    --sdk-root src/torn_sdk \
    --prune

torn-sdk generate mock \
    --openapi openapi.json

torn-sdk generate tests \
    --openapi openapi.json \
    --sdk-root src/torn_sdk \
    --test-root tests/generated \
    --prune
```

Review warnings and file removals before committing. A removed generated model
usually means the corresponding OpenAPI endpoint is no longer compatible with
both TornAPIWrapper client modes. Keep the removal only when that loss of typed
SDK support is intended; otherwise, fix the wrapper compatibility issue or add
an explicit SDK override and regenerate.

Finish by running the generated-artifact check and tests:

```bash
torn-sdk generate sdk \
    --openapi openapi.json \
    --sdk-root src/torn_sdk \
    --check

python -m pytest
```
