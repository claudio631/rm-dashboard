#!/usr/bin/env python3
"""
Report 5: Revenue Requests Cross-Reference Dashboard — 2026-04-02
Generates an HTML dashboard cross-referencing Revenue Requests with FHS, Indeed, and OB Funnel data.

CRITICAL: Every "Live" or "Declined" row in Revenue Requests = one row in output. NO merging/dedup.

Data sources:
  - Revenue Requests: US_Recruitment_Requests__us_ (11).csv
  - FHS Requisitions: requisitions-2026-04-02-495947.csv
  - JobsCampaigns: JobsCampaigns_20260101_20260326.csv
  - OB Funnel: OB Funnel Custom Viewer (24).xlsx
"""

import csv
import re
import os
from collections import defaultdict
from datetime import datetime, date

import openpyxl

# =============================================================================
# FILE PATHS
# =============================================================================
REVENUE_CSV = os.path.expanduser("~/Downloads/US_Recruitment_Requests__us_ (11).csv")
FHS_CSV = os.path.expanduser("~/Downloads/requisitions-2026-04-02-495947.csv")
INDEED_CSV = os.path.expanduser("~/Downloads/JobsCampaigns_20260101_20260326.csv")
OB_FUNNEL_XLSX = os.path.expanduser("~/Downloads/OB Funnel Custom Viewer (24).xlsx")
OUTPUT_HTML = os.path.expanduser("~/RM-Team-Ai/docs/reports/revenue-requests-crossref-2026-04-02.html")
REPORT_DATE = "2026-04-02"
TODAY = date(2026, 4, 2)

# =============================================================================
# CLIENT NAME NORMALIZATION MAPS
# =============================================================================
CLIENT_NAME_MAP = {
    "compass": ["culinaire", "culinaire international"],
    "dc flex": ["cort", "indeed flex", "indeed flex applications"],
    "food glorious": ["culinaire"],
    "bon appetit": ["bon appetit management company, inc", "bon appetit"],
    "legends": ["legends hospitality"],
    "levy": ["levy restaurants"],
    "btx": ["btx global logistics"],
    "lettuce": ["lettuce entertain you enterprises, inc"],
    "soho house": ["soho house austin"],
    "austin club": ["austin catering"],
    "vestals": ["vestals catering"],
    "rhino": ["rhino staging"],
    "power stop": ["power stop"],
    "uplift": ["uplift desk"],
    "ryerson": ["ryerson"],
    "solaren": ["solaren risk management"],
    "hei hotels": ["merritt hospitality llc"],
    "hyatt place": ["merritt hospitality llc", "hyatt", "hei"],
    "merritt": ["merritt hospitality llc"],
    "foxconn": ["foxconn"],
    "ctdi": ["ctdi"],
    "ingram": ["ingram content group"],
    "stord": ["stord, inc"],
    "ontrac": ["ontrac final mile"],
    "tennant": ["tennant solutions"],
    "continental battery": ["continental battery systems, inc."],
    "bath concepts": ["bath concepts"],
    "cort": ["cort"],
    "assurant": ["assurant, inc (hyla)", "assurant"],
    "culinaire": ["culinaire", "culinaire international"],
    "material handler": ["ctdi"],
    "freshella": ["freshella catering"],
    "eurest": ["eurest"],
    "flik": ["flik"],
    "johnstone": ["johnstone supply"],
    "need forklift": ["johnstone supply"],
}

# Metro/Location aliases
LOCATION_ALIASES = {
    "dfw": "dallas",
    "vegas": "las vegas",
    "bedford park": "chicago",
    "hodgkins": "chicago",
    "fort worth": "dallas",
    "lancaster": "dallas",
    "flower mound": "dallas",
    "haslet": "dallas",
    "lavergne": "nashville",
    "la vergne": "nashville",
    "libertyville": "chicago",
    "grove city": "columbus",
    "mccarran": "las vegas",
    "middleburg heights": "columbus",
    "middle heights": "columbus",
    "south brunswick": "newark",
    "lebanon": "nashville",
    "lockbourne": "columbus",
    "logan township": "new jersey",
    "paulsboro": "new jersey",
    "hebron": "cincinnati",
    "west chester": "cincinnati",
    "erlanger": "cincinnati",
    "washington": "washington, d.c.",
    "washington dc": "washington, d.c.",
    "washington, dc": "washington, d.c.",
    "washington d.c.": "washington, d.c.",
    "washington, d.c.": "washington, d.c.",
    "washington, d.c": "washington, d.c.",
    "bedford": "chicago",
    "arlington": "dallas",
    "kissimmee": "orlando",
    "desoto": "dallas",
    "plano": "dallas",
    "garland": "dallas",
    "mesquite": "dallas",
    "fairfield": "cincinnati",
    "cartersville": "atlanta",
    "fort mill": "charlotte",
    "nw atlanta": "atlanta",
    "wimberley": "austin",
    "pasadena": "houston",
    "joliet": "chicago",
    "sparks": "reno",
    "hapeville": "atlanta",
    "mt. juliet": "nashville",
    "mount juliet": "nashville",
    "carrolton": "dallas",
    "irving": "dallas",
    "bensenville": "chicago",
    "stoughton": "boston",
    "lake jackson": "houston",
}


