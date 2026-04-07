import { RedditAuthService } from "./reddit-auth.service";

export interface RedditApiError {
  status: number;
  code: string;
  message: string;
}

const REDDIT_ADS_API_BASE = "https://ads-api.reddit.com/api/v3";
const REDDIT_OAUTH_BASE = "https://oauth.reddit.com";

export class RedditApiClient {
  private readonly authService: RedditAuthService;

  constructor(authService?: RedditAuthService) {
    this.authService = authService ?? new RedditAuthService();
  }

  async get<T>(
    endpoint: string,
    params?: Record<string, string>,
    baseUrl: "ads" | "oauth" = "ads"
  ): Promise<T> {
    const url = this.buildUrl(endpoint, baseUrl, params);
    return this.request<T>("GET", url);
  }

  async post<T>(
    endpoint: string,
    body?: unknown,
    baseUrl: "ads" | "oauth" = "ads"
  ): Promise<T> {
    const url = this.buildUrl(endpoint, baseUrl);
    return this.request<T>("POST", url, body);
  }

  async patch<T>(
    endpoint: string,
    body?: unknown,
    baseUrl: "ads" | "oauth" = "ads"
  ): Promise<T> {
    const url = this.buildUrl(endpoint, baseUrl);
    return this.request<T>("PATCH", url, body);
  }

  private buildUrl(
    endpoint: string,
    baseUrl: "ads" | "oauth",
    params?: Record<string, string>
  ): string {
    const base = baseUrl === "ads" ? REDDIT_ADS_API_BASE : REDDIT_OAUTH_BASE;
    const url = new URL(`${base}/${endpoint.replace(/^\//, "")}`);
    if (params) {
      Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
    }
    return url.toString();
  }

  private async request<T>(
    method: string,
    url: string,
    body?: unknown,
    isRetry = false
  ): Promise<T> {
    let token: string;
    try {
      token = await this.authService.getValidToken();
    } catch {
      throw this.makeError(401, "NOT_CONNECTED", "Reddit account not connected");
    }

    const response = await fetch(url, {
      method,
      headers: {
        Authorization: `bearer ${token}`,
        "Content-Type": "application/json",
        "User-Agent": "RM-Team-AI/1.0",
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });

    if (response.status === 401 && !isRetry) {
      // Token may have been revoked — attempt one refresh and retry
      await this.authService.refreshToken();
      return this.request<T>(method, url, body, true);
    }

    if (!response.ok) {
      const error = await this.parseErrorResponse(response);
      throw error;
    }

    return response.json() as Promise<T>;
  }

  private async parseErrorResponse(response: Response): Promise<RedditApiError> {
    let code = "REDDIT_API_ERROR";
    let message = `HTTP ${response.status}`;
    try {
      const body = (await response.json()) as Record<string, unknown>;
      if (typeof body.message === "string") message = body.message;
      if (typeof body.error === "string") code = body.error;
    } catch {
      // Response body was not JSON
    }
    return this.makeError(response.status, code, message);
  }

  private makeError(status: number, code: string, message: string): RedditApiError {
    return { status, code, message };
  }
}
