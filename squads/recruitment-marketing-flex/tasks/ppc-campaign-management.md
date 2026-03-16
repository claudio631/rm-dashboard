---
task: PPC Campaign Management
responsavel: "@ppc-paid-media-specialist"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - channel: Target advertising channel (Indeed, Google, Meta, Bing, Reddit, Craigslist)
  - campaign_type: Campaign objective (candidate acquisition, brand awareness, retargeting)
  - budget: Daily/monthly budget allocation
  - markets: Target geographic markets
  - job_categories: Job types to promote (warehouse, delivery, retail, hospitality, etc.)
Saida: |
  - campaign_brief: Complete campaign setup document
  - targeting_spec: Audience targeting parameters
  - ad_creatives: Ad copy and creative recommendations
  - bid_strategy: Recommended bidding approach
  - kpi_targets: Expected performance benchmarks
Checklist:
  - "[ ] Define campaign objective and KPIs"
  - "[ ] Research keywords/audiences for target market"
  - "[ ] Create audience targeting spec"
  - "[ ] Write ad copy variations (min 3)"
  - "[ ] Set bid strategy and budget pacing"
  - "[ ] Configure conversion tracking"
  - "[ ] Set up A/B test framework"
  - "[ ] Create negative keyword/exclusion lists"
  - "[ ] Review compliance (job ad regulations)"
  - "[ ] Document campaign in tracking sheet"
---

# PPC Campaign Management

Create and optimize paid recruitment advertising campaigns for Indeed Flex across all channels.

## Supported Channels

| Channel | Campaign Types | Key Features |
|---------|---------------|--------------|
| Indeed Ads | Sponsored jobs, PPC | Job slot bidding, resume targeting |
| Google Ads | Search, PMax, Display, YouTube | Keyword targeting, smart bidding |
| Meta Ads | Lead gen, awareness, retargeting | Lookalike audiences, dynamic creative |
| Bing Ads | Search, audience | LinkedIn targeting, Google import |
| Reddit Ads | Promoted posts, conversations | Subreddit targeting, community focus |
| Craigslist | Job postings | Geographic metro targeting |

## Elicitation Flow

```
? Which channel is this campaign for?
  > Indeed Ads
    Google Ads
    Meta Ads
    Bing Ads
    Reddit Ads
    Craigslist

? Campaign objective?
  > Candidate acquisition (applications)
    Brand awareness (impressions/reach)
    Retargeting (past visitors/applicants)

? Target markets? (comma-separated cities/states)
? Job categories to promote?
? Daily budget?
? Campaign duration?
```

## Output: Campaign Brief

The campaign brief includes:
1. **Objective & KPIs** — What success looks like
2. **Targeting** — Who we reach and where
3. **Creative** — Ad copy, visuals, CTAs
4. **Bidding** — Strategy and budget pacing
5. **Tracking** — UTMs, pixels, conversion events
6. **Testing** — A/B test plan
