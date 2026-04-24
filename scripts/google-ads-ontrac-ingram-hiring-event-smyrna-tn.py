#!/usr/bin/env python3
"""
Google Ads — Ingram/Ontrac Hiring Event — Smyrna, TN (Apr 24, 2026)
Campaigns: Search ($50/day) + Performance Max ($50/day) + App ($50/day)
Flight:    Apr 17–24, 2026  |  Total daily: $150  |  Total: ~$1,050

Search : 3 ad groups × 3 RSAs = 9 RSAs total
P.Max  : 1 asset group (Warehouse — Smyrna TN) — visual assets from BAU Nashville P.Max
App    : 3 ad groups × 1 UAC ad = 3 app ads total

Run: python3 scripts/google-ads-ontrac-ingram-hiring-event-smyrna-tn.py
"""

from typing import Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Source BAU campaign IDs (Nashville Industrial) ─────────────────────────
SOURCE_SEARCH_CAMPAIGN_ID = "23059952812"   # p-b2c-google-search-us-bofu-bau-nashville-industrial--eg--
SOURCE_APP_CAMPAIGN_ID    = "23048055977"   # p-b2c-google-app-us-bofu-bau-nashville-industrial--eg--
SOURCE_PMAX_CAMPAIGN_ID   = "DISCOVER"      # Auto-discover Nashville Industrial P.Max

# ── Event config ────────────────────────────────────────────────────────────
DAILY_BUDGET_MICROS = 50_000_000           # $50/day
EVENT_END_DATE_TIME = "2026-04-24 23:59:59"
FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/504297"
    "&employer=NA&metro=nashville"
    "&role=warehouse-operative"
    "&utm_campaign=ontrac-ingram-hiring-event-smyrna-tn"
)

SEARCH_NAME = "p-b2c-google-search-us-bofu-bau-smyrna-industrial-hiring-event-04242026"
PMAX_NAME   = "p-b2c-google-pmax-us-bofu-bau-smyrna-industrial-hiring-event-04242026"
APP_NAME    = "p-b2c-google-app-us-bofu-bau-smyrna-industrial-hiring-event-04242026"

VISUAL_FIELD_TYPE_NAMES = {
    "MARKETING_IMAGE", "SQUARE_MARKETING_IMAGE", "PORTRAIT_MARKETING_IMAGE",
    "LOGO", "LANDSCAPE_LOGO",
    # YOUTUBE_VIDEO excluded — deleted videos cause API errors
}

# ═══════════════════════════════════════════════════════════════════════════
# SEARCH — Ad Groups, Keywords, RSA Variants
# ═══════════════════════════════════════════════════════════════════════════

SEARCH_AD_GROUPS = [
    {
        "name": "Hiring Event — Smyrna TN",
        "cpc_bid_micros": 2_500_000,
        "keywords": [
            ("hiring event smyrna tn", "PHRASE"),
            ("hiring event near me", "PHRASE"),
            ("warehouse hiring event nashville", "PHRASE"),
            ("job fair smyrna tennessee", "PHRASE"),
            ("walk in job fair nashville", "PHRASE"),
            ("warehouse job fair near me", "PHRASE"),
            ("hiring event murfreesboro tn", "PHRASE"),
            ("immediate hire warehouse tennessee", "PHRASE"),
            ("warehouse hiring event la vergne", "PHRASE"),
        ],
    },
    {
        "name": "Warehouse Jobs — Smyrna Nashville",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("warehouse jobs smyrna tn", "PHRASE"),
            ("warehouse jobs nashville tn", "PHRASE"),
            ("warehouse jobs near me", "PHRASE"),
            ("warehouse worker smyrna tennessee", "PHRASE"),
            ("warehouse jobs hiring now nashville", "PHRASE"),
            ("warehouse jobs murfreesboro tn", "PHRASE"),
            ("general labor jobs nashville tn", "PHRASE"),
            ("warehouse work near smyrna", "PHRASE"),
            ("entry level warehouse jobs nashville", "PHRASE"),
        ],
    },
    {
        "name": "Warehouse Jobs — La Vergne Lebanon",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("warehouse jobs la vergne tn", "PHRASE"),
            ("warehouse jobs lebanon tn", "PHRASE"),
            ("warehouse jobs hiring now la vergne", "PHRASE"),
            ("jobs hiring near me la vergne", "PHRASE"),
            ("warehouse jobs no experience tn", "PHRASE"),
            ("warehouse jobs rutherford county", "PHRASE"),
            ("industrial jobs smyrna tn", "PHRASE"),
            ("jobs hiring near me nashville tn", "PHRASE"),
        ],
    },
]

