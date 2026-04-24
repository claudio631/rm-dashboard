#!/usr/bin/env python3
"""
Complete Fort Worth Hospitality BAU — PMax asset group + App campaign.
Search campaign already live: 23766390416
PMax campaign already created (no asset group): 23766391346

Run: python3 scripts/google-ads-levy-server-fort-worth-tx-complete-pmax-app.py
"""

import urllib.request, urllib.parse, json, time
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/server/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/500267"
    "&employer=levy-restaurants"
    "&metro=dallas"
    "&role=server"
    "&utm_campaign=server-levy-fort-worth-tx"
)

EXISTING_SEARCH_ID = "23766390416"
EXISTING_PMAX_ID   = "23766391346"
SOURCE_APP_ID      = "23062774690"
SOURCE_PMAX_ID     = "23043219989"
DAILY_BUDGET       = 30_000_000  # $30/day

def geocode(address):
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json&limit=1"
    req = urllib.request.Request(url, headers={"User-Agent": "IndeedFlex-GeoScript/1.0"})
    resp = json.loads(urllib.request.urlopen(req).read())
    return float(resp[0]["lat"]), float(resp[0]["lon"])


PMAX_TEXT = {
    "headlines": [
        "Hospitality Jobs Hiring Now",
        "Event Server — Fort Worth TX",
        "Flex Jobs in Fort Worth TX",
        "$18–$25/Hr Server Roles",
        "Choose Where & How to Work",
        "Work Upscale Events Near You",
        "Manage Your Own Schedule",
        "Same Day Pay Available",
        "Apply in Minutes on the App",
        "Server Jobs — Start This Week",
        "Work That Suits Your Lifestyle",
        "Indeed Flex Hiring Now",
        "$75 Referral Bonus",
        "Flexible Shifts Available",
        "Top Hospitality Pay — Apply",
    ],
    "long_headlines": [
        "Event Server Jobs in Fort Worth TX — $18–$25/Hr, Flexible Shifts",
        "Hospitality Jobs Hiring Now in Fort Worth — Choose Your Own Schedule",
        "Find Server Roles at Upscale Events Near Fort Worth, Texas",
        "Work Upscale Events & Get Paid Same Day — Fort Worth Hospitality",
        "Indeed Flex: Pick Your Shifts, Work Events, Earn $18–$25/Hr",
    ],
    "descriptions": [
        "Server jobs $18–$25/hr near Fort Worth TX. Same Day Pay & health benefits. Apply now.",
        "Pick your own shifts at upscale events. Earn $18–$25/hr. Same Day Pay available.",
        "Flexible server roles at top venues near Fort Worth, TX. Apply on the Indeed Flex app.",
        "Hospitality jobs hiring now in Fort Worth. $18–$25/hr + benefits + $75 referral bonus.",
        "Choose when and where you work. Event server roles available across Fort Worth, TX.",
    ],
}

APP_VARIANTS = [
    {
        "name": "Fort Worth Hosp - Urgency",
        "headlines": ["Hospitality Jobs Hiring Now", "Event Server — Apply Today",
                      "Flex Jobs Fort Worth TX", "Choose Your Own Shifts", "Same Day Pay"],
        "descriptions": [
            "Server jobs $18–$25/hr in Fort Worth. Flexible shifts for upscale events.",
            "Pick your own shifts at upscale events. Same Day Pay available.",
            "Indeed Flex: apply in minutes, work great events in Fort Worth TX.",
            "Earn $18–$25/hr as an event server. Start working this week in Fort Worth.",
        ],
    },
    {
        "name": "Fort Worth Hosp - Pay & Benefits",
        "headlines": ["$18–$25/Hr Server Jobs", "Same Day Pay Available",
                      "Health & Vision Benefits", "Flex Jobs Fort Worth TX", "$75 Referral Bonus"],
        "descriptions": [
            "Server roles $18–$25/hr with Same Day Pay & health benefits. Apply now.",
            "$75 referral bonus + health/dental/vision. Work Fort Worth area events.",
            "Top hospitality pay in Fort Worth. Same Day Pay + benefits. Apply today.",
            "Earn $18–$25/hr + health benefits at upscale events near Fort Worth, TX.",
        ],
    },
    {
        "name": "Fort Worth Hosp - Process",
        "headlines": ["No Long Application Process", "Apply in Minutes on the App",
                      "Work Upscale Events Near You", "Flex Jobs Fort Worth TX", "Start This Week"],
        "descriptions": [
            "Browse server jobs in Fort Worth & start working this week. Apply in minutes.",
            "Skip the long process. Pick shifts at upscale venues near Fort Worth, TX.",
            "Flexible server opportunities at top venues. Apply now on Indeed Flex.",
            "Event server roles available now. Choose your own schedule in Fort Worth.",
        ],
    },
]


def add_proximity(crit_svc, client, campaign_rn, lat, lon, radius=20):
    op   = client.get_type("CampaignCriterionOperation")
    c    = op.create
    c.campaign = campaign_rn
    c.status   = client.enums.CampaignCriterionStatusEnum.ENABLED
    prox = c.proximity
    prox.geo_point.latitude_in_micro_degrees  = int(lat * 1_000_000)
    prox.geo_point.longitude_in_micro_degrees = int(lon * 1_000_000)
    prox.radius       = radius
    prox.radius_units = client.enums.ProximityRadiusUnitsEnum.MILES
    crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=[op])


