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
| 2026-03-18 | 0.3 | Added: Google Ads KB (12 guides), Reddit Ads KB, hiring events data, data insights capability, 2025 benchmarks by market/client, squad expansion (7 agents, 72 files), 5S data reorganization, new FRs (FR19-FR24), new Epic 4 (Channel Intelligence), updated reference docs | Pax (PO) |

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

### Ad Channels (by priority and budget share)

| # | Channel | Budget Share | CPC (Median) | CPA (Median) | Status |
|---|---------|:-----------:|:------------:|:------------:|--------|
| 1 | **Indeed Ads** | 30-40% | $0.50 | $15 | Primary — sponsored jobs via FHS |
| 2 | **Google Ads** | 20-30% | $2.50 | $35 | Active — Search, PMax, Display, YouTube |
| 3 | **Meta Ads** | 15-20% | $1.50 | $20 | Active — Facebook, Instagram lead gen |
| 4 | **Bing Ads** | 5-10% | $1.80 | $30 | Active — incremental reach |
| 5 | **Reddit Ads** | 3-5% | $1.00 | N/A | Active — community-driven recruitment |
| 6 | **Craigslist** | 2-5% | N/A | $10-75/post | Active — local job postings |
| 7 | **Programmatic** | 0-10% | $0.40 | $12 | Optional — Appcast, Joveo, PandoLogic |

*Source: `squads/recruitment-marketing-flex/data/benchmarks/industry-benchmarks.yaml`*

### Market Performance Tiers (2025 Baseline)

| Tier | Markets | Account → 1st Shift CR% |
|------|---------|:----------------------:|
| Elite | Columbus, Reno | 23.5-23.7% |
| Strong | Cincinnati, Phoenix, Nashville, Fort Mill, Chicago | 16.3-18.3% |
| On Target | Atlanta | 15.1% |
| Below Average | Las Vegas, Charlotte, Dallas, Austin, Middleburg Hts, Orlando | 9.7-12.7% |
| Critical | Houston | 3.2% |

*Source: `docs/context/2025-conversion-rate-benchmarks.md`*

### Key Data Insights (March 2026 Analysis)

1. **Biggest funnel leak:** 44% of accounts never complete AI interview (23,294 people lost in 2025)
2. **Landing page gap:** 12 high-volume roles (21,355 shifts/year) land on generic LP instead of role-specific pages
3. **Market spread:** 7.4x difference between best (Columbus 23.7%) and worst (Houston 3.2%) markets
4. **Google Ads under-leveraged:** Has 20-30% budget share but offers AI Max (+14% conversions), PMax (+18% incremental), and remarketing capabilities not available on Indeed
5. **Unfilled shifts:** 825 real unfilled per week (65% fill rate), Warehouse Operative = 52% of all gaps
6. **Hiring events:** 48% show rate, 96% DT pass rate — high-intent channel for pre-qualified candidates
7. **Seasonality:** Q1 has 0.9x cost modifier (cheapest quarter to buy traffic)

*Source: `squads/recruitment-marketing-flex/data/insights/top-funnel-levers-2026-03.md`*

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

### Channel Intelligence & Knowledge Base (v0.3)

- **FR19:** The system shall provide channel-specific knowledge bases (Google Ads, Reddit Ads, and future channels) accessible to AI agents for context-aware campaign recommendations
- **FR20:** The system shall surface market-level performance insights comparing conversion rates across the 21 markets with tier classification (Elite/Strong/On Target/Below Average/Critical)
- **FR21:** The system shall track hiring event performance (invites, show rate, DT pass rate, time slot analysis) and integrate event costs into the unified cost-per-hire calculation
- **FR22:** The system shall display a weekly unfilled shifts analysis showing persistent gaps by venue, role, and shift time — with recommended actions (re-engagement vs. more ad spend)
- **FR23:** The system shall provide data-driven budget reallocation recommendations based on market-level conversion rates and unfilled shift demand signals
- **FR24:** The system shall track incentive program costs ($28,725/month Dec 2025 example) alongside ad spend for true cost-per-hire calculations including bonus payouts

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

### Epic 4: Channel Intelligence & Market Optimization (v0.3)
**Goal:** Provide channel-specific knowledge bases, market performance benchmarking, hiring event tracking, and demand-aware budget recommendations.
**FRs:** FR19, FR20, FR21, FR22, FR23, FR24
**NFRs:** NFR1, NFR5, NFR6

**Stories:**
| # | Title | Description |
|---|-------|-------------|
| 4.1 | Channel Knowledge Base System | Searchable KB per channel (Google Ads: 12 guides, Reddit: playbook) with agent-accessible context |
| 4.2 | Market Performance Dashboard | 21-market tier view, CR% benchmarks, year-over-year trends, budget reallocation suggestions |
| 4.3 | Hiring Event Tracker | Invite/show/pass tracking, time slot analysis, cost-per-cleared-worker, show-rate optimization |
| 4.4 | Unfilled Shifts Intelligence | Weekly gap analysis by venue/role/shift, persistent vs. one-off classification, re-engagement vs. ad spend recommendations |
| 4.5 | Budget Reallocation Engine | Demand-signal-driven budget suggestions factoring market CR%, unfilled shifts, seasonality, and incentive costs |

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

