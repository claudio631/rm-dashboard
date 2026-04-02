#!/usr/bin/env python3
"""
Google Ads Dashboard Generator
Pulls data from Google Ads API and cross-references with FHS requisitions
and revenue requests to generate a comprehensive HTML dashboard.
"""

import csv
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, date

from google.ads.googleads.client import GoogleAdsClient

# ── Config ──────────────────────────────────────────────────────────────
GOOGLE_ADS_YAML = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
US_ACCOUNT = "7236100723"
REVENUE_REQUESTS_CSV = "/Users/claudio.santos/Downloads/US_Recruitment_Requests__us_ (2).csv"
REQUISITIONS_CSV = "/Users/claudio.santos/Downloads/requisitions-2026-03-25-892929.csv"
OUTPUT_HTML = "/Users/claudio.santos/RM-Team-Ai/docs/reports/google-ads-dashboard-2026-03-27.html"

# Location → State mapping
LOCATION_STATE_MAP = {
    "dallas": "TX", "ft_worth": "TX", "fort_worth": "TX", "haslet": "TX",
    "arlington": "TX", "austin": "TX", "san_antonio": "TX", "houston": "TX",
    "plano": "TX", "irving": "TX", "desoto": "TX", "garland": "TX",
    "mesquite": "TX", "lancaster": "TX", "flower_mound": "TX", "carrollton": "TX",
    "cedar_park": "TX", "wimberley": "TX", "pasadena": "TX",
    "chicago": "IL", "bedford_park": "IL", "hodgkins": "IL", "joliet": "IL",
    "libertyville": "IL",
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
}

# ── Helpers ─────────────────────────────────────────────────────────────

def micros_to_dollars(micros):
    """Convert micros to dollars."""
    return micros / 1_000_000 if micros else 0.0


def extract_campaign_type(name):
    """Extract campaign type from campaign name."""
    name_lower = name.lower()
    if "p_max" in name_lower or "pmax" in name_lower:
        return "PMax"
    elif "search" in name_lower:
        return "Search"
    elif "display" in name_lower:
        return "Display"
    elif "app" in name_lower:
        return "App"
    else:
        return "Other"


def extract_location(name):
    """Extract location from campaign name."""
    name_lower = name.lower().replace("-", "_").replace(" ", "_")
    # Try to find known locations in the name
    # Sort by length descending to match longer names first (e.g., "south_brunswick" before "south")
    sorted_locs = sorted(LOCATION_STATE_MAP.keys(), key=len, reverse=True)
    for loc in sorted_locs:
        if loc in name_lower:
            return loc.replace("_", " ").title()
    # Fallback: try pattern extraction
    # p-b2c-google-{type}-us-{funnel}-bau-{location}-...
    parts = name_lower.split("-")
    if len(parts) >= 8:
        # Try position 7 (0-indexed) for location
        candidate = parts[7].replace("_", " ").title()
        if len(candidate) > 2:
            return candidate
    return "Unknown"


def get_state_for_location(location):
    """Get state for a location name."""
    loc_key = location.lower().replace(" ", "_")
    return LOCATION_STATE_MAP.get(loc_key, "??")


def fmt_currency(val):
    """Format as currency."""
    if val >= 1000:
        return f"${val:,.0f}"
    return f"${val:,.2f}"


def fmt_number(val):
    """Format number with commas."""
    if isinstance(val, float):
        return f"{val:,.1f}"
    return f"{val:,}"


def parse_city_state(location_str):
    """Parse city and state from various CSV location formats."""
    if not location_str:
        return None, None
    loc = location_str.strip().strip('"')
    # Handle "City, ST" or "City, State, Zip" or "ST, City, Zip"
    parts = [p.strip() for p in loc.split(",")]
    city = None
    state = None
    for p in parts:
        p_clean = p.strip()
        # Check if it's a state abbreviation (2 letters)
        if re.match(r'^[A-Z]{2}$', p_clean):
            state = p_clean
        elif p_clean in ("D.C.", "D.C", "DC"):
            state = "DC"
        elif re.match(r'^\d{5}', p_clean):
            continue  # zip code
        elif not city and len(p_clean) > 2:
            city = p_clean
        elif not state and len(p_clean) == 2:
            state = p_clean.upper()

    # Fix state from known text
    if not state and city:
        c = city.lower().replace(" ", "_")
        state = LOCATION_STATE_MAP.get(c)

    # Fix common misparses
    if state == "WA" and city and "washington" in city.lower():
        state = "DC"

    return city, state


