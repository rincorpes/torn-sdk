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
