---
task: Candidate Nurturing Sequences
responsavel: "@crm-email-specialist"
responsavel_type: agent
atomic_layer: task
elicit: true
Entrada: |
  - sequence_type: welcome | job-match | re-engagement | onboarding | referral
  - candidate_segment: Target audience segment
  - trigger: What initiates the sequence
  - duration: Sequence length
Saida: |
  - sequence_plan: Complete nurture sequence with timing
  - email_templates: Copy for each email in the sequence
  - segmentation_rules: Audience criteria and filters
  - automation_config: Trigger and workflow logic
Checklist:
  - "[ ] Define candidate segment and entry criteria"
  - "[ ] Map candidate journey touchpoints"
  - "[ ] Write email copy for each step (subject + body)"
  - "[ ] Set timing and delays between messages"
  - "[ ] Configure trigger conditions"
  - "[ ] Add personalization tokens"
  - "[ ] Set exit criteria (applied, unsubscribed, etc.)"
  - "[ ] Verify compliance (CAN-SPAM, unsubscribe)"
  - "[ ] Create fallback for SMS channel"
---

# Candidate Nurturing Sequences

Design and deploy automated candidate nurture journeys for Indeed Flex's talent pool.

## Sequence Types

| Type | Trigger | Goal | Duration |
|------|---------|------|----------|
| Welcome | New application | Convert to first shift | 7 days |
| Job Match | New job matching preferences | Drive application | Immediate |
| Re-engagement | 30+ days inactive | Reactivate worker | 14 days |
| Onboarding | First shift booked | Ensure successful start | 5 days |
| Referral | Completed 10+ shifts | Generate referrals | Ongoing |

## Personalization Dimensions

- Job category preferences
- Location/commute radius
- Shift availability (days, nights, weekends)
- Experience level
- Lifecycle stage (prospect, applicant, active worker, dormant)
