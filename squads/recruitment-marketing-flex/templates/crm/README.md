# CRM Email Template Library

Templates for candidate communication campaigns at Indeed Flex US.
Each template is case-specific and ready to adapt with fill-in-the-blank placeholders.

---

## Template Index

| Template | File | Use Case | Channels |
|---|---|---|---|
| **Event Reengagement — Compliance & Booking** | `event-reengagement-compliance-tmpl.md` | Large events needing worker compliance + booking (e.g., SXSW) | Email + SMS + Push + In-App |
| **Client Compliance Reengagement** | `client-compliance-reengagement-tmpl.md` | Client-specific certifications (drug test, background check) to unlock shifts | Email + SMS |
| **New Hire Orientation (NHO)** | `nho-new-hire-orientation-tmpl.md` | Recurring NHO campaigns for clients requiring orientation before shifts | Email + SMS |
| **Incentive & Promotion** | `incentive-promotion-tmpl.md` | Time-limited bonuses and shift incentives for fulfilment boosts | Email + SMS + Push |

---

## When to Use Which Template

```
Need to fill an event with 300+ workers + compliance steps?
→ event-reengagement-compliance-tmpl.md

Client requires drug test or certification before workers can be booked?
→ client-compliance-reengagement-tmpl.md

Client requires orientation (NHO) before regular shifts?
→ nho-new-hire-orientation-tmpl.md

Running a bonus or incentive to boost shift bookings?
→ incentive-promotion-tmpl.md
```

---

## How to Use a Template

1. Copy the relevant template file
2. Replace all `[PLACEHOLDERS]` with campaign-specific values
3. Confirm compliance fields with client/ops team
4. Submit to CRM team via `#marketing-requests-new` with audience list link
5. Sign off on copy before CRM builds campaign
6. Approve test comms before launch

---

## Audience Segmentation (Standard)

| Segment | Definition |
|---|---|
| **Active** | Shift in last 15 days OR login in last 3 days |
| **Lapsing** | No shift 15+ days OR no login 3–90 days |
| **Dormant** | No shift or login 90+ days |

*Always pull audience from Redash with city/market + role filter.*

---

*Maintained by: @crm-email-specialist (Relay)*
*Last updated: 2026-03-20*
