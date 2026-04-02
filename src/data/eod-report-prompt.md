# EOD Update Key Clients — Daily Report Generation Prompt

> Use this prompt with the @analyst agent to generate the daily Slack report.
> Invoke: `@analyst` then paste the instructions below along with fresh data files.

## Prompt

```
Generate the EOD Update Key Clients report for Slack using the following data files from ~/Downloads:

1. **OB Funnel Custom Viewer.xlsx** — Tableau OB funnel split report
2. **JobsCampaigns_YYYYMMDD_YYYYMMDD.csv** — Indeed Analytics campaign spend (MTD)
3. **requisitions-YYYY-MM-DD-NNNNNN.csv** — FHS Requisition report

Use the most recent version of each file.

### Section 1: Key Client Unique Accounts

From the OB Funnel xlsx:
- **Created** = sum of "Worker Accounts Created" for the last 30 rolling days per client/location
- **Verified** = sum of "1st Role Verified (# Workers)" for the last 30 rolling days per client/location
- **(+N)** = the single-day "1st Role Verified (# Workers)" value from D-1 (yesterday)
  - Exception: On **Monday**, use **Friday's** value (D-3) instead of D-1

Key clients and their named locations (everything else goes to "Other Locations"):
- **CORT:** Las Vegas, Chicago, Atlanta, Orlando, Phoenix, Austin, Nashville
- **Stord, Inc:** Las Vegas, Reno, Atlanta, Erlanger (all locations shown individually)
- **OnTrac Final Mile:** Logan Township, Columbus, Middleburg Heights, Reno
- **CTDI:** Dallas, Columbus, Nashville (all locations shown individually)

Sort named locations by Created count (descending). "Other Locations" always appears last.

### Section 2: Indeed Spend Comparison

From the JobsCampaigns CSV:
- Sum the "Spend" column for all rows = MTD spend
- Show the delta vs the last report's spend value: (+$X,XXX.XX since last report)
- Last report spend: $____ (provide this value or retrieve from previous report)

### Section 3: Open Campaigns

Two subsections:

**3a. Named Client Campaigns**
From the requisitions CSV:
- Filter: status = "Open" only
- Exclude: any client name containing "Indeed Flex"
- Normalize location names (fix trailing spaces, inconsistent comma spacing)
- Deduplicate locations per client
- Sort clients alphabetically, locations alphabetically within each client
- Format: Client Name: Location 1; Location 2; Location 3

**3b. Indeed Flex App Locations**
From the requisitions CSV:
- Filter: status = "Open" only AND client name contains "Indeed Flex"
- Group by metro/city (normalize location — strip state abbreviation, trim spaces)
- For each location, list unique job roles (deduplicated, sorted alphabetically)
- Format: Location = Role 1, Role 2, Role 3
- Sort locations alphabetically

### Slack Formatting Rules

- Use *text* (single asterisks) for bold — this is Slack format, NOT markdown
- No blank line between client name and first location
- One blank line between client blocks
- The header always uses: "(last update yesterday)"

### Output Template

@here EOD RM Update Key client unique accounts: (last update yesterday)

*{Client}:*
{Location}: {Created} Created → {Verified} Verified (+{N})
...

*Indeed Spend Comparison:* Indeed {Month} so far: ${MTD} (+${delta} since last report)

*Open Campaigns (Status: Open Only)*

{Client}: {Location 1}; {Location 2}; ...
```

## Required Inputs

| Input | Source | File Pattern |
|-------|--------|-------------|
| OB Funnel | Tableau export | `OB Funnel Custom Viewer.xlsx` |
| Campaign Spend | Indeed Analytics export | `JobsCampaigns_*.csv` |
| Requisitions | FHS export | `requisitions-*.csv` |
| Last report spend | Previous day's report | Manual input or stored value |
