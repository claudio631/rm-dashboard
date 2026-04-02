# CRM Template: Event Staff Compliance & Reengagement
<!-- Case: SXSW 2026 — Reusable for any major event with compliance requirements -->

## Brief Metadata

| Field | Value |
|---|---|
| **Use Case** | Event staff compliance reengagement (multi-step) |
| **Goal** | Complete compliance requirements + book a shift |
| **Primary Metric** | Compliance completion rate |
| **Client/Event** | `{{EVENT_NAME}}` (e.g., SXSW 2026) |
| **Location** | `{{CITY_STATE}}` (e.g., Austin, TX) |
| **Dates** | `{{EVENT_START_DATE}}` to `{{EVENT_END_DATE}}` |
| **Headcount Target** | `{{HC_TARGET}}` Flexers |
| **Pay Rate** | Up to `{{PAY_RATE}}`/hr |
| **Age Requirement** | `{{AGE_REQUIREMENT}}` (e.g., 21+) |

## Audience Segmentation

| Segment | Definition |
|---|---|
| **Active** | Completed shift in last 15 days OR logged in within 3 days |
| **Lapsing** | No shift in 15+ days OR login 3–90 days ago (largest group ~55%) |
| **Dormant** | No shift or login in 90+ days (~60% of reachable audience) |

**Audience Criteria:** Flexers within `{{RADIUS}}` miles of `{{CITY_STATE}}` city center, active in the last 365 days, verified for `{{ROLE_TYPE}}`.

---

## Communication Sequence

### Step 1A — Active Users: Initial Awareness (Push Notification)
**Channel:** Push Notification
**Launch:** `{{LAUNCH_DATE_STEP_1}}`
**Goal:** Prompt user to open the app

> **Header:** Want to work at `{{EVENT_NAME}}`?
>
> **Body:** The festival is coming up, and you could work there! Just take our free training. See app for info.

---

### Step 1B — Lapsing/Dormant Users: Initial Outreach (Email)
**Channel:** Email
**Launch:** `{{LAUNCH_DATE_STEP_1}}`
**Goal:** Complete compliance and book a shift

> **Subject Line:** Come back and cover `{{EVENT_NAME}}`! / Don't miss exclusive `{{EVENT_NAME}}` shifts!
>
> **Pre-header:** Be part of something big! / See the event, earn up to `{{PAY_RATE}}`/hr!
>
> **Header:** Take our quick, free training
>
> **Body:**
> Hi [First Name],
>
> It's `{{EVENT_NAME}}` season in `{{CITY}}` again, which means exclusive shifts are available, right across `{{EVENT_MONTH}}`.
>
> They're looking for `{{ROLE_TYPE}}` like you — paying up to `{{PAY_RATE}}`/hr, covering `{{EVENT_DESCRIPTION}}`.
>
> You can access these shifts by completing our quick, free training.
> Simply click below, search '`{{EVENT_SKILL_NAME}}`', and follow the steps:
>
> **[Start Training]**
>
> Steps:
> 1. Tap 'Start Onboarding'
> 2. Watch the training video in full
> 3. Take the quiz that follows
> 4. `{{COMPLIANCE_STEP_4}}` (e.g., Enter your t-shirt size)
> 5. `{{COMPLIANCE_STEP_5}}` (e.g., Enter your age)

---

### Step 1C — Active Users: In-App Engagement (In-App Message)
**Channel:** In-App Message
**Launch:** `{{LAUNCH_DATE_STEP_1B}}`
**Goal:** Complete compliance and book a shift

> **Header:** Work at `{{EVENT_NAME}}`, earn up to `{{PAY_RATE}}`/hr
>
> **Body:** `{{EVENT_NAME}}` is coming up and you could be part of it!
> They need skilled `{{ROLE_TYPE}}` to cover the whole `{{EVENT_DURATION}}`. Take our free training to access all shifts.
>
> Simply hop onto the Flex app and:
> - Search '`{{EVENT_SKILL_NAME}}`'
> - Tap 'Start Onboarding'
> - Watch the training video in full
> - Take the quiz that follows
> - `{{COMPLIANCE_STEP_4}}`
> - `{{COMPLIANCE_STEP_5}}`
>
> **[Start Now]**

---

### Step 2A — Active Non-Responders: Follow-up (Email)
**Channel:** Email
**Launch:** 48 hours after Step 1
**Audience:** Active users who did not engage with Step 1

