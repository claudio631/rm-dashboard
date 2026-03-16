# A/B Test Plan: {{test_name}}

## Test Overview

| Field | Value |
|-------|-------|
| **Test Name** | {{test_name}} |
| **Channel** | {{channel}} |
| **Campaign** | {{campaign_name}} |
| **Owner** | {{owner}} |
| **Start Date** | {{start_date}} |
| **End Date** | {{end_date}} |
| **Status** | Draft / Running / Complete |

## Hypothesis

**If** we {{change_description}},
**then** we expect {{expected_outcome}},
**because** {{rationale}}.

## Test Variables

| Element | Variant A (Control) | Variant B (Test) |
|---------|-------------------|-----------------|
| {{variable}} | {{control_value}} | {{test_value}} |

## Success Metric

| Metric | Current Baseline | Target Improvement | Minimum Detectable Effect |
|--------|-----------------|-------------------|--------------------------|
| **Primary:** {{primary_metric}} | {{baseline}} | {{target}}% improvement | {{mde}}% |
| **Secondary:** {{secondary_metric}} | {{sec_baseline}} | Monitor | — |

## Test Parameters

| Parameter | Value |
|-----------|-------|
| **Traffic Split** | {{split}} (e.g., 50/50) |
| **Sample Size Needed** | {{sample_size}} per variant |
| **Confidence Level** | 95% |
| **Estimated Duration** | {{duration}} days |
| **Daily Budget** | ${{daily_budget}} |

## Guardrails

- Stop test if CPA exceeds ${{max_cpa}} (2x baseline)
- Stop test if CTR drops below {{min_ctr}}% (50% of baseline)
- Minimum run time: 7 days regardless of early signals

## Implementation

### Variant A (Control)
```
{{control_details}}
```

### Variant B (Test)
```
{{test_details}}
```

## Results (Post-Test)

| Metric | Variant A | Variant B | Difference | Statistical Significance |
|--------|-----------|-----------|------------|------------------------|
| {{primary_metric}} | | | | |
| {{secondary_metric}} | | | | |

## Decision

- [ ] **Winner:** Variant {{winner}}
- [ ] **Action:** {{action_taken}}
- [ ] **Learnings documented**

## Learnings

{{learnings}}

---
*Template: ab-test-plan-tmpl.md | Squad: recruitment-marketing-flex*
