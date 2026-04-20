from app.core.security import create_access_token
from uuid import uuid4


def _create_completed_scan_job(client, auth_header: dict[str, str]) -> dict[str, object]:
    unique_url = f"https://example.org/suspicious-login/{uuid4().hex}"
    response = client.post(
        "/api/v1/scan-jobs",
        headers=auth_header,
        json={
            "artifact": {
                "workspace_id": "demo-workspace",
                "artifact_type": "url",
                "artifact_value": unique_url,
            },
            "ai_mode": "local",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_publish_request_creates_review_and_sets_pending_status(
    client,
    org_auth_header,
    admin_auth_header,
) -> None:
    scan_job = _create_completed_scan_job(client, org_auth_header)

    publish_response = client.post(
        f"/api/v1/reports/{scan_job['report_id']}/publish-request",
        headers=org_auth_header,
        json={
            "include_in_public_feed": True,
            "notes_for_reviewer": "Safe to publish after redaction.",
        },
    )

    assert publish_response.status_code == 200
    publish_body = publish_response.json()
    assert publish_body["status"] == "pending_review"
    assert publish_body["public_payload_preview"]["severity"] in {"low", "medium", "high", "critical", "info"}

    queue_response = client.get("/api/v1/admin-reviews/queue", headers=admin_auth_header)
    assert queue_response.status_code == 200
    queue_items = queue_response.json()
    assert len(queue_items) == 1
    assert queue_items[0]["review_type"] == "report_publish_request"

    report_response = client.get(f"/api/v1/reports/{scan_job['report_id']}", headers=org_auth_header)
    assert report_response.status_code == 200
    assert report_response.json()["publish_status"] == "pending_review"


def test_admin_approval_publishes_report_to_public_feed(
    client,
    org_auth_header,
    admin_auth_header,
) -> None:
    scan_job = _create_completed_scan_job(client, org_auth_header)

    publish_response = client.post(
        f"/api/v1/reports/{scan_job['report_id']}/publish-request",
        headers=org_auth_header,
        json={
            "include_in_public_feed": True,
            "notes_for_reviewer": "Publishable summary.",
        },
    )
    assert publish_response.status_code == 200

    queue_response = client.get("/api/v1/admin-reviews/queue", headers=admin_auth_header)
    assert queue_response.status_code == 200
    review_id = queue_response.json()[0]["review_id"]

    decision_response = client.post(
        f"/api/v1/admin-reviews/{review_id}/decision",
        headers=admin_auth_header,
        json={"decision": "approve", "reviewer_notes": "Redactions are clean."},
    )
    assert decision_response.status_code == 200
    assert decision_response.json()["status"] == "approved"

    public_feed = client.get("/api/v1/public-threats")
    assert public_feed.status_code == 200
    titles = [item["title"] for item in public_feed.json()["items"]]
    assert any(title.startswith("Anonymized threat report") for title in titles)


def test_report_route_hides_reports_outside_workspace(client, org_auth_header) -> None:
    scan_job = _create_completed_scan_job(client, org_auth_header)

    other_workspace_token = create_access_token(
        {
            "sub": "other.analyst@example.edu",
            "email": "other.analyst@example.edu",
            "role": "org_admin",
            "organization_id": "demo-org",
            "workspace_id": "other-workspace",
        }
    )
    other_workspace_header = {"Authorization": f"Bearer {other_workspace_token}"}

    forbidden_response = client.get(
        f"/api/v1/reports/{scan_job['report_id']}",
        headers=other_workspace_header,
    )
    assert forbidden_response.status_code == 404


def test_external_upload_enters_review_and_can_be_approved(
    client,
    org_auth_header,
    admin_auth_header,
) -> None:
    external_response = client.post(
        "/api/v1/reports/external-upload",
        headers=org_auth_header,
        json={
            "organization_id": "demo-org",
            "title": "Malicious infrastructure bulletin",
            "summary": (
                "Observed phishing hosts and lure templates in active campaigns. "
                "Requesting public publication after moderation checks."
            ),
            "source_url": "https://example.org/advisory",
            "requested_visibility": "public_after_review",
        },
    )
    assert external_response.status_code == 200
    upload_reference = external_response.json()["upload_reference"]

    queue_response = client.get("/api/v1/admin-reviews/queue", headers=admin_auth_header)
    assert queue_response.status_code == 200
    review_id = queue_response.json()[0]["review_id"]

    decision_response = client.post(
        f"/api/v1/admin-reviews/{review_id}/decision",
        headers=admin_auth_header,
        json={"decision": "approve", "reviewer_notes": "External submission approved."},
    )
    assert decision_response.status_code == 200

    public_item_response = client.get(f"/api/v1/public-threats/{upload_reference}")
    assert public_item_response.status_code == 200
    assert public_item_response.json()["source_kind"] == "external_upload"
