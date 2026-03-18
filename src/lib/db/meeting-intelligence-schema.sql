-- Meeting Intelligence Schema — RM Team AI
-- Author: Dara (@data-engineer) · 2026-03-18
-- Database: SQLite (MVP) → Postgres (production)
-- Purpose: Structured storage for meeting data, action items, metrics, and market signals

-- =============================================================================
-- MEETINGS — Core meeting records
-- =============================================================================
CREATE TABLE IF NOT EXISTS meetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    title TEXT NOT NULL,
    type TEXT CHECK(type IN ('ops_sync', 'strategy', 'one_on_one', 'working_session', 'pipeline_review', 'vendor', 'ad_hoc')) NOT NULL,
    attendees TEXT NOT NULL,                     -- JSON array of names
    file_path TEXT NOT NULL,                     -- relative path to docs/meetings/
    summary TEXT,
    duration_minutes INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- ACTION_ITEMS — Extracted from meetings, trackable over time
-- =============================================================================
CREATE TABLE IF NOT EXISTS action_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id),
    item_number INTEGER NOT NULL,                -- sequential within action plan
    description TEXT NOT NULL,
    owner TEXT NOT NULL,                          -- person responsible
    priority TEXT CHECK(priority IN ('P0', 'P1', 'P2', 'P3')) NOT NULL,
    category TEXT CHECK(category IN (
        'campaign_launch', 'budget', 'hiring_event', 'churn_reengagement',
        'process_improvement', 'system_integration', 'training', 'credentialing',
        'market_expansion', 'tool_automation', 'team_structure', 'vendor_management',
        'other'
    )) NOT NULL DEFAULT 'other',
    market TEXT,                                  -- NULL = all markets
    client TEXT,                                  -- NULL = all clients
    deadline DATE,
    status TEXT CHECK(status IN ('open', 'in_progress', 'completed', 'blocked', 'cancelled')) NOT NULL DEFAULT 'open',
    blocked_by TEXT,                              -- description of blocker
    depends_on_id INTEGER REFERENCES action_items(id),  -- dependency chain
    completed_at DATETIME,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- MEETING_METRICS — Quantitative data points extracted from meetings
-- =============================================================================
CREATE TABLE IF NOT EXISTS meeting_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id),
    metric_name TEXT NOT NULL,                    -- e.g., 'apply_to_verified_rate'
    metric_value REAL NOT NULL,                   -- numeric value
    metric_unit TEXT NOT NULL,                    -- 'percent', 'usd', 'count', 'ratio', 'days'
    previous_value REAL,                          -- for trend analysis
    delta REAL,                                   -- calculated: value - previous_value
    market TEXT,                                  -- NULL = overall
    client TEXT,                                  -- NULL = all clients
    channel TEXT,                                 -- NULL = all channels
    context TEXT,                                 -- additional context
    captured_at DATE NOT NULL,                    -- when the metric was observed
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- MARKET_SIGNALS — Qualitative signals about market health from meetings
-- =============================================================================
CREATE TABLE IF NOT EXISTS market_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id),
    market TEXT NOT NULL,
    signal_type TEXT CHECK(signal_type IN (
        'demand_spike', 'demand_drop', 'quality_issue', 'churn_alert',
        'new_client', 'client_lost', 'competition_change', 'venue_issue',
        'staffing_gap', 'process_blocker', 'positive_momentum', 'expansion',
        'deadline_pressure'
    )) NOT NULL,
    severity TEXT CHECK(severity IN ('critical', 'high', 'medium', 'low')) NOT NULL,
    description TEXT NOT NULL,
    recommended_action TEXT,
    resolved_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- DECISIONS — Formal decisions captured from meetings
