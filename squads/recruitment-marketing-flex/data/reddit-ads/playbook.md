# Reddit Ads Playbook — Recruitment Marketing

> Source: Reddit Business Learning Hub + industry guides (March 2026)
> For use by: PPC/Paid Media Specialist agent

## Why Reddit for Recruitment Marketing

- 300M+ monthly active users, strong with 18-29 year-olds
- Reddit users are 27% more likely to purchase/act on advertised products vs other platforms
- Reddit organic search traffic grew 122% (Sept 2025)
- CPCs average ~$2 (vs $30+ on LinkedIn/Google for B2B)
- Conversation placements have 83% higher brand awareness and 5.46% higher action intent vs feed-only
- Desktop share ~40% (vs 10-20% on Facebook) — signals higher intent

## Campaign Objectives for Recruitment

| Objective | When to Use |
|-----------|-------------|
| **Conversions** | Primary — optimize for job applications/RSVPs |
| **Traffic** | Drive to job landing pages or hiring event pages |
| **Lead Generation** | Native form for quick applicant capture (no landing page needed) |
| **Brand Awareness** | Employer branding in target markets |
| **Video Views** | "Day in the life" or facility tour content |

## Ad Formats

| Format | Best For Recruitment | Specs |
|--------|---------------------|-------|
| **Free-Form Ads** | Job posts that blend into subreddit discussions | Text + image + GIF, looks like organic post |
| **Image Ads** | Standard job ad with role/pay/location | Feed + conversation placement |
| **Video Ads** | Facility tours, "day in the life", hiring event promos | Autoplay (sound off), square/portrait/landscape |
| **Carousel Ads** | Multiple roles, multiple locations, benefits showcase | 2-6 swipeable cards, TOP PERFORMER |
| **Lead Gen Ads** | Quick apply — collects name/email/phone in-app | Native form, reduces drop-off vs external LP |

## Targeting Strategy for Staffing/Temp Workers

### Community (Subreddit) Targeting — PRIMARY
Target subreddits where potential workers are active:

**Job-seeking communities:**
- r/jobs, r/jobsearch, r/forhire, r/WorkOnline
- r/sidehustle, r/beermoney, r/gig (gig workers)

**Location-specific communities:**
- r/vegas, r/LasVegas, r/orlando, r/chicago, r/dallas, r/austin
- r/[city]jobs (e.g., r/DenverJobs, r/nycjobs)

**Industry communities:**
- r/warehouse, r/warehouseworkers
- r/hospitality, r/TalesFromYourServer, r/bartenders, r/KitchenConfidential
- r/forklift (forklift operators)

**Rules:**
- Start with 3-5 subreddits per ad group
- Minimum 1,000 members per subreddit
- Smaller niche communities outperform large general ones
- Keep community and keyword targeting in SEPARATE ad groups (they compound, not layer)

### Keyword Targeting — SECONDARY
- 29.6% higher CTR than community or interest targeting (per Reddit)
- Target job-related search terms: "warehouse job", "hiring near me", "forklift job Las Vegas"
- Segment by placement (conversation vs feed)

### Interest Targeting — SCALE
- Pre-set categories: use for broad reach after validating with community targeting
- Better for scaling proven campaigns

### Location Targeting
- Target by city/state matching open requisitions
- Critical for staffing — workers need to be local

### Custom Audiences
- **Retargeting:** Website visitors (career page, job listings) — $2-5 CPC vs $30+ elsewhere
- **Customer lists:** Upload past applicant lists (min 1,000 matched users)
- **Lookalikes:** Build from high-quality applicants (min 10,000 retargeting users or 1,000 list contacts)
- **Exclusions:** Current workers, already-hired, competitors

## Campaign Structure

```
Campaign: [Client] - [Market] - [Objective] - [Date]
├── Ad Group 1: Community Targeting (3-5 subreddits)
│   ├── Ad 1: Free-form (job description style)
│   ├── Ad 2: Image (branded job ad)
│   └── Ad 3: Video (facility tour)
├── Ad Group 2: Keyword Targeting (job-related terms)
│   ├── Ad 1: Free-form
│   └── Ad 2: Lead gen
└── Ad Group 3: Retargeting (career page visitors)
    ├── Ad 1: Carousel (multiple roles)
    └── Ad 2: Lead gen (quick apply)
```