# 3 RSA variants applied to EVERY search ad group
RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Hiring-Event",
        "path2": "Smyrna-TN",
        "headlines": [
            "Hiring Event — April 24th",
            "Smyrna TN · Thu Apr 24",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Register Before Spots Fill Up",
            "Get Hired Today — Apr 24",
            "Meet Recruiters Face to Face",
            "Indeed Flex Hiring Event",
            "Warehouse Jobs Hiring Now",
            "Work Near La Vergne TN",
            "1st & 2nd Shift Available",
            "Same Day Pay Available",
            "This Thursday — Apr 24",
            "$75 Referral Bonus",
            "Limited Spots — Register Now",
        ],
        "descriptions": [
            "Join us Apr 24, 9am-3pm at Courtyard Marriott, Smyrna TN. Get hired on the spot!",
            "No long process. Meet our recruiters & get an instant offer on April 24th. Sign up free.",
            "Walk in, interview live, and leave with a job offer on April 24 in Smyrna, TN.",
            "Limited spots left. Register today for the Indeed Flex hiring event on April 24th, 2026.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Warehouse-Jobs",
        "path2": "Smyrna-TN",
        "headlines": [
            "Warehouse Jobs $17–$18/Hr",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Health & Vision Benefits",
            "Warehouse Work $17.50/Hr",
            "Full-Time Potential Available",
            "Hiring Event — April 24th",
            "Smyrna TN · Thu Apr 24",
            "Get Paid Same Day or Next Day",
            "Health & Dental Coverage",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Long & Short-Term Work",
            "Competitive Pay + Benefits",
            "Indeed Flex Hiring Event",
        ],
        "descriptions": [
            "Warehouse roles $17.50-$18/hr. Same Day Pay & health benefits. Apply now.",
            "$75 per referral, Same Day Pay & full health benefits. Join us April 24th.",
            "Competitive pay $17.50-$18/hr, health/dental/vision & Same Day Pay. Join us Apr 24.",
            "Come to our Apr 24 hiring event. Leave with a $17.50-$18/hr offer + full benefits.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "path1": "Warehouse-Jobs",
        "path2": "Nashville-TN",
        "headlines": [
            "No Long Application Process",
            "Get Hired in One Day",
            "Meet Recruiters Face to Face",
            "Start Working This Week",
            "Full-Time Potential Available",
            "Warehouse Jobs Hiring Now",
            "Flexible 1st & 2nd Shifts",
            "Hiring Event — April 24th",
            "Smyrna TN · Thu Apr 24",
            "Walk In, Walk Out Employed",
            "Indeed Flex Hiring Event",
            "Warehouse Jobs $17–$18/Hr",
            "Apply in Minutes on Site",
            "Same Day Pay Available",
            "This Thursday — Apr 24",
        ],
        "descriptions": [
            "Indeed Flex hiring event — walk in & leave with a job offer. 1st & 2nd shift openings.",
            "Skip the wait. Interview live with recruiters on April 24 & start working this week.",
            "Full-time opportunities available. Attend Apr 24 at Courtyard Marriott, Smyrna, TN.",
            "Warehouse roles open now. Walk in on April 24 & leave with a job offer. No wait.",
        ],
    },
]

