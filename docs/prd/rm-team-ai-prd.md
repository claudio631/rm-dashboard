# RM Team AI — Product Requirements Document (PRD)

## Goals

- **G1:** Eliminate the daily manual workflow of downloading reports from FHS, Indeed Analytics, and Tableau, joining them in spreadsheets, and compiling the EOD Slack report with Gemini — reducing 60+ minutes/day to under 5 minutes
- **G2:** Provide a unified 7-stage onboarding funnel dashboard (Account Created → Role Verified → OB Task → Platform Verified → Ready to Book → 1st Shift Booked → 1st Shift Completed) with cost-per-stage analysis by client and market
- **G3:** Surface AI-driven insights that identify underperforming markets, anomalous conversion rates, and budget optimization opportunities across 147 clients and 21 markets
- **G4:** Provide recruitment marketing productivity tools (UTM builder, ad copy generator) that replace shared spreadsheets and enforce naming conventions
- **G5:** Create a historical data repository that enables trend analysis, month-over-month comparisons, and data-driven budget allocation decisions

## Background Context

Indeed Flex is a **W-2 staffing agency** that hires flexible workers (Flexers) across Industrial and Hospitality verticals. Unlike gig platforms, every worker must complete a full onboarding process: app download → account creation → AI interview (English or Spanish) → recruiter review → I-9 form → conditional offer → pay details → legal agreements → shift booking.

The Recruitment Marketing team (Claudio, Craig, Megan — US; Olivia — UK) manages advertising across **7 channels** (Indeed Ads, Google Ads, Meta Ads, TikTok Ads, Bing Ads, Craigslist, and referrals) for **147 clients** across **21 US markets**. In 2025, the team generated **52,987 worker accounts** resulting in **8,146 first shifts completed** (15.4% overall conversion).

**The core problem:** Campaign data lives in 3 separate systems — FHS (ATS with requisitions and RSVPs), Indeed Analytics (campaign spend and metrics), and Tableau (onboarding funnel by client × market). Every day, the team manually downloads Excel exports from each system, joins the data in a 41-column spreadsheet, calculates derived metrics, and compiles a Slack report using Gemini AI. This process takes 60+ minutes daily per specialist.

**Key constraint:** Internal tools (FHS, ACP, Tableau) are behind **Okta SSO with MFA**, preventing API or browser automation. The MVP uses **file upload** for data ingestion.

## Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2026-03-16 | 0.1 | Initial PRD draft — Goals, Requirements, Epic List | Morgan (PM) |
| 2026-03-17 | 0.2 | Major rewrite after context discovery — file-upload architecture, real funnel, real systems | Morgan (PM) |

---

## Indeed Flex Business Context

### Team

| Name | Role | Markets |
|------|------|---------|
| Claudio Santos | Recruitment Marketing Specialist | Austin, Houston, Washington DC, Charlotte, Fort Mill, Orlando, Phoenix, Reno, Las Vegas, Monroe |
| Craig Freeman | Recruitment Marketing Specialist | Columbus, Cincinnati, Hebron, Chicago, Atlanta, Dallas, Logan Township, NJ cluster, North Haven |
| Megan Georgevich | Recruitment Marketing Specialist | US markets (shared) |
| Olivia Smith | Recruitment Marketing Manager | UK |

### Systems Landscape

| System | Purpose | Access |
|--------|---------|--------|
| **FHS** | ATS — requisitions, job postings, RSVP tracking | Okta SSO (file export only) |
| **ACP** | Shift management, dummy shift creation, worker booking | Okta SSO |
| **Indeed Flex App** | Worker-facing mobile app (download → onboard → book shifts) | Public |
| **Indeed Employer** | Campaign creation, budget management, ad performance | Okta SSO (file export only) |
| **Braze** | CRM — email, SMS, push notifications to candidates | Okta SSO |
| **AppsFlyer** | Mobile attribution — app installs, in-app events, campaign attribution | Separate login |
| **Tableau** | BI dashboards — OB funnel viewer, custom reports | Okta SSO (file export only) |
| **Redash** | Secondary dashboards — specific data views | Separate login |
| **Monday.com** | Recruitment request intake from hiring managers | Slack notification |

### Onboarding Funnel (7 Stages)

```
1. Worker Accounts Created     52,987 (2025)  100.0%
2. 1st Role Verified           29,693          56.0%  ← AI interview completed
3. 1st OB Task Completed       27,614          52.1%  ← Started I-9/compliance
4. Platform Verified           19,091          36.0%  ← Fully compliant
5. "Ready to Book" Estimate    15,224          28.7%  ← Eligible for shifts
6. 1st Shift Booked             9,628          18.2%  ← Booked first shift
7. 1st Shift Completed          8,146          15.4%  ← Worked first shift
```

### Top Clients (2025 by volume)