| # | Enhancement | Trigger | Priority |
|---|-------------|---------|----------|
| 1 | Google Ads API integration | OAuth available outside Okta | High |
| 2 | Meta Ads API integration | OAuth available outside Okta | High |
| 3 | AppsFlyer API for per-campaign attribution | API key access obtained | High |
| 4 | Braze integration for re-engagement triggers | API access obtained | High — 44% funnel leak at verification |
| 5 | Dedicated LPs for 12 high-volume roles | UX team availability | High — 21K shifts/year on generic LP |
| 6 | Keyword expander tool | Team requests it | Medium |
| 7 | Audience builder tool | Team requests it | Medium |
| 8 | Budget pacer with alerts | After sufficient historical data | Medium |
| 9 | Scheduled cron-based Slack report | After stable daily usage | Medium |
| 10 | Meta Ads / Bing Ads / TikTok knowledge bases | Channel expansion | Medium |
| 11 | Incentive program tracker | Volume warrants dedicated view | Medium — $28K+/month |
| 12 | Spanish-language ad copy variants | Hispanic market expansion | Low |
| 13 | Hiring event walk-in acquisition (Google Local/Meta Events) | Event program scales | Low |

---

## Squad Capabilities (v0.3)

The recruitment-marketing-flex squad provides an AI agent team with 72 files organized across 7 specialist agents:

| Agent | Persona | Focus |
|-------|---------|-------|
| @ppc-paid-media-specialist | Pixel | Google Ads, Indeed Ads, Bing, campaign management |
| @seo-content-strategist | Atlas | SEO, job posting optimization, content |
| @crm-email-specialist | Relay | Braze campaigns, email/SMS/push sequences |
| @analytics-performance-lead | Metric | Reporting, KPIs, dashboards |
| @ai-automation-specialist | Auto | Workflow automation, AI integrations |
| @funnel-specialist | Flow | Onboarding funnel optimization, conversion |
| @data-scientist | Nova | Statistical analysis, insights, A/B test design |

### Channel Knowledge Bases

| Channel | Files | Coverage |
|---------|:-----:|----------|
| Google Ads | 12 | Campaign types, keywords, ad copy, PMax, YouTube, Display, budget, conversions, AI automation, mobile, lead gen |
| Reddit Ads | 1 | Full playbook — formats, targeting, creative, bidding, measurement |
| *Meta Ads* | — | *Planned* |
| *Indeed Ads* | — | *Planned* |

### Operational Playbooks

| Playbook | Location | Contents |
|----------|----------|----------|
| Hiring Events | `data/hiring-events/` | Master playbook, Las Vegas post-mortem, ideas backlog |
| Top-Funnel Insights | `data/insights/` | 8 actionable levers with estimated impact |
| Industry Benchmarks | `data/benchmarks/` | CPC/CPA/CTR by 7 channels + seasonal adjustments |
| Audience Targeting | `data/targeting/` | 10 audience segments + 7 channel configs |

### Task Library (Google Ads)

| Task | Workflow |
|------|----------|
| Campaign Setup | End-to-end campaign creation (8 steps) |
| Keyword Research | Discovery, match types, ad group structure |
| Ad Copy Creation | Headlines, descriptions, extensions, A/B plan |
| Performance Analysis | 10-step analysis with recommendations |
| Weekly Optimization | 8-step recurring optimization cycle (~2 hrs/week) |

## Sections Pending

- [ ] User Interface Design Goals (delegate to @ux-design-expert)
- [ ] Detailed acceptance criteria per epic (in story files)
- [ ] Meta Ads knowledge base (delegate to @ppc-paid-media-specialist)
- [ ] Indeed Ads knowledge base (delegate to @ppc-paid-media-specialist)

---

## Reference Documents

### Core Context
| Document | Location |
|----------|----------|
| MVP Architecture | `docs/architecture/mvp-architecture.md` |
| Business Operations | `docs/context/business-operations.md` |
| Systems & Platforms | `docs/context/systems-and-platforms.md` |
| Job Categories | `docs/context/job-categories.md` |
| Landing Pages | `docs/context/landing-pages.md` |
| AI Interview Questions (TACO) | `docs/context/ai-interview-questions-taco.md` |
| Job Templates | `docs/context/job-templates/` |

### Operational Data
| Document | Location |
|----------|----------|
| Daily Tracking Spreadsheet | `docs/context/daily-tracking-spreadsheet.md` |
| Daily Slack Report | `docs/context/daily-slack-report.md` |
| SOP: Indeed Ad Request | `docs/context/sop-indeed-ad-request.md` |
| OB Funnel Deep Dive | `docs/context/ob-funnel-deep-dive.md` |
| 2025 Conversion Rate Benchmarks | `docs/context/2025-conversion-rate-benchmarks.md` |
| Las Vegas Hiring Events (Mar 2026) | `docs/context/las-vegas-hiring-events-march-2026.md` |
| Weekly Unfilled Shifts Template | `docs/context/weekly-unfilled-shifts-report-template.md` |
| Incentive Programs | `docs/context/incentive-programs.md` |

### Squad Knowledge Bases (v0.3)
| Document | Location |
|----------|----------|
| Google Ads Knowledge Base (12 guides) | `squads/recruitment-marketing-flex/data/google-ads/` |
| Reddit Ads Playbook | `squads/recruitment-marketing-flex/data/reddit-ads/` |
| Hiring Events Playbook | `squads/recruitment-marketing-flex/data/hiring-events/` |
| Top-Funnel Levers Analysis | `squads/recruitment-marketing-flex/data/insights/` |
| Industry Benchmarks | `squads/recruitment-marketing-flex/data/benchmarks/` |
| Audience & Channel Config | `squads/recruitment-marketing-flex/data/targeting/` |
| Squad Manifest | `squads/recruitment-marketing-flex/squad.yaml` |

---
*RM Team AI PRD v0.3 — Pax (PO) — 2026-03-18*
