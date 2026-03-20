# Indeed Flex — SOP: FHS Requisition Management

> Source: Operational knowledge — Claudio Santos, 2026-03-19
> Related: `sop-indeed-ad-request.md` (ad creation flow)

## How Requisitions Work

### Data Model

A **requisition** in FHS (joinflex.indeed.com) represents a recruitment request for a specific role at a specific location for a specific client. Each requisition is tied to a **dummy shift** in ACP via a **Job ID**.

```
Dummy Shift (ACP)           Requisition (FHS)
┌──────────────┐            ┌──────────────────┐
│ Job ID       │◄──────────►│ job_id           │
│ (one shift)  │            │ requisition_id   │
│              │            │ client           │
│              │            │ location         │
│              │            │ job_title (role)  │
│              │            │ pay_rate_min/max  │
│              │            │ status           │
│              │            │ rsvps            │
│              │            │ target_rsvps     │
└──────────────┘            └──────────────────┘
```

### Key Rules

1. **One Job ID = One Dummy Shift.** Multiple requisitions can share the same Job ID if they're all tied to the same dummy shift in ACP.

2. **Not every requisition has a target_rsvps.** When target = 0 or blank, it means no target was set — it does NOT mean zero demand. These are typically evergreen or upskilling requisitions.

3. **RSVPs ≠ event RSVPs.** In FHS, "RSVPs" actually means **how many AI interviews have been reviewed** (interview outcomes). This is a platform-specific term that can be confusing.

4. **Multiple requisitions can exist for the same Location + Client + Role.** This happens when:
   - Different pay rates are being tested
   - Different dummy shifts (Job IDs) cover different zip codes or date ranges
   - Requisitions were duplicated for tracking purposes
   - A requisition was paused and a new one created alongside it

5. **The meaningful unit of demand is Location + Client + Role**, not individual requisitions. When analyzing demand, always **sum requisitions** at the Location/Client/Role level.

### Requisition Statuses

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| **open** | Active — ad is running, accepting RSVPs | Monitor performance |
| **auto-paused** | System paused — hit threshold, went stale, or scheduling conflict | **Review required** — reactivate, close, or replace |
| **draft** | Created but not activated — no ad running | **Activate** if demand confirmed, otherwise delete |
| **closed** | Completed or cancelled — no longer active | No action (historical) |
| **rejected** | Rejected during review — never activated | No action (historical) |

### Auto-Pause Triggers

Requisitions are auto-paused when:
- RSVPs reach or exceed the target (filled)
- The linked dummy shift expires in ACP
- No new RSVPs for an extended period (stale)
- System detects a scheduling conflict

**Important:** Auto-paused does NOT mean the demand is gone. It means the system stopped the ad automatically and someone needs to decide what to do next.

## How to Read the Requisition Report

### Export Source
- **System:** FHS (joinflex.indeed.com/us/sourcing/requisitions)
- **Export format:** CSV
- **File pattern:** `requisitions-YYYY-MM-DD-XXXXXX.csv`

### Column Reference

| Column | Description | Notes |
|--------|-------------|-------|
| `last_updated` | Timestamp of last change | Use to identify stale reqs |
| `requisition_id` | Unique ID (FLEX-XXXXX) | Primary key |
| `job_id` | Linked dummy shift ID in ACP | May be blank for new/draft reqs |
| `job_title` | Role name | The role being recruited for |
| `agency` | Always "Indeed" | — |
| `client` | Client company name | Match against funnel data |
| `location` | City, State | Match against market names |
| `pay_rate_min` | Minimum hourly pay | — |
| `pay_rate_max` | Maximum hourly pay | — |
| `pay_type` | Always "PayType.HOURLY" | — |
| `rsvps` | AI interviews reviewed | NOT event RSVPs |
| `target_rsvps` | Target number of interviews | 0 = no target set, not zero demand |
| `status` | Current status | open, auto-paused, draft, closed, rejected |

### Aggregation Rule

**Always aggregate at Location + Client + Role level before analyzing.**