# ── Data Loading ────────────────────────────────────────────────────────

def load_google_ads_data():
    """Pull all 3 queries from Google Ads API."""
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    # Query 1: Campaign metrics this month
    query1 = """
        SELECT
            campaign.id, campaign.name, campaign.status,
            campaign.campaign_budget,
            metrics.cost_micros, metrics.impressions, metrics.clicks,
            metrics.conversions, metrics.cost_per_conversion
        FROM campaign
        WHERE campaign.status = 'ENABLED'
        AND segments.date DURING THIS_MONTH
        ORDER BY metrics.cost_micros DESC
    """

    # Query 2: Daily breakdown
    query2 = """
        SELECT
            segments.date,
            campaign.name,
            metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions
        FROM campaign
        WHERE campaign.status = 'ENABLED'
        AND segments.date DURING THIS_MONTH
        ORDER BY segments.date DESC
    """

    # Query 3: Campaign budgets
    query3 = """
        SELECT
            campaign.name,
            campaign_budget.amount_micros,
            campaign_budget.status
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """

    campaigns = {}
    daily_data = []
    budgets = {}

    # Execute Query 1
    print("Pulling campaign metrics (Query 1)...")
    response1 = ga_service.search(customer_id=US_ACCOUNT, query=query1)
    for row in response1:
        cid = row.campaign.id
        cname = row.campaign.name
        if cid not in campaigns:
            campaigns[cid] = {
                "id": cid,
                "name": cname,
                "status": row.campaign.status.name if hasattr(row.campaign.status, 'name') else str(row.campaign.status),
                "cost": 0,
                "impressions": 0,
                "clicks": 0,
                "conversions": 0.0,
                "type": extract_campaign_type(cname),
                "location": extract_location(cname),
            }
        campaigns[cid]["cost"] += row.metrics.cost_micros
        campaigns[cid]["impressions"] += row.metrics.impressions
        campaigns[cid]["clicks"] += row.metrics.clicks
        campaigns[cid]["conversions"] += row.metrics.conversions

    # Execute Query 2
    print("Pulling daily spend breakdown (Query 2)...")
    response2 = ga_service.search(customer_id=US_ACCOUNT, query=query2)
    for row in response2:
        daily_data.append({
            "date": row.segments.date,
            "campaign": row.campaign.name,
            "cost_micros": row.metrics.cost_micros,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "conversions": row.metrics.conversions,
        })

    # Execute Query 3
    print("Pulling campaign budgets (Query 3)...")
    response3 = ga_service.search(customer_id=US_ACCOUNT, query=query3)
    for row in response3:
        cname = row.campaign.name
        budgets[cname] = {
            "daily_budget_micros": row.campaign_budget.amount_micros,
            "budget_status": row.campaign_budget.status.name if hasattr(row.campaign_budget.status, 'name') else str(row.campaign_budget.status),
        }

    # Merge budget into campaigns
    for cid, camp in campaigns.items():
        if camp["name"] in budgets:
            camp["daily_budget"] = micros_to_dollars(budgets[camp["name"]]["daily_budget_micros"])
        else:
            camp["daily_budget"] = 0.0

    # Convert cost from micros
    for cid in campaigns:
        campaigns[cid]["cost_dollars"] = micros_to_dollars(campaigns[cid]["cost"])
        if campaigns[cid]["clicks"] > 0 and campaigns[cid]["conversions"] > 0:
            campaigns[cid]["cpa"] = campaigns[cid]["cost_dollars"] / campaigns[cid]["conversions"]
        else:
            campaigns[cid]["cpa"] = 0.0

    # Compute days elapsed in month
    today = date.today()
    days_elapsed = today.day  # days 1..today

    return campaigns, daily_data, budgets, days_elapsed


