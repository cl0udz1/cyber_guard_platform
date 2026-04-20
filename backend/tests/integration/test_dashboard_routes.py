def test_dashboard_overview_requires_auth(client) -> None:
    response = client.get("/api/v1/dashboard/overview")
    assert response.status_code == 401


def test_dashboard_overview_returns_workspace_scoped_payload(client, org_auth_header) -> None:
    response = client.get("/api/v1/dashboard/overview", headers=org_auth_header)

    assert response.status_code == 200
    body = response.json()
    assert body["workspace_id"] == "demo-workspace"
    assert isinstance(body["metrics"], list)
    assert isinstance(body["recent_scan_statuses"], dict)
    assert isinstance(body["publish_queue_count"], int)
    assert isinstance(body["top_sources"], list)


def test_dashboard_overview_counts_reports_after_scan(client, org_auth_header) -> None:
    create_response = client.post(
        "/api/v1/scan-jobs",
        headers=org_auth_header,
        json={
            "artifact": {
                "workspace_id": "demo-workspace",
                "artifact_type": "url",
                "artifact_value": "https://example.org/dashboard-report-count",
            },
            "ai_mode": "off",
        },
    )
    assert create_response.status_code == 200

    dashboard_response = client.get("/api/v1/dashboard/overview", headers=org_auth_header)
    assert dashboard_response.status_code == 200

    metrics = {item["label"]: item["value"] for item in dashboard_response.json()["metrics"]}
    assert int(metrics["Reports Ready"]) >= 1


def test_dashboard_time_range_filter_excludes_old_data(client, org_auth_header) -> None:
    create_response = client.post(
        "/api/v1/scan-jobs",
        headers=org_auth_header,
        json={
            "artifact": {
                "workspace_id": "demo-workspace",
                "artifact_type": "url",
                "artifact_value": "https://example.org/dashboard-time-filter",
            },
            "ai_mode": "off",
        },
    )
    assert create_response.status_code == 200

    dashboard_response = client.get(
        "/api/v1/dashboard/overview",
        headers=org_auth_header,
        params={"start_date": "2999-01-01T00:00:00Z"},
    )
    assert dashboard_response.status_code == 200

    metrics = {item["label"]: item["value"] for item in dashboard_response.json()["metrics"]}
    assert int(metrics["Reports Ready"]) == 0