-- =============================================================================
CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id),
    decision_text TEXT NOT NULL,
    rationale TEXT,
    impact TEXT,                                  -- description of expected impact
    reversible INTEGER DEFAULT 1,                 -- 0 = irreversible
    decided_by TEXT,                              -- person who made the call
    category TEXT CHECK(category IN (
        'strategy', 'process', 'budget', 'quality', 'staffing',
        'technology', 'client', 'channel', 'team_structure', 'other'
    )) NOT NULL DEFAULT 'other',
    supersedes_id INTEGER REFERENCES decisions(id),  -- if this overrides a prior decision
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- SPEND_SNAPSHOTS — Ad spend data captured per meeting/period
-- =============================================================================
CREATE TABLE IF NOT EXISTS spend_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INTEGER REFERENCES meetings(id),
    period TEXT NOT NULL,                          -- 'monthly', 'weekly', 'daily'
    channel TEXT NOT NULL,                         -- 'indeed', 'google', 'reddit', 'meta', 'craigslist', 'total'
    amount REAL NOT NULL,                          -- USD
    market TEXT,                                   -- NULL = all
    client TEXT,                                   -- NULL = all
    context TEXT,                                  -- e.g., "95% above competition"
    captured_at DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- INDEXES — Optimized for common query patterns
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_action_items_status ON action_items(status);
CREATE INDEX IF NOT EXISTS idx_action_items_owner ON action_items(owner);
CREATE INDEX IF NOT EXISTS idx_action_items_priority ON action_items(priority);
CREATE INDEX IF NOT EXISTS idx_action_items_market ON action_items(market);
CREATE INDEX IF NOT EXISTS idx_action_items_deadline ON action_items(deadline);
CREATE INDEX IF NOT EXISTS idx_meeting_metrics_name ON meeting_metrics(metric_name);
CREATE INDEX IF NOT EXISTS idx_meeting_metrics_market ON meeting_metrics(market);
CREATE INDEX IF NOT EXISTS idx_meeting_metrics_captured ON meeting_metrics(captured_at);
CREATE INDEX IF NOT EXISTS idx_market_signals_market ON market_signals(market);
CREATE INDEX IF NOT EXISTS idx_market_signals_severity ON market_signals(severity);
CREATE INDEX IF NOT EXISTS idx_decisions_category ON decisions(category);
CREATE INDEX IF NOT EXISTS idx_spend_snapshots_channel ON spend_snapshots(channel);

-- =============================================================================
-- VIEWS — Pre-built queries for common analysis
-- =============================================================================

-- Open action items by owner with priority
CREATE VIEW IF NOT EXISTS v_open_actions_by_owner AS
SELECT
    owner,
    priority,
    COUNT(*) as item_count,
    GROUP_CONCAT(id) as item_ids
FROM action_items
WHERE status IN ('open', 'in_progress')
GROUP BY owner, priority
ORDER BY
    CASE priority WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 WHEN 'P3' THEN 3 END,
    owner;

-- Market health dashboard (latest signals)
CREATE VIEW IF NOT EXISTS v_market_health AS
SELECT
    ms.market,
    ms.severity,
    ms.signal_type,
    ms.description,
    m.date as signal_date,
    ms.resolved_at,
    CASE WHEN ms.resolved_at IS NULL THEN 'ACTIVE' ELSE 'RESOLVED' END as status
FROM market_signals ms
JOIN meetings m ON ms.meeting_id = m.id
WHERE ms.resolved_at IS NULL
ORDER BY
    CASE ms.severity WHEN 'critical' THEN 0 WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 END,
    m.date DESC;

-- Metric trends (latest vs. previous for each metric)
CREATE VIEW IF NOT EXISTS v_metric_trends AS
SELECT
    metric_name,
    market,
    metric_value as current_value,
    previous_value,
    delta,
    metric_unit,
    context,
    captured_at
FROM meeting_metrics
ORDER BY captured_at DESC, metric_name;

-- Spend by channel (latest snapshot)
CREATE VIEW IF NOT EXISTS v_spend_by_channel AS
SELECT
    channel,
    amount,
    period,
    market,
    context,
    captured_at
FROM spend_snapshots
ORDER BY captured_at DESC, amount DESC;

-- Overdue action items
CREATE VIEW IF NOT EXISTS v_overdue_actions AS
SELECT
    ai.id,
    ai.description,
    ai.owner,
    ai.priority,
    ai.deadline,
    julianday('now') - julianday(ai.deadline) as days_overdue,
    m.title as source_meeting,
    m.date as meeting_date
FROM action_items ai
JOIN meetings m ON ai.meeting_id = m.id
WHERE ai.status IN ('open', 'in_progress')
  AND ai.deadline < date('now')
ORDER BY ai.priority, ai.deadline;
