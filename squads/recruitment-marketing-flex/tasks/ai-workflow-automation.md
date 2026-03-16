---
task: AI Workflow Automation
responsavel: "@ai-automation-specialist"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - workflow_type: bidding | reporting | creative | integration | scoring
  - current_process: Description of the manual process to automate
  - platforms: Involved marketing platforms
  - frequency: How often the automation should run
Saida: |
  - automation_spec: Complete automation design document
  - workflow_diagram: Visual flow of the automation
  - implementation_steps: Step-by-step setup guide
  - monitoring_plan: Alerts and fallback mechanisms
Checklist:
  - "[ ] Map current manual process"
  - "[ ] Identify automation opportunities and ROI"
  - "[ ] Design workflow with triggers, actions, conditions"
  - "[ ] Define error handling and fallbacks"
  - "[ ] Set up monitoring and alerting"
  - "[ ] Create documentation for maintenance"
  - "[ ] Test in staging/sandbox environment"
  - "[ ] Deploy with rollback plan"
---

# AI Workflow Automation

Design and implement AI-powered automation for Indeed Flex recruitment marketing processes.

## Automation Categories

| Category | Examples | Tools |
|----------|----------|-------|
| Bid Automation | Smart bidding, budget pacing | Google Ads API, Meta Marketing API |
| Report Automation | Scheduled reports, alerts | GA4, Looker, custom scripts |
| Creative Automation | Dynamic ad copy, A/B rotation | Platform APIs, AI generation |
| Integration | ATS ↔ Marketing data sync | Zapier, Make, custom APIs |
| Candidate Scoring | Predictive apply/hire models | ML pipelines, CRM scoring |

## Automation Maturity Roadmap

1. **Foundation** — UTM governance, tracking setup, basic reporting
2. **Efficiency** — Automated reports, rule-based bid management
3. **Intelligence** — Smart bidding, predictive scoring, dynamic creative
4. **Optimization** — Cross-channel orchestration, real-time personalization
