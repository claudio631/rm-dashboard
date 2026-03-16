---
task: Analytics & Performance Reporting
responsavel: "@analytics-performance-lead"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - report_type: weekly | monthly | channel-deep-dive | cost-per-hire | funnel
  - date_range: Reporting period
  - channels: Channels to include
  - markets: Geographic markets to analyze
Saida: |
  - report: Formatted performance report
  - insights: Key findings and trends
  - recommendations: Data-backed action items
  - dashboard_updates: Updated dashboard metrics
Checklist:
  - "[ ] Pull data from all active channels"
  - "[ ] Validate data accuracy and completeness"
  - "[ ] Calculate key metrics (CPA, CPH, ROAS, conversion rates)"
  - "[ ] Compare to benchmarks and prior period"
  - "[ ] Identify top/bottom performing campaigns"
  - "[ ] Analyze funnel drop-off points"
  - "[ ] Generate actionable recommendations"
  - "[ ] Update dashboards"
  - "[ ] Distribute to stakeholders"
---

# Analytics & Performance Reporting

Generate comprehensive recruitment marketing performance reports for Indeed Flex.

## Report Types

| Report | Frequency | Audience | Focus |
|--------|-----------|----------|-------|
| Weekly Performance | Weekly | Marketing team | Campaign metrics, spend, applications |
| Monthly Executive | Monthly | Leadership | Cost-per-hire, fill rate, ROI |
| Channel Deep Dive | Ad hoc | Channel specialists | Single channel optimization |
| Cost-per-Hire | Monthly | Finance + Marketing | Full funnel cost analysis |
| Funnel Analysis | Bi-weekly | All | Apply → Screen → Interview → Hire |

## North Star Metrics

1. **Blended Cost-per-Hire** — Total marketing spend / total hires
2. **Fill Rate** — Positions filled / positions posted
3. **Time-to-Fill** — Days from posted to hired
4. **Candidate Quality** — 90-day retention by source
5. **Marketing ROI** — Revenue from placed workers / marketing spend
