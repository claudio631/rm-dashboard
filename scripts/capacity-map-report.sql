-- ============================================================================
-- Capacity Map Report
-- Purpose: Market-level worker supply vs. job demand → ad priority ranking
-- Sources:
--   - workers         ← WORKER_LIST_US_ACTIVE_LAST_30_DAYS_*.csv
--   - requisitions    ← requisitions-*.csv
-- Database: SQLite
-- Usage:
--   sqlite3 :memory: -init capacity-map-report.sql
--   (after loading CSVs via .import or a Python loader)
-- ============================================================================

-- ============================================================================
-- Step 1: Market zone definitions
-- Each row defines a metro area bounding box (±lat/lon degrees from center)
-- 0.36° lat ≈ 25 miles · lon delta adjusted per latitude
-- ============================================================================
WITH market_zones_raw AS (
    -- market                         lat_center   lon_center  lat_delta  lon_delta
    -- ── Claudio's markets ──────────────────────────────────────────────────────
    SELECT 'Austin, TX'          AS market, 30.2672 AS lat_c, -97.7431 AS lon_c, 0.40 AS lat_d, 0.46 AS lon_d UNION ALL
    SELECT 'Houston, TX',                   29.7604,           -95.3698,          0.40,           0.46 UNION ALL
    SELECT 'Charlotte, NC',                 35.2271,           -80.8431,          0.36,           0.44 UNION ALL
    SELECT 'Fort Mill, SC',                 35.0074,           -80.9428,          0.36,           0.44 UNION ALL
    SELECT 'Orlando, FL',                   28.5383,           -81.3792,          0.36,           0.41 UNION ALL
    SELECT 'Las Vegas, NV',                 36.1699,          -115.1398,          0.36,           0.45 UNION ALL
    SELECT 'Reno, NV',                      39.5296,          -119.8138,          0.36,           0.47 UNION ALL
    SELECT 'Washington, DC',                38.9072,           -77.0369,          0.36,           0.46 UNION ALL
    SELECT 'Monroe, OH',                    39.4367,           -84.3616,          0.30,           0.38 UNION ALL
    SELECT 'Phoenix, AZ',                   33.4484,          -112.0740,          0.40,           0.48 UNION ALL
    SELECT 'Logan Township, NJ',            39.5831,           -75.3949,          0.30,           0.38 UNION ALL
    -- ── High-demand markets (from requisitions analysis) ──────────────────────
    SELECT 'Fort Worth, TX',                32.7555,           -97.3308,          0.36,           0.43 UNION ALL
    SELECT 'Haslet, TX',                    32.9668,           -97.5466,          0.25,           0.32 UNION ALL
    SELECT 'Lebanon, TN',                   36.2082,           -86.2911,          0.25,           0.31 UNION ALL
    SELECT 'Bedford Park, IL',              41.7700,           -87.8500,          0.25,           0.34 UNION ALL
    SELECT 'South Brunswick, NJ',           40.3688,           -74.5338,          0.25,           0.32 UNION ALL
    SELECT 'Grove City, OH',                39.8820,           -83.0938,          0.25,           0.32 UNION ALL
    SELECT 'Flower Mound, TX',              33.0145,           -97.0969,          0.25,           0.31 UNION ALL
    SELECT 'Cedar Park, TX',                30.5052,           -97.8203,          0.25,           0.31 UNION ALL
    SELECT 'Atlanta, GA',                   33.7490,           -84.3880,          0.40,           0.48 UNION ALL
    SELECT 'McCarran, NV',                  36.0700,          -115.1500,          0.25,           0.32 UNION ALL
    SELECT 'West Chester, OH',              39.3254,           -84.4282,          0.25,           0.32 UNION ALL
    SELECT 'Irving, TX',                    32.8140,           -96.9489,          0.25,           0.31 UNION ALL
    SELECT 'DeSoto, TX',                    32.5896,           -96.8572,          0.25,           0.31 UNION ALL
    SELECT 'Cartersville, GA',              34.1648,           -84.7999,          0.25,           0.31
),
market_zones AS (
    SELECT market,
           lat_c                AS lat_center,
           lon_c                AS lon_center,
           lat_c - lat_d        AS lat_min,
           lat_c + lat_d        AS lat_max,
           lon_c - lon_d        AS lon_min,
           lon_c + lon_d        AS lon_max
    FROM market_zones_raw
),

