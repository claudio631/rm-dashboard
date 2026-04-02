# CRM Copy Base Template
<!-- Generic multi-step communication template — use as starting point for any campaign -->
<!-- Source: Indeed Flex CRM Template (UK base) — adapted for US market -->

## Campaign Brief

| Field | Value |
|---|---|
| **Proposition** | `[PROPOSITION — e.g., $10 bonus, compliance unlock, NHO invite]` |
| **Goal / Impact** | `[What changes as a result — e.g., Higher shift fulfilment]` |
| **Audience** | `[Who — e.g., Verified for bartender/waiting staff, US market]` |
| **Channel** | `[Email / SMS / Push / In-App]` |
| **Planned Launch Date** | `[Date]` |

---

## Step 1 — Initial Outreach

**Proposition:** `[Primary value offer]`
**Audience:** `[Segment — e.g., Active, Lapsing, Dormant]`
**Channel:** `[Email / SMS / Push / In-App]`
**Launch Date:** `[Date]`

> **Subject Line:** `[Subject line here]`
> **Pre-header:** `[Pre-header text here]`
> **Header:** `[Email header / push title]`
>
> **Body:**
> Hi [First Name],
>
> `[Opening — acknowledge where they are or what's available]`
>
> `[Value proposition — what's in it for them]`
>
> `[Call to action instruction — clear, simple, 1 step]`
>
> `[Supporting detail — what happens next, reassurance]`
>
> **[CTA Button Text]**
>
> `[Sign-off]`
> `[Team name]`

---

## Step 2 — Follow-up / Non-Responders (48–72h after Step 1)

**Proposition:** Same offer, different angle
**Audience:** Non-responders from Step 1
**Channel:** `[Email / SMS — choose different from Step 1 where possible]`
**Launch Date:** 48–72h after Step 1

> **Subject Line:** `[Urgency or curiosity angle]`
> **Pre-header:** `[Reinforce benefit]`
>
> **Body:**
> Hi [First Name],
>
> `[Acknowledge time passing — "still time", "don't miss out"]`
>
> `[Restate value proposition briefly]`
>
> `[Simplify the action — make it feel easy]`
>
> **[CTA Button Text]**

---

## Step 3 — Final Push (24–48h before deadline)

**Proposition:** Urgency + last chance
**Audience:** All non-converters
**Channel:** SMS (highest open rate for urgency)
**Launch Date:** `[Date — close to deadline]`

> `[SHORT SMS FORMAT]`
> Hi {{${first_name} | default: 'Flexer' | capitalize}}, `[value offer in 1 sentence]`.
> `[Simple action]`: `[LINK]`
> Indeed Flex — Reply STOP to unsubscribe.

---

## Copy Best Practices Checklist

Before submitting to CRM:

- [ ] Subject line < 50 characters
- [ ] Pre-header extends (not repeats) the subject line
- [ ] First line of body is not "I hope this email finds you well"
- [ ] Single CTA per message
- [ ] Personalization token used: `{{${first_name} | default: 'Flexer' | capitalize}}`
- [ ] SMS includes "Reply STOP to unsubscribe"
- [ ] Deep link tested and working
- [ ] Audience list attached or definition is thorough
- [ ] Sign-off is consistent (Indeed Flex Team / Team Flex)

---

## Audience Segment Reference

| Segment | Definition | Best Channel |
|---|---|---|
| **Active** | Shift in last 15 days OR login in last 3 days | Push → In-App |
| **Lapsing** | No shift 15+ days OR login 3–90 days ago | Email → SMS |
| **Dormant** | No shift or login in 90+ days | Email → SMS |
| **Non-responders** | Did not open/click previous step | SMS (48h after email) |

---

## Braze Personalization Tokens

| Token | Output |
|---|---|
| `{{${first_name} \| default: 'Flexer' \| capitalize}}` | Personalized first name or "Flexer" |
| `{{custom_attribute.${job_pay_rate}}}` | Pay rate from profile |
| `{{custom_attribute.${preferred_location}}}` | Worker's preferred location |

---

*Base template — adapt for each campaign*
*Template saved by Relay (CRM Specialist) — recruitment-marketing-flex squad*
