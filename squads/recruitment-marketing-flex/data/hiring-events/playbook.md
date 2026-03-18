# Hiring Events — Master Playbook

> Source: Las Vegas Mar 11 & 16 events + recruiter feedback (Marcus) + funnel data
> Owner: All squad agents

## What Is a Hiring Event

An in-person event where pre-screened workers come to a physical location to accelerate their onboarding journey. The goal is to compress multiple funnel stages (AI interview, drug test, I-9, shift matching) into a single session.

**Core metric:** Workers cleared for shifts / Total invited

## When to Run a Hiring Event

| Trigger | Example |
|---------|---------|
| High pipeline, low conversion | 400+ accounts created but <10% reaching shifts |
| New market launch | Opening a new city with no existing worker base |
| Client surge request | Client needs 100+ workers in 2 weeks |
| Fill rate crisis | <15% fill rate on high-target requisition |
| Stagnant verified-to-booked | Workers verified but not booking shifts |

## Event Types

| Type | Duration | Target Attendees | Focus |
|------|----------|-----------------|-------|
| **Full Onboarding** | 4-6 hours | 50-100 invited | AI interview + DT + I-9 + shift matching |
| **DT & Verification Only** | 2-3 hours | 30-50 invited | Workers already interviewed, need DT/docs |
| **Hiring Fair** | Full day | 100+ invited | Multi-client, multi-role, open to public |
| **Client-Specific** | 3-4 hours | 30-80 invited | Single client (e.g., CORT or Stord only) |

## Planning Timeline

| When | Action | Owner |
|------|--------|-------|
| **2 weeks before** | Select date, venue, target market | RM team + ops |
| **10 days before** | Pull invite list from pipeline (verified but not booked) | RM team |
| **7 days before** | Send initial invite (email + SMS + app notification) | CRM specialist |
| **5 days before** | Build Google Sheet check-in from invite list | RM team |
| **3 days before** | Send reminder with venue address + what to bring | CRM specialist |
| **1 day before** | Final reminder, confirm venue setup, signage ready | RM team + ops |
| **Day of** | Execute event, track check-ins, resolve issues | Full team |
| **1 day after** | Compile results, write post-mortem | Analyst / Funnel specialist |
| **3 days after** | Follow up with no-shows (reschedule or re-engage) | CRM specialist |

## Pre-Event Requirements

### For Workers (communicate clearly in invite)
- [ ] Complete AI interview BEFORE arriving (critical — prevents bottleneck)
- [ ] Bring valid government ID (for I-9)
- [ ] Be prepared for drug test
- [ ] Know which role/client they're interested in

### For the Team
- [ ] Venue booked with private rooms for interviews (if needed)
- [ ] Indeed Flex signage at entrance and inside
- [ ] Google Sheet check-in list pre-built from invite list
- [ ] Recruiting team on standby for manual interview approvals
- [ ] Drug test supplies ready
- [ ] Company phone available for I-9 verification (not personal devices)
- [ ] Laptop/tablet stations for workers to complete app steps on-site
- [ ] Wi-Fi access confirmed

## Known Issues & Workarounds

### AI Interview Scheduling Conflict (CRITICAL)
**Problem:** Workers who have pre-scheduled AI interviews in the app are BLOCKED from doing an on-the-spot interview at the event.

**Workaround:** Worker must cancel their scheduled interview via the confirmation email → reopen app → select "Interview Now."

**Prevention:** Require AI interview completion BEFORE the event. Make this explicit in all communications: "You must complete your AI interview before attending."

### Workers Expect In-Person Interviews
**Problem:** Almost every worker arrives expecting a human interview, defeating the purpose of the AI interview convenience.

**Prevention:** Set expectations clearly in invite: "This is NOT an interview event — it's a verification & shift matching event. Complete your AI interview before arriving."

### Privacy for AI Interviews
**Problem:** If workers do need to interview on-site, they need private space. Some request to step outside or sit in their car.

**Solution:** Book venue with 2-3 private meeting rooms. If not available, designate quiet corners or allow car interviews.

### Low DT-Only Traffic
**Observation:** Only ~2-5% of attendees come specifically for drug testing.

**Implication:** Don't market events as "DT events" — they're full onboarding acceleration events.

### Venue Address Changes
**Impact:** Address changes reduce attendance significantly.

**Prevention:** Confirm venue 2+ weeks ahead, never change last-minute. If must change, send 3+ notifications.

## Check-In Process

1. Worker arrives → check name against Google Sheet
2. Verify AI interview status (completed? or needs workaround?)
3. If interview complete → proceed to DT
4. If interview NOT complete → direct to private room for on-site interview OR have recruiter manually approve
5. DT administered → result logged in Sheet
6. I-9 verification (if applicable)
7. Shift matching discussion → assign client/shift preference
8. Worker marked as "cleared" in Sheet

## Metrics to Track

| Metric | Formula | Target |
|--------|---------|--------|
| **Show Rate** | Arrived / Invited | > 50% |
| **Completion Rate** | DT Passed / Arrived | > 90% |
| **Clearance Rate** | Workers Cleared / Arrived | > 85% |
| **No-Show Rate** | 1 - Show Rate | < 50% |
| **Cost per Cleared Worker** | Total event cost / Workers cleared | < $50 |
| **Time-to-Clear** | Avg minutes from check-in to cleared | < 45 min |

## Post-Event Reporting

Every event should produce a post-mortem with:
1. Numbers: Invited, Arrived, DT Passed, Cleared, No-Shows
2. Show rate by time slot
3. Client/role preference split
4. Issues encountered + resolution
5. Recruiter feedback
6. Recommendations for next event
7. Cost analysis (venue + staff time + materials vs workers cleared)

Template: `docs/context/las-vegas-hiring-events-march-2026.md` (reference)

## Follow-Up Strategy

### No-Shows (within 3 days)
- SMS: "We missed you at the event! You can still complete your onboarding — here's how..."
- Email: Recap what they missed + link to complete AI interview online
- Re-invite to next event if scheduled

### Attendees Who Didn't Complete
- SMS: "You're almost there! Just one more step to start working..."
- Direct outreach from recruiter for manual resolution

### Cleared Workers Who Haven't Booked
- Push notification: "Shifts available near you — book your first one now!"
- Monitor in Tableau: if not booked within 7 days, escalate to ops
