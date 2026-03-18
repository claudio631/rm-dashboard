# Task: Google Ads Performance Analysis

> Agent: @ppc-paid-media-specialist, @analytics-performance-lead
> Elicit: true
> Dependencies: conversion-tracking-guide.md, budget-optimization-guide.md

## Objective
Analyze Google Ads campaign performance, identify optimization opportunities, and generate actionable recommendations.

## Pre-Conditions
- Campaign has been running for at least 2 weeks
- Conversion tracking is active and verified
- Google Analytics 4 is linked
- Access to Google Ads reporting

## Workflow

### Step 1: Define Analysis Scope
**Elicit:** What is the analysis period and focus?
- [ ] Date range (last 7 days, 30 days, custom)
- [ ] Campaigns to analyze (all or specific)
- [ ] Comparison period (previous period, same period last year)
- [ ] Primary KPI focus (CPA, ROAS, volume, quality)

### Step 2: Account-Level Review
- [ ] Total spend vs. budget
- [ ] Total conversions and conversion rate
- [ ] Overall CPA and trend direction
- [ ] Impression share (Search campaigns)
- [ ] Top campaigns by spend and performance

### Step 3: Campaign-Level Analysis
For each campaign, review:

| Metric | Pull Data | Compare To |
|--------|-----------|-----------|
| Spend | Actual vs. budget | Previous period |
| Impressions | Total and trend | Previous period |
| Clicks | Total and CTR | Industry benchmark (3-5%) |
| Conversions | Total and rate | Target CPA |
| CPA | Actual vs. target | Previous period |
| Quality Score | Average across keywords | Benchmark (≥7) |
| Impression Share | Search IS % | Target (>70%) |

### Step 4: Keyword Performance
- [ ] Identify top 10 converting keywords (keep, increase bids)
- [ ] Identify keywords with spend but no conversions (pause or optimize)
- [ ] Review Search Terms Report:
  - Add high-performing new terms as keywords
  - Add irrelevant terms as negatives
- [ ] Check Quality Scores per keyword:
  - <5: Landing page or ad relevance issue
  - 5-6: Optimization opportunity
  - 7+: Good, maintain
- [ ] Analyze match type performance (broad vs. phrase vs. exact)

### Step 5: Ad Copy Performance
- [ ] Review ad-level CTR and conversion rate
- [ ] Identify top-performing headlines and descriptions
- [ ] Check asset performance labels (PMax):
  - Best → Keep, create similar
  - Good → Keep
  - Low → Replace
- [ ] Identify underperforming ads for refresh
- [ ] Note winning copy themes for future use

### Step 6: Audience Performance
- [ ] Review demographic performance (age, gender, device)
- [ ] Analyze audience segment performance (PMax)
- [ ] Check remarketing list performance vs. prospecting
- [ ] Review geographic performance by market
- [ ] Identify bid adjustment opportunities

### Step 7: Landing Page Analysis
- [ ] Review landing page conversion rates by page
- [ ] Check bounce rates (GA4)
- [ ] Review mobile vs. desktop performance
- [ ] Test page speed (PageSpeed Insights)
- [ ] Identify pages needing optimization

### Step 8: Competitive Analysis
- [ ] Review Auction Insights:
  - Impression share vs. competitors
  - Overlap rate
  - Position above rate
- [ ] Note competitive changes (new entrants, increased spend)
- [ ] Identify competitive advantages and threats

### Step 9: Generate Recommendations
Categorize findings into:

**Quick Wins (implement now)**
- Negative keyword additions
- Budget reallocation from underperformers
- Bid adjustments for high/low performers

**Short-Term (next 1-2 weeks)**
- Ad copy refreshes
- New keyword additions
- Landing page optimizations

**Strategic (next 30 days)**
- Campaign restructuring
- New campaign types (e.g., add PMax)
- Budget increases for scaling opportunities

### Step 10: Document & Report
- [ ] Fill in `google-ads-performance-review-tmpl.md`
- [ ] Highlight top 3 wins and top 3 opportunities
- [ ] Include specific action items with owners and deadlines
- [ ] Share with stakeholders

## Post-Conditions
- Performance report generated
- Action items prioritized and assigned
- Budget recommendations documented
- Next review date scheduled

## Outputs
- Performance review document (from template)
- Action item list
- Budget reallocation recommendations
- Competitive landscape summary
