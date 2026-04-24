#!/usr/bin/env python3
"""
Generate Report 4: Recruitment Request Dashboard
Cross-reference HTML report combining Revenue Requests, FHS Requisitions,
Indeed Campaigns, and OB Funnel data.
"""

import csv
import re
import openpyxl
from collections import defaultdict
from datetime import datetime
import html as html_module

REPORT_DATE = "2026-04-13"
OUTPUT_PATH = f"/Users/claudio.santos/RM-Team-Ai/docs/reports/recruitment-request-dashboard-{REPORT_DATE}.html"

# Input files
REVENUE_REQUESTS_PATH = "/Users/claudio.santos/Downloads/US_Recruitment_Requests__us_ (16).csv"
REQUISITIONS_PATH = "/Users/claudio.santos/Downloads/requisitions-2026-04-10-074617.csv"
INDEED_CAMPAIGNS_PATH = "/Users/claudio.santos/Downloads/JobsCampaigns_20260401_20260410.csv"
OB_FUNNEL_PATH = "/Users/claudio.santos/Downloads/OB Funnel Custom Viewer (30).xlsx"

# ============================================================
# CLIENT / METRO NORMALIZATION
# ============================================================
CLIENT_ALIASES = {
    "compass": "culinaire",
    "dc flex": "cort",
    "food glorious": "culinaire",
    "aba nashville": "lettuce",
    "texas motor speedway": "levy",
}

METRO_ALIASES = {
    "dfw": "dallas",
    "vegas": "las vegas",
    "bedford park": "chicago",
    "woodbridge": "chicago",
    "washington dc": "washington, d.c.",
    "washington d.c.": "washington, d.c.",
    "washington": "washington, d.c.",
    "grove city": "columbus",
    "la vergne": "nashville",
    "lavergne": "nashville",
    "haslet": "dallas",
    "sparks": "reno",
    "fort worth": "dallas",
    "libertyville": "chicago",
    "mccarran": "reno",
    "erlanger": "cincinnati",
    "fairfield": "cincinnati",
    "hebron": "cincinnati",
    "boca raton": "orlando",
    "hollywood": "orlando",
    "carrollton": "dallas",
    "carrolton": "dallas",
    "arlington": "dallas",
    "lancaster": "dallas",
    "hodgkins": "chicago",
    "springdale": "cincinnati",
    "west chester": "cincinnati",
    "mount juliet": "nashville",
    "mt juliet": "nashville",
    "fort mill": "charlotte",
}

# State code -> metro mapping (fallback when city extraction fails)
STATE_METRO_MAP = {
    "tx": "dallas",
    "tn": "nashville",
    "nv": "las vegas",
    "il": "chicago",
    "ga": "atlanta",
    "oh": "columbus",
    "fl": "orlando",
    "nc": "charlotte",
    "az": "phoenix",
    "ma": "boston",
    "dc": "washington, d.c.",
}

# FHS client name mapping (revenue request name -> FHS client names)
FHS_CLIENT_MAP = {
    "cort": ["cort"],
    "culinaire": ["culinaire", "culinaire international"],
    "levy": ["levy restaurants", "levy"],
    "legends": ["legends hospitality", "legends"],
    "lettuce": ["lettuce entertain you enterprises, inc", "lettuce entertain you", "lettuce"],
    "ontrac": ["ontrac final mile", "ontrac"],
    "stord": ["stord, inc", "stord"],
    "ingram": ["ingram content group", "ingram"],
    "foxconn": ["foxconn"],
    "ctdi": ["ctdi"],
    "power stop": ["power stop"],
    "bon appetit": ["bon appetit management company, inc", "bon appetit"],
    "soho house": ["soho house austin", "soho house"],
    "vestals": ["vestals catering"],
    "assurant": ["assurant, inc (hyla)", "assurant"],
    "smurfit": ["smurfit kappa", "smurfit"],
    "sigma": ["sigma"],
    "roka": ["roka"],
    "hyatt": ["hyatt"],
    "tennant": ["tennant solutions", "tennant"],
    "johnstone": ["johnstone supply", "johnstone"],
    "merritt": ["merritt hospitality llc", "merritt hospitality", "merritt"],
    "continental": ["continental battery systems", "continental battery"],
    "chartwells": ["chartwells higher education", "chartwells"],
    "pearson": ["pearson"],
    "green worldwide": ["green worldwide shipping", "green worldwide"],
    "six flags": ["six flags"],
    "rhino": ["rhino staging", "rhino"],
    "g texas": ["g texas catering", "g texas"],
    "stadium people": ["stadium people"],
    "vacasun": ["vacasun"],
    "austin arena": ["austin arena company", "austin arena"],
    "indeed flex": ["indeed flex applications", "indeed flex", "indeed inc"],
}


def normalize_client(name):
    """Normalize client name for matching"""
    if not name:
        return ""
    n = name.strip().lower()
    for alias, canonical in CLIENT_ALIASES.items():
        if alias in n:
            return canonical
    return n


