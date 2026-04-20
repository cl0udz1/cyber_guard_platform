# API_CONTRACT.md

Base prefix: `/api/v1`

This contract is intentionally scaffold-level. It defines the route surface, access expectations, and example payloads so backend and frontend work can proceed in parallel.

## Status Labels

- `MVP`: should exist in the core project delivery
- `Later`: useful but can wait until MVP is stable
- `Org-only`: authenticated org/workspace context required
- `Admin`: platform admin or reviewer role required

## Route Groups

| Group | Route | Access | Status | Purpose |
|---|---|---|---|---|
| Auth | `POST /auth/register` | Public | MVP | Create a scaffold user account |
| Auth | `POST /auth/login` | Public | MVP | Return bearer token |
| Auth | `GET /auth/me` | Authenticated | MVP | Return current user context |
| Users | `GET /users/me` | Authenticated | MVP | Return current profile |
| Users | `GET /users/me/memberships` | Authenticated | MVP | Return org/workspace memberships |
| Orgs | `POST /orgs` | Authenticated | MVP | Create organization |
| Orgs | `GET /orgs/{org_id}` | Org-only | MVP | View org summary |
| Orgs | `GET /orgs/{org_id}/memberships` | Org-only | MVP | List members and roles |
| Workspaces | `POST /workspaces` | Org-only | MVP | Create workspace |
| Workspaces | `GET /workspaces` | Org-only | MVP | List available workspaces |
| Workspaces | `GET /workspaces/{workspace_id}` | Org-only | MVP | View workspace summary |
| Scan Jobs | `POST /scan-jobs` | Org-only | MVP | Submit artifact and create async job |
| Scan Jobs | `GET /scan-jobs` | Org-only | MVP | List scan jobs |
| Scan Jobs | `GET /scan-jobs/{scan_job_id}` | Org-only | MVP | Poll one scan job |
| Reports | `GET /reports/{report_id}` | Org-only | MVP | View private threat report |
| Reports | `POST /reports/{report_id}/publish-request` | Org-only | MVP | Request anonymized publication |
| Reports | `POST /reports/external-upload` | Org-only | MVP | Submit external report for admin review |
| Dashboard | `GET /dashboard/overview` | Org-only | MVP | Workspace dashboard overview |
| Public Threats | `GET /public-threats` | Public | MVP | List anonymized public reports |
| Public Threats | `GET /public-threats/{public_report_id}` | Public | MVP | View one public-safe report summary |
| Admin Review | `GET /admin-reviews/queue` | Admin | MVP | Review queue |
| Admin Review | `POST /admin-reviews/{review_id}/decision` | Admin | MVP | Approve/reject/request changes |
| Integrations | `GET /integrations/catalog` | Org-only | MVP | Show available enrichment and AI adapters |
| Integrations | `GET /integrations/public-threats-api` | Public | Later | Show phase-2 public API status |

## Example Requests And Responses

### Auth

`POST /api/v1/auth/login`

Request:

```json
{
  "email": "admin@example.edu",
  "password": "org-admin-demo"
}
```

Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "principal_role": "org_admin"
}
```

### Org + Workspace

`POST /api/v1/workspaces`

Request:

```json
{
  "organization_id": "org-123",
  "name": "Threat Research Workspace",
  "slug": "threat-research"
}
```

Response:

```json
{
  "id": "workspace-123",
  "organization_id": "org-123",
  "name": "Threat Research Workspace",
  "slug": "threat-research",
  "created_at": "2026-03-14T12:00:00Z"
}
```

### Scan Jobs

`POST /api/v1/scan-jobs`

Request:

```json
{
  "artifact": {
    "workspace_id": "workspace-123",
    "artifact_type": "url",
    "artifact_value": "https://example.org/login"
  },
  "ai_mode": "local"
}
```

Response:

```json
{
  "scan_job_id": "job-123",
  "status": "completed",
  "artifact": {
    "submission_id": "submission-123",
    "workspace_id": "workspace-123",
    "artifact_type": "url",
    "normalized_value": "https://example.org/login",
    "created_at": "2026-03-14T12:02:00Z"
  },
  "ai_mode": "local",
  "sources": [
    {
      "source_name": "virustotal",
      "verdict": "observed",
      "confidence_score": 65,
      "summary": "VirusTotal placeholder hit count for the normalized URL."
    },
    {
      "source_name": "source_b",
      "verdict": "malicious",
      "confidence_score": 84,
      "summary": "Source B flagged high-risk overlap."
    }
  ],
  "report_id": "report-123",
  "created_at": "2026-03-14T12:02:00Z",
  "completed_at": "2026-03-14T12:02:04Z"
}
```

### Private Reports

`GET /api/v1/reports/{report_id}`

Response:

```json
{
  "report_id": "report-123",
  "scan_job_id": "job-123",
  "severity": "high",
  "confidence": 84,
  "executive_summary": "Scaffold report for url artifact submission.",
  "recommended_actions": [
    "Review source findings in the private workspace.",
    "Decide whether anonymized publication is appropriate."
  ],
  "source_summary": [
    "VirusTotal placeholder hit count for the normalized URL.",
    "Source B flagged high-risk overlap."
  ],
  "ai_summary": "Local AI mode synthesized source overlap without sending artifact data externally.",
  "publish_status": "private",
  "created_at": "2026-03-14T12:02:04Z"
}
```

### Publish Request

`POST /api/v1/reports/{report_id}/publish-request`

Request:

```json
{
  "include_in_public_feed": true,
  "notes_for_reviewer": "Indicators are safe to share after sanitization."
}
```

Response:

```json
{
  "report_id": "report-123",
  "status": "pending_review",
  "public_payload_preview": {
    "title": "Anonymized threat report ab12cd34",
    "summary": "Sanitized summary text.",
    "severity": "high",
    "indicator_count": 2,
    "notes_for_reviewer": "Indicators are safe to share after sanitization."
  }
}
```

### Public Threats

`GET /api/v1/public-threats`

Response:

```json
{
  "items": [
    {
      "public_report_id": "public-123",
      "public_slug": "threat-abcd1234",
      "title": "Credential phishing infrastructure indicators",
      "summary": "An anonymized report with indicators extracted from a private workspace analysis.",
      "severity": "medium",
      "indicator_count": 3,
      "source_kind": "workspace_publish",
      "published_at": "2026-03-14T12:05:00Z"
    }
  ],
  "next_cursor": null
}
```

### Admin Review

`POST /api/v1/admin-reviews/{review_id}/decision`

Request:

```json
{
  "decision": "approve",
  "reviewer_notes": "Redactions look correct."
}
```

Response:

```json
{
  "review_id": "review-123",
  "decision": "approve",
  "status": "approved"
}
```

## Contract Notes

- `scan-jobs` represents asynchronous execution even though the current scaffold runs inline.
- `public-threats` must remain identity-safe.
- `reports` are private workspace artifacts.
- current scaffold tests already cover auth, scan-jobs, public-threats, and overall route presence.
- remaining MVP route groups should stay explicitly tracked in the test plan until coverage is added.
- `integrations/public-threats-api` is a planned phase-2 surface, not an MVP commitment.
