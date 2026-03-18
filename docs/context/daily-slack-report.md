# Indeed Flex — EOD Update Key Clients

> Source: Stakeholder interview + sample report — 2026-03-17
> This report is posted daily to a Slack channel by the Recruitment Marketing team.

## Report Overview

**Channel:** Slack (team channel, @here mention)
**Frequency:** Daily (end of day, weekdays only — no reports Saturday/Sunday)
**Author:** Claudio (currently compiled manually using Gemini AI)
**Data Sources:** 3 separate systems, manually combined

| Source | Data Provided |
|--------|--------------|
| **Tableau** | OB (Onboarding) funnel split report — unique accounts created vs verified |
| **Indeed Analytics** | Campaign spend (JobsCampaigns CSV) |
| **FHS** | Requisition report (open campaigns, roles, clients) |

## Report Structure

### Section 1: Key Client Unique Accounts

**Data Source:** Tableau — OB (Onboarding) funnel split report (`OB Funnel Custom Viewer.xlsx`)

Organized by **client → location**, showing:
- **Created** = sum of "Worker Accounts Created" for the **last 30 rolling days** per client/location
- **Verified** = sum of "1st Role Verified (# Workers)" for the **last 30 rolling days** per client/location
- **(+N)** = yesterday's (D-1) single-day "1st Role Verified (# Workers)" count — this is a **single day value**, NOT a cumulative difference

**Comparison logic (D-1 rule):**
- **Tuesday → Friday:** `(+N)` = yesterday's (D-1) single-day "1st Role Verified" count from Tableau
- **Monday:** `(+N)` = **Friday's** (D-3) single-day "1st Role Verified" count (weekends are skipped)

**Header day reference:** Always "(last update yesterday)" regardless of day of week.

**Key clients and named locations** (all other locations aggregated as "Other Locations"):

| Client | Named Locations | Other Locations |
|--------|----------------|-----------------|
| **CORT** | Las Vegas, Chicago, Atlanta, Orlando, Phoenix, Austin, Nashville | All remaining grouped |
| **Stord, Inc** | Las Vegas, Reno, Atlanta, Erlanger | All shown individually |
| **OnTrac Final Mile** | Logan Township, Columbus, Middleburg Heights, Reno | All remaining grouped |
| **CTDI** | Dallas, Columbus, Nashville | All shown individually |

Named locations are sorted by Created count (descending). "Other Locations" always appears last.

### Section 2: Indeed Spend Comparison

**Data Source:** Indeed Analytics — `JobsCampaigns_YYYYMMDD_YYYYMMDD.csv`

Shows the **month-to-date (MTD) spend** on Indeed Ads for the current calendar month (sum of "Spend" column).

Includes a delta comparison vs the **last report generated**: `(+$X,XXX.XX since last report)`.

### Section 3: Open Campaigns

**Data Source:** FHS — Requisition report (`requisitions-YYYY-MM-DD-NNNNNN.csv`)

List of all campaigns with status **"Open"** in the Requisition report, organized by **client → locations**.

**Filter rules:**
- **Include:** Only requisitions with status = "Open"
- **Exclude:** Any client name containing "Indeed Flex" — only direct client requisitions are shown
- **Normalize:** Fix trailing spaces and inconsistent comma spacing in location names
- **Deduplicate:** Remove duplicate locations per client
- **Sort:** Clients alphabetically, locations alphabetically within each client

## Slack Formatting Rules

- Use `*text*` (single asterisks) for **bold** — Slack format, NOT markdown `**text**`
- **No blank line** between client name and first location row
- **One blank line** between client blocks
- Client names are bold: `*CORT:*`
- Section headers are bold: `*Indeed Spend Comparison:*`, `*Open Campaigns (Status: Open Only)*`

## Output Template (Slack-ready)

```
@here EOD RM Update Key client unique accounts: (last update yesterday)

*{Client}:*
{Location}: {Created} Created → {Verified} Verified (+{N})
{Location}: {Created} Created → {Verified} Verified (+{N})
Other Locations: {Created} Created → {Verified} Verified (+{N})

*{Client}:*
{Location}: {Created} Created → {Verified} Verified (+{N})
...


*Indeed Spend Comparison:* Indeed {Month} so far: ${MTD} (+${delta} since last report)

*Open Campaigns (Status: Open Only)*

{Client}: {Location 1}; {Location 2}; {Location 3}
{Client}: {Location 1}; {Location 2}
...
```

## Sample Report (March 17, 2026 — Tuesday)