NEGATIVE_KEYWORDS = [
    ("forklift certification", "PHRASE"),
    ("forklift operator", "PHRASE"),
    ("cdl", "PHRASE"),
    ("truck driver", "PHRASE"),
    ("remote", "PHRASE"),
    ("work from home", "PHRASE"),
    ("manager", "PHRASE"),
    ("supervisor", "PHRASE"),
    ("salary", "PHRASE"),
    ("amazon", "PHRASE"),
    ("ups", "PHRASE"),
    ("fedex", "PHRASE"),
    ("driver", "PHRASE"),
    ("internship", "PHRASE"),
    ("volunteer", "PHRASE"),
]

# ═══════════════════════════════════════════════════════════════════════════
# PERFORMANCE MAX — Text Assets
# ═══════════════════════════════════════════════════════════════════════════

PMAX_HEADLINES = [
    "Hiring Event — April 24th",
    "Smyrna TN · Thu Apr 24",
    "Warehouse Jobs $17–$18/Hr",
    "Instant Job Offer on the Spot",
    "Warehouse Jobs Hiring Now",
    "Walk In, Walk Out Employed",
    "Same Day Pay Available",
    "This Thursday — Apr 24",
    "Meet Recruiters Face to Face",
    "Indeed Flex Hiring Event",
    "Work Near La Vergne TN",
    "1st & 2nd Shift Available",
    "Get Hired Today — Apr 24",
    "$75 Referral Bonus",
    "Limited Spots — Register Now",
]

PMAX_LONG_HEADLINES = [
    "Join our April 24 hiring event in Smyrna, TN. Warehouse jobs $17.50-$18/hr.",
    "Walk in, walk out employed. Indeed Flex warehouse jobs near Nashville, TN.",
    "This Thursday only. Warehouse hiring event April 24 in Smyrna — apply free.",
    "Same Day Pay. We're hiring Warehouse Workers in Smyrna, TN. Get hired on the spot Apr 24.",
    "No experience needed. 1st & 2nd shifts available. Get hired on the spot April 24.",
]

PMAX_DESCRIPTIONS = [
    "Hiring event Apr 24, 9am-3pm in Smyrna, TN. Warehouse jobs $17.50-$18/hr. Apply free!",
    "Warehouse roles $17.50-$18/hr. Same Day Pay & health benefits. Apply now.",
    "Indeed Flex hiring event — walk in & leave with a job offer. 1st & 2nd shift openings.",
    "No long process. Meet our recruiters & get an instant offer on April 24th. Sign up free.",
    "$17.50-$18/hr warehouse roles near Nashville. Get hired Apr 24 — same day pay & benefits.",
]

# ═══════════════════════════════════════════════════════════════════════════
# APP CAMPAIGN — 3 Ad Groups × 1 UAC Ad
# ═══════════════════════════════════════════════════════════════════════════

