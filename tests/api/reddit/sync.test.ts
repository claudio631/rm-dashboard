/**
 * Unit test: /api/reddit/sync — RedditAdsService.syncLast30Days() shape
 * Tests the service logic directly, following project pattern (avoids next/server in jsdom).
 */

const mockSyncCampaigns = jest.fn();
const mockSyncPerformance = jest.fn();

jest.mock("@/services/reddit/reddit-api.client", () => ({
  RedditApiClient: jest.fn().mockImplementation(() => ({
    get: mockSyncCampaigns,
    post: mockSyncPerformance,
  })),
}));
jest.mock("@/services/reddit/reddit-auth.service", () => ({
  RedditAuthService: jest.fn(),
}));

const mocks = {
  insert: jest.fn(),
  onConflictDoUpdate: jest.fn().mockResolvedValue(undefined),
  values: jest.fn(),
};
mocks.insert.mockReturnValue({ values: mocks.values });
mocks.values.mockReturnValue({ onConflictDoUpdate: mocks.onConflictDoUpdate });

jest.mock("@/lib/db", () => ({
  db: { insert: (...args: unknown[]) => mocks.insert(...args) },
}));
jest.mock("@/lib/db/schema", () => ({
  redditCampaigns: "reddit_campaigns",
  redditAdPerformance: "reddit_ad_performance",
}));
jest.mock("drizzle-orm", () => ({
  sql: jest.fn((s: TemplateStringsArray) => s[0]),
}));

process.env.REDDIT_ADS_ACCOUNT_ID = "a2_test123";

import { RedditAdsService } from "@/services/reddit/reddit-ads.service";

describe("POST /api/reddit/sync — syncLast30Days()", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mocks.insert.mockReturnValue({ values: mocks.values });
    mocks.values.mockReturnValue({ onConflictDoUpdate: mocks.onConflictDoUpdate });
    mocks.onConflictDoUpdate.mockResolvedValue(undefined);
  });

  it("returns summary with campaigns_synced, performance_rows, synced_at", async () => {
    mockSyncCampaigns.mockResolvedValue({ data: [{ id: "c1", name: "C1", effective_status: "ACTIVE", objective: "CLICKS", configured_status: "ACTIVE" }] });
    mockSyncPerformance.mockResolvedValue({
      data: { metrics: [{ clicks: 100, impressions: 10000, spend: 100000000, ctr: 0.01, cpc: 1000000 }], metrics_updated_at: "2026-04-03T00:00:00Z" }
    });

    const service = new RedditAdsService();
    const summary = await service.syncLast30Days();

    expect(summary).toHaveProperty("campaigns_synced");
    expect(summary).toHaveProperty("performance_rows");
    expect(summary).toHaveProperty("synced_at");
    expect(typeof summary.campaigns_synced).toBe("number");
    expect(typeof summary.performance_rows).toBe("number");
    expect(typeof summary.synced_at).toBe("string");
  });

  it("synced_at is a valid ISO string", async () => {
    mockSyncCampaigns.mockResolvedValue({ data: [] });
    mockSyncPerformance.mockResolvedValue({
      data: { metrics: [], metrics_updated_at: "2026-04-03T00:00:00Z" }
    });

    const service = new RedditAdsService();
    const summary = await service.syncLast30Days();

    expect(() => new Date(summary.synced_at)).not.toThrow();
    expect(new Date(summary.synced_at).toString()).not.toBe("Invalid Date");
  });
});
