# Hiring Event Wrap-Up — Slack Report Generator

Generate the post-event Slack wrap-up report in the standard format. No questions — execute immediately using the provided check-in file and event context.

## How to invoke

```
/hiring-event-wrapup
```

Optionally pass the check-in file path and/or event details as arguments. If not provided, auto-detect the latest hiring event check-in file in ~/Downloads.

## Instructions

### Step 1 — Find the Check-In File

Look in `~/Downloads` for the most recent hiring event check-in Excel file. Patterns:
- `*Hiring Event Check In*.xlsx`
- `*Check In*.xlsx`
- `*check-in*.xlsx`

If multiple files exist, use the most recently modified. If the user passed a file path as an argument, use that.

### Step 2 — Parse Check-In Data

Open the Excel file with `openpyxl`. Expected columns (0-indexed):
- `0` — Timestamp (datetime)
- `1` — First Name
- `2` — Last Name
- `5` — How they found the event (source)
- `6` — App downloaded (Yes/No)
- `9` — Availability
- `10` — Job offer accepted (Yes/No)

Compute:
- **Total show-ups** = total rows
- **Onboarded** = rows where col[10] == 'Yes'
- **Not moving forward** = rows where col[10] == 'No' (or != 'Yes')
- **Onboarding rate** = onboarded / show-ups × 100 (1 decimal)
- **App downloaded** = rows where col[6] == 'Yes' (and %)
- **First check-in** and **Last check-in** times from col[0] (datetime objects only)
- **Attribution** — count col[5], then group as:
  - `Indeed/Google` = rows containing "Indeed" OR "Google" in source
  - `Word of Mouth` = rows containing "Word" or "Mouth" or "Friend" or "Referral"
  - `Social Media` = rows containing "social" or "Facebook" or "Instagram" or "Reddit"
  - `Other` = everything else
  - Show each as `N (X%)` of total
- **Availability** — count col[9]:
  - ASAP = contains "ASAP"
  - 1–2 weeks = contains "1-2" (and not ASAP)
  - 2–3 weeks = contains "2-3" (and not ASAP, not 1-2)

**Multi-day events:** If the Excel has a clear day separator column or if timestamps span multiple calendar dates, build an "Attendance by Day" table. Show each day as: Day | Show-ups | Onboarded | Rate.

### Step 3 — Pull Indeed Ads Spend

Find the latest `CampaignReport_Advanced_*.csv` in `~/Downloads`. Filter rows where:
- Campaign name contains the client name AND location AND matches the event flight dates
- OR campaign name contains "Hiring Event" AND client AND is ACTIVE or was recently DELETED (spent > $0)

Sum `Budget spent` column for matching rows. Format as `$X,XXX.XX`.

**Campaign label for Slack:** Extract date range from campaign name (e.g., "Apr 30 – May 6").

### Step 4 — Pull Google Ads Spend

Query the Google Ads API for campaign spend during the event flight:

```python
from google.ads.googleads.client import GoogleAdsClient
YAML_PATH = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"
client = GoogleAdsClient.load_from_storage(YAML_PATH)
```

Query ALL campaigns matching the location name (BAU + event) — NOT just event campaign IDs. This captures BAU campaigns that were still spending during the event flight window.

Extract the location keyword from the event (e.g., "logan" for Logan Township, "orlando" for Orlando, "swedesboro" for Swedesboro). Use LIKE match on campaign name:

```sql
SELECT campaign.id, campaign.name, campaign.status, metrics.cost_micros
FROM campaign
WHERE campaign.name LIKE '%{location_keyword}%'
  AND segments.date BETWEEN '{start_date}' AND '{end_date}'
  AND metrics.cost_micros > 0
```

Sum ALL rows returned (BAU + event campaigns). This is the true Google Ads cost attributable to the market during the event window. Format as `$X,XXX.XX`. Label as: `Google Ads — {Location} ({start} – {end}, all campaigns)`.

If no results, note "Google Ads: pending".

### Step 5 — Compute Cost Metrics

- **Total spend** = Indeed Ads + Google Ads
- **Cost per show-up** = total / show-ups (2 decimals)
- **Cost per onboarded worker** = total / onboarded (2 decimals)

### Step 6 — RSVPs

RSVPs = total registrations in the FHS hiring session before the event (not the same as show-ups).

**Source options (in priority order):**
1. If the user passes RSVPs as an argument (e.g., `/hiring-event-wrapup rsvps=145`), use that value.
2. If a FHS export file exists in `~/Downloads` matching the event (e.g., `*RSVP*`, `*Session*`, `*registration*`), parse the row count.
3. If neither is available, show `RSVPs: —` (dash) — never omit the line, never guess.

If RSVPs are known, also compute:
- **Show rate** = show-ups / RSVPs × 100 (1 decimal) — append after show-ups: `Show-ups: *{N}* ({X}% show rate)`

### Step 7 — Generate Slack Report

Output EXACTLY in this format (Slack markdown — single asterisks for bold):

```
@here
*{CLIENT} Hiring Event — {City, State} | {Date} Recap*

*Overview*
• RSVPs: *{N}*
• Show-ups: *{N}* ({X}% show rate)
• Onboarded: *{N}* ({X}%)
• Not moving forward: {N}

*Attribution (how they found the event)*
• Indeed/Google: {N} ({X}%)
• Word of Mouth: {N} ({X}%)
• Other: {N} ({X}%)
• Social Media: {N} ({X}%)

*Spend*
• Indeed Ads ({campaign label} · {date range}): ${X,XXX.XX}
• Google Ads — {Location} ({date range}, all campaigns): ${X,XXX.XX}
• *Total: ${X,XXX.XX}*

• Cost per show-up: ${XX.XX}
• Cost per onboarded worker: ${XX.XX}
```

If RSVPs are unknown, show `• RSVPs: —` and omit show rate from the Show-ups line.

**Multi-day events** — add this block after Overview, before Attribution:

```
*Attendance by Day*
| Day | Show-ups | Onboarded | Rate |
|-----|----------|-----------|------|
| {Day Date} | {N} | {N} | {X}% |
```

**Rules:**
- Use `*text*` (single asterisks) for bold — Slack format, NOT markdown `**`
- `@here` always on the first line — no exceptions
- Attribution percentages always round to nearest whole number
- Never show 0% lines — omit attribution sources with 0 count
- If Indeed Ads spend not found: show `• Indeed Ads: not available`
- If Google Ads spend not found: show `• Google Ads: pending`
- No trailing blank lines

### Step 8 — Output

Print the Slack report, ready to paste directly into Slack. No extra commentary before or after the report block itself.
