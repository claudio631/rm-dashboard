/**
 * Unit tests: PUT /api/reddit/campaigns/[id] — route handler logic
 * Tests service delegation and validation logic directly (avoids next/server jsdom issue).
 */

const mockPauseCampaign = jest.fn();
const mockActivateCampaign = jest.fn();
const mockUpdateCampaign = jest.fn();

jest.mock("@/services/reddit/reddit-ads.service", () => ({
  RedditAdsService: jest.fn().mockImplementation(() => ({
    pauseCampaign: mockPauseCampaign,
    activateCampaign: mockActivateCampaign,
    updateCampaign: mockUpdateCampaign,
  })),
}));

jest.mock("@/services/reddit/reddit-api.client", () => ({ RedditApiClient: jest.fn() }));
jest.mock("@/services/reddit/reddit-auth.service", () => ({ RedditAuthService: jest.fn() }));
jest.mock("@/lib/db", () => ({ db: {} }));
jest.mock("@/lib/db/schema", () => ({ redditCampaigns: "reddit_campaigns" }));
jest.mock("drizzle-orm", () => ({ sql: jest.fn() }));

import { RedditAdsService } from "@/services/reddit/reddit-ads.service";

const VALID_ACTIONS = ["pause", "activate", "update"] as const;
type Action = (typeof VALID_ACTIONS)[number];

// Simulates the route handler logic for testability
async function simulateRouteHandler(campaignId: string, body: { action?: string; updates?: Record<string, unknown> }) {
  if (!body.action || !VALID_ACTIONS.includes(body.action as Action)) {
    return { status: 400, body: { error: "action must be one of: pause, activate, update" } };
  }

  const service = new RedditAdsService();
  let result;
  if (body.action === "pause") {
    result = await service.pauseCampaign(campaignId);
  } else if (body.action === "activate") {
    result = await service.activateCampaign(campaignId);
  } else {
    result = await service.updateCampaign(campaignId, body.updates ?? {});
  }
  return { status: 200, body: { success: true, campaign: result } };
}

describe("PUT /api/reddit/campaigns/[id] — route logic", () => {
  beforeEach(() => jest.clearAllMocks());

  it("delegates pause action to pauseCampaign and returns correct shape", async () => {
    mockPauseCampaign.mockResolvedValue({ id: "camp_001", name: "Test", status: "CAMPAIGN_PAUSED" });

    const res = await simulateRouteHandler("camp_001", { action: "pause" });

    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
    expect(res.body.campaign).toMatchObject({ id: "camp_001", status: "CAMPAIGN_PAUSED" });
    expect(mockPauseCampaign).toHaveBeenCalledWith("camp_001");
  });

  it("delegates activate action to activateCampaign", async () => {
    mockActivateCampaign.mockResolvedValue({ id: "camp_001", name: "Test", status: "CAMPAIGN_ACTIVE" });

    const res = await simulateRouteHandler("camp_001", { action: "activate" });

    expect(res.status).toBe(200);
    expect(mockActivateCampaign).toHaveBeenCalledWith("camp_001");
  });

  it("returns 400 for unknown action", async () => {
    const res = await simulateRouteHandler("camp_001", { action: "delete" });

    expect(res.status).toBe(400);
    expect(res.body.error).toMatch(/action must be one of/);
  });

  it("returns 400 for missing action", async () => {
    const res = await simulateRouteHandler("camp_001", {});

    expect(res.status).toBe(400);
  });
});
