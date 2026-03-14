/**
 * Purpose:
 *   Frontend shell that maps major Cyber Guard domains to assignment-friendly page groups.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 * Inputs:
 *   Local active view state and static scaffold page map.
 * Outputs:
 *   A navigable frontend shell that mirrors the repo structure.
 * TODO:
 *   - [ ] Keep this shell lightweight; avoid moving feature logic here.
 *   - [ ] Coordinate with backend owners before changing page names tied to route groups.
 */

import { useState } from "react";

import AppHeader from "../components/layout/AppHeader";
import SideNav from "../components/layout/SideNav";
import { navItems, type ViewKey } from "./navigation";
import { shellStyles } from "./styles";
import { scaffoldSubtitle } from "../utils/copy";
import AccessPage from "../pages/auth/AccessPage";
import AdminReviewPage from "../pages/admin/AdminReviewPage";
import DashboardPage from "../pages/dashboard/DashboardPage";
import PublicThreatsPage from "../pages/public-threats/PublicThreatsPage";
import ReportsPage from "../pages/reports/ReportsPage";
import ScanWorkspacePage from "../pages/scan/ScanWorkspacePage";
import WorkspacePage from "../pages/workspace/WorkspacePage";

const pageByView: Record<ViewKey, JSX.Element> = {
  auth: <AccessPage />,
  workspace: <WorkspacePage />,
  scan: <ScanWorkspacePage />,
  reports: <ReportsPage />,
  dashboard: <DashboardPage />,
  "public-threats": <PublicThreatsPage />,
  admin: <AdminReviewPage />,
};

export default function AppShell() {
  const [activeView, setActiveView] = useState<ViewKey>("scan");
  const activeItem = navItems.find((item) => item.key === activeView) ?? navItems[0];

  return (
    <div style={shellStyles.page}>
      <div style={shellStyles.frame}>
        <SideNav activeView={activeView} onSelect={setActiveView} />
        <main style={shellStyles.main}>
          <AppHeader activeLabel={activeItem.label} subtitle={scaffoldSubtitle} />
          {pageByView[activeView]}
        </main>
      </div>
    </div>
  );
}
