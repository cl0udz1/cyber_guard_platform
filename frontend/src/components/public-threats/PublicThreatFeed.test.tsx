import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import PublicThreatFeed from "./PublicThreatFeed";
import type { PublicThreatCard } from "../../types/publicThreat";

const mockItems: PublicThreatCard[] = [
  {
    title: "Phishing infrastructure",
    severity: "medium",
    source: "workspace_publish",
    summary: "Anonymized summary A.",
  },
  {
    title: "Malware campaign",
    severity: "high",
    source: "external_report_upload",
    summary: "Anonymized summary B.",
  },
  {
    title: "Low severity indicator",
    severity: "low",
    source: "workspace_publish",
    summary: "Anonymized summary C.",
  },
];

describe("PublicThreatFeed", () => {
  it("renders heading", () => {
    render(<PublicThreatFeed items={mockItems} />);
    expect(screen.getByText("Public Threat Feed")).toBeInTheDocument();
  });

  it("renders all items by default", () => {
    render(<PublicThreatFeed items={mockItems} />);
    expect(screen.getByText("Phishing infrastructure")).toBeInTheDocument();
    expect(screen.getByText("Malware campaign")).toBeInTheDocument();
    expect(screen.getByText("Low severity indicator")).toBeInTheDocument();
  });

  it("renders severity filter buttons", () => {
    render(<PublicThreatFeed items={mockItems} />);
    expect(screen.getByRole("button", { name: /all/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /medium/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /high/i })).toBeInTheDocument();
  });

  it("filters to show only high severity items", () => {
    render(<PublicThreatFeed items={mockItems} />);
    fireEvent.click(screen.getByRole("button", { name: /^high$/i }));
    expect(screen.getByText("Malware campaign")).toBeInTheDocument();
    expect(screen.queryByText("Phishing infrastructure")).not.toBeInTheDocument();
    expect(screen.queryByText("Low severity indicator")).not.toBeInTheDocument();
  });

  it("shows empty state when filter has no matches", () => {
    render(<PublicThreatFeed items={mockItems} />);
    fireEvent.click(screen.getByRole("button", { name: /^critical$/i }));
    expect(screen.getByText("No threats match this filter.")).toBeInTheDocument();
  });

  it("restores all items when all filter is clicked", () => {
    render(<PublicThreatFeed items={mockItems} />);
    fireEvent.click(screen.getByRole("button", { name: /^high$/i }));
    fireEvent.click(screen.getByRole("button", { name: /^all$/i }));
    expect(screen.getByText("Phishing infrastructure")).toBeInTheDocument();
    expect(screen.getByText("Low severity indicator")).toBeInTheDocument();
  });

  it("renders source for each item", () => {
    render(<PublicThreatFeed items={mockItems} />);
    expect(screen.getAllByText(/source:/i).length).toBe(3);
  });

  it("renders empty list without crashing", () => {
    render(<PublicThreatFeed items={[]} />);
    expect(screen.getByText("Public Threat Feed")).toBeInTheDocument();
  });
});
