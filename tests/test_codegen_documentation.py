from torn_sdk.codegen.sdk import (
    GENERATED_HEADER,
    EndpointIR,
    ExtractionIR,
    ResourceMixinRenderer,
    ResponsePlan,
    TagIR,
)


def test_resource_renderer_emits_openapi_documentation() -> None:
    endpoint = EndpointIR(
        tag="user",
        name="basic",
        source_paths=("/user/basic",),
        operation_ids=("getMyBasicInformation",),
        parameters=(),
        response=ResponsePlan(
            response_component=None,
            source_schema={},
            model_schema={},
            model_source_component=None,
            public_model_name="UserBasic",
            extraction=ExtractionIR(kind="key", key="profile"),
        ),
        wrapper_method="get_basic",
        documentation="Get your basic profile information.",
    )

    source = ResourceMixinRenderer(async_mode=False).render(
        TagIR(name="user", endpoints=(endpoint,))
    )

    assert source.startswith(
        '"""Typed user resource mixins generated from the Torn OpenAPI specification."""\n'
        "# <torn-sdk:custom-header>\n"
        "# </torn-sdk:custom-header>\n"
        f"{GENERATED_HEADER}\n"
    )
    assert (
        '    """\n    Typed user endpoints generated from Torn OpenAPI.'
        in source
    )
    assert "    Attributes:" in source
    assert "    Args:" in source
    assert "        Get your basic profile information." in source
    assert "        Returns:" in source
    assert "        Raises:" in source
    compile(source, "generated_user.py", "exec")
