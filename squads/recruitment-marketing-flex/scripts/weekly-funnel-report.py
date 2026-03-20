#!/usr/bin/env python3
"""
Weekly OB Funnel Report Generator
Reads Tableau OB Funnel Custom Viewer .xlsx and optionally a requisitions CSV
to generate an HTML report with conditional formatting and open-req demand signals.

Usage:
    python3 weekly-funnel-report.py <xlsx_path> [--reqs <csv_path>] [--owner claudio|craig|all] [--output <path>]

Example:
    python3 weekly-funnel-report.py ~/Downloads/"OB Funnel Custom Viewer (2).xlsx" \
        --reqs ~/Downloads/requisitions-2026-03-19-123275.csv --owner claudio
"""

import openpyxl
import csv
import sys
import os
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

# === CONFIGURATION ===

OWNER_MARKETS = {
    "claudio": [
        "Austin", "Houston", "Charlotte", "Fort Mill", "Orlando",
        "Las Vegas", "Reno", "Washington, D.C.", "Monroe", "Phoenix",
        "Logan Township"
    ],
    "craig": [
        "Columbus", "Cincinnati", "Hebron", "Chicago", "Atlanta",
        "Dallas", "Logan Township", "North Haven", "South Brunswick",
        "Hamilton", "Kearny", "Nashville", "Middleburg Heights",
        "Erlanger", "Newark", "Paulsboro", "McCarran"
    ]
}

STAGES = [
    'Worker Accounts Created',
    '1st Role Verified (# Workers)',
    '1st OB Task Completed (# Workers)',
    'Platform Verified (# Workers)',
    '"Ready to Book" Estimate (# Workers)',
    '1st Shift Booked (# Workers)',
    '1st Shift Completed (# Workers)'
]

SHORT_NAMES = ['Accts', 'Verif', 'OB Task', 'PlatV', 'Ready', 'Booked', 'Comp']

# 2025 benchmarks
BENCHMARKS = {
    'av': 56.0,   # Acct -> Verified
    'vo': 93.0,   # Verified -> OB Task
    'op': 69.1,   # OB Task -> PlatformV
    'pb': 50.4,   # PlatformV -> Booked
    'bc': 84.6,   # Booked -> Completed
    'cr': 15.4    # Overall
}

# Thresholds: (green_min, yellow_min) — below yellow_min = red
THRESHOLDS = {
    'av': (55, 40),
    'vo': (85, 75),
    'op': (65, 50),
    'pb': (40, 15),
    'bc': (80, 60),
    'cr': (15, 8)
}


def safe_div(a, b):
    return (a / b * 100) if b and b > 0 else None


def color_class(val, stage_key):
    if val is None:
        return "na"
    green_min, yellow_min = THRESHOLDS[stage_key]
    if val >= green_min:
        return "green"
    if val >= yellow_min:
        return "yellow"
    return "red"


def fmt_pct(val, stage_key):
    if val is None:
        return '<span class="na">—</span>'
    cls = color_class(val, stage_key)
    icon = {"green": "🟢", "yellow": "🟡", "red": "🔴", "na": ""}[cls]
    return f'<span class="{cls}">{icon} {val:.1f}%</span>'


