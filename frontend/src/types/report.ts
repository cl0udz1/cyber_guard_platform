/**
 * Purpose:
 *   Frontend types for private threat report display.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220041379 - MUHANNAD ALKHARMANI for backend report schema changes
 * TODO:
 *   - [ ] Keep field names aligned with backend ThreatReport model.
 *   - [ ] publicationState values: draft | pending_review | published | rejected.
 */

export interface ReportCard {
  /** Unique report ID. */
  id: string;
  /** Human-readable report title. */
  title: string;
  /** Threat severity level: low | medium | high | critical. */
  severity: string;
  /** List of content section labels included in this report. */
  sections: string[];
  /** Current publication state: draft | pending_review | published | rejected. */
  publicationState: string;
}
