# Google Ads Conversion Tracking Guide

> Source: [Google Business Resource Hub](https://business.google.com/us/resources/)

## What is Conversion Tracking?

Conversion tracking measures what happens after a candidate interacts with your ad — whether they apply, register, call, or take another valuable action. Without it, you're flying blind on ROI.

---

## Conversion Types for Recruitment

| Conversion Action | Type | Value | Priority |
|------------------|------|-------|----------|
| Application submitted | Website | High ($50-100) | Primary |
| Registration completed | Website | Medium ($20-40) | Primary |
| Phone call (>60 seconds) | Phone | Medium ($15-30) | Primary |
| Registration started | Website | Low ($5-10) | Secondary |
| Job listing page viewed | Website | Micro ($1-2) | Observation |
| App install | App | Medium ($10-20) | If applicable |

---

## Setup Steps

### Step 1: Install Google Tag
```html
<!-- Global site tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-XXXXXXXXX');
</script>
```
- Install on ALL pages (sitewide tagging)
- Use Google Tag Manager for easier management
- Verify with Google Tag Assistant

### Step 2: Create Conversion Actions
In Google Ads → Goals → Conversions:
1. Click "+ New conversion action"
2. Select source: Website, App, Phone calls, or Import
3. Define:
   - Category (e.g., "Submit lead form")
   - Conversion name (e.g., "Application Submitted")
   - Value (static or dynamic)
   - Count (every vs. one per click)
   - Click-through window (30-90 days)
   - View-through window (1-30 days)

### Step 3: Add Event Snippets
Place on confirmation/thank-you pages:
```html
<!-- Event snippet for Application Submitted conversion -->
<script>
  gtag('event', 'conversion', {
    'send_to': 'AW-XXXXXXXXX/XXXXXXXXXX',
    'value': 50.0,
    'currency': 'USD'
  });
</script>
```

### Step 4: Enable Enhanced Conversions
Improves accuracy by securely matching conversion data:
- Hash user-provided data (email, phone)
- Recovers conversions lost to cookie limitations
- Setup via Google Tag or GTM
- Requires first-party data consent

### Step 5: Link Google Analytics 4
- Import GA4 goals as Google Ads conversions
- Enable auto-tagging for accurate attribution
- Access post-click behavior data:
  - Bounce rate
  - Pages per session
  - Session duration
  - User flow through application funnel

---

## Key Conversion Metrics

| Metric | Formula | What It Tells You |
|--------|---------|------------------|
| Cost per Conversion | Total Cost ÷ Conversions | How much each application costs |
| Conversion Rate | Conversions ÷ Clicks × 100 | Percentage of clicks that convert |
| Conversion Value | Sum of all conversion values | Total value generated |
| Conversion Value / Cost | Total Value ÷ Total Cost | ROI estimate |
| View-through Conversions | Auto-tracked | Impact of ad impressions |

---

## Attribution Models

### Available Models
| Model | Description | Best For |
|-------|-------------|----------|
| Data-driven | AI assigns credit based on actual paths | Default (recommended) |
| Last click | 100% credit to final click | Simple measurement |
| First click | 100% credit to first interaction | Understanding discovery |
| Linear | Equal credit across all touchpoints | Multi-channel campaigns |
| Time decay | More credit to recent interactions | Long consideration cycles |
| Position-based | 40% first, 40% last, 20% middle | Balanced view |

### Recommendation
Use **Data-driven attribution** (Google's default) — it uses machine learning to assign credit based on how each touchpoint actually contributes to conversions.

---

## Attribution Reports

### 1. Path Metrics Report
Shows how long and how many interactions it takes candidates to convert:
- Average days to conversion
- Average interactions before conversion
- Helps set appropriate conversion windows

### 2. Conversion Paths Report
Displays the most common journeys candidates take:
```
Example paths:
Search → Direct → Conversion
Display → Search → Search → Conversion
YouTube → Display → Search → Conversion
```
Helps understand which channels assist vs. close.

### 3. Assisted Conversions Report
Shows which touchpoints help drive conversions without being the final click:
- YouTube may have low last-click conversions but high assists
- Display remarketing often assists Search conversions
- Helps justify brand/awareness spend

---

## Conversion Tracking Best Practices

1. **Track all meaningful actions** — not just final applications
2. **Assign values** — helps Smart Bidding optimize for quality, not just volume
3. **Use enhanced conversions** — recovers 5-15% of conversions lost to cookie limitations
4. **Review attribution weekly** — understand the full candidate journey
5. **Set appropriate windows** — recruitment consideration can take 1-14 days
6. **Verify tracking monthly** — check for tag firing issues
7. **Import offline conversions** — if applications are processed offline, import back to Google Ads
8. **Separate primary vs. secondary conversions** — only optimize campaigns toward primary actions
