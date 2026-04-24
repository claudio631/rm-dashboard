#!/usr/bin/env python3
"""
Google Ads — Tennant Solutions Hiring Event Cincinnati, OH (Apr 16, 2026)
Campaigns: Search ($50/day) + Performance Max ($50/day) + App ($50/day)
Flight:    Apr 14–16, 2026  |  Total daily: $150  |  Total: ~$450

Search : 3 ad groups × 3 RSAs = 9 RSAs total
P.Max  : 1 asset group (Picker Packer — Cincinnati) — visual assets from BAU P.Max
App    : 3 ad groups × 1 UAC ad = 3 app ads total

Run: python3 scripts/google-ads-tennant-hiring-event-apr16.py
"""

from typing import Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Source BAU campaign IDs ────────────────────────────────────────────────
SOURCE_SEARCH_CAMPAIGN_ID = "23058669077"   # p-b2c-google-search-us-bofu-bau-cincinnati-industrial--eg--
SOURCE_APP_CAMPAIGN_ID    = "23062774690"   # p-b2c-google-app-us-bofu-bau-cincinnati-industrial--eg--
# Set to known P.Max campaign ID, "DISCOVER" to query by name, or "SKIP"
SOURCE_PMAX_CAMPAIGN_ID   = "DISCOVER"

# ── Event config ────────────────────────────────────────────────────────────
DAILY_BUDGET_MICROS = 50_000_000   # $50/day
EVENT_END_DATE_TIME = "2026-04-16 23:59:59"   # account timezone
FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/497086"
    "&employer=tennant-solutions&metro=cincinnati"
    "&role=picker-packer&utm_campaign=hiring-event-tennant"
)

SEARCH_NAME = "p-b2c-google-search-us-bofu-bau-cincinnati-industrial-hiring-event-04162026"
PMAX_NAME   = "p-b2c-google-pmax-us-bofu-bau-cincinnati-industrial-hiring-event-04162026"
APP_NAME    = "p-b2c-google-app-us-bofu-bau-cincinnati-industrial-hiring-event-04162026"

# Asset field types to copy from BAU P.Max
VISUAL_FIELD_TYPE_NAMES = {
    "MARKETING_IMAGE", "SQUARE_MARKETING_IMAGE", "PORTRAIT_MARKETING_IMAGE",
    "LOGO", "LANDSCAPE_LOGO",
    # YOUTUBE_VIDEO excluded — deleted video in BAU P.Max causes API error
}

# ═══════════════════════════════════════════════════════════════════════════
# SEARCH CAMPAIGN — Ad Groups, Keywords, RSA Variants
# ═══════════════════════════════════════════════════════════════════════════

SEARCH_AD_GROUPS = [
    {
        "name": "Hiring Event — Cincinnati",
        "cpc_bid_micros": 2_500_000,
        "keywords": [
            ("hiring event cincinnati", "PHRASE"),
            ("job fair cincinnati ohio", "PHRASE"),
            ("hiring event near me", "PHRASE"),
            ("walk in job fair", "PHRASE"),
            ("warehouse hiring event", "PHRASE"),
            ("job fair near me cincinnati", "PHRASE"),
            ("warehouse job fair ohio", "PHRASE"),
            ("hiring event hamilton ohio", "PHRASE"),
            ("immediate hire warehouse cincinnati", "PHRASE"),
        ],
    },
    {
        "name": "Picker Packer Jobs — Cincinnati",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("picker packer jobs cincinnati", "PHRASE"),
            ("picker packer jobs near me", "PHRASE"),
            ("picker packer cincinnati", "PHRASE"),
            ("warehouse jobs hamilton ohio", "PHRASE"),
            ("warehouse jobs cincinnati ohio", "PHRASE"),
            ("immediate warehouse jobs cincinnati", "PHRASE"),
            ("warehouse jobs hiring now cincinnati", "PHRASE"),
            ("warehouse worker cincinnati", "PHRASE"),
            ("warehouse jobs hamilton oh", "PHRASE"),
        ],
    },
    {
        "name": "Warehouse Jobs — Hamilton OH",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("warehouse jobs near me", "PHRASE"),
            ("warehouse jobs hiring now", "PHRASE"),
            ("warehouse work cincinnati", "PHRASE"),
            ("general labor jobs cincinnati", "PHRASE"),
            ("entry level warehouse jobs cincinnati", "PHRASE"),
            ("warehouse jobs no experience", "PHRASE"),
            ("jobs hiring near me cincinnati", "PHRASE"),
        ],
    },
]

