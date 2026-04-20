/**
 * Purpose:
 *   Renders the anonymized public threat feed cards with title, severity, source, and summary.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend public sharing and sanitization contracts
 * TODO:
 *   - [ ] Replace mock items with live `/public-threats` feed after backend sanitization is confirmed.
 *   - [ ] Never render workspace name, user name, org name, or any identity-linked field here.
 *   - [ ] Source field should reflect the anonymized enrichment source label, not an internal ID.
 */

import { useState } from "react";
import type { PublicThreatCard } from "../../types/publicThreat";
import { mutedTextStyle, panelStyle, pillStyle, sectionTitleStyle, theme } from "../../app/styles";

interface PublicThreatFeedProps {
  items: PublicThreatCard[];
}

const ALL = "all";
const severityOptions = [ALL, "low", "medium", "high", "critical"];

function severityPillKind(severity: string): "warning" | "neutral" {
  return severity === "high" || severity === "critical" ? "warning" : "neutral";
}

export default function PublicThreatFeed(props: PublicThreatFeedProps) {
  const [filter, setFilter] = useState(ALL);

  const visible =
    filter === ALL ? props.items : props.items.filter((item) => item.severity === filter);

  return (
    <section style={panelStyle}>
      <h3 style={sectionTitleStyle}>Public Threat Feed</h3>

      {/* Severity filter */}
      <div
        role="group"
        aria-label="Filter by severity"
        style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "16px" }}
      >
        {severityOptions.map((s) => {
          const active = filter === s;
          return (
            <button
              key={s}
              onClick={() => setFilter(s)}
              style={{
                padding: "4px 12px",
                borderRadius: "999px",
                border: `1.5px solid ${active ? theme.accent : theme.border}`,
                background: active ? theme.accentSoft : "transparent",
                color: active ? theme.accent : theme.muted,
                fontWeight: 700,
                fontSize: "12px",
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
        <p style={{ ...mutedTextStyle, fontSize: "13px" }}>No threats match this filter.</p>
      ) : (
        <div style={{ display: "grid", gap: "12px" }}>
          {visible.map((item) => (
            <article
              key={item.title}
              style={{ borderBottom: `1px solid ${theme.border}`, paddingBottom: "12px" }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                  gap: "8px",
                  marginBottom: "6px",
                }}
              >
                <strong style={{ fontSize: "14px" }}>{item.title}</strong>
                <span style={{ ...pillStyle(severityPillKind(item.severity)), flexShrink: 0 }}>
                  {item.severity}
                </span>
              </div>
              <p style={{ ...mutedTextStyle, fontSize: "13px" }}>{item.summary}</p>
              <p style={{ ...mutedTextStyle, marginTop: "6px", fontSize: "12px", fontWeight: 700 }}>
                Source: {item.source}
              </p>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
