import { RedditAuthService } from "@/services/reddit/reddit-auth.service";

// Mock the db module to avoid SQLite in unit tests
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

// Updated after live API testing: ads:read/ads:manage are invalid Reddit OAuth scopes.
// Ads API access is account-level via Business Manager. adsread is the correct scope.
const REQUIRED_SCOPES = ["identity", "read", "adsread"];

describe("RedditAuthService", () => {
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

  describe("getAuthUrl", () => {
    it("generates a URL pointing to Reddit authorization endpoint", () => {
      const service = new RedditAuthService();
      const url = service.getAuthUrl("test-state");
      expect(url).toContain("https://www.reddit.com/api/v1/authorize");
    });

    it("includes all required scopes", () => {
      const service = new RedditAuthService();
      const url = service.getAuthUrl("test-state");
      const parsed = new URL(url);
      const scopes = parsed.searchParams.get("scope")?.split(" ") ?? [];
      REQUIRED_SCOPES.forEach((scope) => {
        expect(scopes).toContain(scope);
      });
    });

    it("includes the state parameter", () => {
      const service = new RedditAuthService();
      const url = service.getAuthUrl("my-state-value");
      const parsed = new URL(url);
      expect(parsed.searchParams.get("state")).toBe("my-state-value");
    });

    it("includes the redirect_uri", () => {
      const service = new RedditAuthService();
      const url = service.getAuthUrl("state");
      const parsed = new URL(url);
      expect(parsed.searchParams.get("redirect_uri")).toBe(
        "http://localhost:3000/api/reddit/callback"
      );
    });

    it("requests permanent duration for refresh token", () => {
      const service = new RedditAuthService();
      const url = service.getAuthUrl("state");
      const parsed = new URL(url);
      expect(parsed.searchParams.get("duration")).toBe("permanent");
    });

    it("throws if credentials are missing", () => {
      delete process.env.REDDIT_CLIENT_ID;
      expect(() => new RedditAuthService()).toThrow(
        "Missing Reddit credentials"
      );
    });
  });
});
