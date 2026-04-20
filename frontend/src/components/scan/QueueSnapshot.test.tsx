import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import QueueSnapshot from "./QueueSnapshot";

describe("QueueSnapshot", () => {
  it("renders the section heading", () => {
    render(<QueueSnapshot />);
    expect(screen.getByText("Scan Queue")).toBeInTheDocument();
  });

  it("renders all mock queue item IDs", () => {
    render(<QueueSnapshot />);
    expect(screen.getByText("job-101")).toBeInTheDocument();
    expect(screen.getByText("job-102")).toBeInTheDocument();
    expect(screen.getByText("job-103")).toBeInTheDocument();
  });

  it("renders state badges for each item", () => {
    render(<QueueSnapshot />);
    expect(screen.getByTestId("state-badge-completed")).toBeInTheDocument();
    expect(screen.getByTestId("state-badge-enriching")).toBeInTheDocument();
    expect(screen.getByTestId("state-badge-queued")).toBeInTheDocument();
  });

  it("shows artifact type and AI mode for each item", () => {
    render(<QueueSnapshot />);
    expect(screen.getByText(/url · AI: local/i)).toBeInTheDocument();
    expect(screen.getByText(/file · AI: api/i)).toBeInTheDocument();
    expect(screen.getByText(/email_signal · AI: off/i)).toBeInTheDocument();
  });
});
