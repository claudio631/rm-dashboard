# GAE Import Guide — CTDI Hiring Event Haslet TX

## Import Order in Google Ads Editor

Open Google Ads Editor → Account → Import → From CSV

Import in this sequence (order matters):

| Step | File | What it creates |
|------|------|----------------|
| 1 | `01-campaign.csv` | Campaign with settings, budget, bidding |
| 2 | `02-ad-groups.csv` | 3 ad groups with default bids |
| 3 | `03-keywords.csv` | 38 keywords across 3 ad groups (exact/phrase/broad) |
| 4 | `04-negative-keywords.csv` | 23 campaign-level negative keywords |
| 5 | `05-responsive-search-ads.csv` | 3 RSAs (one per ad group, 15 headlines + 4 descs each) |
| 6 | `06-sitelinks.csv` | 4 sitelinks with descriptions |
| 7 | `07-callouts.csv` | 6 callout extensions |
| 8 | `08-structured-snippets.csv` | 3 structured snippet sets |
| 9 | `09-ad-schedule.csv` | 4-day ad schedule with bid adjustments |
| 10 | `10-locations.csv` | 10 location targets with radius + bid adjustments |
| 11 | `11-device-adjustments.csv` | Mobile +20%, tablet -15% |
| 12 | `12-audiences.csv` | 4 observation audiences |

## After Import — Manual Setup in Google Ads UI

These items require manual configuration (can't be CSV-imported):

### Conversion Tracking
- Account Created (Indeed Flex Signup) → Primary → Value: $5.00 → Count: One → Data-driven attribution
- Landing Page View → Observation → Value: $1.00 → Last click
- App Download Click → Secondary → Value: $3.00 → Data-driven

### Location Exclusions (set manually)
- Arlington, TX
- Grand Prairie, TX
- South Dallas area

### Bidding Strategy Switch (Day 3)
- **Apr 1:** Change bid strategy from "Maximize Clicks" → "Maximize Conversions" with target CPA $8.00

### Demographics (observation mode in UI)
- Age 18-24: +10%
- Age 25-34: +15%
- Age 35-44: +10%
- Age 45-54: 0%
- Age 55-64: -10%
- Age 65+: -25%

### Custom Audience Segment (create in Audience Manager)
- Name: "CTDI Hiring Event - Haslet TX"
- Search terms: "hiring event", "job fair", "warehouse jobs", "jobs hiring near me"

## RSA Dollar Sign Note

Google Ads Editor may flag `$` in ad copy. The CSVs use `{DOLLAR}` as placeholder.
**After import**, find & replace `{DOLLAR}` with `$` in all headlines and descriptions.

If GAE accepts `$` directly during import, the replace is not needed — test with one ad first.

## Final URL (all ads + keywords)

```
https://indeedflex.com/find-jobs/lp/hiring-event/?utm_source=google&utm_medium=cpc&link_value=syft://jobs/browse/499299&employer=ctdi&metro=dallas&role=warehouse-operative&utm_campaign=us-ctdi-hiring-event-haslet-tx
```

## Pre-Post Checklist

**Before posting changes:**
- [ ] All 3 RSAs show "Eligible" status
- [ ] No headline/description exceeds char limits
- [ ] All Final URLs resolve (200 OK)
- [ ] Negative keywords don't conflict with active keywords
- [ ] Location targeting shows correct radius on map preview
- [ ] Ad schedule stops at 3:00 PM on Thursday (Apr 2)
- [ ] Budget = $50/day
- [ ] Campaign end date = 2026-04-02

**After posting:**
- [ ] Google Tag fires on LP signup completion (verify Tag Assistant)
- [ ] UTMs resolve in GA4 real-time view
- [ ] Ads enter review → Approved within 1-2 hours
