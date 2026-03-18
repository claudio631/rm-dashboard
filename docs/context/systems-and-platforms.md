# Indeed Flex — Systems & Platforms

> Source: Stakeholder interview — 2026-03-17

## Ad Platforms (by priority)

| # | Platform | Priority | Usage |
|---|----------|----------|-------|
| 1 | **Indeed** | Primary | Main recruitment advertising platform |
| 2 | **Google Ads** | High | Second most used — search, PMax, display |
| 3 | **Meta Ads** | High | Third most used — Facebook & Instagram |
| 4 | **TikTok Ads** | Medium | Video-first candidate acquisition |
| 5 | **Bing Ads** | Medium | Microsoft Advertising — incremental reach |
| 6 | **Craigslist** | Low | Local job postings by market |

## CRM & Communications

| System | Purpose | Channels |
|--------|---------|----------|
| **Braze** | Customer engagement platform | Email, SMS, Push notifications |

**Braze capabilities relevant to RM Team AI:**
- Candidate nurture sequences (email + SMS + push)
- Onboarding drip campaigns
- Re-engagement for dormant Flexers
- Segmentation by funnel stage
- Triggered messaging (download → no account, account → no interview, etc.)
- A/B testing on messaging

## App Analytics & Attribution

| System | Purpose |
|--------|---------|
| **AppsFlyer** | Mobile attribution & app analytics — tracks app installs, in-app events, and campaign attribution |

**AppsFlyer data relevant to RM Team AI:**
- Which ad channel/campaign drove each app download
- In-app event tracking (account created, interview started, interview completed, onboarded, first shift booked)
- Attribution window and model (first-touch, multi-touch)
- Deep linking from ads → app
- Fraud detection on install campaigns
- SKAN/Privacy-preserving attribution (iOS)

## Business Intelligence & Reporting

| System | Purpose |
|--------|---------|
| **Tableau** | Primary BI tool — business analytics and dashboards |
| **Redash** | Secondary dashboards — specific data views |

## Internal Systems

| System | Purpose |
|--------|---------|
| **ACP** | Demand processing & shift management (client-side) |
| **Indeed Flex App** | Worker-facing mobile app (candidate-side) |

## Complete System Map

```
ACQUISITION                    ENGAGEMENT              OPERATIONS
─────────────                  ──────────              ──────────
Indeed Ads ──┐                 Braze ──────→ Email     ACP ──→ Shift Management
Google Ads ──┤                        ├───→ SMS
Meta Ads ────┤                        └───→ Push
TikTok Ads ──┼──→ AppsFlyer ──→ Indeed Flex App ──→ Onboarding ──→ Shift Booking
Bing Ads ────┤    (attribution)   (account, interview,
Craigslist ──┘                     onboard, book)

ANALYTICS
─────────
Tableau ──→ Business dashboards
Redash ───→ Specific data views
AppsFlyer → Campaign attribution
```

## Data Flow for RM Team AI

```
Ad Platforms (spend, clicks, impressions)
    │
    ▼
AppsFlyer (app installs, attribution, in-app events)
    │
    ▼
Indeed Flex App (account, verify, AI interview, onboard, book shift)
    │
    ▼
ACP (shift data, client demand)
    │
    ▼
Tableau / Redash (reporting, dashboards)
    │
    ▼
Braze (re-engagement based on funnel stage)
```

**RM Team AI sits on top of this stack** — pulling from ad platforms + AppsFlyer for attribution, and potentially feeding Braze for smarter re-engagement triggers.

## Key Integration Points

| Integration | Data Direction | Priority |
|-------------|---------------|----------|
| Indeed Ads → RM Team AI | Pull spend, impressions, clicks, applies | P0 |
| Google Ads → RM Team AI | Pull campaign metrics | P0 |
| Meta Ads → RM Team AI | Pull campaign metrics | P0 |
| AppsFlyer → RM Team AI | Pull attribution data (install → events) | P0 |
| TikTok Ads → RM Team AI | Pull campaign metrics | P1 |
| Bing Ads → RM Team AI | Pull campaign metrics | P1 |
| Braze ← RM Team AI | Push segments, trigger campaigns | P1 |
| Tableau/Redash ← RM Team AI | Export/feed data | P2 |
| ACP → RM Team AI | Pull shift booking data for full-funnel | P2 |

## Platform Updates Needed

Based on this discovery, the squad and stories need updates:

1. **Add TikTok Ads** as a channel (missing from original squad)
2. **Replace generic "CRM/Email"** with Braze specifically
3. **Add AppsFlyer** as the attribution source (replaces GA4 assumption)
4. **Add Tableau/Redash** as existing BI (RM Team AI complements, doesn't replace)
5. **Primary CTA is app download** — not "apply on website" (changes conversion tracking fundamentally)