def normalize_location(loc_str):
    """Normalize a location string to a canonical metro name."""
    if not loc_str:
        return ""
    loc = loc_str.lower().strip()

    # Check aliases FIRST on the raw string
    for alias, metro in LOCATION_ALIASES.items():
        if alias in loc:
            return metro

    # Check common metros on raw string
    for metro in ["chicago", "dallas", "austin", "nashville", "las vegas",
                  "orlando", "houston", "atlanta", "columbus", "cincinnati",
                  "charlotte", "phoenix", "reno", "newark", "new jersey",
                  "philadelphia", "cleveland", "san antonio", "inland empire",
                  "washington, d.c.", "boston"]:
        if metro in loc:
            return metro

    # Remove state abbreviations and zip codes
    loc = re.sub(r',\s*[A-Za-z]{2}\s*\d{0,5}\s*$', '', loc_str.lower().strip())
    loc = loc.strip().rstrip(',').strip()

    # Re-check aliases after cleaning
    for alias, metro in LOCATION_ALIASES.items():
        if alias in loc:
            return metro

    for metro in ["chicago", "dallas", "austin", "nashville", "las vegas",
                  "orlando", "houston", "atlanta", "columbus", "cincinnati",
                  "charlotte", "phoenix", "reno", "newark", "new jersey",
                  "philadelphia", "cleveland", "san antonio", "inland empire",
                  "washington, d.c.", "boston"]:
        if metro in loc:
            return metro

    return loc


def normalize_client_for_match(client_short):
    """Get list of possible FHS/Indeed/Funnel client names for a revenue request client."""
    c = client_short.lower().strip()
    for key, vals in CLIENT_NAME_MAP.items():
        if key == c or c.startswith(key):
            return vals
    return [c]


def extract_client_and_location(client_job_str, location_col):
    """Extract short client name and location from the Client-Job and Location columns."""
    s = client_job_str.strip()
    sl = s.lower()

    # Special cases
    if sl.startswith("need forklift"):
        return "Johnstone Supply", "Lancaster, TX"
    if sl == "material handler":
        return "CTDI", "Haslet, TX"
    if sl.startswith("barista") and "allen" in location_col.lower():
        return "Barista", "Allen, TX"
    if sl.startswith("san antonio & austin"):
        return "CORT", "San Antonio/Austin"
    if sl.startswith("assurant"):
        return "Assurant", "Nashville"
    if sl == "foxconn":
        return "Foxconn", "Dallas"
    if sl == "rhino staging":
        return "Rhino", "Charlotte"
    if sl.startswith("sxsw"):
        return "SXSW", "Austin"
    if "vestals catering" in sl:
        return "Vestals", "Austin"
    if "obama foundation" in sl:
        return "Bon Appetit", "Chicago"
    if "dos equis pavilion" in sl and "legends" in sl:
        if "at&t" not in sl:
            return "Legends", "Dallas"
    if "at&t stadium" in sl and "legends" in sl:
        return "Legends", "Dallas"
    if "at&t stadium" in sl and "dos equis" in sl and "legends" in sl:
        return "Legends", "Dallas"
    if "soldier field" in sl and "levy" in sl:
        return "Levy", "Chicago"
    if "new jersey" in sl and "loader" in sl:
        return "CORT", "New Jersey"

    # Parse "Client - Location - Role" pattern
    parts = re.split(r'\s*-\s*', s, maxsplit=3)

    client = parts[0].strip()
    # Remove leading parens like "(Culinaire)"
    if client.startswith("("):
        m = re.match(r'\(([^)]+)\)\s*(.*)', client)
        if m:
            client = m.group(2).strip() if m.group(2).strip() else m.group(1).strip()

    location = ""
    if len(parts) >= 2:
        location = parts[1].strip()

    loc = _extract_city(location, s, location_col)

    # Client name standardization
    cl = client.lower()
    if cl == "cort" or cl.startswith("cort"):
        client = "CORT"
    elif "culinaire" in cl or "food glorious" in cl:
        client = "Culinaire"
    elif "compass" in cl:
        client = "Compass"
    elif "bon appetit" in cl:
        client = "Bon Appetit"
    elif "dc flex" in cl:
        client = "DC Flex"
    elif "foxconn" in cl:
        client = "Foxconn"
    elif "power stop" in cl:
        client = "Power Stop"
    elif "legends" in cl:
        client = "Legends"
    elif "levy" in cl:
        client = "Levy"
    elif "ingram" in cl:
        client = "Ingram"
    elif "ctdi" in cl:
        client = "CTDI"
    elif "bath concepts" in cl:
        client = "Bath Concepts"
    elif "btx" in cl:
        client = "BTX"
    elif "solaren" in cl:
        client = "Solaren"
    elif "hei hotels" in cl or "merritt" in cl:
        client = "HEI Hotels"
    elif "hyatt" in cl:
        client = "Hyatt Place"
    elif "rhino" in cl:
        client = "Rhino"
    elif "uplift" in cl:
        client = "Uplift"
    elif "ryerson" in cl:
        client = "Ryerson"
    elif "lettuce" in cl:
        client = "Lettuce"
    elif "soho" in cl:
        client = "Soho House"
    elif "eurest" in cl:
        client = "Eurest"
    elif "freshella" in cl:
        client = "Freshella"
    elif "stord" in cl:
        client = "Stord"
    elif "flik" in cl or "ncr voyix" in cl:
        client = "FLIK"
    elif "johnstone" in cl:
        client = "Johnstone Supply"

    return client, loc


def _extract_city(loc_part, full_str, location_col=""):
    """Try to extract a city name from location columns."""
    check_str = (full_str + " " + location_col).lower()
    cities = {
        "chicago": "Chicago",
        "dallas": "Dallas",
        "dfw": "Dallas",
        "austin": "Austin",
        "nashville": "Nashville",
        "las vegas": "Las Vegas",
        "vegas": "Las Vegas",
        "orlando": "Orlando",
        "houston": "Houston",
        "atlanta": "Atlanta",
        "columbus": "Columbus",
        "cincinnati": "Cincinnati",
        "charlotte": "Charlotte",
        "phoenix": "Phoenix",
        "reno": "Reno",
        "san antonio": "San Antonio",
        "washington": "Washington, D.C.",
        "fort worth": "Dallas",
        "bedford park": "Chicago",
        "hodgkins": "Chicago",
        "la vergne": "Nashville",
        "lavergne": "Nashville",
        "grove city": "Columbus",
        "libertyville": "Chicago",
        "bedford": "Chicago",
        "mt. juliet": "Nashville",
        "mount juliet": "Nashville",
        "haslet": "Dallas",
        "lancaster": "Dallas",
        "carrolton": "Dallas",
        "new jersey": "New Jersey",
        "bensenville": "Chicago",
        "arlington": "Dallas",
        "irving": "Dallas",
        "hapeville": "Atlanta",
        "athens": "Athens, GA",
        "allen": "Allen, TX",
        "stoughton": "Boston",
        "lake jackson": "Houston",
    }

    for key, city in cities.items():
        if key in check_str:
            return city

    if loc_part:
        cleaned = re.sub(r'\d+\s+\w+\s+(dr|drive|st|street|ave|blvd|rd|way)\b.*', '', loc_part, flags=re.IGNORECASE).strip()
        if cleaned:
            return cleaned
    return loc_part


