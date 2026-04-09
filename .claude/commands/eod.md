# EOD — Daily Reports Generator

// turbo-all

Run all daily reports from the latest files in ~/Downloads. No questions, no permissions — just execute.

## Instructions

You MUST execute ALL 4 reports below in sequence. Do NOT ask for confirmation between them. Read all data files ONCE at the start, then produce all outputs.

### Step 0: Find Latest Files

Find the most recent version of each file in ~/Downloads by modification date. When multiple versions exist for the same day, ALWAYS use the newest one (latest timestamp).

1. **OB Funnel:** `OB Funnel Custom Viewer*.xlsx` — latest **full export** by modification date (may have numbered suffixes like `(2)`, `(3)`). Full exports are ~250KB+ with 5000+ rows and 80+ clients. Filtered/partial exports are ~95KB with <2000 rows and only 4 clients. ALWAYS prefer the latest full export over a newer partial export. To validate: check file size (>200KB = full) or row count (>3000 = full).
2. **Requisitions:** `requisitions-*.csv` — latest by modification date AND largest file size (~2.3MB = full export). Ignore partial exports (<500KB).
3. **Campaign Spend:** `JobsCampaigns_*.csv` — latest by modification date. The file may cover a longer period than the current month (e.g., Jan 1 to Mar 25). Parse the filename dates `JobsCampaigns_YYYYMMDD_YYYYMMDD.csv` to know the range.
4. **Last spend:** Read from `src/data/last-report-spend.json`
5. **Revenue Requests:** `US_Recruitment_Requests__us_*.csv` — latest by modification date
6. **Indeed Campaign Report:** `CampaignReport_Advanced_*.csv` — latest by modification date

If any file is missing, warn and skip that report section — don't halt everything.

### Report 1: EOD Slack Report (Slack format — ready to paste)

Generate the EOD Update using the prompt and rules defined in `src/data/eod-report-prompt.md`.

Key rules:
- Use `*text*` (single asterisks) for bold — Slack format
- Key clients: CORT, Stord, OnTrac, CTDI with their named locations
- D-1 rule: use yesterday's single-day verified count for (+N). On Monday use Friday's.
- Include Indeed Spend Comparison with delta vs last report
- Include Google Ads Spend MTD — pull from Google Ads API (`google-ads.yaml`, US account `7236100723`) for current month. Show as: `*Google Ads Spend:* Google Ads {Month} so far: $X,XXX.XX (+$X,XXX.XX since last report)`. Store last Google Ads spend in `src/data/last-report-spend.json` under `last_google_ads_spend`.
- Include Open Campaigns (status=open, exclude Indeed Flex clients)
- After generating, update `src/data/last-report-spend.json` with both Indeed and Google Ads MTD spend

**Indeed Spend — Month-to-Date calculation:**
The JobsCampaigns CSV may cover a period longer than the current month (e.g., Jan 1 to Mar 25). You MUST use **current-month-only spend**:
- **Preferred:** Use a file whose filename starts with the current month (e.g., `JobsCampaigns_20260301_*.csv`). This gives exact MTD spend. Always prefer this over a multi-month file.
- **Fallback (multi-month file):** If only a multi-month file is available, filter campaigns by the **first date mentioned** in the campaign name. Only include campaigns that START in the current month, plus campaigns with no date in the name. Do NOT include campaigns that start in prior months even if they mention the current month as an end date.
- **Delta** = today's MTD spend − last report's MTD spend (from `last-report-spend.json`). This shows how much was spent since the last report.

### Report 2: Weekly Funnel Report (HTML with conditional formatting)

Run the weekly funnel report script:
```bash
python3 squads/recruitment-marketing-flex/scripts/weekly-funnel-report.py \
  <ob_funnel_path> --reqs <requisitions_path> --owner claudio
```

This generates the HTML report with:
- KPI cards, conditional formatting (🟢🟡🔴), funnel table by Location > Client
- Open Reqs column cross-referenced with requisitions
- Saved to `docs/reports/weekly-funnel-claudio-YYYY-MM-DD.html`

Open the HTML in the browser automatically.

### Report 3: Requisition Status Table (HTML — saved and opened in browser)

Generate as an HTML file saved to `docs/reports/req-status-YYYY-MM-DD.html` and open it automatically.

From the requisitions CSV, build a table grouped by State > Metro > Client > Role.

**Columns:** State | Metro | Client | Role | RSVPs | Last Week RSVPs | Target | Fill% | Open | Auto-Paused | Draft | Total

