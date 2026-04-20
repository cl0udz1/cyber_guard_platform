/**
 * Purpose:
 *   Frontend types for workspace dashboard KPI metrics.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend dashboard overview field names
 * TODO:
 *   - [ ] Keep field names aligned with backend `/dashboard/overview` response shape.
 *   - [ ] All metrics must be scoped to the active workspace — no cross-workspace or public data.
 */

export interface DashboardMetric {
  /** Display label shown above the metric value (e.g. "Total Scans"). */
  label: string;
  /** The metric value to display (e.g. "42"). */
  value: string;
  /** Short contextual note shown below the value (e.g. "last 30 days"). */
  note: string;
}
