/**
 * Purpose:
 *   Frontend types for the public threat feed and admin review queue.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend public sharing and admin review contracts
 * TODO:
 *   - [ ] PublicThreatCard must never include workspace, user, or org identity fields.
 *   - [ ] ReviewItem status values: pending | approved | rejected.
 *   - [ ] Keep these two interfaces separate — public feed and admin review are different flows.
 */

export interface PublicThreatCard {
  /** Anonymized threat title safe for public display. */
  title: string;
  /** Threat severity level: low | medium | high | critical. */
  severity: string;
  /** Anonymized enrichment source label (not an internal source ID). */
  source: string;
  /** Short public-safe summary of the threat. No identity or workspace data. */
  summary: string;
}

export interface ReviewItem {
  /** Unique admin review item ID. */
  id: string;
  /** Type of submission under review (e.g. external_report). */
  type: string;
  /** Current review status: pending | approved | rejected. */
  status: string;
  /** Reviewer note or reason for the current status. */
  note: string;
}
