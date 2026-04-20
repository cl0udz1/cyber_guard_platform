import asyncio

from app.schemas.scan import SourceHit
from app.services.ai.local_ai_service import LocalAiService


def test_local_ai_service_builds_actionable_summary() -> None:
    async def run() -> str | None:
        service = LocalAiService(enabled=True)
        return await service.analyze(
            artifact_value="http://10.0.0.4/login?redirect=account&token=abc123",
            indicators=["10.0.0.4", "login", "redirect=account", "token=abc123"],
            source_hits=[
                SourceHit(
                    source_name="virustotal",
                    verdict="malicious",
                    confidence_score=91,
                    summary="High-risk URL characteristics observed.",
                ),
                SourceHit(
                    source_name="source_a",
                    verdict="suspicious",
                    confidence_score=70,
                    summary="Credential lure keywords detected.",
                ),
            ],
        )

    summary = asyncio.run(run())

    assert summary is not None
    assert "Local AI mode reviewed 4 indicators across 2 source results." in summary
    assert "Dominant verdict: malicious." in summary
    assert "Highest-confidence source: virustotal (91/100)." in summary
    assert "Recommended next step:" in summary
