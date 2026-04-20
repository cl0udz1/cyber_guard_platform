def _create_approved_external_public_report(
    client,
    org_auth_header: dict[str, str],
    admin_auth_header: dict[str, str],
    title: str,
) -> str:
    external_response = client.post(
        "/api/v1/reports/external-upload",
        headers=org_auth_header,
        json={
            "organization_id": "demo-org",
            "title": title,
            "summary": "Approved external report summary for public feed testing and pagination coverage.",
            "source_url": "https://example.org/public-feed-test",
            "requested_visibility": "public_after_review",
        },
    )
    assert external_response.status_code == 200

    queue_response = client.get("/api/v1/admin-reviews/queue", headers=admin_auth_header)
    assert queue_response.status_code == 200
    review_id = queue_response.json()[0]["review_id"]

    decision_response = client.post(
        f"/api/v1/admin-reviews/{review_id}/decision",
        headers=admin_auth_header,
        json={"decision": "approve", "reviewer_notes": "Approved for testing."},
    )
    assert decision_response.status_code == 200
    return external_response.json()["upload_reference"]


def test_public_feed_is_accessible(client) -> None:
    response = client.get("/api/v1/public-threats")

    assert response.status_code == 200
    assert len(response.json()["items"]) >= 1


def test_admin_review_requires_admin(client, org_auth_header, admin_auth_header) -> None:
    forbidden = client.get("/api/v1/admin-reviews/queue", headers=org_auth_header)
    allowed = client.get("/api/v1/admin-reviews/queue", headers=admin_auth_header)

    assert forbidden.status_code == 403
    assert allowed.status_code == 200
    assert isinstance(allowed.json(), list)


def test_public_feed_supports_pagination(client, org_auth_header, admin_auth_header) -> None:
    _create_approved_external_public_report(client, org_auth_header, admin_auth_header, "Pagination item one")
    _create_approved_external_public_report(client, org_auth_header, admin_auth_header, "Pagination item two")
    _create_approved_external_public_report(client, org_auth_header, admin_auth_header, "Pagination item three")

    first_page = client.get("/api/v1/public-threats", params={"limit": 2})
    assert first_page.status_code == 200
    first_body = first_page.json()
    assert len(first_body["items"]) == 2
    assert first_body["next_cursor"] is not None

    second_page = client.get(
        "/api/v1/public-threats",
        params={"limit": 2, "cursor": first_body["next_cursor"]},
    )
    assert second_page.status_code == 200
    second_body = second_page.json()
    assert len(second_body["items"]) >= 1

    first_ids = {item["public_report_id"] for item in first_body["items"]}
    second_ids = {item["public_report_id"] for item in second_body["items"]}
    assert first_ids.isdisjoint(second_ids)


def test_public_feed_supports_severity_filter(client, org_auth_header, admin_auth_header) -> None:
    _create_approved_external_public_report(client, org_auth_header, admin_auth_header, "Severity filter item")

    response = client.get("/api/v1/public-threats", params={"severity": "medium"})
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) >= 1
    assert all(item["severity"] == "medium" for item in body["items"])
