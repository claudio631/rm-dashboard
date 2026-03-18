#!/usr/bin/env python3
"""
EOD Update Key Clients — Daily Slack Report Generator

Reads 3 data files from ~/Downloads and generates a Slack-formatted report.
Also copies the output to clipboard (macOS) for easy pasting.

Usage:
    python3 src/services/eod-report-generator.py
    python3 src/services/eod-report-generator.py --downloads-dir /path/to/downloads

Data files (auto-detected from ~/Downloads, most recent used):
    1. OB Funnel Custom Viewer.xlsx  — Tableau OB funnel split report
    2. JobsCampaigns_*.csv           — Indeed Analytics campaign spend
    3. requisitions-*.csv            — FHS Requisition report
"""

import csv
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

try:
    import openpyxl
except ImportError:
    print("Error: openpyxl is required. Install with: pip3 install openpyxl")
    sys.exit(1)


# --- Configuration ---

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SPEND_HISTORY_FILE = PROJECT_ROOT / "src" / "data" / "last-report-spend.json"
DEFAULT_DOWNLOADS = Path.home() / "Downloads"

# Key clients and their named locations (order matters for output)
KEY_CLIENTS = {
    "CORT": {
        "named": ["Las Vegas", "Chicago", "Atlanta", "Orlando", "Phoenix", "Austin", "Nashville"],
        "group_others": True,
    },
    "Stord, Inc": {
        "named": ["Las Vegas", "Reno", "Atlanta", "Erlanger"],
        "group_others": False,
    },
    "OnTrac Final Mile": {
        "named": ["Logan Township", "Columbus", "Middleburg Heights", "Reno"],
        "group_others": True,
    },
    "CTDI": {
        "named": ["Dallas", "Columbus", "Nashville"],
        "group_others": False,
    },
}

CLIENT_ORDER = ["CORT", "Stord, Inc", "OnTrac Final Mile", "CTDI"]


# --- File Discovery ---

