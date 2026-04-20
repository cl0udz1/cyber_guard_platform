/**
 * Purpose:
 *   Displays supported artifact types (file, hash, url, email_signal) and the planned pipeline stages.
 * Owner:
 *   Primary: 220050709 - GHAZA ALAMTRAFA
 *   Coordinate with: 220053973 - FARIS BIN SUMAYDI for artifact submission backend contracts
 * TODO:
 *   - [ ] Replace static artifact cards with a real submission form once `/scan-jobs` is stable.
 *   - [ ] Keep all four artifact types (file, hash, url, email_signal) visible in the UI.
 *   - [ ] Do not add file upload logic until backend normalization contracts are confirmed.
 */

import { useState } from "react";
import type { CSSProperties } from "react";
import type { ArtifactOption } from "../../types/scan";
import { artifactOptions, pipelineStages } from "../../features/scan-jobs/scanJobMocks";
import { mutedTextStyle, panelStyle, pillStyle, sectionTitleStyle, theme } from "../../app/styles";

type SubmitState = "idle" | "loading" | "success" | "error";

const inputStyle: CSSProperties = {
  width: "100%",
  padding: "10px 12px",
  borderRadius: "10px",
  border: `1px solid ${theme.border}`,
  background: "#fff",
  fontSize: "14px",
  color: theme.ink,
  boxSizing: "border-box",
  outline: "none",
};

const placeholders: Record<ArtifactOption["type"], string> = {
  file: "",
  hash: "Enter SHA-256, MD5, or SHA-1",
  url: "https://example.com/path",
  email_signal: "Paste sender, subject, or suspicious content",
};

export default function ArtifactSubmissionPanel() {
  const [selectedType, setSelectedType] = useState<ArtifactOption["type"]>("url");
  const [inputValue, setInputValue] = useState("");
  const [fileName, setFileName] = useState("");
  const [submitState, setSubmitState] = useState<SubmitState>("idle");

  const selectedOption = artifactOptions.find((o) => o.type === selectedType)!;
  const hasValue = selectedType === "file" ? !!fileName : !!inputValue.trim();

  function handleTypeSelect(type: ArtifactOption["type"]) {
    setSelectedType(type);
    setInputValue("");
    setFileName("");
    setSubmitState("idle");
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!hasValue) return;
    setSubmitState("loading");
    // TODO: Replace with real POST to /api/v1/scan-jobs once backend is ready.
    setTimeout(() => {
      setSubmitState("success");
      setInputValue("");
      setFileName("");
      setTimeout(() => setSubmitState("idle"), 2500);
    }, 900);
  }

  return (
    <section style={panelStyle}>
      <h3 style={sectionTitleStyle}>Submit Artifact</h3>

      {/* Artifact type tabs */}
      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "16px" }}>
        {artifactOptions.map((option) => {
          const active = selectedType === option.type;
          return (
            <button
              key={option.type}
              onClick={() => handleTypeSelect(option.type)}
              style={{
                padding: "6px 14px",
                borderRadius: "999px",
                border: `1.5px solid ${active ? theme.accent : theme.border}`,
                background: active ? theme.accentSoft : "transparent",
                color: active ? theme.accent : theme.muted,
                fontWeight: 700,
                fontSize: "13px",
                cursor: "pointer",
              }}
            >
              {option.label}
            </button>
          );
        })}
      </div>

      <p style={{ ...mutedTextStyle, fontSize: "13px", marginBottom: "14px" }}>
        {selectedOption.detail}
      </p>

      {/* Submission form */}
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: "10px" }}>
        {selectedType === "file" && (
          <input
            key="file"
            type="file"
            aria-label="File upload"
            style={{ ...inputStyle, padding: "8px 12px" }}
            onChange={(e) => setFileName(e.target.files?.[0]?.name ?? "")}
          />
        )}
        {selectedType !== "file" && (
          <input
            key="text"
            type="text"
            value={inputValue}
            aria-label={`${selectedOption.label} input`}
            placeholder={placeholders[selectedType]}
            onChange={(e) => setInputValue(e.target.value)}
            style={inputStyle}
          />
        )}

        <button
          type="submit"
          disabled={!hasValue || submitState === "loading"}
          style={{
            padding: "10px 20px",
            borderRadius: "10px",
            border: "none",
            background: theme.accent,
            color: "#fff",
            fontWeight: 700,
            fontSize: "14px",
            cursor: !hasValue || submitState === "loading" ? "default" : "pointer",
            opacity: !hasValue ? 0.5 : 1,
          }}
        >
          {submitState === "loading" ? "Submitting…" : "Submit for Scan"}
        </button>

        {submitState === "success" && (
          <span role="status" style={{ ...pillStyle("accent"), justifySelf: "start" }}>
            Queued successfully
          </span>
        )}
        {submitState === "error" && (
          <span role="alert" style={{ ...pillStyle("warning"), justifySelf: "start" }}>
            Submission failed — try again
          </span>
        )}
      </form>

      {/* Pipeline stages */}
      <h4 style={{ margin: "20px 0 10px", fontWeight: 700, fontSize: "15px", color: theme.ink }}>
        Pipeline Stages
      </h4>
      <ol style={{ margin: 0, paddingLeft: "20px", color: theme.muted, lineHeight: 1.8, fontSize: "14px" }}>
        {pipelineStages.map((stage) => (
          <li key={stage.name}>
            <strong style={{ color: theme.ink }}>{stage.name}:</strong> {stage.detail}
          </li>
        ))}
      </ol>
    </section>
  );
}