-- ============================================================================
-- Step 2: Worker supply per market
-- Count active workers (not banned) by verify status within each market zone
-- ============================================================================
worker_supply AS (
    SELECT
        mz.market,
        COUNT(*)                                                    AS total_workers,
        SUM(CASE WHEN w.VERIFY_STATUS = 'Verified'   THEN 1 ELSE 0 END) AS verified_workers,
        SUM(CASE WHEN w.VERIFY_STATUS = 'Unverified' THEN 1 ELSE 0 END) AS unverified_workers
    FROM market_zones mz
    JOIN workers w
      ON  CAST(w.WORKER_LATITUDE  AS REAL) BETWEEN mz.lat_min AND mz.lat_max
      AND CAST(w.WORKER_LONGITUDE AS REAL) BETWEEN mz.lon_min AND mz.lon_max
      AND w.COUNTRY_CODE = 'US'
      AND w.BANNED_FLAG  = 'N'
      AND w.WORKER_LATITUDE  IS NOT NULL
      AND w.WORKER_LONGITUDE IS NOT NULL
    GROUP BY mz.market
),

-- ============================================================================
-- Step 3: Job demand per market
-- Normalize location strings before grouping to merge common variants:
--   "Houston , TX" → "Houston, TX"
--   "Washington, DC, WA" / "Washington, D.C., WA" / "Washington, D.C" → "Washington, DC"
--   "West Chester Oh, OH" → "West Chester, OH"
--   "Haslet , TX" → "Haslet, TX"
-- ============================================================================
location_normalized AS (
    SELECT
        CASE
            WHEN LOWER(TRIM(location)) LIKE '%washington%dc%'
              OR LOWER(TRIM(location)) LIKE '%washington%d.c%'
              OR (LOWER(TRIM(location)) LIKE 'washington,%' AND LOWER(location) NOT LIKE '%pa%')
                 THEN 'Washington, DC'
            WHEN LOWER(TRIM(location)) LIKE 'houston %,%'
                 THEN 'Houston, TX'
            WHEN LOWER(TRIM(location)) LIKE 'haslet %,%'
                 THEN 'Haslet, TX'
            WHEN LOWER(TRIM(location)) LIKE 'nashville %,%'
                 THEN 'Nashville, TN'
            WHEN LOWER(TRIM(location)) LIKE '%west chester oh%'
                 THEN 'West Chester, OH'
            ELSE TRIM(location)
        END AS market,
        target_rsvps,
        rsvps,
        status
    FROM requisitions
    WHERE status IN ('open', 'draft')
      AND TRIM(location) != ''
      AND location IS NOT NULL
),
job_demand AS (
    SELECT
        market,
        COUNT(*)                                AS open_jobs,
        SUM(CAST(target_rsvps AS INTEGER))     AS target_workers,
        SUM(CAST(rsvps        AS INTEGER))     AS filled_workers
    FROM location_normalized
    GROUP BY market
),

