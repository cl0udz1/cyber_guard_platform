/**
 * Purpose:
 *   Frontend types for scan artifact options, pipeline stages, and queue items.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220053973 - FARIS BIN SUMAYDI for backend artifact and scan job field changes
 * TODO:
 *   - [ ] Keep type names aligned with backend scan job schema (artifact_type, ai_mode, state).
 *   - [ ] Add new artifact types only after backend normalization service supports them.
 */

export interface ArtifactOption {
  /** One of the four supported indicator types. */
  type: "file" | "hash" | "url" | "email_signal";
  /** Display label shown in the submission panel. */
  label: string;
  /** Short description of what this artifact type represents. */
  detail: string;
}

export interface PipelineStage {
  /** Stage name matching the backend pipeline step (e.g. normalize, enrich, report). */
  name: string;
  /** Short description of what happens at this stage. */
  detail: string;
}

export interface QueueItem {
  /** Unique scan job ID. */
  id: string;
  /** Artifact type submitted for this job (file, hash, url, email_signal). */
  artifactType: string;
  /** Current job state: queued | enriching | reporting | completed | failed. */
  state: string;
  /** AI mode used for this job: local | api | none. */
  aiMode: string;
}
