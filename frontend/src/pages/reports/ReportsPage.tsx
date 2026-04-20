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

import { useState } from "react";
import ReportSummaryCard from "../../components/reports/ReportSummaryCard";
import PlaceholderPanel from "../../components/shared/PlaceholderPanel";
import { reportSections } from "../../features/reports/reportPlan";
import { reportCards } from "../../mocks/overview";
import { theme } from "../../app/styles";

const ALL = "all";
const severityOptions = [ALL, "low", "medium", "high", "critical"];

export default function ReportsPage() {
  const [filter, setFilter] = useState(ALL);

  const visible =
    filter === ALL ? reportCards : reportCards.filter((r) => r.severity === filter);

  return (
    <div style={{ display: "grid", gap: "16px" }}>
      {/* Severity filter */}
      <div
        role="group"
        aria-label="Filter reports by severity"
        style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}
      >
        {severityOptions.map((s) => {
          const active = filter === s;
          return (
            <button
              key={s}
              onClick={() => setFilter(s)}
              style={{
                padding: "5px 14px",
                borderRadius: "999px",
                border: `1.5px solid ${active ? theme.accent : theme.border}`,
                background: active ? theme.accentSoft : "transparent",
                color: active ? theme.accent : theme.muted,
                fontWeight: 700,
                fontSize: "13px",
                cursor: "pointer",
                textTransform: "capitalize",
              }}
            >
              {s}
            </button>
          );
        })}
      </div>

      {visible.length === 0 ? (
        <p style={{ color: theme.muted, fontSize: "14px" }}>No reports match this filter.</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: "16px",
          }}
        >
          {visible.map((report) => (
            <ReportSummaryCard key={report.id} report={report} />
          ))}
        </div>
      )}

      <PlaceholderPanel
        title="Threat Report Shape"
        ownerHint="220041379 MUHANNAD (backend reports) + 220050709 GHAZA (frontend reports)"
        summary="Reports should stay implementation-friendly: one clear artifact story, source summaries, optional AI notes, and publication status."
        todo={reportSections}
      />
    </div>
  );
}
