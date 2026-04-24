#!/usr/bin/env python3
"""
Audit all ENABLED campaigns for:
  1. Geo targeting (LOCATION or PROXIMITY — must have ≥1)
  2. Ad schedule (Mon–Sun 06:00–23:00 — 7 entries required; App campaigns exempt)
  3. Extensions: sitelinks ≥6, callouts ≥4, snippets ≥3 (Search only)

Run: python3 scripts/google-ads-audit-active-campaigns.py
"""

from collections import defaultdict
from google.ads.googleads.client import GoogleAdsClient

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"


def run(client, query):
    ga = client.get_service("GoogleAdsService")
    return list(ga.search(customer_id=CUSTOMER_ID, query=query))


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    # ── 1. All ENABLED campaigns ──────────────────────────────────────
    rows = run(client, """
        SELECT campaign.id, campaign.name,
               campaign.advertising_channel_type,
               campaign.advertising_channel_sub_type
        FROM campaign
        WHERE campaign.status = 'ENABLED'
        ORDER BY campaign.name
    """)

    campaigns = {}
    for r in rows:
        cid = str(r.campaign.id)
        campaigns[cid] = {
            "name":     r.campaign.name,
            "type":     r.campaign.advertising_channel_type.name,
            "sub_type": r.campaign.advertising_channel_sub_type.name,
        }

    print(f"\nTotal ENABLED campaigns: {len(campaigns)}\n")

    # ── 2. Geo targets ────────────────────────────────────────────────
    geo_rows = run(client, """
        SELECT campaign.id, campaign_criterion.type, campaign_criterion.negative
        FROM campaign_criterion
        WHERE campaign_criterion.type IN ('LOCATION', 'PROXIMITY')
          AND campaign_criterion.negative = FALSE
          AND campaign.status = 'ENABLED'
    """)
    geo_count = defaultdict(int)
    for r in geo_rows:
        geo_count[str(r.campaign.id)] += 1

    # ── 3. Ad schedules ───────────────────────────────────────────────
    sched_rows = run(client, """
        SELECT campaign.id, campaign_criterion.ad_schedule.day_of_week,
               campaign_criterion.ad_schedule.start_hour,
               campaign_criterion.ad_schedule.end_hour
        FROM campaign_criterion
        WHERE campaign_criterion.type = 'AD_SCHEDULE'
          AND campaign.status = 'ENABLED'
    """)
    sched_count  = defaultdict(int)
    sched_detail = defaultdict(list)
    for r in sched_rows:
        cid = str(r.campaign.id)
        sched_count[cid] += 1
        sh = r.campaign_criterion.ad_schedule.start_hour
        eh = r.campaign_criterion.ad_schedule.end_hour
        sched_detail[cid].append((sh, eh))

    # ── 4. Campaign assets (extensions) ──────────────────────────────
    asset_rows = run(client, """
        SELECT campaign.id, campaign.status, campaign_asset.field_type
        FROM campaign_asset
        WHERE campaign.status = 'ENABLED'
    """)
    assets = defaultdict(lambda: defaultdict(int))
    for r in asset_rows:
        cid = str(r.campaign.id)
        ft  = r.campaign_asset.field_type.name
        assets[cid][ft] += 1

    # ── 5. Evaluate & report ──────────────────────────────────────────
    issues = {}  # cid → list of issue strings

    for cid, info in campaigns.items():
        camp_issues = []
        ctype    = info["type"]
        sub_type = info["sub_type"]
        is_app    = sub_type == "APP_CAMPAIGN"
        is_search = ctype == "SEARCH"

        # Geo check (all campaigns)
        if geo_count[cid] == 0:
            camp_issues.append("❌ NO GEO TARGET")

        # Ad schedule check (not App campaigns)
        if not is_app:
            n_sched = sched_count[cid]
            if n_sched == 0:
                camp_issues.append("❌ NO AD SCHEDULE")
            elif n_sched < 7:
                camp_issues.append(f"⚠️  PARTIAL AD SCHEDULE ({n_sched}/7 days)")
            else:
                # Check hours are correct (06–23)
                bad = [(sh, eh) for sh, eh in sched_detail[cid] if sh != 6 or eh != 23]
                if bad:
                    camp_issues.append(f"⚠️  WRONG SCHEDULE HOURS: {bad[0]} (expected 6–23)")

        # Extensions check (Search only)
        if is_search:
            sl = assets[cid].get("SITELINK", 0)
            cl = assets[cid].get("CALLOUT", 0)
            sn = assets[cid].get("STRUCTURED_SNIPPET", 0)
            if sl < 6:
                camp_issues.append(f"❌ SITELINKS {sl}/6")
            if cl < 4:
                camp_issues.append(f"❌ CALLOUTS {cl}/4")
            if sn < 3:
                camp_issues.append(f"❌ SNIPPETS {sn}/3")

        if camp_issues:
            issues[cid] = camp_issues

    # ── Print results ─────────────────────────────────────────────────
    if not issues:
        print("✅ All ENABLED campaigns pass the audit.\n")
        return

    print(f"{'='*70}")
    print(f"  CAMPAIGNS WITH ISSUES  ({len(issues)} of {len(campaigns)})")
    print(f"{'='*70}\n")

    for cid, camp_issues in sorted(issues.items(), key=lambda x: campaigns[x[0]]["name"]):
        info = campaigns[cid]
        flag_strs = "  |  ".join(camp_issues)
        print(f"[{info['type'][:6]}] {info['name']}")
        print(f"         ID: {cid}  →  {flag_strs}\n")

    # Summary counts
    print(f"{'='*70}")
    print(f"  SUMMARY")
    print(f"{'='*70}")
    no_geo_list   = [c for c, i in issues.items() if any("GEO" in x for x in i)]
    no_sched_list = [c for c, i in issues.items() if any("SCHEDULE" in x for x in i)]
    no_sl_list    = [c for c, i in issues.items() if any("SITELINK" in x for x in i)]
    no_cl_list    = [c for c, i in issues.items() if any("CALLOUT" in x for x in i)]
    no_sn_list    = [c for c, i in issues.items() if any("SNIPPET" in x for x in i)]

    print(f"  Missing geo target   : {len(no_geo_list)} campaigns")
    print(f"  Missing ad schedule  : {len(no_sched_list)} campaigns")
    print(f"  Missing sitelinks    : {len(no_sl_list)} campaigns")
    print(f"  Missing callouts     : {len(no_cl_list)} campaigns")
    print(f"  Missing snippets     : {len(no_sn_list)} campaigns")
    print()


if __name__ == "__main__":
    main()
