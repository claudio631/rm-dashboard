# Job Template: Industrial General Labor

> Vertical: Industrial
> Example Client: Ingram Content Group
> FHS Industry: Industrial
> Interviewing Type: AI Only

## FHS Configuration

| Field | Value |
|-------|-------|
| Industry | Industrial |
| Job title (system) | Industrial General Labor |
| Custom job title | General Laborer |
| Agency | Indeed |
| Advertise on Indeed.com | Enabled |
| Post on Indeed Flex app | Enabled |
| Interviewing type | AI Only |

## Landing Page URL Pattern

```
https://indeedflex.com/find-jobs/lp/industrial-general-labor/?utm_source=indeed&utm_medium=cpc&link_value=syft://jobs/browse/{{job_id}}&employer={{client_slug}}&metro={{metro_slug}}&role=industrial-general-labor&utm_campaign={{client_slug}}-igl-{{metro_slug}}
```

## Job Description Template

```
Job Title: General Laborer
Location: {{location}}
Pay: {{pay_rate}}
Shift Option: {{shift_schedule}}

Job Description

Hands on, fast-paced warehouse project work. You'll help break down shelving, palletize materials, and prepare items for recycling or shipment. This is high movement work with heavy lifting, you will not be at a stationary workstation.

What you'll do

Remove shelving from warehouse bay units
Break down materials and components as directed
Palletize materials and secure loads with banding for shipment
Move metal and wood flooring from the mezzanine to pallets
Load recyclable materials into metal dumpsters
Keep work areas clean and organized during disassembly

What to expect on every shift

Constant walking, bending, lifting, and carrying
Moving between different areas of the warehouse (no fixed station)
Heavy lifting at times — teamwork encouraged for larger items

What you must bring

Mechanic-style work gloves (required — not provided on site)
Closed-toe, slip-resistant shoes

Physical requirements

Ability to lift, push, and pull heavy materials throughout the shift
Comfort working on your feet for extended periods

{{code}}
```

## Variables

| Variable | Example | Notes |
|----------|---------|-------|
| `{{location}}` | La Vergne, TN | City, State |
| `{{pay_rate}}` | $17.50 | Single rate or range |
| `{{shift_schedule}}` | Schedule will vary between Monday - Sunday | Flexible/varies |
| `{{code}}` | #ING-IGL-LAVTN | Client-Role-Market code |
| `{{job_id}}` | 484855 | FHS job browse ID |
| `{{client_slug}}` | ingram-content-group | URL-friendly client name |
| `{{metro_slug}}` | nashville | URL-friendly metro name |

## Code Pattern

`#ING-IGL-LAVTN` = `{client_abbrev}-{role_abbrev}-{location_abbrev}`
- ING = Ingram
- IGL = Industrial General Labor
- LAVTN = La Vergne, TN

## Notes

- This role is project-based (shelving breakdown, disassembly) — not typical picking/packing
- Gloves are required but NOT provided on site — must be in ad copy
- High-movement, no fixed station — important differentiator from standard warehouse
- Job type listed as Full-time (unlike most IF roles which are Part-time)
