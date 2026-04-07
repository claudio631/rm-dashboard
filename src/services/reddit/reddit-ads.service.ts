import { db } from "@/lib/db";
import { redditCampaigns, redditAdPerformance } from "@/lib/db/schema";
import { sql } from "drizzle-orm";
import { RedditApiClient } from "./reddit-api.client";
import { RedditAuthService } from "./reddit-auth.service";

// Reddit Ads API v3 note: the /reports endpoint returns account-level aggregates only —
// per-campaign breakdown is not available via this endpoint. Campaign metadata is synced
// separately from /campaigns. Performance rows are stored under campaign_id='account_total'.

interface RedditCampaignResponse {
  data: Array<{
    id: string;
    name: string;
    effective_status: string;
    objective: string | null;
    configured_status: string;
  }>;
}

interface RedditCampaignUpdatePayload {
  configured_status?: "ACTIVE" | "PAUSED";
  name?: string;
  daily_budget?: { amount: number; currency: string };
}

export interface CampaignUpdateResult {
  id: string;
  name: string;
  status: string;
}

interface RedditReportMetric {
  clicks: number;
  impressions: number;
  spend: number;
  ctr?: number;
  cpc?: number;
}

interface RedditReportResponse {
  data: {
    metrics: RedditReportMetric[];
    metrics_updated_at: string;
  };
}

export interface SyncSummary {
  campaigns_synced: number;
  performance_rows: number;
  synced_at: string;
}

export class RedditAdsService {
  private readonly client: RedditApiClient;

  constructor(authService?: RedditAuthService) {
    this.client = new RedditApiClient(authService);
  }

  async syncCampaigns(): Promise<number> {
    const ACCOUNT_ID = process.env.REDDIT_ADS_ACCOUNT_ID ?? "";
    if (!ACCOUNT_ID) throw new Error("REDDIT_ADS_ACCOUNT_ID is not set");

    const response = await this.client.get<RedditCampaignResponse>(
      `ad_accounts/${ACCOUNT_ID}/campaigns`
    );

    const campaigns = response.data ?? [];
    const syncedAt = new Date().toISOString();

    if (campaigns.length > 0) {
      await db
        .insert(redditCampaigns)
        .values(
          campaigns.map((c) => ({
            id: c.id,
            name: c.name,
            status: c.effective_status ?? c.configured_status,
            objective: c.objective ?? null,
            dailyBudgetAmount: null,
            currency: null,
            syncedAt,
          }))
        )
        .onConflictDoUpdate({
          target: redditCampaigns.id,
          set: {
            name: sql`excluded.name`,
            status: sql`excluded.status`,
            objective: sql`excluded.objective`,
            syncedAt: sql`excluded.synced_at`,
          },
        });
    }

    // Ensure the synthetic account_total campaign exists for performance rows
    await db
      .insert(redditCampaigns)
      .values({
        id: "account_total",
        name: "Account Total (All Campaigns)",
        status: "ACTIVE",
        objective: null,
        dailyBudgetAmount: null,
        currency: null,
        syncedAt,
      })
      .onConflictDoUpdate({
        target: redditCampaigns.id,
        set: { syncedAt: sql`excluded.synced_at` },
      });

    return campaigns.length;
  }

  async syncPerformance(startDate: string, endDate: string): Promise<number> {
    const ACCOUNT_ID = process.env.REDDIT_ADS_ACCOUNT_ID ?? "";
    if (!ACCOUNT_ID) throw new Error("REDDIT_ADS_ACCOUNT_ID is not set");

    // Reddit Ads API v3 /reports returns account-level aggregate only (no per-campaign breakdown).
    // Stored as a single row per day under campaign_id='account_total'.
    const response = await this.client.post<RedditReportResponse>(
      `ad_accounts/${ACCOUNT_ID}/reports`,
      {
        data: {
          fields: ["IMPRESSIONS", "CLICKS", "SPEND", "CTR", "CPC"],
          starts_at: `${startDate}T00:00:00Z`,
          ends_at: `${endDate}T00:00:00Z`,
        },
      }
    );

    const metrics = response.data?.metrics ?? [];
    if (metrics.length === 0) return 0;

    const metric = metrics[0];
    const syncedAt = new Date().toISOString();

    // Store the aggregate as a single row keyed to endDate
    // (the API does not support daily breakdown — represents the full period total)
    const ctr =
      metric.impressions > 0
        ? (metric.clicks / metric.impressions).toFixed(6)
        : "0";

    await db
      .insert(redditAdPerformance)
      .values({
        campaignId: "account_total",
        date: endDate,
        impressions: metric.impressions ?? 0,
        clicks: metric.clicks ?? 0,
        spend: Math.round(metric.spend ?? 0),
        conversions: 0,
        ctr,
        ecpc: metric.cpc ? Math.round(metric.cpc) : null,
        ecpa: null,
        syncedAt,
      })
      .onConflictDoUpdate({
        target: [redditAdPerformance.campaignId, redditAdPerformance.date],
        set: {
          impressions: sql`excluded.impressions`,
          clicks: sql`excluded.clicks`,
          spend: sql`excluded.spend`,
          ctr: sql`excluded.ctr`,
          ecpc: sql`excluded.ecpc`,
          syncedAt: sql`excluded.synced_at`,
        },
      });

    return 1;
  }

  async updateCampaign(
    campaignId: string,
    updates: { configuredStatus?: "ACTIVE" | "PAUSED"; name?: string; dailyBudgetAmount?: number }
  ): Promise<CampaignUpdateResult> {
    const ACCOUNT_ID = process.env.REDDIT_ADS_ACCOUNT_ID ?? "";
    if (!ACCOUNT_ID) throw new Error("REDDIT_ADS_ACCOUNT_ID is not set");

    const payload: { data: RedditCampaignUpdatePayload } = { data: {} };
    if (updates.configuredStatus) payload.data.configured_status = updates.configuredStatus;
    if (updates.name) payload.data.name = updates.name;
    if (updates.dailyBudgetAmount !== undefined) {
      payload.data.daily_budget = { amount: updates.dailyBudgetAmount, currency: "USD" };
    }

    const response = await this.client.patch<{ data: { id: string; name: string; effective_status: string; configured_status: string } }>(
      `ad_accounts/${ACCOUNT_ID}/campaigns/${campaignId}`,
      payload
    );

    const c = response.data;
    const syncedAt = new Date().toISOString();
    const status = c.effective_status ?? c.configured_status;

    await db
      .insert(redditCampaigns)
      .values({ id: c.id, name: c.name, status, objective: null, dailyBudgetAmount: null, currency: null, syncedAt })
      .onConflictDoUpdate({
        target: redditCampaigns.id,
        set: {
          name: sql`excluded.name`,
          status: sql`excluded.status`,
          syncedAt: sql`excluded.synced_at`,
        },
      });

    return { id: c.id, name: c.name, status };
  }

  async pauseCampaign(campaignId: string): Promise<CampaignUpdateResult> {
    return this.updateCampaign(campaignId, { configuredStatus: "PAUSED" });
  }

  async activateCampaign(campaignId: string): Promise<CampaignUpdateResult> {
    return this.updateCampaign(campaignId, { configuredStatus: "ACTIVE" });
  }

  async syncLast30Days(): Promise<SyncSummary> {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - 30);

    const startDate = start.toISOString().split("T")[0];
    const endDate = end.toISOString().split("T")[0];

    const campaigns_synced = await this.syncCampaigns();
    const performance_rows = await this.syncPerformance(startDate, endDate);

    return {
      campaigns_synced,
      performance_rows,
      synced_at: new Date().toISOString(),
    };
  }
}
