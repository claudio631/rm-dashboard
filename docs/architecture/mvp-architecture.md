# RM Team AI — MVP Architecture

> Version: 1.0 — 2026-03-17
> Architect: Aria (@architect)

## Executive Summary

RM Team AI MVP is an **AI-powered data analyst** that replaces the manual daily workflow of downloading reports from 3 systems, joining them in spreadsheets, and compiling a Slack report using Gemini. It also includes productivity tools for campaign management.

**Constraint:** Internal tools (FHS, ACP, Tableau) are behind Okta SSO with MFA, preventing browser automation. Data ingestion is file-upload based.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      DATA INGESTION                           │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │ FHS Export   │  │ Indeed Export │  │ Tableau OB Export  │   │
│  │ (Excel/CSV)  │  │ (Excel/CSV)  │  │ (Excel)           │   │
│  └──────┬──────┘  └──────┬───────┘  └────────┬──────────┘   │
│         │                │                     │              │
│         └────────────────┼─────────────────────┘              │
│                          ▼                                    │
│                 ┌────────────────┐                            │
│                 │  File Upload   │  Drag & drop or bulk       │
│                 │  + Parser      │  Recognizes file type      │
│                 └────────┬───────┘  auto-maps columns         │
│                          │                                    │
│  Optional future:        │                                    │
│  Google/Meta Ads API ────┘  (OAuth, no Okta dependency)       │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                    DATA LAYER                                 │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │  SQLite / Supabase (Postgres)                        │     │
│  │                                                       │     │
│  │  Tables:                                              │     │
│  │  ├── requisitions (from FHS: req_id, job_id, role,   │     │
│  │  │    client, location, zip, pay, rsvps, target,     │     │
│  │  │    status)                                         │     │
│  │  ├── campaigns (from Indeed: campaign, impressions,   │     │
│  │  │    clicks, ctr, applies, spend, cpc, cpa)         │     │
│  │  ├── funnel (from Tableau: client, location, date,   │     │
│  │  │    stage, count)                                   │     │
│  │  ├── incentives (bonus programs, payouts)             │     │
│  │  ├── uploads (file metadata, upload history)          │     │
│  │  └── reports (generated report snapshots)             │     │
│  └─────────────────────────────────────────────────────┘     │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                 INTELLIGENCE LAYER                             │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Data Join Engine                                     │    │
│  │  ├── Match requisitions ↔ campaigns (by Req ID,      │    │
│  │  │    campaign code, naming convention)                │    │
│  │  ├── Match campaigns ↔ funnel (by client + location)  │    │
│  │  └── Calculate derived metrics per row                 │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Analytics Engine                                     │    │
│  │  ├── Full 7-stage funnel: cost-per-stage              │    │
│  │  │    (cost-per-account, cost-per-verified,            │    │
│  │  │    cost-per-shift-completed)                        │    │
│  │  ├── Channel comparison & efficiency scoring           │    │
│  │  ├── Client × market performance matrix                │    │
│  │  ├── Budget pacing & utilization                       │    │
│  │  ├── Trend analysis (daily velocity, WoW, MoM)        │    │
│  │  └── Anomaly detection (Houston 3.2%, dummy expiry)   │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  AI Insights (Claude API)                             │    │
│  │  ├── Analyze data patterns and surface insights       │    │
│  │  ├── Generate natural language summaries               │    │
│  │  ├── Recommend budget reallocations                    │    │
│  │  ├── Identify underperforming campaigns                │    │
│  │  └── Generate the daily Slack report text              │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                    OUTPUT LAYER                                │
│                                                               │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │  Dashboard   │  │ Daily Slack  │  │ Export             │   │
│  │  (Next.js)   │  │ Report       │  │ (Excel, PDF)       │   │
│  │              │  │ (Webhook)    │  │                     │   │
│  │  - Funnel    │  │              │  │  Download reports   │   │
│  │  - By client │  │  Auto-post   │  │  in familiar        │   │
│  │  - By market │  │  or 1-click  │  │  formats             │   │
│  │  - Trends    │  │              │  │                     │   │
│  │  - Alerts    │  │              │  │                     │   │
│  └─────────────┘  └──────────────┘  └───────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Productivity Tools                                   │    │
│  │  ├── UTM Builder (port from squad script)             │    │
│  │  ├── Ad Copy Generator (template + AI)                │    │
│  │  ├── Keyword Expander (port from squad script)        │    │
│  │  ├── Audience Builder (templates from squad data)     │    │
│  │  └── Budget Pacer (port from squad script)            │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | Next.js 14+ (App Router) | Full-stack React, SSR, API routes |
| **Language** | TypeScript | Type safety across stack |
| **Styling** | Tailwind CSS + shadcn/ui | Fast UI development, consistent components |
| **Database** | SQLite (local dev) → Supabase (prod) | Start simple, scale when needed |
| **File Parsing** | Papa Parse (CSV) + SheetJS (Excel) | Browser-side parsing, no server dependency |
| **Charts** | Recharts or Tremor | Dashboard visualizations |
| **AI** | Claude API (Anthropic SDK) | Insight generation, report writing |
| **Notifications** | Slack Incoming Webhook | Daily report auto-posting |
| **Auth** | NextAuth.js (simple) | Team access control |
| **Deployment** | Vercel | Zero-config Next.js hosting |

