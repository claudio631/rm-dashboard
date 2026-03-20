# Indeed Flex — Campaign Naming Convention

> Source: Claudio Santos — 2026-03-19
> Applies to: All campaigns across Indeed, Google Ads, Meta Ads, Bing, Reddit, Craigslist

## Format

```
{Country} - {Market Type} - {Industry} - {Client Name} - {Role} - {Metro} - {State} - {Period}
```

## Segments

| # | Segment | Description | Required | Examples |
|---|---------|-------------|:--------:|---------|
| 1 | **Country** | Country code | Yes | US, UK |
| 2 | **Market Type** | Business model | Yes | B2C, B2B |
| 3 | **Industry** | Client industry vertical | Yes | Hospitality, Industrial, Logistics, Events, Food Service |
| 4 | **Client Name** | Client company name | Yes | Culinaire, CORT, Stord, OnTrac, Legends Hospitality |
| 5 | **Role** | Job title being recruited | Yes | Servers, Loader / Crew, Warehouse Operative, Picker Packer, Forklift Driver |
| 6 | **Metro** | Metro area or city name | Yes | DFW, Las Vegas, Chicago, Austin, Columbus |
| 7 | **State** | State abbreviation | Yes | TX, NV, IL, OH, GA |
| 8 | **Period** | Campaign date range | Yes | March 16 to March 30, 2026 |

## Rules

1. **Separator:** Always use ` - ` (space-hyphen-space) between segments
2. **Metro names:** Use the same market name as in funnel reports (e.g., "DFW" not "Dallas")
3. **Period format:** Always `{Month} {Day} to {Month} {Day}, {Year}`
4. **Evergreen campaigns:** Use `Evergreen` as the period
5. **No abbreviations** in client names or roles (except standard ones like DFW, NV, TX)
6. **Consistent capitalization:** Title Case for all segments

## Examples

| Campaign Name | Breakdown |
|--------------|-----------|
| `US - B2C - Hospitality - Culinaire - Servers - DFW - TX - March 16 to March 30, 2026` | Standard time-bound campaign |
| `US - B2C - Industrial - OnTrac - Warehouse Operative - Columbus - OH - Evergreen` | Ongoing evergreen campaign |
| `US - B2C - Industrial - Stord - Picker Packer - Las Vegas - NV - March 1 to March 31, 2026` | Monthly campaign |
| `US - B2C - Logistics - CORT - Loader / Crew - Chicago - IL - March 10 to April 10, 2026` | Cross-month campaign |
| `US - B2C - Events - Legends Hospitality - Concession Stand Worker - DFW - TX - March 20 to March 22, 2026` | Short event campaign |
| `US - B2C - Food Service - Bon Appetit - Dishwasher - Chicago - IL - Evergreen` | Evergreen hospitality |
| `US - B2C - Hospitality - Soho House Austin - Hospitality General Labor - Austin - TX - March 15 to April 15, 2026` | Hospitality with full client name |

## Industry Reference

| Industry | Typical Clients | Typical Roles |
|----------|----------------|---------------|
| Industrial | OnTrac, Stord, CTDI, Power Stop, Foxconn | Warehouse Operative, Picker Packer, Forklift Driver, Material Handler |
| Hospitality | CORT, Culinaire, Legends, Merritt, Soho House | Loader / Crew, Server, Bartender, Hospitality General Labor, Hospitality Team Lead |
| Food Service | Bon Appetit, Vestals Catering, Lettuce Entertain You, Compass | Prep Cook, Dishwasher, Line Cook, Server, Bartender |
| Logistics | CORT, OnTrac | Loader / Crew, Assembler |
| Events | Legends, Solaren, Stadium People, SXSW | Concession Stand Worker, Event Staff |
| Tech/Manufacturing | Foxconn, Tennant, AFC Industries, Continental Battery | Assembler, Picker Packer, Warehouse Operative |

## Where This Convention Applies

| System | Field | Notes |
|--------|-------|-------|
| **FHS** | Campaign name (Step 6) | Primary campaign record |
| **Indeed Employer** | Campaign label | Matches FHS |
| **Google Ads** | Campaign name | Same convention for cross-channel consistency |
| **Meta Ads** | Campaign name | Same convention |
| **Bing / Reddit** | Campaign name | Same convention |
| **Budget spreadsheet** | Campaign column | For tracking and reconciliation |
| **UTM parameters** | utm_campaign | URL-safe version (hyphens, lowercase) |

## UTM Version

For UTM parameters, convert the campaign name to URL-safe format:
```
us-b2c-hospitality-culinaire-servers-dfw-tx-mar16-mar30-2026
```
- Lowercase everything
- Replace ` - ` with `-`
- Shorten month names to 3 letters
- Remove spaces in dates

---
*SOP created by Orion (@aiox-master) — 2026-03-19*
*Referenced by: sop-indeed-ad-request.md | campaign-brief-tmpl.md*
