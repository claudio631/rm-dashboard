# Indeed Flex — US Landing Pages by Role

> Source: `W2A Worker Journey Project.xlsx` — imported 2026-03-17
> Landing pages are role-specific URLs used in campaign UTM links.

## Published Landing Pages (Active)

### Industrial

| Role | 2025 Shifts | Landing Page |
|------|------------|-------------|
| **Warehouse Operative** | 129,153 | `indeedflex.com/find-jobs/lp/warehouse-operative/` |
| **Picker Packer** | 84,229 | `indeedflex.com/find-jobs/lp/picker-packer/` |
| **Assembler** | 30,376 | `indeedflex.com/find-jobs/lp/assembler/` |
| **Loader / Crew** | 21,081 | `indeedflex.com/find-jobs/industrial/lp-loader-crew-member-jobs/` |
| **Forklift Driver** | 16,244 | `indeedflex.com/find-jobs/lp/forklift-driver/` |
| **Industrial General Labor** | 8,589 | `indeedflex.com/find-jobs/lp/industrial-general-labor/` |
| **Repair Technician** | 8,456 | `indeedflex.com/find-jobs/lp/repair-technician/` |
| **Industrial Team Lead** | 3,250 | `indeedflex.com/find-jobs/lp/team-lead/` |
| **Machine Operator** | 1,579 | `indeedflex.com/find-jobs/lp/machine-operator/` |
| **Warehouse Clerk** | 1,185 | `indeedflex.com/find-jobs/lp/warehouse-clerk/` |
| **Material Handler** | 170 | `indeedflex.com/find-jobs/lp/material-handler` |

### Hospitality

| Role | 2025 Shifts | Landing Page |
|------|------------|-------------|
| **Event Staff** | 2,167 | `indeedflex.com/find-jobs/hospitality/lp-event-staff/` |
| **Hospitality General Labor** | 675 | `indeedflex.com/find-jobs/lp/hospitality-general-labor/` |
| **Server** | 723 | `indeedflex.com/find-jobs/lp/server/` |
| **Concession Stand Worker** | 576 | `indeedflex.com/find-jobs/lp/concession-stand-worker/` |
| **Line Cook** | 401 | `indeedflex.com/find-jobs/lp/line-cook/` |
| **Housekeeper** | 197 | `indeedflex.com/find-jobs/lp/housekeeper/` |
| **Dishwasher** | 139 | `indeedflex.com/find-jobs/lp/dishwasher` |
| **Busser** | 87 | `indeedflex.com/find-jobs/lp/busser/` |
| **Bartender** | 32 | `indeedflex.com/find-jobs/lp/bartender/` |
| **Host** | 28 | `indeedflex.com/find-jobs/lp/host` |
| **Prep Cook** | 15 | `indeedflex.com/find-jobs/lp/prep-cook/` |
| **Hospitality Team Lead** | 1 | `indeedflex.com/find-jobs/lp/hospitality-team-lead/` |

### Other

| Role | 2025 Shifts | Landing Page |
|------|------------|-------------|
| **Administrative Assistant** | 1,006 | `indeedflex.com/find-jobs/lp/admin-assistant` |
| **Barista** | 27 | `indeedflex.com/find-jobs/lp/` (generic) |

## Roles WITHOUT Published Landing Pages (using generic LP)

These roles fall back to the generic `indeedflex.com/find-jobs/lp/` page:

| Role | 2025 Shifts | Status |
|------|------------|--------|
| FM General Labor | 6,408 | NOT published |
| Parking Services Rep | 4,145 | NOT published |
| Event Student Worker Guard | 3,270 | NOT published |
| PTS Pick up Student Worker | 2,292 | NOT published |
| Customer Service Representative | 1,589 | NOT published |
| Event Student Worker Cashier | 1,115 | NOT published |
| Sure Walk Student Worker | 864 | NOT published |
| Brand Ambassador | 628 | NOT published |
| Assistant Supervisor | 552 | NOT published |
| CDL Driver | 194 | NOT published |
| Delivery Driver 1 | 166 | NOT published |
| Data Entry Specialist | 132 | NOT published |

## URL Pattern

```
https://indeedflex.com/find-jobs/lp/{{role_slug}}/
```

With UTM parameters:
```
?utm_source={{source}}&utm_medium=cpc&link_value=syft://jobs/browse/{{job_browse_id}}&employer={{client_slug}}&metro={{metro_slug}}&role={{role_slug}}&utm_campaign={{campaign_name}}
```

### Special URL patterns
- Loader/Crew uses `/industrial/` path: `indeedflex.com/find-jobs/industrial/lp-loader-crew-member-jobs/`
- Event Staff uses `/hospitality/` path: `indeedflex.com/find-jobs/hospitality/lp-event-staff/`
- Most roles use flat `/lp/` path: `indeedflex.com/find-jobs/lp/{role-slug}/`

## Volume Summary

| Category | Roles with LP | Roles without LP | Total Shifts (with LP) |
|----------|--------------|-----------------|----------------------|
| Industrial | 11 | 3 | 304,312 |
| Hospitality | 12 | 2 | 5,041 |
| Other | 1 | 10+ | 1,006 |
| **Total** | **24 published** | **15+ generic** | **310,359** |

## Implications for PPC Manager AI

1. **UTM Builder** must use the correct LP URL per role — the role-to-LP mapping is critical
2. **12 high-volume roles** without dedicated LPs are using the generic page (conversion opportunity)
3. **LP URL validation** should be part of campaign creation QA (broken link = wasted spend)
4. **`link_value` parameter** uses `syft://` deep link format for Indeed Flex app — essential for app attribution via AppsFlyer
