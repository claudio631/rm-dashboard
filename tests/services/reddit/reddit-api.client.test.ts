import { RedditApiClient } from "@/services/reddit/reddit-api.client";
import { RedditAuthService } from "@/services/reddit/reddit-auth.service";

// Mock fetch globally
global.fetch = jest.fn();

describe("RedditApiClient", () => {
  let mockAuthService: jest.Mocked<Pick<RedditAuthService, "getValidToken" | "refreshToken" | "getStoredTokens" | "clearTokens">>;
  let client: RedditApiClient;

  beforeEach(() => {
    jest.clearAllMocks();
    mockAuthService = {
      getValidToken: jest.fn().mockResolvedValue("test-access-token"),
      refreshToken: jest.fn().mockResolvedValue(undefined),
      getStoredTokens: jest.fn().mockResolvedValue(null),
      clearTokens: jest.fn().mockResolvedValue(undefined),
    };
    client = new RedditApiClient(
      mockAuthService as unknown as RedditAuthService
    );
  });

  describe("Authorization header injection", () => {
    it("injects bearer token on GET requests", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue({ data: "ok" }),
        status: 200,
      });

      await client.get("/campaigns");

      expect(global.fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: "bearer test-access-token",
          }),
        })
      );
    });

    it("injects bearer token on POST requests", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValue({ id: "123" }),
        status: 201,
      });

      await client.post("/campaigns", { name: "Test" });

      expect(global.fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: "bearer test-access-token",
          }),
        })
      );
    });
  });

  describe("Token refresh on 401", () => {
    it("attempts token refresh on 401 and retries", async () => {
      (global.fetch as jest.Mock)
        .mockResolvedValueOnce({
          ok: false,
          status: 401,
          json: jest.fn().mockResolvedValue({ error: "unauthorized" }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: jest.fn().mockResolvedValue({ data: "retried" }),
          status: 200,
        });

      const result = await client.get<{ data: string }>("/campaigns");

      expect(mockAuthService.refreshToken).toHaveBeenCalledTimes(1);
      expect(result).toEqual({ data: "retried" });
    });

    it("does not retry more than once on 401", async () => {
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        status: 401,
        json: jest.fn().mockResolvedValue({ error: "unauthorized" }),
      });

      await expect(client.get("/campaigns")).rejects.toMatchObject({
        status: 401,
      });

      // fetch called twice (original + one retry), refreshToken called once
      expect(global.fetch).toHaveBeenCalledTimes(2);
      expect(mockAuthService.refreshToken).toHaveBeenCalledTimes(1);
    });
  });

  describe("Error normalization", () => {
    it("normalizes non-ok responses into RedditApiError shape", async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 429,
        json: jest.fn().mockResolvedValue({
          error: "RATE_LIMIT_EXCEEDED",
          message: "Too many requests",
        }),
      });

      await expect(client.get("/campaigns")).rejects.toMatchObject({
        status: 429,
        code: "RATE_LIMIT_EXCEEDED",
        message: "Too many requests",
      });
    });
  });
});
