# Google Ads Campaign Types Reference

> Source: [Google Business Resource Hub](https://business.google.com/us/resources/)

## Campaign Type Matrix

| Type | Best For | Channels | Bidding | Complexity |
|------|----------|----------|---------|------------|
| **Search** | High-intent candidates | Google Search, Search Partners | CPC, Smart Bidding | Medium |
| **Performance Max** | Cross-channel reach | Search, Display, YouTube, Gmail, Maps | Smart Bidding only | Low (AI-driven) |
| **Display** | Brand awareness, remarketing | 2M+ websites, apps, YouTube | CPC, CPM, Smart Bidding | Medium |
| **Video/YouTube** | Employer branding, engagement | YouTube, Video Partners | CPV, CPM, CPC | Medium-High |
| **App** | App installs, engagement | Search, Play, YouTube, Display | CPA, Smart Bidding | Low |
| **Local Services** | Local service leads | Google Search (top) | Pay-per-lead | Low |

---

## Search Campaigns

### When to Use
- Targeting candidates actively searching for jobs
- High-intent keywords (e.g., "warehouse jobs near me", "temp work hiring now")
- Driving applications from job seekers with clear intent

### Structure
```
Account
└── Campaign (by job category or market)
    └── Ad Group (by specific role or keyword theme)
        ├── Keywords (match types configured)
        ├── Responsive Search Ads (3-15 headlines, 2-4 descriptions)
        └── Extensions (sitelinks, callouts, location, call)
```

### Key Settings
- **Bidding:** Maximize Conversions or Target CPA for application-focused campaigns
- **Match Types:** Broad match + Smart Bidding recommended (62% of Smart Bidding advertisers use broad match)
- **AI Max for Search:** Activating yields ~14% more conversions at similar CPA
- **Ad Rotation:** Optimize for best-performing ads
- **Networks:** Search Network (opt out of Display for focused Search)

### Recruitment Applications
- Target job-title keywords + location modifiers
- Use ad customizers for dynamic city/role insertion
- Schedule ads for peak candidate search times
- Link to specific job listing pages, not generic career pages

---

## Performance Max Campaigns

### When to Use
- Maximizing reach across all Google channels from a single campaign
- When you have strong creative assets and first-party data
- Complementing existing Search campaigns for incremental conversions

### Key Stats
- **+18% incremental conversions** at similar CPA (Google benchmark)
- Serves across YouTube, Display, Search, Gmail, Maps simultaneously
- AI automatically mixes and matches assets for best combinations

### Asset Requirements
| Asset Type | Minimum | Recommended |
|------------|---------|-------------|
| Headlines | 5 | 15 |
| Long headlines | 1 | 5 |
| Descriptions | 2 | 5 |
| Images (landscape) | 1 | 3+ |
| Images (square) | 1 | 3+ |
| Images (portrait) | 0 | 1+ |
| Videos | 0 | 1+ (auto-generated if missing) |
| Logos | 1 | 2 |

### Optimization Tips
1. Set clear conversion goals (applications, registrations)
2. Integrate first-party candidate data as audience signals
3. Supply 20+ diverse text assets for maximum AI testing
4. Combine with keyword-based Search campaigns for best results
5. Allow 6-week ramp-up before evaluating performance

> See `performance-max-playbook.md` for detailed guide.

---

## Display Campaigns

### When to Use
- Employer brand awareness at scale
- Remarketing to site visitors who didn't apply
- Reaching passive candidates browsing other sites

### Targeting Options
| Method | Description | Recruitment Use |
|--------|-------------|-----------------|
| Affinity Audiences | 80+ predefined interest groups | Target career-minded audiences |
| Custom Affinity | Keywords + URLs you define | Target competitor career page visitors |
| In-Market Audiences | Actively researching similar products | Target active job seekers |
| Demographics | Age, gender, parental status | Filter by candidate demographics |
| Remarketing | Previous site visitors | Re-engage dropped applicants |

### Responsive Display Ads
- Auto-adjust size, shape, and format to fit any placement
- Provide: text + images + logos → Google creates combinations
- Video assets used automatically when they outperform static images
- Key benefit: one ad creation, millions of placements

---

## Video / YouTube Campaigns

### Ad Formats
| Format | Length | Skippable | Best For |
|--------|--------|-----------|----------|
| Skippable in-stream | Any | After 5s | Employer brand storytelling |
| Non-skippable in-stream | 15-30s | No | Key messages that must be seen |
| Bumper | 6s max | No | Quick brand impressions |
| In-feed | Any | N/A | Discovery, browsing context |
| Shorts | <60s | Yes | Mobile-first engagement |
| Masthead | Any | N/A | Mass awareness (premium) |

### Bidding Options
- **CPV (Cost-per-view):** Pay when someone watches 30s or interacts
- **CPM (Cost-per-thousand impressions):** Pay per 1,000 views
- **CPC:** Pay per click to landing page

> See `youtube-ads-playbook.md` for detailed guide.

---

## Local Services Ads

### When to Use
- Location-specific hiring events
- Market-level candidate acquisition
- Pay-per-lead model (only pay for qualified leads)

### Key Features
- Appear at the very top of Search results
- Leads via phone, text, email, or booking
- No keyword research required
- Google Guarantee/Screened badges for trust

### Recruitment Applications
- Promote hiring events in specific cities
- Drive in-person interview sign-ups
- Target candidates within commuting distance

---

## Campaign Selection Guide for Recruitment

| Goal | Primary Campaign | Supporting |
|------|-----------------|------------|
| Drive applications from active job seekers | Search | Performance Max |
| Build employer brand awareness | Video/YouTube | Display |
| Re-engage site visitors who didn't apply | Display (Remarketing) | Performance Max |
| Promote local hiring events | Local Services | Search (geo-targeted) |
| Maximize reach with limited management time | Performance Max | Search |
| Test new markets/roles quickly | Search (broad match) | — |
