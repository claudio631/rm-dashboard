# CRM Template: Client Compliance Reengagement (Drug Test)
<!-- Case: CORT Las Vegas — Reusable for any client requiring drug test compliance -->

## Brief Metadata

| Field | Value |
|---|---|
| **Use Case** | Client-specific compliance reengagement (drug test) |
| **Goal** | Complete compliance (drug test) + book a shift |
| **Primary Metric** | Drug test completion rate |
| **Client** | `{{CLIENT_NAME}}` (e.g., CORT) |
| **Location** | `{{MARKET}}` (e.g., Las Vegas, NV) |
| **Role** | `{{ROLE_TYPE}}` (e.g., Loader/Crew) |
| **Pay Rate** | Up to `{{PAY_RATE}}`/hr |
| **Drug Test Type** | `{{DRUG_TEST_TYPE}}` (e.g., 9-panel) |
| **Onboarding Path** | Browse Jobs → `{{UPSKILLING_SHIFT_NAME}}` shift → follow in-app steps |

## Audience Segmentation

| Segment | Definition |
|---|---|
| **Active** | Completed a shift recently, not yet compliant with client |
| **Inactive** | Has not completed a shift in 90+ days |

**Audience Criteria:** Flexers in `{{MARKET}}`, verified for `{{ROLE_TYPE}}`, not yet compliant with `{{CLIENT_NAME}}`.
**Audience list:** `{{AUDIENCE_LIST_LINK}}`

---

## Communication Sequence

### Step 1A — Inactive Users: Initial Outreach (Email)
**Channel:** Email
**Goal:** Complete compliance (drug test) and book a shift

> **Subject Line:** Want to earn more through `{{CLIENT_NAME}}`?
>
> **Pre-header:** Get compliant, see more shifts
>
> **Header:** See new opportunities
>
> **Body:**
> Hi [First Name],
>
> Want to start earning through Flex again?
>
> We've got brand-new `{{ROLE_TYPE}}` roles available with `{{CLIENT_NAME}}`, paying up to `{{PAY_RATE}}`/hr.
>
> If you've completed your standard Drug Test, you can book any available shifts now. If you haven't had your Drug Test, please go to the app and complete your `{{CLIENT_NAME}}` onboarding.
>
> To get started, go to 'Browse Jobs', tap an '`{{UPSKILLING_SHIFT_NAME}}`' shift, and you'll be shown how to complete the test.
>
> **[Find shifts]**
>
> Once that's complete, you can book as many `{{CLIENT_NAME}}` shifts as are available.

---

### Step 1B — Active Users: Initial Outreach (Email)
**Channel:** Email
**Goal:** Complete compliance (drug test) and unlock more shifts

> **Subject Line:** Want to see even more `{{ROLE_TYPE}}` shifts?
>
> **Pre-header:** Earn more — work for `{{CLIENT_NAME}}`
>
> **Header:** New shifts available
>
> **Body:**
> Hi [First Name],
>
> Want to see even more `{{ROLE_TYPE}}` shifts in your area?
>
> `{{CLIENT_NAME}}` has brand-new shifts, paying up to `{{PAY_RATE}}`/hr.
>
> If you've completed your standard Drug Test, you can book any available shifts now. If you haven't had your Drug Test, please go to the app and complete your `{{CLIENT_NAME}}` onboarding.
>
> To get started, simply 'Browse Jobs', tap an '`{{UPSKILLING_SHIFT_NAME}}`' shift, and you'll be shown how to complete the test.
>
> **[Find shifts]**
>
> Once that's complete, you can book as many `{{CLIENT_NAME}}` shifts as are available.

---

### Step 2A — All Users: SMS Follow-up
**Channel:** SMS
**Audience:** All users (active + inactive) who have not completed drug test

> Hi [First Name], brand-new `{{CLIENT_NAME}}` shifts in your area.
> Drug test complete? Then book.
> If not, please complete your `{{CLIENT_NAME}}` onboarding in the app.
>
> Shifts pay up to `{{PAY_RATE}}`/hr.
> Book test here: `{{APP_DEEPLINK}}`

---

### Step 2B — Inactive Users: SMS Variant
**Channel:** SMS

> Hi [First Name], fancy booking new `{{CLIENT_NAME}}` shifts through Flex? Had your Drug Test? Then book.
> If not, please complete your `{{CLIENT_NAME}}` onboarding in the app.
>
> Shifts pay up to `{{PAY_RATE}}`/hr. Book test here: `{{APP_DEEPLINK}}`

---

### Step 3A — Active Users: Push Notification
**Channel:** Push Notification

> Brand-new `{{ROLE_TYPE}}` shifts!
> Open up even more shifts, with `{{CLIENT_NAME}}`.
> If you've had your Drug Test, book now. If not, please complete your `{{CLIENT_NAME}}` onboarding in the app.
> Simply go to 'Browse Jobs' and tap an `{{UPSKILLING_SHIFT_NAME}}` shift to begin.

---

### Step 3B — Active Users: In-App Message
**Channel:** In-App Message

> Work for `{{CLIENT_NAME}}`
> Want brand-new `{{ROLE_TYPE}}` shifts? Complete your Drug Test. See app for more details.

---

### Step 3C — Inactive Users: Push Notifications (2 variants)
**Channel:** Push Notification — Variant A

> Want new shifts through Flex?
> It's been a while, but you can access brand-new `{{ROLE_TYPE}}` shifts with `{{CLIENT_NAME}}`, if you take their `{{DRUG_TEST_TYPE}}` drug test.
> Tap to book.

**Push Notification — Variant B**

> New shifts to come back to.
> Take `{{CLIENT_NAME}}`'s `{{DRUG_TEST_TYPE}}` drug test and you can access all of their available shifts. Tap to book.

---

## Key Variables to Replace

| Variable | Description |
|---|---|
| `{{CLIENT_NAME}}` | Client requiring compliance (e.g., CORT) |
| `{{MARKET}}` | Target market (e.g., Las Vegas, NV) |
| `{{ROLE_TYPE}}` | Role being staffed (e.g., Loader/Crew) |
| `{{PAY_RATE}}` | Pay rate (e.g., $18) |
| `{{DRUG_TEST_TYPE}}` | Type of drug test (e.g., 9-panel) |
| `{{UPSKILLING_SHIFT_NAME}}` | Shift name in Browse Jobs (e.g., "Indeed Flex Upskilling Loader Crew") |
| `{{APP_DEEPLINK}}` | Indeed Flex app deep link |
| `{{AUDIENCE_LIST_LINK}}` | Link to Redash or audience spreadsheet |

## Notes
- This template is designed for **round 2+** of compliance campaigns (first round already ran)
- Can be adapted for any client requiring specific certifications, not just drug tests
- Replace `{{DRUG_TEST_TYPE}}` with certification type if applicable (e.g., food handler card, background check)

---
*Source: CORT Compliance Reengagement CRM Brief — Las Vegas, NV — March 2026*
*Template saved by Relay (CRM Specialist) — recruitment-marketing-flex squad*
