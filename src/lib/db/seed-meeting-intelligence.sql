-- Seed: Meeting Intelligence Data — March 2026
-- Source: 8 meetings (2026-03-11 to 2026-03-18)
-- Run after: meeting-intelligence-schema.sql

-- =============================================================================
-- MEETINGS
-- =============================================================================
INSERT INTO meetings (date, title, type, attendees, file_path, summary) VALUES
('2026-03-11', 'FHS Non-Member RSVP Communication', 'ad_hoc', '["Claudio","FHS Contact"]', 'docs/meetings/2026-03-11-fhs-non-member-rsvp.md', 'Braze ID gap for ad-generated RSVPs — need alternative send method'),
('2026-03-11', 'Hiring Event Planning — Las Vegas', 'working_session', '["Carlos","Claudio","David","Brett","Marcus","Jordan"]', 'docs/meetings/2026-03-11-hiring-event-planning-vegas.md', 'LV event logistics: 2 rooms, AI interview flow, drug testing, 92 RSVPs'),
('2026-03-11', 'Hiring Event Setup & Virtual Lobby', 'working_session', '["Ben","Claudio","Carlos","Marcos","David","Eric","Leia","Brett","Angela","Lilian","Mason","Liv"]', 'docs/meetings/2026-03-11-hiring-event-setup-virtual-lobby.md', 'QR code deep link issue, AI lobby confirmed, FHS address automation conflict'),
('2026-03-11', 'Las Vegas Venue Change & Comms', 'ad_hoc', '["Craig","Claudio","Ben","Lily","Olivia"]', 'docs/meetings/2026-03-11-vegas-venue-change-comms.md', 'Urgent venue change for 192 RSVPs; FHS SMS only viable channel for ad-generated contacts'),
('2026-03-12', 'Weekly Regional Ops & Pipeline Review', 'pipeline_review', '["Julia","Brad","Brett","Grant","Steffi","Leah","Craig","James","Sander","Leonie","Austin","Lily"]', 'docs/meetings/2026-03-12-weekly-regional-ops-review.md', 'Dallas FIFA/Dos Equis, Nashville CTDI+AQL, Chicago PowerStop fixed, Bath Concepts pipeline'),
('2026-03-13', 'Recruitment Ops & Process Alignment', 'ops_sync', '["Craig","Claudio","Olivia"]', 'docs/meetings/2026-03-13-craig-claudio-olivia-ops.md', 'RACI need, workload crisis, FHS cleanup, revenue team misalignment'),
('2026-03-13', 'One-on-One Carlos & Claudio', 'one_on_one', '["Carlos","Claudio"]', 'docs/meetings/2026-03-13-one-on-one-carlos-claudio.md', 'Revenue call issues, SXSW/SoHo performance, $61K spend, $40K waste estimate'),
('2026-03-13', 'Strategy Review (Carlos)', 'strategy', '["Carlos","Claudio","Craig"]', 'docs/meetings/2026-03-13-strategy-review-carlos.md', 'RACI framework, recruiter empowerment, $40K+ waste, Spanish app, system integration gaps'),
('2026-03-17', 'Claudio-Craig Team Sync', 'ops_sync', '["Claudio","Craig"]', 'docs/meetings/2026-03-17-claudio-craig-sync.md', 'Verification rate crashed to 22%, process gaps post-Mason, Jess integration'),
('2026-03-18', 'Reddit Strategy Session (Elder)', 'vendor', '["Elder","Claudio"]', 'docs/meetings/2026-03-18-reddit-strategy-session.md', 'Reddit Max (-17% CPA), AppsFlyer integration needed, AM assigned, campaign structure issues'),
('2026-03-18', 'US RM & Operations Sync', 'ops_sync', '["Olivia","Jess","Craig","Ameera","Angela","Leah","Arnie","Leona"]', 'docs/meetings/2026-03-18-us-rm-ops-sync.md', 'Dallas quality, Atlanta 300 churn, LV events, FIFA, US Open, Reddit AM, interview questions');

