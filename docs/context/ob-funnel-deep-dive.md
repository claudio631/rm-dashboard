# Indeed Flex — OB (Onboarding) Funnel Deep Dive

> Sources:
> - `OB Funnel Custom Viewer (43).xlsx` — March 2026 (daily, 4 clients)
> - `OB Funnel Custom Viewer (44).xlsx` — Full Year 2025 (monthly, 147 clients)
> Both are Tableau exports used to build the daily Slack report.

## Funnel Stages (7 stages + 7 conversion rates)

### Absolute Counts

| # | Stage | Description |
|---|-------|-------------|
| 1 | **Worker Accounts Created** | Person downloaded app and created an account |
| 2 | **1st Role Verified** | Completed AI interview and got role verified |
| 3 | **1st OB Task Completed** | Completed first onboarding task (I-9, offer, etc.) |
| 4 | **Platform Verified** | Fully verified on the platform (all compliance done) |
| 5 | **"Ready to Book" Estimate** | Eligible to book shifts |
| 6 | **1st Shift Booked** | Booked their first actual shift |
| 7 | **1st Shift Completed** | Successfully completed their first shift |

### Stage-to-Stage Conversion Rates

| # | Conversion | What it measures |
|---|-----------|-----------------|
| 8 | Apply → 1st Role Verified CR% | How many accounts convert to verified role |
| 9 | 1st Role Verified → 1st OB Task CR% | Verified → started onboarding |
| 10 | 1st OB Task → Platform Verified CR% | Onboarding → fully verified |
| 11 | Platform Verified → Book CR% | Verified → actually booked a shift |
| 12 | Platform Verified → "Ready to Book" CR% | Verified → eligible to book |
| 13 | "Ready to Book" → 1st Booked CR% | Eligible → actually booked |
| 14 | 1st Book → 1st Work CR% | Booked → showed up and completed |

---

## Full Year 2025 — Overall Funnel (All 147 Clients)

```
Stage                                    Count      Stage CR%    Cumulative
──────────────────────────────────────────────────────────────────────────────
Worker Accounts Created                  52,987        —          100.0%
1st Role Verified (# Workers)           29,693       56.0%         56.0%   ← BIGGEST DROP
1st OB Task Completed (# Workers)       27,614       93.0%         52.1%
Platform Verified (# Workers)           19,091       69.1%         36.0%   ← 2nd DROP
"Ready to Book" Estimate (# Workers)    15,224       79.7%         28.7%
1st Shift Booked (# Workers)             9,628       63.2%         18.2%   ← 3rd DROP
1st Shift Completed (# Workers)          8,146       84.6%         15.4%
```

**Overall: 15.4% of accounts complete a first shift (8,146 / 52,987)**

### Where people are lost:

| Drop-off | People Lost | % Lost | Impact |
|----------|-------------|--------|--------|
| Account → Verified | 23,294 | 44.0% | **Biggest leak — AI interview completion** |
| OB Task → Platform Verified | 8,523 | 30.9% | Compliance/paperwork drop-off |
| Platform Verified → Booked | 9,463 | 49.6% | Verified but never book a shift |
| Ready → Booked | 5,596 | 36.8% | Eligible but don't commit |

---

## Full Year 2025 — Top 15 Clients

| Client | Created | Verified | Platf V | Booked | Completed | CR% |
|--------|--------:|---------:|--------:|-------:|----------:|----:|
| **OnTrac Final Mile** | 31,561 | 18,303 | 11,513 | 5,869 | 4,924 | 15.6% |
| **Stord, Inc** | 5,333 | 3,131 | 1,956 | 790 | 647 | 12.1% |
| **CORT** | 1,946 | 1,142 | 828 | 422 | 369 | 19.0% |
| **CTDI** | 1,466 | 668 | 437 | 237 | 206 | 14.1% |
| **Tennant Solutions** | 1,130 | 576 | 368 | 266 | 229 | 20.3% |
| **Assurant (Hyla)** | 1,023 | 769 | 593 | 443 | 397 | **38.8%** |
| **Indeed Inc** | 953 | 448 | 408 | 193 | 171 | 17.9% |
| **AFC Industries** | 813 | 411 | 271 | 136 | 116 | 14.3% |
| **Merritt Hospitality** | 804 | 269 | 192 | 75 | 60 | 7.5% |
| **LowCountry Catering** | 703 | 331 | 211 | 96 | 84 | 11.9% |
| **Foxconn** | 697 | 296 | 186 | 89 | 78 | 11.2% |
| **Legends Hospitality** | 604 | 295 | 167 | 65 | 53 | 8.8% |
| **Uplift Desk** | 418 | 224 | 146 | 37 | 29 | 6.9% |
| **Ingram Content Group** | 413 | 206 | 134 | 68 | 63 | 15.3% |
| **UT Housing & Dining** | 332 | 141 | 88 | 35 | 31 | 9.3% |

### Client Performance Insights:

- **OnTrac** dominates volume (59.6% of all accounts) with solid 15.6% conversion
- **Assurant** has the best conversion at **38.8%** — 4x better than average
- **Hospitality clients** (Merritt 7.5%, Legends 8.8%) convert lower than Industrial
- **Tennant Solutions** (20.3%) and **CORT** (19.0%) are high-performers relative to volume

---

## Full Year 2025 — Top 15 Markets

