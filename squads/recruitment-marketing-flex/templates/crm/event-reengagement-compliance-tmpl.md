# CRM Template: Event Reengagement — Compliance & Booking

**Case:** SXSW 2026 (March 2026, Austin TX)
**Use for:** Large-scale events requiring worker compliance + booking campaigns
**Type:** Multi-channel reengagement (Email + SMS + Push + In-App)

---

## Brief Structure

| Field | Description |
|---|---|
| **Objective** | Re-engage existing [ROLE] marketplace to complete compliance and book shifts for [EVENT NAME] |
| **Campaign Goal** | Complete compliance and book a shift |
| **Primary Metric** | Compliance completion rate |
| **Additional Metrics** | Booking rate, SMS click-through, email open rate |

---

## Audience Segmentation

| Segment | Definition | Size Reference | % of Reachable |
|---|---|---|---|
| **Active** | Completed a shift in last 15 days OR logged in within last 3 days | ~15% | Smallest |
| **Lapsing** | No shift in 15+ days OR no login in 3–90 days | ~55% | Largest — priority |
| **Dormant** | No shift or login in 90+ days | ~60% | Re-engagement play |

**Geographic filter:** Within [X] miles of [CITY] city center, active in last 365 days, verified for [ROLE].

---

## Compliance Requirements (fill per event)

- [ ] [SKILL/CERTIFICATION NAME] — e.g., watch training video + quiz
- [ ] [REQUIREMENT 2] — e.g., enter t-shirt size
- [ ] [REQUIREMENT 3] — e.g., age verification (21+ if alcohol venue)
- [ ] [REQUIREMENT 4] — e.g., consent to share phone number

---

## Sequence Map

| Segment | Step | Channel | Goal |
|---|---|---|---|
| Lapsing + Dormant | Initial Outreach | Email | Complete compliance + book shift |
| Lapsing + Dormant | Triggered Follow-up (+24h) | SMS | Complete compliance + book shift |
| Active | Initial Awareness | Push Notification | Open app |
| Active | On-Entry Engagement | In-App Message | Complete compliance + book shift |
| All Non-Responders | Follow-up Reminder | Email | Complete compliance + book shift |
| All Non-Responders | Final Push | SMS | Complete compliance + book shift |

---

## Email Templates

### Email 1 — Active Users / Initial (Launch: [DATE])

**Subject:** Want to work at [EVENT NAME]?
**Pre-header:** Be part of something big — earn up to $[RATE]/hr
**Header:** Take our quick, free training

**Body:**
```
Hi [First Name],

[EVENT NAME] is coming up, and you could work there!

They need skilled [ROLE] pros to cover the whole [DURATION]. Take our free training to access all shifts.

Simply hop onto the Flex app and:
1. Search '[EVENT NAME] [ROLE]'
2. Tap 'Start Onboarding'
3. Watch the training video in full
4. Take the quiz that follows
5. [ADDITIONAL COMPLIANCE STEPS]

[CTA: Start Now]
```

---

### Email 2 — Active Non-Responders (+48h after Email 1)

**Subject:** There's still time to be part of [EVENT NAME]!
**Pre-header:** Earn up to $[RATE]/hr | See the [EVENT TYPE], get paid!
**Header:** Take our quick, free training

**Body:**
```
Hi [First Name],

[EVENT NAME] is just around the corner, which means we've got exciting [ROLE] roles available throughout [DATES].

They're looking for staff to cover [ACTIVITIES] — paying up to $[RATE]/hr.

Want to be part of it?

All you have to do to access shifts is take our quick training and quiz.

To get started simply tap below and search for '[EVENT NAME] [ROLE]', then follow the steps below.

[CTA: Start Training]

Steps:
1. Tap 'Start Onboarding'
2. Watch the training video in full
3. Take the quiz that follows
4. [ADDITIONAL STEPS]
```

---

### Email 3 — Lapsing/Dormant Users / Initial

**Subject:** Come back and cover [EVENT NAME]! / Don't miss exclusive [EVENT NAME] shifts!
**Pre-header:** Be part of something big! / See the event — earn up to $[RATE]/hr!
**Header:** Take our quick, free training

**Body:**
```
Hi [First Name],

It's [EVENT NAME] season in [CITY] again, which means exclusive shifts are available right across [DATES].

They're looking for [ROLE] like you — paying up to $[RATE]/hr, covering [ACTIVITIES].

You can access these shifts by completing our quick, free training.

Simply click below, search '[EVENT NAME]', and follow the steps underneath:

[CTA: Start Training]

Steps:
1. Tap 'Start Onboarding'
2. Watch the training video in full
3. Take the quiz that follows
4. [ADDITIONAL STEPS]
```

---

## SMS Templates

### SMS 1 — Active/Lapsing (paired with Email 1)

```
Hi {{${first_name} | default: 'Flexer' | capitalize}}, still time to land those exclusive [EVENT NAME] shifts, paying up to $[RATE]/hr.

Be part of something big! Take your free training to access them ASAP! Search '[EVENT NAME] [ROLE]' in the app to begin: [DEEP LINK]

Indeed Flex
Reply STOP to unsubscribe.
```

### SMS 2 — Lapsing/Dormant Non-Responders (+24h)

```
Flex Alert: [EVENT NAME] is here again! And they're looking for [ROLE] across the [DURATION] — paying up to $[RATE]/hr! Take our free training to access shifts.

Tap the link below and search '[EVENT NAME]' to get started: [DEEP LINK]

Indeed Flex
Reply STOP to unsubscribe.
```

---

## Push Notification Template

**Header:** Want to work at [EVENT NAME]?
**Body:** The [EVENT TYPE] is coming up, and you could work there! Just take our free training. See app for info.

---

## Placeholders Reference

| Placeholder | Description |
|---|---|
| `[EVENT NAME]` | e.g., SXSW 2026 |
| `[ROLE]` | e.g., Event Staff |
| `[DATES]` | e.g., March 9–18 |
| `[DURATION]` | e.g., two weeks |
| `[CITY]` | e.g., Austin, TX |
| `[RATE]` | e.g., 18 |
| `[ACTIVITIES]` | e.g., concerts, live talks, movies |
| `[DEEP LINK]` | e.g., https://indeedflex.onelink.me/4jvh/flexbrowsejobsusa |

---

*Source: SXSW 2026 - Reengagement Compliance and Booking CRM Brief*
*Template created: 2026-03-20 | Squad: recruitment-marketing-flex*
