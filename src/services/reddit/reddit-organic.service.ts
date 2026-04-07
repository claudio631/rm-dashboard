import { db } from "@/lib/db";
import { redditTrackedTerms, redditMentions } from "@/lib/db/schema";
import { RedditApiClient } from "./reddit-api.client";

interface RedditSearchChild {
  data: {
    id: string;
    title: string;
    url: string;
    subreddit: string;
    score: number;
    num_comments: number;
    created_utc: number;
    over_18: boolean;
  };
}

interface RedditSearchResponse {
  data: {
    children: RedditSearchChild[];
  };
}

export interface OrganicSyncSummary {
  terms_synced: number;
  new_mentions: number;
  synced_at: string;
}

export class RedditOrganicService {
  private readonly client: RedditApiClient;

  constructor() {
    this.client = new RedditApiClient();
  }

  async searchMentions(term: string): Promise<number> {
    const response = await this.client.get<RedditSearchResponse>(
      "search",
      { q: term, sort: "new", limit: "25", type: "link" },
      "oauth"
    );

    const children = response.data?.children ?? [];
    if (children.length === 0) return 0;

    const syncedAt = new Date().toISOString();
    const rows = children.map((child) => ({
      term,
      postId: child.data.id,
      title: child.data.title,
      url: child.data.url,
      subreddit: child.data.subreddit,
      score: child.data.score ?? 0,
      numComments: child.data.num_comments ?? 0,
      createdUtc: Math.floor(child.data.created_utc),
      over18: child.data.over_18 ?? false,
      syncedAt,
    }));

    const result = await db
      .insert(redditMentions)
      .values(rows)
      .onConflictDoNothing();

    return (result as { changes?: number }).changes ?? rows.length;
  }

  async syncAllTerms(): Promise<OrganicSyncSummary> {
    const terms = await db.select().from(redditTrackedTerms);

    let newMentions = 0;
    for (const { term } of terms) {
      const count = await this.searchMentions(term);
      newMentions += count;
    }

    return {
      terms_synced: terms.length,
      new_mentions: newMentions,
      synced_at: new Date().toISOString(),
    };
  }
}
