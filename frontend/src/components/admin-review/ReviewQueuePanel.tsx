/**
 * Purpose:
 *   Renders the admin moderation queue showing pending external report review items.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend admin review contracts
 * TODO:
 *   - [ ] Replace mock items with live `/admin-reviews/queue` data after backend review flow is confirmed.
 *   - [ ] Status values to support: pending_review | approved | rejected.
 *   - [ ] Wire Approve/Reject buttons to POST /api/v1/admin-reviews/{id}/decision once backend is ready.
 */

import { useState } from "react";
import type { ReviewItem } from "../../types/publicThreat";
import { panelStyle, pillStyle, sectionTitleStyle, theme } from "../../app/styles";

interface ReviewQueuePanelProps {
  items: ReviewItem[];
}

type Decision = "approved" | "rejected";
type DecisionMap = Record<string, Decision | undefined>;

function statusPillKind(status: string): "accent" | "warning" | "neutral" {
  if (status === "approved") return "accent";
  if (status === "rejected") return "warning";
  return "neutral";
}

export default function ReviewQueuePanel(props: ReviewQueuePanelProps) {
  const [decisions, setDecisions] = useState<DecisionMap>({});

  function decide(id: string, decision: Decision) {
    setDecisions((prev) => ({ ...prev, [id]: decision }));
    // TODO: Wire to POST /api/v1/admin-reviews/{id}/decision once backend is ready.
  }

  return (
    <section style={panelStyle}>
      <h3 style={sectionTitleStyle}>Moderation Queue</h3>
      <div style={{ display: "grid", gap: "12px" }}>
        {props.items.map((item) => {
          const decision = decisions[item.id];
          const resolvedStatus = decision ?? item.status;
          const isPending = !decision && item.status === "pending_review";

          return (
            <article
              key={item.id}
              style={{
                border: `1px solid ${theme.border}`,
                borderRadius: "14px",
                padding: "14px",
                background: "#fffdf8",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                  marginBottom: "8px",
                }}
              >
                <strong style={{ fontSize: "14px" }}>{item.id}</strong>
                <span style={pillStyle(statusPillKind(resolvedStatus))}>{resolvedStatus}</span>
              </div>

              <p style={{ margin: "0 0 4px", color: theme.muted, fontSize: "13px" }}>{item.type}</p>
              <p style={{ margin: "0 0 12px", color: theme.muted, fontSize: "13px" }}>{item.note}</p>

              {/* Action buttons — only shown while item is pending */}
              {isPending && (
                <div style={{ display: "flex", gap: "8px" }}>
                  <button
                    onClick={() => decide(item.id, "approved")}
                    style={{
                      padding: "6px 16px",
                      borderRadius: "8px",
                      border: `1px solid ${theme.accent}`,
                      background: theme.accentSoft,
                      color: theme.accent,
                      fontWeight: 700,
                      fontSize: "13px",
                      cursor: "pointer",
                    }}
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => decide(item.id, "rejected")}
                    style={{
                      padding: "6px 16px",
                      borderRadius: "8px",
                      border: `1px solid ${theme.border}`,
                      background: "transparent",
                      color: theme.muted,
                      fontWeight: 700,
                      fontSize: "13px",
                      cursor: "pointer",
                    }}
                  >
                    Reject
                  </button>
                </div>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}
