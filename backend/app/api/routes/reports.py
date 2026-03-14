"""
Purpose:
    Private report and sharing workflow endpoints.
Owner:
    Primary: 220041379 - MUHANNAD ALKHARMANI
    Coordinate with: 220028863 - BANDER SHOWAIL for access rules
Inputs:
    Report IDs, publish requests, and external upload payloads.
Outputs:
    Threat report details and sharing workflow status.
Dependencies:
    Report service, public sharing service, admin review service, and auth dependencies.
TODO Checklist:
    - [ ] Add real report persistence and fetch-by-workspace authorization.
    - [ ] Add report export endpoints if PDF generation becomes part of the delivery plan.
    - [ ] Preserve Disconnect by Design when publication flow gets richer.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    get_admin_review_service,
    get_current_principal,
    get_public_sharing_service,
    get_report_service,
)
from app.schemas.auth import CurrentPrincipal
from app.schemas.report import ExternalReportUploadRequest, PublishRequest, ThreatReportResponse
from app.services.admin_review_service import AdminReviewService
from app.services.public_sharing_service import PublicSharingService
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{report_id}", response_model=ThreatReportResponse)
async def get_report(
    report_id: str,
    _: CurrentPrincipal = Depends(get_current_principal),
    report_service: ReportService = Depends(get_report_service),
) -> ThreatReportResponse:
    """Return a private threat report built by the scaffold pipeline."""
    report = report_service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Threat report not found.")
    return report


@router.post("/{report_id}/publish-request")
async def request_publication(
    report_id: str,
    payload: PublishRequest,
    _: CurrentPrincipal = Depends(get_current_principal),
    report_service: ReportService = Depends(get_report_service),
    public_sharing_service: PublicSharingService = Depends(get_public_sharing_service),
    admin_review_service: AdminReviewService = Depends(get_admin_review_service),
) -> dict[str, object]:
    """Create a publication request preview for a private report."""
    report = report_service.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Threat report not found.")
    publish_request = public_sharing_service.create_publish_request(report, payload)
    admin_review_service.create_review("report_publish_request", f"Review publish request for report {report_id}.")
    return publish_request


@router.post("/external-upload")
async def upload_external_report(
    payload: ExternalReportUploadRequest,
    _: CurrentPrincipal = Depends(get_current_principal),
    public_sharing_service: PublicSharingService = Depends(get_public_sharing_service),
    admin_review_service: AdminReviewService = Depends(get_admin_review_service),
) -> dict[str, object]:
    """Accept an external report upload placeholder and place it in review."""
    result = public_sharing_service.accept_external_upload(payload)
    admin_review_service.create_review(
        "external_report_upload",
        f"Review external upload '{payload.title}' before public release.",
    )
    return result
