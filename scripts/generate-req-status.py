#!/usr/bin/env python3
"""Report 3: Requisition Status Table — grouped by State > Metro > Client > Role."""
import csv, glob, os, re
from collections import defaultdict
from datetime import datetime, timedelta

TODAY    = datetime.today()
DATE_STR = TODAY.strftime("%Y-%m-%d")
ACTIVE   = {"open", "auto-paused", "auto_paused", "draft"}
SKIP_CLIENTS = {"indeed flex upskilling"}  # exclude upskilling; keep IFA for RSVPs

def latest(pat):
    files = sorted(glob.glob(os.path.expanduser(pat)), key=os.path.getmtime, reverse=True)
    return files[0] if files else None

def prev_week_file(pat):
    files = sorted(glob.glob(os.path.expanduser(pat)), key=os.path.getmtime, reverse=True)
    target = TODAY - timedelta(days=7)
    best, best_delta = None, None
    for f in files:
        mt = datetime.fromtimestamp(os.path.getmtime(f))
        d  = abs((mt - target).total_seconds())
        if best_delta is None or d < best_delta:
            best, best_delta = f, d
    return best

def _state(loc):
    m = re.search(r',\s*([A-Z]{2})', loc)
    return m.group(1) if m else ""

def _metro(loc):
    return re.sub(r',\s*[A-Z]{2}\s*\d{0,5}\s*$', '', loc.strip()).strip().rstrip(',').strip()

def load_reqs(path, active_only=True):
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r.get("client","").strip().lower() in SKIP_CLIENTS:
                continue
            status = r.get("status","").lower().strip()
            if active_only and status not in ACTIVE:
                continue
            rows.append({
                "state":  _state(r.get("location","")),
                "metro":  _metro(r.get("location","")),
                "client": r.get("client","").strip(),
                "role":   r.get("job_title","").strip(),
                "rsvps":  int(float(r.get("rsvps") or 0)),
                "target": int(float(r.get("target_rsvps") or 0)),
                "status": status,
            })
    return rows

REQS_FILE = latest("~/Downloads/requisitions-*.csv")
REQS_PREV = prev_week_file("~/Downloads/requisitions-*.csv")

# ── Current groups ────────────────────────────────────────────
groups = defaultdict(lambda: {"rsvps":0,"open":0,"auto_paused":0,"draft":0,"target":0})
for r in load_reqs(REQS_FILE):
    k = (r["state"], r["metro"], r["client"], r["role"])
    groups[k]["rsvps"]  += r["rsvps"]
    groups[k]["target"]  = max(groups[k]["target"], r["target"])
    st = r["status"].replace("-","_")
    col = st if st in ("open","auto_paused","draft") else "open"
    groups[k][col] += 1

# ── Last-week RSVPs ───────────────────────────────────────────
prev_map = defaultdict(int)
if REQS_PREV and REQS_PREV != REQS_FILE:
    for r in load_reqs(REQS_PREV, active_only=False):
        prev_map[(r["state"], r["metro"], r["client"], r["role"])] += r["rsvps"]

sorted_groups = sorted(groups.items(), key=lambda x: x[1]["rsvps"])

# ── HTML helpers ──────────────────────────────────────────────
def rsvp_bg(v):
    if v < 50:  return "background:#fff0f0"
    if v < 100: return "background:#fff8e6"
    return ""

def fill_style(pct, has_target):
    if not has_target: return ""
    if pct < 30:  return "color:#dc2626;font-weight:600"
    if pct < 70:  return "color:#d97706;font-weight:600"
    return "color:#16a34a;font-weight:600"

rows_html = []
for (state, metro, client, role), v in sorted_groups:
    rsvps   = v["rsvps"]
    target  = v["target"]
    lw      = prev_map.get((state, metro, client, role))
    lw_str  = str(lw) if lw is not None else "&mdash;"
    pct     = round(rsvps / target * 100) if target else 0
    fill    = f"{pct}%" if target else "&mdash;"
    total   = v["open"] + v["auto_paused"] + v["draft"]
    bg      = rsvp_bg(rsvps)
    fc      = fill_style(pct, bool(target))
    d_bg    = "background:#fffde7" if v["draft"]      > 0 else ""
    p_bg    = "background:#fffde7" if v["auto_paused"] > 0 else ""
    tr_sty  = f' style="{bg}"' if bg else ""
    td_r    = f'<b style="color:#dc2626">{rsvps}</b>' if rsvps < 50 else str(rsvps)
    rows_html.append(
        f'    <tr{tr_sty}>'
        f'<td>{state}</td><td>{metro}</td>'
        f'<td style="white-space:nowrap">{client}</td><td>{role}</td>'
        f'<td style="text-align:center{";"+bg if bg else ""}">{td_r}</td>'
        f'<td style="text-align:center">{lw_str}</td>'
        f'<td style="text-align:center">{target or "&mdash;"}</td>'
        f'<td style="text-align:center;{fc}">{fill}</td>'
        f'<td style="text-align:center">{v["open"]}</td>'
        f'<td style="text-align:center;{p_bg}">{v["auto_paused"]}</td>'
        f'<td style="text-align:center;{d_bg}">{v["draft"]}</td>'
        f'<td style="text-align:center">{total}</td>'
        f'</tr>'
    )

