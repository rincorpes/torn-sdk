# Contributing to Torn SDK

Thanks for helping improve Torn SDK.

Torn SDK is built on top of **[TornAPIWrapper](https://github.com/cxdzc/TornAPIWrapper)** and generated primarily from Torn's OpenAPI specification, so the most important part of contributing is identifying **which layer owns the problem**.

## Before opening an issue

Ask where the problem lives.

### TornAPIWrapper

A change probably belongs in TornAPIWrapper when it concerns:

* HTTP requests
* Torn API authentication
* request sessions
* endpoint transport
* API error handling
* TornAPIWrapper parameter conversion
* an endpoint missing entirely from TornAPIWrapper

### Torn SDK

A change belongs here when it concerns:

* generated response models
* incorrect Pydantic types
* resource method signatures
* SDK naming
* response extraction
* response parsing
* OpenAPI generation
* mock generation
* generated contract tests
* developer experience

Sometimes a Torn API change requires work in both projects.

That's okay.

The goal is to preserve the boundary rather than duplicate TornAPIWrapper inside Torn SDK.

## Development setup

Clone the repository and create a Python 3.13+ environment.

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev,docs]"
```

Run the tests:

```bash
python -m pytest
```

## Generated code

A large portion of Torn SDK is generated.

Files beginning with:

```text
AUTO-GENERATED
```

must not be edited directly.

Changes to generated output should normally be implemented in:

```text
src/torn_sdk/codegen/
```

or in the Torn-specific override layer.

Then regenerate the affected files.

## Regeneration workflow

For a complete regeneration:

```bash
torn-sdk generate sdk \
    --openapi openapi.json \
    --sdk-root src/torn_sdk \
    --scaffold-resources

torn-sdk generate mock \
    --openapi openapi.json

torn-sdk generate tests \
    --openapi openapi.json \
    --sdk-root src/torn_sdk
```

Then run:

```bash
python -m pytest
```

You can limit generation while developing:

```bash
torn-sdk generate sdk --tag User
```

Before submitting a PR, verify the complete generated surface when your change affects shared generator behavior.

## Code quality

Before opening a pull request, run the relevant project checks.

At minimum:

```bash
python -m pytest
```

For Python changes, also run the configured formatting, linting, and type-checking tools where applicable.

## Pull requests

Keep pull requests focused.

A good pull request explains:

1. what Torn/API behavior caused the change
2. whether TornAPIWrapper is involved
3. what SDK behavior changes
4. whether generated files changed
5. how the change was tested

For code-generation changes, include an example of the generated output before and after when that makes the change easier to review.

## API keys and private data

Never commit or publish:

* Torn API keys
* private API responses
* player information that should not be public
* credentials from local configuration

Examples and tests should use fake values or the generated network-free mock client.

## TornAPIWrapper Acknowledgement

Please be respectful of the separation between the two projects.

Torn SDK intentionally depends on TornAPIWrapper rather than replacing its transport layer.

When an improvement belongs upstream, contributing it to TornAPIWrapper is better than duplicating the implementation here.

That keeps both projects useful and allows Torn SDK to benefit from improvements made by the wider Torn developer community.
