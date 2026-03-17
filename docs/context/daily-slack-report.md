# Indeed Flex — Daily Slack Report (EOD RM Update)

> Source: Stakeholder interview + sample report — 2026-03-17
> This report is posted daily to a Slack channel by the Recruitment Marketing team.

## Report Overview

**Channel:** Slack (team channel, @here mention)
**Frequency:** Daily (end of day)
**Author:** Claudio (currently compiled manually using Gemini AI)
**Data Sources:** 3 separate systems, manually combined

| Source | Data Provided |
|--------|--------------|
| **FHS** | Requisition report (open campaigns, roles, clients) |
| **Indeed Analytics** | Campaign spend and cost metrics |
| **Tableau** | OB (Onboarding) funnel split report — unique accounts created vs verified |

## Report Structure

### Section 1: Key Client Unique Accounts

Organized by **client → location**, showing:
- **Created** = total unique accounts created (people who signed up)
- **Verified** = total accounts that completed verification (role verified)
- **(+N)** = daily delta (new verified since yesterday)

**Example format:**
```
CORT:
  Las Vegas: 405 Created → 240 Verified (+12)
  Chicago: 311 Created → 165 Verified (+7)
  Atlanta: 160 Created → 107 Verified (+4)
```

**Key metric:** Created → Verified conversion rate and daily velocity (+N)

### Section 2: Indeed Spend Comparison

Monthly spend-to-date on Indeed Ads.

**Example:** `Indeed March so far: $44,673.43`

### Section 3: Open Campaigns

List of all campaigns with status "Open", organized by **client → locations**.

Shows the current portfolio of active advertising across all markets.

## Sample Report (March 2026)

### Clients in Report (with market count)

| Client | Markets | Vertical |
|--------|---------|----------|
| **CORT** | 8 (LV, CHI, ATL, ORL, PHX, AUS, NSH, Other) | Industrial |
| **Stord** | 4 (LV, Reno, Erlanger, ATL) | Industrial |
| **OnTrac Final Mile** | 4 (Logan Twp, Columbus, Middleburg Hts, Reno, Other) | Logistics |
| **CTDI** | 3 (Dallas, Nashville, Columbus) | Electronics |

### Additional Active Clients (from Open Campaigns)

| Client | Markets | Vertical |
|--------|---------|----------|
| Bon Appetit Management | Chicago | Hospitality/Food |
| Continental Battery Systems | Reno | Industrial |
| Culinaire | Dallas | Hospitality/Food |
| Foxconn | Fort Worth | Industrial |
| Johnstone Supply | Lancaster, TX | Industrial |
| Legends Hospitality | Dallas | Hospitality/Events |
| Lettuce Entertain You | Austin | Hospitality/Food |
| Power Stop | Bedford Park, Hodgkins (IL) | Industrial |
| Ryerson | Carrolton, TX | Industrial |
| SXSW | Austin | Events |
| Soho House | Austin | Hospitality |
| Tennant Solutions | Cincinnati | Industrial |
| Vestals Catering | Austin | Hospitality/Food |
| BTX | Austin | Industrial |

**Total:** 18+ unique clients across 20+ markets (larger than initial clients list)

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

### What PPC Manager AI Should Automate

| Current Step | Automation |
|-------------|------------|
| Export FHS requisition data | API pull from FHS |
| Export Indeed cost data | Indeed Analytics API |
| Export Tableau OB funnel | Tableau API or direct data source |
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
