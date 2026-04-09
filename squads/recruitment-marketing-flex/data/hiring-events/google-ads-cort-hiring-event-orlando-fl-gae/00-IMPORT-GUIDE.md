# GAE Import Guide — CORT Hiring Event Orlando FL

> **Campaign:** Search only (P.Max, Display, and App require manual setup — see below)
> **Flight:** Apr 14–21, 2026 | **Budget:** $50/day Search | **Total Search:** ~$400

## Final URL (all ads + keywords)

```
https://indeedflex.com/find-jobs/lp/hiring-event/?utm_source=google&utm_medium=cpc&link_value=syft://jobs/browse/501764&employer=cort&metro=orlando&role=loader--crew&utm_campaign=us-cort-hiring-event-orlando-fl
```

---

## Import Order — Google Ads Editor

Open Google Ads Editor → Account → Import → From CSV

| Step | File | What it creates |
|------|------|----------------|
| 1 | `01-campaign.csv` | Search campaign, budget $50, Maximize Clicks, Apr 14–21 |
| 2 | `02-ad-groups.csv` | 3 ad groups with default bids |
| 3 | `03-keywords.csv` | 27 phrase match keywords across 3 ad groups |
| 4 | `04-negative-keywords.csv` | 19 campaign-level negative keywords |
| 5 | `05-responsive-search-ads.csv` | 3 RSAs (15 headlines + 4 descriptions each) |
| 6 | `06-sitelinks.csv` | 4 sitelinks with descriptions |
| 7 | `07-callouts.csv` | 6 callout extensions |
| 8 | `08-structured-snippets.csv` | 3 structured snippet sets |
| 9 | `09-ad-schedule.csv` | 7-day schedule with bid adjustments |
| 10 | `10-locations.csv` | 8 location targets with radius + bid adjustments |
| 11 | `11-device-adjustments.csv` | Mobile +20%, tablet -15% |
| 12 | `12-audiences.csv` | 4 observation audiences |

---

## After CSV Import — Manual Setup in Google Ads UI

These items cannot be CSV-imported and must be configured manually.

### Bidding Strategy Switch (Day 3)
- **Apr 16 (Wed):** Change Search bid strategy from Maximize Clicks to Maximize Conversions, target CPA $8.00

### Location Exclusions
- Tampa, FL
- Gainesville, FL
- Any location outside 30-mile radius of 32812

### Demographics (observation mode)
- Age 18-24: +10%
- Age 25-34: +15%
- Age 35-44: +10%
- Age 45-54: 0%
- Age 55-64: -10%
- Age 65+: -25%

### Custom Audience Segment (create in Audience Manager)
- Name: `CORT Hiring Event - Orlando FL`
- Search terms: "hiring event orlando", "loader jobs near me", "job fair orlando", "same day pay"

### Conversion Actions (confirm at account level)
- Account Created (Indeed Flex Signup) — Primary — $5.00 — Count: One — Data-driven attribution
- Landing Page View — Observation — $1.00 — Last click
- App Download Click — Secondary — $3.00 — Data-driven

---

## P.Max, Display, and App Campaigns (manual setup required)

These 3 campaigns must be built manually — duplicate from BAU and update accordingly.

| Campaign | Duplicate From | New Name | Budget |
|----------|---------------|----------|--------|
| P.Max | `p-b2c-google-pmax-us-bofu-bau-orlando-industrial--eg--` | `p-b2c-google-pmax-us-bofu-bau-orlando-industrial-hiring-event-04202026` | $50/day |
| Display | `p-b2c-google-display-us-bofu-bau-orlando-industrial--eg--` *(or create new)* | `p-b2c-google-display-us-bofu-bau-orlando-industrial-hiring-event-04202026` | $30/day |
| App | `p-b2c-google-app-us-bofu-bau-orlando-industrial--eg--` | `p-b2c-google-app-us-bofu-bau-orlando-industrial-hiring-event-04202026` | $50/day |

For full copy and settings for these campaigns, see: `google-ads-cort-hiring-event-orlando-fl-editor.md`

---

## {DOLLAR} Note

GAE may flag `$` in ad copy. The RSA CSV uses `{DOLLAR}` as placeholder.
After import, find and replace `{DOLLAR}` with `$` in all headlines and descriptions.
If GAE accepts `$` directly, no replacement needed — test with one ad first.

---

## Monday Ad Schedule Note

The ad schedule sets Monday to +30% (to cover event day 2, Apr 21).
This also applies to the launch day (Apr 14 Mon) — acceptable for a short urgent campaign.
**Manually pause all 4 campaigns at 2pm on Apr 21** — GAE schedule cannot target a specific calendar date.

---

## Pre-Post Checklist

**Before posting changes:**
- [ ] All 3 RSAs show Eligible status
- [ ] No headline or description exceeds character limits
- [ ] Final URL resolves (job browse ID 501764 active)
- [ ] Negative keywords don't conflict with active keywords
- [ ] Location targeting shows correct radius on map preview
- [ ] Ad schedule stops at 14:00 on Sunday (event day 1)
- [ ] Budget = $50/day, end date = 2026-04-21
- [ ] {DOLLAR} replaced with $ in all ad copy

**After posting:**
- [ ] Google Tag fires on LP signup completion (verify Tag Assistant)
- [ ] UTMs resolve in GA4 real-time view
- [ ] Ads enter review and approved within 1-2 hours
- [ ] Set calendar alert for Apr 16: switch Search to Maximize Conversions
- [ ] Set calendar alert for Apr 21 at 2pm: pause all 4 campaigns + restore BAU budgets
