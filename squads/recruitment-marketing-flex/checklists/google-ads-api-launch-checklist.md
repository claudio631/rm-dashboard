# Google Ads API Launch Checklist

> **MANDATORY** for every `*launch-campaign` or `*create-campaign` execution via Google Ads Python SDK.
> Follow this checklist sequentially. Do NOT skip steps.

---

## NON-NEGOTIABLE Campaign Standards

These rules apply to EVERY campaign. Violation = blocked launch.

| # | Rule | Severity |
|---|------|----------|
| 1 | Every campaign must have **minimum 3 ad groups** | NON-NEGOTIABLE |
| 2 | Every ad group must have **minimum 3 ads** (RSAs) | NON-NEGOTIABLE |
| 3 | Every ad must have **relevant keywords** from the keyword setup + a **different copy strategy** (e.g., Urgency / Pay & Benefits / Process) to A/B test performance | NON-NEGOTIABLE |
| 4 | All keywords must be **PHRASE match only** — no Exact, no Broad | NON-NEGOTIABLE |
| 5 | Final URL must be the **exact URL from the approved brief** — no modifications | NON-NEGOTIABLE |
| 6 | Display path must always be `{industry}-Jobs / {Location}` (e.g., `Warehouse-Jobs / Lebanon-TN`) | NON-NEGOTIABLE |
| 7 | Ad copy headlines should be **based on best performers** from other campaigns — check existing campaign metrics before writing new copy | NON-NEGOTIABLE |
| 8 | **NEVER mention the client name** in ad copy (no "OnTrac", "Tennant", "Stord", etc.) — ads may be reused for other clients | NON-NEGOTIABLE |
| 9 | P.Max asset group must have **minimum 5 images** matching the industry type | NON-NEGOTIABLE |
| 10 | Business Name must **always** be "Indeed Flex" | NON-NEGOTIABLE |
| 11 | **Minimum 6 sitelinks** — complementary to ad copy, not redundant | NON-NEGOTIABLE |
| 12 | **Structured snippets enabled**, minimum 3 | NON-NEGOTIABLE |
| 13 | **Minimum 4 callout extensions** | NON-NEGOTIABLE |

---

## Prerequisites

- [ ] **Approved brief exists** in `squads/recruitment-marketing-flex/data/campaign-briefs/`
- [ ] **Final URL verified** — run `WebFetch` to confirm page loads, correct job browse ID, employer, metro
- [ ] **Final URL matches brief exactly** — do NOT modify the URL from what was approved (Rule 5)
- [ ] **Pay rate confirmed** — match ad copy to actual pay (no placeholders like `$XX`)
- [ ] **No client names in ad copy** — verify all headlines/descriptions are client-agnostic (Rule 8)
- [ ] **Reference script identified** — pick closest existing script from `scripts/google-ads-*.py`
- [ ] **Check top-performing headlines** from existing campaigns before writing copy (Rule 7):
  ```sql
  SELECT ad_group_ad.ad.responsive_search_ad.headlines, metrics.impressions, metrics.clicks, metrics.conversions
  FROM ad_group_ad
  WHERE campaign.advertising_channel_type = 'SEARCH'
  AND ad_group_ad.status = 'ENABLED'
  AND metrics.impressions > 1000
  ORDER BY metrics.conversions DESC
  LIMIT 20
  ```

## SDK Setup (every script)

```python
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"
client = GoogleAdsClient.load_from_storage(YAML_PATH)
```

- [ ] Config path: `google-ads.yaml` (project root)
- [ ] Customer ID: `7236100723`
- [ ] Login customer ID: `6531650309` (in yaml)

## Campaign Creation Order

### 1. Budget

- [ ] Create dedicated budget (`explicitly_shared = False`)
- [ ] Set `amount_micros` (e.g., $30/day = `30_000_000`)
- [ ] Name format: `BAU {Location} {Type}` or `Hiring Event {Location} {Type} {Date}`

### 2. Search Campaign

- [ ] Set `advertising_channel_type = SEARCH`
- [ ] Set `maximize_conversions.target_cpa_micros = 0` (no tCPA initially)
- [ ] Set `contains_eu_political_advertising = 3` (DOES_NOT_CONTAIN) — **REQUIRED**
- [ ] Set network settings (target_google_search=True, target_content_network=False)
- [ ] Set `end_date` ONLY for hiring events (BAU = no end date)
- [ ] Set geo target via `CampaignCriterionService`

### 3. Search Ad Groups — minimum 3 per campaign (Rule 1)