**Last Week RSVPs column:**
- Find the requisitions file closest to 7 days ago (e.g., if today is Apr 8, look for the Apr 1 file).
- For each (State, Metro, Client, Role) row, sum the `rsvps` column from the 7-day-old file for matching rows.
- Show the value. If no match exists in the old file, show `—`.

**Sorting:** Sort rows ascending by RSVPs (lowest first) so the neediest rows appear at the top.

**Conditional formatting:**
- RSVPs < 50: red background (`#fff0f0`), bold red RSVPs value
- RSVPs 50–99: amber background (`#fff8e6`)
- RSVPs ≥ 100: no highlight (white)
- Fill% < 30%: red text on Fill% cell
- Fill% 30–69%: amber text
- Fill% ≥ 70%: green text
- Draft > 0: yellow cell background (`#fffde7`) on the Draft column cell
- Auto-Paused > 0: yellow cell background (`#fffde7`) on the Auto-Paused column cell

**Filters:** Active statuses only (open + auto-paused + draft). Exclude Indeed Flex Application clients. Show ALL markets.

### Report 4: Recruitment Request Dashboard (HTML)

Cross-reference the revenue team's recruitment requests against FHS requisitions, Indeed campaigns, and OB Funnel data. Generate an HTML dashboard saved to `docs/reports/recruitment-request-dashboard-YYYY-MM-DD.html`.

**Input files:**
- `US_Recruitment_Requests__us_*.csv` — include ALL rows (Live AND Declined)
- `requisitions-*.csv` — match reqs by client+location+role
- `JobsCampaigns_*.csv` — match Indeed campaigns by client+location+role (latest file by modification date)
- `OB Funnel Custom Viewer*.xlsx` — match funnel data (Created, Verified, RTB) by client+location+role

**Row integrity rule (NON-NEGOTIABLE):**
- Every row in the Revenue Requests file (Live or Declined) MUST appear as its own row in Report 5. NEVER merge, deduplicate, or drop rows — even if they share the same client and location. Two Levy requests = two rows in the report.

**Declined requests rule:**
- Rows with Request Status = "Declined" appear in the table but ALL metric columns (FHS, Indeed, OB Funnel, Fill) are left BLANK. We don't run campaigns for declined requests.

**Client matching rules:**
- Normalize client names (e.g. "Compass" → "Culinaire", "DC Flex" → "CORT", "Food Glorious" → "Culinaire", "Aba Nashville" → "Lettuce", "Texas Motor Speedway" → "Levy")
- Use metro aliases for location matching (e.g. "DFW" ↔ "Dallas", "Vegas" ↔ "Las Vegas", "Bedford Park" ↔ "Chicago")

**Columns:**
- St (request status badge: `O` = Open, `C` = Closed — color-coded, no priority score), Client (shortened), Owner (first name), Role, HC, Start (format: mmm/dd/yyyy e.g. Mar/31/2026), Shifts (Yes/No tag)
- FHS: Open reqs count (status=open AND status=auto-paused both count as open), Interview (sum of RSVPs from matching reqs after the revenue request submission date), Int. Target (HC × 10 — interview pipeline target). Matching priority: (1) client+location+role, (2) fallback to location+role only if no client match (picks up Indeed Flex reqs for same role+metro)
- Indeed Ads: status emoji, # campaigns (Camps), spend (value only, no campaign names). Matching priority: (1) client+location+role, (2) fallback to location+role only if no client match (picks up Indeed Flex campaigns for same role+metro)
- OB Funnel: Created, Verified, RTB
- Fulfillment: Target (RTB Target = HC × 2.5), Fill% = RTB ÷ (HC × 2.5) (last column, with progress bar)
- Shifts: This is the list of unfilled shifts from ACP, we need to match the location/city, role, client/brand company and update yes if exists shift posted or no if has no shift posted.

**UI rules:**
- Sticky header rows (table scrolls inside container with `max-height: calc(100vh - 60px)`)
- Large fonts: body 14px, table cells 14-15px, numbers 15px bold, KPI cards 32px
- No priority column. No priority-based row coloring.
- **Sorted by submission date ascending** (oldest request first — matches Slack submission list order)
- Summary cards at top: Live Requests, Total HC, No FHS, Shifts TBD

Open the HTML in the browser automatically.

### Final Output

After all 4 reports, show a summary:
```
EOD Reports Complete:
✅ Slack Report — ready to paste
✅ Funnel Report — opened in browser (docs/reports/...)
✅ Requisition Status — opened in browser (docs/reports/...)
✅ Recruitment Request Dashboard — opened in browser (docs/reports/...)
📊 Last spend updated: $XX,XXX.XX
```
