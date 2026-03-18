# Indeed Flex — Daily Tracking Spreadsheet Structure

> Source: `Claudio - March 2026.xlsx` — imported 2026-03-17
> This is the spreadsheet updated daily by the marketing team. It is the primary operational tool.

## Spreadsheet Architecture

### Daily Sheets (one per working day)

**Sheets:** `03_02`, `03_03`, `03_04`, `03_05`, `03_09`, `03_10`, `03_11`, `03_12`, `03_13`, `03_16`

Each daily sheet captures the ads placed that day, combining FHS requisition data with Indeed campaign metrics.

**Columns (41 total):**

| Column | Field | Source | Description |
|--------|-------|--------|-------------|
| A | Req ID | FHS | Requisition ID (e.g., FLEX-23845) |
| B | Job ID attached | ACP | Dummy shift Job ID from ACP |
| C | Role | FHS | Job title (e.g., Loader/Crew, Warehouse Associate) |
| D | Client | FHS | Client name (e.g., CORT, OnTrac, Stord) |
| E | Coverage | Manual | In Coverage / Out of Coverage |
| F | Location | FHS | City, State |
| G | Zip Code | FHS | Zip code of the job |
| H | Status | FHS | Open / Closed |
| I | Channel | Manual | Indeed, Bing, Craigslist, Next Door, Referral, Other |
| J | Campaign Name | Indeed | Full campaign name with naming convention |
| K | Campaign code | Manual | Short code (e.g., #CT-LC-LASNV) |
| L | Campaign Budget | Indeed | Budget allocated |
| M | Status | Indeed | active / closed / paused |
| N | Spend | Indeed | Actual spend |
| O | Clicks | Indeed | Total clicks |
| P | CTR% | Indeed | Click-through rate |
| Q | Cost per click | Calculated | Spend / Clicks |
| R | Started applications | Indeed | Apply starts |
| S | Cost per started app | Calculated | Spend / Started applications |
| T | RSVPs | FHS | AI interviews completed (NOT event RSVPs) |
| U | Total RSVPs (AI Interview complete) | FHS | Cumulative AI interview completions |
| V | Apply > RSVPs | Calculated | Conversion rate: applications to interviews |
| W | Cost per RSVP | Calculated | Spend / RSVPs (cost per AI interview) |
| X | Number verified (role verified) | FHS | Workers who passed verification |
| Y | Conversion (interview attended > verified) | Calculated | Interview to verification rate |
| Z | Cost per verified | Calculated | Spend / Verified |
| AA | RSVP > Verified | Calculated | Conversion: interview to verified |
| AB | ID fixed | Manual | Cleaned Req ID |
| AC | Pay (min) | FHS | Minimum hourly pay |
| AD | Pay (max) | FHS | Maximum hourly pay |

### General Base Sheet (consolidated)

**2,777 rows** — All campaigns across all dates, combining FHS + Indeed data. Same column structure as daily sheets.

### FHS Sheet (requisition data source)

**15,934 rows** — Raw data pulled from FHS (the ATS).

| Column | Field | Description |
|--------|-------|-------------|
| last_updated | Timestamp | When the requisition was last updated |
| requisition_id | Req ID | e.g., FLEX-24214 |
| job_id | Job ID | Numeric ID from FHS |
| job_title | Role | e.g., Cleaner, Loader/Crew, Warehouse Operative |
| agency | Source | Always "Indeed" (this is FHS data) |
| client | Client | e.g., Indeed Flex Applications (dummy shift client) |
| location | Market | e.g., Atlanta, GA |
| pay_rate_min | Pay min | Hourly rate minimum |
| pay_rate_max | Pay max | Hourly rate maximum |
| pay_type | Pay type | PayType.HOURLY |
| rsvps | AI Interviews | Number of completed AI interviews |
| target_rsvps | Target | Target number of AI interviews |
| status | Status | draft / open / closed |

### Indeed Sheet (campaign performance data)

**2,222 rows** — Campaign performance data from Indeed Ads.

| Column | Field | Description |
|--------|-------|-------------|
| Campaign | Name | Campaign name |
| Impressions | Impr | Total impressions |
| Clickthrough rate (CTR) | CTR | Click-through rate |
| Clicks | Clicks | Total clicks |
| Apply start rate (ASR) | ASR | % of clicks that start application |
| Apply starts | Starts | Number of started applications |
| Apply completion rate (ACR) | ACR | % of started apps that complete |
| Applies | Applies | Completed applications |
| Apply rate (AR) | AR | Overall apply rate |
| Spend | Spend | Total spend in USD |
| Cost per click (CPC) | CPC | Average cost per click |
| Cost per apply start (CPAS) | CPAS | Cost per started application |
| Cost per apply (CPA) | CPA | Cost per completed application |
| Job Count | Jobs | Number of jobs in campaign |
| Avg clicks per job | Avg | Average clicks per job |
| Avg apply starts per job | Avg | Average apply starts per job |
| Avg applies per job | Avg | Average applies per job |
| Avg spend per job | Avg | Average spend per job |

## Key Metrics Tracked (Current State)

### Top Funnel (from Indeed)
- Impressions
- Clicks / CTR
- Apply starts / Apply start rate
- Completed applies / Apply completion rate
- Spend / CPC / CPA

### Mid Funnel (from FHS)
- RSVPs (= AI interviews completed)
- Cost per RSVP (cost per AI interview)
- Apply-to-RSVP conversion rate

### Bottom Funnel (from FHS)
- Number verified (role verified after interview)
- Interview-to-verified conversion rate
- Cost per verified worker

## Campaign Naming Convention (Observed)

```
{country}-B2C-{vertical}-{client}-{role_code}-{city},{state}-{month} {year}
```

**Examples:**
- `US-B2C-Industrial-Cort-LC-Las Vegas, NV- March 03`
- `US-B2C-Industrial-Ontrac-Reno, NV- March`
- `US-B2C-Hospitality - SXSW - Event Staff - Austin, Nextdoor`

**Short codes:** `#CT-LC-LASNV` (Client-Role-Market abbreviation)

## Observed Roles in March 2026

| Role | Vertical | Clients |
|------|----------|---------|
| Loader/Crew | Industrial | CORT |
| Picker Packer | Industrial | Stord |
| Assembler | Industrial | CORT |
| Warehouse Associate | Industrial | OnTrac |
| Warehouse Operative | Industrial | OnTrac |
| Package Handler | Industrial | OnTrac |
| Event Staff | Hospitality | SXSW |
| Cleaner | Hospitality | Indeed Flex Applications |
| Concession Stand Worker | Hospitality | Indeed Flex Applications |
| Housekeeping | Hospitality | Raines |
| Electronics Repair Technician | Other | CTDI |

## What RM Team AI Must Replace/Automate

This spreadsheet is the **#1 automation target.** The daily manual workflow is:

1. Pull FHS data (requisitions, RSVPs, verified counts)
2. Pull Indeed data (campaign metrics, spend, clicks, applies)
3. Match requisitions to campaigns by Req ID / Campaign code
4. Calculate derived metrics (CPC, CPA, cost per RSVP, cost per verified)
5. Log in a new daily tab
6. Update General Base with cumulative data
7. Analyze cost per interview, cost per location, cost per client

**RM Team AI should do all of this automatically** by integrating with FHS and Indeed APIs, with the dashboard replacing the spreadsheet.