-- =============================================================================
-- SPEND SNAPSHOTS
-- =============================================================================
INSERT INTO spend_snapshots (meeting_id, period, channel, amount, captured_at, context) VALUES
(7, 'monthly', 'indeed', 36000, '2026-03-13', 'Primary channel — 30-40% budget share'),
(7, 'monthly', 'google', 20000, '2026-03-13', 'Search + PMax + Display'),
(7, 'monthly', 'reddit', 5000, '2026-03-13', '~5% of Google budget; no conversion tracking'),
(7, 'monthly', 'total', 61000, '2026-03-13', 'Estimated total across all channels'),
(7, 'monthly', 'waste', 40000, '2026-03-13', 'Carlos estimate — conservative; 65.6% waste rate'),
(7, 'weekly', 'indeed', 1000, '2026-03-13', 'SoHo Austin — 95% above competition'),
(7, 'daily', 'google', 400, '2026-03-13', 'SXSW Austin hospitality only');

-- =============================================================================
-- MEETING METRICS
-- =============================================================================
INSERT INTO meeting_metrics (meeting_id, metric_name, metric_value, metric_unit, previous_value, delta, market, context, captured_at) VALUES
-- Funnel metrics
(9, 'apply_to_verified_rate', 22.0, 'percent', 56.0, -34.0, NULL, 'Crashed after Mason departure — no one manually re-verifying', '2026-03-17'),
(11, 'hospitality_pass_rate', 53.0, 'percent', 75.0, -22.0, NULL, '75% was abnormally high; 53% normalizing. 30 questions vs 17 industrial', '2026-03-18'),
(7, 'sxsw_accounts_created', 200.0, 'count', NULL, NULL, 'Austin', '30-day performance', '2026-03-13'),
(7, 'sxsw_verified', 148.0, 'count', NULL, NULL, 'Austin', '74% account-to-verified (above average)', '2026-03-13'),
(7, 'sxsw_ready_to_book', 68.0, 'count', NULL, NULL, 'Austin', '34% account-to-ready — workers not booking shifts', '2026-03-13'),
(7, 'soho_weekly_interviews', 15.0, 'count', NULL, NULL, 'Austin', 'Only 7 conversions', '2026-03-13'),
(7, 'soho_offers_sent', 453.0, 'count', NULL, NULL, 'Austin', 'For 1 position — massive waste', '2026-03-13'),
-- Hiring event metrics
(11, 'lv_event_show_rate', 48.0, 'percent', NULL, NULL, 'Las Vegas', '89 arrived from 187 invited across 2 events', '2026-03-18'),
(11, 'lv_event_dt_pass_rate', 96.0, 'percent', NULL, NULL, 'Las Vegas', '85 of 89 arrivals passed drug test', '2026-03-18'),
(11, 'lv_event_total_cleared', 91.0, 'count', NULL, NULL, 'Las Vegas', '85 DT pass + 6 walk-in DT', '2026-03-18'),
-- Outreach metrics
(11, 'security_outreach_conversion', 42.0, 'percent', NULL, NULL, NULL, '40+ RSVPs from 96 contacts — very strong', '2026-03-18'),
(11, 'fifa_credentialing_list', 215.0, 'count', 87.0, 128.0, NULL, 'Workers who authorized info sharing for FIFA', '2026-03-18'),
(11, 'austin_hospitality_interviews', 150.0, 'count', NULL, NULL, 'Austin', 'Weekly — improvement from previous month', '2026-03-18'),
(11, 'atlanta_churn_eligible', 300.0, 'count', NULL, NULL, 'Atlanta', '400+ total across all store locations', '2026-03-18'),
-- PowerStop fix
(5, 'powerstop_fill_rate', 100.0, 'percent', 25.0, 75.0, 'Chicago', '20/20 filled (was 5/20) — switched to individual bookings', '2026-03-12');

