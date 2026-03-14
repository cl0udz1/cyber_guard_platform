/**
 * Purpose:
 *   Placeholder reports page for private threat report ownership and future report flow work.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend report shape changes
 * Inputs:
 *   Static report cards and planned report section list.
 * Outputs:
 *   Assignment-friendly report page scaffold.
 * TODO:
 *   - [ ] Keep report UI aligned with `docs/API_CONTRACT.md`.
 *   - [ ] Add live data wiring only after backend report fields stabilize.
 */

import ReportSummaryCard from "../../components/reports/ReportSummaryCard";
import PlaceholderPanel from "../../components/shared/PlaceholderPanel";
import { reportSections } from "../../features/reports/reportPlan";
import { reportCards } from "../../mocks/overview";

export default function ReportsPage() {
  return (
    <div style={{ display: "grid", gap: "16px" }}>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "16px" }}>
        {reportCards.map((report) => (
          <ReportSummaryCard key={report.id} report={report} />
        ))}
      </div>
      <PlaceholderPanel
        title="Threat Report Shape"
        ownerHint="Backend report owner + frontend report owner"
        summary="Reports should stay implementation-friendly: one clear artifact story, source summaries, optional AI notes, and publication status."
        todo={reportSections}
      />
    </div>
  );
}
