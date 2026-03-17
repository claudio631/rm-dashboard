# Job Template: Picker Packer / Warehouse Team Member

> Vertical: Industrial
> Example Client: Stord, Inc
> FHS Industry: Industrial
> Interviewing Type: AI Only

## FHS Configuration

| Field | Value |
|-------|-------|
| Industry | Industrial |
| Job title (system) | Picker Packer |
| Custom job title | Warehouse Team Member |
| Agency | Indeed |
| Advertise on Indeed.com | Enabled |
| Post on Indeed Flex app | Enabled |
| Interviewing type | AI Only |

## Landing Page URL Pattern

```
https://indeedflex.com/find-jobs/lp/picker-packer/?utm_source=indeed&utm_medium=cpc&link_value=syft://jobs/browse/{{job_id}}&employer={{client_slug}}&metro={{metro_slug}}&role=picker-packer&utm_campaign={{client_slug}}-picker-packer-{{metro_slug}}
```

## Job Description Template

```
Job Title: Warehouse Team Member (Picker Packer)

Hourly Rate: {{pay_rate}}

Location: {{location}}

Shift Options:

{{shift_schedule}}

Indeed Flex is hiring Picker Packers for their top industrial client, {{client_name}}.

Perks for You

Health Benefits – Medical, dental, and vision coverage available.
Free Training & Growth – Gain new skills and advance your career with free upskilling programs.

Duties & Responsibilities:

Performs manual labor tasks (packaging, labeling, lifting, and loading)
Must maintain productivity and accuracy standards
Manage product movement and shipment

Job Requirements:

Must be able to work safely and productively within the warehouse
Punctual and consistent attendance required
Ability to follow directions and work alongside other workers in the warehouse

Why You'll Love Working for Indeed Flex:

Work when it works for you. Pick shift times that fit your lifestyle and schedule.
New Skills and Career Development. Get upskilled in new trades. We offer a variety of free training and development opportunities.
Apply today – fast track your next paycheck!

{{code}}
```

## Variables

| Variable | Example | Notes |
|----------|---------|-------|
| `{{location}}` | McCarran, NV | City, State |
| `{{pay_rate}}` | $19.50/hour | Single rate |
| `{{shift_schedule}}` | Monday-Thursday 5:00am-3:30pm / Friday-Sunday 5:00am-5:30pm | Multiple options listed |
| `{{client_name}}` | Stord, Inc | For cobranding mention in body |
| `{{code}}` | #STORD-PK-MRN | Client-Role-Market code |
| `{{job_id}}` | 449234 | FHS job browse ID |
| `{{client_slug}}` | stord-inc | URL-friendly client name |
| `{{metro_slug}}` | reno | URL-friendly metro name |

## Code Pattern

`#STORD-PK-MRN` = `{client_abbrev}-{role_abbrev}-{location_abbrev}`
- STORD = Stord
- PK = Picker Packer
- MRN = McCarran, NV

## Notes

- This template uses **cobranding** — explicitly names the client ("Stord, Inc") in the body
- Highlights health benefits (medical, dental, vision) — differentiator for W-2 roles
- Multiple shift options listed — common for picker packer roles
- "Apply today – fast track your next paycheck!" — strong CTA closing