APP_AD_GROUPS = [
    {
        "name": "Smyrna HE - Urgency",
        "headlines": [
            "Download App & Attend Apr 24",
            "Hiring Event — April 24th",
            "Warehouse Jobs $17–$18/Hr",
            "Limited Spots — Register Now",
            "Get Hired at Our Live Event",
        ],
        "descriptions": [
            "Download Indeed Flex & register for our Apr 24 hiring event in Smyrna, TN.",
            "Walk in April 24, 9am-3pm. Get hired on the spot. Register via app today.",
            "Limited spots available. Download the app & register for Apr 24 event in TN.",
            "No long process. Download, sign up & attend our hiring event on April 24th.",
            "Get hired on April 24 in Smyrna, TN. Download the Indeed Flex app now.",
        ],
    },
    {
        "name": "Smyrna HE - Pay & Benefits",
        "headlines": [
            "Warehouse Jobs $17–$18/Hr",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Warehouse Jobs Near Nashville",
            "Health Benefits Included",
        ],
        "descriptions": [
            "Warehouse $17.50-$18/hr. Same Day Pay & health benefits. Download the app.",
            "Download Indeed Flex, register for Apr 24 hiring event & earn $17.50-$18/hr.",
            "Same Day Pay, $75 referral & health benefits. Come to our Apr 24 event.",
            "Competitive pay + benefits. Download Indeed Flex & attend hiring event April 24.",
            "Same Day Pay, health/dental/vision. Join us Apr 24 in Smyrna, TN.",
        ],
    },
    {
        "name": "Smyrna HE - Process",
        "headlines": [
            "Download App & Attend Apr 24",
            "Get Hired at Our Live Event",
            "Full-Time Potential Available",
            "No Long Interview Process",
            "Hiring Event — April 24th",
        ],
        "descriptions": [
            "Download Indeed Flex & come to our Apr 24 event. Walk in, get hired, start this week.",
            "Skip the wait — attend our live hiring event. Get an instant job offer on April 24.",
            "Full-time opportunities available. Download app, register & attend Apr 24 event.",
            "No lengthy process. Interview live Apr 24 in Smyrna, TN. Download Indeed Flex today.",
            "Walk in on April 24, meet our recruiters & leave with a $17.50-$18/hr offer.",
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def create_budget(client, label: str) -> str:
    svc = client.get_service("CampaignBudgetService")
    op  = client.get_type("CampaignBudgetOperation")
    b   = op.create
    b.name              = f"Smyrna Industrial HE {label} 20260424"
    b.amount_micros     = DAILY_BUDGET_MICROS
    b.delivery_method   = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    result = svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ Budget: ${DAILY_BUDGET_MICROS // 1_000_000}/day  →  {rn}")
    return rn


def fetch_campaign(client, campaign_id: str):
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT
            campaign.id, campaign.name,
            campaign.advertising_channel_type,
            campaign.advertising_channel_sub_type,
            campaign.network_settings.target_google_search,
            campaign.network_settings.target_search_network,
            campaign.network_settings.target_content_network,
            campaign.network_settings.target_partner_search_network,
            campaign.app_campaign_setting.app_id,
            campaign.app_campaign_setting.app_store,
            campaign.app_campaign_setting.bidding_strategy_goal_type
        FROM campaign
        WHERE campaign.id = {campaign_id}
        LIMIT 1
    """
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        return row.campaign
    raise ValueError(f"Campaign {campaign_id} not found")


def discover_pmax_campaign(client) -> Optional[str]:
    ga_svc = client.get_service("GoogleAdsService")
    query  = """
        SELECT campaign.id, campaign.name
        FROM campaign
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND campaign.name LIKE '%nashville%industrial%'
          AND campaign.status != 'REMOVED'
        LIMIT 5
    """
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        c = row.campaign
        print(f"  Found P.Max candidate: {c.name}  (ID: {c.id})")
        return str(c.id)
    return None


def fetch_geo_targets(client, campaign_id: str) -> list:
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT
            campaign_criterion.location.geo_target_constant,
            campaign_criterion.bid_modifier,
            campaign_criterion.negative
        FROM campaign_criterion
        WHERE campaign.id = {campaign_id}
          AND campaign_criterion.type = 'LOCATION'
    """
    results = []
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        cc = row.campaign_criterion
        results.append({
            "geo_target_constant": cc.location.geo_target_constant,
            "bid_modifier":        cc.bid_modifier,
            "negative":            cc.negative,
        })
    return results


def fetch_pmax_asset_group(client, pmax_campaign_id: str) -> Optional[str]:
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT asset_group.resource_name
        FROM asset_group
        WHERE campaign.id = {pmax_campaign_id}
          AND asset_group.status != 'REMOVED'
        LIMIT 1
    """
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        return row.asset_group.resource_name
    return None


def fetch_visual_assets(client, asset_group_rn: str) -> list:
    ga_svc  = client.get_service("GoogleAdsService")
    ft_enum = client.enums.AssetFieldTypeEnum
    query   = f"""
        SELECT asset_group_asset.asset, asset_group_asset.field_type
        FROM asset_group_asset
        WHERE asset_group_asset.asset_group = '{asset_group_rn}'
          AND asset_group_asset.status != 'REMOVED'
    """
    results = []
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        aga     = row.asset_group_asset
        ft_name = ft_enum(aga.field_type).name
        if ft_name in VISUAL_FIELD_TYPE_NAMES:
            results.append({"asset": aga.asset, "field_type": aga.field_type})
    return results


def copy_geo_targets(client, geo_targets: list, campaign_rn: str) -> int:
    if not geo_targets:
        print("  ⚠️  No geo targets on source — skipping")
        return 0
    svc = client.get_service("CampaignCriterionService")
    ops = []
    for gt in geo_targets:
        op = client.get_type("CampaignCriterionOperation")
        cc = op.create
        cc.campaign                     = campaign_rn
        cc.location.geo_target_constant = gt["geo_target_constant"]
        cc.negative                     = gt["negative"]
        if gt["bid_modifier"] and gt["bid_modifier"] != 1.0:
            cc.bid_modifier = gt["bid_modifier"]
        ops.append(op)
    svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f"  ✅ {len(ops)} geo target(s) copied")
    return len(ops)


def add_negative_keywords(client, campaign_rn: str) -> None:
    svc = client.get_service("CampaignCriterionService")
    me  = client.enums.KeywordMatchTypeEnum
    ops = []
    for kw_text, match in NEGATIVE_KEYWORDS:
        op = client.get_type("CampaignCriterionOperation")
        cc = op.create
        cc.campaign           = campaign_rn
        cc.negative           = True
        cc.keyword.text       = kw_text
        cc.keyword.match_type = getattr(me, match)
        ops.append(op)
    svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f"  ✅ {len(ops)} negative keywords added")


# ═══════════════════════════════════════════════════════════════════════════
# CAMPAIGN 1: SEARCH
# ═══════════════════════════════════════════════════════════════════════════

def create_search_campaign(client, budget_rn: str, source, geo_targets: list) -> str:
    print("\n── Creating Search Campaign ──")
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name            = SEARCH_NAME
    c.campaign_budget = budget_rn
    c.status          = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    c.end_date_time   = EVENT_END_DATE_TIME
    c.contains_eu_political_advertising             = 3
    c.network_settings.target_google_search          = source.network_settings.target_google_search
    c.network_settings.target_search_network         = source.network_settings.target_search_network
    c.network_settings.target_content_network        = source.network_settings.target_content_network
    c.network_settings.target_partner_search_network = source.network_settings.target_partner_search_network
    c.maximize_conversions.target_cpa_micros = 0
    result   = svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    camp_rn  = result.results[0].resource_name
    camp_id  = camp_rn.split("/")[-1]
    print(f"  ✅ Search campaign: {SEARCH_NAME}  (ID: {camp_id})")
    copy_geo_targets(client, geo_targets, camp_rn)
    add_negative_keywords(client, camp_rn)
    return camp_rn


def create_search_ad_groups(client, campaign_rn: str) -> None:
    ag_svc   = client.get_service("AdGroupService")
    ad_svc   = client.get_service("AdGroupAdService")
    crit_svc = client.get_service("AdGroupCriterionService")
    me       = client.enums.KeywordMatchTypeEnum

    for ag_data in SEARCH_AD_GROUPS:
        print(f"\n  Ad Group: {ag_data['name']}")

        ag_op = client.get_type("AdGroupOperation")
        ag    = ag_op.create
        ag.name           = ag_data["name"]
        ag.campaign       = campaign_rn
        ag.status         = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_          = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ag.cpc_bid_micros = ag_data["cpc_bid_micros"]
        ag_resp = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
        ag_rn   = ag_resp.results[0].resource_name
        print(f"    ✅ Ad group: {ag_rn.split('/')[-1]}")

        for variant in RSA_VARIANTS:
            ad_op = client.get_type("AdGroupAdOperation")
            ada   = ad_op.create
            ada.ad_group = ag_rn
            ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
            rsa          = ada.ad.responsive_search_ad
            rsa.path1    = variant["path1"]
            rsa.path2    = variant["path2"]
            ada.ad.final_urls.append(FINAL_URL)
            for hl in variant["headlines"]:
                asset      = client.get_type("AdTextAsset")
                asset.text = hl
                rsa.headlines.append(asset)
            for desc in variant["descriptions"]:
                asset      = client.get_type("AdTextAsset")
                asset.text = desc
                rsa.descriptions.append(asset)
            ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
            print(f"    ✅ RSA [{variant['label']}]: {variant['path1']}/{variant['path2']}")

        kw_ops = []
        for kw_text, match_type in ag_data["keywords"]:
            kw_op = client.get_type("AdGroupCriterionOperation")
            kw    = kw_op.create
            kw.ad_group           = ag_rn
            kw.status             = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw.keyword.text       = kw_text
            kw.keyword.match_type = getattr(me, match_type)
            kw_ops.append(kw_op)
        crit_svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=kw_ops)
        print(f"    ✅ {len(kw_ops)} phrase-match keywords added")


# ═══════════════════════════════════════════════════════════════════════════
# CAMPAIGN 2: PERFORMANCE MAX
# ═══════════════════════════════════════════════════════════════════════════

def create_pmax_campaign(client, budget_rn: str, geo_targets: list, visual_assets: list) -> str:
    print("\n── Creating Performance Max Campaign ──")
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                              = PMAX_NAME
    c.campaign_budget                   = budget_rn
    c.status                            = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type          = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    c.end_date_time                     = EVENT_END_DATE_TIME
    c.contains_eu_political_advertising = 3
    c.brand_guidelines_enabled          = False
    c.maximize_conversions.target_cpa_micros = 0
    result  = svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    camp_rn = result.results[0].resource_name
    camp_id = camp_rn.split("/")[-1]
    print(f"  ✅ P.Max campaign: {PMAX_NAME}  (ID: {camp_id})")
    copy_geo_targets(client, geo_targets, camp_rn)
    _create_pmax_asset_group(client, camp_rn, visual_assets)
    return camp_rn


def _create_pmax_asset_group(client, camp_rn: str, visual_assets: list) -> str:
    ga_svc  = client.get_service("GoogleAdsService")
    ft      = client.enums.AssetFieldTypeEnum
    ag_tmp  = f"customers/{CUSTOMER_ID}/assetGroups/-1"
    ops     = []
    lk_ops  = []
    counter = [-1]

    ag_op = client.get_type("MutateOperation")
    ag    = ag_op.asset_group_operation.create
    ag.resource_name = ag_tmp
    ag.campaign      = camp_rn
    ag.name          = "Warehouse Workers — Smyrna TN"
    ag.status        = client.enums.AssetGroupStatusEnum.ENABLED
    ag.final_urls.append(FINAL_URL)
    ops.append(ag_op)

    def add_text(text: str, field_type) -> None:
        counter[0] -= 1
        temp_rn = f"customers/{CUSTOMER_ID}/assets/{counter[0]}"
        a_op = client.get_type("MutateOperation")
        a    = a_op.asset_operation.create
        a.resource_name   = temp_rn
        a.text_asset.text = text
        ops.append(a_op)
        lop = client.get_type("MutateOperation")
        aga = lop.asset_group_asset_operation.create
        aga.asset_group = ag_tmp
        aga.asset       = temp_rn
        aga.field_type  = field_type
        lk_ops.append(lop)

    def link_existing(asset_rn: str, field_type) -> None:
        lop = client.get_type("MutateOperation")
        aga = lop.asset_group_asset_operation.create
        aga.asset_group = ag_tmp
        aga.asset       = asset_rn
        aga.field_type  = field_type
        lk_ops.append(lop)

    add_text("Indeed Flex", ft.BUSINESS_NAME)
    for h in PMAX_HEADLINES:
        add_text(h, ft.HEADLINE)
    for lh in PMAX_LONG_HEADLINES:
        add_text(lh, ft.LONG_HEADLINE)
    for d in PMAX_DESCRIPTIONS:
        add_text(d, ft.DESCRIPTION)

    ft_enum  = client.enums.AssetFieldTypeEnum
    seen_ft  = set()
    for va in visual_assets:
        ft_name = ft_enum(va["field_type"]).name
        link_existing(va["asset"], va["field_type"])
        seen_ft.add(ft_name)

    if "LOGO" not in seen_ft:
        link_existing(f"customers/{CUSTOMER_ID}/assets/56893637546", ft.LOGO)
    if "LANDSCAPE_LOGO" not in seen_ft:
        link_existing(f"customers/{CUSTOMER_ID}/assets/56894244206", ft.LANDSCAPE_LOGO)

    all_ops = ops + lk_ops
    print(f"  Batch: 1 asset group + {-counter[0] - 1} text assets + "
          f"{len(visual_assets)} BAU visual assets = {len(all_ops)} ops")
    response = ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=all_ops)

    for res in response.mutate_operation_responses:
        kind = res._pb.WhichOneof("response")
        if kind == "asset_group_result":
            rn = res.asset_group_result.resource_name
            print(f"  ✅ Asset group: {rn}")
            return rn
    raise ValueError("Asset group resource name not found in mutate response")


# ═══════════════════════════════════════════════════════════════════════════
# CAMPAIGN 3: APP (UAC)
# ═══════════════════════════════════════════════════════════════════════════

def create_app_campaign(client, budget_rn: str, source, geo_targets: list) -> str:
    print("\n── Creating App Campaign ──")
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                         = APP_NAME
    c.campaign_budget              = budget_rn
    c.status                       = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type     = client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL
    c.advertising_channel_sub_type = client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN
    c.end_date_time                = EVENT_END_DATE_TIME
    c.contains_eu_political_advertising = 3
    c.app_campaign_setting.app_id    = source.app_campaign_setting.app_id
    c.app_campaign_setting.app_store = source.app_campaign_setting.app_store
    c.app_campaign_setting.bidding_strategy_goal_type = (
        client.enums.AppCampaignBiddingStrategyGoalTypeEnum
        .OPTIMIZE_INSTALLS_WITHOUT_TARGET_INSTALL_COST
    )
    c.maximize_conversions.target_cpa_micros = 0
    result  = svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    camp_rn = result.results[0].resource_name
    camp_id = camp_rn.split("/")[-1]
    print(f"  ✅ App campaign: {APP_NAME}  (ID: {camp_id})")
    copy_geo_targets(client, geo_targets, camp_rn)

    ag_svc = client.get_service("AdGroupService")
    ad_svc = client.get_service("AdGroupAdService")

    for ag_data in APP_AD_GROUPS:
        ag_op = client.get_type("AdGroupOperation")
        ag    = ag_op.create
        ag.name     = ag_data["name"]
        ag.campaign = camp_rn
        ag.status   = client.enums.AdGroupStatusEnum.ENABLED
        ag_resp = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
        ag_rn   = ag_resp.results[0].resource_name
        print(f"\n  Ad Group: {ag_data['name']}")
        print(f"    ✅ Ad group: {ag_rn.split('/')[-1]}")

        ad_op  = client.get_type("AdGroupAdOperation")
        ada    = ad_op.create
        ada.ad_group = ag_rn
        ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
        app_ad = ada.ad.app_ad
        for h in ag_data["headlines"]:
            asset      = client.get_type("AdTextAsset")
            asset.text = h
            app_ad.headlines.append(asset)
        for d in ag_data["descriptions"]:
            asset      = client.get_type("AdTextAsset")
            asset.text = d
            app_ad.descriptions.append(asset)
        ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
        print(f"    ✅ UAC ad created")

    return camp_rn


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n═══════════════════════════════════════════════════════════════")
    print("  Ingram/Ontrac Hiring Event — Smyrna, TN — Apr 24, 2026")
    print("  Search + P.Max + App  |  $50/day each  |  ~$1,050 total")
    print("═══════════════════════════════════════════════════════════════\n")

    # ── Phase 1: Fetch BAU data ─────────────────────────────────────────
    print("── Phase 1: Fetching BAU Nashville Industrial data ──")

    source_search = fetch_campaign(client, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  ✅ BAU Search: {source_search.name}")

    source_app = fetch_campaign(client, SOURCE_APP_CAMPAIGN_ID)
    print(f"  ✅ BAU App: {source_app.name}")

    geo_targets = fetch_geo_targets(client, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  ✅ {len(geo_targets)} geo target(s) fetched from BAU Search")

    # P.Max BAU discovery
    visual_assets  = []
    pmax_source_id = SOURCE_PMAX_CAMPAIGN_ID

    if pmax_source_id == "DISCOVER":
        print("  Discovering Nashville Industrial P.Max BAU campaign...")
        pmax_source_id = discover_pmax_campaign(client) or "SKIP"

    if pmax_source_id != "SKIP":
        source_pmax = fetch_campaign(client, pmax_source_id)
        print(f"  ✅ BAU P.Max: {source_pmax.name}")
        ag_rn = fetch_pmax_asset_group(client, pmax_source_id)
        if ag_rn:
            visual_assets = fetch_visual_assets(client, ag_rn)
            print(f"  ✅ {len(visual_assets)} visual asset(s) fetched from BAU P.Max")
        else:
            print("  ⚠️  No asset group found on BAU P.Max — using account logos only")
    else:
        print("  ℹ️  No Nashville Industrial P.Max BAU found — using account logos + text only")

    # ── Phase 2: Create campaigns ───────────────────────────────────────
    print("\n── Phase 2: Creating campaigns ──")

    search_budget_rn = create_budget(client, "Search")
    search_rn        = create_search_campaign(client, search_budget_rn, source_search, geo_targets)
    create_search_ad_groups(client, search_rn)

    pmax_budget_rn = create_budget(client, "PMax")
    pmax_rn        = create_pmax_campaign(client, pmax_budget_rn, geo_targets, visual_assets)

    app_budget_rn = create_budget(client, "App")
    app_rn        = create_app_campaign(client, app_budget_rn, source_app, geo_targets)

    # ── Summary ─────────────────────────────────────────────────────────
    search_id = search_rn.split("/")[-1]
    pmax_id   = pmax_rn.split("/")[-1]
    app_id    = app_rn.split("/")[-1]

    print("\n" + "═" * 63)
    print("  ✅ ALL 3 CAMPAIGNS LIVE")
    print("═" * 63)
    print(f"  Search : {SEARCH_NAME}")
    print(f"           ID: {search_id}")
    print(f"  P.Max  : {PMAX_NAME}")
    print(f"           ID: {pmax_id}")
    print(f"  App    : {APP_NAME}")
    print(f"           ID: {app_id}")
    print()
    print("  MANUAL STEPS — Google Ads UI:")
    print("  Sitelinks (min 6):")
    print("    1. Event Details | Apr 24, 9am–3pm, Courtyard Marriott, Smyrna TN")
    print("    2. Download the App | Get the Indeed Flex app to register")
    print("    3. See Warehouse Shifts | $17.50–$18/hr — start this week")
    print("    4. Same Day Pay Info | Get paid the same or next day")
    print("    5. Benefits Overview | Health, dental, vision coverage")
    print("    6. Browse All Jobs | See all available jobs near you")
    print()
    print("  Callouts (min 4):")
    print("    - Hired on the Spot | $17.50–$18/Hr | No Long Process")
    print("    - Same Day Pay Available | $75 Referral Bonus")
    print()
    print("  Structured Snippets (min 3):")
    print("    - Job Types: Warehouse Worker, Unloader, Sorter, General Labor")
    print("    - Benefits: Same-Day Pay, Health Benefits, Flexible Scheduling")
    print("    - Shifts: 1st Shift, 2nd Shift, Weekday")
    print()
    print(f"  POST-EVENT (Apr 24 after 3pm):")
    print(f"    python3 scripts/google-ads-pause-campaigns.py \\")
    print(f"      --label 'Smyrna Industrial HE 04242026' \\")
    print(f"      --ids {search_id} {pmax_id} {app_id}")
    print("═" * 63 + "\n")


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
