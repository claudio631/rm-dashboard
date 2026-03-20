# EOD — Daily Reports Generator

Run all daily reports from the latest files in ~/Downloads. No questions, no permissions — just execute.

## Instructions

You MUST execute ALL 4 reports below in sequence. Do NOT ask for confirmation between them. Read all data files ONCE at the start, then produce all outputs.

### Step 0: Find Latest Files

Find the most recent version of each file in ~/Downloads by modification date. When multiple versions exist for the same day, ALWAYS use the newest one (latest timestamp).

1. **OB Funnel:** `OB Funnel Custom Viewer*.xlsx` — latest by modification date (may have numbered suffixes like `(2)`, `(3)`)
2. **Requisitions:** `requisitions-*.csv` — latest by modification date AND largest file size (~2.3MB = full export). Ignore partial exports (<500KB).
3. **Campaign Spend:** `JobsCampaigns_*.csv` — latest by modification date
4. **Last spend:** Read from `src/data/last-report-spend.json`

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

### Final Output

After all 4 reports, show a summary:
```
EOD Reports Complete:
✅ Slack Report — ready to paste
✅ Funnel Report — opened in browser (docs/reports/...)
✅ Requisition Status — table above
✅ Campaign Spend — table above
📊 Last spend updated: $XX,XXX.XX
```
