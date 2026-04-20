/**
 * Purpose:
 *   Displays a single private threat report card with title, severity, sections, and publication state.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend report field changes
 * TODO:
 *   - [ ] Keep publicationState pill logic simple: pending = warning, others = accent.
 *   - [ ] Do not add report detail navigation until backend report endpoints are confirmed.
 *   - [ ] Section list comes from ReportCard.sections — keep it read-only for now.
 */

import { useState } from "react";
import type { ReportCard } from "../../types/report";
import { mutedTextStyle, panelStyle, pillStyle, sectionTitleStyle, theme } from "../../app/styles";
import type { CSSProperties } from "react";

interface ReportSummaryCardProps {
  report: ReportCard;
}

function severityStyle(severity: string): CSSProperties {
  if (severity === "critical" || severity === "high") return pillStyle("warning");
  return pillStyle("neutral");
}

export default function ReportSummaryCard(props: ReportSummaryCardProps) {
  const [expanded, setExpanded] = useState(false);
  const { report } = props;

  return (
    <section style={panelStyle}>
      {/* State + severity pills */}
      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "14px" }}>
        <span style={pillStyle(report.publicationState.includes("pending") ? "warning" : "accent")}>
          {report.publicationState}
        </span>
        <span style={severityStyle(report.severity)}>{report.severity}</span>
      </div>

      <h3 style={{ ...sectionTitleStyle, marginTop: 0 }}>{report.title}</h3>

      {/* Expand / collapse sections */}
      <button
        onClick={() => setExpanded((v) => !v)}
        aria-expanded={expanded}
        style={{
          background: "none",
          border: "none",
          padding: 0,
          cursor: "pointer",
          color: theme.accent,
          fontWeight: 700,
          fontSize: "13px",
          marginBottom: "10px",
        }}
      >
        {expanded ? "Hide sections ▲" : `Sections (${report.sections.length}) ▼`}
      </button>

      {expanded && (
        <ul
          style={{
            margin: "0 0 12px",
            paddingLeft: "18px",
            color: theme.muted,
            lineHeight: 1.7,
            fontSize: "14px",
          }}
        >
          {report.sections.map((section) => (
            <li key={section}>{section}</li>
          ))}
        </ul>
      )}

      {/* Placeholder action — wire to /reports/{id} once backend is ready */}
      <p style={{ ...mutedTextStyle, fontSize: "12px" }}>
        View Report — available after backend <code>/reports/{"{id}"}</code> is wired
      </p>
    </section>
  );
}
