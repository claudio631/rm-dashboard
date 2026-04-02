# CRM Template: New Hire Orientation (NHO)

**Case:** Stord Atlanta NHO — Picker Packer recurring orientations
**Use for:** Any client requiring a New Hire Orientation before workers can begin regular shifts
**Type:** Multi-channel (Email + SMS), ready-to-pull template with fill-in-the-blank fields
**Process:** Pull updated list → submit to CRM → send on NHO announcement (48h+ notice)

---

## Brief Structure

| Field | Description |
|---|---|
| **Objective** | Develop ready-to-go templates for [CLIENT] NHOs so comms can be sent quickly when orientations are posted |
| **Campaign Goal** | Reserve NHO spot |
| **Primary Metric** | NHO registration/booking rate |
| **Cadence** | 1 email + 1 SMS per NHO opening; review after 4–5 sends |

---

## Audience Segments

| Segment | Definition |
|---|---|
| **Previously worked [CLIENT]** | Worked for client, not within last 90 days, eligible to return |
| **Never worked [CLIENT]** | Verified for [ROLE], no prior [CLIENT] experience |

**Geographic:** [CITY/MARKET], active in Flex platform
**Source:** Pull from Redash — provide link when submitting CRM request

---

## Process Flow

```
48h before NHO posted → Pull updated Redash list →
Submit CRM request (#marketing-requests-new) →
CRM sends templated comms → Track NHO fill rate
```

---

## Email Templates

### Email 1 — Initial Outreach

**Subject:** New [CLIENT] Shifts Are Live — Orientation Spots Open
**Pre-header:** Whether you've worked with [CLIENT] before or not, this is your shot.

**Body:**
```
Hi [First Name],

We've got new shifts opening up at [CLIENT], and you're invited to take the first step by attending our upcoming New Hire Orientation (NHO).

✅ Never worked at [CLIENT]? This gets you eligible for upcoming shifts.
✅ Worked there before? If it's been more than 90 days, you're eligible to return and attend an NHO again!

We're currently hiring for the [INSERT ROLE], with [INSERT SHIFT INFO] starting [INSERT DATE].

Bonus Alert: Earn a tiered shift completion bonus when you complete orientation and your first few shifts — more shifts, more $$$ in your pocket!

👉 [CTA: Reserve Your Spot Now]

See you there,
The Indeed Flex Team
```

---

### Email 2 — Second Outreach / Different Angle

**Subject:** Be Shift-Ready for [CLIENT] — Join Our Next NHO
**Pre-header:** Time to gear up for shifts at [CLIENT].

**Body:**
```
Hey [First Name],

We're kicking off another New Hire Orientation (NHO) for [CLIENT], and whether you're new to the [FACILITY TYPE] or returning after some time away, you're welcome to join.

📌 Hiring for: [INSERT ROLE]
📅 Start Date: [INSERT DATE]
🕒 Shifts: [INSERT SHIFT INFO]

Already worked with [CLIENT]? If it's been 90+ days, you can return and get started again through this NHO.

Earn More as You Go: Complete orientation and start picking up shifts to unlock a tiered bonus payout. The more you work, the more you earn!

👉 [CTA: Book Your NHO]

Let's do this,
The Indeed Flex Team
```

---

### Email 3 — Final Push / Bonus Emphasis

**Subject:** Jump Into [CLIENT] Shifts — Sign Up for NHO Today
**Pre-header:** All roads to [CLIENT] start here.

**Body:**
```
Hi [First Name],

New Bonus Opportunity! You'll now earn a tiered bonus just for showing up and working your first few shifts after orientation.

[CLIENT] is ramping up again, and we've opened up New Hire Orientation (NHO) to get qualified Flexers shift-ready.

Whether you're brand new to [CLIENT] or have worked there in the past, this is your chance. If you've previously worked with [CLIENT] but it's been more than 90 days, you're welcome to return by completing another NHO.

We're hiring for [INSERT ROLE] with [INSERT SHIFT INFO] starting [INSERT DATE].

Secure your spot and get first dibs on great-paying shifts.

👉 [CTA: Sign Up Now]

The Indeed Flex Team
```

---

