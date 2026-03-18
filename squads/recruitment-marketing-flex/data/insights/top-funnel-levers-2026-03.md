# Top-Funnel Traffic Levers — Data-Driven Insights

> **Analyst:** Nova (@data-scientist) · **Date:** 2026-03-18
> **Objective:** Identify levers to improve ad performance and drive more top-funnel traffic
> **Data Sources:** OB Funnel 2025 (52,987 accounts), March 2026 tracking, industry benchmarks, channel config, unfilled shifts report, hiring event data, landing pages, incentive programs
> **MTD Spend (as of 3/17):** $51,155

---

## Executive Summary

The data reveals **5 high-impact levers** that don't require increasing budget — they improve yield from existing spend. The biggest opportunity is not "more traffic" but "better conversion of existing traffic" through the 7-stage funnel. Every percentage point improvement at the Account → Verified stage (currently 56%) saves approximately **$4.80 per eventual hire** at current CPA rates.

**Top 3 quick-win levers:**
1. Fix the 12 high-volume roles without dedicated landing pages (+21,000 annual shifts on generic LP)
2. Deploy Google Ads alongside Indeed for underperforming markets (Dallas, Austin, Orlando, Houston)
3. Activate retargeting for the 44% who create accounts but never complete AI interview

---

## Insight 1: The Funnel is the Lever, Not Just the Top

### The Data

```
52,987 accounts → 8,146 first shifts = 15.4% end-to-end conversion (2025)

Where people are lost:
  Account → Verified:           -44.0% (23,294 lost)  ← BIGGEST LEAK
  OB Task → Platform Verified:  -30.9% (8,523 lost)
  Platform Verified → Booked:   -49.6% (9,463 lost)   ← HIDDEN WASTE
```

### So What?

**Driving more top-funnel traffic without fixing the 44% drop at Account → Verified is like pouring water into a bucket with a hole.** Every 100 new accounts created costs ~$1,500 in ad spend (at blended $15 CPA), but only 15 will ever complete a shift.

### The Math

| Scenario | Accounts | CR% | Completions | Cost/Completion |
|----------|:--------:|:---:|:-----------:|:---------------:|
| Current state | 100 | 15.4% | 15 | $100 |
| +10% more traffic (same CR) | 110 | 15.4% | 17 | $100 |
| Same traffic, +5pp at verification | 100 | 19.3% | 19 | $79 |
| Both levers combined | 110 | 19.3% | 21 | $79 |

**Improving verification rate by 5pp is equivalent to 27% more traffic at zero additional cost.**

### Action
- Deploy Braze push + SMS campaign: "Complete your AI interview" targeting the 44% who create accounts but stall
- A/B test simplified AI interview flow for top 3 roles
- Track Account → Verified CR% as a **primary KPI** alongside CPA in ad reporting

---

## Insight 2: 12 High-Volume Roles Without Landing Pages = Conversion Leak

### The Data

From [landing-pages.md](../../docs/context/landing-pages.md):

| Role (no dedicated LP) | 2025 Shifts | Falling to Generic LP |
|------------------------|:-----------:|:---------------------:|
| FM General Labor | 6,408 | Yes |
| Parking Services Rep | 4,145 | Yes |
| Event Student Worker Guard | 3,270 | Yes |
| PTS Pick up Student Worker | 2,292 | Yes |
| Customer Service Rep | 1,589 | Yes |
| Event Student Worker Cashier | 1,115 | Yes |
| Sure Walk Student Worker | 864 | Yes |
| Brand Ambassador | 628 | Yes |
| Assistant Supervisor | 552 | Yes |
| CDL Driver | 194 | Yes |
| Delivery Driver 1 | 166 | Yes |
| Data Entry Specialist | 132 | Yes |
| **Total** | **21,355** | — |

### So What?

**21,355 shifts** (6.9% of total volume) are advertised but land on a generic page that doesn't match the ad's promise. Industry benchmarks show role-specific landing pages convert 30-50% better than generic pages. If these roles are being advertised on Indeed or Google Ads, every click to the generic LP is underperforming.

### Estimated Impact

| Metric | Generic LP (est.) | Role-Specific LP (est.) | Delta |
|--------|:-----------------:|:----------------------:|:-----:|
| Apply Rate | 5% | 7-8% | +40-60% |
| Cost per Apply | $10 | $6-7 | -30-40% |

At even **$0.50 CPC × 21,000 clicks**, that's $10,500 in spend hitting a generic page. A 40% improvement in apply rate would generate ~4,200 additional apply starts at zero additional spend.