---

## Data Flow (Daily Workflow)

### Current (60+ minutes manual)

```
1. Login to FHS (Okta) → download requisition export       [5 min]
2. Login to Indeed (Okta) → download campaign report        [5 min]
3. Login to Tableau (Okta) → download OB funnel             [5 min]
4. Open spreadsheet → paste/update daily tab                [15 min]
5. Calculate metrics (CPA, cost per RSVP, etc.)             [10 min]
6. Open Gemini → compile Slack report                       [10 min]
7. Format and post to Slack                                  [5 min]
8. Answer follow-up questions from team                      [10 min]
```

### With RM Team AI (5 minutes)

```
1. Download 3 files from FHS, Indeed, Tableau               [5 min]
2. Drop files into RM Team AI                            [30 sec]
3. System auto-parses, joins, analyzes                       [10 sec]
4. Review dashboard + AI insights                            [1 min]
5. Click "Post to Slack" → done                              [5 sec]
```

**Time saved: ~55 minutes/day × 2 people = ~110 minutes/day**

---

## File Parser Specifications

### FHS Export (requisitions)

**Expected columns:** `last_updated`, `requisition_id`, `job_id`, `job_title`, `agency`, `client`, `location`, `pay_rate_min`, `pay_rate_max`, `pay_type`, `rsvps`, `target_rsvps`, `status`

**Rows:** ~15,000+ (all requisitions)

**Key fields for matching:** `requisition_id` (joins to daily tracking Req ID)

### Indeed Export (campaign metrics)

**Expected columns:** `Campaign`, `Impressions`, `Clickthrough rate (CTR)`, `Clicks`, `Apply start rate (ASR)`, `Apply starts`, `Apply completion rate (ACR)`, `Applies`, `Apply rate (AR)`, `Spend`, `Cost per click (CPC)`, `Cost per apply start (CPAS)`, `Cost per apply (CPA)`, `Job Count`, `Avg clicks per job`, `Avg apply starts per job`, `Avg applies per job`, `Avg spend per job`

**Rows:** ~2,000+ campaigns

**Key fields for matching:** `Campaign` name → parse client, role, market from naming convention

### Tableau OB Funnel Export

**Expected columns:** `Slice by.. 1` (client), `Slice by.. 2` (location), stage name column, date columns (daily or monthly), `Grand Total`

**Stages:** Worker Accounts Created, 1st Role Verified, 1st OB Task Completed, Platform Verified, "Ready to Book" Estimate, 1st Shift Booked, 1st Shift Completed, + 7 conversion rate rows

**Rows:** ~500 (daily) or ~3,500 (annual, 147 clients)

**Key fields for matching:** Client name + Location → join with campaigns

---

## Join Logic

The critical data engineering challenge: matching data across 3 systems that don't share IDs.

### Primary Join: FHS ↔ Indeed

```
FHS.requisition_id ↔ Daily Tracking.Req ID
Daily Tracking.Campaign Name ↔ Indeed.Campaign
```

**Campaign naming convention parsing:**
```
"US-B2C-Industrial-Cort-LC-Las Vegas, NV- March 03"
  │      │          │    │   │              │
  country vertical  client role market      date
```

### Secondary Join: Indeed ↔ Tableau Funnel

```
Parse Indeed.Campaign → extract client + market
Match to Tableau.client + Tableau.location
```

