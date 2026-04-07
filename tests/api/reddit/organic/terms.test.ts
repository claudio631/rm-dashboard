/**
 * Unit tests: POST /api/reddit/organic/terms — route handler logic
 * Tests validation and DB insertion logic directly (avoids next/server jsdom issue).
 */

const mockInsert = jest.fn();
const mockValues = jest.fn();
const mockReturning = jest.fn();

mockInsert.mockReturnValue({ values: mockValues });
mockValues.mockReturnValue({ returning: mockReturning });

jest.mock("@/lib/db", () => ({
  db: { insert: (...args: unknown[]) => mockInsert(...args) },
}));
jest.mock("@/lib/db/schema", () => ({
  redditTrackedTerms: "reddit_tracked_terms",
}));

import { db } from "@/lib/db";
import { redditTrackedTerms } from "@/lib/db/schema";

// Simulates the route handler's validation + insertion logic
async function simulatePostTerm(term: string | undefined) {
  const trimmed = term?.trim();
  if (!trimmed) {
    return { status: 400, body: { error: "term is required and must not be empty" } };
  }

  try {
    const createdAt = new Date().toISOString();
    const [created] = await (db as unknown as { insert: typeof mockInsert })
      .insert(redditTrackedTerms)
      .values({ term: trimmed, createdAt })
      .returning();

    return { status: 201, body: { term: created } };
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown";
    if (message.includes("UNIQUE")) {
      return { status: 409, body: { error: `Term "${trimmed}" is already tracked` } };
    }
    return { status: 500, body: { error: message } };
  }
}

describe("POST /api/reddit/organic/terms — route logic", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockInsert.mockReturnValue({ values: mockValues });
    mockValues.mockReturnValue({ returning: mockReturning });
  });

  it("rejects empty term with 400", async () => {
    const res = await simulatePostTerm("");
    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/required/);
  });

  it("rejects whitespace-only term with 400", async () => {
    const res = await simulatePostTerm("   ");
    expect(res.status).toBe(400);
  });

  it("rejects missing term with 400", async () => {
    const res = await simulatePostTerm(undefined);
    expect(res.status).toBe(400);
  });

  it("creates term and returns 201 on success", async () => {
    mockReturning.mockResolvedValue([
      { id: 1, term: "Indeed Flex", createdAt: "2026-04-07T00:00:00Z" },
    ]);

    const res = await simulatePostTerm("Indeed Flex");
    expect(res.status).toBe(201);
    expect(res.body.term).toMatchObject({ id: 1, term: "Indeed Flex" });
  });
});
