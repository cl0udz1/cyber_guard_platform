# DATA_FLOW.md

## Purpose

This document explains the intended end-to-end flow from artifact submission to optional public sharing.

## Private Analysis Flow

1. A user logs in and selects an organization workspace.
2. The user submits an artifact:
   - file upload
   - hash
   - URL
   - email indicator / pasted email signal
3. The backend creates a scan job.
4. The scan orchestrator normalizes the artifact.
5. IOC extraction pulls out useful indicators.
6. Enrichment adapters query multiple sources.
7. Optional AI analysis runs in local or API mode.
8. The report service generates a private threat report.
9. The dashboard service can summarize activity for the workspace.

Current scaffold note:

- the product flow is modeled as asynchronous scan work
- the current scaffold may still execute that flow inline inside one backend process

## Publication Flow

1. An organization views a private report.
2. The organization requests publication to the public feed.
3. The sanitization service removes or rejects identity/workspace-linked data.
4. If policy requires review, the request enters the admin review queue.
5. After approval, a public-safe report is written to the public layer.
6. The public threats page exposes only sanitized threat content.

## External Report Upload Flow

1. An organization uploads or pastes an external report summary.
2. The request is treated as a moderated public-sharing candidate.
3. Admin review checks redactions, wording, and suitability.
4. Approved content becomes a public report entry.

## Data Separation Rule

Private flow data may include:

- user identity
- organization membership
- workspace scope
- raw artifact content
- private report context

Public flow data may include only:

- sanitized summary
- generalized severity
- safe indicator counts
- public-safe tags or categories

Public flow data must not include:

- user IDs
- organization IDs
- workspace IDs
- direct private report IDs
- raw private references that allow re-linking

This separation should stay consistent across routes, services, tests, and docs.