| Market | Created | Verified | Platf V | Booked | Completed | CR% |
|--------|--------:|---------:|--------:|-------:|----------:|----:|
| **Atlanta** | 7,766 | 4,090 | 2,699 | 1,342 | 1,169 | 15.1% |
| **Dallas** | 6,773 | 3,021 | 1,849 | 859 | 732 | 10.8% |
| **Chicago** | 6,763 | 3,303 | 2,479 | 1,289 | 1,102 | 16.3% |
| **Columbus** | 5,855 | 3,863 | 2,336 | 1,619 | 1,385 | **23.7%** |
| **Nashville** | 4,646 | 2,887 | 1,801 | 976 | 841 | 18.1% |
| **Cincinnati** | 4,179 | 2,279 | 1,424 | 900 | 763 | 18.3% |
| **Austin** | 2,611 | 1,536 | 997 | 348 | 282 | 10.8% |
| **Orlando** | 2,326 | 1,353 | 803 | 248 | 226 | 9.7% |
| **Phoenix** | 2,097 | 1,351 | 867 | 462 | 384 | 18.3% |
| **Las Vegas** | 1,929 | 1,219 | 838 | 298 | 245 | 12.7% |
| **Charlotte** | 1,203 | 730 | 466 | 176 | 137 | 11.4% |
| **Fort Mill** | 1,068 | 650 | 441 | 221 | 180 | 16.9% |
| **Reno** | 928 | 637 | 422 | 265 | 218 | **23.5%** |
| **Houston** | 755 | 409 | 239 | 32 | 24 | **3.2%** |
| **Middleburg Hts** | 685 | 385 | 251 | 111 | 70 | 10.2% |

### Market Performance Insights:

- **Columbus** (23.7%) and **Reno** (23.5%) are the most efficient markets
- **Houston** (3.2%) is severely underperforming — investigate why
- **Atlanta** has highest volume (7,766) but mediocre conversion (15.1%)
- **Chicago** converts well (16.3%) with high volume — strong market
- **Dallas** underperforms (10.8%) despite being 2nd in volume — optimization opportunity

---

## Data Scale (2025)

| Dimension | Count |
|-----------|-------|
| Total clients | **147** |
| Total markets | **21** (Atlanta, Austin, Charlotte, Chicago, Cincinnati, Columbus, Dallas, Erlanger, Fort Mill, Houston, Inland Empire, Las Vegas, Logan Township, McCarran, Middleburg Heights, Nashville, NW Arkansas, Orlando, Philadelphia, Phoenix, Reno) |
| Total accounts created | **52,987** |
| Total shifts completed | **8,146** |
| Monthly data columns | 12 (Jan–Dec 2025) |
| Total data rows | 3,473 |

---

## March 2026 Snapshot (from Viewer 43)

**4 key clients tracked daily:** CORT, Stord, OnTrac, CTDI
**21 markets** with daily granularity (date columns per day)

### CORT / Las Vegas (March 2026 example):

```
Worker Accounts Created        411     100%
1st Role Verified              238      57.9%
1st OB Task Completed          226      55.0%
Platform Verified              160      38.9%
"Ready to Book" Estimate        78      19.0%
1st Shift Booked                46      11.2%
1st Shift Completed             35       8.5%
```

---

## What This Means for PPC Manager AI

### The real funnel is 7 stages deep (not 3)

Traditional PPC: Click → Apply → Hire
Indeed Flex reality: Click → Download → Account → Verified → OB Task → Platform Verified → Ready → Booked → Completed

### The most valuable metrics:

1. **Cost per Account Created** — what does each channel cost to get someone to sign up?
2. **Cost per Verified** — what does it cost to get a fully verified Flexer?
3. **Cost per First Shift Completed** — the true cost-per-hire
4. **Account → Verified CR%** — biggest drop-off (44%), most impactable by re-engagement
5. **Daily velocity (+N)** — are we accelerating or stalling per client/market?

### Benchmarks (from 2025 data):

| Metric | Overall | Best Market | Worst Market |
|--------|---------|-------------|-------------|
| Account → Completed CR% | 15.4% | Columbus 23.7% | Houston 3.2% |
| Account → Verified CR% | 56.0% | — | — |
| Verified → Completed CR% | 27.4% | — | — |

### Re-engagement opportunities at each drop-off:

| Drop-off Point | People Lost (2025) | Braze Campaign | Channel |
|----------------|-------------------|---------------|---------|
| Account → Verified | 23,294 (44%) | "Complete your AI interview" | Push + SMS |
| OB Task → Platform Verified | 8,523 (31%) | "Finish onboarding — you're almost there" | Push + Email |
| Platform Verified → Ready | 3,867 (20%) | "Complete your last step" | Push |
| Ready → Booked | 5,596 (37%) | "Shifts available near you now" | Push + SMS |
| Booked → Completed | 1,482 (15%) | "Don't forget your shift tomorrow" | Push + SMS |

### Integration priority for PPC Manager AI:

| Data | Source | Priority | Value |
|------|--------|----------|-------|
| Funnel counts (daily) | Tableau API or underlying DB | P0 | Powers the daily Slack report |
| Funnel by client × location | Tableau | P0 | Cost-per-stage by channel |
| Ad spend by campaign | Indeed Analytics + Google + Meta | P0 | Join with funnel for true ROI |
| Attribution (which ad → which account) | AppsFlyer | P1 | Per-campaign funnel analysis |
| Full year historical | Tableau | P1 | Benchmarks and trends |
