import { db } from "@/lib/db";
import { redditTokens } from "@/lib/db/schema";
import { desc } from "drizzle-orm";

const REDDIT_AUTH_URL = "https://www.reddit.com/api/v1/authorize";
const REDDIT_TOKEN_URL = "https://www.reddit.com/api/v1/access_token";

// Reddit OAuth scopes — ads API access is controlled at account level in Business Manager,
// not via OAuth scopes. Only standard scopes are valid here.
const SCOPES = ["identity", "read", "adsread"];

interface RedditTokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  scope: string;
  token_type: string;
}

export class RedditAuthService {
  private readonly clientId: string;
  private readonly clientSecret: string;
  private readonly redirectUri: string;

  constructor() {
    this.clientId = process.env.REDDIT_CLIENT_ID ?? "";
    this.clientSecret = process.env.REDDIT_CLIENT_SECRET ?? "";
    this.redirectUri = process.env.REDDIT_REDIRECT_URI ?? "";

    if (!this.clientId || !this.clientSecret || !this.redirectUri) {
      throw new Error(
        "Missing Reddit credentials: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_REDIRECT_URI must be set"
      );
    }
  }

  getAuthUrl(state: string): string {
    const params = new URLSearchParams({
      client_id: this.clientId,
      response_type: "code",
      state,
      redirect_uri: this.redirectUri,
      duration: "permanent",
      scope: SCOPES.join(" "),
    });
    return `${REDDIT_AUTH_URL}?${params.toString()}`;
  }

  async exchangeCode(code: string): Promise<void> {
    const credentials = Buffer.from(
      `${this.clientId}:${this.clientSecret}`
    ).toString("base64");

    const response = await fetch(REDDIT_TOKEN_URL, {
      method: "POST",
      headers: {
        Authorization: `Basic ${credentials}`,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "RM-Team-AI/1.0",
      },
      body: new URLSearchParams({
        grant_type: "authorization_code",
        code,
        redirect_uri: this.redirectUri,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Reddit token exchange failed: ${response.status} ${error}`);
    }

    const data = (await response.json()) as RedditTokenResponse;
    await this.persistTokens(data);
  }

  async refreshToken(): Promise<void> {
    const current = await this.getStoredTokens();
    if (!current) throw new Error("No stored Reddit tokens to refresh");

    const credentials = Buffer.from(
      `${this.clientId}:${this.clientSecret}`
    ).toString("base64");

    const response = await fetch(REDDIT_TOKEN_URL, {
      method: "POST",
      headers: {
        Authorization: `Basic ${credentials}`,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "RM-Team-AI/1.0",
      },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: current.refreshToken,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Reddit token refresh failed: ${response.status} ${error}`);
    }

    const data = (await response.json()) as RedditTokenResponse;
    // Reddit may not return a new refresh_token on refresh — keep existing one
    if (!data.refresh_token) {
      data.refresh_token = current.refreshToken;
    }
    await this.persistTokens(data);
  }

  async getValidToken(): Promise<string> {
    const current = await this.getStoredTokens();
    if (!current) throw new Error("Reddit account not connected");

    const expiresAt = new Date(current.expiresAt);
    const now = new Date();
    // Refresh if less than 5 minutes remaining
    if (expiresAt.getTime() - now.getTime() < 5 * 60 * 1000) {
      await this.refreshToken();
      const refreshed = await this.getStoredTokens();
      if (!refreshed) throw new Error("Token refresh failed");
      return refreshed.accessToken;
    }

    return current.accessToken;
  }

  async getStoredTokens() {
    const rows = await db
      .select()
      .from(redditTokens)
      .orderBy(desc(redditTokens.id))
      .limit(1);
    return rows[0] ?? null;
  }

  async clearTokens(): Promise<void> {
    await db.delete(redditTokens);
  }

  private async persistTokens(data: RedditTokenResponse): Promise<void> {
    const expiresAt = new Date(Date.now() + data.expires_in * 1000).toISOString();
    const now = new Date().toISOString();

    // Clear existing tokens and insert fresh row (single-account model)
    await db.delete(redditTokens);
    await db.insert(redditTokens).values({
      accessToken: data.access_token,
      refreshToken: data.refresh_token,
      expiresAt,
      scope: data.scope,
      createdAt: now,
      updatedAt: now,
    });
  }
}