| Client | Accounts | Completed | CR% | Vertical |
|--------|----------|-----------|-----|----------|
| OnTrac Final Mile | 31,561 | 4,924 | 15.6% | Industrial/Logistics |
| Stord, Inc | 5,333 | 647 | 12.1% | Industrial/Warehouse |
| CORT | 1,946 | 369 | 19.0% | Industrial/Furniture |
| CTDI | 1,466 | 206 | 14.1% | Electronics |
| Tennant Solutions | 1,130 | 229 | 20.3% | Industrial |
| Assurant (Hyla) | 1,023 | 397 | 38.8% | Industrial |

### Top Markets (2025 by volume)

| Market | Accounts | Completed | CR% |
|--------|----------|-----------|-----|
| Atlanta | 7,766 | 1,169 | 15.1% |
| Dallas | 6,773 | 732 | 10.8% |
| Chicago | 6,763 | 1,102 | 16.3% |
| Columbus | 5,855 | 1,385 | 23.7% |
| Nashville | 4,646 | 841 | 18.1% |
| Cincinnati | 4,179 | 763 | 18.3% |

### Ad Channels (by priority)

1. **Indeed Ads** — Primary (sponsored jobs via FHS)
2. **Google Ads** — Second most used (search, PMax)
3. **Meta Ads** — Third (Facebook, Instagram)
4. **TikTok Ads** — Video-first candidate acquisition
5. **Bing Ads** — Incremental reach
6. **Craigslist** — Local job postings
7. **Referrals** — Worker referral programs

---

## Functional Requirements

### Data Ingestion (File Upload)

- **FR1:** The system shall accept drag-and-drop file uploads of Excel (.xlsx) and CSV (.csv) exports from FHS, Indeed Analytics, and Tableau OB Funnel
- **FR2:** The system shall auto-detect file type based on column headers (FHS: `requisition_id`, `rsvps`; Indeed: `Campaign`, `Spend`; Tableau: `Slice by.. 1`, funnel stage names)
- **FR3:** The system shall parse and store uploaded data in a structured database with upload history and metadata tracking

### Data Join & Matching

- **FR4:** The system shall automatically join FHS requisitions with Indeed campaigns using Req ID, campaign code, or campaign naming convention parsing
- **FR5:** The system shall join campaign data with Tableau funnel data by normalized client name + location
- **FR6:** The system shall provide a configurable client name mapping to normalize naming variations across systems (e.g., "CORT" in Tableau = "Cort" in Indeed campaign names = "Indeed Flex Applications" in FHS)
- **FR7:** The system shall report match rates after each upload, showing matched vs unmatched rows with fuzzy match suggestions

### Analytics & Dashboard

- **FR8:** The system shall display a 7-stage onboarding funnel visualization (Account Created through 1st Shift Completed) filterable by client, market, and date range
- **FR9:** The system shall calculate cost-per-stage metrics: cost-per-account, cost-per-RSVP (AI interview), cost-per-verified, cost-per-shift-completed — broken down by client and market
- **FR10:** The system shall include incentive bonus costs in total cost-per-hire calculations when incentive data is uploaded
- **FR11:** The system shall display client performance and market performance comparison tables with sortable columns and color-coded conversion rates
- **FR12:** The system shall generate AI-powered insights (via Claude API) identifying top/bottom performers, anomalies, trends, and budget recommendations

### Daily Slack Report

- **FR13:** The system shall generate a daily EOD Slack report matching the current format: key client unique accounts (client → location → Created → Verified (+N daily delta)), Indeed spend month-to-date, and open campaigns list
- **FR14:** The system shall calculate daily deltas (+N) by comparing current upload data to the previous upload
- **FR15:** The system shall support one-click "Post to Slack" via Slack Incoming Webhook, with editable preview before posting

### Productivity Tools

- **FR16:** The system shall provide a UTM builder that generates tracking parameters following the Indeed Flex naming convention (`{country}-B2C-{vertical}-{client}-{role}-{market}`) with pre-populated channel and role dropdowns
- **FR17:** The system shall provide an AI-assisted ad copy generator that produces channel-specific recruitment ad variants (Indeed, Google, Meta, TikTok, Bing) respecting character limits, with cobranding toggle for client name inclusion
- **FR18:** The system shall auto-select the correct landing page URL per role from the published landing page registry (24 published role-specific LPs)

## Non-Functional Requirements

- **NFR1:** The dashboard shall load within 3 seconds for datasets up to 15,000 FHS rows + 2,000 Indeed campaigns + 3,500 Tableau funnel rows
- **NFR2:** File parsing shall complete within 10 seconds for the largest expected file (FHS at 15,934 rows)
- **NFR3:** The system shall support 3-5 concurrent users (the US RM team)
- **NFR4:** All API keys (Claude, Slack webhook) shall be stored as environment variables, never in client-side code
- **NFR5:** The platform shall be accessible via web browser (responsive) on desktop and tablet
- **NFR6:** Uploaded data shall be retained for a minimum of 12 months to enable historical trend analysis
- **NFR7:** The system shall handle partial uploads gracefully (e.g., FHS + Tableau uploaded but Indeed not yet available)

---

## Epic List (MVP — 3 Epics)

