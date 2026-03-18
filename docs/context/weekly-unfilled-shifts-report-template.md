# Weekly Unfilled Shifts — Focus Points of Action

> **Template version:** 1.1 · **Created by:** Atlas (@analyst) · **Updated:** 2026-03-17
>
> **How to use:** Export the week's shift CSV from ACP. Paste into your analysis tool. Use this template to structure your output each week. Replace all `[PLACEHOLDER]` values.
>
> **Important:** Exclude all shifts where the brand/company is **"Indeed Flex Application"** — these are dummy shifts created for onboarding purposes and are intentionally unfilled. Only count real client venue shifts.

---

## Data Prep — What to Exclude

Before counting unfilled shifts, filter out:

| Pattern | Reason |
|---------|--------|
| `[Role] Jobs in [City, State]` | Indeed Flex dummy shifts — open market postings for onboarding |
| `[City] - [Role] Jobs` | Same as above (reversed format) |
| `[Type] jobs in [City]` | Same (lowercase variant) |
| `Loader/Crew Jobs in [City]` | Same |
| `Clerical in [City]` | Same |
| `[Venue] — Orientation` / `Tour/Orientation` | Onboarding orientation dummy slots |

**Do count:** Named client venues — hub codes (ATL1, CVG1, HNJ001), warehouse addresses, stadium/event venues.

---

## Week of [START DATE] – [END DATE]

**Report generated:** [DATE] · **Source:** `[Shift CSV filename]`

---

## 1. Weekly Snapshot

| Metric | Count |
|--------|------:|
| Total real shifts (dummy excluded) | [X] |
| Filled | [X] |
| **Unfilled** | **[X]** |
| **True fill rate** | **[X]%** |

### Unfilled by Day

| Date | Day | Unfilled | vs. Prior Week |
|------|-----|:--------:|:--------------:|
| [DATE] | Mon | [X] | [±X] |
| [DATE] | Tue | [X] | [±X] |
| [DATE] | Wed | [X] | [±X] |
| [DATE] | Thu | [X] | [±X] |
| [DATE] | Fri | [X] | [±X] |
| [DATE] | Sat | [X] | [±X] |
| [DATE] | Sun | [X] | [±X] |

---

## 2. CRITICAL — Persistent Daily Gaps

> Venues unfilled on 5+ of 7 days. Structural fill problems — not one-offs.

### 🔴 Tier 1 — Every Day (7/7)

| Venue | Owner | Role(s) | Shift Time | Daily Avg | Total |
|-------|-------|---------|-----------|:---------:|:-----:|
| [VENUE] | [Craig/Claudio] | [ROLE] | [TIME] | [X] | [X] |

**Actions:**
- [ ] Braze re-engagement: verified workers not booked in 14+ days for this market
- [ ] Confirm job posting is live and searchable in FHS + app
- [ ] Check incentive status — is a sign-on bonus active?
- [ ] Consider dummy shift creation in ACP to surface availability

### 🟠 Tier 2 — Most Days (5–6/7)

| Venue | Owner | Role(s) | Shift Time | Days | Total |
|-------|-------|---------|-----------|:----:|:-----:|
| [VENUE] | [Craig/Claudio] | [ROLE] | [TIME] | [X/7] | [X] |

---

## 3. TODAY / TOMORROW — Immediate Dispatch

> Shifts starting within 24–48 hours, still unfilled. Act now.

| Venue | Role | Shift Time | Unfilled | Owner |
|-------|------|-----------|:--------:|-------|
| [VENUE] | [ROLE] | [TIME] | [X] | [Craig/Claudio] |

---

## 4. Venue-by-Venue Breakdown

> All real client venues, sorted by total unfilled. Use day columns to spot patterns (daily = structural, spike = demand event).

| Venue | Owner | Roles | Times | Mon | Tue | Wed | Thu | Fri | Sat | Sun | Total |
|-------|-------|-------|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:-----:|
| [VENUE] | [C/K] | [ROLES] | [TIMES] | — | — | — | — | — | — | — | [X] |

