/**
 * Purpose:
 *   Renders a grid of KPI metric cards for the workspace dashboard.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend dashboard field names
 * TODO:
 *   - [ ] Replace mock metrics with live `/dashboard/overview` data after backend fields are locked.
 *   - [ ] Keep metrics private to the active workspace — do not mix with public feed data.
 *   - [ ] Do not add charts or trend lines until basic metric wiring is working.
 */

import type { DashboardMetric } from "../../types/dashboard";
import { panelStyle, sectionTitleStyle, theme } from "../../app/styles";

interface MetricsBoardProps {
  metrics: DashboardMetric[];
  /** Show skeleton cards while data is loading. Defaults to false. */
  loading?: boolean;
}

function SkeletonCard() {
  return (
    <section
      aria-busy="true"
      style={{ ...panelStyle, opacity: 0.5 }}
    >
      <p style={{ margin: 0, color: theme.muted, fontSize: "12px", fontWeight: 700, textTransform: "uppercase" }}>
        Loading…
      </p>
      <div style={{ height: "40px", margin: "10px 0 6px", background: theme.surfaceAlt, borderRadius: "8px" }} />
      <div style={{ height: "16px", background: theme.surfaceAlt, borderRadius: "6px" }} />
    </section>
  );
}

export default function MetricsBoard(props: MetricsBoardProps) {
  const gridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "12px",
  };

  if (props.loading) {
    return (
      <div style={gridStyle}>
        {[0, 1, 2].map((i) => <SkeletonCard key={i} />)}
      </div>
    );
  }

  return (
    <div style={gridStyle}>
      {props.metrics.map((metric) => (
        <section key={metric.label} style={panelStyle}>
          <p
            style={{
              margin: 0,
              color: theme.muted,
              textTransform: "uppercase",
              fontSize: "12px",
              fontWeight: 700,
            }}
          >
            {metric.label}
          </p>
          <h3 style={{ ...sectionTitleStyle, margin: "10px 0 6px", fontSize: "32px" }}>{metric.value}</h3>
          <p style={{ margin: 0, color: theme.muted, lineHeight: 1.5, fontSize: "13px" }}>{metric.note}</p>
        </section>
      ))}
    </div>
  );
}