### Epic 1: Foundation + Data Ingestion
**Goal:** Build the project foundation and enable file upload, parsing, and data joining from FHS, Indeed, and Tableau exports.
**FRs:** FR1, FR2, FR3, FR4, FR5, FR6, FR7
**NFRs:** NFR1, NFR2, NFR4

**Stories:**
| # | Title | Description |
|---|-------|-------------|
| 1.1 | Project Foundation | Next.js + TypeScript + Tailwind + shadcn/ui + SQLite |
| 1.2 | File Upload System | Drag-drop with auto-detect, FHS/Indeed/Tableau parsers |
| 1.3 | Client Name Mapping & Data Join | Normalization config, campaign name parser, join engine |

### Epic 2: Analytics + Dashboard + Slack Report
**Goal:** Provide a 7-stage funnel dashboard with cost-per-stage analysis, AI insights, and automated daily Slack report generation.
**FRs:** FR8, FR9, FR10, FR11, FR12, FR13, FR14, FR15
**NFRs:** NFR1, NFR5, NFR6, NFR7

**Stories:**
| # | Title | Description |
|---|-------|-------------|
| 2.1 | Funnel Dashboard | 7-stage funnel by client × market with filters and performance tables |
| 2.2 | Cost-Per-Stage Analysis | Cost per RSVP, per verified, per completed — includes incentive costs |
| 2.3 | AI Insights Engine | Claude API for pattern analysis, anomaly detection, recommendations |
| 2.4 | Daily Slack Report Generator | One-click report matching current format with Slack webhook posting |

### Epic 3: Productivity Tools
**Goal:** Provide campaign management tools that replace shared spreadsheets and enforce naming conventions.
**FRs:** FR16, FR17, FR18
**NFRs:** NFR5

**Stories:**
| # | Title | Description |
|---|-------|-------------|
| 3.1 | UTM Builder | Pre-populated channels/roles, naming convention enforcement, batch mode |
| 3.2 | Ad Copy Generator | Template + AI variants for all 7 channels, cobranding, character limits |

---

## Key Metrics (Success Criteria)

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Daily report compilation time | 60+ min | <5 min | Time from file download to Slack post |
| Data sources manually joined | 3 spreadsheets | 0 (auto-joined) | File upload → dashboard |
| Funnel visibility | Per-client only (Tableau) | Client × market × channel | Dashboard filters |
| Cost-per-stage analysis | Manual calculation | Automated, real-time | Dashboard metrics |
| Historical data | 1 month (spreadsheet tabs) | 12+ months | Database retention |

---

## Technical Assumptions

- **Framework:** Next.js 14+ with App Router, TypeScript, Tailwind CSS, shadcn/ui
- **Database:** SQLite (local dev) → Supabase Postgres (production)
- **File Parsing:** SheetJS (xlsx) for Excel, Papa Parse for CSV — client-side
- **AI:** Claude API via Anthropic SDK for insights and ad copy generation
- **Notifications:** Slack Incoming Webhook for daily report posting
- **Deployment:** Vercel
- **No API integrations in MVP** — all data ingestion via file upload (Okta SSO constraint)

---

## Future Enhancements (Post-MVP)

| # | Enhancement | Trigger |
|---|-------------|---------|
| 1 | Google Ads API integration | OAuth available outside Okta |
| 2 | Meta Ads API integration | OAuth available outside Okta |
| 3 | AppsFlyer API for per-campaign attribution | API key access obtained |
| 4 | Braze integration for re-engagement triggers | API access obtained |
| 5 | Keyword expander tool | Team requests it |
| 6 | Audience builder tool | Team requests it |
| 7 | Budget pacer with alerts | After sufficient historical data |
| 8 | Scheduled cron-based Slack report | After stable daily usage |
| 9 | Incentive program tracker | Volume warrants dedicated view |
| 10 | Spanish-language ad copy variants | Hispanic market expansion |

---

## Sections Pending

- [ ] User Interface Design Goals (delegate to @ux-design-expert)
- [ ] Detailed acceptance criteria per epic (in story files)

---

## Reference Documents

| Document | Location |
|----------|----------|
| MVP Architecture | `docs/architecture/mvp-architecture.md` |
| Clients & Markets | `docs/context/clients-and-markets.md` |
| Business Operations | `docs/context/business-operations.md` |
| Job Categories | `docs/context/job-categories.md` |
| Systems & Platforms | `docs/context/systems-and-platforms.md` |
| SOP: Indeed Ad Request | `docs/context/sop-indeed-ad-request.md` |
| Daily Tracking Spreadsheet | `docs/context/daily-tracking-spreadsheet.md` |
| Daily Slack Report | `docs/context/daily-slack-report.md` |
| OB Funnel Deep Dive | `docs/context/ob-funnel-deep-dive.md` |
| Incentive Programs | `docs/context/incentive-programs.md` |
| Landing Pages | `docs/context/landing-pages.md` |
| AI Interview Questions (TACO) | `docs/context/ai-interview-questions-taco.md` |
| Job Templates | `docs/context/job-templates/` |

---
*RM Team AI PRD v0.2 — Morgan (PM) — 2026-03-17*
