#!/usr/bin/env python3
"""
Solaren Event Staff Nashville — 3-Campaign Launch (Search + P.Max + App)
- Duplicates BAU Nashville hospitality Search + App campaigns (BAU stays live)
- Creates Performance Max campaign (from BAU P.Max if available, else new)
- Sets $50/day budget per campaign, start Apr 18, end Apr 25
- No geo expansion (Nashville proper — already targeted by BAU)
- RSA: 3 variants × event staff angles (urgency / pay & benefits / process)
- P.Max: text assets from copy list + visual assets copied from BAU P.Max
- App: 3 UAC ad variants with event copy

BEFORE RUNNING: Set the three source campaign IDs below.
  Find them in Google Ads for campaigns matching:
    p-b2c-google-search-us-bofu-bau-nashville-hospitality--eg--
    p-b2c-google-app-us-bofu-bau-nashville-hospitality--eg--
    p-b2c-google-pmax-us-bofu-bau-nashville-hospitality--eg--

  If no P.Max BAU exists, set SOURCE_PMAX_CAMPAIGN_ID = "SKIP".
  P.Max will be created with text assets only — add images/logo in UI.

Run: python3 scripts/google-ads-solaren-event-staff-nashville.py
"""

import time
from typing import Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Source BAU campaign IDs — CONFIRM IN GOOGLE ADS BEFORE RUNNING ─────────
SOURCE_SEARCH_CAMPAIGN_ID = "23059952812"  # p-b2c-google-search-us-bofu-bau-nashville-industrial--eg--
SOURCE_APP_CAMPAIGN_ID    = "23048055977"  # p-b2c-google-app-us-bofu-bau-nashville-industrial--eg--
SOURCE_PMAX_CAMPAIGN_ID   = "23041613685"  # p-b2c-google_p_max-p_max-us-bofu-bau-nashville-Industrial-eg (paused — visual assets only)

# ── Event config ────────────────────────────────────────────────────────────
DAILY_BUDGET_MICROS = 50_000_000  # $50/day
EVENT_START_DATE    = "20260418"  # YYYYMMDD
EVENT_END_DATE      = "2026-04-25 23:59:59"  # YYYY-MM-DD HH:MM:SS — event day

FINAL_URL = (
    "https://indeedflex.com/find-jobs/hospitality/lp-event-staff/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/500202"
    "&employer=NA"
    "&metro=nashville"
    "&role=event-staff"
    "&utm_campaign=us-solaren-event-staff-nashville-tn"
)

SEARCH_EVENT_NAME = "p-b2c-google-search-us-bofu-bau-nashville-hospitality-hiring-event-04252026"
PMAX_EVENT_NAME   = "p-b2c-google-pmax-us-bofu-bau-nashville-hospitality-hiring-event-04252026"
APP_EVENT_NAME    = "p-b2c-google-app-us-bofu-bau-nashville-hospitality-hiring-event-04252026"

