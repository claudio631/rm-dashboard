#!/usr/bin/env python3
"""
Lebanon, TN — RESUME: Complete campaign setup from failed run.
Search campaign (23744408536) exists with 1 ad group (warehouse_operative, no ads).
This script:
1. Adds 3 RSAs to existing warehouse_operative ad group
2. Creates ontrac_jobs + generic_immediate ad groups with keywords + negatives + RSAs
3. Creates App campaign from scratch

Run: python3 scripts/google-ads-lebanon-tn-resume.py
"""
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# Existing resources from previous run
SEARCH_CAMPAIGN_RN = "customers/7236100723/campaigns/23744408536"
EXISTING_AG_RN     = "customers/7236100723/adGroups/197988632569"  # warehouse_operative

# App campaign source
SOURCE_APP_CAMPAIGN_ID = "23062774690"
APP_CAMPAIGN_NAME = "p-b2c-google-app-us-bofu-bau-lebanon-warehouse-ontrac--eg--"
DAILY_BUDGET_MICROS = 30_000_000
LEBANON_GEO_TARGET = "geoTargetConstants/1027402"

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/warehouse-operative/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/501955"
    "&employer=ontrac-final-mile"
    "&metro=nashville"
    "&role=warehouse-operative"
    "&utm_campaign=ontrac-warehouse-operative-lebanon-tn"
)

NEGATIVE_KEYWORDS = [
    "remote", "work from home", "cdl", "truck driver",
    "forklift operator", "forklift certification", "manager",
    "supervisor", "salary", "reviews", "indeed",
    "amazon", "ups", "fedex", "driver", "office", "clerical",
]

# Remaining ad groups to create
REMAINING_AD_GROUPS = [
    {
        "name": "p---ontrac_jobs--",
        "keywords": [
            ("ontrac jobs lebanon tn", "PHRASE"),
            ("ontrac warehouse jobs near me", "PHRASE"),
            ("ontrac hiring lebanon tennessee", "PHRASE"),
            ("ontrac jobs near me", "PHRASE"),
            ("ontrac warehouse operative", "PHRASE"),
            ("delivery warehouse jobs lebanon tn", "PHRASE"),
            ("logistics jobs lebanon tennessee", "PHRASE"),
            ("last mile delivery jobs lebanon tn", "PHRASE"),
            ("ontrac warehouse jobs tennessee", "BROAD"),
            ("delivery company warehouse hiring lebanon tn", "BROAD"),
        ],
    },
    {
        "name": "p---generic_immediate--",
        "keywords": [
            ("jobs hiring now lebanon tn", "PHRASE"),
            ("immediate hire lebanon tennessee", "PHRASE"),
            ("jobs near me lebanon tn", "PHRASE"),
            ("entry level jobs lebanon tn", "PHRASE"),
            ("warehouse jobs nearby tennessee", "PHRASE"),
            ("same day pay jobs lebanon tn", "PHRASE"),
            ("jobs hiring immediately near lebanon tennessee", "BROAD"),
            ("warehouse work near lebanon tn", "BROAD"),
        ],
    },
]

RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Warehouse-Jobs",
        "path2": "Lebanon-TN",
        "headlines": [
            "Warehouse Jobs Lebanon TN",
            "Hiring Now \u2014 Apply Today",
            "Warehouse Operative Roles",
            "$18/Hr Warehouse Work",
            "Start This Week \u2014 Lebanon",
            "Same Day Pay Available",
            "OnTrac Hiring Near You",
            "Immediate Openings TN",
            "Apply in Minutes \u2014 Mobile",
            "Indeed Flex \u2014 Apply Now",
            "Flexible Shift Options",
            "Warehouse Work Near Me",
            "Lebanon TN \u2014 Hiring Now",
            "Get Hired This Week",
            "No Experience Required",
        ],
        "descriptions": [
            "Warehouse operative roles in Lebanon, TN. $18/hr + Same Day Pay. Apply today!",
            "OnTrac is hiring warehouse operatives in Lebanon, TN. Start this week \u2014 apply in minutes.",
            "Flexible warehouse shifts near Lebanon, TN. Same Day Pay, health benefits & quick hiring.",
            "Join Indeed Flex & start warehouse work in Lebanon, TN. Multiple shifts \u2014 apply now free.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Warehouse-Jobs",
        "path2": "Lebanon-TN",
        "headlines": [
            "$18/Hr Warehouse Work",
            "Same Day Pay Available",
            "Health & Dental Benefits",
            "Warehouse Jobs $18/Hr",
            "$75 Referral Bonus",
            "Get Paid Same or Next Day",
            "Competitive Pay + Benefits",
            "Hiring Now \u2014 Lebanon TN",
            "OnTrac Warehouse Jobs",
            "Full-Time Potential Open",
            "Flexible Shift Options",
            "Health & Vision Coverage",
            "Warehouse Operative $18",
            "Apply Today \u2014 Start Now",
            "No Experience Required",
        ],
        "descriptions": [
            "Warehouse operative jobs in Lebanon, TN. $18/hr, Same Day Pay, health/dental/vision.",
            "Earn $75 per referral + Same Day Pay + full benefits. Warehouse roles in Lebanon, TN now.",
            "$18/hr warehouse work with health & dental benefits. Same Day Pay. Hiring Lebanon, TN now.",
            "Full-time potential + $18/hr. Warehouse operative openings at OnTrac in Lebanon, TN.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "path1": "Warehouse-Jobs",
        "path2": "Lebanon-TN",
        "headlines": [
            "No Long Application",
            "Apply in Under 2 Minutes",
            "Start Working This Week",
            "Warehouse Jobs Near Me",
            "Full-Time Potential Open",
            "Indeed Flex \u2014 Lebanon TN",
            "OnTrac Warehouse Hiring",
            "$18/Hr \u2014 Hire Fast",
            "Flexible Shifts Available",
            "Same Day Pay Option",
            "Warehouse Operative Roles",
            "No Experience Needed",
            "Free to Apply \u2014 Start Now",
            "Lebanon TN \u2014 Hiring Now",
            "$75 Referral Bonus",
        ],
        "descriptions": [
            "Apply in under 2 minutes. Warehouse operative jobs in Lebanon, TN \u2014 start this week.",
            "Skip the wait. Warehouse work at OnTrac in Lebanon, TN. Same Day Pay + full benefits.",
            "No experience needed. Warehouse operative roles near Lebanon, TN. Apply free via app.",
            "Get hired fast for warehouse work in Lebanon, TN. $18/hr + flex shifts + Same Day Pay.",
        ],
    },
]

APP_AD_VARIANTS = [
    {
        "label": "Urgency",
        "headlines": [
            "Download App \u2014 Warehouse Jobs",
            "OnTrac Hiring Lebanon TN",
            "Warehouse Work $18/Hr",
            "Same Day Pay Available",
            "Apply in Minutes Near You",
        ],
        "descriptions": [
            "Download Indeed Flex & apply for warehouse operative jobs at OnTrac in Lebanon, TN.",
            "Warehouse jobs $18/hr near Lebanon, TN. Same Day Pay. Download the app & apply now.",
            "Download the app, apply in minutes & start warehouse work at OnTrac this week in TN.",
            "Same Day Pay + health benefits. Warehouse operative roles at OnTrac. Download & apply.",
            "Indeed Flex is hiring warehouse operatives in Lebanon, TN. Download app & get started.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "headlines": [
            "Warehouse Work $18/Hr",
            "$75 Referral Bonus",
            "Same Day Pay Available",
            "Health & Dental Benefits",
            "OnTrac Hiring Lebanon TN",
        ],
        "descriptions": [
            "$18/hr warehouse work with health/dental benefits. Download Indeed Flex & apply now.",
            "Earn $75 per referral + Same Day Pay. Download the app for Lebanon, TN warehouse jobs.",
            "Competitive pay, flex shifts & Same Day Pay. Download Indeed Flex & start this week.",
            "Full-time potential + benefits. Download Indeed Flex for OnTrac warehouse jobs in TN.",
            "Indeed Flex \u2014 warehouse operative roles $18/hr near Lebanon, TN. Download & apply.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "headlines": [
            "Download App \u2014 Warehouse Jobs",
            "Get Hired Fast Lebanon TN",
            "Full-Time Potential Available",
            "No Long Application Process",
            "Apply in Under 2 Minutes",
        ],
        "descriptions": [
            "Download Indeed Flex & apply in under 2 min. Warehouse jobs Lebanon, TN \u2014 start now.",
            "Skip the wait. Download the app & get warehouse work at OnTrac in Lebanon, TN.",
            "Full-time opportunities available. Download Indeed Flex for OnTrac warehouse jobs.",
            "No experience needed. Download app, apply free & start warehouse work in Lebanon, TN.",
            "Get hired fast for $18/hr warehouse work. Download Indeed Flex & apply in minutes.",
        ],
    },
]


# ── Helpers ──────────────────────────────────────────────────────────────

