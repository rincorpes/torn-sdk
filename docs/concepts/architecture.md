# Architecture

Torn SDK deliberately separates transport from SDK ergonomics.

```text
Application
    │
    ▼
TornClient / AsyncTornClient
    │
    ▼
Typed resource
    │
    ▼
Endpoint decorator
    │
    ▼
TornAPIWrapper resource
    │
    ▼
TornAPIWrapper transport
    │
    ▼
Torn API
```

## TornAPIWrapper owns

* HTTP communication
* synchronous and asynchronous transport
* Torn endpoint implementations
* wrapper parameter conversion
* API error handling

## Torn SDK owns

* typed public resource methods
* Pydantic response models
* response extraction and parsing
* OpenAPI interpretation
* developer-facing names and typing
* SDK code generation
* network-free mocks
* generated contract tests

Keeping this boundary explicit prevents Torn SDK from becoming a competing HTTP wrapper.