### Fuzzy Matching Required

Client names vary across systems:
- FHS: "Indeed Flex Applications"
- Indeed: "US-B2C-Industrial-Cort-LC-Las Vegas"
- Tableau: "CORT"

**Solution:** Client name normalization map (configurable, stored in DB)

---

## MVP Features (Prioritized)

### P0 — Core (Must Have)

1. **File Upload & Auto-Parse** — Drop FHS, Indeed, Tableau exports
2. **Data Join Engine** — Auto-match requisitions ↔ campaigns ↔ funnel
3. **Funnel Dashboard** — 7-stage funnel by client × market
4. **Cost Analysis** — Cost per RSVP, cost per verified, cost per shift completed
5. **Daily Slack Report** — One-click generation matching current format
6. **Client Name Mapping** — Configurable normalization across systems

### P1 — Important (Should Have)

7. **Trend Analysis** — Daily velocity, WoW comparison, historical charts
8. **Channel Comparison** — Performance across Indeed, Google, Meta, etc.
9. **Budget Pacing** — Spend tracking vs allocation
10. **Anomaly Alerts** — Flag zero-velocity markets, underperformers
11. **UTM Builder** — Port from squad script
12. **Ad Copy Generator** — Template + AI-powered variants

### P2 — Nice to Have

13. **Keyword Expander** — Port from squad script
14. **Audience Builder** — Templates from squad data
15. **Incentive Tracker** — Bonus spend alongside ad spend
16. **Export** — PDF/Excel reports for stakeholders
17. **Historical Data** — Store uploads for trend analysis over months

---

## Revised Epic Structure

### Epic 1: Foundation + Data Ingestion (replaces original Epic 1)

| Story | Title | Description |
|-------|-------|-------------|
| 1.1 | Project Foundation | Next.js + TypeScript + Tailwind + shadcn/ui |
| 1.2 | File Upload System | Drag-and-drop upload with file type detection |
| 1.3 | FHS Parser | Parse FHS Excel export into requisitions table |
| 1.4 | Indeed Parser | Parse Indeed campaign export into campaigns table |
| 1.5 | Tableau Parser | Parse OB Funnel export into funnel table |
| 1.6 | Client Name Mapping | Configurable name normalization across sources |
| 1.7 | Data Join Engine | Match requisitions ↔ campaigns ↔ funnel data |

### Epic 2: Analytics + Dashboard (replaces original Epics 4-5)

| Story | Title | Description |
|-------|-------|-------------|
| 2.1 | Funnel Dashboard | 7-stage funnel visualization by client × market |
| 2.2 | Cost-per-Stage Analysis | CPA, cost per RSVP, cost per verified, cost per completed |
| 2.3 | Client Performance View | Matrix of all clients with key metrics |
| 2.4 | Market Performance View | Matrix of all markets with key metrics |
| 2.5 | AI Insights Engine | Claude API integration for pattern analysis |
| 2.6 | Daily Slack Report | Auto-generate + post matching current format |

### Epic 3: Productivity Tools (original Epic 2)

| Story | Title | Description |
|-------|-------|-------------|
| 3.1 | UTM Builder | Port from squad, full UI |
| 3.2 | Ad Copy Generator | Template + AI variants |
| 3.3 | Keyword Expander | Port from squad, full UI |
| 3.4 | Budget Pacer | Port from squad + dashboard widget |
| 3.5 | Audience Builder | Templates + custom builder |

---

## Security

- **Auth:** NextAuth.js with email/password (team of 3-5 users)
- **Data:** All uploaded files processed server-side, not stored permanently unless opted in
- **Credentials:** No Indeed Flex internal system credentials stored (Okta blocks automation anyway)
- **API Keys:** Claude API key + Slack webhook token in environment variables
- **Deployment:** Vercel with environment variable encryption

---

## Future Enhancements (Post-MVP)

1. **Google Ads API** — Direct integration (OAuth, no Okta dependency)
2. **Meta Ads API** — Direct integration (OAuth)
3. **AppsFlyer API** — Attribution data for per-campaign funnel analysis
4. **Braze API** — Trigger re-engagement campaigns from anomaly alerts
5. **Scheduled Reports** — Cron-based daily Slack posting (no manual trigger)
6. **Multi-user** — Role-based access for Craig, Megan, Olivia
7. **Historical Trending** — Months of stored data for long-term analysis