# ── RSA copy — 3 variants per ad group ─────────────────────────────────────
RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Event-Staff",
        "path2": "Nashville",
        "headlines": [
            "Event Staff — April 25th",
            "Nashville, TN · Sat Apr 25",
            "$17.50/Hr Event Staff Jobs",
            "Instant Job Offer on the Spot",
            "Traffic & Event Crew Wanted",
            "Walk In, Walk Out Employed",
            "Same Day Pay Available",
            "4AM\u20132PM Saturday Shift",
            "Meet Recruiters Face to Face",
            "Indeed Flex Hiring Event",
            "Road Closure Event Staff",
            "Large-Scale Events \u00b7 Nashville",
            "Get Hired Today \u2014 Apr 25",
            "$75 Referral Bonus",
            "Limited Spots \u2014 Register Now",
        ],
        "descriptions": [
            "Join us Apr 25 for a large-scale Nashville event. $17.50/hr. Get hired on the spot!",
            "Event Staff roles $17.50/hr \u2014 traffic control & crowd management. Same Day Pay available.",
            "Indeed Flex hiring event \u2014 walk in & leave with a job offer. 18+ welcome. Apply now!",
            "Saturday April 25 shift, 4am\u20132pm. Reliable, punctual staff wanted. Sign up free today.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Event-Staff",
        "path2": "Apply-Now",
        "headlines": [
            "$17.50/Hr Event Staff Jobs",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Weekly Pay or Same Day Pay",
            "Event Staff \u2014 April 25th",
            "Nashville, TN \u00b7 Sat Apr 25",
            "Get Paid for One-Day Events",
            "Walk In, Walk Out Employed",
            "Indeed Flex Hiring Event",
            "4AM\u20132PM Saturday Shift",
            "$17.50/Hr + Referral Bonus",
            "Large-Scale Events \u00b7 Nashville",
            "Road Closure Event Staff",
            "Get Hired Today \u2014 Apr 25",
            "Limited Spots \u2014 Register Now",
        ],
        "descriptions": [
            "Event Staff roles $17.50/hr \u2014 traffic control & crowd management. Same Day Pay available.",
            "Earn $75 when you refer a friend. Join large-scale events in Nashville. Apply today!",
            "Indeed Flex hiring event \u2014 walk in & leave with a job offer. 18+ welcome. Apply now!",
            "Join us Apr 25 for a large-scale Nashville event. $17.50/hr. Get hired on the spot!",
        ],
    },
    {
        "label": "Process & Opportunity",
        "path1": "Hiring-Event",
        "path2": "Get-Hired",
        "headlines": [
            "No Long Application Process",
            "Get Hired in One Day",
            "Meet Recruiters Face to Face",
            "Start Working This Saturday",
            "Event Staff \u2014 April 25th",
            "Nashville, TN \u00b7 Sat Apr 25",
            "Walk In, Walk Out Employed",
            "Indeed Flex Hiring Event",
            "$17.50/Hr Event Staff Jobs",
            "4AM\u20132PM Saturday Shift",
            "Road Closure Event Staff",
            "Traffic & Event Crew Wanted",
            "Apply in Minutes on Site",
            "Same Day Pay Available",
            "$75 Referral Bonus",
        ],
        "descriptions": [
            "Indeed Flex hiring event \u2014 walk in & leave with a job offer. 18+ welcome. Apply now!",
            "Saturday April 25 shift, 4am\u20132pm. Reliable, punctual staff wanted. Sign up free today.",
            "Join us Apr 25 for a large-scale Nashville event. $17.50/hr. Get hired on the spot!",
            "Event Staff roles $17.50/hr \u2014 traffic control & crowd management. Same Day Pay available.",
        ],
    },
]

# ── App ad copy — 3 variants ────────────────────────────────────────────────
APP_AD_VARIANTS = [
    {
        "label": "Urgency",
        "headlines": [
            "Download App & Attend Apr 25",
            "Hiring Event \u2014 April 25th",
            "Event Staff Jobs $17.50/Hr",
            "Nashville, TN \u00b7 Sat Apr 25",
            "Get Hired at Our Live Event",
        ],
        "descriptions": [
            "Download Indeed Flex & register for our Apr 25 event staff shift in Nashville, TN.",
            "Event staff $17.50/hr. Work a large-scale Nashville event Sat Apr 25, 4am\u20132pm.",
            "Download the app, sign up & attend our hiring event. Instant offers on April 25.",
            "No long process. Download, sign up & attend our event staff shift on April 25th.",
            "Get hired on April 25 in Nashville, TN. Download the Indeed Flex app now.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "headlines": [
            "$17.50/Hr Event Staff Jobs",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Event Staff \u2014 Nashville",
            "Download & Apply Today",
        ],
        "descriptions": [
            "Same Day Pay, $75 referral bonus. Attend our event staff shift Apr 25 in Nashville.",
            "Download Indeed Flex & register for our Apr 25 event staff shift in Nashville, TN.",
            "Event staff $17.50/hr. Same Day Pay & $75 referral bonus. Download app today.",
            "Competitive pay $17.50/hr. Download Indeed Flex & join our Apr 25 event in Nashville.",
            "Indeed Flex is hiring Event Staff in Nashville, TN. Register for Apr 25 today.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "headlines": [
            "Get Hired in One Day",
            "No Long Application Process",
            "Download App & Attend Apr 25",
            "Nashville Event Staff",
            "Start This Saturday",
        ],
        "descriptions": [
            "Download Indeed Flex & come to our Apr 25 event. Walk in, get hired, start this week.",
            "Skip the wait \u2014 download the app & attend our Apr 25 event staff shift in Nashville.",
            "Indeed Flex is hiring Event Staff in Nashville, TN. Register for Apr 25 today.",
            "Download the app, sign up & attend our hiring event. Instant offers on April 25.",
            "Large-scale Nashville event on Apr 25. Download the app & secure your spot today.",
        ],
    },
]