```
@here EOD RM Update Key client unique accounts: (last update yesterday)

*CORT:*
Las Vegas: 413 Created → 242 Verified (+3)
Chicago: 320 Created → 174 Verified (+8)
Atlanta: 158 Created → 105 Verified (+4)
Orlando: 121 Created → 76 Verified (+6)
Phoenix: 115 Created → 78 Verified (+0)
Austin: 95 Created → 63 Verified (+1)
Nashville: 100 Created → 53 Verified (+2)
Other Locations: 169 Created → 69 Verified (+10)

*Stord, Inc:*
Las Vegas: 298 Created → 192 Verified (+8)
Reno: 188 Created → 126 Verified (+6)
Atlanta: 120 Created → 67 Verified (+7)
Erlanger: 97 Created → 65 Verified (+0)

*OnTrac Final Mile:*
Logan Township: 165 Created → 101 Verified (+3)
Columbus: 95 Created → 77 Verified (+1)
Middleburg Heights: 49 Created → 29 Verified (+0)
Reno: 12 Created → 11 Verified (+1)
Other Locations: 260 Created → 165 Verified (+3)

*CTDI:*
Dallas: 146 Created → 65 Verified (+2)
Columbus: 40 Created → 17 Verified (+5)
Nashville: 2 Created → 2 Verified (+0)


*Indeed Spend Comparison:* Indeed March so far: $51,154.98 (+$6,481.55 since last report)

*Open Campaigns (Status: Open Only)*

Bon Appetit Management Company, Inc: Chicago, IL
CORT: Atlanta, GA; Austin, TX; Charlotte, NC; Chicago, IL; Houston, TX; Las Vegas, NV; Nashville, TN; Orlando, FL; Washington, DC, WA
Continental Battery Systems, Inc.: Reno, NV
CTDI: Flower Mound, TX; Grove City, OH; Haslet, TX
Culinaire: Dallas, TX
Foxconn: Fort Worth, TX
Legends Hospitality: Dallas, TX
Lettuce Entertain You Enterprises, Inc: Austin, TX
OnTrac Final Mile: Logan Township, NJ; Orlando, FL; South Brunswick, NJ
Power Stop: Bedford Park, IL
SXSW: Austin, TX
Soho House Austin: Austin, TX
Stord, Inc: Atlanta, GA; Hebron, KY; Las Vegas, NV; McCarran, NV; Reno, NV; Sparks, NV
Tennant Solutions: Cincinnati, OH
Vestals Catering: Austin, TX
```

## Key Observations

### The report reveals metrics NOT in the daily spreadsheet:
- **Unique accounts Created** — from Tableau OB funnel (not in FHS or Indeed data)
- **Verified count** — post-interview verification (beyond RSVPs)
- **Daily velocity (+N)** — daily incremental progress per client/market

### Current Pain Points (Automation Targets)

1. **Manual compilation from 3 systems** — FHS + Indeed Analytics + Tableau, compiled via Gemini AI
2. **No single dashboard** — Claudio must export from 3 tools and merge manually
3. **Daily repetitive task** — same format every day, different numbers
4. **No historical tracking** — report is ephemeral (posted in Slack, lost in history)
5. **No alerts** — if a market shows 0 velocity (+0) for days, no automatic flag

### What RM Team AI Should Automate

| Current Step | Automation |
|-------------|------------|
| Export Tableau OB funnel | Tableau API or direct data source |
| Export Indeed cost data | Indeed Analytics API |
| Export FHS requisition data | API pull from FHS |
| Combine in Gemini | Automated report generation |
| Format for Slack | Slack webhook with formatted message |
| Post to channel | Scheduled daily post (or on-demand) |

**Ideal state:** One-click (or zero-click scheduled) daily report, auto-posted to Slack, with alerts for anomalies (zero velocity, budget pacing issues, funnel drop-offs).

## Updated Conversion Funnel (with Tableau data)

```
Ad Impression → Click → Apply Start → Apply Complete → RSVP (AI Interview)
                                                            ↓
                                               Account Created (Tableau)
                                                            ↓
                                               Verified (role verified)
                                                            ↓
                                               Shift Booked (ACP)
```

**Three data sources map to the funnel:**
- **Indeed Analytics:** Impression → Click → Apply Start → Apply Complete
- **FHS:** RSVP (AI Interview) → Target RSVPs
- **Tableau OB Funnel:** Account Created → Verified

## Generation Prompt

The reusable prompt for generating this report is saved at: `src/data/eod-report-prompt.md`