### Action
- **Priority:** Create dedicated LPs for FM General Labor (6,408 shifts) and Parking Services Rep (4,145 shifts) — these two alone represent 50% of the gap
- Audit current Google Ads and Indeed campaigns to confirm which roles are sending traffic to the generic LP
- Add LP-role match validation to the campaign setup checklist

---

## Insight 3: Market-Level Performance Variance = Budget Reallocation Opportunity

### The Data

| Tier | Markets | CR% | 2025 Accounts | Action |
|------|---------|:---:|:-------------:|--------|
| Elite | Columbus, Reno | 23.5-23.7% | 6,783 | Maintain, scale cautiously |
| Strong | Cincinnati, Phoenix, Nashville, Fort Mill, Chicago | 16.3-18.3% | 22,753 | Invest — high ROI |
| On Target | Atlanta | 15.1% | 7,766 | +1pp = 78 more completions |
| Below Average | Las Vegas, Charlotte, Dallas, Austin, Middleburg, Orlando | 9.7-12.7% | 15,527 | Diagnose before spending more |
| Critical | Houston | 3.2% | 755 | Stop scaling until diagnosed |

### So What?

**The spread is 7.4x between best and worst markets (23.7% Columbus vs. 3.2% Houston).** This means a dollar spent in Columbus produces ~7x the outcome of a dollar in Houston.

**Dallas is the biggest opportunity:** 2nd largest market by volume (6,773 accounts) but converts at only 10.8% — 4.6pp below average. If Dallas matched Chicago's 16.3%, that would be **+372 additional shift completions** per year at current volume.

### Budget Reallocation Model

| Market | Current Est. Spend Share | Proposed | Rationale |
|--------|:------------------------:|:--------:|-----------|
| Columbus | ~8% | 10% | High CR, scale |
| Chicago | ~12% | 14% | High volume + strong CR |
| Dallas | ~13% | 10% | Reduce until CR improves; fix funnel first |
| Houston | ~3% | 1% | Freeze scaling; diagnose 3.2% CR |
| Nashville/Cincinnati | ~10% each | 12% each | Strong CR, room to grow |
| Atlanta | ~14% | 14% | Maintain — high volume, every pp matters |

### Action
- Run market-level CPA analysis joining ad spend with OB funnel data
- Flag Houston for investigation: is it a demand issue (no shifts to fill) or a funnel issue (people dropping off)?
- Test Google Ads in Dallas/Austin (currently Indeed-heavy) — different channel may reach different candidate profiles

---

## Insight 4: Google Ads is Under-Leveraged Relative to Budget Share

### The Data

| Channel | Budget Share | CPC (Median) | CPA (Median) | Key Advantage |
|---------|:-----------:|:------------:|:------------:|---------------|
| Indeed | 30-40% | $0.50 | $15 | Direct job intent, high volume |
| Google | 20-30% | $2.50 | $35 | Broad reach, AI optimization, multi-format |
| Meta | 15-20% | $1.50 | $20 | Visual creative, lookalikes, younger demos |
| Bing | 5-10% | $1.80 | $30 | 20-30% lower CPC than Google |

### So What?

Indeed dominates spend but has **limited creative control and no audience targeting beyond job category/location**. Google Ads offers:
- **AI Max for Search:** +14% more conversions at similar CPA
- **Performance Max:** +18% incremental conversions across all Google channels
- **Remarketing:** Re-engage the 44% who created accounts but stalled
- **YouTube/Display:** Employer brand for passive candidates

The current Google budget share (20-30%) leaves significant headroom, especially for:
1. **Remarketing campaigns** (Display) targeting account-created-but-not-verified candidates
2. **Performance Max** for cross-channel reach in underperforming markets
3. **YouTube** employer brand videos for markets with low awareness

### Estimated Impact of Google Ads Expansion

| Campaign Type | Est. Monthly Budget | Expected CPA | Est. Conversions |
|--------------|:-------------------:|:------------:|:----------------:|
| Search (new markets) | $3,000 | $30-40 | 75-100 |
| Performance Max | $2,000 | $25-35 | 57-80 |
| Display Remarketing | $1,000 | $15-25 | 40-67 |
| YouTube Awareness | $1,000 | N/A (CPV) | Brand lift |
| **Total** | **$7,000** | — | **172-247** |

