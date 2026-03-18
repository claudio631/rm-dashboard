# Mobile Optimization Guide for Google Ads

> Source: [Google Business Resource Hub](https://business.google.com/us/resources/)

## Why Mobile Matters for Recruitment

Most job seekers search on mobile devices. If your landing pages don't work well on mobile, you're paying for clicks that won't convert.

---

## 5 Mobile Landing Page Principles

### 1. Responsive Design
- Pages must adapt to device screen size — not just shrink desktop layouts
- Use responsive frameworks (already handled by Next.js)
- Test on multiple devices and screen sizes
- Ensure tap targets are at least 48x48px

### 2. Relevance & Landing Page Match
- Ad for "warehouse jobs in Dallas" → land on Dallas warehouse jobs page
- **Never** send mobile users to a generic homepage
- Match headline on landing page to ad headline
- Show the specific job/role advertised

### 3. Speed & Simplicity
- **Target:** <3 second load time on 4G
- Prioritize content candidates need immediately
- Feature prominent search functionality
- Minimize required scrolling to reach CTA
- Test with Google PageSpeed Insights

### 4. Easy Navigation
- Intuitive menu with drop-down buttons
- Home button accessible from every page
- Clear back navigation
- Sticky CTA button (always visible)

### 5. No Intrusive Pop-ups
- Avoid full-screen promotions or chat widgets that block content
- Use discrete banners instead of modal overlays
- Google penalizes intrusive interstitials in mobile rankings
- If using pop-ups, ensure easy dismissal

---

## Mobile Copy Guidelines

- Fewer words per screen than desktop — prioritize ruthlessly
- Lead with the most important information (pay, location, shift)
- Short sentences, bullet points over paragraphs
- CTAs should be action-specific: "Apply Now" not "Learn More"
- Phone numbers should be click-to-call

---

## Mobile Image Strategy

- Use images that work at small sizes
- Product/workplace photos engage without excessive text
- Consider how video plays on mobile (autoplay without sound)
- Optimize image file sizes for fast loading
- Use WebP format for 25-35% smaller files

---

## Page Speed Optimization

### Google's Requirements
| Metric | Target | Tool |
|--------|--------|------|
| Largest Contentful Paint (LCP) | <2.5 seconds | PageSpeed Insights |
| First Input Delay (FID) | <100ms | PageSpeed Insights |
| Cumulative Layout Shift (CLS) | <0.1 | PageSpeed Insights |
| Overall Score | >80 (mobile) | PageSpeed Insights |

### Speed Optimization Checklist
- [ ] Compress all images (WebP, max 200KB)
- [ ] Minimize JavaScript bundles
- [ ] Enable browser caching
- [ ] Use CDN for static assets
- [ ] Lazy-load below-fold images
- [ ] Preload critical resources
- [ ] Reduce server response time (<200ms)
- [ ] Remove unused CSS/JS

---

## Mobile Form Optimization

### Application Form Best Practices
- Minimize required fields (name, email, phone = minimum viable)
- Use autofill-compatible field names
- Enable Google Sign In for single-tap registration
- Use dropdown menus instead of free-text where possible
- Show progress indicator for multi-step forms
- Save partial progress (don't lose data on back-navigation)
- Add click-to-call as alternative to form completion

### Form Field Recommendations
| Field | Required? | Mobile Optimization |
|-------|-----------|-------------------|
| Name | Yes | Autocomplete="name" |
| Email | Yes | type="email", autocomplete |
| Phone | Yes | type="tel", autocomplete |
| Location | Optional | Use device GPS / zip code |
| Job Interest | Optional | Dropdown, not free text |
| Resume | No (mobile) | Allow later upload |

---

## Mobile Ad Considerations

### Device Targeting
- Review device performance data in Google Ads
- Adjust mobile bid modifiers based on mobile conversion rates
- If mobile CPA is higher: optimize landing page before reducing bids
- Use call extensions for mobile (direct phone application)

### Mobile-Specific Ad Extensions
| Extension | Mobile Benefit |
|-----------|---------------|
| Call | Tap-to-call for immediate connection |
| Location | Map link for nearby positions |
| Lead Form | In-ad application (no page load needed) |
| App | Direct to app store for registration |
| Sitelinks | Quick links to key pages |

### Mobile Ad Copy Tips
- First headline must be compelling (limited visible space)
- Include location in visible headlines
- Use call CTA on mobile-heavy campaigns
- Test shorter vs. longer descriptions