def normalize_location(loc):
    """Extract city from location string and normalize"""
    if not loc:
        return ""
    loc = loc.strip()

    # Remove zip codes
    loc = re.sub(r'\d{5}(-\d{4})?', '', loc).strip().rstrip(',').strip()

    # Check if the entire string is a known city or alias directly
    loc_lower = loc.lower().strip()
    for alias, canonical in METRO_ALIASES.items():
        if alias in loc_lower:
            return canonical

    # Check for well-known city names anywhere in the string
    known_cities = [
        "dallas", "chicago", "nashville", "austin", "atlanta", "orlando",
        "houston", "las vegas", "charlotte", "columbus", "cincinnati",
        "reno", "phoenix", "philadelphia", "boston", "newark",
        "fort worth", "boca raton", "bedford park", "grove city",
        "la vergne", "lavergne", "sparks", "haslet",
    ]
    for city in known_cities:
        if city in loc_lower:
            # Apply metro alias
            for alias, canonical in METRO_ALIASES.items():
                if alias == city:
                    return canonical
            return city

    # Try standard City, State format
    parts = [p.strip() for p in loc.split(",")]
    if len(parts) >= 2:
        city = parts[0].strip().lower()
        # If first part looks like an address (starts with number), try second part
        if re.match(r'^\d', city):
            # Try to find city in remaining parts
            for part in parts[1:]:
                p_clean = part.strip().lower()
                p_clean = re.sub(r'\b[a-z]{2}\b$', '', p_clean).strip()
                if p_clean and not re.match(r'^\d', p_clean) and len(p_clean) > 2:
                    for alias, canonical in METRO_ALIASES.items():
                        if alias == p_clean or alias in p_clean:
                            return canonical
                    return p_clean
        else:
            for alias, canonical in METRO_ALIASES.items():
                if alias == city or alias in city:
                    return canonical
            return city

    # Single value - might be a state abbreviation
    city = parts[0].strip().lower()
    if len(city) == 2 and city in STATE_METRO_MAP:
        return STATE_METRO_MAP[city]

    # Check if it's a state name
    state_names = {
        "texas": "tx", "tennessee": "tn", "nevada": "nv",
        "illinois": "il", "georgia": "ga", "ohio": "oh",
        "florida": "fl", "north carolina": "nc", "arizona": "az",
    }
    if city in state_names:
        return STATE_METRO_MAP.get(state_names[city], city)

    for alias, canonical in METRO_ALIASES.items():
        if alias == city:
            return canonical

    return city


def extract_state(loc):
    """Extract state abbreviation from location"""
    if not loc:
        return "Unknown"
    # Match 2-letter state code after comma
    m = re.search(r',\s*([A-Z]{2})\b', loc)
    if m:
        return m.group(1)
    m = re.search(r',\s*([a-zA-Z]{2})\s*\d', loc)
    if m:
        return m.group(1).upper()
    # Check for state abbreviation anywhere
    m = re.search(r'\b([A-Z]{2})\s*\d{5}', loc)
    if m:
        return m.group(1)
    # Check for state names
    loc_lower = loc.lower()
    state_names = {
        "texas": "TX", "tennessee": "TN", "nevada": "NV",
        "illinois": "IL", "georgia": "GA", "ohio": "OH",
        "florida": "FL", "north carolina": "NC", "arizona": "AZ",
        "massachusetts": "MA", "washington dc": "DC", "d.c.": "DC",
    }
    for name, code in state_names.items():
        if name in loc_lower:
            return code
    # Metro-based state inference
    metro_state = {
        "dallas": "TX", "fort worth": "TX", "austin": "TX", "houston": "TX",
        "haslet": "TX",
        "chicago": "IL", "bedford park": "IL", "libertyville": "IL",
        "nashville": "TN", "la vergne": "TN", "lavergne": "TN",
        "las vegas": "NV", "sparks": "NV", "reno": "NV",
        "atlanta": "GA",
        "charlotte": "NC",
        "orlando": "FL", "boca raton": "FL", "hollywood": "FL",
        "columbus": "OH", "grove city": "OH", "fairfield": "OH",
        "cincinnati": "OH", "hebron": "OH", "erlanger": "OH",
        "phoenix": "AZ",
        "boston": "MA",
    }
    for city, state in metro_state.items():
        if city in loc_lower:
            return state
    return "Unknown"


def shorten_client(client_job):
    """Extract short client name from Client - Job field"""
    if not client_job:
        return ""
    parts = client_job.split(" - ")
    return parts[0].strip()


def get_owner_first(email):
    """Extract first name from email"""
    if not email:
        return ""
    local = email.split("@")[0]
    first = local.split(".")[0]
    return first.capitalize()