**Key:** C = Craig · K = Claudio · — = 0 unfilled · ⚠️ = 5+ unfilled

---

## 5. Role Shortage Summary

| Role | Unfilled | Venues | Action |
|------|:--------:|:------:|--------|
| Warehouse Operative | [X] | [X] | Platform Verified → Booked re-engagement |
| Picker Packer | [X] | [X] | "Shifts available near you" push |
| Forklift Driver | [X] | [X] | Certified worker re-engagement (niche pool) |
| Assembler | [X] | [X] | Venue-specific targeted campaign |
| Material Handler | [X] | [X] | — |
| Loader / Crew | [X] | [X] | Event-day direct outreach |

---

## 6. Action Checklist

### Today

- [ ] **[VENUE]** — [X] [ROLE] unfilled — [ACTION]

### This Week

- [ ] **[VENUE]** — [ACTION]

### Watch List (escalate if unresolved by [DATE])

- [ ] **[VENUE]** — [RISK DESCRIPTION]

---

## 7. Notes & Observations

- [NOTE]

---

*Template: `docs/context/weekly-unfilled-shifts-report-template.md` · Atlas (@analyst)*

---
---

# EXAMPLE: Week of 17 Mar – 25 Mar 2026

> **Source:** `shifts (4).csv` — 3,828 total rows · **Generated:** 2026-03-17 · Atlas (@analyst)
>
> **Dummy shifts excluded:** 1,471 rows (Indeed Flex Application branded postings + orientation slots).
> Of those, 1,465 were unfilled — as expected for dummy/onboarding shifts.

---

## 1. Weekly Snapshot

| Metric | Count |
|--------|------:|
| Total real shifts (dummy excluded) | 2,357 |
| Filled | 1,532 |
| **Unfilled** | **825** |
| **True fill rate** | **65.0%** |

### Unfilled by Day

| Date | Day | Unfilled |
|------|-----|:--------:|
| 17 Mar | Mon | 11 |
| 18 Mar | Tue | 93 |
| 19 Mar | Wed | 110 |
| 20 Mar | Thu | 102 |
| 21 Mar | Fri | 93 |
| 22 Mar | Sat | 78 |
| 23 Mar | Sun | 126 |
| 24 Mar | Mon | 123 |
| 25 Mar | Tue | 89 |

> 17 Mar (today) is low — data pulled mid-day, most shifts already dispatched.

---

## 2. CRITICAL — Persistent Daily Gaps

### 🔴 Tier 1 — Every Day (9/9 days)

| Venue | Owner | Role(s) | Shift Time | Daily Avg | Total |
|-------|-------|---------|-----------|:---------:|:-----:|
| ATL1 | Craig | Forklift Driver (84%) | 20:00–04:30 (primary) | 6 | **56** |

**ATL1 detail:** 47 Forklift Drivers + 5 Picker Packers + 4 Warehouse Operatives. Night shift 20:00–04:30 accounts for 63% of gaps. Forklift certification is the bottleneck — there are not enough credentialed workers in the Atlanta pipeline.

**Actions:**
- [ ] Braze: re-engage all Atlanta verified workers with forklift certification not booked in 14 days
- [ ] Confirm ATL forklift job posting is visible in the app (FHS + Indeed)
- [ ] Check ATL1 incentive: is a bonus active for Forklift Driver role?
- [ ] Review Atlanta Forklift Driver Indeed Ads budget — ATL is at 15.1% CR so funnel exists, booking is the gap

### 🟠 Tier 2 — Most Days (7–8/9)

