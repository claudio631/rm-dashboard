# Task: Hospitality Campaign Launch

> Agent: @ppc-paid-media-specialist, @rm-coordinator
> Elicit: true
> Dependencies: google-ads/knowledge-base.md, reddit-ads/playbook.md, targeting/channel-config.yaml, benchmarks/industry-benchmarks.yaml

## Purpose

Specialized campaign launch workflow for **hospitality roles** (servers, event staff, banquet, housekeeping, bartenders, line cooks). Hospitality has unique characteristics that require a different approach than industrial campaigns:

- **Lower expected CR** (7-10% vs 15% industrial average)
- **Niche candidate pool** (experience-preferred, certifications required)
- **Bilingual opportunity** (Spanish-speaking candidates in many markets)
- **Event-driven demand** (spikes around specific dates, not steady-state)
- **Younger demographic** (18-35 skews heavier than industrial)

## Pre-Conditions
- FHS requisition is Open
- Landing page exists for the role (`indeedflex.com/find-jobs/lp/{role-slug}/`)
- Google Ads conversion tracking verified (run `google-ads-pre-launch-verification.md` first)

## Inputs Required

| Input | Source | Required |
|-------|--------|----------|
| Req ID | FHS | Yes |
| Client name | FHS | Yes |
| Role (Server, Event Staff, etc.) | FHS | Yes |
| Market (city, state) | FHS | Yes |
| Pay rate | FHS | Yes |
| Bilingual required? | JD | Yes |
| Event-specific dates? | Client/JD | If applicable |
| Target RSVPs | User | Yes (suggest: 30 for hospitality) |
| Daily budget (all channels) | User | Yes |
| Landing page URL | FHS/Manual | Yes |

## Workflow

### Phase 1: Market & Role Assessment (5 min)

**Elicit:** Confirm campaign details from requisition.

1. **Check market tier** from `docs/context/2025-conversion-rate-benchmarks.md`:
   - Elite/Strong market → standard approach
   - Below Average/Critical → multi-channel required, flag risk

2. **Check hospitality CR baseline:**
   - Hospitality clients average 7.5-8.8% CR (Merritt 7.5%, Legends 8.8%)
   - Set expectations: **plan for 8% CR, not 15%**
   - Calculate: To get {target RSVPs}, need {RSVPs ÷ 0.08} accounts = {X} clicks at {Y}% CTR