### Action
- Launch Google Search campaigns for top 5 underperforming markets (Dallas, Austin, Orlando, Las Vegas, Houston)
- Set up Display remarketing targeting Indeed Flex account-holders who haven't completed verification
- Pilot Performance Max with strong audience signals from top-worker CRM data
- Reference: `google-ads/campaign-types-reference.md`, `google-ads/performance-max-playbook.md`

---

## Insight 5: Unfilled Shifts Data Reveals WHERE to Focus Ad Spend

### The Data

Weekly unfilled shifts (17-25 Mar 2026):
- **825 unfilled** out of 2,357 real shifts (65% fill rate)
- **Warehouse Operative: 432 unfilled** (52% of all gaps)
- **Picker Packer: 200 unfilled** (24%)
- **Forklift Driver: 68 unfilled** (8%)

Top unfilled venues:
| Venue | Market | Unfilled | Role |
|-------|--------|:--------:|------|
| PowerStop Bedford Park | Chicago | 249 | Picker Packer, WO |
| Logan Township | NJ | 119 | Warehouse Operative |
| Nashville HTN001 | Nashville | 100 | Warehouse Operative |
| TX Branch 157 | Dallas | 66 | Warehouse Operative |
| CVG1 | Cincinnati | 65 | Picker Packer |
| ATL1 | Atlanta | 56 | Forklift Driver |

### So What?

**Ad spend should follow demand, not be spread evenly.** The data tells us exactly where to point our Google Ads and Indeed campaigns:

1. **Chicago/Bedford Park** needs Picker Packer + Warehouse Operative candidates NOW (249 unfilled)
2. **Nashville** needs PM shift Warehouse Operatives (100 unfilled, all 14:00-22:00+)
3. **Dallas** needs Warehouse Operatives across all shifts (66 unfilled, already low-CR market)
4. **Atlanta** needs certified Forklift Drivers specifically (56 unfilled, night shift)

### The Paradox
Nashville (18.1% CR) and Cincinnati (18.3% CR) have **healthy funnels** but unfilled shifts. This means the gap is at **Ready → Booked**, not at top-of-funnel. More ads won't help — Braze re-engagement of verified-but-not-booked workers is the lever.

For Dallas (10.8% CR) and Chicago-area Bedford Park, the funnel IS the issue — more top-funnel traffic with better conversion is needed.

### Action
- **Reallocate ad budget** toward roles/markets with active unfilled shifts
- **For high-CR markets with unfilled shifts** (Nashville, Cincinnati): Focus on Braze re-engagement, not more ads
- **For low-CR markets with unfilled shifts** (Dallas): Increase ad spend + fix funnel
- **For ATL Forklift Drivers**: This is a niche pool problem — consider Google Ads targeting "forklift certification" keywords specifically

---

## Insight 6: Hiring Events are a High-Intent Channel (48% Show, 96% Pass)

### The Data

Las Vegas Hiring Events (March 11 + 16):
- **187 invited → 89 arrived (48% show rate)**
- **85 passed drug test (96% of arrivals)**
- **Walk-ins: 100% arrival rate (14 people)**
- **Cost context:** CORT LV: $3,532 Indeed spend for 23 RSVPs vs 91 cleared at events

### So What?

Hiring events deliver **pre-qualified, high-intent candidates** at potentially lower cost-per-cleared-worker than digital alone. But the **52% no-show rate** is a lever.

If we could improve show rate from 48% to 65%:
- Same 187 invites → 122 arrivals (vs 89)
- At 96% pass rate → 117 cleared (vs 91)
- **+26 additional cleared workers** from the same pool

### Improving Show Rate (Ad + CRM Levers)
1. **Multi-touch reminder sequence** via Braze: 3-day, 1-day, morning-of push/SMS
2. **Time slot optimization**: 9 AM (59% show) and 2 PM (67% show) outperform 10 AM (17%) and 3 PM (20%) — consolidate to high-show slots
3. **Google Ads for events**: Geo-targeted "hiring event near me" Search + YouTube pre-roll in the week before
4. **Walk-in acquisition**: 100% show rate = highest intent. Advertise events publicly (Google Local, Meta Events) to drive walk-ins

### Action
- Design a Braze re-engagement sequence for event invites (3-touch: D-3, D-1, D-0)
- Test Google Ads "hiring event" campaigns geo-fenced to 25-mile radius, 7 days before event
- Consolidate event time slots to 9 AM and 2 PM (highest show rates)
- Create a walk-in acquisition ad campaign for upcoming events

---

