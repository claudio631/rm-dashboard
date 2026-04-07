/**
 * Unit tests: RedditAdsService campaign management methods
 * Tests updateCampaign, pauseCampaign, activateCampaign
 */

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

const mockPatch = jest.fn();
const mockGet = jest.fn();
const mockPost = jest.fn();

jest.mock("@/services/reddit/reddit-api.client", () => ({
  RedditApiClient: jest.fn().mockImplementation(() => ({
    get: mockGet,
    post: mockPost,
    patch: mockPatch,
  })),
}));

jest.mock("@/services/reddit/reddit-auth.service", () => ({
  RedditAuthService: jest.fn(),
}));

process.env.REDDIT_ADS_ACCOUNT_ID = "a2_test123";

import { RedditAdsService } from "@/services/reddit/reddit-ads.service";

const mockCampaignResponse = {
  data: {
    id: "camp_001",
    name: "Test Campaign",
    effective_status: "CAMPAIGN_PAUSED",
    configured_status: "PAUSED",
  },
};

describe("RedditAdsService — campaign management", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mocks.insert.mockReturnValue({ values: mocks.values });
    mocks.values.mockReturnValue({ onConflictDoUpdate: mocks.onConflictDoUpdate });
    mocks.onConflictDoUpdate.mockResolvedValue(undefined);
  });

  describe("updateCampaign()", () => {
    it("sends correct PATCH body and upserts DB row", async () => {
      mockPatch.mockResolvedValue(mockCampaignResponse);

      const service = new RedditAdsService();
      const result = await service.updateCampaign("camp_001", { configuredStatus: "PAUSED" });

      expect(mockPatch).toHaveBeenCalledWith(
        "ad_accounts/a2_test123/campaigns/camp_001",
        { data: { configured_status: "PAUSED" } }
      );
      expect(mocks.insert).toHaveBeenCalledTimes(1);
      expect(result).toMatchObject({ id: "camp_001", name: "Test Campaign" });
    });

    it("returns campaign with status from effective_status field", async () => {
      mockPatch.mockResolvedValue({
        data: {
          id: "camp_001",
          name: "Test Campaign",
          effective_status: "CAMPAIGN_ACTIVE",
          configured_status: "ACTIVE",
        },
      });

      const service = new RedditAdsService();
      const result = await service.updateCampaign("camp_001", { configuredStatus: "ACTIVE" });

      expect(result.status).toBe("CAMPAIGN_ACTIVE");
    });
  });

  describe("pauseCampaign()", () => {
    it("calls updateCampaign with configured_status PAUSED", async () => {
      mockPatch.mockResolvedValue(mockCampaignResponse);

      const service = new RedditAdsService();
      await service.pauseCampaign("camp_001");

      expect(mockPatch).toHaveBeenCalledWith(
        expect.stringContaining("camp_001"),
        { data: { configured_status: "PAUSED" } }
      );
    });
  });

  describe("activateCampaign()", () => {
    it("calls updateCampaign with configured_status ACTIVE", async () => {
      mockPatch.mockResolvedValue({
        data: {
          id: "camp_001",
          name: "Test Campaign",
          effective_status: "CAMPAIGN_ACTIVE",
          configured_status: "ACTIVE",
        },
      });

      const service = new RedditAdsService();
      await service.activateCampaign("camp_001");

      expect(mockPatch).toHaveBeenCalledWith(
        expect.stringContaining("camp_001"),
        { data: { configured_status: "ACTIVE" } }
      );
    });
  });
});