| Venue | Owner | Role(s) | Primary Shift Time | Days | Total |
|-------|-------|---------|-------------------|:----:|:-----:|
| PowerStop Bedford Park | Craig | Picker Packer + Warehouse Operative | 06:00–14:30 / 15:00–01:30 | 8/9 | **249** |
| TX - Branch 157 (700 Lakeside) | Craig | Warehouse Operative | 06:00–14:30, 15:00–23:30, 23:45–05:30 | 8/9 | **66** |
| Nashville HTN001 | Craig | Warehouse Operative | 14:00–22:00 (primary) | 7/9 | **100** |
| CVG1 | Craig | Picker Packer | 06:30–15:00 | 7/9 | **65** |
| West Chester (8531 Trade Center) | Craig | Assembler | 07:00–15:00 | 7/9 | **62** |

**PowerStop Bedford Park** is the single largest gap: 249 unfilled (130 Picker Packers + 104 Warehouse Operatives). All 3 shifts affected — AM (06:00–14:30), PM (15:00–01:30), and a shorter mid-shift (14:00–22:30).

---

## 3. TODAY / TOMORROW — Immediate Dispatch (18–19 Mar)

| Venue | Role | Shift Time | Unfilled | Owner |
|-------|------|-----------|:--------:|-------|
| Logan Township HNJ001 | Warehouse Operative | 06:00–13:00 | **40** | Craig |
| PowerStop Bedford Park | Picker Packer + WO | 06:00–14:30 / 15:00–01:30 | **38** | Craig |
| TX - Branch 157 | Warehouse Operative | All 3 shifts | **22** | Craig |
| CVG1 | Picker Packer | 06:30–15:00 | **21** | Craig |
| West Chester | Assembler | 07:00–15:00 | **20** | Craig |
| ATL1 | Forklift Driver | 20:00–04:30 | **17** | Craig |
| Power Stop - Hodgkins | Warehouse Operative | 14:30–23:00 / 05:30–15:00 | **9** | Craig |
| DAL - AT&T Stadium | Loader / Crew | 08:30–18:30 | **10** | Craig |
| NSH - Music City Center | Loader / Crew | 08:00–17:30 | **5** | Craig |
| Soho House Austin | Hospitality General Labor | 18:00–02:00 | **1** | Claudio |

> AT&T Stadium (18 Mar) and Music City Center (19 Mar) are event-specific — single-day dispatch window.

---

## 4. Venue-by-Venue Breakdown

