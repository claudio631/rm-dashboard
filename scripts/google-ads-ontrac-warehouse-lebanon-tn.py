#!/usr/bin/env python3
"""
Lebanon, TN — BAU Campaign Launch (Search + App)
- Creates NEW Search campaign with 3 ad groups, 3 RSAs each, keywords, negatives
- Creates NEW App campaign with 3 app ad variants
- $30/day each, Maximize Conversions, ongoing BAU (no end date)
- Geo: Lebanon, TN 37087 area

Run: python3 scripts/google-ads-ontrac-warehouse-lebanon-tn.py
"""
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Copy App campaign settings from Nashville BAU ────────────────────────
SOURCE_APP_CAMPAIGN_ID = "23062774690"  # Nashville BAU App

# ── Budget config ────────────────────────────────────────────────────────
DAILY_BUDGET_MICROS = 30_000_000  # $30/day

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/warehouse-operative/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/501955"
    "&employer=ontrac-final-mile"
    "&metro=nashville"
    "&role=warehouse-operative"
    "&utm_campaign=ontrac-warehouse-operative-lebanon-tn"
)

SEARCH_CAMPAIGN_NAME = "p-b2c-google-search-us-bofu-bau-lebanon-warehouse-ontrac--eg--"
APP_CAMPAIGN_NAME    = "p-b2c-google-app-us-bofu-bau-lebanon-warehouse-ontrac--eg--"

# ── Geo targeting: Lebanon, TN 37087 ────────────────────────────────────
# Google Ads geo target constant for Lebanon, TN (city)
# 1027402 = Lebanon city, TN
LEBANON_GEO_TARGET = "geoTargetConstants/1027402"

# ── Ad Groups ────────────────────────────────────────────────────────────
AD_GROUPS = [
    {
        "name": "p---warehouse_operative--",
        "keywords": [
            ("warehouse operative jobs lebanon tn", "PHRASE"),
            ("warehouse operative jobs near lebanon tennessee", "PHRASE"),
            ("warehouse worker jobs lebanon tn", "PHRASE"),
            ("warehouse jobs lebanon tennessee", "PHRASE"),
            ("warehouse jobs near me lebanon", "PHRASE"),
            ("warehouse jobs hiring now lebanon tn", "PHRASE"),
            ("warehouse operative near lebanon", "PHRASE"),
            ("warehouse work lebanon tennessee", "PHRASE"),
            ("picker packer jobs lebanon tn", "PHRASE"),
            ("fulfillment jobs lebanon tn", "PHRASE"),
            ("warehouse jobs wilson county", "PHRASE"),
            ("warehouse operative hiring lebanon tennessee", "BROAD"),
            ("warehouse jobs near lebanon tn now", "BROAD"),
            ("fulfillment center jobs near lebanon tennessee", "BROAD"),
        ],
    },
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

NEGATIVE_KEYWORDS = [
    "remote", "work from home", "cdl", "truck driver",
    "forklift operator", "forklift certification", "manager",
    "supervisor", "salary", "reviews", "indeed",
    "amazon", "ups", "fedex", "driver", "office", "clerical",
]

# ── RSA copy — 3 variants per ad group ───────────────────────────────────
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

# ── App ad copy — 3 variants ────────────────────────────────────────────
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
            "Download Indeed Flex & apply in under 2 minutes. Warehouse jobs Lebanon, TN \u2014 start now.",
            "Skip the wait. Download the app & get warehouse work at OnTrac in Lebanon, TN.",
            "Full-time opportunities available. Download Indeed Flex for OnTrac warehouse jobs.",
            "No experience needed. Download app, apply free & start warehouse work in Lebanon, TN.",
            "Get hired fast for $18/hr warehouse work. Download Indeed Flex & apply in minutes.",
        ],
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Helper functions
# ══════════════════════════════════════════════════════════════════════════