prev_label = (datetime.fromtimestamp(os.path.getmtime(REQS_PREV)).strftime("%b %d")
              if REQS_PREV and REQS_PREV != REQS_FILE else "N/A")

# ── Collect unique values for filter dropdowns ────────────────
all_states   = sorted(set(k[0] for k in groups if k[0]))
all_metros   = sorted(set(k[1] for k in groups if k[1]))
all_clients  = sorted(set(k[2] for k in groups if k[2]))
all_roles    = sorted(set(k[3] for k in groups if k[3]))

def opts(values):
    return "".join(f'<option value="{v}">{v}</option>' for v in values)

body_rows = "\n".join(rows_html)
html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Requisition Status {DATE_STR}</title>
<style>
body{{font-family:system-ui,sans-serif;font-size:14px;margin:0;padding:16px;background:#f9fafb}}
h1{{font-size:20px;font-weight:700;margin-bottom:4px}}
.sub{{color:#6b7280;font-size:13px;margin-bottom:12px}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;align-items:center}}
.filters label{{font-size:12px;font-weight:600;color:#374151}}
.filters select{{font-size:13px;padding:4px 8px;border:1px solid #d1d5db;border-radius:6px;
                 background:#fff;cursor:pointer;min-width:140px}}
.filters button{{font-size:12px;padding:4px 10px;border:1px solid #d1d5db;border-radius:6px;
                 background:#f3f4f6;cursor:pointer;color:#374151}}
.filters button:hover{{background:#e5e7eb}}
.wrap{{max-height:calc(100vh - 140px);overflow-y:auto;overflow-x:auto;
       border:1px solid #e5e7eb;border-radius:8px}}
table{{border-collapse:collapse;width:100%;font-size:14px}}
th{{background:#f3f4f6;padding:8px 10px;text-align:left;font-size:12px;font-weight:600;
    color:#374151;position:sticky;top:0;border-bottom:2px solid #d1d5db;white-space:nowrap}}
td{{padding:7px 10px;border-bottom:1px solid #f3f4f6;vertical-align:middle}}
tr:hover td{{background:#f5f5f5}}
tr.hidden{{display:none}}
#count{{font-size:12px;color:#6b7280;margin-left:4px}}
</style></head><body>
<h1>Requisition Status &mdash; {TODAY.strftime('%B %d, %Y')}</h1>
<div class="sub">{len(sorted_groups)} active groups &middot; Last Week = {prev_label} file &middot; Sorted by RSVPs &uarr;</div>
<div class="filters">
  <label>State</label>
  <select id="f-state" onchange="applyFilters()">
    <option value="">All</option>{opts(all_states)}
  </select>
  <label>Metro</label>
  <select id="f-metro" onchange="applyFilters()">
    <option value="">All</option>{opts(all_metros)}
  </select>
  <label>Client</label>
  <select id="f-client" onchange="applyFilters()">
    <option value="">All</option>{opts(all_clients)}
  </select>
  <label>Role</label>
  <select id="f-role" onchange="applyFilters()">
    <option value="">All</option>{opts(all_roles)}
  </select>
  <button onclick="clearFilters()">Clear</button>
  <span id="count"></span>
</div>
<div class="wrap"><table id="tbl">
  <thead><tr>
    <th>State</th><th>Metro</th><th>Client</th><th>Role</th>
    <th style="text-align:center">RSVPs</th>
    <th style="text-align:center">Last Week RSVPs</th>
    <th style="text-align:center">Target</th>
    <th style="text-align:center">Fill%</th>
    <th style="text-align:center">Open</th>
    <th style="text-align:center">Auto-Paused</th>
    <th style="text-align:center">Draft</th>
    <th style="text-align:center">Total</th>
  </tr></thead>
  <tbody id="tbody">
{body_rows}
  </tbody>
</table></div>
<script>
function applyFilters() {{
  const fs = document.getElementById('f-state').value;
  const fm = document.getElementById('f-metro').value;
  const fc = document.getElementById('f-client').value;
  const fr = document.getElementById('f-role').value;
  let visible = 0;
  document.querySelectorAll('#tbody tr').forEach(tr => {{
    const cells = tr.querySelectorAll('td');
    const match =
      (!fs || cells[0].textContent === fs) &&
      (!fm || cells[1].textContent === fm) &&
      (!fc || cells[2].textContent.trim() === fc) &&
      (!fr || cells[3].textContent === fr);
    tr.classList.toggle('hidden', !match);
    if (match) visible++;
  }});
  document.getElementById('count').textContent = `${{visible}} row${{visible !== 1 ? 's' : ''}}`;
}}
function clearFilters() {{
  ['f-state','f-metro','f-client','f-role'].forEach(id => document.getElementById(id).value = '');
  applyFilters();
}}
applyFilters();
</script>
</body></html>"""

out = f"docs/reports/req-status-{DATE_STR}.html"
with open(out, "w") as f:
    f.write(html)

# Verify problem locations
print(f"Saved: {out}  ({len(sorted_groups)} rows)")
for (state, metro, client, role), v in sorted_groups:
    if any(x in metro.lower() for x in ("monroe","logan")):
        print(f"  CHECK: {state}|{metro}|{client}|{role} -> rsvps={v['rsvps']} target={v['target']}")
