# EOD — Daily Reports Generator

Run all daily reports from the latest files in ~/Downloads. No questions, no permissions — just execute.

## Instructions

You MUST execute ALL 5 reports below in sequence. Do NOT ask for confirmation between them. Read all data files ONCE at the start, then produce all outputs.

### Step 0: Find Latest Files

Find the most recent version of each file in ~/Downloads by modification date. When multiple versions exist for the same day, ALWAYS use the newest one (latest timestamp).

1. **OB Funnel:** `OB Funnel Custom Viewer*.xlsx` — latest by modification date (may have numbered suffixes like `(2)`, `(3)`)
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
- Include Open Campaigns (status=open, exclude Indeed Flex clients)
- After generating, update `src/data/last-report-spend.json` with the new MTD spend

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

### Report 3: Requisition Status Table (markdown table)

From the requisitions CSV, generate a table structured as:
- Category: Location
- Subcategory: Client
- Sub-subcategory: Role

Columns: RSVPs | Target | Fill% | Open | Auto-Paused | Draft | Total

Filter to active statuses only (open + auto-paused + draft). Exclude Indeed Flex Application clients.

Show ALL markets (not just Claudio's).

Group by State > Metro > Client > Role hierarchy.

### Report 4: Campaign Spend Breakdown (markdown table)

From the JobsCampaigns CSV, parse campaign names and aggregate spend by:
- Category: State
- Subcategory: Metro
- Sub-subcategory: Client

Show totals at each level. Flag any campaigns that don't follow the naming convention.

### Report 5: Revenue Requests Cross-Reference Dashboard (HTML)

Cross-reference the revenue team's recruitment requests against FHS requisitions, Indeed campaigns, and OB Funnel data. Generate an HTML dashboard saved to `docs/reports/revenue-requests-crossref-YYYY-MM-DD.html`.

**Input files:**
- `US_Recruitment_Requests__us_*.csv` — include ALL rows (Live AND Declined)
- `requisitions-*.csv` — match reqs by client+location
- `JobsCampaigns_*.csv` — match Indeed campaigns by client+location (latest file by modification date)
- `OB Funnel Custom Viewer*.xlsx` — match funnel data (Created, Verified, RTB) by client+location

**Row integrity rule (NON-NEGOTIABLE):**
- Every row in the Revenue Requests file (Live or Declined) MUST appear as its own row in Report 5. NEVER merge, deduplicate, or drop rows — even if they share the same client and location. Two Levy requests = two rows in the report.

**Declined requests rule:**
- Rows with Request Status = "Declined" appear in the table but ALL metric columns (FHS, Indeed, OB Funnel, Fill) are left BLANK. We don't run campaigns for declined requests.

**Client matching rules:**
- Normalize client names (e.g. "Compass" → "Culinaire", "DC Flex" → "CORT", "Food Glorious" → "Culinaire")
- Use metro aliases for location matching (e.g. "DFW" ↔ "Dallas", "Vegas" ↔ "Las Vegas", "Bedford Park" ↔ "Chicago")

**Columns:**
- P (priority score), Client (shortened), Owner (first name), Role, HC, Start (format: mmm/dd/yyyy e.g. Mar/31/2026), Shifts (Yes/No tag)
- FHS: Open reqs count (status=open AND status=auto-paused both count as open), Interview (sum of RSVPs from matching reqs — renamed from "RSVPs")
- Indeed Ads: status emoji (St), # campaigns (Camps), spend (value only, no campaign names)
- OB Funnel: Created, Verified, RTB
- Fill: Target (HC × 10 — the HC is the headcount revenue needs, we need 10× interviews to fill), Fill% = RTB ÷ HC (last column, with progress bar)

**UI rules:**
- Sticky header rows (table scrolls inside container with `max-height: calc(100vh - 60px)`)
- Large fonts: body 14px, table cells 14-15px, numbers 15px bold, KPI cards 32px
- Priority rows color-coded: red (≥7), amber (4-6), white (0-3)
- Sorted by priority descending
- Summary cards at top: Live Requests, Total HC, High Priority, No FHS, No Indeed, Shifts TBD

Open the HTML in the browser automatically.

### Final Output

After all 5 reports, show a summary:
```
EOD Reports Complete:
✅ Slack Report — ready to paste
✅ Funnel Report — opened in browser (docs/reports/...)
✅ Requisition Status — table above
✅ Campaign Spend — table above
✅ Revenue Requests Dashboard — opened in browser (docs/reports/...)
📊 Last spend updated: $XX,XXX.XX
```
