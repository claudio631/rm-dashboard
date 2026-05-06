---
task: zip-code-discovery
title: Feeder Zone & ZIP Code Discovery
description: Identify the top 3 residential feeder zones for a job site hub address. Outputs a zip code table ready to paste into Indeed Ads and FHS requisitions.
agents: [ppc-paid-media-specialist, google-ads-specialist, aiox-master]
elicit: true
outputs:
  - feeder_zones_table (markdown)
  - indeed_zip_codes (comma-separated string)
  - feeder_zones_csv (csv file)
---

# Task: Feeder Zone & ZIP Code Discovery

## Purpose

Identify the top 3 residential "feeder" zones for a specific job site hub address. Produces:

1. A **Markdown table** to embed in the active campaign brief
2. An **Indeed-ready ZIP code list** (comma-separated, paste directly into geo targeting)
3. An **FHS-ready ZIP code list** for requisition radius configuration
4. A **CSV file** for CRM or map tool export

---

## Step 1 — Elicit Inputs

Ask the user for the venue address only. Do NOT ask for job type or ad spend context.

```
To generate the feeder zone ZIP code analysis, I need the venue address:

1. **Venue Address** (full street address of the job site)
   → e.g., "1234 W Diversey Ave, Chicago, IL 60614"
```

Capture response as:
- `{hub_address}` — full physical address

Defaults (always applied, never ask):
- `{job_type}` — low-income / blue-collar labor (applies to all roles)
- `{ad_spend_context}` — B: Already covering 20 miles — look for satellite feeder hubs

---

## Step 2 — Execute Feeder Zone Analysis

Apply the following analysis once inputs are collected:

---

### Role
You are a Strategic Talent Sourcing Specialist specializing in high-volume, hourly labor markets.

### Objective
Identify the **top 3 residential feeder zones** for `{hub_address}` that provide high density of blue-collar, warehouse-ready, or service-sector workers suited for `{job_type}` positions.

### Primary Constraints

| Constraint | Rule |
|-----------|------|
| **Target Demographic** | Low-income to lower-middle-income residential areas with a high percentage of renters |
| **The 20-Minute Rule** | Prioritize locations where peak-hour commute (8:00 AM) to the hub is under 25 minutes |
| **Path of Least Resistance** | Account for reverse commutes (traveling away from city centers) or surface street alternatives that bypass major highway bottlenecks |
| **Institutional Anchor** | Always include one "Academic Pipeline" (Community College or Vocational School) that serves the target demographic |
| **Ad Spend Context** | Already covering 20 miles — look for satellite feeder hubs (default, always applied) |

---

## Step 3 — Output

Produce all four outputs below in sequence.

---

### Output A — Hub Coordinates

Provide the latitude and longitude for the hub address. Format: `{lat}, {lng}` (decimal degrees, 6+ decimal places).

**Hub Address:** `{hub_address}`
**Coordinates:** `{hub_lat}, {hub_lng}`

> These coordinates can be used directly in Google Ads, Indeed Ads radius targeting, and FHS geo-configuration.

---

### Output B — Feeder Zones Markdown Table

Embed this table directly into the **Feeder Zones & ZIP Code Targeting** section of the active campaign brief.

| Category | Name | ZIP Codes | Coordinates | Distance | Peak Drive Time | Google Maps |
|----------|------|-----------|-------------|----------|-----------------|-------------|
| Feeder Zone 1 | {name_1} | {zips_1} | {lat_1}, {lng_1} | {dist_1} mi | {drive_1} min | [Directions](https://www.google.com/maps/dir/{hub_encoded}/{zone1_encoded}) |
| Feeder Zone 2 | {name_2} | {zips_2} | {lat_2}, {lng_2} | {dist_2} mi | {drive_2} min | [Directions](https://www.google.com/maps/dir/{hub_encoded}/{zone2_encoded}) |
| Academic Pipeline | {name_3} | {zips_3} | {lat_3}, {lng_3} | {dist_3} mi | {drive_3} min | [Directions](https://www.google.com/maps/dir/{hub_encoded}/{zone3_encoded}) |

**Google Maps link format:**
`https://www.google.com/maps/dir/[Hub+Address+URL+Encoded]/[Target+Area+Name+or+ZIP+URL+Encoded]`

---

### Output C — Zone Justifications

Write 2–3 sentences per zone explaining why it was selected. Reference demographic signals, commute patterns, or local infrastructure (e.g., "High-density apartment corridor," "Traditional industrial stronghold," "Reverse commute away from downtown").

**Zone 1 — {name_1}:**
{justification_1}

**Zone 2 — {name_2}:**
{justification_2}

**Academic Pipeline — {name_3}:**
{justification_3}

---

### Output D — CSV Export

Produce the following CSV block. The user can save this as a `.csv` file for CRM or map tool import.

```csv
Category,Name,ZIP_Codes,Latitude,Longitude,Distance_Miles,Peak_Drive_Min,Maps_Link
Hub,{hub_address},,{hub_lat},{hub_lng},,,
Feeder Zone 1,{name_1},{zips_1},{lat_1},{lng_1},{dist_1},{drive_1},{maps_link_1}
Feeder Zone 2,{name_2},{zips_2},{lat_2},{lng_2},{dist_2},{drive_2},{maps_link_2}
Academic Pipeline,{name_3},{zips_3},{lat_3},{lng_3},{dist_3},{drive_3},{maps_link_3}
```

---

### Output E — Indeed & FHS ZIP Code Lists

**Indeed Ads — Geographic Targeting (paste directly into Indeed Ads location field):**

```
{all_zip_codes_comma_separated}
```

**FHS Requisition ZIP Codes (all feeder zones combined):**

```
{all_zip_codes_comma_separated}
```

> These are all ZIP codes from all 3 feeder zones combined, deduplicated, comma-separated.

---

## Step 4 — Embed in Brief

Copy **Output A** (the Markdown table) and **Output D** (ZIP code lists) into the **Feeder Zones & ZIP Code Targeting** section of the active campaign brief. Confirm with the user that the section has been updated.