def parse_xlsx(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb[wb.sheetnames[0]]

    header = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    # Find date columns and Grand Total
    date_cols = []
    grand_total_idx = None
    for i, h in enumerate(header):
        if h and "Grand Total" in str(h):
            grand_total_idx = i
        elif h and ("'" in str(h) or "20" in str(h)):
            date_cols.append((i, str(h)))

    dates = [str(h) for _, h in date_cols if h]
    week_start = dates[0] if dates else "?"
    week_end = dates[-1] if dates else "?"

    data = {}
    current_client = None
    current_location = None

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
        row = list(row)
        if row[0]:
            current_client = str(row[0]).strip()
        if row[1]:
            current_location = str(row[1]).strip()
        stage = row[2]
        if not stage:
            continue
        stage = str(stage).strip()
        grand_total = row[grand_total_idx] if grand_total_idx and row[grand_total_idx] else 0

        key = (current_client, current_location)
        if key not in data:
            data[key] = {}
        data[key][stage] = int(grand_total) if grand_total else 0

    return data, week_start, week_end


# === REQUISITIONS PARSING ===

def parse_requisitions(csv_path):
    """Parse requisitions CSV and return a lookup dict keyed by (city, client_normalized)."""
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Only active demand
    active_statuses = ('open', 'auto-paused', 'draft')
    active = [r for r in rows if r.get('status', '').strip() in active_statuses]

    # Build lookup: city_key -> client_key -> {reqs, rsvps, target, titles, statuses}
    lookup = defaultdict(lambda: defaultdict(lambda: {
        'reqs': 0, 'rsvps': 0, 'target': 0, 'titles': set(), 'statuses': set()
    }))

    for r in active:
        loc = r.get('location', '').strip()
        client = r.get('client', '').strip()
        city = loc.split(',')[0].strip()
        city_key = _normalize_city(city)
        client_key = _normalize_client(client)

        entry = lookup[city_key][client_key]
        entry['reqs'] += 1
        try:
            entry['rsvps'] += int(r.get('rsvps', 0) or 0)
        except ValueError:
            pass
        try:
            entry['target'] += int(r.get('target_rsvps', 0) or 0)
        except ValueError:
            pass
        entry['titles'].add(r.get('job_title', '').strip())
        entry['statuses'].add(r.get('status', '').strip())

    return lookup


def _normalize_city(city):
    """Normalize city names for fuzzy matching between funnel and requisition data."""
    city = city.lower().strip()
    # Handle common variations
    mappings = {
        'washington, d.c.': 'washington',
        'washington, d.c': 'washington',
        'washington, dc': 'washington',
        'middleburg hts': 'middleburg heights',
        'fort mill': 'fort mill',
    }
    for k, v in mappings.items():
        if k in city:
            return v
    return city


def _normalize_client(client):
    """Normalize client names for fuzzy matching."""
    client = client.lower().strip()
    # Strip common suffixes
    for suffix in [', inc.', ', inc', ' inc.', ' inc', ', llc', ' llc',
                   ' corporation', ' corp', ' co.', ' co']:
        if client.endswith(suffix):
            client = client[:-len(suffix)]
    return client


def get_req_info(req_lookup, location, client):
    """Look up requisition info for a location/client combo."""
    city_key = _normalize_city(location.split(',')[0].strip() if ',' in location else location)
    client_key = _normalize_client(client)

    # Try exact match first
    if city_key in req_lookup:
        city_data = req_lookup[city_key]
        # Exact match
        if client_key in city_data:
            return city_data[client_key]
        # Fuzzy: check if client_key is contained in any req client or vice versa
        for req_client_key, info in city_data.items():
            if client_key in req_client_key or req_client_key in client_key:
                return info

    return None


def get_market_req_totals(req_lookup, location):
    """Get total requisitions for an entire market (all clients)."""
    city_key = _normalize_city(location.split(',')[0].strip() if ',' in location else location)
    if city_key not in req_lookup:
        return None

    total = {'reqs': 0, 'rsvps': 0, 'target': 0, 'titles': set(), 'statuses': set()}
    for client_key, info in req_lookup[city_key].items():
        total['reqs'] += info['reqs']
        total['rsvps'] += info['rsvps']
        total['target'] += info['target']
        total['titles'].update(info['titles'])
        total['statuses'].update(info['statuses'])

    return total if total['reqs'] > 0 else None


# === REPORT BUILDING ===

def build_report(data, markets, owner_name, week_start, week_end):
    market_data = {}
    grand_total = {s: 0 for s in STAGES}

    for loc in sorted(set(m for m in markets)):
        loc_total = {s: 0 for s in STAGES}
        loc_clients = {}

        for (client, location), stages in data.items():
            if location != loc:
                continue
            loc_clients[client] = {}
            for s in STAGES:
                val = stages.get(s, 0)
                loc_clients[client][s] = val
                loc_total[s] += val
                grand_total[s] += val

        if loc_clients:
            market_data[loc] = {'total': loc_total, 'clients': loc_clients}

    sorted_markets = sorted(market_data.items(),
                            key=lambda x: x[1]['total'][STAGES[0]], reverse=True)

    return sorted_markets, grand_total


def _fmt_req_cell(req_info, platv=0, is_total=False):
    """Format the requisition column cell with conditional coloring."""
    if req_info is None:
        if platv > 0:
            return '<span class="red">❌ No reqs</span>'
        return '<span class="na">—</span>'

    reqs = req_info['reqs']
    rsvps = req_info['rsvps']
    target = req_info['target']
    fill_pct = safe_div(rsvps, target) if target else None
    titles = sorted(req_info.get('titles', set()) - {''})
    title_str = ', '.join(t[:20] for t in titles[:3])

    if reqs == 0:
        if platv > 0:
            return '<span class="red">❌ No reqs</span>'
        return '<span class="na">—</span>'

    # Color based on fill rate
    if fill_pct is not None and fill_pct >= 80:
        cls = "yellow"
        icon = "⚠️"
        note = "near full"
    elif fill_pct is not None and fill_pct < 30:
        cls = "green"
        icon = "✅"
        note = "needs workers"
    else:
        cls = "green"
        icon = "✅"
        note = ""

    fill_str = f" ({fill_pct:.0f}%)" if fill_pct is not None else ""
    detail = f'<span class="{cls}">{icon} {reqs} reqs</span>'
    sub = f'<br><span style="font-size:10px;color:#666">{rsvps}/{target} RSVPs{fill_str}</span>'
    if title_str and not is_total:
        sub += f'<br><span style="font-size:9px;color:#999">{title_str}</span>'

    return detail + sub


def generate_html(sorted_markets, grand_total, owner_name, week_start, week_end, req_lookup=None):
    gt = [grand_total[s] for s in STAGES]
    total_accts = gt[0]
    total_comp = gt[6]
    total_platv = gt[3]
    total_booked = gt[5]
    verified_not_booking = total_platv - total_booked

    has_reqs = req_lookup is not None
    colspan = "15" if has_reqs else "14"

    rows_html = ""

    # Grand total row
    a, v, ob, pv, rd, bk, co = gt
    req_cell = ""
    if has_reqs:
        # Sum all reqs across all markets in this report
        total_req_info = {'reqs': 0, 'rsvps': 0, 'target': 0, 'titles': set(), 'statuses': set()}
        for loc, _ in sorted_markets:
            mri = get_market_req_totals(req_lookup, loc)
            if mri:
                total_req_info['reqs'] += mri['reqs']
                total_req_info['rsvps'] += mri['rsvps']
                total_req_info['target'] += mri['target']
        req_cell = _fmt_req_cell(total_req_info, pv, is_total=True) if total_req_info['reqs'] > 0 else _fmt_req_cell(None, pv)

    rows_html += _make_row(
        f"<strong>{owner_name.upper()} TOTAL</strong>",
        a, v, ob, pv, rd, bk, co, req_cell=req_cell, is_total=True, has_reqs=has_reqs
    )
    rows_html += f'<tr class="spacer"><td colspan="{colspan}"></td></tr>'

    # Per market
    for loc, md in sorted_markets:
        t = md['total']
        a, v, ob, pv, rd, bk, co = [t[s] for s in STAGES]

        mkt_req_cell = ""
        if has_reqs:
            mri = get_market_req_totals(req_lookup, loc)
            mkt_req_cell = _fmt_req_cell(mri, pv, is_total=True)

        rows_html += _make_row(
            f"<strong>{loc.upper()}</strong>", a, v, ob, pv, rd, bk, co,
            req_cell=mkt_req_cell, is_market=True, has_reqs=has_reqs
        )

        sorted_clients = sorted(md['clients'].items(),
                                key=lambda x: x[1].get(STAGES[0], 0), reverse=True)
        for client, cs in sorted_clients:
            ca = cs.get(STAGES[0], 0)
            if ca == 0:
                continue
            cv, cob, cpv, crd, cbk, cco = [cs.get(s, 0) for s in STAGES[1:]]
            short_name = client if len(client) <= 35 else client[:33] + '..'

            client_req_cell = ""
            if has_reqs:
                cri = get_req_info(req_lookup, loc, client)
                client_req_cell = _fmt_req_cell(cri, cpv)

            rows_html += _make_row(
                f"&nbsp;&nbsp;- {short_name}", ca, cv, cob, cpv, crd, cbk, cco,
                req_cell=client_req_cell, has_reqs=has_reqs
            )

        rows_html += f'<tr class="spacer"><td colspan="{colspan}"></td></tr>'

    # Build HTML
    today = date.today().strftime("%Y-%m-%d")
    cr_total = safe_div(total_comp, total_accts)
    cr_display = f"{cr_total:.1f}%" if cr_total else "0.0%"

    markets_with_comp = sum(1 for _, md in sorted_markets if md['total'][STAGES[6]] > 0)
    total_markets = len(sorted_markets)

    req_header_col = '<th>Open Reqs</th>' if has_reqs else ''
    req_data_source = " + Requisitions CSV" if has_reqs else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Weekly OB Funnel Report — {owner_name}'s Markets ({week_start} to {week_end})</title>
<style>
    @media print {{
        body {{ margin: 0; font-size: 9pt; }}
        .page-break {{ page-break-before: always; }}
        @page {{ size: landscape; margin: 1cm; }}
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        max-width: 1500px;
        margin: 0 auto;
        padding: 20px;
        color: #1a1a1a;
        font-size: 13px;
        line-height: 1.4;
    }}
    h1 {{
        font-size: 22px;
        border-bottom: 3px solid #0066cc;
        padding-bottom: 8px;
        margin-bottom: 5px;
    }}
    h2 {{
        font-size: 16px;
        color: #0066cc;
        margin-top: 25px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 4px;
    }}
    h3 {{ font-size: 14px; margin-top: 15px; }}
    .meta {{ color: #666; font-size: 12px; margin-bottom: 20px; }}
    .summary-box {{
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 15px 20px;
        margin: 15px 0;
    }}
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin: 15px 0;
    }}
    .kpi-card {{
        background: #fff;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
    }}
    .kpi-card .value {{ font-size: 24px; font-weight: bold; }}
    .kpi-card .label {{ font-size: 11px; color: #666; margin-top: 4px; }}
    .kpi-card.red {{ border-left: 4px solid #dc3545; }}
    .kpi-card.yellow {{ border-left: 4px solid #ffc107; }}
    .kpi-card.green {{ border-left: 4px solid #28a745; }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 12px;
    }}
    th {{
        background: #2c3e50;
        color: white;
        padding: 8px 6px;
        text-align: center;
        font-size: 11px;
        font-weight: 600;
        white-space: nowrap;
    }}
    th:first-child {{ text-align: left; min-width: 200px; }}
    td {{
        padding: 5px 6px;
        border-bottom: 1px solid #eee;
        text-align: center;
        vertical-align: top;
    }}
    td:first-child {{ text-align: left; }}
    td:last-child {{ text-align: left; min-width: 140px; }}
    tr.market-row {{ background: #f0f4f8; font-weight: 600; }}
    tr.market-row td {{ border-bottom: 1px solid #ccc; }}
    tr.total-row {{ background: #2c3e50; color: white; font-weight: 700; }}
    tr.total-row td {{ border-bottom: 2px solid #1a252f; }}
    tr.total-row .green, tr.total-row .yellow, tr.total-row .red {{ color: white; }}
    tr.spacer td {{ border: none; height: 8px; background: white; }}
    tr:hover:not(.spacer):not(.total-row) {{ background: #f5f7fa; }}
    .green {{ color: #28a745; font-weight: 600; }}
    .yellow {{ color: #b8860b; font-weight: 600; }}
    .red {{ color: #dc3545; font-weight: 600; }}
    .na {{ color: #999; }}
    .num {{ color: #333; }}
    .legend-table {{ max-width: 700px; }}
    .legend-table td {{ padding: 4px 10px; }}
    .req-legend {{ max-width: 600px; margin-top: 10px; }}
    .req-legend td {{ padding: 3px 8px; font-size: 12px; }}
    .footer {{
        margin-top: 30px;
        padding-top: 10px;
        border-top: 1px solid #ddd;
        color: #999;
        font-size: 11px;
    }}
</style>
</head>
<body>

<h1>Weekly OB Funnel Report — {owner_name.title()}'s Markets</h1>
<div class="meta">
    <strong>Period:</strong> {week_start} — {week_end} &nbsp;|&nbsp;
    <strong>Generated:</strong> {today} &nbsp;|&nbsp;
    <strong>Source:</strong> OB Funnel Custom Viewer (Tableau){req_data_source} &nbsp;|&nbsp;
    <strong>Agent:</strong> Fiona (@funnel-specialist)
</div>

<div class="kpi-grid">
    <div class="kpi-card {'red' if (cr_total or 0) < 8 else 'yellow' if (cr_total or 0) < 15 else 'green'}">
        <div class="value">{cr_display}</div>
        <div class="label">Overall CR% (benchmark: 15.4%)</div>
    </div>
    <div class="kpi-card red">
        <div class="value">{total_accts}</div>
        <div class="label">Accounts Created</div>
    </div>
    <div class="kpi-card red">
        <div class="value">{total_comp}</div>
        <div class="label">Shifts Completed</div>
    </div>
    <div class="kpi-card red">
        <div class="value">{verified_not_booking}</div>
        <div class="label">Verified but NOT Booking</div>
    </div>
</div>

<div class="summary-box">
    <strong>Portfolio snapshot:</strong> {total_accts} accounts &rarr; {gt[1]} verified &rarr; {gt[3]} platform verified &rarr; {gt[5]} booked &rarr; {total_comp} completed
    <br><strong>Markets with completions:</strong> {markets_with_comp} of {total_markets}
    &nbsp;|&nbsp; <strong>Verified workers not booking:</strong> {verified_not_booking} ({safe_div(verified_not_booking, total_platv):.0f}% of pipeline wasted)
</div>

<h2>Conditional Formatting</h2>
<table class="legend-table">
<tr><th>Stage</th><th>🟢 Good</th><th>🟡 Watch</th><th>🔴 Critical</th><th>2025 Benchmark</th></tr>
<tr><td>Acct &rarr; Verified</td><td class="green">&ge; 55%</td><td class="yellow">40-54%</td><td class="red">&lt; 40%</td><td>56.0%</td></tr>
<tr><td>Verified &rarr; OB Task</td><td class="green">&ge; 85%</td><td class="yellow">75-84%</td><td class="red">&lt; 75%</td><td>93.0%</td></tr>
<tr><td>OB Task &rarr; PlatformV</td><td class="green">&ge; 65%</td><td class="yellow">50-64%</td><td class="red">&lt; 50%</td><td>69.1%</td></tr>
<tr><td>PlatformV &rarr; Booked</td><td class="green">&ge; 40%</td><td class="yellow">15-39%</td><td class="red">&lt; 15%</td><td>50.4%</td></tr>
<tr><td>Booked &rarr; Completed</td><td class="green">&ge; 80%</td><td class="yellow">60-79%</td><td class="red">&lt; 60%</td><td>84.6%</td></tr>
<tr><td>Overall CR%</td><td class="green">&ge; 15%</td><td class="yellow">8-14.9%</td><td class="red">&lt; 8%</td><td>15.4%</td></tr>
</table>

{"<table class='req-legend'><tr><th colspan='2'>Open Reqs Column</th></tr><tr><td>✅ N reqs</td><td>Active requisitions — demand exists, workers can book</td></tr><tr><td>⚠️ N reqs</td><td>Reqs near full (RSVPs &ge; 80% of target)</td></tr><tr><td>❌ No reqs</td><td>No open requisitions — verified workers CANNOT book (red flag if PlatV &gt; 0)</td></tr></table>" if has_reqs else ""}

<h2>Full Funnel — By Location & Client</h2>
<table>
<tr>
    <th>Market / Client</th>
    <th>Accts</th>
    <th>Verif</th><th>A&rarr;V</th>
    <th>OB Task</th><th>V&rarr;OB</th>
    <th>PlatV</th><th>OB&rarr;PV</th>
    <th>Ready</th>
    <th>Booked</th><th>PV&rarr;Bk</th>
    <th>Comp</th><th>Bk&rarr;Co</th>
    <th>CR%</th>
    {req_header_col}
</tr>
{rows_html}
</table>

<div class="footer">
    Report generated by Fiona (@funnel-specialist) &middot; Template: weekly-funnel-report-tmpl.md &middot; Squad: recruitment-marketing-flex<br>
    Data source: OB Funnel Custom Viewer (Tableau){req_data_source} &middot; Benchmarks: 2025 full-year baseline (52,987 accounts &rarr; 8,146 completed = 15.4%)
</div>

</body>
</html>"""

    return html


def _make_row(label, a, v, ob, pv, rd, bk, co, req_cell="", is_market=False, is_total=False, has_reqs=False):
    av = safe_div(v, a)
    vo = safe_div(ob, v)
    op = safe_div(pv, ob)
    pb = safe_div(bk, pv)
    bc = safe_div(co, bk)
    cr = safe_div(co, a)

    row_class = ""
    if is_total:
        row_class = ' class="total-row"'
    elif is_market:
        row_class = ' class="market-row"'

    req_td = f"<td>{req_cell}</td>" if has_reqs else ""

    return f"""<tr{row_class}>
    <td>{label}</td>
    <td class="num">{a}</td>
    <td class="num">{v}</td><td>{fmt_pct(av, 'av')}</td>
    <td class="num">{ob}</td><td>{fmt_pct(vo, 'vo')}</td>
    <td class="num">{pv}</td><td>{fmt_pct(op, 'op')}</td>
    <td class="num">{rd}</td>
    <td class="num">{bk}</td><td>{fmt_pct(pb, 'pb')}</td>
    <td class="num">{co}</td><td>{fmt_pct(bc, 'bc')}</td>
    <td>{fmt_pct(cr, 'cr')}</td>
    {req_td}
</tr>\n"""


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Weekly OB Funnel Report Generator')
    parser.add_argument('xlsx_path', help='Path to OB Funnel Custom Viewer .xlsx')
    parser.add_argument('--reqs', default=None,
                        help='Path to requisitions CSV (adds Open Reqs column)')
    parser.add_argument('--owner', default='claudio', choices=['claudio', 'craig', 'all'],
                        help='Market owner to filter (default: claudio)')
    parser.add_argument('--output', default=None,
                        help='Output HTML path (default: docs/reports/weekly-funnel-YYYY-MM-DD.html)')
    args = parser.parse_args()

    xlsx_path = os.path.expanduser(args.xlsx_path)
    if not os.path.exists(xlsx_path):
        print(f"Error: File not found: {xlsx_path}")
        sys.exit(1)

    print(f"Reading funnel: {xlsx_path}")
    data, week_start, week_end = parse_xlsx(xlsx_path)

    req_lookup = None
    if args.reqs:
        reqs_path = os.path.expanduser(args.reqs)
        if not os.path.exists(reqs_path):
            print(f"Warning: Requisitions file not found: {reqs_path}, skipping")
        else:
            print(f"Reading requisitions: {reqs_path}")
            req_lookup = parse_requisitions(reqs_path)
            total_active = sum(sum(info['reqs'] for info in city.values()) for city in req_lookup.values())
            print(f"Active requisitions loaded: {total_active}")

    if args.owner == 'all':
        markets = list(set(loc for (_, loc) in data.keys()))
        owner_name = "All Markets"
    else:
        markets = OWNER_MARKETS[args.owner]
        owner_name = args.owner.title()

    print(f"Owner: {owner_name} ({len(markets)} markets)")
    sorted_markets, grand_total = build_report(data, markets, owner_name, week_start, week_end)

    html = generate_html(sorted_markets, grand_total, owner_name, week_start, week_end, req_lookup)

    if args.output:
        output_path = args.output
    else:
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        reports_dir = project_root / "docs" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        today = date.today().strftime("%Y-%m-%d")
        output_path = str(reports_dir / f"weekly-funnel-{args.owner}-{today}.html")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Report saved: {output_path}")
    print(f"Open in browser and use Cmd+P / Ctrl+P to print as PDF")

    return output_path


if __name__ == '__main__':
    main()