> **Subject Line:** There's still time to be part of `{{EVENT_NAME}}`! / Be part of `{{CITY}}`'s biggest event!
>
> **Pre-header:** Earn up to `{{PAY_RATE}}`/hr / See the festival, get paid!
>
> **Header:** Take our quick, free training
>
> **Body:**
> Hi [First Name],
>
> `{{EVENT_NAME}}` is just around the corner, which means we've got exciting event roles available throughout `{{EVENT_MONTH}}`.
>
> They're looking for staff to cover `{{EVENT_DESCRIPTION}}` — paying up to `{{PAY_RATE}}`/hr.
>
> Want to be part of it? All you have to do is take our quick training and quiz.
>
> To get started simply tap below and search for '`{{EVENT_SKILL_NAME}}`', then follow the steps.
>
> **[Start Training]**
>
> **CTA:** [Start Training]

---

### Step 2B — Lapsing/Dormant Non-Responders: Follow-up SMS
**Channel:** SMS
**Launch:** 24 hours after Step 1B
**Audience:** Lapsing/Dormant users who did not open email

> Hi {{${first_name} | default: 'Flexer' | capitalize}}, still time to land those exclusive `{{EVENT_NAME}}` event shifts, paying up to `{{PAY_RATE}}`/hr.
>
> Be part of something big! Take your free training to access them ASAP! Search '`{{EVENT_SKILL_NAME}}`' in the app to begin: `{{APP_DEEPLINK}}`
>
> Indeed Flex
>
> Reply STOP to unsubscribe.

---

### Step 3 — All Non-Responders: Final Push (Email + SMS)
**Channel:** Email + SMS
**Launch:** `{{FINAL_PUSH_DATE}}`
**Audience:** Anyone who has not completed compliance

> **Email Subject:** Last chance — `{{EVENT_NAME}}` shifts filling fast!
>
> **SMS:**
> Flex Alert: `{{EVENT_NAME}}` is here! `{{ROLE_TYPE}}` roles available across `{{EVENT_DURATION}}` — paying up to `{{PAY_RATE}}`/hr! Take our free training to access shifts.
> Tap the link and search '`{{EVENT_SKILL_NAME}}`': `{{APP_DEEPLINK}}`
> Indeed Flex — Reply STOP to unsubscribe.

---

## Compliance Requirements Checklist
*Fill in for each event:*

- [ ] `{{COMPLIANCE_ITEM_1}}` (e.g., Watch training video + take quiz)
- [ ] `{{COMPLIANCE_ITEM_2}}` (e.g., Enter t-shirt size)
- [ ] `{{COMPLIANCE_ITEM_3}}` (e.g., Enter age — confirm 21+)
- [ ] `{{COMPLIANCE_ITEM_4}}` (e.g., Consent to phone number sharing)
- [ ] Age restriction noted in all comms: `{{AGE_REQUIREMENT}}`

## Key Variables to Replace

| Variable | Description |
|---|---|
| `{{EVENT_NAME}}` | Name of the event (e.g., SXSW 2026) |
| `{{CITY_STATE}}` | City and state (e.g., Austin, TX) |
| `{{CITY}}` | City only |
| `{{EVENT_START_DATE}}` / `{{EVENT_END_DATE}}` | Event dates |
| `{{EVENT_MONTH}}` | Month range (e.g., March) |
| `{{EVENT_DURATION}}` | Duration text (e.g., "two weeks") |
| `{{EVENT_DESCRIPTION}}` | What the event involves |
| `{{EVENT_SKILL_NAME}}` | Skill name in app (e.g., "SXSW Event Staff") |
| `{{ROLE_TYPE}}` | Role being filled (e.g., Event Staff) |
| `{{PAY_RATE}}` | Pay rate (e.g., $18) |
| `{{HC_TARGET}}` | Headcount needed |
| `{{AGE_REQUIREMENT}}` | Age requirement (e.g., 21+) |
| `{{RADIUS}}` | Geographic radius (e.g., 15) |
| `{{COMPLIANCE_STEP_4/5}}` | Event-specific compliance steps |
| `{{APP_DEEPLINK}}` | Indeed Flex app deep link |
| `{{LAUNCH_DATE_STEP_1}}` | Date for first send |
| `{{FINAL_PUSH_DATE}}` | Date for final reminder |

---
*Source: SXSW 2026 CRM Brief — March 2026*
*Template saved by Relay (CRM Specialist) — recruitment-marketing-flex squad*
