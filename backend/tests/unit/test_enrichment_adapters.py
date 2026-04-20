import asyncio

from app.services.enrichment.source_a_client import SourceAClient
from app.services.enrichment.source_b_client import SourceBClient
from app.services.enrichment.virustotal_client import VirusTotalClient


def test_enrichment_adapters_return_expected_shape() -> None:
    async def run() -> list[dict[str, object]]:
        adapters = [
            VirusTotalClient(api_key="", base_url="https://example.test", timeout_seconds=5),
            SourceAClient(),
            SourceBClient(),
        ]
        return [await adapter.enrich(["indicator"], "https://example.org") for adapter in adapters]

    results = asyncio.run(run())

    assert [result["source_name"] for result in results] == ["virustotal", "source_a", "source_b"]
    assert all("confidence_score" in result for result in results)


def test_virustotal_client_scores_risky_http_login_url() -> None:
    async def run() -> dict[str, object]:
        client = VirusTotalClient(
            api_key="",
            base_url="https://example.test",
            timeout_seconds=5,
        )
        return await client.enrich(
            indicators=["10.0.0.4", "login", "redirect=account", "token=abc123"],
            artifact_value="http://10.0.0.4/login?redirect=account&token=abc123",
        )

    result = asyncio.run(run())

    assert result["source_name"] == "virustotal"
    assert result["verdict"] in {"suspicious", "malicious"}
    assert result["confidence_score"] >= 60
    assert "VirusTotal-style local assessment" in result["summary"]