- [ ] Create **minimum 3 ad groups** with `type_ = SEARCH_STANDARD`
- [ ] Set `cpc_bid_micros` (default: `2_500_000` = $2.50)
- [ ] Add keywords via `AdGroupCriterionService`:
  - Match type: **PHRASE only** — no Exact, no Broad (Rule 4)
  - Each ad group gets its own relevant keyword set
  - Verify keyword count matches brief
- [ ] Add negative keywords (`negative = True`, match type = PHRASE)

### 4. Search Ads — minimum 3 per ad group (Rule 2)

- [ ] Add **3 RSAs per ad group** — each with a **different copy strategy** (Rule 3):
  - Variant 1: **Urgency** angle (hiring now, start this week, limited spots)
  - Variant 2: **Pay & Benefits** angle (pay rate, Same Day Pay, health benefits)
  - Variant 3: **Process & Opportunity** angle (easy apply, no experience, full-time potential)
- [ ] Each RSA must have:
  - 15 headlines (max 30 chars each)
  - 4 descriptions (max **90 chars** each — validate lengths before sending)
  - Display path: `path1 = {Industry}-Jobs`, `path2 = {Location}` (Rule 6)
    - Example: `Warehouse-Jobs / Lebanon-TN`
  - `final_urls` = exact URL from approved brief — no changes (Rule 5)
- [ ] **No client names in any headline or description** (Rule 8)
  - BAD: "OnTrac Hiring Near You", "Join Tennant Today"
  - GOOD: "Warehouse Jobs Near You", "Hiring Now — Apply Today"
- [ ] Headlines should reference **top performers from other campaigns** (Rule 7)
- [ ] Verify: minimum 3 ads created per ad group, minimum 9 total

### 5. Ad Extensions (Search Campaign)

- [ ] **Sitelinks: minimum 6** — complementary to ad copy, not redundant (Rule 11)
  - Each sitelink must add value beyond what the ad already says
  - Example: Browse All Jobs, Download the App, Same Day Pay Info, Benefits Overview, Shift Schedule, How It Works
- [ ] **Structured snippets: minimum 3, enabled** (Rule 12)
  - Job Types, Benefits, Shifts — use relevant categories
- [ ] **Callout extensions: minimum 4** (Rule 13)
  - Example: Same Day Pay, No Experience Required, Flexible Shifts, Health Benefits, $75 Referral Bonus

### 6. App Campaign

- [ ] Fetch source app campaign settings (app_id, app_store, bidding_strategy_goal_type)
- [ ] Source reference: Nashville BAU App (ID: `23062774690`)
- [ ] Set `advertising_channel_type = MULTI_CHANNEL`
- [ ] Set `advertising_channel_sub_type = APP_CAMPAIGN`
- [ ] Copy `app_campaign_setting` from source (app_id=`com.syftapp.android`, store=GOOGLE)
- [ ] Set bidding: `target_cpa.target_cpa_micros = 2_000_000` ($2.00 tCPA)
- [ ] Set `contains_eu_political_advertising = 3` — **REQUIRED**
- [ ] Set geo target
- [ ] **App ad limit: 1 ad per ad group** — create separate ad group per variant (minimum 3 ad groups)
- [ ] Add 5 headlines + 5 descriptions per app ad
- [ ] **No client names in headlines or descriptions** (Rule 8)
- [ ] Business Name = "Indeed Flex" (Rule 10)

### 7. Performance Max Campaign

> P.Max requires **atomic batch creation** due to Brand Guidelines.

- [ ] **Step A — Create campaign + brand assets atomically** via `GoogleAdsService.mutate()`:
  ```
  MutateOperation: campaign_operation.create (use temp resource_name: customers/{cid}/campaigns/-1)
  MutateOperation: campaign_asset_operation.create → BUSINESS_NAME (asset ID: 11226590211)
  MutateOperation: campaign_asset_operation.create → LOGO (asset IDs: 56893637546, 336730299860)
  MutateOperation: campaign_asset_operation.create → LANDSCAPE_LOGO (asset ID: 56894244206)
  MutateOperation: campaign_criterion_operation.create → geo target
  ```
- [ ] Set `advertising_channel_type = PERFORMANCE_MAX`
- [ ] Set `maximize_conversions.target_cpa_micros = 0`
- [ ] Set `contains_eu_political_advertising = 3`

- [ ] **Step B — Create text assets** via `AssetService.mutate_assets()` (batch all at once):
  - 15 headlines
  - 5 long headlines (max 90 chars)
  - 5 descriptions (max 90 chars)

