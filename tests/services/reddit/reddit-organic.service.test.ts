/**
 * Unit tests: RedditOrganicService
 */

const mockInsert = jest.fn();
const mockSelect = jest.fn();
const mockOnConflictDoNothing = jest.fn().mockResolvedValue({ changes: 2 });
const mockValues = jest.fn().mockReturnValue({ onConflictDoNothing: mockOnConflictDoNothing });
mockInsert.mockReturnValue({ values: mockValues });

const mockSelectReturn = jest.fn();
mockSelect.mockReturnValue({ from: mockSelectReturn });

jest.mock("@/lib/db", () => ({
  db: {
    insert: (...args: unknown[]) => mockInsert(...args),
    select: () => mockSelect(),
  },
}));

jest.mock("@/lib/db/schema", () => ({
  redditTrackedTerms: "reddit_tracked_terms",
  redditMentions: "reddit_mentions",
}));

const mockGet = jest.fn();
jest.mock("@/services/reddit/reddit-api.client", () => ({
  RedditApiClient: jest.fn().mockImplementation(() => ({ get: mockGet })),
}));
jest.mock("@/services/reddit/reddit-auth.service", () => ({
  RedditAuthService: jest.fn(),
}));

const mockSearchResponse = {
  data: {
    children: [
      {
        data: {
          id: "abc123",
          title: "Anyone using Indeed Flex for logistics jobs?",
          url: "https://www.reddit.com/r/jobs/comments/abc123/",
          subreddit: "jobs",
          score: 42,
          num_comments: 7,
          created_utc: 1712345678,
          over_18: false,
        },
      },
      {
        data: {
          id: "def456",
          title: "Indeed Flex review — is it legit?",
          url: "https://www.reddit.com/r/WorkOnline/comments/def456/",
          subreddit: "WorkOnline",
          score: 15,
          num_comments: 3,
          created_utc: 1712234567,
          over_18: false,
        },
      },
    ],
  },
};

import { RedditOrganicService } from "@/services/reddit/reddit-organic.service";

describe("RedditOrganicService", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockInsert.mockReturnValue({ values: mockValues });
    mockValues.mockReturnValue({ onConflictDoNothing: mockOnConflictDoNothing });
    mockOnConflictDoNothing.mockResolvedValue({ changes: 2 });
    mockSelect.mockReturnValue({ from: mockSelectReturn });
  });

  describe("searchMentions()", () => {
    it("maps Reddit API response to DB schema correctly", async () => {
      mockGet.mockResolvedValue(mockSearchResponse);

      const service = new RedditOrganicService();
      await service.searchMentions("Indeed Flex");

      expect(mockGet).toHaveBeenCalledWith(
        "search",
        expect.objectContaining({ q: "Indeed Flex", sort: "new", type: "link" }),
        "oauth"
      );

      const insertedRows = mockValues.mock.calls[0][0];
      expect(insertedRows).toHaveLength(2);
      expect(insertedRows[0]).toMatchObject({
        term: "Indeed Flex",
        postId: "abc123",
        title: "Anyone using Indeed Flex for logistics jobs?",
        subreddit: "jobs",
        score: 42,
        numComments: 7,
      });
    });

    it("returns 0 when no results found", async () => {
      mockGet.mockResolvedValue({ data: { children: [] } });

      const service = new RedditOrganicService();
      const count = await service.searchMentions("no results here");

      expect(count).toBe(0);
      expect(mockInsert).not.toHaveBeenCalled();
    });
  });

  describe("syncAllTerms()", () => {
    it("returns correct summary shape", async () => {
      mockSelectReturn.mockResolvedValue([
        { id: 1, term: "Indeed Flex", createdAt: "2026-04-07T00:00:00Z" },
        { id: 2, term: "indeed flex jobs", createdAt: "2026-04-07T00:00:00Z" },
      ]);
      mockGet.mockResolvedValue({ data: { children: [] } });

      const service = new RedditOrganicService();
      const summary = await service.syncAllTerms();

      expect(summary).toHaveProperty("terms_synced", 2);
      expect(summary).toHaveProperty("new_mentions");
      expect(summary).toHaveProperty("synced_at");
      expect(typeof summary.synced_at).toBe("string");
    });
  });
});