**Naming convention:** `Campaign Type | Client | Market | Launch Date`

## Bidding & Budget

| Strategy | When to Use | Notes |
|----------|-------------|-------|
| **Lowest Cost** | Default — recommended | Maximizes conversions within budget |
| **Cost Cap** | When you need CPC control | Sets average CPC cap |
| **Manual** | Advanced — strict CPC limit | Use after learning phase |

- **Minimum budget:** $30/day per ad group for algorithmic optimization
- **Average CPC:** ~$2 (rarely exceeds $5)
- **Recommended test budget:** 10-15% of total recruitment media spend

## Creative Best Practices for Job Ads

1. **Tone:** Conversational, not corporate — Reddit users reject "HR speak"
2. **Lead with value:** Pay rate, benefits, schedule flexibility — not company mission statements
3. **Emojis:** Significantly higher CTR (use sparingly, not excessively)
4. **Enable comments:** Makes ads look organic; monitor and respond
5. **Soft CTA:** "Check out these open roles" > "Apply Now!"
6. **Authenticity:** Match the subreddit's language and culture
7. **A/B test:** Duplicate ads, change one variable (headline, image, CTA)

**Example job ad copy:**
```
💰 $17-19/hr Warehouse Jobs in Las Vegas — Start This Week

We're hiring picker/packers and forklift operators for day and night shifts.
No experience needed for most roles. Weekly pay, flexible scheduling.

Multiple locations in LV area. Quick apply — 2 minutes.
```

## Placement Strategy

| Placement | Best For | Intent Level |
|-----------|----------|-------------|
| **Conversation** | High-intent job seekers actively discussing work | HIGHEST — recommended |
| **Feed** | Broad awareness, employer branding | MEDIUM — passive scrolling |
| **Desktop** | Higher intent, better conversion rates | HIGHEST |
| **Mobile** | Volume, younger demographic | HIGH — most traffic |

**Recommended:** Conversation + Desktop for best CPL. Mobile for volume.

## Conversion Tracking Setup

1. Install Reddit Pixel via Google Tag Manager
2. Create conversion events: `lead`, `sign-up`, `page_visit`
3. Set attribution windows to maximum for data collection
4. Add UTM parameters to all landing pages:
   - `utm_source=reddit`
   - `utm_medium=paid`
   - `utm_campaign=[campaign-name]`
   - `{{CLICK_ID}}` for Reddit attribution
   - `{{ADVERTISING_ID}}` for device tracking

## MAX Campaigns (New — 2026)

Reddit's AI-optimized campaign type:
- **17% lower cost per action** vs standard campaigns
- **27% more conversions** in split tests
- Automated targeting, bidding, and creative optimization
- **Recommendation:** Allocate 10-15% of Reddit budget to MAX as a test

## Brand Safety

**Exclude these communities** (low intent, high waste):
- r/Funny, r/Memes, r/Gaming, r/Movies, r/aww, r/Music
- Any community not relevant to your target market

## Performance Benchmarks

| Metric | Reddit Avg | Indeed Flex Target |
|--------|-----------|-------------------|
| CPC | $2.00 | < $3.00 |
| CTR | 0.5-1.5% | > 1.0% |
| Apply Rate | 5-15% | > 10% |
| Cost per RSVP | TBD | < $20.00 |
| Cost per Hire | TBD | < $100.00 |

## Optimization Cadence

| Timeframe | Action |
|-----------|--------|
| Day 1-3 | Monitor delivery, ensure pixel fires, check placements |
| Week 1 | Review CTR and CPC by ad group, pause underperformers |
| Week 2 | Shift budget to top-performing communities and formats |
| Week 3 | Expand with keyword targeting or new communities |
| Week 4 | Full performance review, build retargeting audiences |
| Monthly | Report on Cost/RSVP, Cost/Hire, compare vs Indeed/Google |
