# Google Ads — New Campaign Implementation Checklist

> **Owner:** Parker (@ppc-paid-media-specialist)
> **Use:** Every time Claudio asks to implement a new Google Ads campaign
> **Last Updated:** 2026-04-09

---

## Phase 0: Intake & Clarification

Before writing any brief or code, confirm these with Claudio:

- [ ] **Campaign type:** BAU (ongoing) or Hiring Event (burst)?
- [ ] **Client name** and **role/job title**
- [ ] **Location** (city, state, zip) — confirm metro area for geo-targeting
- [ ] **Pay rate** confirmed (never use placeholder in live ads)
- [ ] **Daily budget** per campaign (Search / P.Max / App)
- [ ] **Start date** and **end date** (if hiring event)
- [ ] **Final URL** — confirm job browse ID, employer slug, metro, role
- [ ] **Any special promos?** (sign-on bonus, referral bonus, same-day pay, etc.)

### If Hiring Event:
- [ ] **Event date, time, and venue address**
- [ ] **Duplicate BAU campaigns** — never edit originals (they stay live untouched)
- [ ] **Post-event plan:** Pause the duplicate campaigns after event ends (never $1/day wind-down)
- [ ] **Never pause existing ad groups** — only UPDATE with event copy and ADD new event-specific groups

---

## Phase 1: Campaign Brief

Write the full brief in `squads/recruitment-marketing-flex/data/campaign-briefs/google-ads-{client}-{role}-{location}.md`

### Brief Structure (required sections):

- [ ] **Campaign Overview tables** — one per campaign type (Search, P.Max, App)
  - Campaign name following convention: `p-b2c-google-{type}-us-bofu-{bau|event}-{market}-{role}-{client}--eg--`
  - Campaign type, objective, dates, daily budget, bidding strategy, target CPA
- [ ] **Budget Summary table** — all campaigns + total daily spend
- [ ] **Job Details table** — client, role, location, pay rate, shift schedule
- [ ] **Final URL** with full UTM parameters
- [ ] **Geo-Targeting table** — radius tiers with bid adjustments + exclusions
- [ ] **Ad Group Structure** — minimum 2–3 themed ad groups per Search campaign
- [ ] **Keywords section** — organized by ad group
- [ ] **Ad Copy section** — 3 RSA variants per ad group (see Phase 2)
- [ ] **P.Max Asset Group** — headlines, long headlines, descriptions, images, audience signals
- [ ] **App Campaign copy** — 5 headlines + 5 descriptions
- [ ] **Ad Extensions** — sitelinks (4+), callouts (6+), structured snippets
- [ ] **Conversion Setup table**
- [ ] **Success Criteria table** — CPA, CTR, impression share, CPC targets
- [ ] **Implementation Checklist** — pre-launch, per-campaign, post-launch
- [ ] **Approvals table** — awaiting Claudio's sign-off

---

## Phase 2: Ad Copy Rules (NON-NEGOTIABLE)

### RSAs — Search Campaign
- [ ] **3 RSAs per ad group** — each with a DISTINCT angle (e.g., Urgency / Pay & Benefits / Process & Opportunity)
- [ ] **15 headlines** per RSA (max 30 chars each)
- [ ] **4 descriptions** per RSA (max 90 chars each)
- [ ] **Display paths on EVERY RSA** — `path1` + `path2` (e.g., `Warehouse-Jobs` / `Lebanon-TN`). NEVER omit.
- [ ] **Final URL** set on every ad
- [ ] Character count verified — no headline > 30 chars, no description > 90 chars

### Copywriter Workflow
- [ ] **Activate @copywriter** BEFORE writing ads: `/AIOX:agents:copywriter` then `*write-ad-copy google-ads {role} {market}`
- [ ] 3 copy variants with different hooks, CTAs, and narratives
- [ ] Review for character limits and keyword alignment
- [ ] **No em dashes (—)** in ad copy — signals AI writing, not human tone

### P.Max Asset Group
- [ ] 15 short headlines (30 chars)
- [ ] 5 long headlines (90 chars) — must be self-contained (shown without description)
- [ ] 5 descriptions (90 chars)
- [ ] Images: 3+ landscape (1200x628), 3+ square (1200x1200), 1+ portrait (960x1200)
- [ ] Logo (square + landscape)
- [ ] Audience signals configured