## Insight 7: Seasonality is Working in Our Favor (Q1 Modifier: 0.9x)

### The Data

From industry benchmarks:
| Quarter | Modifier | What It Means |
|---------|:--------:|---------------|
| Q1 (Now) | **0.9x** | Lower competition, lower CPCs |
| Q2 | 1.0x | Baseline |
| Q3 | 1.1x | Costs increase 10% |
| Q4 | **1.3x** | Peak — costs 30% higher |

### So What?

**Right now is the cheapest time of year to acquire candidates.** The same budget buys ~10% more traffic in Q1 than Q2, and ~30% more than Q4. This is the time to:
- **Test new channels** (Google Ads, Reddit) while CPCs are low
- **Build remarketing pools** for Q3/Q4 when costs spike
- **Scale top-funnel volume** to fill the pipeline for spring/summer demand

### Action
- Accelerate Google Ads testing in Q1 while CPCs are favorable
- Build remarketing audiences NOW that can be activated cheaper in Q2-Q4
- Front-load hiring event marketing to Q1-Q2 before Q4 cost premium

---

## Insight 8: Ad Creative Intelligence — Recruitment Copy Formulas

### The Data

From the daily tracking spreadsheet campaign naming patterns and Google Ads knowledge base:

**Current Indeed ads** follow a standardized format with limited creative testing:
```
US-B2C-Industrial-{Client}-{Role}-{City},{State}-{Month}
```

**Google Ads best practices** (from knowledge base) show:
- Responsive Search Ads with 15 headlines test thousands of combinations
- Ad Strength "Excellent" = lower CPC, better positions
- Including pay rate in headlines increases CTR by 10-15% (industry benchmark)
- Urgency CTAs ("Hiring Now", "Start This Week") outperform generic CTAs

### So What?

Indeed's limited creative format means **Google Ads is the creative testing ground.** On Google, we can:
1. Test pay-in-headline vs. benefit-in-headline
2. Test urgency ("Start tomorrow") vs. security ("Steady weekly pay")
3. Test role-specific copy vs. general flexible-work copy
4. Use AI Max to auto-generate and optimize headline combinations

### Action
- Launch Google Search campaigns with the ad copy formulas from `google-ads/ad-copywriting-playbook.md`
- A/B test: "$18/hr Warehouse Jobs — Dallas" vs "Flexible Warehouse Work — Choose Your Schedule"
- Use insights from Google creative testing to inform Indeed job title optimization

---

## Summary: Lever Priority Matrix

| # | Lever | Type | Effort | Impact | Timeframe |
|---|-------|------|:------:|:------:|:---------:|
| 1 | Braze re-engagement at Account → Verified (44% drop) | CRM | Low | **Very High** | 1-2 weeks |
| 2 | Create dedicated LPs for 12 high-volume roles | Web | Medium | **High** | 2-4 weeks |
| 3 | Launch Google Ads in underperforming markets | Paid | Medium | **High** | 1-2 weeks |
| 4 | Reallocate budget from low-CR to high-CR markets | Paid | Low | **Medium-High** | Immediate |
| 5 | Activate Display remarketing (account holders not verified) | Paid | Low | **Medium-High** | 1 week |
| 6 | Focus ads on roles with active unfilled shifts | Paid | Low | **Medium** | Immediate |
| 7 | Hiring event show-rate optimization | CRM + Paid | Medium | **Medium** | 2 weeks |
| 8 | Google Ads creative testing (pay/urgency/benefits) | Paid | Low | **Medium** | 1-2 weeks |
| 9 | Capitalize on Q1 lower CPCs for testing | Paid | Low | **Medium** | Now (time-sensitive) |

### Expected Aggregate Impact

If levers 1-5 are executed:
- **+5pp at Account → Verified** (56% → 61%) = +2,649 more verified workers/year
- **+40% apply rate** on 12 roles with new LPs = ~4,200 more apply starts/year
- **Google Ads incremental reach** = 172-247 additional conversions/month
- **Budget reallocation** = 10-15% lower blended CPA without spending more

**Confidence level:** Medium-High. The funnel data is robust (52,987 accounts). Market-level patterns are consistent across 12 months. The levers are directionally sound even if individual estimates have ±30% uncertainty.

---

*— Nova, encontrando padrões nos dados 🧬*

*Assumptions stated. Confidence levels noted. Correlation ≠ causation — the market-level CR differences could be driven by client mix, not pure geography. Recommend controlled tests before permanent budget shifts.*
