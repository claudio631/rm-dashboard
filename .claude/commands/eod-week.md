# EOD Week — Weekly Reports Generator

Run weekly reports from the latest files in ~/Downloads. No questions, no permissions — just execute.

## Instructions

### Step 0: Find Latest Files

Find the most recent version of each file in ~/Downloads by modification date.

1. **Campaign Spend:** `JobsCampaigns_*.csv` — latest by modification date. The file may cover a longer period than the current month (e.g., Jan 1 to Mar 25). Parse the filename dates `JobsCampaigns_YYYYMMDD_YYYYMMDD.csv` to know the range.

If the file is missing, warn and skip.

### Report 1: Campaign Spend Breakdown — MTD Only (markdown table)

**This report is MTD (current month only). Never show YTD or full-file data.**

Apply the MTD filter before aggregating anything:
- **Preferred:** If the filename starts with the current month (`JobsCampaigns_20260401_*.csv`), all rows are already MTD — use them all.
- **Fallback (multi-month file):** Filter to campaigns whose **first date in the campaign name** falls in the current month. Exclude campaigns that started in prior months. Campaigns with no date in the name are always included.
- **No current-month data:** If no campaigns qualify after filtering, show an empty table and note: "No {Month} campaigns in file — download a current-month export from Indeed Analytics."

After filtering to MTD-only rows, aggregate spend by:
- Category: State
- Subcategory: Metro
- Sub-subcategory: Client

Show totals at each level. Flag any campaigns that don't follow the naming convention.

Label the report header with the current month (e.g., "April 2026 MTD"), never with the file's full date range.

### Final Output

```
EOD Week Reports Complete:
✅ Campaign Spend — table above
```