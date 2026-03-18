# Google Ads Pre-Launch Verification Checklist

> Source: Google Ads Knowledge Base (conversion-tracking-guide.md, mobile-optimization-guide.md, ad-copywriting-playbook.md)
> Use: **MANDATORY gate before activating any Google Ads campaign spend**
> This checklist enforces verification steps that the setup checklist mentions but doesn't block on.

## When to Use

Run this checklist:
- Before launching ANY new Google Ads campaign
- After changing landing pages on existing campaigns
- After adding new conversion actions
- Monthly as a health check on active campaigns

**BLOCKING:** Do not activate campaign spend until all P0 items pass.

---

## P0 — Conversion Tracking (MUST PASS)

> Without these, every dollar spent is unmeasurable.

- [ ] **Google Tag installed on landing page** — verify with [Google Tag Assistant](https://tagassistant.google.com/)
  - Open the landing page URL in Tag Assistant
  - Confirm gtag.js or GTM container fires
  - If NOT firing: escalate to web team before proceeding
- [ ] **Primary conversion action exists** in Google Ads → Goals → Conversions
  - Name: "Application Submitted" (or equivalent)
  - Category: Submit Lead Form
  - Value: assigned ($20-50 for recruitment)
  - Count: One (per click)
- [ ] **Conversion fires on thank-you/confirmation page**
  - Submit a test application through the full flow
  - Verify conversion appears in Google Ads → Conversions (may take up to 24hrs)
  - Alternative: check Tag Assistant real-time for conversion event
- [ ] **Enhanced Conversions enabled**
  - Google Ads → Goals → Settings → Enhanced Conversions: ON
  - Hashes email/phone for better attribution
  - Critical for iOS/cookie-limited environments
- [ ] **Auto-tagging enabled**
  - Google Ads → Settings → Account Settings → Auto-tagging: ON
  - Required for accurate GA4 ↔ Google Ads data flow
- [ ] **Google Analytics 4 linked**
  - Google Ads → Linked accounts → Google Analytics: connected
  - GA4 property shows Google Ads as traffic source

### P0 Verdict
```
All 6 items pass → PROCEED to P1
Any item fails → STOP. Fix before spending.
```

---

## P1 — Landing Page Quality (MUST PASS)

> A slow or mismatched landing page wastes clicks.

- [ ] **Mobile PageSpeed score ≥ 70**
  - Test: `https://pagespeed.web.dev/analysis?url={LANDING_PAGE_URL}`
  - Record score: ____
  - If < 70: flag to web team, document in campaign notes
- [ ] **Core Web Vitals passing**
  - LCP (Largest Contentful Paint): < 2.5 seconds
  - FID (First Input Delay): < 100ms
  - CLS (Cumulative Layout Shift): < 0.1
- [ ] **Landing page headline matches ad promise**
  - If ad says "Banquet Servers — $18-$25/hr — Dallas" → LP headline must mention banquet servers, pay, and Dallas
  - No generic "Find Jobs" pages for role-specific ads
- [ ] **Application form is mobile-friendly**
  - Test on actual mobile device (not just browser resize)
  - Form fields: max 3-5 required fields
  - Autocomplete attributes set (name, email, phone)
  - No file upload required on mobile (resume can come later)
- [ ] **No intrusive pop-ups on mobile**
  - No full-screen modals, chat widgets, or cookie banners blocking content
  - Google penalizes intrusive interstitials
- [ ] **HTTPS active** (SSL certificate valid)
  - URL starts with `https://` not `http://`
- [ ] **Landing page loads correctly** (no 404, no redirect loops)
  - Test the exact URL from the campaign, including UTM parameters

### P1 Verdict
```
All 7 items pass → PROCEED to P2
Score < 70 but functional → PROCEED with note (optimize LP in parallel)
404/broken/no HTTPS → STOP. Fix before spending.
```

---

## P2 — Ad Extensions & Assets (SHOULD PASS)

> Extensions add +10-15% CTR. Missing them = leaving performance on the table.

- [ ] **Sitelinks added** (minimum 4)
  - Example: "Browse All Jobs", "See Pay Rates", "How It Works", "Apply Now"
  - Each sitelink has a description (2 lines)
- [ ] **Callout extensions added** (minimum 4)
  - Example: "$18-$25/hr", "Flexible Shifts", "Weekly Pay", "No Long-Term Commitment"
- [ ] **Structured snippets added** (at least 1)
  - Header: "Types" → list of role types or event types
  - Header: "Neighborhoods" → market areas
- [ ] **Location extension enabled** (if applicable)
  - Google Business Profile linked
  - Or manual location extension set
- [ ] **Call extension enabled** (if phone applications accepted)
  - Click-to-call for mobile users
  - Call tracking enabled for reporting
- [ ] **Lead Form extension configured** (recommended for mobile)
  - Fields: Name, Email, Phone (+ optional qualifier)
  - CTA: "Apply Now"
  - Thank-you message with next steps
  - Webhook/download configured for lead delivery
- [ ] **Image extensions uploaded** (if available)
  - Workplace/event photos
  - Minimum 1 landscape (1200x628) + 1 square (1200x1200)

### P2 Verdict
```
All 7 items pass → OPTIMAL setup
4-6 items pass → ACCEPTABLE (add remaining within first week)
< 4 items pass → NOT BLOCKING but schedule fix within 48hrs
```

---

## P3 — Campaign Settings Verification (SHOULD PASS)

- [ ] **Campaign name follows convention**
  - `{Channel}-{JobCategory}-{Market}-{Goal}` (e.g., `Search-Server-Dallas-Applications`)
- [ ] **Geographic targeting correct**
  - Set to "People IN this location" (not "People interested in")
  - Radius or city matches job location
- [ ] **Language targeting set**
  - English (always)
  - Spanish (if bilingual role — as separate ad group)
- [ ] **Ad schedule configured** (if known peak hours)
  - Hospitality candidates: evenings 6-10pm + weekends often peak
- [ ] **Bidding strategy appropriate**
  - New campaign: Maximize Conversions
  - Established (15+ conv/month): Target CPA
  - Budget ≥ 10x target CPA for Smart Bidding
- [ ] **Ad Strength indicator checked**
  - Target: "Good" or "Excellent"
  - If "Poor" or "Average": add more headline variety + keyword inclusion
- [ ] **Negative keywords applied**
  - Shared negative keyword list applied
  - Role-specific negatives added (see hospitality-campaign-launch.md)

---

## Verification Summary

| Section | Items | Status | Verdict |
|---------|:-----:|:------:|---------|
| P0 — Conversion Tracking | 6 | ☐ Pass / ☐ Fail | **BLOCKING** |
| P1 — Landing Page Quality | 7 | ☐ Pass / ☐ Fail | **BLOCKING** |
| P2 — Extensions & Assets | 7 | ☐ Pass / ☐ Partial | Advisory |
| P3 — Campaign Settings | 7 | ☐ Pass / ☐ Partial | Advisory |

**Verified by:** _________________ **Date:** _______________

**Campaign cleared for launch:** ☐ Yes ☐ No — Fix items: _________________

---

*This checklist is a pre-launch GATE. P0 and P1 must pass before any spend is activated. P2 and P3 are advisory but should be completed within 48 hours of launch.*