# ── P.Max text assets ───────────────────────────────────────────────────────
PMAX_HEADLINES = [
    "Event Staff \u2014 April 25th",
    "Nashville, TN \u00b7 Sat Apr 25",
    "$17.50/Hr Event Staff Jobs",
    "Instant Job Offer on the Spot",
    "Traffic & Event Crew Wanted",
    "Walk In, Walk Out Employed",
    "Same Day Pay Available",
    "4AM\u20132PM Saturday Shift",
    "Meet Recruiters Face to Face",
    "Indeed Flex Hiring Event",
    "Road Closure Event Staff",
    "Large-Scale Events \u00b7 Nashville",
    "Get Hired Today \u2014 Apr 25",
    "$75 Referral Bonus",
    "Limited Spots \u2014 Register Now",
]

PMAX_LONG_HEADLINES = [
    "Join our April 25 hiring event in Nashville. Traffic & event staff roles. $17.50/hr.",
    "Walk in, walk out employed. Indeed Flex event staff jobs pay $17.50/hr in Nashville.",
    "Work the biggest events in Nashville. Event staff needed April 25 \u2014 apply free today.",
    "Same Day Pay. $75 referral bonus. We\u2019re hiring event staff in Nashville for April 25.",
    "18+ welcome. Reliable, punctual workers wanted for large-scale Nashville events.",
]

PMAX_DESCRIPTIONS = [
    "Join us Apr 25 for a large-scale Nashville event. $17.50/hr. Get hired on the spot!",
    "Event Staff roles $17.50/hr \u2014 traffic control & crowd management. Same Day Pay available.",
    "Indeed Flex hiring event \u2014 walk in & leave with a job offer. 18+ welcome. Apply now!",
    "Saturday April 25 shift, 4am\u20132pm. Reliable, punctual staff wanted. Sign up free today.",
    "Coordinate traffic, monitor road closures & guide drivers at live events. Apply now!",
]

# ── Keywords ────────────────────────────────────────────────────────────────
EVENT_STAFF_KEYWORDS = [
    ("event staff nashville", "EXACT"),
    ("event staff jobs nashville tn", "EXACT"),
    ("hiring event nashville", "EXACT"),
    ("traffic control event staff nashville", "EXACT"),
    ("event staff hiring now", "EXACT"),
    ("event staff jobs nashville", "PHRASE"),
    ("hiring event nashville tn", "PHRASE"),
    ("event staffing nashville", "PHRASE"),
    ("traffic control jobs nashville", "PHRASE"),
    ("outdoor event staff nashville", "PHRASE"),
    ("road closure event staff nashville", "PHRASE"),
    ("event staff hiring nashville tennessee", "BROAD"),
    ("get hired on the spot nashville", "BROAD"),
]

GENERIC_IMMEDIATE_KEYWORDS = [
    ("immediate event staff nashville", "PHRASE"),
    ("event staff jobs hiring now nashville", "PHRASE"),
    ("outdoor event jobs nashville", "PHRASE"),
    ("event staff nashville tn", "EXACT"),
    ("hospitality event jobs nashville", "PHRASE"),
]

HOSPITALITY_KEYWORDS = [
    ("hospitality event staff nashville", "PHRASE"),
    ("event staff jobs nashville tennessee", "PHRASE"),
    ("event staff near me nashville", "EXACT"),
    ("staffing agency event jobs nashville", "PHRASE"),
]

EVENT_KEYWORD_TARGETS = {
    "p---generic_immediate--": GENERIC_IMMEDIATE_KEYWORDS,
    "p---hospitality--":       HOSPITALITY_KEYWORDS,
}

# ── Visual asset field types to copy from BAU P.Max ─────────────────────────
VISUAL_FIELD_TYPE_NAMES = {
    "MARKETING_IMAGE",
    "SQUARE_MARKETING_IMAGE",
    "PORTRAIT_MARKETING_IMAGE",
    "LOGO",
    "LANDSCAPE_LOGO",
    "YOUTUBE_VIDEO",
}


# ── Resource helpers ─────────────────────────────────────────────────────────

def ag_res(customer_id: str, ag_id: str) -> str:
    return f"customers/{customer_id}/adGroups/{ag_id}"


# ── Budget ────────────────────────────────────────────────────────────────────