def load_revenue_requests():
    """Load revenue requests CSV and filter Live status."""
    requests = []
    try:
        with open(REVENUE_REQUESTS_CSV, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = row.get("Request Status", "")
                if "Live" in status:
                    location = row.get("Location (City, State, Zip)", "")
                    city, state = parse_city_state(location)
                    hc = row.get("Headcount needed", "0")
                    try:
                        hc_num = int(hc) if hc else 0
                    except ValueError:
                        hc_num = 0
                    requests.append({
                        "client": row.get("Client - Job", ""),
                        "location_raw": location,
                        "city": city,
                        "state": state,
                        "role": row.get("Role", ""),
                        "hc_needed": hc_num,
                        "status": status,
                        "actions": row.get("Current Actions", ""),
                    })
    except FileNotFoundError:
        print(f"WARNING: Revenue requests file not found: {REVENUE_REQUESTS_CSV}")
    return requests


def load_requisitions():
    """Load FHS requisitions CSV and filter open status."""
    reqs = []
    try:
        with open(REQUISITIONS_CSV, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                status = row.get("status", "")
                if status in ("open", "draft"):
                    location = row.get("location", "")
                    city, state = parse_city_state(location)
                    rsvps = row.get("rsvps", "0")
                    target = row.get("target_rsvps", "0")
                    try:
                        rsvps_num = int(float(rsvps)) if rsvps else 0
                    except ValueError:
                        rsvps_num = 0
                    try:
                        target_num = int(float(target)) if target else 0
                    except ValueError:
                        target_num = 0
                    reqs.append({
                        "requisition_id": row.get("requisition_id", ""),
                        "job_title": row.get("job_title", ""),
                        "client": row.get("client", ""),
                        "location_raw": location,
                        "city": city,
                        "state": state,
                        "rsvps": rsvps_num,
                        "target_rsvps": target_num,
                        "status": status,
                    })
    except FileNotFoundError:
        print(f"WARNING: Requisitions file not found: {REQUISITIONS_CSV}")
    return reqs


# ── Analysis ────────────────────────────────────────────────────────────

def analyze_by_type(campaigns):
    """Aggregate metrics by campaign type."""
    types = defaultdict(lambda: {"spend": 0, "impressions": 0, "clicks": 0, "conversions": 0, "count": 0})
    for c in campaigns.values():
        t = c["type"]
        types[t]["spend"] += c["cost_dollars"]
        types[t]["impressions"] += c["impressions"]
        types[t]["clicks"] += c["clicks"]
        types[t]["conversions"] += c["conversions"]
        types[t]["count"] += 1
    # Compute CPA
    for t in types:
        if types[t]["conversions"] > 0:
            types[t]["cpa"] = types[t]["spend"] / types[t]["conversions"]
        else:
            types[t]["cpa"] = 0.0
    return dict(types)


def analyze_by_location(campaigns):
    """Aggregate metrics by location, grouped by state."""
    locs = defaultdict(lambda: {"spend": 0, "impressions": 0, "clicks": 0, "conversions": 0, "count": 0, "daily_budget": 0})
    for c in campaigns.values():
        loc = c["location"]
        locs[loc]["spend"] += c["cost_dollars"]
        locs[loc]["impressions"] += c["impressions"]
        locs[loc]["clicks"] += c["clicks"]
        locs[loc]["conversions"] += c["conversions"]
        locs[loc]["count"] += 1
        locs[loc]["daily_budget"] += c["daily_budget"]
    # CPA
    for loc in locs:
        if locs[loc]["conversions"] > 0:
            locs[loc]["cpa"] = locs[loc]["spend"] / locs[loc]["conversions"]
        else:
            locs[loc]["cpa"] = 0.0
        locs[loc]["state"] = get_state_for_location(loc)
    return dict(locs)


def analyze_budget_utilization(campaigns, days_elapsed):
    """Compute budget utilization per location."""
    loc_budgets = defaultdict(lambda: {"daily_budget": 0, "total_spend": 0, "campaigns": []})
    for c in campaigns.values():
        loc = c["location"]
        loc_budgets[loc]["daily_budget"] += c["daily_budget"]
        loc_budgets[loc]["total_spend"] += c["cost_dollars"]
        loc_budgets[loc]["campaigns"].append(c["name"])

    results = {}
    for loc, data in loc_budgets.items():
        avg_daily = data["total_spend"] / days_elapsed if days_elapsed > 0 else 0
        if data["daily_budget"] > 0:
            utilization = (avg_daily / data["daily_budget"]) * 100
        else:
            utilization = 0
        results[loc] = {
            "daily_budget": data["daily_budget"],
            "total_spend": data["total_spend"],
            "avg_daily_spend": avg_daily,
            "utilization": utilization,
            "state": get_state_for_location(loc),
            "num_campaigns": len(data["campaigns"]),
        }
    return results


def gap_analysis(campaigns, revenue_requests, requisitions):
    """Cross-reference ad locations with demand locations."""
    # Build set of ad locations (normalized)
    ad_locations = {}
    for c in campaigns.values():
        loc = c["location"].lower().replace(" ", "_")
        if loc not in ad_locations:
            ad_locations[loc] = {"daily_budget": 0, "spend": 0, "campaigns": 0}
        ad_locations[loc]["daily_budget"] += c["daily_budget"]
        ad_locations[loc]["spend"] += c["cost_dollars"]
        ad_locations[loc]["campaigns"] += 1

    # Collect demand locations from revenue requests
    demand = {}
    for rr in revenue_requests:
        city = rr["city"]
        if not city:
            continue
        key = city.lower().replace(" ", "_")
        if key not in demand:
            demand[key] = {
                "city": city,
                "state": rr["state"] or "??",
                "clients": set(),
                "hc_needed": 0,
                "fhs_rsvps": 0,
                "req_count": 0,
            }
        demand[key]["clients"].add(rr["client"].split(" - ")[0].strip() if " - " in rr["client"] else rr["client"])
        demand[key]["hc_needed"] += rr["hc_needed"]

    # Add requisition locations
    for req in requisitions:
        city = req["city"]
        if not city:
            continue
        key = city.lower().replace(" ", "_")
        if key not in demand:
            demand[key] = {
                "city": city,
                "state": req["state"] or "??",
                "clients": set(),
                "hc_needed": 0,
                "fhs_rsvps": 0,
                "req_count": 0,
            }
        demand[key]["clients"].add(req["client"])
        demand[key]["fhs_rsvps"] += req["rsvps"]
        demand[key]["req_count"] += 1

    # Cross-reference
    gap_rows = []
    for loc_key, d in demand.items():
        ad = ad_locations.get(loc_key)
        # Also try partial matches
        if not ad:
            for ak in ad_locations:
                if ak in loc_key or loc_key in ak:
                    ad = ad_locations[ak]
                    break

        if not ad:
            status = "none"
            daily_budget = 0
            rec = "Launch Google Ads campaign"
        elif ad["daily_budget"] < 30:
            status = "low"
            daily_budget = ad["daily_budget"]
            rec = f"Increase budget (currently ${daily_budget:.0f}/day)"
        else:
            status = "good"
            daily_budget = ad["daily_budget"]
            rec = "Monitoring - budget adequate"

        gap_rows.append({
            "city": d["city"],
            "state": d["state"],
            "clients": ", ".join(sorted(d["clients"]))[:80],
            "hc_needed": d["hc_needed"],
            "fhs_rsvps": d["fhs_rsvps"],
            "req_count": d["req_count"],
            "ad_status": status,
            "daily_budget": daily_budget,
            "recommendation": rec,
        })

    # Sort: none first, then low, then good
    order = {"none": 0, "low": 1, "good": 2}
    gap_rows.sort(key=lambda x: (order.get(x["ad_status"], 3), -x["hc_needed"]))
    return gap_rows


# ── HTML Generation ─────────────────────────────────────────────────────

def generate_html(campaigns, daily_data, budgets, days_elapsed,
                  revenue_requests, requisitions):
    """Generate the full HTML dashboard."""
    type_data = analyze_by_type(campaigns)
    loc_data = analyze_by_location(campaigns)
    budget_data = analyze_budget_utilization(campaigns, days_elapsed)
    gap_rows = gap_analysis(campaigns, revenue_requests, requisitions)

    # KPI totals
    total_spend = sum(c["cost_dollars"] for c in campaigns.values())
    total_campaigns = len(campaigns)
    total_conversions = sum(c["conversions"] for c in campaigns.values())
    avg_cpa = total_spend / total_conversions if total_conversions > 0 else 0
    locations_covered = len(set(c["location"] for c in campaigns.values() if c["location"] != "Unknown"))
    total_impressions = sum(c["impressions"] for c in campaigns.values())
    total_clicks = sum(c["clicks"] for c in campaigns.values())

    # Type chart max for bar width
    max_type_spend = max((v["spend"] for v in type_data.values()), default=1)

    # Type colors
    type_colors = {
        "Search": "#2563eb",
        "PMax": "#7c3aed",
        "App": "#059669",
        "Display": "#ea580c",
        "Other": "#6b7280",
    }

    # Build type bars HTML
    type_bars_html = ""
    for t_name in ["Search", "PMax", "App", "Display", "Other"]:
        if t_name not in type_data:
            continue
        td = type_data[t_name]
        pct = (td["spend"] / max_type_spend * 100) if max_type_spend > 0 else 0
        color = type_colors.get(t_name, "#6b7280")
        cpa_str = fmt_currency(td["cpa"]) if td["cpa"] > 0 else "N/A"
        ctr = (td["clicks"] / td["impressions"] * 100) if td["impressions"] > 0 else 0
        type_bars_html += f"""
        <div class="type-row">
            <div class="type-label">{t_name} <span class="type-count">({td['count']} campaigns)</span></div>
            <div class="type-bar-container">
                <div class="type-bar" style="width: {pct:.1f}%; background: {color};">
                    {fmt_currency(td['spend'])}
                </div>
            </div>
            <div class="type-metrics">
                <span>{fmt_number(td['impressions'])} imp</span>
                <span>{fmt_number(td['clicks'])} clicks</span>
                <span>{ctr:.1f}% CTR</span>
                <span>{td['conversions']:.0f} conv</span>
                <span>CPA: {cpa_str}</span>
            </div>
        </div>"""

    # Location table rows grouped by state
    state_groups = defaultdict(list)
    for loc, data in loc_data.items():
        state_groups[data["state"]].append((loc, data))

    # Sort states by total spend descending
    state_totals = {}
    for state, locs in state_groups.items():
        state_totals[state] = sum(d["spend"] for _, d in locs)

    sorted_states = sorted(state_totals.keys(), key=lambda s: state_totals[s], reverse=True)

    loc_table_rows = ""
    for state in sorted_states:
        locs = state_groups[state]
        locs.sort(key=lambda x: x[1]["spend"], reverse=True)
        st_spend = sum(d["spend"] for _, d in locs)
        st_imp = sum(d["impressions"] for _, d in locs)
        st_clicks = sum(d["clicks"] for _, d in locs)
        st_conv = sum(d["conversions"] for _, d in locs)
        st_cpa = st_spend / st_conv if st_conv > 0 else 0
        st_count = sum(d["count"] for _, d in locs)

        loc_table_rows += f"""
        <tr class="state-row">
            <td colspan="2"><strong>{state}</strong></td>
            <td><strong>{st_count}</strong></td>
            <td><strong>{fmt_currency(st_spend)}</strong></td>
            <td><strong>{fmt_number(st_imp)}</strong></td>
            <td><strong>{fmt_number(st_clicks)}</strong></td>
            <td><strong>{st_conv:.0f}</strong></td>
            <td><strong>{fmt_currency(st_cpa) if st_cpa > 0 else 'N/A'}</strong></td>
        </tr>"""

        for loc, data in locs:
            spend_class = ""
            if data["spend"] > 5000:
                spend_class = "high-spend"
            elif data["spend"] > 1000:
                spend_class = "mid-spend"
            else:
                spend_class = "low-spend"
            cpa = fmt_currency(data["cpa"]) if data["cpa"] > 0 else "N/A"
            loc_table_rows += f"""
        <tr class="{spend_class}">
            <td></td>
            <td>{loc}</td>
            <td>{data['count']}</td>
            <td>{fmt_currency(data['spend'])}</td>
            <td>{fmt_number(data['impressions'])}</td>
            <td>{fmt_number(data['clicks'])}</td>
            <td>{data['conversions']:.0f}</td>
            <td>{cpa}</td>
        </tr>"""

    # Budget utilization table
    budget_rows = ""
    sorted_budget = sorted(budget_data.items(), key=lambda x: x[1]["utilization"])
    for loc, bd in sorted_budget:
        flag = ""
        row_class = ""
        if bd["utilization"] < 50:
            flag = " underspend-flag"
            row_class = "underspend"
        elif bd["utilization"] > 90:
            flag = " maxed-flag"
            row_class = "maxed"

        budget_rows += f"""
        <tr class="{row_class}">
            <td>{loc}</td>
            <td>{bd['state']}</td>
            <td>{bd['num_campaigns']}</td>
            <td>{fmt_currency(bd['daily_budget'])}</td>
            <td>{fmt_currency(bd['avg_daily_spend'])}</td>
            <td class="{flag.strip()}">{bd['utilization']:.0f}%</td>
        </tr>"""

    # Gap analysis table
    gap_table_rows = ""
    no_ads_count = 0
    low_budget_count = 0
    good_count = 0
    for g in gap_rows:
        if g["ad_status"] == "none":
            icon = '<span style="font-size:18px">&#x1F534;</span>'
            status_text = "No Campaign"
            row_class = "gap-red"
            no_ads_count += 1
        elif g["ad_status"] == "low":
            icon = '<span style="font-size:18px">&#x1F7E1;</span>'
            status_text = "Low Budget"
            row_class = "gap-yellow"
            low_budget_count += 1
        else:
            icon = '<span style="font-size:18px">&#x1F7E2;</span>'
            status_text = "Active"
            row_class = "gap-green"
            good_count += 1

        budget_str = fmt_currency(g["daily_budget"]) if g["daily_budget"] > 0 else "-"

        gap_table_rows += f"""
        <tr class="{row_class}">
            <td>{g['city']}</td>
            <td>{g['state']}</td>
            <td>{g['clients']}</td>
            <td>{g['hc_needed']}</td>
            <td>{g['fhs_rsvps']}</td>
            <td>{icon} {status_text}</td>
            <td>{budget_str}</td>
            <td>{g['recommendation']}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Ads Dashboard — 2026-03-27</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f3f4f6; font-size: 14px; color: #111827; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); color: white; padding: 24px 32px; }}
        .header h1 {{ font-size: 22px; font-weight: 700; }}
        .header p {{ font-size: 13px; opacity: 0.85; margin-top: 4px; }}

        /* KPI Cards */
        .kpi-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; padding: 20px 32px; }}
        .kpi-card {{ background: white; border-radius: 12px; padding: 16px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }}
        .kpi-card .number {{ font-size: 28px; font-weight: 800; line-height: 1.2; }}
        .kpi-card .label {{ font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }}
        .kpi-card.blue .number {{ color: #2563eb; }}
        .kpi-card.green .number {{ color: #22c55e; }}
        .kpi-card.amber .number {{ color: #f59e0b; }}
        .kpi-card.red .number {{ color: #ef4444; }}
        .kpi-card.purple .number {{ color: #7c3aed; }}

        /* Sections */
        .section {{ margin: 0 32px 24px; background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }}
        .section-title {{ background: #1e3a5f; color: white; padding: 12px 20px; font-size: 15px; font-weight: 600; }}

        /* Type bars */
        .type-chart {{ padding: 20px; }}
        .type-row {{ margin-bottom: 16px; }}
        .type-label {{ font-weight: 600; font-size: 14px; margin-bottom: 4px; }}
        .type-count {{ font-weight: 400; color: #6b7280; font-size: 12px; }}
        .type-bar-container {{ background: #e5e7eb; border-radius: 6px; height: 32px; overflow: hidden; }}
        .type-bar {{ height: 100%; border-radius: 6px; color: white; font-weight: 700; font-size: 13px; display: flex; align-items: center; padding-left: 12px; min-width: 80px; transition: width 0.5s; }}
        .type-metrics {{ display: flex; gap: 16px; font-size: 12px; color: #6b7280; margin-top: 4px; }}
        .type-metrics span {{ white-space: nowrap; }}

        /* Tables */
        .table-scroll {{ overflow-y: auto; max-height: 600px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th {{ position: sticky; top: 0; z-index: 10; background: #1e3a5f; color: white; padding: 8px 10px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; white-space: nowrap; text-align: left; }}
        td {{ padding: 7px 10px; border-bottom: 1px solid #e5e7eb; vertical-align: middle; }}
        tr:hover {{ background: #f9fafb; }}

        /* State rows */
        .state-row {{ background: #eff6ff; }}
        .state-row td {{ border-bottom: 2px solid #2563eb; }}

        /* Spend coloring */
        .high-spend td:nth-child(4) {{ color: #dc2626; font-weight: 600; }}
        .mid-spend td:nth-child(4) {{ color: #d97706; }}
        .low-spend td:nth-child(4) {{ color: #6b7280; }}

        /* Budget flags */
        .underspend td {{ background: #fef3c7; }}
        .underspend-flag {{ color: #d97706; font-weight: 700; }}
        .maxed td {{ background: #fee2e2; }}
        .maxed-flag {{ color: #dc2626; font-weight: 700; }}

        /* Gap analysis */
        .gap-red td {{ background: #fef2f2; }}
        .gap-yellow td {{ background: #fffbeb; }}
        .gap-green td {{ background: #f0fdf4; }}

        /* Legend */
        .legend {{ margin: 8px 20px 16px; display: flex; gap: 20px; font-size: 12px; color: #6b7280; flex-wrap: wrap; }}
        .legend span {{ display: inline-flex; align-items: center; gap: 4px; }}
        .dot {{ width: 10px; height: 10px; border-radius: 3px; display: inline-block; }}

        .footer {{ text-align: center; padding: 16px; color: #9ca3af; font-size: 11px; }}

        /* ===== PRINT / PDF STYLES ===== */
        @media print {{
            @page {{
                size: landscape;
                margin: 12mm 10mm;
            }}
            body {{ background: white; font-size: 11pt; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}

            /* Remove scroll constraints — show full tables */
            .table-scroll {{ overflow: visible; max-height: none; }}

            /* Each section starts on a new page */
            .section {{ break-inside: avoid; page-break-inside: avoid; margin: 0 0 12px; box-shadow: none; border: 1px solid #d1d5db; }}
            .section:nth-child(n+2) {{ break-before: page; page-break-before: always; }}

            /* Keep header compact */
            .header {{ padding: 12px 16px; }}
            .header h1 {{ font-size: 18pt; }}
            .header p {{ font-size: 9pt; }}

            /* KPI grid: force single row, readable sizes */
            .kpi-grid {{ padding: 12px 16px; gap: 10px; }}
            .kpi-card {{ padding: 10px 12px; box-shadow: none; border: 1px solid #d1d5db; }}
            .kpi-card .number {{ font-size: 20pt; }}
            .kpi-card .label {{ font-size: 8pt; }}

            /* Tables: readable column sizing */
            table {{ font-size: 9pt; width: 100%; table-layout: auto; }}
            th {{ font-size: 8pt; padding: 5px 6px; background: #1e3a5f !important; color: white !important; }}
            td {{ padding: 4px 6px; font-size: 9pt; }}

            /* Sticky headers off for print */
            th {{ position: static; }}

            /* Don't break rows across pages */
            tr {{ break-inside: avoid; page-break-inside: avoid; }}

            /* Legend readable */
            .legend {{ font-size: 9pt; }}

            /* Type chart bars */
            .type-label {{ font-size: 10pt; }}
            .type-bar {{ font-size: 9pt; min-width: 60px; }}
            .type-metrics {{ font-size: 9pt; }}

            /* Footer */
            .footer {{ font-size: 8pt; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Google Ads Dashboard — Indeed Flex US</h1>
        <p>Generated 2026-03-27 | Account: 723-610-0723 | MTD data ({days_elapsed} days elapsed) | Cross-referenced with Revenue Requests + FHS Requisitions</p>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="number">{fmt_currency(total_spend)}</div>
            <div class="label">Total Spend MTD</div>
        </div>
        <div class="kpi-card purple">
            <div class="number">{total_campaigns}</div>
            <div class="label">Active Campaigns</div>
        </div>
        <div class="kpi-card amber">
            <div class="number">{fmt_currency(avg_cpa)}</div>
            <div class="label">Avg CPA</div>
        </div>
        <div class="kpi-card green">
            <div class="number">{locations_covered}</div>
            <div class="label">Locations Covered</div>
        </div>
        <div class="kpi-card red">
            <div class="number">{no_ads_count}</div>
            <div class="label">Locations w/ No Ads</div>
        </div>
    </div>

    <!-- Section 1: Cost by Campaign Type -->
    <div class="section">
        <div class="section-title">Section 1: Cost Breakdown by Campaign Type</div>
        <div class="type-chart">
            {type_bars_html}
        </div>
    </div>

    <!-- Section 2: Spend by Location/State -->
    <div class="section">
        <div class="section-title">Section 2: Spend by Location / State</div>
        <div class="legend">
            <span><span class="dot" style="background:#dc2626"></span> High spend (&gt;$5K)</span>
            <span><span class="dot" style="background:#d97706"></span> Mid spend ($1K-$5K)</span>
            <span><span class="dot" style="background:#6b7280"></span> Low spend (&lt;$1K)</span>
        </div>
        <div class="table-scroll">
            <table>
                <thead>
                    <tr>
                        <th>State</th>
                        <th>Location</th>
                        <th># Campaigns</th>
                        <th>Spend</th>
                        <th>Impressions</th>
                        <th>Clicks</th>
                        <th>Conversions</th>
                        <th>CPA</th>
                    </tr>
                </thead>
                <tbody>
                    {loc_table_rows}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Section 3: Daily Budget per Location -->
    <div class="section">
        <div class="section-title">Section 3: Daily Budget Utilization per Location</div>
        <div class="legend">
            <span><span class="dot" style="background:#d97706"></span> Underspending (&lt;50% utilization)</span>
            <span><span class="dot" style="background:#dc2626"></span> Maxed out (&gt;90% utilization)</span>
        </div>
        <div class="table-scroll">
            <table>
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>State</th>
                        <th># Campaigns</th>
                        <th>Daily Budget</th>
                        <th>Avg Daily Spend</th>
                        <th>Utilization %</th>
                    </tr>
                </thead>
                <tbody>
                    {budget_rows}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Section 4: Gap Analysis -->
    <div class="section">
        <div class="section-title">Section 4: Critical Locations Gap Analysis ({no_ads_count} no ads, {low_budget_count} low budget, {good_count} active)</div>
        <div class="legend">
            <span>&#x1F534; No Google Ads campaign</span>
            <span>&#x1F7E1; Budget &lt; $30/day</span>
            <span>&#x1F7E2; Active with adequate budget</span>
        </div>
        <div class="table-scroll">
            <table>
                <thead>
                    <tr>
                        <th>Location</th>
                        <th>State</th>
                        <th>Client(s)</th>
                        <th>HC Needed</th>
                        <th>FHS RSVPs</th>
                        <th>Google Ads Status</th>
                        <th>Daily Budget</th>
                        <th>Recommended Action</th>
                    </tr>
                </thead>
                <tbody>
                    {gap_table_rows}
                </tbody>
            </table>
        </div>
    </div>

    <div class="footer">
        Indeed Flex US — Recruitment Marketing | Google Ads Account 723-610-0723 | MCC 653-165-0309 | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </div>
</body>
</html>"""

    return html


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Google Ads Dashboard Generator")
    print("=" * 60)

    # Load Google Ads data
    campaigns, daily_data, budgets, days_elapsed = load_google_ads_data()
    print(f"  Loaded {len(campaigns)} campaigns, {len(daily_data)} daily rows")

    # Load cross-reference data
    revenue_requests = load_revenue_requests()
    print(f"  Loaded {len(revenue_requests)} live revenue requests")

    requisitions = load_requisitions()
    print(f"  Loaded {len(requisitions)} open/draft requisitions")

    # Generate HTML
    print("Generating HTML dashboard...")
    html = generate_html(campaigns, daily_data, budgets, days_elapsed,
                         revenue_requests, requisitions)

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Saved to: {OUTPUT_HTML}")

    # Open in browser
    subprocess.run(["open", OUTPUT_HTML])
    print("\nDashboard saved and opened")


if __name__ == "__main__":
    main()
