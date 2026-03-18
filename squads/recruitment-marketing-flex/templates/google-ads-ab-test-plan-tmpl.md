# Google Ads A/B Test Plan

> Template for planning and documenting Google Ads experiments
> One test per document for clear tracking

---

## Test Overview

| Field | Value |
|-------|-------|
| **Test Name** | {Descriptive name, e.g., "Pay in Headline vs. Benefit Headline"} |
| **Test ID** | {GADS-TEST-001} |
| **Campaign** | {Campaign name} |
| **Ad Group(s)** | {Ad group(s) being tested} |
| **Owner** | {Name} |
| **Start Date** | {YYYY-MM-DD} |
| **End Date** | {YYYY-MM-DD} |
| **Status** | Planning / Running / Complete / Cancelled |

---

## Hypothesis

**If** we {change being made},
**then** {expected outcome},
**because** {rationale based on data or best practice}.

Example:
> **If** we include the pay rate ($18/hr) in Headline 1,
> **then** CTR will increase by 10-15%,
> **because** pay is the #1 motivator for our candidate audience based on survey data.

---

## Test Design

### Variable Being Tested
| Element | Control (A) | Variant (B) |
|---------|------------|------------|
| {e.g., Headline 1} | {Current: "Warehouse Jobs — Houston"} | {Test: "$18/hr Warehouse Jobs — Houston"} |

### What Stays the Same
- [ ] All other headlines remain identical
- [ ] Descriptions unchanged
- [ ] Landing page unchanged
- [ ] Targeting unchanged
- [ ] Budget split equally
- [ ] Bidding strategy unchanged

### Test Method
- [ ] **Google Ads Experiment** (recommended — automatic 50/50 split)
- [ ] **Ad Variation** (for text-only changes)
- [ ] **Manual A/B** (separate ad groups — less reliable)
- [ ] **Campaign Experiment** (for bidding/targeting changes)

---

## Success Metrics

### Primary Metric
| Metric | Current Baseline | Target Improvement | Minimum Detectable Effect |
|--------|-----------------|-------------------|--------------------------|
| {e.g., CTR} | {e.g., 4.2%} | {e.g., +15% → 4.8%} | {e.g., +10%} |

### Secondary Metrics (monitor for negative impact)
| Metric | Current Baseline | Acceptable Range |
|--------|-----------------|-----------------|
| {e.g., Conversion Rate} | {e.g., 5.1%} | {e.g., ≥4.5%} |
| {e.g., CPA} | {e.g., $42} | {e.g., ≤$50} |
| {e.g., Quality Score} | {e.g., 7} | {e.g., ≥6} |

---

## Sample Size & Duration

| Parameter | Value |
|-----------|-------|
| Estimated weekly clicks (per variant) | {X} |
| Required sample size per variant | {X clicks or conversions} |
| Confidence level | 95% |
| Estimated test duration | {X weeks} |
| Minimum test duration | 2 weeks (1 full business cycle) |

**Note:** Do not end the test early even if results look promising. Wait for statistical significance.

---

## Execution Checklist

### Pre-Launch
- [ ] Baseline metrics recorded
- [ ] Test variant created in Google Ads
- [ ] Traffic split configured (50/50)
- [ ] No other changes scheduled during test period
- [ ] Test documented in team tracking system
- [ ] Stakeholders notified

### During Test
- [ ] Monitor daily for errors or anomalies
- [ ] Do NOT make changes to test variables
- [ ] Record any external factors (seasonality, market changes)
- [ ] Check that traffic split is balanced

### Post-Test
- [ ] Wait for statistical significance (95% confidence)
- [ ] Record final results
- [ ] Analyze primary and secondary metrics
- [ ] Document winner and learnings
- [ ] Implement winning variant
- [ ] Plan next test based on learnings

---

## Results

### Raw Data
| Metric | Control (A) | Variant (B) | Difference | Stat. Sig? |
|--------|------------|------------|-----------|-----------|
| Impressions | {X} | {X} | | |
| Clicks | {X} | {X} | | |
| CTR | {X}% | {X}% | +/-{X}% | Yes/No |
| Conversions | {X} | {X} | | |
| Conv. Rate | {X}% | {X}% | +/-{X}% | Yes/No |
| CPA | ${X} | ${X} | +/-${X} | Yes/No |

### Winner
**{Control (A) / Variant (B) / No clear winner}**

### Confidence Level
{X}% confidence that {winner} outperforms {loser} on {primary metric}.

---

## Learnings & Next Steps

### Key Takeaways
1. {What did we learn?}
2. {What surprised us?}
3. {How does this inform future strategy?}

### Implementation
- [ ] Winning variant applied to campaign
- [ ] Results shared with team
- [ ] Insights added to ad copy playbook

### Next Test
| Field | Value |
|-------|-------|
| Proposed test | {Description} |
| Variable | {What to test next} |
| Hypothesis | {If/then/because} |
| Estimated start | {Date} |