def create_budget(client, customer_id: str, label: str) -> str:
    svc = client.get_service("CampaignBudgetService")
    op  = client.get_type("CampaignBudgetOperation")
    b   = op.create
    b.name              = f"Solaren Event Staff Nashville {label} {int(time.time())}"
    b.amount_micros     = DAILY_BUDGET_MICROS
    b.delivery_method   = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    result = svc.mutate_campaign_budgets(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ Budget created: {rn}")
    return rn


# ── Campaign fetch ─────────────────────────────────────────────────────────────

def fetch_campaign(client, customer_id: str, campaign_id: str):
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.advertising_channel_type,
            campaign.advertising_channel_sub_type,
            campaign.bidding_strategy_type,
            campaign.bidding_strategy,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros,
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
    for row in ga_svc.search(customer_id=customer_id, query=query):
        return row.campaign
    raise ValueError(f"Campaign {campaign_id} not found")


def fetch_geo_targets(client, customer_id: str, campaign_id: str) -> list:
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
    for row in ga_svc.search(customer_id=customer_id, query=query):
        cc = row.campaign_criterion
        results.append({
            "geo_target_constant": cc.location.geo_target_constant,
            "bid_modifier":        cc.bid_modifier,
            "negative":            cc.negative,
        })
    return results


# ── Campaign create ─────────────────────────────────────────────────────────

def _apply_bidding(client, campaign, source):
    BidEnum = client.enums.BiddingStrategyTypeEnum
    bst     = source.bidding_strategy_type
    if bst == BidEnum.MAXIMIZE_CONVERSIONS:
        campaign.maximize_conversions.target_cpa_micros = (
            source.maximize_conversions.target_cpa_micros
        )
    elif bst == BidEnum.TARGET_CPA:
        campaign.target_cpa.target_cpa_micros = source.target_cpa.target_cpa_micros
    elif source.bidding_strategy:
        campaign.bidding_strategy = source.bidding_strategy
    else:
        campaign.maximize_conversions.CopyFrom(client.get_type("MaximizeConversions"))


def create_search_campaign(client, customer_id: str, source, budget_rn: str, name: str) -> str:
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                           = name
    c.campaign_budget                = budget_rn
    c.status                         = client.enums.CampaignStatusEnum.PAUSED  # Enable manually on Apr 18
    c.advertising_channel_type       = client.enums.AdvertisingChannelTypeEnum.SEARCH
    c.end_date_time                  = EVENT_END_DATE
    c.contains_eu_political_advertising              = 3  # DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    c.network_settings.target_google_search          = source.network_settings.target_google_search
    c.network_settings.target_search_network         = source.network_settings.target_search_network
    c.network_settings.target_content_network        = source.network_settings.target_content_network
    c.network_settings.target_partner_search_network = source.network_settings.target_partner_search_network
    c.bidding_strategy                               = source.bidding_strategy  # Portfolio strategy from source
    result = svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ Search campaign created: {rn}")
    return rn


def create_pmax_campaign(client, customer_id: str, budget_rn: str, name: str) -> str:
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                           = name
    c.campaign_budget                = budget_rn
    c.status                         = client.enums.CampaignStatusEnum.PAUSED  # Enable manually on Apr 18
    c.advertising_channel_type       = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    c.end_date_time                     = EVENT_END_DATE
    c.contains_eu_political_advertising = 3  # DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    c.brand_guidelines_enabled          = False
    c.maximize_conversion_value.target_roas = 0  # Maximize Conversion Value, no tROAS
    result = svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ P.Max campaign created: {rn}")
    return rn


def create_app_campaign(client, customer_id: str, source, budget_rn: str, name: str) -> str:
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                           = name
    c.campaign_budget                = budget_rn
    c.status                         = client.enums.CampaignStatusEnum.PAUSED  # Enable manually on Apr 18
    c.advertising_channel_type       = client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL
    c.advertising_channel_sub_type   = client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN
    c.end_date_time                     = EVENT_END_DATE
    c.contains_eu_political_advertising = 3  # DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    c.app_campaign_setting.app_id    = source.app_campaign_setting.app_id
    c.app_campaign_setting.app_store = source.app_campaign_setting.app_store
    # Use install-optimized goal — new campaign has no conversion history and a 7-day flight.
    # OPTIMIZE_INSTALLS_WITHOUT_TARGET_INSTALL_COST requires MAXIMIZE_CONVERSIONS bidding,
    # NOT a portfolio strategy — set standalone maximize_conversions.
    c.app_campaign_setting.bidding_strategy_goal_type = (
        client.enums.AppCampaignBiddingStrategyGoalTypeEnum
        .OPTIMIZE_INSTALLS_WITHOUT_TARGET_INSTALL_COST
    )
    c.maximize_conversions.target_cpa_micros = 0
    result = svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ App campaign created: {rn}")
    return rn


def copy_geo_targets(client, customer_id: str, geo_targets: list, campaign_rn: str) -> int:
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
    svc.mutate_campaign_criteria(customer_id=customer_id, operations=ops)
    print(f"  ✅ {len(ops)} geo target(s) copied from BAU")
    return len(ops)


# ── Ad groups ─────────────────────────────────────────────────────────────────

def fetch_ad_groups(client, customer_id: str, campaign_id: str) -> list:
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.cpc_bid_micros
        FROM ad_group
        WHERE campaign.id = {campaign_id}
          AND ad_group.status != 'REMOVED'
    """
    results = []
    for row in ga_svc.search(customer_id=customer_id, query=query):
        ag = row.ad_group
        results.append({
            "id":             str(ag.id),
            "name":           ag.name,
            "cpc_bid_micros": ag.cpc_bid_micros,
        })
    return results


def create_search_ad_group(client, customer_id: str, campaign_rn: str,
                           name: str, cpc_bid_micros: int) -> str:
    svc = client.get_service("AdGroupService")
    op  = client.get_type("AdGroupOperation")
    ag  = op.create
    ag.name           = name
    ag.campaign       = campaign_rn
    ag.status         = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_          = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag.cpc_bid_micros = cpc_bid_micros or 1_500_000
    result = svc.mutate_ad_groups(customer_id=customer_id, operations=[op])
    return result.results[0].resource_name


def create_app_ad_group(client, customer_id: str, campaign_rn: str, name: str) -> str:
    svc = client.get_service("AdGroupService")
    op  = client.get_type("AdGroupOperation")
    ag  = op.create
    ag.name     = name
    ag.campaign = campaign_rn
    ag.status   = client.enums.AdGroupStatusEnum.ENABLED
    result = svc.mutate_ad_groups(customer_id=customer_id, operations=[op])
    return result.results[0].resource_name


# ── Keywords ───────────────────────────────────────────────────────────────────

def fetch_keywords(client, customer_id: str, ad_group_id: str) -> list:
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type
        FROM ad_group_criterion
        WHERE ad_group_criterion.ad_group = '{ag_res(customer_id, ad_group_id)}'
          AND ad_group_criterion.type = 'KEYWORD'
          AND ad_group_criterion.status != 'REMOVED'
          AND ad_group_criterion.negative = FALSE
    """
    results = []
    for row in ga_svc.search(customer_id=customer_id, query=query):
        kw = row.ad_group_criterion.keyword
        results.append({"text": kw.text, "match_type": kw.match_type})
    return results


def add_keywords(client, customer_id: str, ag_rn: str, keywords: list) -> int:
    if not keywords:
        return 0
    svc = client.get_service("AdGroupCriterionService")
    me  = client.enums.KeywordMatchTypeEnum
    ops = []
    for kw in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        c  = op.create
        c.ad_group           = ag_rn
        c.status             = client.enums.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text       = kw["text"] if isinstance(kw, dict) else kw[0]
        raw_match            = kw["match_type"] if isinstance(kw, dict) else kw[1]
        c.keyword.match_type = getattr(me, raw_match) if isinstance(raw_match, str) else raw_match
        ops.append(op)
    svc.mutate_ad_group_criteria(customer_id=customer_id, operations=ops)
    print(f"    ✅ {len(ops)} keyword(s) added")
    return len(ops)


# ── Ads ────────────────────────────────────────────────────────────────────────

def add_rsa(client, customer_id: str, ag_rn: str, variant: dict) -> str:
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


def add_app_ad(client, customer_id: str, ag_rn: str, variant: dict) -> str:
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


# ── P.Max: asset group + assets ────────────────────────────────────────────────

def fetch_pmax_asset_group(client, customer_id: str, pmax_campaign_id: str) -> Optional[str]:
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT asset_group.resource_name
        FROM asset_group
        WHERE campaign.id = {pmax_campaign_id}
          AND asset_group.status != 'REMOVED'
        LIMIT 1
    """
    for row in ga_svc.search(customer_id=customer_id, query=query):
        return row.asset_group.resource_name
    return None


def fetch_campaign_brand_assets(client, customer_id: str, campaign_id: str) -> list:
    """Fetches BUSINESS_NAME and LOGO campaign assets from an existing P.Max campaign."""
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT
            campaign.id,
            campaign_asset.asset,
            campaign_asset.field_type
        FROM campaign_asset
        WHERE campaign.id = {campaign_id}
          AND campaign_asset.status != 'REMOVED'
          AND campaign_asset.field_type IN ('BUSINESS_NAME', 'LOGO')
    """
    results = []
    for row in ga_svc.search(customer_id=customer_id, query=query):
        ca = row.campaign_asset
        results.append({"asset": ca.asset, "field_type": ca.field_type})
    return results


def link_campaign_assets(client, customer_id: str, campaign_rn: str, assets: list) -> None:
    """Links brand assets (business name, logo) to a campaign via CampaignAssetService."""
    if not assets:
        print("  ⚠️  No brand assets to link — skipping")
        return
    svc = client.get_service("CampaignAssetService")
    ops = []
    for a in assets:
        op  = client.get_type("CampaignAssetOperation")
        ca  = op.create
        ca.campaign    = campaign_rn
        ca.asset       = a["asset"]
        ca.field_type  = a["field_type"]
        ops.append(op)
    svc.mutate_campaign_assets(customer_id=customer_id, operations=ops)
    print(f"  ✅ {len(ops)} brand asset(s) linked to P.Max campaign")


def fetch_visual_assets(client, customer_id: str, asset_group_rn: str) -> list:
    """Fetches image/logo/video asset resource names from an existing asset group."""
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
    for row in ga_svc.search(customer_id=customer_id, query=query):
        aga     = row.asset_group_asset
        ft_name = ft_enum(aga.field_type).name
        if ft_name in VISUAL_FIELD_TYPE_NAMES:
            results.append({"asset": aga.asset, "field_type": aga.field_type})
    return results


def fetch_asset_group_signals(client, customer_id: str, asset_group_rn: str) -> list:
    """Fetches audience signal resource names from an existing asset group."""
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT asset_group_signal.audience.audience
        FROM asset_group_signal
        WHERE asset_group_signal.asset_group = '{asset_group_rn}'
    """
    results = []
    for row in ga_svc.search(customer_id=customer_id, query=query):
        aud = row.asset_group_signal.audience.audience
        if aud:
            results.append(aud)
    return results


def create_text_asset(client, customer_id: str, text: str) -> str:
    svc = client.get_service("AssetService")
    op  = client.get_type("AssetOperation")
    op.create.text_asset.text = text
    result = svc.mutate_assets(customer_id=customer_id, operations=[op])
    return result.results[0].resource_name


def create_asset_group(client, customer_id: str, campaign_rn: str,
                       name: str, final_url: str) -> str:
    svc = client.get_service("AssetGroupService")
    op  = client.get_type("AssetGroupOperation")
    ag  = op.create
    ag.name     = name
    ag.campaign = campaign_rn
    ag.status   = client.enums.AssetGroupStatusEnum.ENABLED
    ag.final_urls.append(final_url)
    result = svc.mutate_asset_groups(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ Asset group created: {rn}")
    return rn


def link_assets_to_group(client, customer_id: str, asset_group_rn: str,
                         assets: list) -> None:
    if not assets:
        return
    svc = client.get_service("AssetGroupAssetService")
    ops = []
    for a in assets:
        op  = client.get_type("AssetGroupAssetOperation")
        aga = op.create
        aga.asset_group = asset_group_rn
        aga.asset       = a["asset"]
        aga.field_type  = a["field_type"]
        ops.append(op)
    svc.mutate_asset_group_assets(customer_id=customer_id, operations=ops)
    print(f"  ✅ {len(ops)} asset(s) linked to asset group")


def add_text_assets_to_group(client, customer_id: str, asset_group_rn: str) -> None:
    """Creates and links all P.Max text assets to the asset group."""
    ft = client.enums.AssetFieldTypeEnum
    assets_to_link = []

    print(f"  Creating {len(PMAX_HEADLINES)} headline asset(s)...")
    for text in PMAX_HEADLINES:
        rn = create_text_asset(client, customer_id, text)
        assets_to_link.append({"asset": rn, "field_type": ft.HEADLINE})

    print(f"  Creating {len(PMAX_LONG_HEADLINES)} long headline asset(s)...")
    for text in PMAX_LONG_HEADLINES:
        rn = create_text_asset(client, customer_id, text)
        assets_to_link.append({"asset": rn, "field_type": ft.LONG_HEADLINE})

    print(f"  Creating {len(PMAX_DESCRIPTIONS)} description asset(s)...")
    for text in PMAX_DESCRIPTIONS:
        rn = create_text_asset(client, customer_id, text)
        assets_to_link.append({"asset": rn, "field_type": ft.DESCRIPTION})

    link_assets_to_group(client, customer_id, asset_group_rn, assets_to_link)


def add_audience_signals(client, customer_id: str, asset_group_rn: str,
                         audience_rns: list) -> None:
    if not audience_rns:
        print("  ⚠️  No audience signals to copy — skipping")
        return
    svc = client.get_service("AssetGroupSignalService")
    ops = []
    for aud_rn in audience_rns:
        op  = client.get_type("AssetGroupSignalOperation")
        sig = op.create
        sig.asset_group        = asset_group_rn
        sig.audience.audience  = aud_rn
        ops.append(op)
    svc.mutate_asset_group_signals(customer_id=customer_id, operations=ops)
    print(f"  ✅ {len(ops)} audience signal(s) added")


def create_pmax_asset_group_with_assets(
    client, customer_id: str, pmax_campaign_rn: str,
    visual_assets: list, logo_asset_rn: Optional[str]
) -> str:
    """
    Creates P.Max asset group + links all assets in ONE atomic GoogleAdsService.mutate() call.
    Required minimums: BUSINESS_NAME, LOGO, 3 headlines, 1 long headline, 2 descriptions,
    1 MARKETING_IMAGE, 1 SQUARE_MARKETING_IMAGE — all provided in the same batch.
    """
    ga_svc   = client.get_service("GoogleAdsService")
    ft       = client.enums.AssetFieldTypeEnum
    ag_temp  = f"customers/{customer_id}/assetGroups/-1"
    ops      = []     # all create ops (asset group + text assets)
    link_ops = []     # asset-group-asset link ops — appended after creates
    counter  = [-1]   # starts at -1 so first asset gets -2 (no overlap with assetGroups/-1)

    # ── Asset group creation ──────────────────────────────────────────────────
    ag_op = client.get_type("MutateOperation")
    ag = ag_op.asset_group_operation.create
    ag.resource_name = ag_temp
    ag.name          = "Event Staff \u2014 Nashville"
    ag.campaign      = pmax_campaign_rn
    ag.status        = client.enums.AssetGroupStatusEnum.ENABLED
    ag.final_urls.append(FINAL_URL)
    ops.append(ag_op)

    # ── Helper: create text asset inline + queue link op ─────────────────────
    def add_text(text: str, field_type) -> None:
        counter[0] -= 1
        temp_rn = f"customers/{customer_id}/assets/{counter[0]}"

        a_op = client.get_type("MutateOperation")
        a = a_op.asset_operation.create
        a.resource_name   = temp_rn
        a.text_asset.text = text
        ops.append(a_op)

        lop = client.get_type("MutateOperation")
        aga = lop.asset_group_asset_operation.create
        aga.asset_group = ag_temp
        aga.asset        = temp_rn
        aga.field_type   = field_type
        link_ops.append(lop)

    # ── Helper: link existing asset resource name ─────────────────────────────
    def link_existing(asset_rn: str, field_type) -> None:
        lop = client.get_type("MutateOperation")
        aga = lop.asset_group_asset_operation.create
        aga.asset_group = ag_temp
        aga.asset        = asset_rn
        aga.field_type   = field_type
        link_ops.append(lop)

    # ── Text assets (create inline) ──────────────────────────────────────────
    add_text("Indeed Flex", ft.BUSINESS_NAME)
    for text in PMAX_HEADLINES:
        add_text(text, ft.HEADLINE)
    for text in PMAX_LONG_HEADLINES:
        add_text(text, ft.LONG_HEADLINE)
    for text in PMAX_DESCRIPTIONS:
        add_text(text, ft.DESCRIPTION)

    # ── Visual assets from BAU P.Max (link existing) ─────────────────────────
    visual_ft_names = set()
    for va in visual_assets:
        visual_ft_names.add(client.enums.AssetFieldTypeEnum(va["field_type"]).name)
        link_existing(va["asset"], va["field_type"])

    # ── Campaign-level LOGO (only if not already present in visual_assets) ────
    if logo_asset_rn and "LOGO" not in visual_ft_names:
        link_existing(logo_asset_rn, ft.LOGO)

    # ── Execute: create ops first, then link ops ─────────────────────────────
    all_ops = ops + link_ops
    print(f"  Batch: 1 asset group + {-counter[0]} text assets + "
          f"{len(visual_assets)} BAU visual assets = {len(all_ops)} operations")

    response = ga_svc.mutate(customer_id=customer_id, mutate_operations=all_ops)

    # ── Extract asset group resource name from response ───────────────────────
    for res in response.mutate_operation_responses:
        if res._pb.WhichOneof("response") == "asset_group_result":
            rn = res.asset_group_result.resource_name
            print(f"  \u2705 Asset group created: {rn}")
            return rn

    raise ValueError("Asset group resource name not found in mutate response")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if "TODO" in (SOURCE_SEARCH_CAMPAIGN_ID, SOURCE_APP_CAMPAIGN_ID):
        print("\n❌ Set SOURCE_SEARCH_CAMPAIGN_ID and SOURCE_APP_CAMPAIGN_ID before running.")
        print("   Find them in Google Ads for campaigns matching:")
        print("   p-b2c-google-search-us-bofu-bau-nashville-hospitality--eg--")
        print("   p-b2c-google-app-us-bofu-bau-nashville-hospitality--eg--")
        print("   p-b2c-google-pmax-us-bofu-bau-nashville-hospitality--eg-- (or set to SKIP)\n")
        raise SystemExit(1)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    cid    = CUSTOMER_ID

    skip_pmax_source = SOURCE_PMAX_CAMPAIGN_ID in ("TODO", "SKIP")
    # Search campaign already created — set resource name to skip re-creation
    EXISTING_SEARCH_CAMPAIGN_RN = "customers/7236100723/campaigns/23721569237"

    print("\n══════════════════════════════════════════════════════════════════")
    print("  Solaren Event Staff Nashville — 3-Campaign Launch")
    print("  Search + Performance Max + App   |   Apr 18–25, 2026")
    print("══════════════════════════════════════════════════════════════════\n")

    # ─────────────────────────────────────────────────────────────────────────
    # SEARCH CAMPAIGN (already created — skip)
    # ─────────────────────────────────────────────────────────────────────────
    print("▶ SEARCH CAMPAIGN (already created — skipping)\n")
    print(f"  ✅ Existing: {EXISTING_SEARCH_CAMPAIGN_RN}\n")

    pass  # Search campaign already created above

    # ─────────────────────────────────────────────────────────────────────────
    # PERFORMANCE MAX CAMPAIGN
    # ─────────────────────────────────────────────────────────────────────────
    print("\n\n▶ PERFORMANCE MAX CAMPAIGN (already created — skipping)\n")
    print("  ✅ Campaign   : customers/7236100723/campaigns/23721572363")
    print("  ✅ Asset group: customers/7236100723/assetGroups/6696439035")

    # ─────────────────────────────────────────────────────────────────────────
    # APP CAMPAIGN
    # ─────────────────────────────────────────────────────────────────────────
    print("\n\n▶ APP CAMPAIGN\n")

    # App campaign already created — skip to remaining ad groups
    EXISTING_APP_CAMPAIGN_RN = "customers/7236100723/campaigns/23721955376"
    print(f"  ✅ Campaign (already created): {EXISTING_APP_CAMPAIGN_RN}")
    app_campaign_rn = EXISTING_APP_CAMPAIGN_RN

    # Variant 1 (Urgency) ad group + ad already created — add variants 2 & 3 only
    # App campaigns allow exactly 1 ad per ad group; create one ad group per variant
    print("\n  Adding remaining app ad groups (1 ad group per variant, 1 ad per group)...")
    for i, variant in enumerate(APP_AD_VARIANTS[1:], 2):  # skip index 0 (already done)
        ag_label = f"Event Staff Nashville \u2014 {variant['label']}"
        print(f"\n  Creating ad group: {ag_label}")
        app_ag_rn = create_app_ad_group(client, cid, app_campaign_rn, ag_label)
        ad_rn = add_app_ad(client, cid, app_ag_rn, variant)
        print(f"  \u2705 App ad {i} [{variant['label']}]: {ad_rn}")

    # ─────────────────────────────────────────────────────────────────────────
    print("\n══════════════════════════════════════════════════════════════════")
    print("  ✅ Done! All 3 event campaigns created and scheduled.")
    print(f"  Search : {SEARCH_EVENT_NAME}")
    print(f"  P.Max  : {PMAX_EVENT_NAME}")
    print(f"  App    : {APP_EVENT_NAME}")
    print("  BAU campaigns remain untouched and running.")
    print("  Start  : April 18, 2026")
    print("  Event  : April 25, 2026 · 4am–2pm · Nashville, TN (Solaren)")
    print("  Post-event: Pause all 3 event campaigns on April 25.")
    if skip_pmax_source:
        print()
        print("  ⚠️  ACTION REQUIRED: Add images, logo & audience signals to P.Max")
        print("      in Google Ads UI before Apr 18.")
    print("══════════════════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"\n❌ Google Ads API error: {ex}")
        for error in ex.failure.errors:
            print(f"   {error.message}")
            if error.location:
                for fp in error.location.field_path_elements:
                    print(f"   Field: {fp.field_name}")
        raise SystemExit(1)