- [ ] **Step C — Create asset group + link assets atomically** via `GoogleAdsService.mutate()`:
  ```
  MutateOperation: asset_group_operation.create (temp: customers/{cid}/assetGroups/-2)
  MutateOperation: asset_group_asset_operation.create × N (headlines, long headlines, descriptions, images)
  ```
  - **Image aspect ratio mapping** (CRITICAL — wrong mapping = API error):
    - `MARKETING_IMAGE` → landscape images (1.91:1 ratio, ~1200×628)
    - `SQUARE_MARKETING_IMAGE` → square images (1:1 ratio, ~1200×1200)
    - `PORTRAIT_MARKETING_IMAGE` → portrait images (4:5 ratio, ~960×1200)
    - `LOGO` → square logos (1:1)
  - **Minimum 5 images matching the industry type** (Rule 9):
    - At least 3 landscape (1.91:1)
    - At least 2 square (1:1)
    - Portrait recommended (4:5)
  - Reuse image assets from existing BAU P.Max campaigns (Houston, Nashville, etc.)
  - Do NOT link LOGO or BUSINESS_NAME at asset group level — already at campaign level
  - **No client names in any text asset** (Rule 8)
  - **Business Name = "Indeed Flex"** always (Rule 10)
  - Check image dimensions with GAQL query before mapping:
    ```sql
    SELECT asset.id, asset.image_asset.full_size.width_pixels, asset.image_asset.full_size.height_pixels
    FROM asset WHERE asset.id IN (...)
    ```

## Post-Launch Verification

- [ ] Query GAQL to confirm all campaigns are ENABLED:
  ```sql
  SELECT campaign.id, campaign.name, campaign.status
  FROM campaign WHERE campaign.name LIKE '%{location}%' AND campaign.status != 'REMOVED'
  ```
- [ ] **Rule 1 check:** Verify minimum 3 ad groups per campaign
- [ ] **Rule 2 check:** Verify minimum 3 ads per ad group (Search: 3 RSAs, App: 1 per AG × 3 AGs)
- [ ] **Rule 4 check:** Verify all keywords are PHRASE match (no Exact, no Broad)
- [ ] **Rule 5 check:** Verify Final URL matches approved brief exactly
- [ ] **Rule 6 check:** Verify display paths follow `{Industry}-Jobs / {Location}` format
- [ ] **Rule 8 check:** Grep all headlines/descriptions — NO client names present
- [ ] **Rule 9 check:** P.Max has minimum 5 images
- [ ] **Rule 10 check:** Business Name = "Indeed Flex"
- [ ] **Rule 11 check:** Minimum 6 sitelinks attached
- [ ] **Rule 12 check:** Structured snippets enabled, minimum 3
- [ ] **Rule 13 check:** Minimum 4 callout extensions
- [ ] Update brief checklist — mark all items [x] with campaign IDs
- [ ] Update brief status → `LIVE`
- [ ] Update brief change log with launch date, campaign IDs, asset counts

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `BIDDING_STRATEGY_TYPE_INCOMPATIBLE_WITH_SHARED_BUDGET` | Budget is shared | Set `explicitly_shared = False` on budget |
| `REQUIRED` (contains_eu_political_advertising) | Missing field | Add `c.contains_eu_political_advertising = 3` |
| `TOO_LONG` (string_length) | Description > 90 chars | Trim descriptions, validate lengths before sending |
| `REQUIRED_BUSINESS_NAME_ASSET_NOT_LINKED` | Brand Guidelines enabled | Create campaign + brand assets atomically via batch mutate |
| `ASPECT_RATIO_NOT_ALLOWED` | Wrong image → field_type mapping | Check actual image dimensions, map 1.91:1→MARKETING, 1:1→SQUARE |
| `RESOURCE_LIMIT` (APP_ADS_PER_AD_GROUP) | App campaign: 1 ad/AG limit | Create separate ad group per ad variant |
| `NOT_ENOUGH_*_ASSET` | Asset group created without assets | Use atomic batch: asset_group + asset_group_asset in one mutate() |

## Key Asset IDs (Account-Level)

| Asset | ID | Type |
|-------|----|------|
| Business Name "Indeed Flex" | `11226590211` | TEXT |
| Square Logo (RGB) | `56893637546` | IMAGE |
| Square Logo (Icon) | `336730299860` | IMAGE |
| Landscape Logo (RGB) | `56894244206` | IMAGE |
| App ID | `com.syftapp.android` | — |

## Script Naming Convention

```
scripts/google-ads-{client}-{role}-{location}.py       # BAU campaigns
scripts/google-ads-{location}-hiring-event.py          # Hiring events
scripts/google-ads-{location}-resume.py                # Resume failed run
```

---

*Checklist v2.0 — Updated 2026-04-09 — Added 13 non-negotiable campaign standards per Claudio*
