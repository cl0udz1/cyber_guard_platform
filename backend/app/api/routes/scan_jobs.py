"""
Purpose:
    Async scan job endpoints for artifact submission and job polling.
Owner:
    Primary: 220053973 - FARIS BIN SUMAYDI
    Support: 220042711 - OMAR ABDURASHEED
Inputs:
    Scan job create payloads and authenticated principal context.
Outputs:
    Scan job status responses built by the orchestrator scaffold.
Dependencies:
    Scan orchestrator, auth dependencies, and scan schemas.
TODO Checklist:
    - [ ] Split file upload handling from pasted artifacts when multipart support is added.
    - [ ] Add DB-backed job history and pagination once persistence exists.
    - [ ] Keep route behavior aligned with `docs/API_CONTRACT.md`.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_principal, get_scan_orchestrator
from app.schemas.auth import CurrentPrincipal
from app.schemas.scan import ScanJobCreateRequest, ScanJobResponse
from app.services.scan_orchestrator import ScanOrchestrator

router = APIRouter(prefix="/scan-jobs", tags=["scan-jobs"])


@router.post("", response_model=ScanJobResponse)
async def create_scan_job(
    payload: ScanJobCreateRequest,
    principal: CurrentPrincipal = Depends(get_current_principal),
    orchestrator: ScanOrchestrator = Depends(get_scan_orchestrator),
) -> ScanJobResponse:
    """Accept a normalized intake request and hand it off to the orchestration scaffold."""
    if principal.workspace_id and payload.artifact.workspace_id != principal.workspace_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Artifact submission must stay inside the active workspace.",
        )
    return await orchestrator.start_scan(payload)


@router.get("", response_model=list[ScanJobResponse])
async def list_scan_jobs(
    principal: CurrentPrincipal = Depends(get_current_principal),
    orchestrator: ScanOrchestrator = Depends(get_scan_orchestrator),
) -> list[ScanJobResponse]:
    """List known scaffold scan jobs."""
    if not principal.workspace_id:
        return orchestrator.list_jobs()
    return [
        job
        for job in orchestrator.list_jobs()
        if job.artifact.workspace_id == principal.workspace_id
    ]


@router.get("/{scan_job_id}", response_model=ScanJobResponse)
async def get_scan_job(
    scan_job_id: str,
    principal: CurrentPrincipal = Depends(get_current_principal),
    orchestrator: ScanOrchestrator = Depends(get_scan_orchestrator),
) -> ScanJobResponse:
    """Return one scan job or a 404 if the scaffold has not created it."""
    result = orchestrator.get_job(scan_job_id)
    if result is None or (
        principal.workspace_id is not None
        and result.artifact.workspace_id != principal.workspace_id
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan job not found.")
    return result
