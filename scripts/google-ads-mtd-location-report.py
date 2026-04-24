#!/usr/bin/env python3
"""
Google Ads MTD Location Budget Report
Pulls MTD spend + daily budgets per location and prints a terminal table.
"""

from collections import defaultdict
from datetime import date

from google.ads.googleads.client import GoogleAdsClient

GOOGLE_ADS_YAML = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

LOCATION_STATE_MAP = {
    "dallas": "TX", "ft_worth": "TX", "fort_worth": "TX", "haslet": "TX",
    "arlington": "TX", "austin": "TX", "san_antonio": "TX", "houston": "TX",
    "plano": "TX", "irving": "TX", "desoto": "TX", "garland": "TX",
    "mesquite": "TX", "lancaster": "TX", "flower_mound": "TX", "carrollton": "TX",
    "cedar_park": "TX", "wimberley": "TX", "pasadena": "TX",
    "chicago": "IL", "bedford_park": "IL", "hodgkins": "IL", "joliet": "IL",
    "libertyville": "IL", "bolingbrook": "IL",
    "las_vegas": "NV", "reno": "NV", "sparks": "NV", "mccarran": "NV",
    "logan_township": "NJ", "south_brunswick": "NJ", "paulsboro": "NJ",
    "nashville": "TN", "la_vergne": "TN", "mount_juliet": "TN", "lebanon": "TN",
    "orlando": "FL", "kissimmee": "FL",
    "atlanta": "GA", "hapeville": "GA", "cartersville": "GA",
    "phoenix": "AZ",
    "charlotte": "NC",
    "washington": "DC", "washington_dc": "DC",
    "cincinnati": "OH", "west_chester": "OH", "grove_city": "OH",
    "middleburg_heights": "OH", "fairfield": "OH", "lockbourne": "OH",
    "hebron": "KY",
    "columbus": "OH",
    "monroe": "OH",
    "tennant": "MN", "minneapolis": "MN",
    "bolingbrook": "IL",
}


def micros(v):
    return v / 1_000_000 if v else 0.0


def extract_location(name):
    name_lower = name.lower().replace("-", "_").replace(" ", "_")
    for loc in sorted(LOCATION_STATE_MAP.keys(), key=len, reverse=True):
        if loc in name_lower:
            return loc.replace("_", " ").title()
    parts = name_lower.split("-")
    if len(parts) >= 8:
        candidate = parts[7].replace("_", " ").title()
        if len(candidate) > 2:
            return candidate
    return "Unknown"


def get_state(location):
    return LOCATION_STATE_MAP.get(location.lower().replace(" ", "_"), "??")


def fmt_usd(v):
    return f"${v:,.2f}"


def fmt_pct(v):
    return f"{v:.1f}%"