3. **Assess role specificity:**
   - Generic (Event Staff, Hospitality General Labor) → broader targeting OK
   - Specialized (Server, Bartender, Line Cook) → niche targeting, lower volume
   - Certified (Food Handler's required) → mention in ad to pre-qualify

4. **Check bilingual opportunity:**
   - If JD mentions Spanish support → YES: create Spanish ad variants
   - Markets with >20% Hispanic population: Dallas, Houston, Austin, Phoenix, Las Vegas, Orlando, Chicago

### Phase 2: Channel Activation Plan (10 min)

Build the multi-channel plan. Hospitality requires **more channels at lower individual budgets** because the candidate pool is smaller:

| Channel | Include? | Min Budget | Rationale |
|---------|:--------:|:----------:|-----------|
| Indeed Sponsored | **Always** | $15/day | Primary job search channel — CHECK IF ENABLED |
| Google Search | **Always** | $20/day | High-intent hospitality keywords |
| Google Lead Form Extension | **Always** | (included in Search) | Zero-friction mobile apply |
| Google PMax | If budget allows | $25/day | Cross-channel reach for niche role |
| Meta Lead Gen | **Always** | $10/day | Young demo, visual, bilingual targeting |
| Reddit | If market has active subs | $30/day per AG | r/TalesFromYourServer, r/hospitality, r/[city] |
| Craigslist | **Always** | $10/post | Hospitality workers browse CL for event work |
| YouTube Shorts | If video assets exist | $10/day | 15s "work at upscale events" vertical video |
| Braze re-engagement | **Always** | $0 | Push to verified hospitality workers in market |

**Decision tree:**
```
Budget < $50/day  → Indeed + Google Search + Craigslist + Braze
Budget $50-100/day → Above + Meta + Reddit (1 AG)
Budget $100-150/day → Above + PMax + Reddit (2 AGs)
Budget $150+/day  → Full channel activation including YouTube Shorts
```

### Phase 3: Keyword & Targeting Setup (15 min)

#### Google Ads Keywords
| Theme | Keywords | Match |
|-------|----------|:-----:|
| Role-specific | "{role} jobs {city}", "{role} hiring now" | Broad |
| Hospitality broad | "hospitality jobs {city}", "event staff {city}" | Broad |
| Pay-qualified | "{role} jobs ${pay} hour", "high pay {role} {city}" | Broad |
| Long-tail | "upscale {role} part time {city}", "banquet {role} weekends" | Broad |
| Spanish (if bilingual) | "trabajos de {role_es} {city}", "empleo {role_es}" | Broad |

#### Negative Keywords (Hospitality-Specific)
```
- "restaurant manager"
- "chef jobs"
- "server tips reddit"
- "food handler certification class"
- "server training course"
- "culinary school"
- "hotel management"
- "salary" / "salario"
- "remote" / "remoto"
```

#### Meta Targeting
- Age: 18-45
- Interests: Hospitality, Food & Beverage, Event Planning, Catering
- Behaviors: Part-time workers, recently changed jobs
- Location: {city} 25-mile radius
- Language: English + Spanish (if bilingual)

#### Reddit Communities
Research and validate (min 1,000 members each):
- r/{city}, r/{city}jobs
- r/TalesFromYourServer, r/hospitality, r/KitchenConfidential
- r/bartenders (if bartender role)

### Phase 4: Ad Creative (20 min)

**For each channel, create:**

1. **English ad copy** — follow `google-ads/ad-copywriting-playbook.md`:
   - 15 headlines (mix: role+pay, location, urgency, benefits, questions)
   - 4 descriptions (value prop, benefits, urgency, trust)
   - Ad extensions (sitelinks, callouts, structured snippets, location, lead form)

2. **Spanish ad copy** (if bilingual) — use `spanish-ad-copy-tmpl.md`:
   - 10 Spanish headlines
   - 3 Spanish descriptions
   - Separate Spanish ad group in Google

3. **Reddit variants** — per `reddit-ads/playbook.md`:
   - Free-form (organic tone), Image, Lead Gen form
   - Enable comments

4. **Craigslist posting** — lead with pay in title, include role details, direct apply link

5. **Braze push/SMS** — "New {role} shifts in {city} — ${pay}/hr. Book now."

### Phase 5: Pre-Launch Verification (10 min)

- [ ] Run `google-ads-pre-launch-verification.md` checklist
- [ ] Indeed Sponsored status: **ENABLED** (not Disabled!)
- [ ] Landing page loads <3s on mobile (PageSpeed Insights)
- [ ] LP headline matches primary ad headline
- [ ] UTM parameters correct for each channel
- [ ] Reddit Pixel verified (if Reddit active)
- [ ] Meta Pixel verified (if Meta active)
- [ ] Braze segment built for {market} + {role} + verified workers

### Phase 6: Launch & Monitor (ongoing)

1. **Launch all channels simultaneously**
2. **Day 1-3:** Monitor delivery, pixel fires, any errors
3. **Day 5 checkpoint:** If <5 new RSVPs → escalate:
   - Double Google budget
   - Activate PMax if not running
   - Consider hiring event for this market
4. **Day 10 checkpoint:** If <15 RSVPs → deploy contingency:
   - $50 shift completion bonus (per incentive programs)
   - Expand to additional channels
5. **Day 14:** Full performance review → adjust or close

### Phase 7: Optimization Schedule

| Timing | Action |
|--------|--------|
| Day 1-3 | Monitor pixel fires, delivery, placement |
| Day 5 | First checkpoint — RSVPs vs. target |
| Week 1 | Pause underperforming keywords/ads, shift budget |
| Week 2 | Add Spanish variant if not launched, test new creative |
| Week 3 | Expand to secondary channels or reduce spend |
| Week 4 | Full review, decide continue/pause/close |

## Post-Conditions
- All selected channels live and delivering
- Conversion tracking verified across all channels
- RSVP velocity being monitored
- Escalation triggers set at Day 5 and Day 10

## Outputs
- Multi-channel campaign configuration
- Ad copy (English + Spanish if applicable)
- Keyword lists with negatives
- Reddit campaign brief (from template)
- Optimization schedule
- Escalation plan with triggers