def find_latest_file(downloads_dir: Path, pattern: str) -> Optional[Path]:
    matches = sorted(
        downloads_dir.glob(pattern),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    return matches[0] if matches else None


def discover_files(downloads_dir: Path) -> dict:
    ob_funnel = find_latest_file(downloads_dir, "OB Funnel Custom Viewer*.xlsx")
    jobs_campaigns = find_latest_file(downloads_dir, "JobsCampaigns_*.csv")
    requisitions = find_latest_file(downloads_dir, "requisitions-*.csv")

    missing = []
    if not ob_funnel:
        missing.append("OB Funnel Custom Viewer.xlsx")
    if not jobs_campaigns:
        missing.append("JobsCampaigns_*.csv")
    if not requisitions:
        missing.append("requisitions-*.csv")

    if missing:
        print(f"Error: Could not find the following files in {downloads_dir}:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)

    return {
        "ob_funnel": ob_funnel,
        "jobs_campaigns": jobs_campaigns,
        "requisitions": requisitions,
    }


# --- Section 1: Key Client Unique Accounts ---

def get_comparison_date(today: datetime) -> datetime:
    """D-1 for Tue-Fri, D-3 (Friday) for Monday."""
    if today.weekday() == 0:  # Monday
        return today - timedelta(days=3)  # Friday
    return today - timedelta(days=1)


def process_ob_funnel(filepath: Path, today: datetime) -> dict:
    """Parse OB Funnel xlsx and return client/location data."""
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]

    # Parse header dates
    header = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    date_cols = {}
    for i in range(3, len(header)):
        if header[i] and isinstance(header[i], str) and "'" in header[i]:
            try:
                d = datetime.strptime(header[i], "%b %d '%y")
                date_cols[i] = d
            except ValueError:
                pass

    window_start = today - timedelta(days=30)
    comparison_date = get_comparison_date(today)

    # Column indices
    window_cols = [i for i, d in date_cols.items() if window_start <= d <= today]
    comp_col = next((i for i, d in date_cols.items() if d == comparison_date), None)

    # Parse rows
    current_client = None
    current_location = None
    results = {}

    for row in ws.iter_rows(min_row=2, values_only=True):
        vals = list(row)
        if vals[0]:
            current_client = vals[0]
        if vals[1]:
            current_location = vals[1]
        if not current_client or not current_location:
            continue

        metric = vals[2]
        if metric not in ("Worker Accounts Created", "1st Role Verified (# Workers)"):
            continue

        key = (current_client, current_location)
        if key not in results:
            results[key] = {"created": 0, "verified": 0, "delta": 0}

        if metric == "Worker Accounts Created":
            total = sum(
                int(vals[c]) for c in window_cols
                if c < len(vals) and vals[c] and isinstance(vals[c], (int, float))
            )
            results[key]["created"] = total

        elif metric == "1st Role Verified (# Workers)":
            total = sum(
                int(vals[c]) for c in window_cols
                if c < len(vals) and vals[c] and isinstance(vals[c], (int, float))
            )
            results[key]["verified"] = total

            d1_val = 0
            if comp_col and comp_col < len(vals) and vals[comp_col]:
                d1_val = int(vals[comp_col])
            results[key]["delta"] = d1_val

    wb.close()
    return results


def format_section1(data: dict) -> str:
    """Format key client unique accounts section."""
    lines = []

    for client_name in CLIENT_ORDER:
        config = KEY_CLIENTS[client_name]
        named_locs = config["named"]
        group_others = config["group_others"]

        # Collect all locations for this client
        client_data = [
            {"location": loc, **vals}
            for (c, loc), vals in data.items()
            if c == client_name
        ]

        if not client_data:
            continue

        lines.append(f"*{client_name}:*")

        # Named locations sorted by Created desc
        named_entries = []
        other_created = 0
        other_verified = 0
        other_delta = 0

        for loc_name in named_locs:
            entry = next((d for d in client_data if d["location"] == loc_name), None)
            if entry:
                named_entries.append(entry)

        # Sort named by created desc
        named_entries.sort(key=lambda x: -x["created"])

        for entry in named_entries:
            lines.append(
                f"{entry['location']}: {entry['created']} Created → "
                f"{entry['verified']} Verified (+{entry['delta']})"
            )

        # Other locations
        for entry in client_data:
            if entry["location"] not in named_locs:
                if group_others:
                    other_created += entry["created"]
                    other_verified += entry["verified"]
                    other_delta += entry["delta"]
                else:
                    # Show individually (sorted by created desc)
                    pass

        if not group_others:
            # Show non-named locations individually
            extras = sorted(
                [e for e in client_data if e["location"] not in named_locs],
                key=lambda x: -x["created"],
            )
            for entry in extras:
                lines.append(
                    f"{entry['location']}: {entry['created']} Created → "
                    f"{entry['verified']} Verified (+{entry['delta']})"
                )

        if group_others and (other_created > 0 or other_verified > 0):
            lines.append(
                f"Other Locations: {other_created} Created → "
                f"{other_verified} Verified (+{other_delta})"
            )

        lines.append("")  # blank line between clients

    return "\n".join(lines)


# --- Section 2: Indeed Spend ---

def process_indeed_spend(filepath: Path) -> float:
    """Sum the Spend column from JobsCampaigns CSV."""
    total = 0.0
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                total += float(row.get("Spend", 0))
            except (ValueError, TypeError):
                pass
    return total


def load_last_spend() -> Optional[float]:
    """Load last report spend from JSON file."""
    if SPEND_HISTORY_FILE.exists():
        with open(SPEND_HISTORY_FILE, "r") as f:
            data = json.load(f)
            return data.get("last_spend")
    return None


def save_current_spend(spend: float):
    """Save current spend for next report's comparison."""
    SPEND_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SPEND_HISTORY_FILE, "w") as f:
        json.dump({"last_spend": spend, "updated_at": datetime.now().isoformat()}, f, indent=2)


