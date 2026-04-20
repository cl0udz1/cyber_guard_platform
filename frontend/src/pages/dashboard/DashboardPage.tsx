/**
 * Purpose:
 *   Placeholder dashboard page for workspace metrics and owner-visible summary cards.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend dashboard fields
 * Inputs:
 *   Static metric cards and dashboard ownership notes.
 * Outputs:
 *   Assignment-friendly dashboard page scaffold.
 * TODO:
 *   - [ ] Add live `/dashboard/overview` integration after backend fields are locked.
 */

import MetricsBoard from "../../components/dashboard/MetricsBoard";
import PlaceholderPanel from "../../components/shared/PlaceholderPanel";
import { dashboardMetrics } from "../../mocks/overview";

export default function DashboardPage() {
  return (
    <div style={{ display: "grid", gap: "16px" }}>
      <MetricsBoard metrics={dashboardMetrics} />
      <PlaceholderPanel
        title="Dashboard Ownership Notes"
        ownerHint="220050709 GHAZA (frontend dashboard) + 220041379 MUHANNAD (backend dashboard)"
        summary="Dashboard work should stay lightweight at first: KPI cards, recent scan states, publish queue visibility, and source usage overview."
        todo={[
          "Wire `/dashboard/overview` before building extra charts.",
          "Keep dashboard private to the active workspace context.",
          "Avoid mixing public feed metrics with identity-linked private metrics.",
        ]}
      />
    </div>
  );
}
