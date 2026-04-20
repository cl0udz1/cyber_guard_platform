/**
 * Purpose:
 *   Placeholder workspace page showing organization scope, workspace context, and role ownership.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220028863 - BANDER SHOWAIL for backend RBAC and membership contracts
 * Inputs:
 *   Static org/workspace summary and role guide from feature mocks.
 * Outputs:
 *   Assignment-friendly workspace page scaffold.
 * TODO:
 *   - [ ] Wire active org/workspace context after auth and membership contracts stabilize.
 *   - [ ] Keep role labels aligned with backend RBAC definitions (owner, admin, analyst, viewer).
 *   - [ ] Do not add role-switching logic here until backend permissions are confirmed.
 */

import PlaceholderPanel from "../../components/shared/PlaceholderPanel";
import { organizationOverview, workspaceRoleGuide } from "../../features/orgs/orgSummary";
import { mutedTextStyle, panelStyle, sectionTitleStyle } from "../../app/styles";

export default function WorkspacePage() {
  return (
    <div style={{ display: "grid", gap: "16px" }}>
      <section style={panelStyle}>
        <h3 style={sectionTitleStyle}>Organization + Workspace Scope</h3>
        <p style={mutedTextStyle}>
          {organizationOverview.organizationName} / {organizationOverview.workspaceName}
        </p>
        <p style={{ ...mutedTextStyle, marginTop: "10px" }}>{organizationOverview.identityBoundary}</p>
      </section>
      <PlaceholderPanel
        title="Role Ownership"
        ownerHint="220028863 BANDER (backend RBAC) + 220050709 GHAZA (frontend workspace)"
        summary="Keep role modeling simple and visible. This repo is meant to help assignments land in the right place fast."
        todo={workspaceRoleGuide.map((item) => `${item.role}: ${item.responsibilities}`)}
      />
    </div>
  );
}