def format_section2(current_spend: float, last_spend: Optional[float]) -> str:
    """Format Indeed spend comparison line."""
    month_name = datetime.now().strftime("%B")
    line = f"*Indeed Spend Comparison:* Indeed {month_name} so far: ${current_spend:,.2f}"
    if last_spend is not None:
        delta = current_spend - last_spend
        line += f" (+${delta:,.2f} since last report)"
    return line


# --- Section 3: Open Campaigns ---

def process_requisitions(filepath: Path) -> dict:
    """Extract open campaigns from requisitions CSV."""
    open_reqs = {}
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"].strip().lower() != "open":
                continue

            client = row["client"].strip()

            # Exclude Indeed Flex
            if "indeed flex" in client.lower():
                continue

            # Normalize location
            location = row["location"].strip()
            location = re.sub(r"\s*,\s*", ", ", location)
            location = re.sub(r"\s+", " ", location)

            if client not in open_reqs:
                open_reqs[client] = set()
            open_reqs[client].add(location)

    return open_reqs


def format_section3(data: dict) -> str:
    """Format open campaigns section."""
    lines = ["*Open Campaigns (Status: Open Only)*", ""]
    for client in sorted(data.keys()):
        locations = sorted(data[client])
        lines.append(f"{client}: {'; '.join(locations)}")
    return "\n".join(lines)


# --- Main ---

def generate_report(downloads_dir: Path) -> str:
    """Generate the full EOD report."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    print(f"Report date: {today.strftime('%A, %B %d, %Y')}")
    print(f"Comparison day (D-1): {get_comparison_date(today).strftime('%A, %B %d')}")
    print()

    # Discover files
    files = discover_files(downloads_dir)
    print(f"OB Funnel:       {files['ob_funnel'].name}")
    print(f"JobsCampaigns:   {files['jobs_campaigns'].name}")
    print(f"Requisitions:    {files['requisitions'].name}")
    print()

    # Section 1: Key Client Unique Accounts
    ob_data = process_ob_funnel(files["ob_funnel"], today)
    section1 = format_section1(ob_data)

    # Section 2: Indeed Spend
    current_spend = process_indeed_spend(files["jobs_campaigns"])
    last_spend = load_last_spend()
    section2 = format_section2(current_spend, last_spend)

    # Section 3: Open Campaigns
    req_data = process_requisitions(files["requisitions"])
    section3 = format_section3(req_data)

    # Assemble report
    report = (
        "@here EOD RM Update Key client unique accounts: (last update yesterday)\n"
        "\n"
        f"{section1}"
        "\n"
        f"{section2}\n"
        "\n"
        f"{section3}\n"
    )

    # Save spend for next run
    save_current_spend(current_spend)

    return report


def copy_to_clipboard(text: str):
    """Copy text to macOS clipboard."""
    try:
        process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        process.communicate(text.encode("utf-8"))
        return True
    except FileNotFoundError:
        return False


def main():
    downloads_dir = DEFAULT_DOWNLOADS

    # Allow custom downloads dir via --downloads-dir flag
    if "--downloads-dir" in sys.argv:
        idx = sys.argv.index("--downloads-dir")
        if idx + 1 < len(sys.argv):
            downloads_dir = Path(sys.argv[idx + 1])

    report = generate_report(downloads_dir)

    print("=" * 60)
    print("SLACK REPORT (copy below)")
    print("=" * 60)
    print()
    print(report)

    # Copy to clipboard on macOS
    if copy_to_clipboard(report):
        print("=" * 60)
        print("Copied to clipboard! Paste directly into Slack.")
    else:
        print("=" * 60)
        print("Could not copy to clipboard. Copy the text above manually.")


if __name__ == "__main__":
    main()
