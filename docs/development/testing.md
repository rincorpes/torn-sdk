# Testing

Generated contract tests make no live Torn API calls.

They exercise the complete stack down to TornAPIWrapper's request boundary.

```text
SDK resource
    ↓
SDK endpoint decorator
    ↓
real TornAPIWrapper endpoint
    ↓
real TornAPIWrapper parameter mapping
    ↓
mock request()
    ↓
OpenAPI-generated payload
    ↓
Pydantic model validation
```

Run tests using:

```bash
python -m pytest
```

Using `python -m pytest` rather than a globally installed `pytest` executable ensures tests run with the active project's Python interpreter.

Contract tests verify:

* the endpoint executes
* the declared Pydantic model is returned
* TornAPIWrapper calls the expected route
* required route parameters are sent
* parameters distinguishing alternate route variants are absent when appropriate
* sync and async clients behave consistently

A failing generated contract test is useful.

It usually tells us that one of these layers drifted:

```text
Torn OpenAPI
TornAPIWrapper
Torn SDK
```