| Venue | Owner | Roles | Times | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | Total |
|-------|-------|-------|-------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:-----:|
| PowerStop Bedford Park | Craig | Picker Packer, WO | 06:00–14:30, 15:00–01:30 | — | 30 | 8 | 6 | 45 | 47 | 43 | 41 | 29 | **249** |
| Logan Township HNJ001 | Craig | Warehouse Operative | 06:00–13:00 | — | — | 40 | 40 | 39 | — | — | — | — | **119** |
| Nashville HTN001 | Craig | Warehouse Operative | 14:00–22:00, 18:00–23:30 | — | — | 3 | 3 | 1 | 22 | 26 | 29 | 16 | **100** |
| TX - Branch 157 | Craig | Warehouse Operative | 06:00–14:30, 15:00–23:30, 23:45–05:30 | 3 | 11 | 11 | 8 | — | 3 | 11 | 11 | 8 | **66** |
| CVG1 | Craig | Picker Packer | 06:30–15:00 | — | 10 | 11 | 9 | — | 2 | 11 | 11 | 11 | **65** |
| West Chester (8531) | Craig | Assembler, Forklift | 07:00–15:00 | 2 | 10 | 10 | 10 | — | — | 10 | 10 | 10 | **62** |
| ATL1 | Craig | Forklift Driver (84%) | 20:00–04:30, 07:00–15:30 | 5 | 9 | 8 | 8 | 6 | 1 | 8 | 8 | 3 | **56** |
| IL - Branch 189 (Great Lakes) | Craig | Material Handler | 06:00–14:30 | — | — | 3 | 3 | — | — | 3 | 3 | 3 | **15** |
| Power Stop - Hodgkins | Craig | WO, Overbook-WO | 14:30–23:00, 05:30–15:00 | — | 5 | 4 | 5 | — | — | — | — | — | **14** |
| Lancaster | Craig | Forklift Driver | 10:00–14:00 | — | — | — | 3 | — | — | 3 | 3 | 3 | **12** |
| TX - Haslet Branch 216 | Craig | Warehouse Operative | 06:00–14:30, 23:45–05:30 | 1 | 2 | 2 | 1 | — | — | 2 | 2 | 1 | **11** |
| DAL - AT&T Stadium | Craig | Loader / Crew | 08:30–18:30 | — | 10 | — | — | — | — | — | — | — | **10** |
| Fairfield - 420 Distribution | Craig | Warehouse Operative | 07:00–15:00 | — | 2 | 1 | 2 | — | — | 1 | 1 | 1 | **8** |
| C7500 - Irving TX | Craig | Assembler | 06:30–15:00 | — | 1 | 1 | 1 | — | — | 1 | 1 | 1 | **6** |
| 10132 Business Center (Tennant) | Craig | Warehouse Operative | 07:00–15:30 | — | — | 2 | 1 | — | — | 1 | 1 | 1 | **6** |
| LaVergne - Distribution | Craig | Warehouse Operative | 07:00–15:30 | — | — | — | 2 | — | 2 | 2 | — | — | **6** |
| NSH - Music City Center | Craig | Loader / Crew | 08:00–17:30 | — | — | 5 | — | — | — | — | — | — | **5** |
| Cardinal Paint Warehouse | ? | Industrial General Labor | 10:00–20:30 | — | 1 | 1 | — | — | — | 1 | 1 | 1 | **5** |
| Paulsboro, NJ (BNJ003) | Craig | Warehouse Operative | 00:30–07:30 | — | — | — | — | 2 | 1 | 1 | — | — | **4** |
| Flex Assurant | ? | Forklift Driver | 16:30–03:00 | — | — | — | — | — | — | 1 | 1 | 1 | **3** |
| Cleveland, OH (BOH005) | Craig | Warehouse Operative | 03:00–08:30 | — | 1 | — | — | — | — | — | — | — | **1** |
| Soho House Austin | Claudio | Overbook - Hosp. General Labor | 18:00–02:00 | — | 1 | — | — | — | — | — | — | — | **1** |
| CTDI Grove City | Craig | Material Handler | 07:00–15:30 | — | — | — | — | — | — | 1 | — | — | **1** |

**Key:** — = 0 unfilled · ? = confirm market owner

> **Logan Township pattern:** Gaps cluster Wed–Fri (19–21 Mar) only. Likely tied to a weekly contract volume spike — not a persistent structural problem. Monitor next week before escalating.
>
> **Nashville pattern:** Back-loaded (Sat 22 – Tue 25). PM shift (14:00–22:00) dominates. Weekend demand spike, not a Monday–Friday issue.
>
> **PowerStop:** Unusual spike on Fri–Sun (21–23 Mar) — 45, 47, 43 unfilled vs. single-digits earlier in the week. Possible demand increase or cancellation wave mid-week.

---

## 5. Role Shortage Summary

| Role | Unfilled | Venues Affected | Action |
|------|:--------:|:---------------:|--------|
| **Warehouse Operative** | **432** | 14 | Platform Verified → Booked Braze re-engagement; largest lever |
| **Picker Packer** | **200** | 3 | PowerStop + CVG1 dominant; "shifts near you" push |
| **Forklift Driver** | **68** | 4 | ATL1 + Lancaster + Assurant; certified worker pool is small — may need dedicated recruiting |
| **Assembler** | **62** | 2 | West Chester + Irving; venue-specific sourcing |
| **Material Handler** | **16** | 2 | IL Branch 189 + CTDI Grove City |
| **Loader / Crew** | **11** | 2 | AT&T Stadium + Music City Center — event-day dispatch |