def parse_submission_date(date_str):
    """Parse submission date from format like '01/04/2025, 09:07'"""
    if not date_str:
        return None
    date_str = date_str.strip()
    for fmt in ["%d/%m/%Y, %H:%M", "%d/%m/%Y", "%m/%d/%Y, %H:%M", "%m/%d/%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    return None


def parse_shift_start(date_str):
    """Parse shift start date"""
    if not date_str:
        return None
    date_str = date_str.strip()
    for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    return None


def format_date_display(dt):
    """Format date as mmm/dd/yyyy"""
    if not dt:
        return ""
    return dt.strftime("%b/%d/%Y")


def get_headcount(hc_str):
    """Parse headcount"""
    if not hc_str:
        return 0
    try:
        return int(float(hc_str.strip()))
    except ValueError:
        return 0


def get_role(row):
    """Get role from request"""
    role = row.get("Role", "").strip()
    if role == "Other":
        other = row.get("If 'Other'", "").strip()
        if other:
            return other
    return role


def extract_location_from_client_job(client_job):
    """Extract location hint from Client - Job field when location field is unusable"""
    if not client_job:
        return ""
    # Common pattern: "Client - City - Role" or "Client- City - Role"
    parts = re.split(r'\s*-\s*', client_job)
    # Known cities to look for in the parts
    known_cities_map = {
        "orlando": "orlando", "chicago": "chicago", "dallas": "dallas",
        "nashville": "nashville", "austin": "austin", "atlanta": "atlanta",
        "houston": "houston", "las vegas": "las vegas", "charlotte": "charlotte",
        "columbus": "columbus", "cincinnati": "cincinnati", "reno": "reno",
        "phoenix": "phoenix", "philadelphia": "philadelphia", "boston": "boston",
        "fort worth": "dallas", "bedford park": "chicago", "arlington": "dallas",
        "lavergne": "nashville", "la vergne": "nashville",
        "washington": "washington, d.c.",
    }
    for part in parts:
        p = part.strip().lower()
        for city_key, city_val in known_cities_map.items():
            if city_key in p:
                return city_val
    return ""


def get_client_aliases(client_norm):
    """Get all possible client name variations for FHS matching"""
    aliases = [client_norm]
    for key, vals in FHS_CLIENT_MAP.items():
        if key in client_norm or client_norm in key:
            aliases.extend(vals)
    return list(set(aliases))


def fmt_number(n):
    """Format number with comma separator"""
    if n == 0:
        return "0"
    return f"{n:,}"


def progress_bar_html(fill_pct):
    """Generate fill% progress bar"""
    capped = min(fill_pct, 100)
    if fill_pct >= 75:
        color = "#22c55e"
    elif fill_pct >= 40:
        color = "#f59e0b"
    else:
        color = "#ef4444"
    pct_display = min(int(round(fill_pct)), 999)
    return f'''<div style="display:flex;align-items:center;gap:6px;">
        <div style="flex:1;background:#e5e7eb;border-radius:4px;height:14px;min-width:60px;">
            <div style="width:{capped:.1f}%;background:{color};height:100%;border-radius:4px;"></div>
        </div>
        <span style="font-size:13px;font-weight:bold;min-width:40px;text-align:right;">{pct_display}%</span>
    </div>'''


# ============================================================
# 1. READ REVENUE REQUESTS
# ============================================================
requests_data = []
with open(REVENUE_REQUESTS_PATH, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        requests_data.append(row)

print(f"Revenue Requests: {len(requests_data)}")

# ============================================================
# 2. READ REQUISITIONS
# ============================================================
reqs_data = []
with open(REQUISITIONS_PATH, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        reqs_data.append(row)

print(f"Requisitions: {len(reqs_data)}")

# ============================================================
# 3. READ INDEED CAMPAIGNS
# ============================================================
campaigns_data = []
with open(INDEED_CAMPAIGNS_PATH, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        campaigns_data.append(row)

print(f"Indeed Campaigns: {len(campaigns_data)}")

# ============================================================
# 4. READ OB FUNNEL
# ============================================================
wb = openpyxl.load_workbook(OB_FUNNEL_PATH, data_only=True)
ws = wb.active

ob_data = {}  # (client_lower, location_lower) -> {created, verified, rtb}

current_client = None
current_location = None
in_total_group = False
current_key = None

for row in ws.iter_rows(min_row=2, values_only=False):
    c = row[0].value
    l = row[1].value
    total_label = row[2].value
    metric = str(row[3].value) if row[3].value else ""
    grand_total = row[34].value if len(row) > 34 else None

    if c is not None and str(c).strip():
        current_client = str(c).strip()
    if l is not None and str(l).strip():
        current_location = str(l).strip()

    if total_label == "Total":
        in_total_group = True
        current_key = (
            current_client.lower() if current_client else "",
            current_location.lower() if current_location else ""
        )
        if "Worker Accounts Created" in metric:
            if current_key not in ob_data:
                ob_data[current_key] = {"created": 0, "verified": 0, "rtb": 0}
            try:
                ob_data[current_key]["created"] = int(float(grand_total)) if grand_total else 0
            except (ValueError, TypeError):
                ob_data[current_key]["created"] = 0
    elif total_label is None and in_total_group and current_key and current_key in ob_data:
        if "1st Role Verified" in metric and "CR%" not in metric:
            try:
                ob_data[current_key]["verified"] = int(float(grand_total)) if grand_total else 0
            except (ValueError, TypeError):
                pass
        elif '"Ready to Book" Estimate' in metric and "CR%" not in metric:
            try:
                ob_data[current_key]["rtb"] = int(float(grand_total)) if grand_total else 0
            except (ValueError, TypeError):
                pass
    elif total_label is not None and total_label != "Total":
        in_total_group = False

print(f"OB Funnel entries: {len(ob_data)}")

# ============================================================
# BUILD LOOKUP STRUCTURES
# ============================================================

# Requisitions: (client_lower, city_lower) -> list
req_by_client_loc = defaultdict(list)
req_by_loc = defaultdict(list)

for r in reqs_data:
    client = r.get("client", "").strip().lower()
    location = r.get("location", "").strip()
    city = normalize_location(location)
    status = r.get("status", "").strip().lower()
    rsvps = 0
    try:
        rsvps = int(float(r.get("rsvps", "0")))
    except (ValueError, TypeError):
        pass
    job_title = r.get("job_title", "").strip().lower()

    entry = {
        "client": client,
        "city": city,
        "status": status,
        "rsvps": rsvps,
        "job_title": job_title,
    }
    req_by_client_loc[(client, city)].append(entry)
    req_by_loc[city].append(entry)

# Indeed campaigns: parsed entries
campaign_entries = []
for c in campaigns_data:
    job_url = c.get("Job URL", "")
    campaign_name = c.get("Campaigns", "")
    company = c.get("Company name", "").strip()
    city = c.get("City", "").strip()
    job_status = c.get("Job status", "").strip()
    spend = 0
    try:
        spend = float(c.get("Spend", "0"))
    except (ValueError, TypeError):
        pass

    employer = ""
    metro = ""
    role_url = ""
    if job_url:
        em = re.search(r'employer=([^&]+)', job_url)
        if em:
            employer = em.group(1).lower().replace("-", " ").replace("+", " ")
        mm = re.search(r'metro=([^&]+)', job_url)
        if mm:
            metro = mm.group(1).lower().replace("-", " ").replace("+", " ")
        rm = re.search(r'role=([^&]+)', job_url)
        if rm:
            role_url = rm.group(1).lower().replace("-", " ").replace("+", " ")

    campaign_entries.append({
        "company": company.lower(),
        "city": city.lower(),
        "employer": employer,
        "metro": metro,
        "role_url": role_url,
        "campaign_name": campaign_name.lower() if campaign_name else "",
        "spend": spend,
        "status": job_status.lower(),
        "job_name": c.get("Job", "").lower(),
    })


# ============================================================
# MATCHING FUNCTIONS
# ============================================================

def match_fhs(client_norm, city_norm, role):
    """Match FHS requisitions. Returns (open_count, rsvps_sum)"""
    role_lower = role.lower() if role else ""
    open_count = 0
    rsvps_sum = 0

    role_keywords = set(re.findall(r'\w+', role_lower))
    significant = role_keywords - {"and", "or", "the", "a", "an", "of", "in", "for"}

    def role_matches(job_title_lower):
        if not significant:
            return True
        jt_words = set(re.findall(r'\w+', job_title_lower))
        matches = significant & jt_words
        return len(matches) >= 1

    # Get city aliases
    city_aliases = [city_norm]
    for alias, canonical in METRO_ALIASES.items():
        if city_norm == canonical:
            city_aliases.append(alias)
        if city_norm == alias:
            city_aliases.append(canonical)

    matched = False
    for alias_client in get_client_aliases(client_norm):
        for ca in city_aliases:
            for r in req_by_client_loc.get((alias_client, ca), []):
                if role_matches(r["job_title"]):
                    matched = True
                    if r["status"] in ["open", "auto-paused", "auto_paused", "draft"]:
                        open_count += 1
                    rsvps_sum += r["rsvps"]

    if not matched:
        for ca in city_aliases:
            for r in req_by_loc.get(ca, []):
                if role_matches(r["job_title"]):
                    if r["status"] in ["open", "auto-paused", "auto_paused", "draft"]:
                        open_count += 1
                    rsvps_sum += r["rsvps"]

    return open_count, rsvps_sum


def match_indeed(client_norm, city_norm, role):
    """Match Indeed campaigns. Returns (active_count, spend_sum)"""
    role_lower = role.lower() if role else ""
    active_count = 0
    spend_sum = 0.0

    city_aliases = [city_norm]
    for alias, canonical in METRO_ALIASES.items():
        if city_norm == canonical:
            city_aliases.append(alias)
        if city_norm == alias:
            city_aliases.append(canonical)

    for c in campaign_entries:
        city_match = False
        for ca in city_aliases:
            if ca and (ca in c["city"] or ca in c["metro"] or ca in c["campaign_name"]):
                city_match = True
                break

        if not city_match:
            continue

        client_match = False
        for alias in get_client_aliases(client_norm):
            if alias and (alias in c["employer"] or alias in c["company"]
                          or alias in c["campaign_name"] or alias in c["job_name"]):
                client_match = True
                break

        role_match = False
        if role_lower:
            role_words = set(re.findall(r'\w+', role_lower)) - {
                "and", "or", "the", "a", "an", "of", "in", "for"
            }
            for rw in role_words:
                if len(rw) >= 4 and (rw in c["role_url"] or rw in c["job_name"]
                                     or rw in c["campaign_name"]):
                    role_match = True
                    break

        if client_match or role_match:
            if c["status"] in ["open", "active"]:
                active_count += 1
            spend_sum += c["spend"]

    return active_count, spend_sum


def match_ob_funnel(client_norm, city_norm):
    """Match OB Funnel data. Returns (created, verified, rtb)"""
    city_aliases = [city_norm]
    for alias, canonical in METRO_ALIASES.items():
        if city_norm == canonical:
            city_aliases.append(alias)
        if city_norm == alias:
            city_aliases.append(canonical)

    # Collect all matching entries, then pick the best one (highest created)
    candidates = []
    for alias_client in get_client_aliases(client_norm):
        for ca in city_aliases:
            for key, val in ob_data.items():
                ob_client, ob_loc = key
                if (alias_client and alias_client in ob_client
                        and ca and ca in ob_loc):
                    candidates.append(val)

    if candidates:
        # Return the entry with highest created (most relevant match)
        best = max(candidates, key=lambda x: x["created"])
        return best["created"], best["verified"], best["rtb"]

    return 0, 0, 0


# ============================================================
# PROCESS ALL REQUESTS
# ============================================================

processed = []
for req in requests_data:
    client_job = req.get("Client - Job", "").strip()
    status_raw = req.get("Request Status", "").strip()
    owner_email = req.get("Request Owner", "").strip()
    location = req.get("Location (City, State, Zip)", "").strip()
    shift_info = req.get("Shift information", "").strip()
    shift_start_raw = req.get("Shift start date", "").strip()
    hc = get_headcount(req.get("Headcount needed", ""))
    role = get_role(req)
    submission_raw = req.get("Submission date", "").strip()

    status_lower = status_raw.lower()
    if "decline" in status_lower:
        status_code = "D"
    elif "complete" in status_lower or "close" in status_lower:
        status_code = "C"
    else:
        status_code = "O"

    client_short = shorten_client(client_job)
    owner = get_owner_first(owner_email)
    city_norm = normalize_location(location)
    # Fallback: if location field yielded nothing useful, try client-job field
    if not city_norm or re.match(r'^\d+$', city_norm):
        city_from_cj = extract_location_from_client_job(client_job)
        if city_from_cj:
            city_norm = city_from_cj
    client_norm = normalize_client(client_job)
    state = extract_state(location)
    # Fallback state from client-job
    if state == "Unknown":
        state = extract_state(client_job)

    submission_dt = parse_submission_date(submission_raw)
    shift_start_dt = parse_shift_start(shift_start_raw)

    shifts_yes = bool(shift_info)
    is_inactive = status_code in ["D", "C"]

    if not is_inactive:
        fhs_open, fhs_interview = match_fhs(client_norm, city_norm, role)
        indeed_count, indeed_spend = match_indeed(client_norm, city_norm, role)
        ob_created, ob_verified, ob_rtb = match_ob_funnel(client_norm, city_norm)
    else:
        fhs_open = fhs_interview = 0
        indeed_count = 0
        indeed_spend = 0.0
        ob_created = ob_verified = ob_rtb = 0

    int_target = hc * 10 if hc else 0
    fill_target = hc * 2.5 if hc else 0

    if fill_target > 0 and not is_inactive:
        fill_pct = (ob_rtb / fill_target) * 100
    else:
        fill_pct = 0

    processed.append({
        "status_code": status_code,
        "status_raw": status_raw,
        "client_short": client_short,
        "client_norm": client_norm,
        "owner": owner,
        "role": role,
        "hc": hc,
        "shifts": shifts_yes,
        "location": location,
        "city_norm": city_norm,
        "state": state,
        "submission_dt": submission_dt,
        "submission_raw": submission_raw,
        "shift_start_dt": shift_start_dt,
        "fhs_open": fhs_open,
        "fhs_interview": fhs_interview,
        "int_target": int_target,
        "indeed_count": indeed_count,
        "indeed_spend": indeed_spend,
        "ob_created": ob_created,
        "ob_verified": ob_verified,
        "ob_rtb": ob_rtb,
        "fill_target": fill_target,
        "fill_pct": fill_pct,
        "is_inactive": is_inactive,
    })

# Sort by submission date ascending
processed.sort(key=lambda x: x["submission_dt"] or datetime(1900, 1, 1))

# ============================================================
# KPI CALCULATIONS
# ============================================================
live_requests = [p for p in processed if p["status_code"] == "O"]
total_live = len(live_requests)
total_hc = sum(p["hc"] for p in live_requests)
no_fhs = sum(1 for p in live_requests if p["fhs_open"] == 0)
no_indeed = sum(1 for p in live_requests if p["indeed_count"] == 0)
shifts_tbd = sum(1 for p in live_requests if not p["shifts"])

fill_pcts = [p["fill_pct"] for p in live_requests if p["hc"] > 0]
avg_fill = sum(fill_pcts) / len(fill_pcts) if fill_pcts else 0

print(f"\nKPIs: Live={total_live}, HC={total_hc}, No FHS={no_fhs}, "
      f"No Indeed={no_indeed}, Shifts TBD={shifts_tbd}, Avg Fill={avg_fill:.0f}%")
print(f"Total rows: {len(processed)}")


# Collect unique filter values
all_states = sorted(set(p["state"] for p in processed))
all_roles = sorted(set(p["role"] for p in processed if p["role"]))
all_owners = sorted(set(p["owner"] for p in processed if p["owner"]))

# ============================================================
# GENERATE HTML
# ============================================================

rows_html = []
for i, p in enumerate(processed):
    if p["is_inactive"]:
        bg = "#f9fafb" if p["status_code"] == "C" else "#f3f4f6"
    else:
        bg = "#ffffff"

    # Status badge
    if p["status_code"] == "O":
        st_bg = "#16a34a"
        st_label = "O"
    elif p["status_code"] == "D":
        st_bg = "#6b7280"
        st_label = "D"
    else:
        st_bg = "#111827"
        st_label = "C"

    # Client cell
    client_cell = f'<strong>{html_module.escape(p["client_short"])}</strong>'
    city_display = p["city_norm"].title() if p["city_norm"] else ""
    if city_display:
        client_cell += (
            f'<br><span style="color:#6b7280;font-size:12px;">'
            f'{html_module.escape(city_display)}</span>'
        )
    if p["status_code"] == "D":
        client_cell += (
            '<br><span style="background:#9ca3af;color:white;padding:2px 6px;'
            'border-radius:4px;font-size:11px;">DECLINED</span>'
        )
    elif p["status_code"] == "C":
        client_cell += (
            '<br><span style="background:#111827;color:white;padding:2px 6px;'
            'border-radius:4px;font-size:11px;">COMPLETE</span>'
        )

    # Shifts badge
    if p["shifts"]:
        shifts_html = (
            '<span style="background:#dcfce7;color:#166534;padding:2px 8px;'
            'border-radius:4px;font-size:12px;">Yes</span>'
        )
    else:
        shifts_html = (
            '<span style="background:#fef3c7;color:#92400e;padding:2px 8px;'
            'border-radius:4px;font-size:12px;">No</span>'
        )

    TD_NUM = 'style="text-align:center;font-weight:bold;font-size:15px;"'
    TD_MONEY = 'style="text-align:right;font-weight:bold;font-size:15px;"'

    if p["is_inactive"]:
        fhs_open_td = f'<td {TD_NUM}></td>'
        fhs_int_td = f'<td {TD_NUM}></td>'
        fhs_target_td = f'<td {TD_NUM}></td>'
        indeed_st_td = '<td style="text-align:center;"></td>'
        indeed_camps_td = f'<td {TD_NUM}></td>'
        indeed_spend_td = f'<td {TD_MONEY}></td>'
        ob_created_td = f'<td {TD_NUM}></td>'
        ob_verified_td = f'<td {TD_NUM}></td>'
        ob_rtb_td = f'<td {TD_NUM}></td>'
        fill_target_td = f'<td {TD_NUM}></td>'
        fill_pct_td = '<td style="min-width:120px;"></td>'
    else:
        fhs_open_td = f'<td {TD_NUM}>{fmt_number(p["fhs_open"])}</td>'
        fhs_int_td = f'<td {TD_NUM}>{fmt_number(p["fhs_interview"])}</td>'
        if p["hc"] == 0:
            fhs_target_td = f'<td {TD_NUM}>\u2014</td>'
        else:
            fhs_target_td = f'<td {TD_NUM}>{fmt_number(p["int_target"])}</td>'

        if p["indeed_count"] > 0:
            indeed_emoji = "\U0001f7e2"  # green circle
        else:
            indeed_emoji = "\u26ab"  # black circle
        indeed_st_td = f'<td style="text-align:center;">{indeed_emoji}</td>'
        indeed_camps_td = f'<td {TD_NUM}>{p["indeed_count"]}</td>'
        indeed_spend_td = (
            f'<td {TD_MONEY}>${fmt_number(int(round(p["indeed_spend"])))}</td>'
        )

        ob_created_td = f'<td {TD_NUM}>{fmt_number(p["ob_created"])}</td>'
        ob_verified_td = f'<td {TD_NUM}>{fmt_number(p["ob_verified"])}</td>'
        ob_rtb_td = f'<td {TD_NUM}>{fmt_number(p["ob_rtb"])}</td>'

        if p["hc"] == 0:
            fill_target_td = f'<td {TD_NUM}>\u2014</td>'
            fill_pct_td = (
                '<td style="min-width:120px;">'
                '<span style="color:#9ca3af;">\u2014</span></td>'
            )
        else:
            fill_target_td = f'<td {TD_NUM}>{p["fill_target"]:.1f}</td>'
            fill_pct_td = (
                f'<td style="min-width:120px;">'
                f'{progress_bar_html(p["fill_pct"])}</td>'
            )

    obs_key = (
        f'{p["client_short"]}|'
        f'{p["city_norm"].title() if p["city_norm"] else ""}|'
        f'{p["role"]}'
    )

    row_html = f'''<tr style="background:{bg};" data-state="{html_module.escape(p["state"])}" data-role="{html_module.escape(p["role"])}" data-owner="{html_module.escape(p["owner"])}">
        <td style="text-align:center;font-weight:bold;font-size:14px;color:#fff;background:{st_bg};">{st_label}</td>
        <td style="text-align:center;font-size:13px;">{format_date_display(p["submission_dt"])}</td>
        <td style="text-align:center;font-size:13px;">{format_date_display(p["shift_start_dt"])}</td>
        <td>{client_cell}</td>
        <td>{html_module.escape(p["owner"])}</td>
        <td>{html_module.escape(p["role"])}</td>
        <td style="text-align:center;font-weight:bold;font-size:15px;">{p["hc"]}</td>
        <td style="text-align:center;">{shifts_html}</td>
        {fhs_open_td}
        {fhs_int_td}
        {fhs_target_td}
        {indeed_st_td}
        {indeed_camps_td}
        {indeed_spend_td}
        {ob_created_td}
        {ob_verified_td}
        {ob_rtb_td}
        {fill_target_td}
        {fill_pct_td}
        <td class="obs-cell" contenteditable="true" data-key="{html_module.escape(obs_key)}" style="min-width:180px;font-size:12px;color:#374151;border-left:2px solid #d1d5db;"></td>
    </tr>'''
    rows_html.append(row_html)

state_options = "\n".join(
    f'<option value="{s}">{s}</option>' for s in all_states
)
role_options = "\n".join(
    f'<option value="{html_module.escape(r)}">{html_module.escape(r)}</option>'
    for r in all_roles
)
owner_options = "\n".join(
    f'<option value="{o}">{o}</option>' for o in all_owners
)

html_output = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recruitment Request Dashboard — {REPORT_DATE}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f3f4f6; font-size: 14px; color: #111827; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%); color: white; padding: 24px 32px; }}
        .header h1 {{ font-size: 22px; font-weight: 700; }}
        .header p {{ font-size: 13px; opacity: 0.85; margin-top: 4px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; padding: 20px 32px; }}
        .kpi-card {{ background: white; border-radius: 12px; padding: 16px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }}
        .kpi-card .number {{ font-size: 32px; font-weight: 800; line-height: 1.2; }}
        .kpi-card .label {{ font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; }}
        .kpi-card.red .number {{ color: #ef4444; }}
        .kpi-card.amber .number {{ color: #f59e0b; }}
        .kpi-card.blue .number {{ color: #2563eb; }}
        .kpi-card.green .number {{ color: #22c55e; }}
        .table-container {{ margin: 0 32px 32px; background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }}
        .table-scroll {{ overflow-y: auto; max-height: calc(100vh - 60px); }}
        thead tr:first-child th {{ position: sticky; top: 0; z-index: 20; }}
        thead tr:nth-child(2) th {{ position: sticky; top: 34px; z-index: 19; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
        th {{ position: sticky; top: 0; z-index: 10; background: #1e3a5f; color: white; padding: 8px 10px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; white-space: nowrap; }}
        th[data-tip] {{ cursor: help; }}
        #tooltip {{
            position: fixed;
            background: #111827;
            color: #fff;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 400;
            line-height: 1.5;
            max-width: 320px;
            z-index: 9999;
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            pointer-events: none;
            display: none;
        }}
        th.group-header {{ background: #0f2540; padding: 6px 10px; font-size: 11px; text-align: center; border-left: 2px solid rgba(255,255,255,0.15); }}
        th.sub-header {{ background: #1e3a5f; font-size: 11px; }}
        th:first-child {{ border-left: none; }}
        td {{ padding: 8px 10px; border-bottom: 1px solid #e5e7eb; font-size: 14px; vertical-align: middle; }}
        tr:hover {{ filter: brightness(0.97); }}
        .legend {{ margin: 12px 32px; display: flex; gap: 24px; font-size: 12px; color: #6b7280; }}
        .legend span {{ display: inline-flex; align-items: center; gap: 6px; }}
        .legend .dot {{ width: 12px; height: 12px; border-radius: 3px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Recruitment Request Dashboard</h1>
        <p>Generated {REPORT_DATE} | Every Live revenue request = one row (no merging) | Data: FHS Requisitions, Indeed Campaign Report, OB Funnel</p>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="number">{total_live}</div>
            <div class="label">Live Requests</div>
        </div>
        <div class="kpi-card blue">
            <div class="number">{fmt_number(total_hc)}</div>
            <div class="label">Total HC</div>
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
        <span><span class="dot" style="background:#f3f4f6;border:1px solid #d1d5db;"></span> Declined / Complete</span>
        <span>Ordered by revenue team submission date</span>
    </div>

    <div style="margin: 12px 32px; display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
        <label style="font-size:13px; font-weight:600; color:#374151;">State:</label>
        <select id="stateFilter" onchange="applyFilters()" style="padding:6px 12px; border-radius:6px; border:1px solid #d1d5db; font-size:13px; background:white; cursor:pointer;">
            <option value="all">All States</option>
            {state_options}
        </select>
        <label style="font-size:13px; font-weight:600; color:#374151; margin-left:8px;">Role:</label>
        <select id="roleFilter" onchange="applyFilters()" style="padding:6px 12px; border-radius:6px; border:1px solid #d1d5db; font-size:13px; background:white; cursor:pointer;">
            <option value="all">All Roles</option>
            {role_options}
        </select>
        <label style="font-size:13px; font-weight:600; color:#374151; margin-left:8px;">Owner:</label>
        <select id="ownerFilter" onchange="applyFilters()" style="padding:6px 12px; border-radius:6px; border:1px solid #d1d5db; font-size:13px; background:white; cursor:pointer;">
            <option value="all">All Owners</option>
            {owner_options}
        </select>
        <span id="rowCount" style="font-size:12px; color:#6b7280;"></span>
    </div>

    <div class="table-container">
        <div class="table-scroll">
            <table id="mainTable">
                <thead>
                    <tr>
                        <th rowspan="2" style="min-width:30px;" data-tip="O = Open (Live request), D = Declined, C = Closed (Completed)">St</th>
                        <th rowspan="2" style="min-width:90px;" data-tip="Date the revenue team submitted this request">Submitted</th>
                        <th rowspan="2" style="min-width:90px;" data-tip="Date when shifts start for this request">Shift Start</th>
                        <th rowspan="2" style="min-width:160px;" data-tip="Client name and location from the revenue request">Client</th>
                        <th rowspan="2" style="min-width:70px;" data-tip="Market owner responsible for this location">Owner</th>
                        <th rowspan="2" style="min-width:120px;" data-tip="Job role requested by the revenue team">Role</th>
                        <th rowspan="2" style="min-width:40px;" data-tip="Headcount — number of workers the revenue team needs to fill">HC</th>
                        <th rowspan="2" style="min-width:55px;" data-tip="Whether shift schedules have been posted for this request">Shifts</th>
                        <th colspan="3" class="group-header" data-tip="Data from FHS (Flex Hiring System) requisitions">FHS Requisitions</th>
                        <th colspan="3" class="group-header" data-tip="Data from Indeed sponsored job campaigns">Indeed Ads</th>
                        <th colspan="3" class="group-header" data-tip="Data from the OB (Onboarding) Funnel — worker pipeline progress">OB Funnel</th>
                        <th colspan="2" class="group-header" data-tip="Fulfillment progress: RTB vs pipeline target">Fulfillment</th>
                        <th rowspan="2" style="min-width:180px;" data-tip="Manual observations — saved in your browser (localStorage)">Notes</th>
                    </tr>
                    <tr>
                        <th class="sub-header" style="text-align:center;" data-tip="Count of FHS requisitions with status Open or Auto-Paused for this client+location+role">Open</th>
                        <th class="sub-header" style="text-align:center;" data-tip="Sum of RSVPs (interview candidates) from FHS reqs created after the revenue request submission date">Interview</th>
                        <th class="sub-header" style="text-align:center;" data-tip="Target interviews needed = HC x 10 (10 interviews per hire)">Target</th>
                        <th class="sub-header" style="text-align:center;" data-tip="Indeed campaign status: Active (campaigns running) or None (no campaigns)">St</th>
                        <th class="sub-header" style="text-align:center;" data-tip="Number of active Indeed campaigns matching this client+location+role">Camps</th>
                        <th class="sub-header" style="text-align:right;" data-tip="Total Indeed sponsored job spend for matching campaigns (client+location+role)">Spend</th>
                        <th class="sub-header" style="text-align:center;" data-tip="Worker Accounts Created — new workers who signed up via the OB funnel">Created</th>
                        <th class="sub-header" style="text-align:center;" data-tip="1st Role Verified — workers who completed role verification in the OB funnel">Verified</th>
                        <th class="sub-header" style="text-align:center;" data-tip="Ready to Book — workers who completed onboarding and are available for shifts">RTB</th>
                        <th class="sub-header" style="text-align:center;" data-tip="RTB Target = HC x 2.5 — pipeline target of Ready to Book workers needed">Target</th>
                        <th class="sub-header" style="text-align:center;" data-tip="Fill% = RTB / (HC x 2.5) — workers ready to book vs. pipeline target">Fill%</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(rows_html)}
                </tbody>
            </table>
        </div>
    </div>
    <div id="tooltip"></div>
    <script>
    // Tooltip logic
    const tip = document.getElementById('tooltip');
    document.querySelectorAll('th[data-tip]').forEach(th => {{
        th.addEventListener('mouseenter', e => {{
            tip.textContent = th.getAttribute('data-tip');
            tip.style.display = 'block';
            const rect = th.getBoundingClientRect();
            let left = rect.left + rect.width / 2 - tip.offsetWidth / 2;
            let top = rect.bottom + 8;
            if (left + tip.offsetWidth > window.innerWidth - 16) left = window.innerWidth - tip.offsetWidth - 16;
            if (left < 16) left = 16;
            if (top + tip.offsetHeight > window.innerHeight - 16) top = rect.top - tip.offsetHeight - 8;
            tip.style.left = left + 'px';
            tip.style.top = top + 'px';
        }});
        th.addEventListener('mouseleave', () => {{ tip.style.display = 'none'; }});
    }});

    function applyFilters() {{
        const stateVal = document.getElementById('stateFilter').value;
        const roleVal = document.getElementById('roleFilter').value;
        const ownerVal = document.getElementById('ownerFilter').value;
        const rows = document.querySelectorAll('#mainTable tbody tr');
        let visible = 0;
        const anyFilter = stateVal !== 'all' || roleVal !== 'all' || ownerVal !== 'all';
        rows.forEach(row => {{
            const matchState = stateVal === 'all' || row.dataset.state === stateVal;
            const matchRole = roleVal === 'all' || row.dataset.role === roleVal;
            const matchOwner = ownerVal === 'all' || row.dataset.owner === ownerVal;
            if (matchState && matchRole && matchOwner) {{
                row.style.display = '';
                visible++;
            }} else {{
                row.style.display = 'none';
            }}
        }});
        document.getElementById('rowCount').textContent = anyFilter ? visible + ' of ' + rows.length + ' rows' : '';
    }}
    // --- Notes localStorage ---
    const NOTES_KEY = 'rrd_notes';
    function loadNotes() {{
        try {{ return JSON.parse(localStorage.getItem(NOTES_KEY) || '{{}}'); }} catch {{ return {{}}; }}
    }}
    function saveNotes(notes) {{
        localStorage.setItem(NOTES_KEY, JSON.stringify(notes));
    }}
    const notes = loadNotes();
    document.querySelectorAll('.obs-cell').forEach(cell => {{
        const key = cell.dataset.key;
        if (notes[key]) cell.textContent = notes[key];
        cell.addEventListener('blur', () => {{
            const n = loadNotes();
            if (cell.textContent.trim()) n[key] = cell.textContent.trim();
            else delete n[key];
            saveNotes(n);
        }});
    }});
    </script>
</body>
</html>'''

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"\nReport written to: {OUTPUT_PATH}")
print(f"Total rows: {len(processed)}")
print(f"Live: {total_live}, Declined: {sum(1 for p in processed if p['status_code']=='D')}, "
      f"Complete: {sum(1 for p in processed if p['status_code']=='C')}")
