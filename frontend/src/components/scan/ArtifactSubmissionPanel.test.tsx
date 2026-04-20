import { describe, it, expect } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ArtifactSubmissionPanel from "./ArtifactSubmissionPanel";

describe("ArtifactSubmissionPanel", () => {
  it("renders all four artifact type buttons", () => {
    render(<ArtifactSubmissionPanel />);
    expect(screen.getByText("File Upload")).toBeInTheDocument();
    expect(screen.getByText("Hash Lookup")).toBeInTheDocument();
    expect(screen.getByText("URL")).toBeInTheDocument();
    expect(screen.getByText("Email Signal")).toBeInTheDocument();
  });

  it("renders submit button", () => {
    render(<ArtifactSubmissionPanel />);
    expect(screen.getByRole("button", { name: /submit for scan/i })).toBeInTheDocument();
  });

  it("submit button is disabled when input is empty", () => {
    render(<ArtifactSubmissionPanel />);
    const submitBtn = screen.getByRole("button", { name: /submit for scan/i });
    expect(submitBtn).toBeDisabled();
  });

  it("enables submit button when URL input has a value", () => {
    render(<ArtifactSubmissionPanel />);
    const input = screen.getByLabelText(/url input/i);
    fireEvent.change(input, { target: { value: "https://example.com" } });
    expect(screen.getByRole("button", { name: /submit for scan/i })).not.toBeDisabled();
  });

  it("switches to Hash tab and shows correct placeholder", () => {
    render(<ArtifactSubmissionPanel />);
    fireEvent.click(screen.getByText("Hash Lookup"));
    const input = screen.getByLabelText(/hash lookup input/i);
    expect(input).toHaveAttribute("placeholder", "Enter SHA-256, MD5, or SHA-1");
  });

  it("switches to Email Signal tab and shows correct placeholder", () => {
    render(<ArtifactSubmissionPanel />);
    fireEvent.click(screen.getByText("Email Signal"));
    const input = screen.getByLabelText(/email signal input/i);
    expect(input).toHaveAttribute("placeholder", "Paste sender, subject, or suspicious content");
  });

  it("shows File tab with file input when File Upload is selected", () => {
    render(<ArtifactSubmissionPanel />);
    fireEvent.click(screen.getByText("File Upload"));
    expect(screen.getByLabelText(/file upload/i)).toHaveAttribute("type", "file");
  });

  it("shows success message after submission", async () => {
    render(<ArtifactSubmissionPanel />);
    const input = screen.getByLabelText(/url input/i);
    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.click(screen.getByRole("button", { name: /submit for scan/i }));
    await waitFor(() => expect(screen.getByRole("status")).toHaveTextContent("Queued successfully"), {
      timeout: 2000,
    });
  });

  it("renders all pipeline stages", () => {
    render(<ArtifactSubmissionPanel />);
    expect(screen.getByText("Pipeline Stages")).toBeInTheDocument();
    // Match the <strong> stage name labels specifically
    expect(screen.getByText("Normalize:")).toBeInTheDocument();
    expect(screen.getByText("Enrich:")).toBeInTheDocument();
    expect(screen.getByText("Report:")).toBeInTheDocument();
  });
});