> **Warehouse Operative** alone is 52% of all real unfilled shifts. Any re-engagement campaign targeting this role has the highest single impact on fill rate.

---

## 6. Action Checklist

### Today (18 Mar)

- [ ] **ATL1** — Braze push: Atlanta verified forklift-qualified workers not booked in 14 days (night shift focus)
- [ ] **Logan Township HNJ001** — 40 Warehouse Operatives needed Wed–Fri (19–21 Mar). Confirm NJ market active worker pool; check Braze last send date
- [ ] **DAL - AT&T Stadium** — 10 Loader/Crew for today's event (08:30–18:30). Direct dispatch to Dallas active Flexers
- [ ] **NSH - Music City Center** — 5 Loader/Crew for tomorrow (19 Mar). Nashville active Flexers dispatch

### This Week

- [ ] **PowerStop Bedford Park** — 249 total unfilled (largest gap). Escalate to Craig: spike on Fri 21–Sun 23 (45–47/day) suggests demand surge or cancellation wave. Check client headcount request vs. available pool
- [ ] **Nashville HTN001** — PM + weekend shift gaps (22–25 Mar). Braze "shifts available" push targeting Nashville WO workers verified but not booked
- [ ] **CVG1** — 65 Picker Packers unfilled Mon–Wed. Cincinnati is at 18.3% CR — strong funnel. Booking gap, not sourcing. Trigger "shifts available near you" re-engagement
- [ ] **West Chester** — 56 Assemblers unfilled daily. Assembler is a specific skill set. Review West Chester pipeline: are enough Assembler-role verified workers in the pool?
- [ ] **TX Branch 157** — All 3 shifts unfilled every day. Check if Dallas requisitions are fully open and if Dallas Warehouse Operative campaign is active (Dallas at 10.8% CR — high priority market)

### Watch List (flag if unresolved by 21 Mar)

- [ ] **ATL1 Forklift Driver** — 9 consecutive days unfilled. If still unresolved by EOW, request dedicated certified forklift worker acquisition campaign for Atlanta
- [ ] **PowerStop Bedford Park** — If >150 remain unfilled after 21 Mar, escalate to operations: available Flexer pool may be exhausted; over-rota may exceed capacity
- [ ] **Flex Assurant** — 3 Forklift Drivers unfilled 23–25 Mar. Assurant is the top-performing client at 38.8% CR — any gap here is unusual. Investigate before it extends

---

## 7. Notes & Observations

- **This week is almost entirely Craig's portfolio.** Only 2 Claudio-owned venues appear (Soho House Austin: 1 shift, Flex Assurant: 3 shifts — market TBC). The 825 unfilled real shifts are a Craig-side operational issue this week
- **Dummy shifts excluded: 1,471 rows** — of which 1,465 were unfilled by design. Excluding these corrects the apparent fill rate from 40.2% to the true **65.0%**
- **Overbook shifts** (Overbook - Warehouse Operative, Overbook - Loader/Crew) appear at PowerStop and AT&T Stadium — these are intentional overbook buffers expecting cancellations. Not a concern unless they consistently go unfilled past shift start
- **Logan Township is a weekly pattern, not a chronic gap** — gaps only on Wed–Fri suggest a contract schedule structure. Monitor before labeling as a fill problem
- **Nashville and CVG1 are booking gaps, not funnel gaps** — both markets (Nashville 18.1%, Cincinnati 18.3%) have healthy conversion. Workers are getting verified but not booking. Re-engagement is the lever, not more ad spend
- **Confirm market owner** for Cardinal Paint Warehouse and Flex Assurant — not mapped in current market ownership data

---

*Source: `shifts (4).csv` — 3,828 rows · Dummy shifts excluded: 1,471 · Real unfilled: 825 · True fill rate: 65.0%*
*Atlas (@analyst) · 2026-03-17 · `docs/context/weekly-unfilled-shifts-report-template.md`*
