"""
Purpose:
    Public feed endpoints for anonymized threat reports.
Inputs:
    Public report identifiers.
Outputs:
    Public-safe summaries suitable for unauthenticated consumption.
Dependencies:
    Public sharing service and public threat schemas.
TODO Checklist:
    - [ ] Add pagination, search, and filters if the public feed grows.
    - [ ] Add separate rate limiting if the phase-2 API is exposed publicly.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_public_sharing_service
from app.schemas.public_threats import PublicThreatListResponse, PublicThreatSummary
from app.services.public_sharing_service import PublicSharingService
from app.utils.enums import ThreatSeverity

router = APIRouter(prefix="/public-threats", tags=["public-threats"])


@router.get("", response_model=PublicThreatListResponse)
async def list_public_threats(
    public_sharing_service: PublicSharingService = Depends(get_public_sharing_service),
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None),
    severity: ThreatSeverity | None = Query(default=None),
) -> PublicThreatListResponse:
    """Return public-safe threat summaries."""
    return public_sharing_service.list_public_reports(
        limit=limit,
        cursor=cursor,
        severity=severity,
    )


@router.get("/{public_report_id}", response_model=PublicThreatSummary)
async def get_public_threat(
    public_report_id: str,
    public_sharing_service: PublicSharingService = Depends(get_public_sharing_service),
) -> PublicThreatSummary:
    """Return one public threat summary or 404."""
    report = public_sharing_service.get_public_report(public_report_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Public report not found.")
    return report
