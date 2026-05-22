# Task: Ad Test Management

**Agent:** @ad-test-specialist (Scout)
**Trigger:** `*new-test`, `*log-metrics`, `*review-test`, `*declare-winner`

---

## *new-test — Create Test Tracker

**Elicit (required):**

1. **Channel** — Google | Indeed | Reddit | Meta | TikTok
2. **Test name** — short slug (e.g., `google-nashville-headline-july`)
3. **Test type** — ad copy · creative · audience · bid strategy · landing page · format
4. **Variable** — the one thing being changed between control and variant
5. **Hypothesis** — "If X, then Y will change by Z%, because W"
6. **Control (A)** — description + creative link + copy doc link
7. **Variant (B)** — description + creative link + copy doc link
8. **Budget + split** — total budget and % per variant (default: 50/50)
9. **Duration** — start date → end date (minimum runtime per channel enforced)
10. **Owner** — who is running this test

**Output:**

- Generate `TEST_ID` = `{channel}-{slug}-{YYYYMMDD}` (e.g., `google-nashville-headline-20260522`)
- Fill `ad-test-tracker-tmpl.md` with all elicited values
- Save to `data/tests/{TEST_ID}.md`
- Print summary: ID, hypothesis, variants, KPIs, minimum threshold, next step

**Channel enforcement:**
- Apply channel_metrics minimums from agent YAML (min runtime, min conversions per variant)
- Warn if budget too low to reach minimum thresholds

---

## *log-metrics — Record Metric Snapshot

**Inputs:** TEST_ID

**Steps:**
1. Open `data/tests/{TEST_ID}.md`
2. Ask for today's metrics for each variant (use channel-native KPIs from channel_metrics)
3. Append row to Section 5 Snapshot Log
4. Check if minimum thresholds are met
5. If thresholds met: "✅ Minimum data reached — run *review-test {TEST_ID} to analyze"
6. If not met: show progress (e.g., "Variant B: 18/30 conversions — keep running")

---

## *review-test — Analyze Results

**Inputs:** TEST_ID

**Steps:**
1. Open `data/tests/{TEST_ID}.md` — read all metric snapshots
2. Calculate per-variant totals for all KPIs
3. Calculate lift: `(Variant B − Control A) / Control A × 100`
4. Assess data sufficiency against channel minimums
5. Flag significance level (rough heuristic: >20% lift with >30 conversions = strong signal)
6. Fill Section 6 Results Summary
7. Output: variant comparison table, lift per KPI, data sufficiency verdict
8. Recommend: "Declare winner", "Continue running (N more {unit} needed)", or "Inconclusive"

---

## *declare-winner — Close Test

**Inputs:** TEST_ID, WINNER (A | B | inconclusive)

**Steps:**
1. Fill Section 7 Winner Declaration
2. Write Section 8 Key Insight (one sentence, actionable)
3. Recommend next test based on this result
4. Update Status to ✅ Complete
5. Notify: "Share this with @ppc-paid-media-specialist (Parker) to scale the winner"
6. Save `data/tests/{TEST_ID}.md`

---

## *best-practices {channel}

**Output:** Channel-specific testing rules from `channel_metrics` in the agent YAML:
- Minimum sample sizes
- Minimum runtime
- Recommended test types for that channel
- Common pitfalls
- KPI definitions

---

## *test-status

**Output:** Table of all files in `data/tests/` — ID, channel, status, days running, threshold progress

---

## *insights-report

**Output:**
1. All completed tests grouped by channel
2. Win rate per channel (% of tests where variant beat control)
3. Average lift by KPI across winning tests
4. Top 3 insights with the highest impact
5. Recommended next tests based on pattern
