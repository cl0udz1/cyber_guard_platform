/**
 * Purpose:
 *   Placeholder public threats page for the anonymized, public-facing threat feed.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend public sharing contracts
 * Inputs:
 *   Static public threat cards and privacy principle notes.
 * Outputs:
 *   Assignment-friendly public threats page scaffold.
 * TODO:
 *   - [ ] Wire `/public-threats` feed only after backend sanitization logic is confirmed.
 *   - [ ] Never display workspace identity, user identity, or org data on this page.
 *   - [ ] Keep "Disconnect by Design" note visible until real data wiring begins.
 */

import PublicThreatFeed from "../../components/public-threats/PublicThreatFeed";
import PlaceholderPanel from "../../components/shared/PlaceholderPanel";
import { publicThreatPrinciples } from "../../features/public-threats/publicThreatMocks";
import { publicThreatCards } from "../../mocks/overview";

export default function PublicThreatsPage() {
  return (
    <div style={{ display: "grid", gap: "16px" }}>
      <PublicThreatFeed items={publicThreatCards} />
      <PlaceholderPanel
        title="Disconnect by Design"
        ownerHint="220050709 GHAZA (frontend) + 220041379 MUHANNAD (backend public sharing)"
        summary="Public content is a different layer, not a view into private workspace records. That separation should stay visible in both frontend copy and backend contracts."
        todo={publicThreatPrinciples}
      />
    </div>
  );
}