Individual requisitions can have 0 target or 0 RSVPs because they share demand with other reqs for the same Job ID. The sum tells the real story.

Example:
```
Wrong: "FLEX-24286 has 0 RSVPs — no traction"
Right: "Austin / Lettuce Entertain You / Dishwasher has 3 reqs
        totaling 0 RSVPs against 580 target — no traction"
```

## Weekly Requisition Review Process

### Monday: Review Active Demand (during Weekly Ops)

1. **Export** fresh requisition CSV from FHS
2. **Filter** to active statuses: open + auto-paused + draft
3. **Aggregate** by Location > Client > Role
4. **Review** each category:

| Category | Filter | Action |
|----------|--------|--------|
| **Open reqs** | status = open | Check RSVPs vs. target — are we pacing? |
| **Auto-paused** | status = auto-paused | Triage: close if filled, reactivate if still needed, replace if stale |
| **Drafts** | status = draft | Activate if demand confirmed, delete if outdated |
| **Over-filled** | RSVPs >= target | Close or increase target if demand continues |
| **Zero traction** | open + RSVPs = 0 + age > 7 days | Investigate: pay rate? wrong location? ad copy? |
| **No open reqs** | markets with 0 active reqs | Flag to ops: is this intentional or an oversight? |

### Triage Decision Tree for Auto-Paused Reqs

```
Auto-paused requisition
    │
    ├── RSVPs >= Target?
    │   ├── YES → Is demand still active?
    │   │         ├── YES → Increase target, reactivate
    │   │         └── NO  → Close requisition
    │   └── NO  → Was it paused due to stale dummy shift?
    │             ├── YES → Check ACP, extend dummy shift, reactivate
    │             └── NO  → Has it been stale > 14 days?
    │                       ├── YES → Close and create new req if needed
    │                       └── NO  → Reactivate
    │
    └── No Job ID?
        └── Create dummy shift in ACP first, then link and activate
```

### Cross-Reference with Funnel Report

The requisition report should always be read alongside the weekly funnel report:

| Funnel Signal | Requisition Signal | Diagnosis |
|---------------|-------------------|-----------|
| High PlatV, 0 bookings | Open reqs exist | **App UX or awareness problem** — workers are verified but don't see/use the booking feature |
| High PlatV, 0 bookings | No open reqs | **Supply problem** — no shifts to book. Open/reactivate reqs |
| High PlatV, 0 bookings | Only auto-paused reqs | **Stale demand** — reqs expired. Reactivate or create new ones |
| Low accounts | Open reqs with low RSVPs | **Marketing problem** — ads not reaching enough people. Increase budget or improve targeting |
| Low accounts | Open reqs with high RSVPs | **Healthy** — good conversion, may need more volume |
| 0 accounts | Draft reqs only | **Market not launched** — activate drafts and start campaigns |

## Metrics to Track Weekly

| Metric | Formula | Target |
|--------|---------|--------|
| **Active demand** | Count of open + auto-paused reqs | Growing or stable |
| **Fill rate** | Sum RSVPs / Sum target (where target > 0) | 30-60% is healthy |
| **Stale reqs** | Open reqs with 0 RSVPs and age > 7 days | 0 (investigate any) |
| **Auto-paused backlog** | Count of auto-paused reqs | < 10 (triage weekly) |
| **Draft backlog** | Count of draft reqs | < 5 (activate or delete) |
| **Markets with no reqs** | Markets in portfolio with 0 active reqs | 0 (every market should have demand) |
| **Avg reqs per market** | Active reqs / active markets | Track trend |

## Systems

| System | URL | What It Does |
|--------|-----|-------------|
| **FHS** | joinflex.indeed.com/us/sourcing/requisitions | Create, manage, export requisitions |
| **ACP** | admin.indeedflex.com/dashboard | Create dummy shifts (linked via Job ID) |
| **Indeed Employer** | employers.indeed.com/reporting/ads | Campaign performance reporting |

---
*SOP created by Fiona (@funnel-specialist) — 2026-03-19*
*Related: sop-indeed-ad-request.md | weekly-funnel-report-tmpl.md*
