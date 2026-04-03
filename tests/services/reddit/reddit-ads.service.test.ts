import { RedditAdsService } from "@/services/reddit/reddit-ads.service";

// Hoisting-safe: define mock fns inside the factory, export refs via module variable
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
  sql: jest.fn((strings: TemplateStringsArray) => strings[0]),
}));

const mockGet = jest.fn();
const mockPost = jest.fn();
jest.mock("@/services/reddit/reddit-api.client", () => ({
  RedditApiClient: jest.fn().mockImplementation(() => ({
    get: mockGet,
    post: mockPost,
  })),
}));
jest.mock("@/services/reddit/reddit-auth.service", () => ({
  RedditAuthService: jest.fn(),
}));

process.env.REDDIT_ADS_ACCOUNT_ID = "a2_test123";

describe("RedditAdsService", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mocks.insert.mockReturnValue({ values: mocks.values });
    mocks.values.mockReturnValue({ onConflictDoUpdate: mocks.onConflictDoUpdate });
    mocks.onConflictDoUpdate.mockResolvedValue(undefined);
  });

  describe("syncCampaigns()", () => {
    it("maps API response correctly to DB schema fields", async () => {
      mockGet.mockResolvedValue({
        data: [
          {
            id: "123456789",
            name: "Test Campaign",
            effective_status: "CAMPAIGN_ACTIVE",
            objective: "CLICKS",
            configured_status: "ACTIVE",
          },
        ],
      });

      const service = new RedditAdsService();
      const count = await service.syncCampaigns();

      expect(count).toBe(1);
      // insert called twice: real campaigns + synthetic account_total
      expect(mocks.insert).toHaveBeenCalledTimes(2);
      const firstCallValues = mocks.values.mock.calls[0][0];
      expect(firstCallValues).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            id: "123456789",
            name: "Test Campaign",
            status: "CAMPAIGN_ACTIVE",
            objective: "CLICKS",
          }),
        ])
      );
    });

    it("falls back to configured_status when effective_status is missing", async () => {
      mockGet.mockResolvedValue({
        data: [
          {
            id: "987",
            name: "No Effective",
            effective_status: undefined,
            objective: null,
            configured_status: "PAUSED",
          },
        ],
      });

      const service = new RedditAdsService();
      await service.syncCampaigns();

      const firstCallValues = mocks.values.mock.calls[0][0];
      expect(firstCallValues[0]).toMatchObject({ status: "PAUSED" });
    });

    it("inserts synthetic account_total campaign", async () => {
      mockGet.mockResolvedValue({ data: [] });

      const service = new RedditAdsService();
      await service.syncCampaigns();

      // With empty campaigns, only the synthetic insert happens (one insert call)
      const syntheticValues = mocks.values.mock.calls[0][0];
      expect(syntheticValues).toMatchObject({
        id: "account_total",
        name: "Account Total (All Campaigns)",
      });
    });
  });

  describe("syncPerformance()", () => {
    it("computes CTR correctly from clicks and impressions", async () => {
      mockPost.mockResolvedValue({
        data: {
          metrics: [
            {
              clicks: 500,
              impressions: 100000,
              spend: 5000000000,
              ctr: 0.005,
              cpc: 10000000,
            },
          ],
          metrics_updated_at: "2026-04-03T00:00:00Z",
        },
      });

      const service = new RedditAdsService();
      const rows = await service.syncPerformance("2026-03-01", "2026-04-01");

      expect(rows).toBe(1);
      const insertedValues = mocks.values.mock.calls[0][0];
      // clicks / impressions = 500 / 100000 = 0.005000
      expect(insertedValues).toMatchObject({
        campaignId: "account_total",
        date: "2026-04-01",
        clicks: 500,
        impressions: 100000,
        ctr: "0.005000",
      });
    });

    it("handles zero impressions without division by zero", async () => {
      mockPost.mockResolvedValue({
        data: {
          metrics: [{ clicks: 0, impressions: 0, spend: 0, ctr: 0, cpc: 0 }],
          metrics_updated_at: "2026-04-03T00:00:00Z",
        },
      });

      const service = new RedditAdsService();
      const rows = await service.syncPerformance("2026-03-01", "2026-04-01");

      expect(rows).toBe(1);
      const insertedValues = mocks.values.mock.calls[0][0];
      expect(insertedValues.ctr).toBe("0");
    });

    it("returns 0 when API returns empty metrics array", async () => {
      mockPost.mockResolvedValue({
        data: { metrics: [], metrics_updated_at: "2026-04-03T00:00:00Z" },
      });

      const service = new RedditAdsService();
      const rows = await service.syncPerformance("2026-03-01", "2026-04-01");

      expect(rows).toBe(0);
      expect(mocks.insert).not.toHaveBeenCalled();
    });
  });
});
