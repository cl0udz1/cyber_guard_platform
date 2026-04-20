import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import ReportSummaryCard from "./ReportSummaryCard";
import type { ReportCard } from "../../types/report";

const mockReport: ReportCard = {
  id: "report-001",
  title: "Test phishing report",
  severity: "high",
  sections: ["Artifact summary", "IOC overview", "Recommended actions"],
  publicationState: "private",
};

const pendingReport: ReportCard = {
  id: "report-002",
  title: "Pending review report",
  severity: "low",
  sections: ["Summary"],
  publicationState: "pending_review",
};

describe("ReportSummaryCard", () => {
  it("renders the report title", () => {
    render(<ReportSummaryCard report={mockReport} />);
    expect(screen.getByText("Test phishing report")).toBeInTheDocument();
  });

  it("renders severity pill", () => {
    render(<ReportSummaryCard report={mockReport} />);
    expect(screen.getByText("high")).toBeInTheDocument();
  });

  it("renders publication state pill", () => {
    render(<ReportSummaryCard report={mockReport} />);
    expect(screen.getByText("private")).toBeInTheDocument();
  });

  it("sections are hidden by default", () => {
    render(<ReportSummaryCard report={mockReport} />);
    expect(screen.queryByText("Artifact summary")).not.toBeInTheDocument();
  });

  it("shows sections count in toggle button", () => {
    render(<ReportSummaryCard report={mockReport} />);
    expect(screen.getByRole("button", { name: /sections \(3\)/i })).toBeInTheDocument();
  });

  it("expands to show sections on button click", () => {
    render(<ReportSummaryCard report={mockReport} />);
    fireEvent.click(screen.getByRole("button", { name: /sections/i }));
    expect(screen.getByText("Artifact summary")).toBeInTheDocument();
    expect(screen.getByText("IOC overview")).toBeInTheDocument();
    expect(screen.getByText("Recommended actions")).toBeInTheDocument();
  });

  it("collapses sections on second click", () => {
    render(<ReportSummaryCard report={mockReport} />);
    const btn = screen.getByRole("button", { name: /sections/i });
    fireEvent.click(btn);
    expect(screen.getByText("Artifact summary")).toBeInTheDocument();
    fireEvent.click(btn);
    expect(screen.queryByText("Artifact summary")).not.toBeInTheDocument();
  });

  it("shows warning pill for pending publication state", () => {
    render(<ReportSummaryCard report={pendingReport} />);
    expect(screen.getByText("pending_review")).toBeInTheDocument();
  });
});