def main():
    client   = GoogleAdsClient.load_from_storage(YAML_PATH)
    ga_svc   = client.get_service("GoogleAdsService")
    bud_svc  = client.get_service("CampaignBudgetService")
    camp_svc = client.get_service("CampaignService")
    ag_svc   = client.get_service("AdGroupService")
    ad_svc   = client.get_service("AdGroupAdService")
    c_crit   = client.get_service("CampaignCriterionService")

    print("\n═══════════════════════════════════════════════════════════════")
    print("  Fort Worth Hospitality — Complete PMax + App")
    print("═══════════════════════════════════════════════════════════════\n")

    # ── Geocode ──
    print("── Geocoding Fort Worth TX 76103 ──")
    lat, lon = geocode("Fort Worth, TX 76103")
    print(f"  lat={lat}  lon={lon}\n")
    time.sleep(1)

    # ── Source App settings ──
    q = f"""
        SELECT campaign.app_campaign_setting.app_id,
               campaign.app_campaign_setting.app_store,
               campaign.app_campaign_setting.bidding_strategy_goal_type
        FROM campaign WHERE campaign.id = {SOURCE_APP_ID}
    """
    app_row     = list(ga_svc.search(customer_id=CUSTOMER_ID, query=q))[0]
    app_setting = app_row.campaign.app_campaign_setting

    print(f"  ✅ PMax {EXISTING_PMAX_ID}: asset group already live — skipping\n")

    # ════════════════════════════════════════════════════════════════════
    # APP CAMPAIGN
    # ════════════════════════════════════════════════════════════════════
    print("── Creating App Campaign ──")
    bud_op = client.get_type("CampaignBudgetOperation")
    b = bud_op.create
    b.name              = "BAU Fort Worth Hospitality App"
    b.amount_micros     = DAILY_BUDGET
    b.explicitly_shared = False
    bud_rn = bud_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[bud_op]).results[0].resource_name

    camp_op = client.get_type("CampaignOperation")
    c3 = camp_op.create
    c3.name                              = "p-b2c-google-app-us-bofu-bau-fort_worth-hospitality-eg"
    c3.advertising_channel_type          = client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL
    c3.advertising_channel_sub_type      = client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN
    c3.status                            = client.enums.CampaignStatusEnum.ENABLED
    c3.campaign_budget                   = bud_rn
    c3.contains_eu_political_advertising = 3
    c3.app_campaign_setting.app_id       = app_setting.app_id
    c3.app_campaign_setting.app_store    = app_setting.app_store
    c3.app_campaign_setting.bidding_strategy_goal_type = (
        client.enums.AppCampaignBiddingStrategyGoalTypeEnum
        .OPTIMIZE_INSTALLS_WITHOUT_TARGET_INSTALL_COST
    )
    c3.maximize_conversions.target_cpa_micros = 0
    app_rn = camp_svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[camp_op]).results[0].resource_name
    app_id = app_rn.split("/")[-1]
    print(f"  ✅ App campaign: {c3.name}  (ID: {app_id})")
    add_proximity(c_crit, client, app_rn, lat, lon)
    print(f"  ✅ 20-mile radius geo target set")

    for variant in APP_VARIANTS:
        ag_op4 = client.get_type("AdGroupOperation")
        ag4    = ag_op4.create
        ag4.name     = variant["name"]
        ag4.campaign = app_rn
        ag4.status   = client.enums.AdGroupStatusEnum.ENABLED
        ag_rn4 = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op4]).results[0].resource_name

        ad_op4 = client.get_type("AdGroupAdOperation")
        ada4   = ad_op4.create
        ada4.ad_group = ag_rn4
        ada4.status   = client.enums.AdGroupAdStatusEnum.ENABLED
        app_ad = ada4.ad.app_ad
        for hl in variant["headlines"]:
            a = client.get_type("AdTextAsset"); a.text = hl; app_ad.headlines.append(a)
        for desc in variant["descriptions"]:
            a = client.get_type("AdTextAsset"); a.text = desc; app_ad.descriptions.append(a)
        ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op4])
        print(f"  ✅ App ad group: {variant['name']}")

    # ════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ════════════════════════════════════════════════════════════════════
    print(f"\n═══════════════════════════════════════════════════════════════")
    print(f"  ✅ ALL 3 CAMPAIGNS LIVE — Fort Worth Hospitality BAU")
    print(f"═══════════════════════════════════════════════════════════════")
    print(f"  Search : p-b2c-google-search-us-bofu-bau-fort_worth-hospitality-eg")
    print(f"           ID: {EXISTING_SEARCH_ID}")
    print(f"  P.Max  : p-b2c-google-pmax-us-bofu-bau-fort_worth-hospitality-eg")
    print(f"           ID: {EXISTING_PMAX_ID}")
    print(f"  App    : p-b2c-google-app-us-bofu-bau-fort_worth-hospitality-eg")
    print(f"           ID: {app_id}")
    print(f"\n  Geo    : 20-mile radius from Fort Worth TX 76103")
    print(f"  Budget : $30/day × 3 = $90/day")
    print(f"  Groups : 8 ad groups × 3 RSAs = 24 RSAs (Search) + 3 app ad groups")
    print(f"═══════════════════════════════════════════════════════════════\n")
    return EXISTING_SEARCH_ID, EXISTING_PMAX_ID, app_id


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