-- =============================================================================
-- MARKET SIGNALS
-- =============================================================================
INSERT INTO market_signals (meeting_id, market, signal_type, severity, description, recommended_action) VALUES
(9, 'all', 'process_blocker', 'critical', 'Apply-to-verified rate crashed 56%→22% after Mason departure. ~$26K/month extra cost.', 'Clarify verification criteria with recruitment leadership immediately'),
(8, 'all', 'process_blocker', 'critical', 'No centralized weekly priority guidance. Team feels lost. $40K+/month estimated waste.', 'Build consolidated priority reporting tool. Use ACP 7-14 day outlook interim'),
(11, 'Dallas', 'quality_issue', 'critical', 'Hospitality quality crisis. Culinaire: quality>quantity. Gates US Open + Washington + NYC.', 'Multi-channel with quality filters, $100 referral, bi-weekly events, training videos'),
(11, 'Logan Township NJ', 'deadline_pressure', 'high', '130 flex workers needed by 2026-04-06 for OnTrac expansion.', 'Surge NJ warehouse recruitment'),
(5, 'Dallas', 'demand_spike', 'high', 'Dos Equis 39 days/35 workers + FIFA credentialing + Johnstone forklift gap.', 'Three concurrent Dallas demands — prioritize by deadline'),
(11, 'Atlanta', 'churn_alert', 'high', '~300 ATL candidates eligible to return. 400+ total across store locations.', 'Complete list cleanup → deploy churn Braze campaign to all locations'),
(7, 'Austin', 'competition_change', 'high', 'SXSW volunteer badge ($2,000 value) competing with hourly pay. SoHo: 453 offers, 1 needed.', 'Cannot compete with badge. Focus SoHo post-SXSW'),
(11, 'UK', 'expansion', 'high', 'Enterprise clients flex transition 2026-04-01. Olivia sole UK RM person.', 'Olivia → Roxy meeting. Activate dormant UK workers'),
(11, 'Las Vegas', 'positive_momentum', 'medium', 'Hiring events working: 48% show, 96% DT pass, 91 cleared. But 3-day notice too short.', 'Create monthly event calendar. Consolidate to 9 AM + 2 PM slots'),
(5, 'Chicago', 'positive_momentum', 'medium', 'PowerStop fixed 5/20→20/20. Bath Concepts new pipeline 30-40 reps.', 'Maintain momentum. Fresh recruitment pool needed for clerical'),
(5, 'Nashville', 'expansion', 'medium', 'CTDI ramp April (20-30). AQL new client LaVergne (~30/day eventual).', 'Monitor capacity — Ingram also ramping in same area'),
(11, 'New York', 'expansion', 'medium', 'US Open Aug-Sep 2026 with Restaurant Associates. Credentialing needed.', 'Begin credentialing early. Premium event attracts quality workers');

-- =============================================================================
-- DECISIONS
-- =============================================================================
INSERT INTO decisions (meeting_id, decision_text, rationale, impact, category, decided_by) VALUES
(11, 'Maintain 30-question hospitality interview structure', 'Quality > volume. 25% qualifying + 16-17 skill-based questions. Increase top-of-funnel instead of reducing rigor.', 'Need 51% more top-of-funnel traffic to compensate', 'quality', 'Leah + Team'),
(3, 'AI-driven interviews at hiring events (not live recruiter)', 'Simplifies setup: one requisition handles Spanish + English natively. No new lobby needed.', 'Reduced event setup complexity', 'process', 'Team'),
(6, 'Venue sourcing is NOT recruitment marketing responsibility', 'Marketing team absorbing logistics outside core scope. Summer/ops team should own.', 'Boundary set — protects RM bandwidth', 'process', 'Carlos'),
(8, 'Fulfillment > budget concerns (Azul directive)', '"Fulfillment is all that matters. Nothing else matters." — despite $40K+ waste estimate.', 'Spend continues. Focus on effectiveness not cost cutting.', 'budget', 'Azul'),
(6, 'Two-week grace period for Carlos + Leah before formal RACI', 'New leaders need time to understand teams. Target ~2026-03-27 for formal process discussion.', 'Delays process improvements but respects transition', 'team_structure', 'Olivia + Team'),
(11, 'Churn communications will go to ALL store locations', 'Not just Atlanta — 400+ eligible across all sites.', 'Broader re-engagement reach', 'strategy', 'Craig + Angela'),
(5, 'PowerStop shifted from block to individual bookings', 'Block booking required same workers all days — too restrictive. Individual bookings resolved fill rate.', 'Fill rate: 5/20 → 20/20', 'process', 'Grant + Client');