def create_search_ad_group(client, customer_id, campaign_rn, name):
    svc = client.get_service("AdGroupService")
    op  = client.get_type("AdGroupOperation")
    ag  = op.create
    ag.name           = name
    ag.campaign       = campaign_rn
    ag.status         = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_          = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag.cpc_bid_micros = 2_500_000
    result = svc.mutate_ad_groups(customer_id=customer_id, operations=[op])
    return result.results[0].resource_name


def add_keywords(client, customer_id, ag_rn, keywords):
    svc = client.get_service("AdGroupCriterionService")
    me  = client.enums.KeywordMatchTypeEnum
    ops = []
    for text, match in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        c  = op.create
        c.ad_group           = ag_rn
        c.status             = client.enums.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text       = text
        c.keyword.match_type = getattr(me, match)
        ops.append(op)
    svc.mutate_ad_group_criteria(customer_id=customer_id, operations=ops)
    print(f"    \u2705 {len(ops)} keyword(s) added")


def add_negative_keywords(client, customer_id, ag_rn, negatives):
    svc = client.get_service("AdGroupCriterionService")
    ops = []
    for text in negatives:
        op = client.get_type("AdGroupCriterionOperation")
        c  = op.create
        c.ad_group           = ag_rn
        c.status             = client.enums.AdGroupCriterionStatusEnum.ENABLED
        c.negative           = True
        c.keyword.text       = text
        c.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
    svc.mutate_ad_group_criteria(customer_id=customer_id, operations=ops)
    print(f"    \u2705 {len(ops)} negative keyword(s) added")


def add_rsa(client, customer_id, ag_rn, variant):
    svc = client.get_service("AdGroupAdService")
    op  = client.get_type("AdGroupAdOperation")
    ada = op.create
    ada.ad_group = ag_rn
    ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
    ad  = ada.ad
    ad.final_urls.append(FINAL_URL)
    rsa       = ad.responsive_search_ad
    rsa.path1 = variant["path1"]
    rsa.path2 = variant["path2"]
    for hl in variant["headlines"]:
        asset = client.get_type("AdTextAsset")
        asset.text = hl
        rsa.headlines.append(asset)
    for desc in variant["descriptions"]:
        asset = client.get_type("AdTextAsset")
        asset.text = desc
        rsa.descriptions.append(asset)
    result = svc.mutate_ad_group_ads(customer_id=customer_id, operations=[op])
    return result.results[0].resource_name


