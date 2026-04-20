import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import MetricsBoard from "./MetricsBoard";
import type { DashboardMetric } from "../../types/dashboard";

const mockMetrics: DashboardMetric[] = [
  { label: "Queued Jobs", value: "3", note: "Waiting for enrichment." },
  { label: "Private Reports", value: "8", note: "Workspace only." },
  { label: "Public Posts", value: "2", note: "Already approved." },
];

describe("MetricsBoard", () => {
  it("renders all metric labels", () => {
    render(<MetricsBoard metrics={mockMetrics} />);
    expect(screen.getByText("Queued Jobs")).toBeInTheDocument();
    expect(screen.getByText("Private Reports")).toBeInTheDocument();
    expect(screen.getByText("Public Posts")).toBeInTheDocument();
  });

  it("renders all metric values", () => {
    render(<MetricsBoard metrics={mockMetrics} />);
    expect(screen.getByText("3")).toBeInTheDocument();
    expect(screen.getByText("8")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
  });

  it("renders all metric notes", () => {
    render(<MetricsBoard metrics={mockMetrics} />);
    expect(screen.getByText("Waiting for enrichment.")).toBeInTheDocument();
    expect(screen.getByText("Workspace only.")).toBeInTheDocument();
    expect(screen.getByText("Already approved.")).toBeInTheDocument();
  });

  it("renders skeleton cards when loading is true", () => {
    render(<MetricsBoard metrics={mockMetrics} loading={true} />);
    const skeletons = screen.getAllByText("Loading…");
    expect(skeletons.length).toBe(3);
  });

  it("does not render metrics when loading", () => {
    render(<MetricsBoard metrics={mockMetrics} loading={true} />);
    expect(screen.queryByText("Queued Jobs")).not.toBeInTheDocument();
  });

  it("renders metrics when loading is false", () => {
    render(<MetricsBoard metrics={mockMetrics} loading={false} />);
    expect(screen.getByText("Queued Jobs")).toBeInTheDocument();
  });

  it("renders empty state with no metrics", () => {
    render(<MetricsBoard metrics={[]} />);
    expect(screen.queryByText("Loading…")).not.toBeInTheDocument();
  });
});
