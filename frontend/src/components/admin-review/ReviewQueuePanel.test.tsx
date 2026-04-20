import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import ReviewQueuePanel from "./ReviewQueuePanel";
import type { ReviewItem } from "../../types/publicThreat";

const mockItems: ReviewItem[] = [
  { id: "review-301", type: "external_report_upload", status: "pending_review", note: "Check redactions." },
  { id: "review-302", type: "report_publish_request", status: "approved", note: "Ready for public feed." },
];

describe("ReviewQueuePanel", () => {
  it("renders the heading", () => {
    render(<ReviewQueuePanel items={mockItems} />);
    expect(screen.getByText("Moderation Queue")).toBeInTheDocument();
  });

  it("renders all review item IDs", () => {
    render(<ReviewQueuePanel items={mockItems} />);
    expect(screen.getByText("review-301")).toBeInTheDocument();
    expect(screen.getByText("review-302")).toBeInTheDocument();
  });

  it("renders item types and notes", () => {
    render(<ReviewQueuePanel items={mockItems} />);
    expect(screen.getByText("external_report_upload")).toBeInTheDocument();
    expect(screen.getByText("Check redactions.")).toBeInTheDocument();
  });

  it("shows Approve and Reject buttons only for pending_review items", () => {
    render(<ReviewQueuePanel items={mockItems} />);
    expect(screen.getByRole("button", { name: /approve/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /reject/i })).toBeInTheDocument();
  });

  it("does not show action buttons for already-approved items", () => {
    render(<ReviewQueuePanel items={[mockItems[1]]} />);
    expect(screen.queryByRole("button", { name: /approve/i })).not.toBeInTheDocument();
  });

  it("clicking Approve changes status to approved", () => {
    render(<ReviewQueuePanel items={[mockItems[0]]} />);
    fireEvent.click(screen.getByRole("button", { name: /approve/i }));
    expect(screen.getByText("approved")).toBeInTheDocument();
  });

  it("clicking Reject changes status to rejected", () => {
    render(<ReviewQueuePanel items={[mockItems[0]]} />);
    fireEvent.click(screen.getByRole("button", { name: /reject/i }));
    expect(screen.getByText("rejected")).toBeInTheDocument();
  });

  it("hides action buttons after a decision is made", () => {
    render(<ReviewQueuePanel items={[mockItems[0]]} />);
    fireEvent.click(screen.getByRole("button", { name: /approve/i }));
    expect(screen.queryByRole("button", { name: /approve/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reject/i })).not.toBeInTheDocument();
  });

  it("renders empty list without crashing", () => {
    render(<ReviewQueuePanel items={[]} />);
    expect(screen.getByText("Moderation Queue")).toBeInTheDocument();
  });
});
