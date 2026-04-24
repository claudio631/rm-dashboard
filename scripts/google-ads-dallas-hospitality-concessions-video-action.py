#!/usr/bin/env python3
"""
Dallas Hospitality Concessions — Demand Gen Video Campaign
Replaces the awareness-only FIFA YouTube campaign (23743450442) with a
conversion-optimised Demand Gen campaign using the same video asset.

VIDEO_ACTION sub-type is deprecated in the Google Ads API; Demand Gen is
the current equivalent for conversion-focused video campaigns.

New campaign: p-b2c-google-demand-gen-us-bofu-bau-dallas-hospitality-concessions--eg--
Objective:    Conversions (Maximize Conversions, tCPA $10)
Bidding:      maximize_conversions (target_cpa_micros = 10_000_000)
Geo:          Dallas-Fort Worth DMA (geoTargetConstants/200623)
Budget:       $50/day (same as existing for A/B comparison)

Existing campaign 23743450442 is NOT paused — running in parallel for comparison.
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

CAMPAIGN_NAME = "p-b2c-google-demand-gen-us-bofu-bau-dallas-hospitality-concessions--eg--"
DAILY_BUDGET  = 50_000_000   # $50/day
TARGET_CPA    = 10_000_000   # $10 target CPA

GEO_TARGET_RN = "geoTargetConstants/200623"  # Dallas-Fort Worth DMA

# Same video asset as existing campaign
VIDEO_ASSET_RN = "customers/7236100723/assets/348593134157"

# Square logo (1:1, min 128×128)
LOGO_ASSET_RN = "customers/7236100723/assets/56893637546"

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/concession-stand-worker/"
    "?utm_source=youtube&utm_medium=cpc"
    "&link_value=syft://jobs/browse/499915"
    "&employer=legends-hospitality"
    "&metro=dallas"
    "&role=concession-stand-worker"
    "&utm_campaign=us-evergreen-concessions-dallas-tx"
)

# In-market audience IDs
IN_MARKET_IDS = [
    80412,   # Employment
    80423,   # Temporary & Seasonal Jobs
    81002,   # Leisure & Hospitality Jobs
]

# DemandGenVideoResponsiveAd copy
HEADLINES = [
    "Concession Stand Jobs Dallas",
    "Stadium Work - Apply Now",
    "Hospitality Jobs Dallas TX",
    "Get Paid Same Day",
    "No Experience Needed",
]
LONG_HEADLINES = [
    "Support major sporting events across Dallas, TX. Flexible Shifts and Same Day Pay.",
    "Concession stand and event staff jobs in Dallas, TX. Get paid the same day you work.",
    "Hiring now for stadium and arena events in Dallas. Flexible shifts, instant pay.",
]
DESCRIPTIONS = [
    "Flexible Scheduling - Pick shifts that fit your availability. Apply Now.",
    "Concession stand worker roles in Dallas. Same Day Pay, flexible shifts. Apply free.",
    "Stadium and event staff jobs near Dallas, TX. No experience needed. Start this week.",
]
BUSINESS_NAME = "Indeed Flex"
BREADCRUMB1   = "Jobs"
BREADCRUMB2   = "Dallas"


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n" + "═" * 65)
    print("  Dallas Hospitality Concessions — Demand Gen Video Campaign")
    print("  Parallel to existing 23743450442 (NOT paused)")
    print("═" * 65 + "\n")

    # ── Budget + Campaign (already created) ──────────────────────────────────
    camp_rn = "customers/7236100723/campaigns/23757742736"
    camp_id = "23757742736"
    print(f"▶  Reusing campaign: {camp_rn}")

    # ── Geo + Ad group (already created) ─────────────────────────────────────
    ag_rn = "customers/7236100723/adGroups/201144264651"
    print(f"▶  Reusing ad group: {ag_rn}")
    print("     ⚠️  Add geo (Dallas-Fort Worth DMA) in UI — API geo blocked for DEMAND_GEN")
    print("     ⚠️  Add audiences in UI: Employment | Temp & Seasonal Jobs | Leisure & Hospitality Jobs")

    # ── DemandGenVideoResponsiveAd ────────────────────────────────────────────
    print("\n▶  Creating DemandGenVideoResponsiveAd...")
    ada_svc = client.get_service("AdGroupAdService")
    ada_op  = client.get_type("AdGroupAdOperation")
    ada = ada_op.create
    ada.ad_group = ag_rn
    ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED

    ad  = ada.ad
    ad.name = "Demand Gen Video — Concession Stand Dallas TX"
    ad.final_urls.append(FINAL_URL)

    dg = ad.demand_gen_video_responsive_ad

    # Business name (required)
    dg.business_name.text = BUSINESS_NAME

    # Breadcrumbs (display URL)
    dg.breadcrumb1 = BREADCRUMB1
    dg.breadcrumb2 = BREADCRUMB2

    # Video asset
    v = client.get_type("AdVideoAsset")
    v.asset = VIDEO_ASSET_RN
    dg.videos.append(v)

    # Logo image (required)
    logo = client.get_type("AdImageAsset")
    logo.asset = LOGO_ASSET_RN
    dg.logo_images.append(logo)

    # Headlines
    for hl in HEADLINES:
        h = client.get_type("AdTextAsset")
        h.text = hl
        dg.headlines.append(h)

    # Long headlines
    for lh in LONG_HEADLINES:
        h = client.get_type("AdTextAsset")
        h.text = lh
        dg.long_headlines.append(h)

    # Descriptions
    for desc in DESCRIPTIONS:
        d = client.get_type("AdTextAsset")
        d.text = desc
        dg.descriptions.append(d)

    ada_result = ada_svc.mutate_ad_group_ads(
        customer_id=CUSTOMER_ID, operations=[ada_op]
    )
    print(f"  ✅ DemandGenVideoResponsiveAd: {ada_result.results[0].resource_name}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "═" * 65)
    print("  ✅ DEMAND GEN VIDEO CAMPAIGN LIVE")
    print("═" * 65)
    print(f"  New:      {camp_id} — maximize_conversions, tCPA $10")
    print(f"  Existing: 23743450442 — TARGET_CPV (running for comparison)")
    print(f"  Budget:   $50/day each")
    print(f"  Audiences: 3 in-market layers (no keywords — Demand Gen audience-based)")
    print(f"  Ad:       DemandGenVideoResponsiveAd — {len(HEADLINES)} HL, {len(LONG_HEADLINES)} LH, {len(DESCRIPTIONS)} Desc")
    print("═" * 65 + "\n")


if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"\n❌ Google Ads API error:")
        for error in ex.failure.errors:
            print(f"  [{error.error_code}] {error.message}")
            if error.location:
                for fv in error.location.field_path_elements:
                    print(f"    Field: {fv.field_name} (index {fv.index})")
        raise SystemExit(1)