def create_budget(client, customer_id, label):
    svc = client.get_service("CampaignBudgetService")
    op  = client.get_type("CampaignBudgetOperation")
    b   = op.create
    b.name              = f"BAU Lebanon TN {label}"
    b.amount_micros     = DAILY_BUDGET_MICROS
    b.delivery_method   = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    result = svc.mutate_campaign_budgets(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  \u2705 Budget created: {rn}")
    return rn


def create_search_campaign(client, customer_id, budget_rn, name):
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name            = name
    c.campaign_budget = budget_rn
    c.status          = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    # BAU = no end date
    c.network_settings.target_google_search          = True
    c.network_settings.target_search_network         = True
    c.network_settings.target_content_network        = False
    c.network_settings.target_partner_search_network = False
    # Maximize Conversions (no tCPA initially)
    c.maximize_conversions.target_cpa_micros = 0
    c.contains_eu_political_advertising = 3  # DOES_NOT_CONTAIN
    result = svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  \u2705 Search campaign created: {rn}")
    return rn


def create_app_campaign(client, customer_id, source, budget_rn, name):
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name            = name
    c.campaign_budget = budget_rn
    c.status          = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type     = client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL
    c.advertising_channel_sub_type = client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN
    c.app_campaign_setting.app_id                     = source.app_campaign_setting.app_id
    c.app_campaign_setting.app_store                  = source.app_campaign_setting.app_store
    c.app_campaign_setting.bidding_strategy_goal_type = (
        source.app_campaign_setting.bidding_strategy_goal_type
    )
    c.maximize_conversions.target_cpa_micros = 0
    result = svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  \u2705 App campaign created: {rn}")
    return rn


def set_geo_target(client, customer_id, campaign_rn, geo_constant):
    svc = client.get_service("CampaignCriterionService")
    op  = client.get_type("CampaignCriterionOperation")
    cc  = op.create
    cc.campaign = campaign_rn
    cc.location.geo_target_constant = geo_constant
    cc.negative = False
    svc.mutate_campaign_criteria(customer_id=customer_id, operations=[op])
    print(f"  \u2705 Geo target set: Lebanon, TN")


def create_search_ad_group(client, customer_id, campaign_rn, name):
    svc = client.get_service("AdGroupService")
    op  = client.get_type("AdGroupOperation")
    ag  = op.create
    ag.name           = name
    ag.campaign       = campaign_rn
    ag.status         = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_          = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag.cpc_bid_micros = 2_500_000  # $2.50 max CPC
    result = svc.mutate_ad_groups(customer_id=customer_id, operations=[op])
    return result.results[0].resource_name


def create_app_ad_group(client, customer_id, campaign_rn, name):
    svc = client.get_service("AdGroupService")
    op  = client.get_type("AdGroupOperation")
    ag  = op.create
    ag.name     = name
    ag.campaign = campaign_rn
    ag.status   = client.enums.AdGroupStatusEnum.ENABLED
    result = svc.mutate_ad_groups(customer_id=customer_id, operations=[op])
    return result.results[0].resource_name


def add_keywords(client, customer_id, ag_rn, keywords):
    if not keywords:
        return 0
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
    return len(ops)


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


def fetch_campaign(client, customer_id, campaign_id):
    ga_svc = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            campaign.id, campaign.name,
            campaign.app_campaign_setting.app_id,
            campaign.app_campaign_setting.app_store,
            campaign.app_campaign_setting.bidding_strategy_goal_type
        FROM campaign
        WHERE campaign.id = {campaign_id}
        LIMIT 1
    """
    for row in ga_svc.search(customer_id=customer_id, query=query):
        return row.campaign
    raise ValueError(f"Campaign {campaign_id} not found")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    cid    = CUSTOMER_ID

    print("\n\u2550" * 62)
    print("  Lebanon, TN \u2014 BAU Campaign Launch (Search + App)")
    print("  OnTrac Warehouse Operative | $30/day each | Maximize Conversions")
    print("\u2550" * 62 + "\n")

    # ─────────────────────────────────────────────────────────────────
    # SEARCH CAMPAIGN
    # ─────────────────────────────────────────────────────────────────
    print("\u25b6 SEARCH CAMPAIGN\n")

    print("  [1/3] Creating $30/day budget...")
    search_budget_rn = create_budget(client, cid, "Search")

    print("\n  [2/3] Creating search campaign...")
    search_campaign_rn = create_search_campaign(
        client, cid, search_budget_rn, SEARCH_CAMPAIGN_NAME
    )

    print("\n  [3/3] Setting geo target (Lebanon, TN)...")
    set_geo_target(client, cid, search_campaign_rn, LEBANON_GEO_TARGET)

    print("\n  \u2500\u2500 Ad Groups \u2500\u2500")
    for ag_def in AD_GROUPS:
        print(f"\n  \u2192 {ag_def['name']}")
        ag_rn = create_search_ad_group(client, cid, search_campaign_rn, ag_def["name"])

        # Keywords
        print(f"    Adding {len(ag_def['keywords'])} keywords...")
        add_keywords(client, cid, ag_rn, ag_def["keywords"])

        # Negative keywords
        print(f"    Adding {len(NEGATIVE_KEYWORDS)} negatives...")
        add_negative_keywords(client, cid, ag_rn, NEGATIVE_KEYWORDS)

        # 3 RSA variants
        print("    Adding 3 RSA variants...")
        for i, variant in enumerate(RSA_VARIANTS, 1):
            rsa_rn = add_rsa(client, cid, ag_rn, variant)
            print(f"    \u2705 RSA {i} [{variant['label']}]: {rsa_rn}")

    # ─────────────────────────────────────────────────────────────────
    # APP CAMPAIGN
    # ─────────────────────────────────────────────────────────────────
    print("\n\n\u25b6 APP CAMPAIGN\n")

    print("  [1/4] Fetching Nashville BAU App campaign settings...")
    src_app = fetch_campaign(client, cid, SOURCE_APP_CAMPAIGN_ID)

    print("\n  [2/4] Creating $30/day budget...")
    app_budget_rn = create_budget(client, cid, "App")

    print("\n  [3/4] Creating app campaign...")
    app_campaign_rn = create_app_campaign(
        client, cid, src_app, app_budget_rn, APP_CAMPAIGN_NAME
    )

    print("\n  [4/4] Setting geo target (Lebanon, TN)...")
    set_geo_target(client, cid, app_campaign_rn, LEBANON_GEO_TARGET)

    print("\n  \u2500\u2500 App Ad Group \u2500\u2500")
    app_ag_rn = create_app_ad_group(
        client, cid, app_campaign_rn, "Lebanon TN \u2014 Warehouse Operative"
    )
    print(f"  \u2192 Lebanon TN \u2014 Warehouse Operative")

    print("    Adding 3 app ad variants...")
    for i, variant in enumerate(APP_AD_VARIANTS, 1):
        ad_rn = add_app_ad(client, cid, app_ag_rn, variant)
        print(f"    \u2705 App Ad {i} [{variant['label']}]: {ad_rn}")

    # ─────────────────────────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────────────────────────
    print("\n" + "\u2550" * 62)
    print("  \u2705 LAUNCH COMPLETE")
    print(f"  Search: {SEARCH_CAMPAIGN_NAME}")
    print(f"  App:    {APP_CAMPAIGN_NAME}")
    print(f"  Budget: $30/day each ($60/day total)")
    print(f"  Geo:    Lebanon, TN (Wilson County)")
    print(f"  Status: ENABLED (live)")
    print("\u2550" * 62 + "\n")
    print("  Note: P.Max campaign requires manual creation in Google Ads UI")
    print("  (API does not support full P.Max asset group creation)\n")


if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"\n\u274c Google Ads API error:\n")
        for error in ex.failure.errors:
            print(f"  {error.error_code}: {error.message}")
        sys.exit(1)