def parse_owner(email):
    """Extract first name from email."""
    owners = {
        "claudio.santos": "Claudio",
        "craig.freeman": "Craig",
        "megan.mccue": "Megan",
        "angela": "Angela",
        "lacey.henderson": "Lacey",
        "david.starkman": "David",
    }
    email_lower = email.lower().strip()
    for key, name in owners.items():
        if key in email_lower:
            return name
    m = re.match(r'([a-z]+)', email_lower)
    return m.group(1).title() if m else email


def parse_headcount(hc_str):
    """Parse headcount from string."""
    s = hc_str.strip()
    if not s:
        return 0
    if s.upper() == "LFDTW":
        return "LFDTW"
    m = re.search(r'(\d+)', s)
    if m:
        return int(m.group(1))
    return 0


def has_shifts(shift_info):
    """Determine if shifts are posted (Yes) or not (No/TBD)."""
    if not shift_info:
        return False
    s = shift_info.lower().strip()
    no_indicators = ["not posted", "tbd", "no posted", "shifts not posted",
                     "need to immediately start recruiting", "not yet",
                     "will be based on client posts", "dates/times tbd",
                     "shift not posted"]
    for ind in no_indicators:
        if ind in s:
            return False
    if re.search(r'\d+\s*(am|pm|a\.m|p\.m)', s, re.IGNORECASE):
        return True
    if re.search(r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun|m-f)', s, re.IGNORECASE):
        return True
    if len(s) > 10:
        return True
    return False


def parse_currency(val_str):
    """Parse a currency string to float."""
    if not val_str or val_str.strip() == '-':
        return 0.0
    s = val_str.strip().replace('$', '').replace(',', '').strip()
    try:
        return float(s)
    except ValueError:
        return 0.0


# =============================================================================
# LOAD DATA
# =============================================================================