### Email 4 — Operational Detail Version (Shift-Specific)

**Subject:** New [CLIENT] shifts — orientation spots now open
**Pre-header:** Book yours now so you can start working with them!

**Body:**
```
Hello {{${first_name} | default: 'Flexer' | capitalize}},

We have new [INSERT ROLE] Induction shifts, starting [INSERT DATE TIME].

This shift will serve as your First Day Orientation at [CLIENT]. Once you complete this, you'll be assigned to your long-term booking. Please be prepared to work the full day on the day of orientation.

Important Details:
💰 Pay: [INSERT PAY RATE]/hour
🍱 Lunch: [INSERT LUNCH INFO]
👕 Dress: [INSERT DRESS CODE]
🪪 ID Required: [INSERT ID REQUIREMENTS]

Limited spots available! Click below to book your shift and get started right away!
```

**CTA:** Book shift → [DEEP LINK]

---

## SMS Templates

### SMS 1 — Initial Outreach

```
📢 [CLIENT] is hiring in [CITY]! New Hire Orientation for [INSERT ROLE] on [INSERT DATE].
✅ New to [CLIENT]? Get started.
✅ Worked before (90+ days ago)? You're eligible to return!
Reserve your spot now: [SHORT-LINK]
💰 Tiered bonus available after NHO + shifts — earn more the more you work!
```

### SMS 2 — Shift Details Focused

```
[CLIENT] New Hire Orientations are live! We're hiring for [INSERT ROLE] with [INSERT SHIFT INFO] starting [INSERT DATE]. We are also including a new tiered bonus when you finish NHO + shifts. More shifts = more cash 💸
New or returning after 90+ days? You are eligible to attend.
Book here: [SHORT-LINK]
```

### SMS 3 — Urgency + Bonus

```
Want shifts at [CLIENT]? Attending a New Hire Orientation is required.
📍 [INSERT ROLE], starts [INSERT DATE]
✅ New to [CLIENT] or returning after 90 days? You're in!
✅ Complete NHO + shifts & earn a tiered bonus! A little extra to get you started 🚀
Lock in your spot: [SHORT-LINK]
```

### SMS 4 — Non-Openers (Short)

```
Hello {{${first_name} | default: 'Flexer' | capitalize}}, we have [INSERT ROLE] Orientation shifts available at [CLIENT], starting on [INSERT DATE], paying $[RATE]/hour!
Spots are limited, so book this shift quickly! [DEEP LINK]
Reply STOP to unsubscribe
```

---

## Bonus Structure Reference

| Tier | Condition | Reward |
|---|---|---|
| Tier 1 | Complete NHO | Base bonus |
| Tier 2 | Complete NHO + 1st shift | + $[AMOUNT] |
| Tier 3 | Complete NHO + [X] shifts | + $[AMOUNT] |

*(Fill in actual bonus amounts per client agreement)*

---

## Placeholders Reference

| Placeholder | Description |
|---|---|
| `[CLIENT]` | e.g., Stord, Amazon, CORT |
| `[INSERT ROLE]` | e.g., Picker Packer, Loader/Crew |
| `[INSERT DATE]` | NHO date |
| `[INSERT DATE TIME]` | NHO date + start time |
| `[INSERT SHIFT INFO]` | e.g., Mon–Fri, 6am–2pm |
| `[INSERT PAY RATE]` | e.g., $16 |
| `[INSERT LUNCH INFO]` | e.g., Bring your own — nearest restaurant is 20 min away |
| `[INSERT DRESS CODE]` | e.g., Facility is not climate-controlled, dress comfortably |
| `[INSERT ID REQUIREMENTS]` | e.g., Government-issued ID required |
| `[CITY/MARKET]` | e.g., Atlanta, GA |
| `[FACILITY TYPE]` | e.g., warehouse, distribution center |
| `[DEEP LINK]` | https://indeedflex.onelink.me/4jvh/flexbrowsejobsusa |
| `[SHORT-LINK]` | Shortened deep link for SMS |
| `[RATE]` | Hourly pay rate |

---

*Source: Stord NHO CRM Brief — Atlanta, GA*
*Template created: 2026-03-20 | Squad: recruitment-marketing-flex*
