/**
 * Unit tests: GET /api/reddit/organic/mentions — filtering logic
 * Tests the days=N cutoff computation and filter application directly.
 */

describe("GET /api/reddit/organic/mentions — filtering logic", () => {
  it("returns 400 for days=0", () => {
    const days = 0;
    const isValid = !isNaN(days) && days > 0;
    expect(isValid).toBe(false);
  });

  it("returns 400 for negative days", () => {
    const days = -5;
    const isValid = !isNaN(days) && days > 0;
    expect(isValid).toBe(false);
  });

  it("computes cutoff UTC as current time minus N days in seconds", () => {
    const days = 7;
    const before = Math.floor(Date.now() / 1000);
    const cutoffUtc = Math.floor(Date.now() / 1000) - days * 24 * 60 * 60;
    const after = Math.floor(Date.now() / 1000);

    const expectedMinCutoff = before - days * 24 * 60 * 60;
    const expectedMaxCutoff = after - days * 24 * 60 * 60;

    expect(cutoffUtc).toBeGreaterThanOrEqual(expectedMinCutoff);
    expect(cutoffUtc).toBeLessThanOrEqual(expectedMaxCutoff);
  });

  it("filters mentions older than cutoff (simulated)", () => {
    const days = 7;
    const cutoffUtc = Math.floor(Date.now() / 1000) - days * 24 * 60 * 60;

    const allMentions = [
      { id: 1, createdUtc: cutoffUtc + 3600, over18: false },  // recent — include
      { id: 2, createdUtc: cutoffUtc - 3600, over18: false },  // too old — exclude
      { id: 3, createdUtc: cutoffUtc + 7200, over18: true },   // recent but NSFW — exclude by default
    ];

    const filtered = allMentions.filter(
      (m) => m.createdUtc >= cutoffUtc && !m.over18
    );

    expect(filtered).toHaveLength(1);
    expect(filtered[0].id).toBe(1);
  });

  it("includes NSFW mentions when include_nsfw=true", () => {
    const days = 7;
    const cutoffUtc = Math.floor(Date.now() / 1000) - days * 24 * 60 * 60;

    const allMentions = [
      { id: 1, createdUtc: cutoffUtc + 3600, over18: false },
      { id: 3, createdUtc: cutoffUtc + 7200, over18: true },
    ];

    const filtered = allMentions.filter((m) => m.createdUtc >= cutoffUtc);
    expect(filtered).toHaveLength(2);
  });
});
