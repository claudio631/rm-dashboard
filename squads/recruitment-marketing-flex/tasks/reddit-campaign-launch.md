# Task: Reddit Campaign Launch

> Agent: @ppc-paid-media-specialist
> Trigger: `*launch-reddit-campaign`
> Template: `reddit-campaign-brief-tmpl.md`
> Playbook: `data/reddit-ads-playbook.md`

## Purpose

Launch a new Reddit Ads campaign for a client/market recruitment need. Follows the Reddit Ads Playbook targeting strategy optimized for staffing/temp worker acquisition.

## Inputs Required

| Input | Source | Required |
|-------|--------|----------|
| Client name | User | Yes |
| Market (city, state) | User or FHS requisitions | Yes |
| Role(s) | User or FHS requisitions | Yes |
| Pay rate | User or FHS requisitions | Yes |
| Daily budget | User | Yes (min $30/ad group) |
| Landing page URL | User | Yes |
| Campaign duration | User | Yes |

## Workflow

### Phase 1: Research (elicit: true)

1. **Confirm campaign details** with user:
   - Client, market, role, pay rate
   - Budget and duration
   - Landing page URL
   - Objective (default: Conversions)

2. **Research subreddits** for the target market:
   - Search for r/[city] and r/[city]jobs communities
   - Search for industry-relevant communities (r/warehouse, r/hospitality, etc.)
   - Verify each has 1,000+ members
   - Recommend 3-5 subreddits per ad group

3. **Identify keywords** for keyword targeting ad group:
   - Job-related: "[role] job [city]", "hiring [city]", "[role] near me"
   - Industry-related: "warehouse work", "forklift job", "server job"
   - Recommend 5-10 keywords

### Phase 2: Build Campaign Brief

4. **Generate campaign brief** from template `reddit-campaign-brief-tmpl.md`:
   - Fill all placeholders with confirmed details
   - Include subreddit and keyword recommendations
   - Set UTM parameters

5. **Write ad creative variants:**
   - Variant A: Free-form ad (organic style, conversational tone)
   - Variant B: Image ad (branded, lead with pay rate)
   - Variant C: Lead gen or carousel (if applicable)
   - Follow playbook creative rules: no HR speak, emojis OK, enable comments

6. **Present brief to user for approval** (elicit: true)

### Phase 3: Launch Checklist

7. **Walk through launch checklist:**
   - [ ] Reddit Pixel verified
   - [ ] Conversion events configured
   - [ ] UTM parameters added
   - [ ] Brand safety exclusions set
   - [ ] Subreddits validated
   - [ ] Ad copy reviewed (community voice, not corporate)
   - [ ] A/B test configured
   - [ ] Budget set (≥$30/ad group/day)
   - [ ] Comments enabled
   - [ ] Landing page tested (mobile + desktop)

8. **Output final campaign brief** → save to `docs/campaigns/reddit-[client]-[market]-[date].md`

### Phase 4: Optimization Plan

9. **Set optimization schedule:**
   - Day 1-3: Monitor delivery, pixel fires, placements
   - Week 1: Review CTR/CPC by ad group, pause underperformers
   - Week 2: Shift budget to top communities/formats
   - Week 3: Expand with new keywords or communities
   - Week 4: Full review, build retargeting audiences

## Output

- Campaign brief document (saved to `docs/campaigns/`)
- Ad copy variants (3 minimum)
- Subreddit research list
- Keyword list
- Optimization schedule

## Dependencies

- `data/reddit-ads-playbook.md` — Campaign strategy and benchmarks
- `templates/reddit-campaign-brief-tmpl.md` — Brief template
- `checklists/campaign-launch-checklist.md` — Launch validation
