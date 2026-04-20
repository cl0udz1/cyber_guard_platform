EXPECTED_PATHS = {
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/me",
    "/api/v1/users/me",
    "/api/v1/orgs",
    "/api/v1/workspaces",
    "/api/v1/scan-jobs",
    "/api/v1/reports/{report_id}",
    "/api/v1/reports/{report_id}/publish-request",
    "/api/v1/reports/external-upload",
    "/api/v1/public-threats",
    "/api/v1/admin-reviews/queue",
    "/api/v1/dashboard/overview",
    "/api/v1/integrations/catalog",
    "/api/v1/integrations/public-threats-api",
}


def test_openapi_contains_expected_route_groups(client) -> None:
    schema = client.get("/openapi.json").json()
    paths = set(schema["paths"].keys())

    assert EXPECTED_PATHS.issubset(paths)


def test_public_threat_schema_excludes_private_identity_fields(client) -> None:
    schema = client.get("/openapi.json").json()
    public_threat_properties = schema["components"]["schemas"]["PublicThreatSummary"]["properties"]

    forbidden_fields = {
        "organization_id",
        "workspace_id",
        "user_id",
        "private_report_id",
        "owner_email",
    }
    for field in forbidden_fields:
        assert field not in public_threat_properties


def test_publish_request_schema_forbids_extra_fields(client) -> None:
    schema = client.get("/openapi.json").json()
    publish_request_schema = schema["components"]["schemas"]["PublishRequest"]

    assert publish_request_schema.get("additionalProperties") is False
