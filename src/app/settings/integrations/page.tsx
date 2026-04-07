import { RedditAuthService } from "@/services/reddit/reddit-auth.service";
import { db } from "@/lib/db";
import { redditAdPerformance, redditCampaigns, redditTrackedTerms, redditMentions } from "@/lib/db/schema";
import { desc, count, sum, gte, ne, and } from "drizzle-orm";
import { RedditCampaignTable } from "@/components/reddit/RedditCampaignTable";
import { RedditOrganicMonitoring } from "@/components/reddit/RedditOrganicMonitoring";

interface RedditStatus {
  connected: boolean;
  scopes: string[];
  expires_at: string | null;
}

interface SyncSummary {
  lastSync: string | null;
  totalCampaigns: number;
  last7dSpend: number; // microcurrency
}

async function getRedditStatus(): Promise<RedditStatus> {
  try {
    const authService = new RedditAuthService();
    const tokens = await authService.getStoredTokens();
    if (!tokens) return { connected: false, scopes: [], expires_at: null };
    return {
      connected: true,
      scopes: tokens.scope.split(" "),
      expires_at: tokens.expiresAt,
    };
  } catch {
    return { connected: false, scopes: [], expires_at: null };
  }
}

async function getSyncSummary(): Promise<SyncSummary> {
  try {
    const [lastRow] = await db
      .select({ syncedAt: redditAdPerformance.syncedAt })
      .from(redditAdPerformance)
      .orderBy(desc(redditAdPerformance.syncedAt))
      .limit(1);

    const [campaignCount] = await db
      .select({ value: count() })
      .from(redditCampaigns)
      .where(
        gte(redditCampaigns.id, "0") // exclude 'account_total' synthetic row
      );

    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - 7);
    const cutoffDate = cutoff.toISOString().split("T")[0];

    const [spendRow] = await db
      .select({ value: sum(redditAdPerformance.spend) })
      .from(redditAdPerformance)
      .where(gte(redditAdPerformance.date, cutoffDate));

    return {
      lastSync: lastRow?.syncedAt ?? null,
      totalCampaigns: Math.max(0, (campaignCount?.value ?? 0) - 1), // subtract synthetic row
      last7dSpend: Number(spendRow?.value ?? 0),
    };
  } catch {
    return { lastSync: null, totalCampaigns: 0, last7dSpend: 0 };
  }
}

function formatSpend(microcurrency: number): string {
  return (microcurrency / 1_000_000).toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  });
}

async function getTrackedTerms() {
  try {
    return await db.select().from(redditTrackedTerms);
  } catch {
    return [];
  }
}

async function getRecentMentions() {
  try {
    const cutoffUtc = Math.floor(Date.now() / 1000) - 30 * 24 * 60 * 60;
    return await db
      .select()
      .from(redditMentions)
      .where(and(gte(redditMentions.createdUtc, cutoffUtc), ne(redditMentions.over18, true)))
      .orderBy(desc(redditMentions.createdUtc))
      .limit(50);
  } catch {
    return [];
  }
}

async function getCampaigns() {
  try {
    return await db
      .select()
      .from(redditCampaigns)
      .where(ne(redditCampaigns.id, "account_total"));
  } catch {
    return [];
  }
}

export default async function IntegrationsPage() {
  const [reddit, sync, campaigns, trackedTerms, recentMentions] = await Promise.all([
    getRedditStatus(),
    getSyncSummary(),
    getCampaigns(),
    getTrackedTerms(),
    getRecentMentions(),
  ]);

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Integrations</h1>

      <div className="max-w-2xl">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-orange-500 flex items-center justify-center text-white font-bold text-sm">
                R
              </div>
              <div>
                <h2 className="text-base font-semibold text-gray-900">Reddit Ads</h2>
                <p className="text-sm text-gray-500">
                  Pull campaign analytics, manage ads, and monitor subreddits
                </p>
              </div>
            </div>

            <span
              className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
                reddit.connected
                  ? "bg-green-50 text-green-700"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              <span
                className={`w-1.5 h-1.5 rounded-full ${
                  reddit.connected ? "bg-green-500" : "bg-gray-400"
                }`}
              />
              {reddit.connected ? "Connected" : "Disconnected"}
            </span>
          </div>

          {reddit.connected && (
            <div className="mt-4 pt-4 border-t border-gray-100 space-y-2 text-sm text-gray-600">
              <div>
                <span className="font-medium">Scopes:</span>{" "}
                {reddit.scopes.join(", ")}
              </div>
              {reddit.expires_at && (
                <div>
                  <span className="font-medium">Token expires:</span>{" "}
                  {new Date(reddit.expires_at).toLocaleString()}
                </div>
              )}
            </div>
          )}

          {reddit.connected && (
            <div className="mt-4 pt-4 border-t border-gray-100">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
                Performance Data
              </h3>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div>
                  <p className="text-xs text-gray-500">Last Sync</p>
                  <p className="text-sm font-medium text-gray-900 mt-0.5">
                    {sync.lastSync
                      ? new Date(sync.lastSync).toLocaleString()
                      : "Never"}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Campaigns</p>
                  <p className="text-sm font-medium text-gray-900 mt-0.5">
                    {sync.totalCampaigns > 0 ? sync.totalCampaigns : "—"}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Last 7d Spend</p>
                  <p className="text-sm font-medium text-gray-900 mt-0.5">
                    {sync.last7dSpend > 0 ? formatSpend(sync.last7dSpend) : "—"}
                  </p>
                </div>
              </div>

              <form action="/api/reddit/sync" method="POST">
                <button
                  type="submit"
                  className="px-3 py-1.5 text-xs font-medium text-orange-600 bg-white border border-orange-200 rounded-md hover:bg-orange-50 transition-colors"
                >
                  Sync Now
                </button>
              </form>
            </div>
          )}

          {reddit.connected && campaigns.length > 0 && (
            <div className="mt-4 pt-4 border-t border-gray-100">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
                Campaigns
              </h3>
              <RedditCampaignTable initialCampaigns={campaigns} />
            </div>
          )}

          {reddit.connected && (
            <div className="mt-4 pt-4 border-t border-gray-100">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">
                Organic Monitoring
              </h3>
              <RedditOrganicMonitoring
                initialTerms={trackedTerms}
                initialMentions={recentMentions}
              />
            </div>
          )}

          <div className="mt-4 pt-4 border-t border-gray-100 flex gap-3">
            {reddit.connected ? (
              <form action="/api/reddit/disconnect" method="POST">
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-red-600 bg-white border border-red-200 rounded-md hover:bg-red-50 transition-colors"
                >
                  Disconnect
                </button>
              </form>
            ) : (
              <a
                href="/api/reddit/auth"
                className="px-4 py-2 text-sm font-medium text-white bg-orange-500 rounded-md hover:bg-orange-600 transition-colors"
              >
                Connect Reddit
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
