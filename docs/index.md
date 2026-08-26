# Torn SDK

Torn SDK is a typed Python SDK for Torn API v2. It layers generated Pydantic
models and resource-oriented clients on top of TornAPIWrapper, which remains
responsible for HTTP communication, parameter conversion, and Torn API errors.

```{toctree}
:hidden:
:maxdepth: 2
:caption: Documentation

getting-started
guides/sync
guides/async
guides/parameters-and-filters
guides/errors
guides/raw-access
concepts/models
concepts/architecture
development/code-generation
development/testing
api/modules
```

Start with [Getting started](getting-started.md) to make a typed request, or
visit the generated API reference for the exact routes and signatures in this
SDK version. Torn's official API documentation remains the source of truth for
endpoint permissions, API-key access levels, and API semantics.