def load_revenue_requests():
    """Load all Live and Declined rows from revenue requests CSV."""
    rows = []
    with open(REVENUE_CSV, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 12:
                continue
            status = row[2].strip()
            # Only Live or Declined
            if "Live" not in status and "Declined" not in status:
                continue
            is_declined = "Declined" in status

            client_job = row[0].strip()
            owner_email = row[1].strip()
            location_col = row[8].strip() if len(row) > 8 else ""
            role_col = row[5].strip()
            other_role = row[6].strip() if len(row) > 6 else ""
            shift_info = row[9].strip() if len(row) > 9 else ""
            start_date = row[10].strip() if len(row) > 10 else ""
            hc_str = row[11].strip() if len(row) > 11 else "0"

            client, location = extract_client_and_location(client_job, location_col)
            owner = parse_owner(owner_email)
            hc = parse_headcount(hc_str)

            # Role: use Role column, or other_role if Role is "Other", or extract from client_job
            role = role_col
            if role.lower() == "other" and other_role:
                role = other_role
            if not role:
                parts = re.split(r'\s*-\s*', client_job)
                if len(parts) >= 3:
                    role = parts[-1].strip()
                    if re.match(r'^\d', role) or len(role) > 60:
                        role = parts[2].strip() if len(parts) > 2 else ""

            shifts = has_shifts(shift_info)

            # Format start date as mmm/dd/yyyy
            formatted_date = start_date
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
                try:
                    dt = datetime.strptime(start_date, fmt)
                    formatted_date = dt.strftime('%b/%d/%Y')
                    break
                except ValueError:
                    continue

            # Parse start date for priority calculation
            start_dt = None
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
                try:
                    start_dt = datetime.strptime(start_date, fmt).date()
                    break
                except ValueError:
                    continue

            rows.append({
                'client_job': client_job,
                'client': client,
                'location': location,
                'owner': owner,
                'role': role,
                'hc': hc,
                'start_date': formatted_date,
                'start_dt': start_dt,
                'shifts': shifts,
                'shift_info': shift_info,
                'is_declined': is_declined,
                'status': status,
            })

    return rows


def load_fhs_requisitions():
    """Load FHS requisitions."""
    rows = []
    with open(FHS_CSV, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 13:
                continue
            client = row[5].strip()
            location = row[6].strip()
            status = row[12].strip()
            rsvps = int(row[10]) if row[10].strip().isdigit() else 0

            loc_norm = normalize_location(location)
            job_title = row[3].strip().lower() if len(row) > 3 else ""
            rows.append({
                'client': client.lower().strip(),
                'loc_norm': loc_norm,
                'job_title': job_title,
                'status': status,
                'rsvps': rsvps,
            })
    return rows


def load_indeed_campaigns():
    """Load Indeed campaigns from JobsCampaigns CSV.
    JobsCampaigns has: Campaign, Impressions, ..., Spend, ...
    No Status column — all campaigns with spend > 0 are relevant.
    Also include campaigns with spend=0 but that match naming patterns.
    """
    rows = []
    with open(INDEED_CSV, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            campaign_name = row.get('Campaign', '').strip()
            spend = parse_currency(row.get('Spend', '0'))

            # Skip meta rows
            if not campaign_name or campaign_name == "Jobs not in a campaign":
                continue
            # Skip non-B2C campaigns (e.g., "Senior Demand Generation Manager")
            if campaign_name.lower().startswith("senior demand"):
                continue

            client, location, role = _parse_campaign_name_with_role(campaign_name)
            if not client:
                continue

            loc_norm = normalize_location(location)
            rows.append({
                'client': client.lower().strip(),
                'loc_norm': loc_norm,
                'role': role.lower().strip() if role else '',
                'spend': spend,
                'name': campaign_name,
            })

    return rows


def _parse_campaign_name_with_role(name):
    """Parse Indeed campaign name to extract client, location, AND role.
    Format: US - B2C - {category} - {client} - {role} - {location} - {dates}
    Returns (client, location, role).
    """
    s = name.strip()
    parts = re.split(r'\s*-\s*', s)

    known_clients = {
        'cort', 'johnstone', 'bon appetit', 'evergreen', 'ontrac', 'tennant',
        'legends', 'culinaire', 'afc', 'foxconn', 'stord', 'powerstop',
        'power stop', 'powerststop', 'ryerson', 'bath concepts', 'btx',
        'ctdi', 'ingram', 'indeed flex', 'indeed', 'lettuce',
        'continental battery', 'hyatt', 'ac', 'levy', 'solaren',
        'uplift', 'soho house', 'soho', 'rhino', 'vestals', 'sxsw',
        'hei hotels', 'austin club', 'moody', 'freshella',
    }

    skip_words = {'us', 'b2c', 'industrial', 'hospitality', 'hiring event', 'clerical'}

    client = None
    location = None
    role = None

    # Find location (pattern "City, ST" or "City, oh" etc.)
    loc_idx = None
    for i, part in enumerate(parts):
        p = part.strip()
        if re.match(r'^[A-Za-z\s\.]+,\s*[A-Z]{2}$', p):
            location = p
            loc_idx = i
            break
        # Also match lowercase state: "Cincinnati, oh"
        if re.match(r'^[A-Za-z\s\.]+,\s*[A-Za-z]{2}$', p):
            location = p
            loc_idx = i
            break

    if loc_idx is not None:
        before_loc = [p.strip() for p in parts[:loc_idx]]
        candidate_parts = [p for p in before_loc if p.lower().strip() not in skip_words]

        combined = ' '.join(candidate_parts).lower()
        client_idx_in_candidates = None
        for kc in sorted(known_clients, key=len, reverse=True):
            if kc in combined:
                client = kc
                for ci, cp in enumerate(candidate_parts):
                    if kc in cp.lower():
                        client_idx_in_candidates = ci
                        break
                break

        if not client and candidate_parts:
            client = candidate_parts[0]
            client_idx_in_candidates = 0

        # Role = parts between client and location
        if client_idx_in_candidates is not None and client_idx_in_candidates + 1 < len(candidate_parts):
            role_parts = candidate_parts[client_idx_in_candidates + 1:]
            if role_parts:
                role = ' '.join(role_parts).strip()
    else:
        # No "City, ST" location found
        candidate_parts = [p.strip() for p in parts if p.strip().lower() not in skip_words]
        non_date_parts = []
        for cp in candidate_parts:
            if re.match(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d', cp, re.IGNORECASE):
                break
            non_date_parts.append(cp)

        combined = ' '.join(non_date_parts).lower()
        client_idx_in_nondates = None
        for kc in sorted(known_clients, key=len, reverse=True):
            if kc in combined:
                client = kc
                for ci, cp in enumerate(non_date_parts):
                    if kc in cp.lower():
                        client_idx_in_nondates = ci
                        break
                break
        if not client and non_date_parts:
            client = non_date_parts[0]
            client_idx_in_nondates = 0

        if client_idx_in_nondates is not None and client_idx_in_nondates + 1 < len(non_date_parts):
            role_parts = non_date_parts[client_idx_in_nondates + 1:]
            if role_parts:
                role = ' '.join(role_parts).strip()

        # Infer location from client defaults
        if client and not location:
            client_default_locations = {
                'levy': 'Chicago, IL',
                'bath concepts': 'Libertyville, IL',
                'foxconn': 'Fort Worth, TX',
                'ryerson': 'Dallas, TX',
                'sxsw': 'Austin, TX',
                'material handler': 'Haslet, TX',
            }
            location = client_default_locations.get(client.lower(), '')

    # Normalize client names
    if client:
        cl = client.lower().strip()
        if cl in ('powerstop', 'powerststop'):
            client = 'Power Stop'
        elif cl == 'ac':
            client = 'Austin Club'

    # Clean up role
    if role:
        role = re.sub(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s*\d+.*', '', role, flags=re.IGNORECASE).strip()
        role = re.sub(r'\b(premium|additional\s+location\w*)\b', '', role, flags=re.IGNORECASE).strip()
        role = role.strip(' -,')

    return client, location if location else "", role if role else ""


def load_ob_funnel():
    """Load OB Funnel data from Excel.
    Structure: Col 0 = Client (only on first row of client block)
               Col 1 = Location (only on first row of location block)
               Col 2 = Role slice ("Total" for aggregate, or role name like "Assembler")
               Col 3 = Metric name
    When Col 2 = "Total", it starts a block of ~14 metric rows.
    The first metric row has Col2="Total", subsequent rows in the block have Col2=None.
    We track the current role_slice and only capture metrics when role_slice == "Total".
    Grand Total is the last column (col 35 = index 34).
    Returns dict keyed by (client_lower, loc_norm) with created/verified/rtb.
    """
    data = defaultdict(lambda: {'created': 0, 'verified': 0, 'rtb': 0})

    wb = openpyxl.load_workbook(OB_FUNNEL_XLSX, data_only=True)
    ws = wb.active

    current_client = None
    current_loc = None
    current_role_slice = None
    grand_total_col = ws.max_column  # Last column is Grand Total (col 35 = index 34)

    for row in ws.iter_rows(min_row=2, values_only=False):
        cells = [c.value for c in row]

        if cells[0] is not None and str(cells[0]).strip():
            current_client = str(cells[0]).strip()
        if cells[1] is not None and str(cells[1]).strip():
            current_loc = str(cells[1]).strip()
        if cells[2] is not None and str(cells[2]).strip():
            current_role_slice = str(cells[2]).strip()

        # Only capture metrics when we are in a "Total" block
        if current_role_slice != "Total":
            continue

        metric = cells[3]  # Col 3 = metric name
        if not metric or not current_client or not current_loc:
            continue

        metric_str = str(metric).strip()
        grand_total = cells[grand_total_col - 1]  # 0-indexed
        if grand_total is None:
            grand_total = 0
        try:
            val = int(float(grand_total))
        except (ValueError, TypeError):
            val = 0

        loc_norm = normalize_location(current_loc)
        key = (current_client.lower().strip(), loc_norm)

        if "Worker Accounts Created" in metric_str:
            data[key]['created'] += val
        elif "1st Role Verified" in metric_str:
            data[key]['verified'] += val
        elif '"Ready to Book" Estimate' in metric_str:
            data[key]['rtb'] += val

    wb.close()
    return data


# =============================================================================
# CROSS-REFERENCE MATCHING
# =============================================================================

def _fuzzy_client_match(a, b):
    """Basic fuzzy matching for client names."""
    for suffix in [', inc', ' inc', ', llc', ' llc', ', ltd', ' ltd']:
        a = a.replace(suffix, '')
        b = b.replace(suffix, '')
    a = a.strip().rstrip('.')
    b = b.strip().rstrip('.')
    if a == b:
        return True
    if a in b or b in a:
        return True
    a_words = a.split()
    b_words = b.split()
    if a_words and b_words and a_words[0] == b_words[0] and len(a_words[0]) > 3:
        return True
    return False


def _location_match(loc_a, loc_b):
    """Check if two normalized locations match."""
    if not loc_a or not loc_b:
        return not loc_a and not loc_b
    a = loc_a.lower().strip()
    b = loc_b.lower().strip()
    if a == b:
        return True
    if a in b or b in a:
        return True
    if "/" in a:
        parts = a.split("/")
        return any(p.strip() == b for p in parts)
    if "/" in b:
        parts = b.split("/")
        return any(p.strip() == a for p in parts)
    return False


def _role_match(rev_role, fhs_job_title):
    """Check if a revenue request role matches an FHS job title."""
    a = rev_role.lower().strip()
    b = fhs_job_title.lower().strip()
    if not a or not b:
        return True
    if a == b:
        return True
    if a in b or b in a:
        return True
    role_aliases = {
        'food preps': ['prep cook', 'prep'],
        'prep cook': ['food preps', 'prep'],
        'prep': ['prep cook', 'food preps'],
        'loader/crew': ['loader', 'crew', 'lc', 'loader / crew'],
        'loader': ['loader/crew', 'crew', 'lc', 'loader / crew'],
        'loader / crew': ['loader/crew', 'loader', 'crew', 'lc'],
        'lc': ['loader/crew', 'loader', 'crew'],
        'warehouse operative': ['warehouse', 'warehouse operator', 'picker packer', 'material handler', 'wo'],
        'warehouse operator': ['warehouse', 'warehouse operative', 'picker packer', 'material handler', 'wo'],
        'wo': ['warehouse operative', 'warehouse operator', 'warehouse'],
        'picker packer': ['warehouse operative', 'warehouse operator', 'warehouse', 'pp'],
        'pp': ['picker packer', 'warehouse operative', 'warehouse'],
        'material handler': ['warehouse operative', 'warehouse operator', 'warehouse'],
        'industrial general labor': ['industrial general laborer', 'general labor', 'general laborer', 'igl'],
        'industrial general laborer': ['industrial general labor', 'general labor', 'general laborer', 'igl'],
        'igl': ['industrial general labor', 'industrial general laborer', 'general labor'],
        'dishwasher': ['dishwash', 'dishwhasher'],
        'dishwash': ['dishwasher', 'dishwhasher'],
        'server': ['event server', 'buffet server', 'banquet server', 'servers'],
        'servers': ['server', 'event server', 'buffet server'],
        'event server': ['server'],
        'buffet server': ['server'],
        'barista': ['barista'],
        'bartender': ['bartender', 'bart'],
        'cashier': ['cashier'],
        'assembler': ['assembler'],
        'repair technician': ['repair tech', 'cellphone repair specialist', 'repair specialist'],
        'repair tech': ['repair technician', 'cellphone repair specialist'],
        'htl': ['hospitality', 'hospitality general labor'],
        'hospitality': ['htl', 'hospitality general labor'],
        'concession stand worker': ['concessions', 'concession'],
        'concessions': ['concession stand worker'],
        'multi': ['hospitality', 'general'],
        'forklift': ['forklift driver', 'forklift operator'],
        'forklift driver': ['forklift'],
        'lead generation specialist': ['lead generation', 'lead gen'],
    }
    aliases = role_aliases.get(a, [])
    for alias in aliases:
        if alias in b or b in alias:
            return True
    return False


def match_fhs(client_short, location, fhs_rows, role=None):
    """Find FHS data matching a revenue request client+location.
    Open count: only open + auto-paused status reqs
    Interview (RSVPs): sum from open + auto-paused reqs
    """
    possible_clients = normalize_client_for_match(client_short)
    loc_norm = normalize_location(location)

    total = {'count': 0, 'rsvps': 0}

    for fhs_row in fhs_rows:
        client_match = False
        for pc in possible_clients:
            pc_lower = pc.lower().strip()
            if (pc_lower in fhs_row['client'] or fhs_row['client'] in pc_lower or
                    _fuzzy_client_match(pc_lower, fhs_row['client'])):
                client_match = True
                break
        if not client_match:
            continue
        if not _location_match(loc_norm, fhs_row['loc_norm']):
            continue

        # Role filtering
        if role:
            if not fhs_row['job_title']:
                continue
            if not _role_match(role, fhs_row['job_title']):
                continue

        # Open count: only open + auto-paused
        if fhs_row['status'] in ('open', 'auto-paused'):
            total['count'] += 1
            total['rsvps'] += fhs_row['rsvps']

    return total


def match_indeed(client_short, location, indeed_rows, role=None):
    """Find Indeed campaign data matching a revenue request client+location."""
    possible_clients = normalize_client_for_match(client_short)
    loc_norm = normalize_location(location)

    total = {'count': 0, 'spend': 0.0}

    for ind_row in indeed_rows:
        client_match = False
        for pc in possible_clients:
            pc_lower = pc.lower().strip()
            if (pc_lower in ind_row['client'] or ind_row['client'] in pc_lower or
                    _fuzzy_client_match(pc_lower, ind_row['client'])):
                client_match = True
                break
        if not client_match:
            continue
        if not _location_match(loc_norm, ind_row['loc_norm']):
            continue

        # Role filtering
        if role and ind_row['role']:
            if not _role_match(role, ind_row['role']):
                continue

        total['count'] += 1
        total['spend'] += ind_row['spend']

    return total


# OB Funnel client overrides for DC Flex
OB_FUNNEL_CLIENT_OVERRIDES = {
    "dc flex": ["cort", "ontrac final mile", "ontrac"],
}


def match_ob_funnel(client_short, location, ob_data):
    """Find OB Funnel data matching a revenue request client+location.
    Priority:
      1. client + location match
      2. location-only match (across all clients)
    """
    possible_clients = normalize_client_for_match(client_short)
    override_clients = OB_FUNNEL_CLIENT_OVERRIDES.get(client_short.lower().strip(), [])
    if override_clients:
        possible_clients = possible_clients + override_clients
    loc_norm = normalize_location(location)

    total = {'created': 0, 'verified': 0, 'rtb': 0}

    # 1. Try client + location
    matched = False
    for (ob_client, ob_loc), vals in ob_data.items():
        if not _location_match(loc_norm, ob_loc):
            continue
        client_match = False
        for pc in possible_clients:
            pc_lower = pc.lower().strip()
            if (pc_lower in ob_client or ob_client in pc_lower or
                    _fuzzy_client_match(pc_lower, ob_client)):
                client_match = True
                break
        if not client_match:
            continue

        total['created'] += vals['created']
        total['verified'] += vals['verified']
        total['rtb'] += vals['rtb']
        matched = True

    if matched:
        return total

    # 2. Fallback: location-only (sum all clients at this metro)
    if loc_norm:
        for (ob_client, ob_loc), vals in ob_data.items():
            if _location_match(loc_norm, ob_loc):
                total['created'] += vals['created']
                total['verified'] += vals['verified']
                total['rtb'] += vals['rtb']

    return total


# =============================================================================
# PRIORITY CALCULATION
# =============================================================================

def calculate_priority(row, fhs, indeed):
    """Calculate priority score for a row.
    Base: HC / 10, capped at 10
    +2 if no FHS reqs found
    +1 if no Indeed campaigns
    +1 if start date is within 14 days
    Cap at 10
    """
    hc = row['hc'] if isinstance(row['hc'], int) else 0
    p = min(hc / 10, 10)

    if fhs['count'] == 0:
        p += 2
    if indeed['count'] == 0:
        p += 1
    if row.get('start_dt'):
        days_until = (row['start_dt'] - TODAY).days
        if days_until <= 14:
            p += 1

    return min(round(p, 1), 10)


# =============================================================================
# HTML GENERATION
# =============================================================================

def generate_html(processed_rows):
    """Generate the full HTML report."""
    # Sort by priority descending, then by client name
    processed_rows.sort(key=lambda r: (-r['priority'], r['client'].lower()))

    # Calculate KPIs
    live_rows = [r for r in processed_rows if not r.get('is_declined')]
    declined_rows = [r for r in processed_rows if r.get('is_declined')]
    total_live = len(live_rows)
    total_hc = sum(r['hc'] for r in live_rows if isinstance(r['hc'], int))
    high_priority = sum(1 for r in live_rows if r['priority'] >= 7)
    no_fhs = sum(1 for r in live_rows if r['fhs']['count'] == 0)
    no_indeed = sum(1 for r in live_rows if r['indeed']['count'] == 0)
    shifts_tbd = sum(1 for r in live_rows if not r['shifts'])

    rows_html = ""
    for r in processed_rows:
        is_declined = r.get('is_declined', False)
        p = r['priority']

        # Priority color-coding
        if is_declined:
            bg = "#f3f4f6"
        elif p >= 7:
            bg = "#fef2f2"  # Red tint
        elif p >= 4:
            bg = "#fffbeb"  # Amber tint
        else:
            bg = "#ffffff"

        # Priority cell styling
        if is_declined:
            p_bg = "#9ca3af"
            p_color = "#fff"
            p_display = "D"
        elif p >= 7:
            p_bg = "#dc2626"
            p_color = "#fff"
            p_display = f"{p:.0f}" if p == int(p) else f"{p:.1f}"
        elif p >= 4:
            p_bg = "#f59e0b"
            p_color = "#fff"
            p_display = f"{p:.0f}" if p == int(p) else f"{p:.1f}"
        else:
            p_bg = "#e5e7eb"
            p_color = "#374151"
            p_display = f"{p:.0f}" if p == int(p) else f"{p:.1f}"

        hc_display = str(r['hc']) if isinstance(r['hc'], int) else r['hc']
        shifts_tag = ('<span style="background:#dcfce7;color:#166534;padding:2px 8px;border-radius:4px;font-size:12px;">Yes</span>'
                      if r['shifts'] else
                      '<span style="background:#fef3c7;color:#92400e;padding:2px 8px;border-radius:4px;font-size:12px;">No</span>')

        # Metric cells for declined rows are BLANK
        if is_declined:
            fhs_open_html = ""
            fhs_interview_html = ""
            indeed_st_html = ""
            indeed_camps_html = ""
            indeed_spend_html = ""
            ob_created_html = ""
            ob_verified_html = ""
            ob_rtb_html = ""
            target_html = ""
            fill_cell_html = ""
        else:
            fhs_open_html = f'{r["fhs"]["count"]}'
            fhs_interview_html = f'{r["fhs"]["rsvps"]:,}'

            # Indeed status emoji
            if r['indeed']['count'] > 0 and r['indeed']['spend'] > 0:
                indeed_st_html = "✅"
            elif r['indeed']['count'] > 0:
                indeed_st_html = "⚠️"
            else:
                indeed_st_html = "❌"
            indeed_camps_html = f'{r["indeed"]["count"]}'
            indeed_spend_html = f"${r['indeed']['spend']:,.0f}" if r['indeed']['spend'] > 0 else "$0"

            ob_created_html = f'{r["ob"]["created"]}'
            ob_verified_html = f'{r["ob"]["verified"]}'
            ob_rtb_html = f'{r["ob"]["rtb"]}'

            # Target = HC × 10
            hc_val = r['hc'] if isinstance(r['hc'], int) else 0
            target = hc_val * 10
            target_html = f'{target:,}' if target > 0 else '—'

            # Fill% = RTB / HC
            ob_rtb = r['ob']['rtb']
            if hc_val > 0:
                fill_pct = min((ob_rtb / hc_val) * 100, 100)
                fill_color = "#ef4444" if fill_pct < 25 else "#f59e0b" if fill_pct < 50 else "#22c55e"
                fill_cell_html = f'''<div style="display:flex;align-items:center;gap:6px;">
            <div style="flex:1;background:#e5e7eb;border-radius:4px;height:14px;min-width:60px;">
                <div style="width:{fill_pct:.1f}%;background:{fill_color};height:100%;border-radius:4px;"></div>
            </div>
            <span style="font-size:13px;font-weight:bold;min-width:40px;text-align:right;">{fill_pct:.0f}%</span>
        </div>'''
            else:
                fill_cell_html = '<span style="color:#9ca3af;">—</span>'

        # Escape HTML
        client_safe = r['client'].replace('&', '&amp;').replace('<', '&lt;')
        location_safe = r['location'].replace('&', '&amp;').replace('<', '&lt;') if r['location'] else ''
        role_safe = r['role'].replace('&', '&amp;').replace('<', '&lt;') if r['role'] else ''

        status_label = ''
        if is_declined:
            status_label = '<br><span style="background:#9ca3af;color:white;padding:2px 6px;border-radius:4px;font-size:11px;">DECLINED</span>'

        rows_html += f'''<tr style="background:{bg};">
        <td style="text-align:center;font-weight:800;font-size:15px;color:{p_color};background:{p_bg};min-width:36px;border-radius:0;">{p_display}</td>
        <td><strong>{client_safe}</strong><br><span style="color:#6b7280;font-size:12px;">{location_safe}</span>{status_label}</td>
        <td>{r['owner']}</td>
        <td>{role_safe}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{hc_display}</td>
        <td style="text-align:center;font-size:13px;">{r['start_date']}</td>
        <td style="text-align:center;">{shifts_tag}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{fhs_open_html}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{fhs_interview_html}</td>
        <td style="text-align:center;">{indeed_st_html}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{indeed_camps_html}</td>
        <td style="text-align:right;font-weight:bold;font-size:15px;">{indeed_spend_html}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{ob_created_html}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{ob_verified_html}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{ob_rtb_html}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{target_html}</td>
        <td style="min-width:120px;">{fill_cell_html}</td>
    </tr>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Revenue Requests Cross-Reference Dashboard — {REPORT_DATE}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f3f4f6; font-size: 14px; color: #111827; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); color: white; padding: 24px 32px; }}
        .header h1 {{ font-size: 22px; font-weight: 700; }}
        .header p {{ font-size: 13px; opacity: 0.85; margin-top: 4px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; padding: 20px 32px; }}
        .kpi-card {{ background: white; border-radius: 12px; padding: 16px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }}
        .kpi-card .number {{ font-size: 32px; font-weight: 800; line-height: 1.2; }}
        .kpi-card .label {{ font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }}
        .kpi-card.red .number {{ color: #ef4444; }}
        .kpi-card.amber .number {{ color: #f59e0b; }}
        .kpi-card.blue .number {{ color: #2563eb; }}
        .kpi-card.green .number {{ color: #22c55e; }}
        .table-container {{ margin: 0 32px 32px; background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }}
        .table-scroll {{ overflow-y: auto; max-height: calc(100vh - 60px); }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        thead th {{ position: sticky; top: 0; z-index: 20; }}
        thead tr:first-child th {{ position: sticky; top: 0; z-index: 20; }}
        thead tr:nth-child(2) th {{ position: sticky; top: 34px; z-index: 19; }}
        th {{ background: #1e3a5f; color: white; padding: 8px 10px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; white-space: nowrap; }}
        th.group-header {{ background: #0f2540; padding: 6px 10px; font-size: 11px; text-align: center; border-left: 2px solid rgba(255,255,255,0.15); }}
        th.sub-header {{ background: #1e3a5f; font-size: 11px; }}
        td {{ padding: 8px 10px; border-bottom: 1px solid #e5e7eb; font-size: 14px; vertical-align: middle; }}
        tr:hover {{ filter: brightness(0.97); }}
        .legend {{ margin: 12px 32px; display: flex; gap: 24px; font-size: 12px; color: #6b7280; }}
        .legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
        .legend .dot {{ width: 12px; height: 12px; border-radius: 3px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Revenue Requests Cross-Reference Dashboard</h1>
        <p>Generated {REPORT_DATE} | Sorted by priority (descending) | Every revenue request row = one table row (no merging) | Data: FHS Requisitions, Indeed JobsCampaigns, OB Funnel</p>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="number">{total_live}</div>
            <div class="label">Live Requests</div>
        </div>
        <div class="kpi-card blue">
            <div class="number">{total_hc:,}</div>
            <div class="label">Total HC</div>
        </div>
        <div class="kpi-card red">
            <div class="number">{high_priority}</div>
            <div class="label">High Priority (P>=7)</div>
        </div>
        <div class="kpi-card red">
            <div class="number">{no_fhs}</div>
            <div class="label">No FHS</div>
        </div>
        <div class="kpi-card amber">
            <div class="number">{no_indeed}</div>
            <div class="label">No Indeed</div>
        </div>
        <div class="kpi-card amber">
            <div class="number">{shifts_tbd}</div>
            <div class="label">Shifts TBD</div>
        </div>
    </div>

    <div class="legend">
        <span><span class="dot" style="background:#fef2f2;border:1px solid #fecaca;"></span> P >= 7 (High)</span>
        <span><span class="dot" style="background:#fffbeb;border:1px solid #fde68a;"></span> P 4-6 (Medium)</span>
        <span><span class="dot" style="background:#ffffff;border:1px solid #d1d5db;"></span> P 0-3 (Low)</span>
        <span><span class="dot" style="background:#f3f4f6;border:1px solid #d1d5db;"></span> Declined</span>
    </div>

    <div class="table-container">
        <div class="table-scroll">
            <table id="mainTable">
                <thead>
                    <tr>
                        <th rowspan="2" style="min-width:36px;">P</th>
                        <th rowspan="2" style="min-width:160px;">Client</th>
                        <th rowspan="2" style="min-width:70px;">Owner</th>
                        <th rowspan="2" style="min-width:120px;">Role</th>
                        <th rowspan="2" style="min-width:40px;">HC</th>
                        <th rowspan="2" style="min-width:90px;">Start</th>
                        <th rowspan="2" style="min-width:55px;">Shifts</th>
                        <th colspan="2" class="group-header">FHS</th>
                        <th colspan="3" class="group-header">Indeed</th>
                        <th colspan="3" class="group-header">OB Funnel</th>
                        <th colspan="2" class="group-header">Fill</th>
                    </tr>
                    <tr>
                        <th class="sub-header" style="text-align:center;">Open</th>
                        <th class="sub-header" style="text-align:center;">Interview</th>
                        <th class="sub-header" style="text-align:center;">St</th>
                        <th class="sub-header" style="text-align:center;">Camps</th>
                        <th class="sub-header" style="text-align:right;">Spend</th>
                        <th class="sub-header" style="text-align:center;">Created</th>
                        <th class="sub-header" style="text-align:center;">Verified</th>
                        <th class="sub-header" style="text-align:center;">RTB</th>
                        <th class="sub-header" style="text-align:center;">Target</th>
                        <th class="sub-header" style="text-align:center;">Fill%</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>'''

    return html


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("Loading Revenue Requests...")
    revenue_rows = load_revenue_requests()
    live_count = sum(1 for r in revenue_rows if not r['is_declined'])
    declined_count = sum(1 for r in revenue_rows if r['is_declined'])
    print(f"  Found {live_count} Live + {declined_count} Declined = {len(revenue_rows)} total rows")

    print("Loading FHS Requisitions...")
    fhs_rows = load_fhs_requisitions()
    print(f"  Loaded {len(fhs_rows)} individual FHS rows")

    print("Loading Indeed Campaigns (JobsCampaigns)...")
    indeed_data = load_indeed_campaigns()
    print(f"  Loaded {len(indeed_data)} individual campaign rows")

    print("Loading OB Funnel...")
    ob_data = load_ob_funnel()
    print(f"  Loaded {len(ob_data)} client+location groups")

    print("\nCross-referencing...")
    processed = []
    for i, row in enumerate(revenue_rows):
        if row['is_declined']:
            fhs = {'count': 0, 'rsvps': 0}
            indeed = {'count': 0, 'spend': 0.0}
            ob = {'created': 0, 'verified': 0, 'rtb': 0}
            priority = 0
        else:
            fhs = match_fhs(row['client'], row['location'], fhs_rows, row.get('role'))
            indeed = match_indeed(row['client'], row['location'], indeed_data, row.get('role'))
            ob = match_ob_funnel(row['client'], row['location'], ob_data)
            priority = calculate_priority(row, fhs, indeed)

        processed.append({
            **row,
            'fhs': fhs,
            'indeed': indeed,
            'ob': ob,
            'priority': priority,
        })

        status_tag = "DECLINED" if row['is_declined'] else "LIVE"
        print(f"  [{i+1:2d}] {row['client']:20s} | {row['location']:20s} | P={priority:>4} | FHS={fhs['count']:>2} | Indeed={indeed['count']:>2} ${indeed['spend']:>8,.0f} | OB RTB={ob['rtb']:>4} [{status_tag}]")

    print(f"\nGenerating HTML report...")
    html = generate_html(processed)

    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML saved to: {OUTPUT_HTML}")
    print(f"Total rows: {len(processed)} ({live_count} Live + {declined_count} Declined)")

    # KPI summary
    live_processed = [r for r in processed if not r['is_declined']]
    total_hc = sum(r['hc'] for r in live_processed if isinstance(r['hc'], int))
    high_p = sum(1 for r in live_processed if r['priority'] >= 7)
    no_fhs_count = sum(1 for r in live_processed if r['fhs']['count'] == 0)
    no_indeed_count = sum(1 for r in live_processed if r['indeed']['count'] == 0)
    shifts_tbd_count = sum(1 for r in live_processed if not r['shifts'])
    print(f"KPIs: Live={len(live_processed)}, HC={total_hc}, HighP={high_p}, NoFHS={no_fhs_count}, NoIndeed={no_indeed_count}, ShiftsTBD={shifts_tbd_count}")


if __name__ == "__main__":
    main()
