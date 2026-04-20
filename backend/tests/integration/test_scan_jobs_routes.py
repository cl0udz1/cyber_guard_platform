from app.core.security import create_access_token


def test_scan_job_flow_returns_report(client, org_auth_header) -> None:
    response = client.post(
        "/api/v1/scan-jobs",
        headers=org_auth_header,
        json={
            "artifact": {
                "workspace_id": "demo-workspace",
                "artifact_type": "url",
                "artifact_value": "https://example.org/login",
            },
            "ai_mode": "local",
        },
    )

    assert response.status_code == 200
    job = response.json()
    assert job["status"] == "completed"
    assert len(job["sources"]) >= 2

    report_response = client.get(f"/api/v1/reports/{job['report_id']}", headers=org_auth_header)
    assert report_response.status_code == 200
    assert report_response.json()["scan_job_id"] == job["scan_job_id"]


def test_duplicate_submission_returns_cached_job(client, org_auth_header) -> None:
    payload = {
        "artifact": {
            "workspace_id": "demo-workspace",
            "artifact_type": "url",
            "artifact_value": "https://example.org/login",
        },
        "ai_mode": "local",
    }

    first = client.post("/api/v1/scan-jobs", headers=org_auth_header, json=payload)
    second = client.post("/api/v1/scan-jobs", headers=org_auth_header, json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["scan_job_id"] == second.json()["scan_job_id"]


def test_scan_job_can_be_listed_and_retrieved(client, org_auth_header) -> None:
    create_response = client.post(
        "/api/v1/scan-jobs",
        headers=org_auth_header,
        json={
            "artifact": {
                "workspace_id": "demo-workspace",
                "artifact_type": "email_signal",
                "artifact_value": "From admin@example.org visit https://example.org/login",
            },
            "ai_mode": "off",
        },
    )

    assert create_response.status_code == 200
    created_job = create_response.json()

    list_response = client.get("/api/v1/scan-jobs", headers=org_auth_header)
    assert list_response.status_code == 200
    assert any(job["scan_job_id"] == created_job["scan_job_id"] for job in list_response.json())

    get_response = client.get(f"/api/v1/scan-jobs/{created_job['scan_job_id']}", headers=org_auth_header)
    assert get_response.status_code == 200
    assert get_response.json()["scan_job_id"] == created_job["scan_job_id"]


def test_scan_job_rejects_workspace_mismatch(client, org_auth_header) -> None:
    response = client.post(
        "/api/v1/scan-jobs",
        headers=org_auth_header,
        json={
            "artifact": {
                "workspace_id": "other-workspace",
                "artifact_type": "url",
                "artifact_value": "https://example.org/login",
            },
            "ai_mode": "local",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Artifact submission must stay inside the active workspace."


def test_scan_job_accepts_hash_submission(client, org_auth_header) -> None:
    response = client.post(
        "/api/v1/scan-jobs",
        headers=org_auth_header,
        json={
            "artifact": {
                "workspace_id": "demo-workspace",
                "artifact_type": "hash",
                "artifact_value": "A" * 64,
            },
            "ai_mode": "off",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["artifact"]["normalized_value"] == "a" * 64
    assert body["sources"]


def test_scan_job_is_hidden_from_other_workspaces(client, org_auth_header) -> None:
    create_response = client.post(
        "/api/v1/scan-jobs",
        headers=org_auth_header,
        json={
            "artifact": {
                "workspace_id": "demo-workspace",
                "artifact_type": "url",
                "artifact_value": "https://example.org/private",
            },
            "ai_mode": "off",
        },
    )
    assert create_response.status_code == 200

    other_workspace_token = create_access_token(
        {
            "sub": "another.analyst@example.edu",
            "email": "another.analyst@example.edu",
            "role": "org_admin",
            "organization_id": "demo-org",
            "workspace_id": "other-workspace",
        }
    )
    other_workspace_header = {"Authorization": f"Bearer {other_workspace_token}"}

    list_response = client.get("/api/v1/scan-jobs", headers=other_workspace_header)
    assert list_response.status_code == 200
    assert list_response.json() == []

    get_response = client.get(
        f"/api/v1/scan-jobs/{create_response.json()['scan_job_id']}",
        headers=other_workspace_header,
    )
    assert get_response.status_code == 404
