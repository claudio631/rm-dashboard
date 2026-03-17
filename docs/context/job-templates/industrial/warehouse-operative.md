# Job Template: Warehouse Operative / Warehouse Distribution Associate

> Vertical: Industrial
> Primary Client: OnTrac Final Mile
> FHS Industry: Industrial
> Interviewing Type: AI Only

## FHS Configuration

| Field | Value |
|-------|-------|
| Industry | Industrial |
| Job title (system) | Warehouse Operative |
| Custom job title | Warehouse Distribution Associate |
| Agency | Indeed |
| Advertise on Indeed.com | Enabled |
| Post on Indeed Flex app | Enabled |
| Interviewing type | AI Only |

## Landing Page URL Pattern

```
https://indeedflex.com/find-jobs/lp/warehouse-operative/?utm_source=indeed&utm_medium=cpc&link_value=syft://jobs/browse/{{job_id}}&employer={{client_slug}}&metro={{metro_slug}}&role=warehouse-operative&utm_campaign={{client_slug}}-warehouse-operative-{{metro_slug}}
```

## Job Description Template

```
Entrevistas y apoyo disponibles en español

Now Hiring: Warehouse Distribution Associate – {{location}}

Earn {{pay_rate}}

Join Indeed Flex and take on a hands-on warehouse role that rewards reliability, teamwork, and effort. Perfect for active individuals who want consistent work and multiple ways to earn extra this season.

Shift Schedule

{{shift_schedule}}

Your Daily Responsibilities

Unload trailers and sort packages for delivery
Load trucks accurately and efficiently
Maintain a clean, organized, and safe workspace
Collaborate with your team to hit daily production goals

Requirements

Ability to lift 50 lbs repeatedly
Comfortable being on your feet in a busy warehouse environment
Dependable, punctual, and team-oriented
Completed safety and heat illness prevention training
Willingness to work in varying warehouse temperatures
Work boots and gloves recommended
Basic English language proficiency (spoken and written) required for understanding safety and operational instructions in a fast-paced warehouse environment

Why You'll Enjoy Working Here

Flexible shifts to match your schedule
Fast pay options: Same Day Pay or weekly
Free training and development opportunities
Active, hands-on work — no desk required

{{code}}
```

## Variables

| Variable | Example | Notes |
|----------|---------|-------|
| `{{location}}` | South Brunswick, NJ | City, State |
| `{{pay_rate}}` | $17.50 - 18.50/hr | Per client/location |
| `{{shift_schedule}}` | 10:00 a.m. – 10:00 p.m. | Per client/location |
| `{{code}}` | #OT-WHO-DAY | Tracking code (client-role-shift) |
| `{{job_id}}` | 490642 | FHS job browse ID |
| `{{client_slug}}` | ontrac-final-mile | URL-friendly client name |
| `{{metro_slug}}` | south-brunswick | URL-friendly metro name |

## Code Pattern

`#OT-WHO-DAY` = `{client_abbrev}-{role_abbrev}-{shift_type}`
- OT = OnTrac
- WHO = Warehouse Operative
- DAY = Day shift
