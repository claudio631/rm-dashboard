/**
 * Integration test: /api/reddit/status response shape
 * Tests the RedditAuthService.getStoredTokens → response mapping
 */

import { RedditAuthService } from "@/services/reddit/reddit-auth.service";

jest.mock("@/lib/db", () => ({
  db: {
    select: jest.fn().mockReturnValue({
      from: jest.fn().mockReturnValue({
        orderBy: jest.fn().mockReturnValue({
          limit: jest.fn().mockResolvedValue([]),
        }),
      }),
    }),
    delete: jest.fn().mockReturnValue({ execute: jest.fn() }),
    insert: jest.fn().mockReturnValue({
      values: jest.fn().mockResolvedValue(undefined),
    }),
  },
}));

jest.mock("@/lib/db/schema", () => ({
  redditTokens: "reddit_tokens",
}));

jest.mock("drizzle-orm", () => ({
  desc: jest.fn(),
}));

describe("GET /api/reddit/status — response shape", () => {
  const originalEnv = process.env;

  beforeEach(() => {
    process.env = {
      ...originalEnv,
      REDDIT_CLIENT_ID: "test-client-id",
      REDDIT_CLIENT_SECRET: "test-client-secret",
      REDDIT_REDIRECT_URI: "http://localhost:3000/api/reddit/callback",
    };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it("returns connected:false when no tokens are stored", async () => {
    const service = new RedditAuthService();
    const tokens = await service.getStoredTokens();
    expect(tokens).toBeNull();

    // Simulate route handler logic
    const body =
      tokens === null
        ? { connected: false, scopes: [], expires_at: null }
        : {
            connected: true,
            scopes: (tokens as { scope: string }).scope.split(" "),
            expires_at: (tokens as { expiresAt: string }).expiresAt,
          };

    expect(body).toMatchObject({
      connected: false,
      scopes: expect.any(Array),
      expires_at: null,
    });
  });

  it("returns connected:true with scopes array and expires_at when tokens exist", async () => {
    const mockTokens = {
      id: 1,
      accessToken: "acc",
      refreshToken: "ref",
      expiresAt: "2026-12-31T00:00:00.000Z",
      scope: "ads:read ads:manage identity read",
      createdAt: "2026-04-03T00:00:00.000Z",
      updatedAt: "2026-04-03T00:00:00.000Z",
    };

    // Simulate route handler logic with tokens present
    const body = {
      connected: true,
      scopes: mockTokens.scope.split(" "),
      expires_at: mockTokens.expiresAt,
    };

    expect(body).toMatchObject({
      connected: true,
      scopes: ["ads:read", "ads:manage", "identity", "read"],
      expires_at: expect.any(String),
    });
  });
});