# 3 RSA variants applied to EVERY search ad group
RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Hiring-Event",
        "path2": "Cincinnati",
        "headlines": [
            "Hiring Event — April 16th",
            "Hamilton, OH · Thu Apr 16",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Register Before Spots Fill Up",
            "Get Hired Today — Apr 16",
            "Meet Recruiters Face to Face",
            "Indeed Flex Hiring Event",
            "Picker Packer Hiring Now",
            "Warehouse Work Near Cincinnati",
            "1st & 2nd Shift Available",
            "Same Day Pay Available",
            "This Thursday — Apr 16",
            "$75 Referral Bonus",
            "Limited Spots — Register Now",
        ],
        "descriptions": [
            "Join us Apr 16, 10am–2pm at 101 Knightsbridge Dr, Hamilton, OH. Get hired on the spot!",
            "No long process. Meet our recruiters & get an instant offer on April 16th. Sign up free.",
            "Walk in, interview live, and walk out with a job offer on April 16 in Hamilton, OH.",
            "Limited spots left. Register today for the Indeed Flex hiring event on April 16th, 2026.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Warehouse-Jobs",
        "path2": "Cincinnati",
        "headlines": [
            "Warehouse Jobs $14–$15/Hr",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Health & Vision Benefits",
            "Picker Packer $14–$15/Hr",
            "Full-Time Potential Available",
            "Hiring Event — April 16th",
            "Hamilton, OH · Thu Apr 16",
            "Get Paid Same Day or Next Day",
            "Health & Dental Coverage",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Long & Short-Term Work",
            "Competitive Pay + Benefits",
            "Indeed Flex Hiring Event",
        ],
        "descriptions": [
            "Picker Packer roles $14–$15/hr. Same Day Pay & health benefits. Apply now.",
            "$75 per referral, Same Day Pay & full health benefits. Join us April 16th.",
            "Competitive pay $14–$15/hr, health/dental/vision & Same Day Pay. Join us April 16th.",
            "Come to our Apr 16 hiring event. Leave with a $14–$15/hr offer + full benefits.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "path1": "Warehouse-Jobs",
        "path2": "Hamilton-OH",
        "headlines": [
            "No Long Application Process",
            "Get Hired in One Day",
            "Meet Recruiters Face to Face",
            "Start Working This Week",
            "Full-Time Potential Available",
            "Picker Packer Hiring Now",
            "Flexible 1st & 2nd Shifts",
            "Hiring Event — April 16th",
            "Hamilton, OH · Thu Apr 16",
            "Walk In, Walk Out Employed",
            "Indeed Flex Hiring Event",
            "Warehouse Jobs $14–$15/Hr",
            "Apply in Minutes on Site",
            "Same Day Pay Available",
            "This Thursday — Apr 16",
        ],
        "descriptions": [
            "Indeed Flex hiring event — walk in & leave with a job offer. 1st & 2nd shift openings.",
            "Skip the wait. Interview live with recruiters on April 16 & start working this week.",
            "Full-time opportunities available. Attend Apr 16 at 101 Knightsbridge Dr, Hamilton, OH.",
            "Picker Packer roles open now. Walk in on April 16 & leave with a job offer. No wait.",
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
    "Hiring Event — April 16th",
    "Hamilton, OH · Thu Apr 16",
    "Warehouse Jobs $14–$15/Hr",
    "Instant Job Offer on the Spot",
    "Picker Packer Hiring Now",
    "Walk In, Walk Out Employed",
    "Same Day Pay Available",
    "This Thursday — Apr 16",
    "Meet Recruiters Face to Face",
    "Indeed Flex Hiring Event",
    "Warehouse Work Near Cincinnati",
    "1st & 2nd Shift Available",
    "Get Hired Today — Apr 16",
    "$75 Referral Bonus",
    "Limited Spots — Register Now",
]

PMAX_LONG_HEADLINES = [
    "Join our April 16 hiring event in Hamilton, OH. Picker Packer $14–$15/hr.",
    "Walk in, walk out employed. Indeed Flex Picker Packer jobs near Cincinnati, OH.",
    "This Thursday only. Picker Packer hiring event April 16 in Hamilton — apply free.",
    "Same Day Pay. We're hiring Picker Packers in Hamilton, OH. Get hired on the spot Apr 16.",
    "No experience needed. 1st & 2nd shifts available. Get hired on the spot April 16.",
]

PMAX_DESCRIPTIONS = [
    "Hiring event Apr 16, 10am–2pm in Hamilton, OH. Picker Packer $14–$15/hr. Apply free!",
    "Picker Packer roles $14–$15/hr. Same Day Pay & health benefits. Apply now.",
    "Indeed Flex hiring event — walk in & leave with a job offer. 1st & 2nd shift openings.",
    "No long process. Meet our recruiters & get an instant offer on April 16th. Sign up free.",
    "$14–$15/hr warehouse roles near Cincinnati. Get hired Apr 16 — same day pay & benefits.",
]

# ═══════════════════════════════════════════════════════════════════════════
# APP CAMPAIGN — 3 Ad Groups × 1 UAC Ad
# ═══════════════════════════════════════════════════════════════════════════

APP_AD_GROUPS = [
    {
        "name": "Cincinnati HE - Urgency",
        "headlines": [
            "Download App & Attend Apr 16",
            "Hiring Event — April 16th",
            "Warehouse Jobs $14–$15/Hr",
            "Limited Spots — Register Now",
            "Get Hired at Our Live Event",
        ],
        "descriptions": [
            "Download Indeed Flex & register for our Apr 16 hiring event in Hamilton, OH.",
            "Walk in April 16, 10am–2pm. Get hired on the spot. Register via app today.",
            "Limited spots available. Download the app & register for Apr 16 event in OH.",
            "No long process. Download, sign up & attend our hiring event on April 16th.",
            "Get hired on April 16 in Hamilton, OH. Download the Indeed Flex app now.",
        ],
    },
    {
        "name": "Cincinnati HE - Pay & Benefits",
        "headlines": [
            "Warehouse Jobs $14–$15/Hr",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Picker Packer Jobs Cincinnati",
            "Health Benefits Included",
        ],
        "descriptions": [
            "Picker Packer $14–$15/hr. Same Day Pay & health benefits. Download the app.",
            "Download Indeed Flex, register for Apr 16 hiring event & earn $14–$15/hr.",
            "Same Day Pay, $75 referral & health benefits. Come to our Apr 16 event.",
            "Competitive pay + benefits. Download Indeed Flex & attend hiring event April 16.",
            "Same Day Pay, health/dental/vision. Join us Apr 16 in Hamilton, OH.",
        ],
    },
    {
        "name": "Cincinnati HE - Process",
        "headlines": [
            "Download App & Attend Apr 16",
            "Get Hired at Our Live Event",
            "Full-Time Potential Available",
            "No Long Interview Process",
            "Hiring Event — April 16th",
        ],
        "descriptions": [
            "Download Indeed Flex & come to our Apr 16 event. Walk in, get hired, start this week.",
            "Skip the wait — attend our live hiring event. Get an instant job offer on April 16.",
            "Full-time opportunities available. Download app, register & attend Apr 16 event.",
            "No lengthy process. Interview live Apr 16 in Hamilton, OH. Download Indeed Flex today.",
            "Walk in on April 16, meet our recruiters & leave with a $14–$15/hr offer. Download now.",
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
    b.name              = "Tennant Cincinnati HE " + label + " 20260416"
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
            campaign.id,
            campaign.name,
            campaign.advertising_channel_type,
            campaign.advertising_channel_sub_type,
            campaign.bidding_strategy_type,
            campaign.maximize_conversions.target_cpa_micros,
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
    """Query for a Cincinnati industrial P.Max BAU by name pattern."""
    ga_svc = client.get_service("GoogleAdsService")
    query  = """
        SELECT campaign.id, campaign.name
        FROM campaign
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND campaign.name LIKE '%cincinnati%'
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
        SELECT
            asset_group_asset.asset,
            asset_group_asset.field_type
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
    c.contains_eu_political_advertising             = 3  # DOES_NOT_CONTAIN
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

        # Create ad group
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

        # 3 RSAs — one per variant
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

        # Keywords (PHRASE match only)
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
    c.name                            = PMAX_NAME
    c.campaign_budget                 = budget_rn
    c.status                          = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type        = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    c.end_date_time                   = EVENT_END_DATE_TIME
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
    ops     = []   # asset group + text asset creates
    lk_ops  = []   # asset group asset links
    counter = [-1]

    # Asset group
    ag_op = client.get_type("MutateOperation")
    ag    = ag_op.asset_group_operation.create
    ag.resource_name = ag_tmp
    ag.campaign      = camp_rn
    ag.name          = "Picker Packer — Cincinnati"
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

    # Business name + text assets
    add_text("Indeed Flex", ft.BUSINESS_NAME)
    for h in PMAX_HEADLINES:
        add_text(h, ft.HEADLINE)
    for lh in PMAX_LONG_HEADLINES:
        add_text(lh, ft.LONG_HEADLINE)
    for d in PMAX_DESCRIPTIONS:
        add_text(d, ft.DESCRIPTION)

    # Visual assets from BAU P.Max (or fallback to account logos)
    ft_enum = client.enums.AssetFieldTypeEnum
    seen_ft = set()
    for va in visual_assets:
        ft_name = ft_enum(va["field_type"]).name
        link_existing(va["asset"], va["field_type"])
        seen_ft.add(ft_name)

    # Ensure logo assets are linked (account-level shared logos)
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
    print("  Tennant Solutions Hiring Event Cincinnati — Apr 16, 2026")
    print("  Search + P.Max + App  |  $50/day each  |  $450 total")
    print("═══════════════════════════════════════════════════════════════\n")

    # ── Phase 1: Fetch BAU data ─────────────────────────────────────────
    print("── Phase 1: Fetching BAU data ──")

    source_search = fetch_campaign(client, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  ✅ BAU Search: {source_search.name}")

    source_app = fetch_campaign(client, SOURCE_APP_CAMPAIGN_ID)
    print(f"  ✅ BAU App: {source_app.name}")

    geo_targets = fetch_geo_targets(client, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  ✅ {len(geo_targets)} geo target(s) fetched from BAU Search")

    # P.Max BAU discovery
    visual_assets   = []
    pmax_source_id  = SOURCE_PMAX_CAMPAIGN_ID

    if pmax_source_id == "DISCOVER":
        print("  Discovering Cincinnati P.Max BAU campaign...")
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
        print("  ℹ️  No Cincinnati P.Max BAU found — P.Max will use account logos + text only")

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
    print("\n" + "═" * 63)
    print("  ✅ ALL 3 CAMPAIGNS LIVE")
    print("═" * 63)
    print(f"  Search : {SEARCH_NAME}")
    print(f"           {search_rn}")
    print(f"  P.Max  : {PMAX_NAME}")
    print(f"           {pmax_rn}")
    print(f"  App    : {APP_NAME}")
    print(f"           {app_rn}")
    print()
    print("  BAU CAMPAIGNS: untouched and running")
    print()
    print("  MANUAL STEPS — Google Ads UI:")
    print("  Sitelinks (min 6):")
    print("    - Event Details | Apr 16, 10am–2pm, 101 Knightsbridge Dr, Hamilton, OH")
    print("    - Download the App | Get the Indeed Flex app to register")
    print("    - See Picker Packer Shifts | $14–$15/hr — start this week")
    print("    - Same Day Pay Info | Get paid the same or next day")
    print("    - Benefits Overview | Health, dental, vision coverage")
    print("    - Browse All Jobs | See all available jobs near you")
    print()
    print("  Callouts (min 4):")
    print("    - Hired on the Spot | $14–$15/Hr | No Experience Needed")
    print("    - Same Day Pay Available | $75 Referral Bonus")
    print()
    print("  Structured Snippets (min 3):")
    print("    - Job Types: Picker, Packer, Warehouse Worker, General Labor")
    print("    - Benefits: Same-Day Pay, Health Benefits, Flexible Scheduling")
    print("    - Shifts: 1st Shift, 2nd Shift, Weekday")
    print()
    print("  POST-EVENT (Apr 16 after 2pm):")
    print("    - Pause: Search + P.Max + App event campaigns")
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