def add_app_ad(client, customer_id, ag_rn, variant):
    svc = client.get_service("AdGroupAdService")
    op  = client.get_type("AdGroupAdOperation")
    ada = op.create
    ada.ad_group = ag_rn
    ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
    app_ad = ada.ad.app_ad
    for hl in variant["headlines"]:
        asset = client.get_type("AdTextAsset")
        asset.text = hl
        app_ad.headlines.append(asset)
    for desc in variant["descriptions"]:
        asset = client.get_type("AdTextAsset")
        asset.text = desc
        app_ad.descriptions.append(asset)
    result = svc.mutate_ad_group_ads(customer_id=customer_id, operations=[op])
    return result.results[0].resource_name


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    cid    = CUSTOMER_ID

    print("\n" + "\u2550" * 62)
    print("  Lebanon, TN \u2014 RESUME Campaign Setup")
    print("\u2550" * 62 + "\n")

    # ─── STEP 1: Add RSAs to existing warehouse_operative ad group ────
    print("\u25b6 SEARCH CAMPAIGN (existing: 23744408536)\n")
    print("  \u2192 p---warehouse_operative-- (existing, adding RSAs)")
    for i, variant in enumerate(RSA_VARIANTS, 1):
        rsa_rn = add_rsa(client, cid, EXISTING_AG_RN, variant)
        print(f"    \u2705 RSA {i} [{variant['label']}]: {rsa_rn}")

    # ─── STEP 2: Create remaining 2 ad groups ────────────────────────
    for ag_def in REMAINING_AD_GROUPS:
        print(f"\n  \u2192 {ag_def['name']} (new)")
        ag_rn = create_search_ad_group(client, cid, SEARCH_CAMPAIGN_RN, ag_def["name"])
        print(f"    AG created: {ag_rn}")

        print(f"    Adding {len(ag_def['keywords'])} keywords...")
        add_keywords(client, cid, ag_rn, ag_def["keywords"])

        print(f"    Adding {len(NEGATIVE_KEYWORDS)} negatives...")
        add_negative_keywords(client, cid, ag_rn, NEGATIVE_KEYWORDS)

        print("    Adding 3 RSA variants...")
        for i, variant in enumerate(RSA_VARIANTS, 1):
            rsa_rn = add_rsa(client, cid, ag_rn, variant)
            print(f"    \u2705 RSA {i} [{variant['label']}]: {rsa_rn}")

    # ─── STEP 3: App Campaign ────────────────────────────────────────
    print("\n\n\u25b6 APP CAMPAIGN\n")

    print("  [1/4] Fetching Nashville BAU App campaign settings...")
    ga_svc = client.get_service("GoogleAdsService")
    q = f"""SELECT campaign.id, campaign.name,
                   campaign.app_campaign_setting.app_id,
                   campaign.app_campaign_setting.app_store,
                   campaign.app_campaign_setting.bidding_strategy_goal_type
            FROM campaign WHERE campaign.id = {SOURCE_APP_CAMPAIGN_ID} LIMIT 1"""
    src_app = None
    for row in ga_svc.search(customer_id=cid, query=q):
        src_app = row.campaign
    if not src_app:
        print("  \u274c Source app campaign not found!")
        return

    print("\n  [2/4] Creating $30/day budget...")
    bsvc = client.get_service("CampaignBudgetService")
    bop  = client.get_type("CampaignBudgetOperation")
    b    = bop.create
    b.name              = "BAU Lebanon TN App"
    b.amount_micros     = DAILY_BUDGET_MICROS
    b.delivery_method   = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    result = bsvc.mutate_campaign_budgets(customer_id=cid, operations=[bop])
    app_budget_rn = result.results[0].resource_name
    print(f"  \u2705 Budget created: {app_budget_rn}")

    print("\n  [3/4] Creating app campaign...")
    csvc = client.get_service("CampaignService")
    cop  = client.get_type("CampaignOperation")
    c    = cop.create
    c.name            = APP_CAMPAIGN_NAME
    c.campaign_budget = app_budget_rn
    c.status          = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type     = client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL
    c.advertising_channel_sub_type = client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN
    c.app_campaign_setting.app_id                     = src_app.app_campaign_setting.app_id
    c.app_campaign_setting.app_store                  = src_app.app_campaign_setting.app_store
    c.app_campaign_setting.bidding_strategy_goal_type = src_app.app_campaign_setting.bidding_strategy_goal_type
    c.maximize_conversions.target_cpa_micros = 0
    result = csvc.mutate_campaigns(customer_id=cid, operations=[cop])
    app_campaign_rn = result.results[0].resource_name
    print(f"  \u2705 App campaign created: {app_campaign_rn}")

    print("\n  [4/4] Setting geo target (Lebanon, TN)...")
    crsvc = client.get_service("CampaignCriterionService")
    crop  = client.get_type("CampaignCriterionOperation")
    cc    = crop.create
    cc.campaign = app_campaign_rn
    cc.location.geo_target_constant = LEBANON_GEO_TARGET
    cc.negative = False
    crsvc.mutate_campaign_criteria(customer_id=cid, operations=[crop])
    print("  \u2705 Geo target set: Lebanon, TN")

    print("\n  \u2500\u2500 App Ad Group \u2500\u2500")
    agsvc = client.get_service("AdGroupService")
    agop  = client.get_type("AdGroupOperation")
    ag    = agop.create
    ag.name     = "Lebanon TN \u2014 Warehouse Operative"
    ag.campaign = app_campaign_rn
    ag.status   = client.enums.AdGroupStatusEnum.ENABLED
    result = agsvc.mutate_ad_groups(customer_id=cid, operations=[agop])
    app_ag_rn = result.results[0].resource_name
    print(f"  \u2192 Lebanon TN \u2014 Warehouse Operative: {app_ag_rn}")

    print("    Adding 3 app ad variants...")
    for i, variant in enumerate(APP_AD_VARIANTS, 1):
        ad_rn = add_app_ad(client, cid, app_ag_rn, variant)
        print(f"    \u2705 App Ad {i} [{variant['label']}]: {ad_rn}")

    # ─── SUMMARY ─────────────────────────────────────────────────────
    print("\n" + "\u2550" * 62)
    print("  \u2705 LAUNCH COMPLETE")
    print(f"  Search: p-b2c-google-search-us-bofu-bau-lebanon-warehouse-ontrac--eg--")
    print(f"  App:    {APP_CAMPAIGN_NAME}")
    print(f"  Budget: $30/day each ($60/day total)")
    print(f"  Geo:    Lebanon, TN (Wilson County)")
    print(f"  Status: ENABLED (live)")
    print("\u2550" * 62 + "\n")
    print("  Note: P.Max campaign requires manual creation in Google Ads UI\n")


if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"\n\u274c Google Ads API error:\n")
        for error in ex.failure.errors:
            print(f"  {error.error_code}: {error.message}")
        sys.exit(1)