### App Campaign (UAC)
- [ ] 5 headlines + 5 descriptions per ad group
- [ ] 3 ad groups with distinct angles (matching Search RSA themes)

---

## Phase 3: Keywords (NON-NEGOTIABLE)

- [ ] **PHRASE match ONLY** — never exact match. Broad allowed as supplement.
- [ ] Keywords organized into themed ad groups (role-specific, client-brand, generic-intent)
- [ ] **Negative keyword list** applied to ALL ad groups (remote, work from home, CDL, manager, supervisor, competitor brands, etc.)
- [ ] No duplicate keywords across ad groups
- [ ] Location modifiers included in keyword text

---

## Phase 4: Approval Gate

- [ ] Brief presented to Claudio for review
- [ ] **Wait for explicit "APPROVED" or "go" before implementation**
- [ ] Any requested changes applied to brief before proceeding

---

## Phase 5: API Implementation

### Script Creation
- [ ] Create script: `scripts/google-ads-{description}.py`
- [ ] Reference existing patterns in `scripts/google-ads-*.py`
- [ ] Use `GoogleAdsClient.load_from_storage("google-ads.yaml")`
- [ ] Customer ID: `7236100723` / Login Customer ID: `6531650309`

### Script Must Include (in single `main()` flow):
- [ ] Campaign creation with correct naming convention
- [ ] Budget creation ($X/day)
- [ ] Bidding strategy (Maximize Conversions / tCPA)
- [ ] Geo-targeting (location IDs with radius + bid adjustments)
- [ ] Ad group creation (all groups)
- [ ] Keywords — all PHRASE match (+ BROAD where specified)
- [ ] Negative keywords on all ad groups
- [ ] **All 3 RSAs per ad group baked into the script** — never create 1 ad then fix later
- [ ] `path1` and `path2` on every RSA
- [ ] Final URL on every ad
- [ ] Ad extensions (sitelinks, callouts, structured snippets)

### For P.Max:
- [ ] Campaign + budget + bidding
- [ ] Asset group with all headlines, long headlines, descriptions
- [ ] Image assets (copy from nearest active P.Max if no new creatives)
- [ ] Audience signals

### For App (UAC):
- [ ] Campaign + budget + bidding (tCPA)
- [ ] 3 ad groups with 5 headlines + 5 descriptions each
- [ ] Geo-targeting

---

## Phase 6: Execution & Verification

- [ ] Run script via Bash
- [ ] Capture all campaign/ad group/ad IDs from output
- [ ] **Update brief** with campaign IDs and LIVE status
- [ ] Mark implementation checklist items as `[x]` in brief
- [ ] Update brief Change Log with deployment details

---

## Phase 7: Post-Launch Verification (Day 0–3)

- [ ] Final URL loads correctly on mobile
- [ ] Conversion tracking fires on registration / app download
- [ ] Impressions appearing within 2 hours of launch
- [ ] Search impression share > 40% after 48 hours (if not, review keywords/bids)
- [ ] P.Max search terms align with intent (first 7 days)
- [ ] No policy disapprovals on ads

### If Hiring Event:
- [ ] Event date reminders set for campaign pause
- [ ] BAU campaigns confirmed still running untouched

---

## Quick Reference — Common Mistakes to Avoid

| Rule | Violation | Correct |
|------|-----------|---------|
| 3 ads per ad group | Launching with 1 RSA | Always 3 distinct RSAs per ad group |
| Display paths | Omitting path1/path2 | Every RSA gets path1 + path2 |
| Match type | Using EXACT match | PHRASE only (+ BROAD supplement) |
| Hiring events | Editing BAU campaigns | Duplicate BAU, keep originals live |
| Post-event | $1/day wind-down | Pause duplicate campaigns |
| Existing ad groups | Pausing them during events | Keep running, only add/update |
| Copy tone | Overusing em dashes (—) | Use commas, periods, natural punctuation |
| Script structure | 1 ad now, fix later | All 3 RSAs in the initial main() flow |

---

*Parker (@ppc-paid-media-specialist) — optimizing every impression*
