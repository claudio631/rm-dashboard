# Indeed Flex — Business Operations & Systems

> Source: Stakeholder interview — 2026-03-17

## Business Model

Indeed Flex is a **W-2 staffing agency** (not 1099/gig). All workers are hired as W-2 employees, which means full onboarding compliance is required before any shift work.

## Key Terminology

| Term | Definition |
|------|-----------|
| **Flexer** | An Indeed Flex worker (W-2 employee) who books shifts via the app |
| **ACP** | Indeed Flex's internal system that processes demand for workers and manages shift booking |
| **Shift** | A single work assignment at a client location, booked by a Flexer |

## Candidate-to-Flexer Journey

```
1. AWARENESS     → Candidate discovers Indeed Flex (ads, organic, referral)
2. DOWNLOAD      → Downloads the Indeed Flex app
3. ACCOUNT       → Creates account in the app
4. VERIFICATION  → Verified role / identity verification
5. INTERVIEW     → AI-conducted interview (reviewed by human recruiter after)
6. ONBOARDING    → W-2 compliance (all required before first shift):
                    - I-9 form (employment eligibility)
                    - Conditional offer letter
                    - Pay details
                    - Legal information / agreements
7. ACTIVE FLEXER → Can browse and book available shifts in the app
8. SHIFT BOOKING → Books shifts via the Indeed Flex app
9. WORKING       → Completes shifts at client locations
```

## Core Systems

| System | Purpose | Role |
|--------|---------|------|
| **Indeed Flex App** | Worker-facing mobile app | Download → Account → Onboarding → Shift booking |
| **ACP** | Demand processing & shift management | Processes client demand, manages shift availability, worker booking |

## Key Implications for PPC Manager AI

### Conversion Funnel (Marketing Perspective)

The marketing funnel is longer than typical job advertising because of the W-2 onboarding:

```
Ad Impression → Click → App Download → Account Created → Verified →
Interviewed → Onboarded (I-9, offer, pay, legal) → First Shift Booked
```

**This means:**
- **CPA (Cost-per-Apply)** is really **Cost-per-Download** or **Cost-per-Account**
- **True Cost-per-Hire** must track through the full onboarding funnel
- **Drop-off analysis** at each stage is critical (download → account → verify → interview → onboard → book)
- **Re-engagement campaigns** target people who dropped off at any stage (not just "didn't apply")

### Pay Rates
- Pay ranges vary by **client** and **location** (not fixed per job category)
- Ad copy and job postings need dynamic pay ranges per market/client combination

### Audience Strategy
- **Primary CTA:** Download the Indeed Flex app
- **Retargeting segments:** Downloaded but didn't create account, created account but didn't onboard, onboarded but never booked a shift
- **Re-engagement:** Flexers who haven't booked in 30+ days

## Questions to Resolve

- [ ] What analytics/reporting does ACP provide? Can we pull funnel data from it?
- [ ] Is there an API or data export from the Indeed Flex app (downloads, accounts, onboarding completion)?
- [ ] What CRM/email system sends communications to candidates during onboarding?
- [ ] What ad platforms are currently active and who manages them?
- [ ] What does the current reporting stack look like (spreadsheets, dashboards, BI tools)?
