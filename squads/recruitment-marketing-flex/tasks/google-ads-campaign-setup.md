# Task: Google Ads Campaign Setup

// turbo-all

> Agent: @ppc-paid-media-specialist
> Elicit: true
> Dependencies: keyword-strategy-guide.md, campaign-types-reference.md

## Objective
Set up a new Google Ads campaign from scratch following Google's best practices and the recruitment marketing context.

## Pre-Conditions
- Google Ads account exists and is active
- Conversion tracking is configured (see `conversion-tracking-guide.md`)
- Landing pages are live and mobile-optimized
- Budget has been approved

## Workflow

### Step 1: Campaign Type Selection
**Elicit:** What is the primary goal?
- [ ] Drive job applications (→ Search or Performance Max)
- [ ] Build employer brand awareness (→ Video/YouTube or Display)
- [ ] Re-engage past visitors (→ Display Remarketing)
- [ ] Cross-channel reach (→ Performance Max)
- [ ] Promote hiring event (→ Search + Local Services)

### Step 2: Campaign Configuration
- [ ] Name campaign using convention: `{Channel}-{JobCategory}-{Market}-{Goal}`
  - Example: `Search-Warehouse-Texas-Applications`
- [ ] Set campaign goal aligned with conversion actions
- [ ] Select network (Search only, Display, or All)
- [ ] Set geographic targeting (markets with active positions)
- [ ] Set language targeting
- [ ] Set ad schedule (candidate peak search times)
- [ ] Set device targeting preferences

### Step 3: Budget & Bidding
- [ ] Set daily budget (monthly budget ÷ 30.4)
- [ ] Select bidding strategy:
  - New campaign: Maximize Conversions
  - Established (15+ conversions/month): Target CPA
  - Value-focused: Target ROAS
- [ ] Set bid limits if applicable
- [ ] Document budget rationale

### Step 4: Keyword Setup (Search campaigns)
Reference: `keyword-strategy-guide.md`
- [ ] Research keywords using Keyword Planner
- [ ] Organize into themed ad groups (3-20 keywords each)
- [ ] Set match types (broad match recommended with Smart Bidding)
- [ ] Add initial negative keyword list
- [ ] Verify keyword-to-landing-page alignment

### Step 5: Ad Creation
Reference: `ad-copywriting-playbook.md`
- [ ] Create Responsive Search Ads (minimum per ad group):
  - 8-15 headlines (30 chars each)
  - 3-4 descriptions (90 chars each)
  - 2 display URL paths
- [ ] Pin essential headlines to position 1 if needed
- [ ] Check Ad Strength indicator (target: "Good" or "Excellent")
- [ ] Set up ad extensions:
  - [ ] Sitelinks (4+)
  - [ ] Callouts (4+)
  - [ ] Structured snippets
  - [ ] Location extension
  - [ ] Call extension
  - [ ] Lead form extension (if applicable)

### Step 6: Asset Setup (Performance Max)
Reference: `performance-max-playbook.md`
- [ ] Create asset group(s)
- [ ] Upload 15 headlines + 5 descriptions
- [ ] Upload images (landscape, square, portrait)
- [ ] Upload/create video assets
- [ ] Set audience signals (Customer Match, remarketing, custom segments)
- [ ] Verify asset group strength

### Step 7: Conversion Verification
Reference: `conversion-tracking-guide.md`
- [ ] Verify Google Tag fires on all pages
- [ ] Test primary conversion action fires correctly
- [ ] Verify conversion values are assigned
- [ ] Check enhanced conversions are enabled
- [ ] Confirm GA4 is linked

### Step 8: Review & Launch
- [ ] Run through `google-ads-setup-checklist.md`
- [ ] Review all settings in campaign preview
- [ ] Set calendar reminder for 2-week check-in
- [ ] Launch campaign
- [ ] Monitor first 24 hours for issues

## Post-Conditions
- Campaign is live and serving ads
- Conversions are tracking correctly
- Campaign follows naming conventions
- Initial performance benchmarks documented

## Outputs
- Active Google Ads campaign
- Campaign configuration document
- First-week monitoring schedule