-- ============================================================================
-- Step 4: Capacity map — join supply and demand, compute gap and priority
-- ============================================================================
capacity_map AS (
    SELECT
        COALESCE(jd.market, ws.market)          AS market,

        -- Demand side
        COALESCE(jd.open_jobs,       0)          AS open_jobs,
        COALESCE(jd.target_workers,  0)          AS target_workers,
        COALESCE(jd.filled_workers,  0)          AS filled_workers,
        COALESCE(jd.target_workers, 0)
          - COALESCE(jd.filled_workers, 0)       AS unfilled_demand,

        -- Supply side
        COALESCE(ws.verified_workers,   0)       AS verified_workers,
        COALESCE(ws.unverified_workers, 0)       AS unverified_workers,
        COALESCE(ws.total_workers,      0)       AS total_workers,

        -- Gap: workers still needed vs. verified supply
        (COALESCE(jd.target_workers, 0)
          - COALESCE(jd.filled_workers, 0))
          - COALESCE(ws.verified_workers, 0)     AS net_gap,

        -- Fill rate: % of target already filled
        CASE WHEN COALESCE(jd.target_workers, 0) > 0
             THEN ROUND(100.0 * COALESCE(jd.filled_workers, 0)
                        / COALESCE(jd.target_workers, 1), 1)
             ELSE NULL
        END                                      AS fill_rate_pct,

        -- Coverage ratio: verified workers per unfilled slot
        CASE WHEN (COALESCE(jd.target_workers, 0) - COALESCE(jd.filled_workers, 0)) > 0
             THEN ROUND(
                    CAST(COALESCE(ws.verified_workers, 0) AS REAL)
                    / (COALESCE(jd.target_workers, 0) - COALESCE(jd.filled_workers, 0))
                  , 2)
             ELSE NULL
        END                                      AS coverage_ratio,

        -- Ad priority: HIGH = high unfilled demand + low coverage
        -- Score: unfilled_demand × (1 - coverage_ratio), capped at 0
        CASE
            WHEN (COALESCE(jd.target_workers, 0) - COALESCE(jd.filled_workers, 0)) <= 0
                 THEN 'NO_NEED'
            WHEN COALESCE(ws.verified_workers, 0) = 0
                 THEN 'CRITICAL'
            WHEN ROUND(CAST(COALESCE(ws.verified_workers, 0) AS REAL)
                       / (COALESCE(jd.target_workers, 0) - COALESCE(jd.filled_workers, 0)), 2) < 0.25
                 THEN 'HIGH'
            WHEN ROUND(CAST(COALESCE(ws.verified_workers, 0) AS REAL)
                       / (COALESCE(jd.target_workers, 0) - COALESCE(jd.filled_workers, 0)), 2) < 0.75
                 THEN 'MEDIUM'
            ELSE 'LOW'
        END                                      AS ad_priority

    FROM job_demand jd
    LEFT JOIN worker_supply ws ON LOWER(TRIM(ws.market)) = LOWER(TRIM(jd.market))

    UNION ALL

    -- Markets with workers but no open requisitions (low demand)
    SELECT
        ws.market,
        0, 0, 0, 0,
        ws.verified_workers,
        ws.unverified_workers,
        ws.total_workers,
        0 - ws.verified_workers,   -- surplus (negative gap)
        NULL,
        NULL,
        'SURPLUS'
    FROM worker_supply ws
    WHERE NOT EXISTS (
        SELECT 1 FROM job_demand jd
        WHERE LOWER(TRIM(jd.market)) = LOWER(TRIM(ws.market))
    )
)

-- ============================================================================
-- Final output: Capacity Map Report
-- Sorted by ad priority (CRITICAL → HIGH → MEDIUM → LOW → SURPLUS → NO_NEED)
-- ============================================================================
SELECT
    market,
    ad_priority,
    open_jobs,
    target_workers,
    filled_workers,
    unfilled_demand,
    verified_workers,
    total_workers,
    net_gap,
    COALESCE(CAST(fill_rate_pct AS TEXT) || '%', '—')   AS fill_rate,
    COALESCE(CAST(coverage_ratio AS TEXT), '—')          AS coverage_ratio
FROM capacity_map
ORDER BY
    CASE ad_priority
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH'     THEN 2
        WHEN 'MEDIUM'   THEN 3
        WHEN 'LOW'      THEN 4
        WHEN 'SURPLUS'  THEN 5
        WHEN 'NO_NEED'  THEN 6
        ELSE 7
    END,
    net_gap DESC;