def main():
    today = date.today()
    days_elapsed = today.day
    days_in_month = 30  # approximate for April

    print(f"\nGoogle Ads — MTD Budget & Performance by Location")
    print(f"Account: {CUSTOMER_ID} | Date: {today} | Days elapsed: {days_elapsed}/{days_in_month}")
    print("=" * 100)

    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga = client.get_service("GoogleAdsService")

    # Query 1: MTD spend per campaign
    q_spend = """
        SELECT
            campaign.id, campaign.name, campaign.status,
            metrics.cost_micros, metrics.impressions, metrics.clicks,
            metrics.conversions, metrics.cost_per_conversion
        FROM campaign
        WHERE campaign.status = 'ENABLED'
        AND segments.date DURING THIS_MONTH
        ORDER BY metrics.cost_micros DESC
    """

    # Query 2: Daily budgets (no date filter — current budgets)
    q_budget = """
        SELECT
            campaign.name,
            campaign_budget.amount_micros,
            campaign_budget.total_amount_micros,
            campaign_budget.status
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """

    # Fetch spend
    campaigns = {}
    print("Fetching MTD spend...")
    for row in ga.search(customer_id=CUSTOMER_ID, query=q_spend):
        cid = row.campaign.id
        cname = row.campaign.name
        if cid not in campaigns:
            campaigns[cid] = {
                "name": cname,
                "location": extract_location(cname),
                "cost": 0.0,
                "impressions": 0,
                "clicks": 0,
                "conversions": 0.0,
                "daily_budget": 0.0,
            }
        campaigns[cid]["cost"] += micros(row.metrics.cost_micros)
        campaigns[cid]["impressions"] += row.metrics.impressions
        campaigns[cid]["clicks"] += row.metrics.clicks
        campaigns[cid]["conversions"] += row.metrics.conversions

    # Fetch budgets
    print("Fetching daily budgets...")
    budgets = {}
    for row in ga.search(customer_id=CUSTOMER_ID, query=q_budget):
        budgets[row.campaign.name] = micros(row.campaign_budget.amount_micros)

    for cid, c in campaigns.items():
        c["daily_budget"] = budgets.get(c["name"], 0.0)

    # Aggregate by location
    locs = defaultdict(lambda: {
        "spend": 0.0, "daily_budget": 0.0, "impressions": 0,
        "clicks": 0, "conversions": 0.0, "n_campaigns": 0
    })
    for c in campaigns.values():
        loc = c["location"]
        locs[loc]["spend"] += c["cost"]
        locs[loc]["daily_budget"] += c["daily_budget"]
        locs[loc]["impressions"] += c["impressions"]
        locs[loc]["clicks"] += c["clicks"]
        locs[loc]["conversions"] += c["conversions"]
        locs[loc]["n_campaigns"] += 1

    # Compute derived metrics
    rows = []
    for loc, d in locs.items():
        monthly_budget = d["daily_budget"] * days_in_month
        expected_spend = d["daily_budget"] * days_elapsed
        pacing_pct = (d["spend"] / expected_spend * 100) if expected_spend > 0 else 0
        budget_util = (d["spend"] / monthly_budget * 100) if monthly_budget > 0 else 0
        cpa = d["spend"] / d["conversions"] if d["conversions"] > 0 else 0
        ctr = (d["clicks"] / d["impressions"] * 100) if d["impressions"] > 0 else 0
        rows.append({
            "location": loc,
            "state": get_state(loc),
            "n": d["n_campaigns"],
            "spend": d["spend"],
            "daily_budget": d["daily_budget"],
            "monthly_budget": monthly_budget,
            "expected_spend": expected_spend,
            "pacing_pct": pacing_pct,
            "budget_util": budget_util,
            "impressions": d["impressions"],
            "clicks": d["clicks"],
            "ctr": ctr,
            "conversions": d["conversions"],
            "cpa": cpa,
        })

    # Sort by spend desc
    rows.sort(key=lambda x: x["spend"], reverse=True)

    # Totals
    total_spend = sum(r["spend"] for r in rows)
    total_budget = sum(r["monthly_budget"] for r in rows)
    total_expected = sum(r["expected_spend"] for r in rows)
    total_conv = sum(r["conversions"] for r in rows)
    total_impr = sum(r["impressions"] for r in rows)
    total_clicks = sum(r["clicks"] for r in rows)

    # Print table
    header = (
        f"{'Location':<22} {'ST':>3} {'Cmp':>4} "
        f"{'Spend MTD':>12} {'Daily Bdgt':>11} {'Mo Budget':>10} "
        f"{'Expected':>10} {'Pacing':>8} {'Mo Util':>8} "
        f"{'Impr':>8} {'Clicks':>7} {'CTR':>6} {'Conv':>6} {'CPA':>9}"
    )
    print(header)
    print("-" * len(header))

    for r in rows:
        # Pacing flag
        if r["pacing_pct"] < 70:
            pace_flag = " ⬇"
        elif r["pacing_pct"] > 110:
            pace_flag = " ⬆"
        else:
            pace_flag = "  "

        print(
            f"{r['location']:<22} {r['state']:>3} {r['n']:>4} "
            f"{fmt_usd(r['spend']):>12} {fmt_usd(r['daily_budget']):>11} {fmt_usd(r['monthly_budget']):>10} "
            f"{fmt_usd(r['expected_spend']):>10} {fmt_pct(r['pacing_pct']):>7}{pace_flag} {fmt_pct(r['budget_util']):>8} "
            f"{r['impressions']:>8,} {r['clicks']:>7,} {fmt_pct(r['ctr']):>6} {r['conversions']:>6.1f} "
            f"{fmt_usd(r['cpa']) if r['cpa'] else 'N/A':>9}"
        )

    print("-" * len(header))
    total_pacing = (total_spend / total_expected * 100) if total_expected > 0 else 0
    total_util = (total_spend / total_budget * 100) if total_budget > 0 else 0
    total_cpa = total_spend / total_conv if total_conv > 0 else 0
    total_ctr = (total_clicks / total_impr * 100) if total_impr > 0 else 0
    print(
        f"{'TOTAL':<22} {'':>3} {len(rows):>4} "
        f"{fmt_usd(total_spend):>12} {'':>11} {fmt_usd(total_budget):>10} "
        f"{fmt_usd(total_expected):>10} {fmt_pct(total_pacing):>8}  {fmt_pct(total_util):>8} "
        f"{total_impr:>8,} {total_clicks:>7,} {fmt_pct(total_ctr):>6} {total_conv:>6.1f} "
        f"{fmt_usd(total_cpa) if total_cpa else 'N/A':>9}"
    )

    print(f"\nLegend: ⬇ Underpacing (<70% of expected) | ⬆ Overpacing (>110% of expected)")
    print(f"Pacing = Actual spend vs expected spend based on {days_elapsed} days elapsed")
    print(f"Mo Budget = Daily budget × {days_in_month} days")
    print()

    # Pacing alerts
    alerts = [r for r in rows if r["pacing_pct"] < 70 or r["pacing_pct"] > 115]
    if alerts:
        print("PACING ALERTS:")
        for r in alerts:
            status = "UNDERPACING" if r["pacing_pct"] < 70 else "OVERPACING"
            print(f"  {status}: {r['location']} ({r['state']}) — {fmt_pct(r['pacing_pct'])} of expected | Spend: {fmt_usd(r['spend'])} vs Expected: {fmt_usd(r['expected_spend'])}")
        print()


if __name__ == "__main__":
    main()
