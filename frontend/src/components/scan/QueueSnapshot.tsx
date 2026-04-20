/**
 * Purpose:
 *   Shows a static snapshot of scan job queue items with artifact type, AI mode, and state.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220053973 - FARIS BIN SUMAYDI for scan job state names
 * TODO:
 *   - [ ] Replace mock queue with live `/scan-jobs` polling after backend job states are locked.
 *   - [ ] States to support: queued, enriching, reporting, completed, failed.
 *   - [ ] Keep AI mode label (local / api / none) visible per queue item.
 */

import type { CSSProperties } from "react";
import type { QueueItem } from "../../types/scan";
import { scanQueue } from "../../mocks/overview";
import { panelStyle, sectionTitleStyle, theme } from "../../app/styles";

function stateBadgeStyle(state: string): CSSProperties {
  if (state === "completed") return { background: theme.accentSoft, color: theme.accent };
  if (state === "enriching" || state === "reporting") return { background: theme.warningSoft, color: theme.warning };
  if (state === "failed") return { background: "#fde8e8", color: theme.danger };
  return { background: theme.surfaceAlt, color: theme.muted }; // queued / unknown
}

function StateBadge({ state }: { state: string }) {
  return (
    <span
      data-testid={`state-badge-${state}`}
      style={{
        display: "inline-block",
        padding: "3px 10px",
        borderRadius: "999px",
        fontSize: "11px",
        fontWeight: 700,
        textTransform: "uppercase",
        letterSpacing: "0.05em",
        ...stateBadgeStyle(state),
      }}
    >
      {state}
    </span>
  );
}

export default function QueueSnapshot() {
  return (
    <section style={panelStyle}>
      <h3 style={sectionTitleStyle}>Scan Queue</h3>
      <div style={{ display: "grid", gap: "10px" }}>
        {scanQueue.map((item: QueueItem) => (
          <div
            key={item.id}
            style={{
              border: `1px solid ${theme.border}`,
              borderRadius: "14px",
              padding: "12px 16px",
              background: "#fffdf8",
              display: "grid",
              gridTemplateColumns: "1fr auto",
              alignItems: "center",
              gap: "8px",
            }}
          >
            <div>
              <strong style={{ fontSize: "14px" }}>{item.id}</strong>
              <p style={{ margin: "4px 0 0", color: theme.muted, fontSize: "13px" }}>
                {item.artifactType} · AI: {item.aiMode}
              </p>
            </div>
            <StateBadge state={item.state} />
          </div>
        ))}
      </div>
    </section>
  );
}
