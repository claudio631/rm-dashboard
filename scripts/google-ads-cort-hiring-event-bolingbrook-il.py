#!/usr/bin/env python3
"""
Google Ads — CORT Hiring Event Bolingbrook, IL (Apr 23, 2026)
Campaigns: Search ($50/day) + Performance Max ($50/day) + App ($50/day)
Flight:    Apr 15–23, 2026  |  Total daily: $150  |  Total: ~$1,350

Search : 3 ad groups × 3 RSAs = 9 RSAs total
P.Max  : 1 asset group (Warehouse Operative — Bolingbrook IL) — visual assets from BAU P.Max
App    : 3 ad groups × 1 UAC ad = 3 app ads total
Ext    : 6 sitelinks + 6 callouts + 3 structured snippets — added inline after campaign creation

BAU discovery:
  - Chicago BAU Search/P.Max/App auto-discovered by name pattern (%chicago% + %industrial%)
  - App fallback: Nashville BAU App (ID: 23062774690 — same app_id com.syftapp.android)
  - Geo fallback: GeoTargetConstantService lookup for Bolingbrook + Chicago if no BAU Search geo found

Brief: squads/recruitment-marketing-flex/data/hiring-events/google-ads-cort-hiring-event-bolingbrook-il.md

Run: python3 scripts/google-ads-cort-hiring-event-bolingbrook-il.py
"""

from typing import Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Fallback BAU IDs ──────────────────────────────────────────────────────────
FALLBACK_APP_CAMPAIGN_ID = "23062774690"  # Nashville BAU App — same app settings

# ── Event config ──────────────────────────────────────────────────────────────
DAILY_BUDGET_MICROS = 50_000_000   # $50/day
EVENT_END_DATE_TIME = "2026-04-23 23:59:59"   # CT account timezone

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/503583"
    "&employer=cort&metro=chicago&role=warehouse-operative"
    "&utm_campaign=cort-warehouse-operative-hiring-event"
)

BROWSE_JOBS_URL = "https://indeedflex.com/find-jobs/?search&area_name=Chicago+IL"
INDEEDFLEX_URL  = "https://indeedflex.com/"

SEARCH_NAME = "p-b2c-google-search-us-bofu-bau-chicago-industrial-hiring-event-04232026"
PMAX_NAME   = "p-b2c-google-pmax-us-bofu-bau-chicago-industrial-hiring-event-04232026"
APP_NAME    = "p-b2c-google-app-us-bofu-bau-chicago-industrial-hiring-event-04232026"

VISUAL_FIELD_TYPE_NAMES = {
    "MARKETING_IMAGE", "SQUARE_MARKETING_IMAGE", "PORTRAIT_MARKETING_IMAGE",
    "LOGO", "LANDSCAPE_LOGO",
}


# ═══════════════════════════════════════════════════════════════════════════════
# SEARCH — Ad Groups, Keywords, RSA Variants
# ═══════════════════════════════════════════════════════════════════════════════

SEARCH_AD_GROUPS = [
    {
        "name": "Hiring Event — Bolingbrook IL",
        "cpc_bid_micros": 2_500_000,
        "keywords": [
            ("hiring event near me", "PHRASE"),
            ("job fair chicago", "PHRASE"),
            ("hiring event bolingbrook il", "PHRASE"),
            ("walk in hiring event near me", "PHRASE"),
            ("job fair near me", "PHRASE"),
            ("hiring event april 2026", "PHRASE"),
            ("walk in hiring chicago", "PHRASE"),
            ("hiring event illinois", "PHRASE"),
            ("get hired on the spot chicago", "PHRASE"),
            ("job fair bolingbrook", "PHRASE"),
        ],
    },
    {
        "name": "Warehouse Operative Jobs — Chicago",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("warehouse operative jobs chicago", "PHRASE"),
            ("warehouse jobs bolingbrook il", "PHRASE"),
            ("loader jobs chicago", "PHRASE"),
            ("warehouse operative near me", "PHRASE"),
            ("warehouse jobs hiring now chicago", "PHRASE"),
            ("loader crew jobs chicago", "PHRASE"),
            ("warehouse jobs no experience", "PHRASE"),
            ("mover jobs chicago", "PHRASE"),
            ("entry level warehouse chicago", "PHRASE"),
        ],
    },
    {
        "name": "General Jobs — Chicago IL",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("jobs near me bolingbrook il", "PHRASE"),
            ("jobs hiring now chicago", "PHRASE"),
            ("entry level jobs bolingbrook", "PHRASE"),
            ("manual labor jobs chicago", "PHRASE"),
            ("warehouse jobs near me", "PHRASE"),
            ("jobs hiring today chicago", "PHRASE"),
            ("entry level jobs near me", "PHRASE"),
        ],
    },
]

# 3 RSA variants — applied to EVERY search ad group (= 9 RSAs total)
RSA_VARIANTS = [
    {
        "label":    "Urgency",
        "path1":    "Hiring-Event",
        "path2":    "Bolingbrook-IL",
        "headlines": [
            "Hiring Event Apr 23",
            "Bolingbrook IL Wed Apr 23",
            "Walk In Walk Out Employed",
            "Get Hired on the Spot",
            "Indeed Flex Hiring Event",
            "Warehouse Jobs Hiring Now",
            "Limited Spots Register Now",
            "9AM to 3PM April 23",
            "Meet Recruiters In Person",
            "Start Working This Week",
            "Same Day Pay Available",
            "Free Event Register Today",
            "Loader Crew Jobs Chicago",
            "No Experience Needed",
            "Get a Job Offer Apr 23",
        ],
        "descriptions": [
            "Hiring event Apr 23, 9am-3pm in Bolingbrook, IL. Warehouse roles. Get hired on the spot!",
            "Walk in, meet recruiters & leave with a job offer on Apr 23. Free event — register today.",
            "Same Day Pay, $75 referral bonus. Indeed Flex hiring event Apr 23. No experience needed!",
            "Limited spots. Come to Residence Inn Bolingbrook Apr 23. Apply in minutes — register free.",
        ],
    },
    {
        "label":    "Pay & Benefits",
        "path1":    "Warehouse-Jobs",
        "path2":    "Bolingbrook-IL",
        "headlines": [
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "No Experience Needed",
            "Warehouse Jobs Hiring Now",
            "Hiring Event Apr 23",
            "Bolingbrook IL Wed Apr 23",
            "Flexible Shifts Available",
            "Get Hired on the Spot",
            "Loader Crew Jobs Chicago",
            "No Resume Required",
            "Start Working This Week",
            "Benefits and Same Day Pay",
            "Indeed Flex Hiring Event",
            "Meet Recruiters Apr 23",
            "Warehouse Work Near Chicago",
        ],
        "descriptions": [
            "Warehouse jobs with Same Day Pay & $75 referral bonus. Come to our Apr 23 event. Apply!",
            "Get paid the same day you work. $75 referral bonus. Indeed Flex hiring event Apr 23.",
            "Same Day Pay, flexible shifts & $75 referral. Join us Apr 23 in Bolingbrook, IL.",
            "Warehouse jobs with great benefits. Come Apr 23 & walk out with a job offer today.",
        ],
    },
    {
        "label":    "Process & Opportunity",
        "path1":    "Warehouse-Jobs",
        "path2":    "Chicago-IL",
        "headlines": [
            "No Long Application Process",
            "Get Hired in One Day",
            "Meet Recruiters Face to Face",
            "Start Working This Week",
            "No Experience Needed",
            "Flexible Shifts Available",
            "Hiring Event Apr 23",
            "Bolingbrook IL Apr 23",
            "Walk In Walk Out Employed",
            "Indeed Flex Hiring Event",
            "Apply in Minutes on Site",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Loader Crew Jobs Chicago",
            "Warehouse Work Near Chicago",
        ],
        "descriptions": [
            "Indeed Flex hiring event: walk in & leave with a job offer. Flexible shifts, same day pay.",
            "Skip the wait. Interview live Apr 23 & start working this week. Register free today.",
            "No experience needed. Attend Apr 23 at Residence Inn, Bolingbrook. Apply in 2 minutes.",
            "Loader/Crew roles. Walk in on Apr 23 & leave with a job offer. No long process needed.",
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


# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE MAX — Text Assets
# ═══════════════════════════════════════════════════════════════════════════════

PMAX_HEADLINES = [
    "Hiring Event Apr 23",
    "Bolingbrook IL Wed Apr 23",
    "Walk In Walk Out Employed",
    "Get Hired on the Spot",
    "Warehouse Jobs Hiring Now",
    "Same Day Pay Available",
    "9AM to 3PM April 23",
    "Meet Recruiters In Person",
    "Indeed Flex Hiring Event",
    "No Experience Needed",
    "Start Working This Week",
    "Loader Crew Jobs Chicago",
    "Free Event Register Now",
    "Limited Spots Available",
    "$75 Referral Bonus",
]

PMAX_LONG_HEADLINES = [
    "Join our Apr 23 hiring event in Bolingbrook, IL. Warehouse Operative jobs — apply free!",
    "Walk in, walk out employed. Indeed Flex warehouse jobs near Chicago, IL. Apr 23 event.",
    "One day only. Warehouse Operative hiring event Apr 23 in Bolingbrook, IL — apply free.",
    "Same Day Pay. We're hiring Warehouse Operatives in Bolingbrook, IL. Get hired Apr 23.",
    "No experience needed. Flexible shifts available. Get hired on the spot April 23, 2026.",
]

PMAX_DESCRIPTIONS = [
    "Hiring event Apr 23, 9am-3pm in Bolingbrook, IL. Warehouse roles. Get hired on the spot!",
    "Warehouse jobs with Same Day Pay & $75 referral. Come to our Apr 23 event. Apply free.",
    "Walk in & leave with a job offer. Flexible shifts & same day pay. Register for Apr 23.",
    "No experience needed. Meet recruiters on Apr 23 & get an instant offer. Register free.",
    "Loader/Crew roles near Chicago. $75 referral bonus, Same Day Pay. Get hired April 23.",
]


# ═══════════════════════════════════════════════════════════════════════════════
# APP — 3 Ad Groups × 1 UAC Ad
# ═══════════════════════════════════════════════════════════════════════════════

APP_AD_GROUPS = [
    {
        "name": "Bolingbrook HE - Urgency",
        "headlines": [
            "Download App & Attend Apr 23",
            "Hiring Event Apr 23",
            "Warehouse Jobs Chicago IL",
            "Limited Spots Register Now",
            "Get Hired at Our Live Event",
        ],
        "descriptions": [
            "Download Indeed Flex & register for our Apr 23 hiring event in Bolingbrook, IL.",
            "Walk in Apr 23, 9am-3pm. Get hired on the spot. Register via the app today.",
            "Limited spots available. Download the app & register for Apr 23 event in IL.",
            "No long process. Download, sign up & attend our hiring event on April 23rd.",
            "Get hired on April 23 in Bolingbrook, IL. Download the Indeed Flex app now.",
        ],
    },
    {
        "name": "Bolingbrook HE - Pay & Benefits",
        "headlines": [
            "Warehouse Jobs Chicago IL",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Loader Crew Jobs Chicago",
            "No Experience Needed",
        ],
        "descriptions": [
            "Same Day Pay & $75 referral bonus. Download the app. Attend hiring event Apr 23.",
            "Download Indeed Flex, register for Apr 23 hiring event & earn same day pay.",
            "Same Day Pay, $75 referral & flexible shifts. Come to our Apr 23 event.",
            "Great benefits. Download Indeed Flex & attend hiring event April 23 in IL.",
            "Same Day Pay, $75 referral bonus. Join us Apr 23 in Bolingbrook, IL.",
        ],
    },
    {
        "name": "Bolingbrook HE - Process",
        "headlines": [
            "Download App & Attend Apr 23",
            "Get Hired at Our Live Event",
            "No Long Interview Process",
            "Start Working This Week",
            "Hiring Event Apr 23",
        ],
        "descriptions": [
            "Download Indeed Flex & come to our Apr 23 event. Walk in, get hired, start this week.",
            "Skip the wait. Attend our live hiring event Apr 23 in Bolingbrook, IL. Get hired fast.",
            "No experience needed. Download app, register & attend our Apr 23 hiring event.",
            "No lengthy process. Interview live Apr 23 in Bolingbrook, IL. Download Indeed Flex today.",
            "Walk in on April 23, meet our recruiters & leave with a job offer. Download now.",
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# EXTENSIONS — Sitelinks, Callouts, Structured Snippets
# ═══════════════════════════════════════════════════════════════════════════════

SITELINKS = [
    {
        "link_text":    "Event Details",
        "description1": "Apr 23, 9am-3pm in Bolingbrook, IL",
        "description2": "Residence Inn, Bolingbrook IL 60440",
        "final_url":    FINAL_URL,
    },
    {
        "link_text":    "Download the App",
        "description1": "Get the Indeed Flex app",
        "description2": "Register for the hiring event",
        "final_url":    INDEEDFLEX_URL,
    },
    {
        "link_text":    "Warehouse Jobs Chicago",
        "description1": "Loader/Crew roles hiring now",
        "description2": "Apply now, start this week",
        "final_url":    FINAL_URL,
    },
    {
        "link_text":    "Same Day Pay",
        "description1": "Get paid the same day you work",
        "description2": "Work for Indeed Flex",
        "final_url":    INDEEDFLEX_URL,
    },
    {
        "link_text":    "Referral Bonus",
        "description1": "$75 per successful referral",
        "description2": "Terms apply",
        "final_url":    INDEEDFLEX_URL,
    },
    {
        "link_text":    "Browse Jobs Chicago",
        "description1": "See all jobs near you",
        "description2": "No resume needed — apply today",
        "final_url":    BROWSE_JOBS_URL,
    },
]

CALLOUTS = [
    "Hired on the Spot",
    "No Experience Needed",
    "Same Day Pay Available",
    "$75 Referral Bonus",
    "Flexible Shifts",
    "Free Hiring Event",
]

STRUCTURED_SNIPPETS = [
    {
        "header": "Types",
        "values": ["Warehouse Operative", "Loader", "Crew Member", "Event Setup"],
    },
    {
        "header": "Amenities",
        "values": ["Same-Day Pay", "Flexible Scheduling", "$75 Referral Bonus", "No Experience Needed"],
    },
    {
        "header": "Service catalog",
        "values": ["9AM-3PM Apr 23", "Wednesday Apr 23", "Bolingbrook IL"],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# BAU DISCOVERY
# ═══════════════════════════════════════════════════════════════════════════════

def discover_bau_search(client) -> Optional[str]:
    ga_svc = client.get_service("GoogleAdsService")
    query  = """
        SELECT campaign.id, campaign.name, campaign.status
        FROM campaign
        WHERE campaign.advertising_channel_type = 'SEARCH'
          AND campaign.name LIKE '%chicago%'
          AND campaign.name LIKE '%industrial%'
          AND campaign.status != 'REMOVED'
        LIMIT 5
    """
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        c = row.campaign
        print(f"  Found BAU Search: {c.name}  (ID: {c.id})")
        return str(c.id)
    return None


def discover_bau_pmax(client) -> Optional[str]:
    ga_svc = client.get_service("GoogleAdsService")
    query  = """
        SELECT campaign.id, campaign.name
        FROM campaign
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND campaign.name LIKE '%chicago%'
          AND campaign.status != 'REMOVED'
        LIMIT 5
    """
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        c = row.campaign
        print(f"  Found BAU P.Max: {c.name}  (ID: {c.id})")
        return str(c.id)
    return None


def discover_bau_app(client) -> Optional[str]:
    ga_svc = client.get_service("GoogleAdsService")
    query  = """
        SELECT campaign.id, campaign.name
        FROM campaign
        WHERE campaign.advertising_channel_type = 'MULTI_CHANNEL'
          AND campaign.name LIKE '%chicago%'
          AND campaign.status != 'REMOVED'
        LIMIT 5
    """
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        c = row.campaign
        print(f"  Found BAU App: {c.name}  (ID: {c.id})")
        return str(c.id)
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def create_budget(client, label: str) -> str:
    svc = client.get_service("CampaignBudgetService")
    op  = client.get_type("CampaignBudgetOperation")
    b   = op.create
    b.name              = f"CORT Bolingbrook HE {label} 20260423"
    b.amount_micros     = DAILY_BUDGET_MICROS
    b.delivery_method   = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    result = svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[op])
    rn     = result.results[0].resource_name
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
        print("  ⚠️  No geo targets from BAU — add Bolingbrook/Chicago manually in Google Ads UI")
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


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 1: SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

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
    c.contains_eu_political_advertising = 3  # DOES_NOT_CONTAIN
    c.maximize_conversions.target_cpa_micros = 0
    # Copy network settings from BAU Search if available, otherwise use Search defaults
    search_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    if source and source.advertising_channel_type == search_type:
        c.network_settings.target_google_search          = source.network_settings.target_google_search
        c.network_settings.target_search_network         = source.network_settings.target_search_network
        c.network_settings.target_content_network        = source.network_settings.target_content_network
        c.network_settings.target_partner_search_network = source.network_settings.target_partner_search_network
    else:
        c.network_settings.target_google_search          = True
        c.network_settings.target_search_network         = False
        c.network_settings.target_content_network        = False
        c.network_settings.target_partner_search_network = False
    result  = svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    camp_rn = result.results[0].resource_name
    camp_id = camp_rn.split("/")[-1]
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

        # 3 RSA variants per ad group
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

        # PHRASE-match keywords only
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


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 2: PERFORMANCE MAX
# ═══════════════════════════════════════════════════════════════════════════════

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
    c.contains_eu_political_advertising  = 3
    c.brand_guidelines_enabled           = False
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

    # Asset group
    ag_op = client.get_type("MutateOperation")
    ag    = ag_op.asset_group_operation.create
    ag.resource_name = ag_tmp
    ag.campaign      = camp_rn
    ag.name          = "Warehouse Operative — Bolingbrook IL"
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

    # Text assets
    add_text("Indeed Flex", ft.BUSINESS_NAME)
    for h in PMAX_HEADLINES:
        add_text(h, ft.HEADLINE)
    for lh in PMAX_LONG_HEADLINES:
        add_text(lh, ft.LONG_HEADLINE)
    for d in PMAX_DESCRIPTIONS:
        add_text(d, ft.DESCRIPTION)

    # Visual assets from BAU P.Max
    ft_enum = client.enums.AssetFieldTypeEnum
    seen_ft = set()
    for va in visual_assets:
        ft_name = ft_enum(va["field_type"]).name
        link_existing(va["asset"], va["field_type"])
        seen_ft.add(ft_name)

    # Ensure account logos are linked
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


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 3: APP (UAC)
# ═══════════════════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════════════════
# EXTENSIONS — Sitelinks, Callouts, Structured Snippets
# ═══════════════════════════════════════════════════════════════════════════════

def _create_sitelink_asset(client, sitelink: dict) -> str:
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    sl    = asset.sitelink_asset
    sl.link_text    = sitelink["link_text"]
    sl.description1 = sitelink["description1"]
    sl.description2 = sitelink["description2"]
    asset.final_urls.append(sitelink["final_url"])
    return svc.mutate_assets(customer_id=CUSTOMER_ID, operations=[op]).results[0].resource_name


def _create_callout_asset(client, text: str) -> str:
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    asset.callout_asset.callout_text = text
    return svc.mutate_assets(customer_id=CUSTOMER_ID, operations=[op]).results[0].resource_name


def _create_snippet_asset(client, snippet: dict) -> str:
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    ss    = asset.structured_snippet_asset
    ss.header = snippet["header"]
    for v in snippet["values"]:
        ss.values.append(v)
    return svc.mutate_assets(customer_id=CUSTOMER_ID, operations=[op]).results[0].resource_name


def _link_asset_to_campaign(client, asset_rn: str, campaign_rn: str, field_type_name: str) -> None:
    svc = client.get_service("CampaignAssetService")
    op  = client.get_type("CampaignAssetOperation")
    ca  = op.create
    ca.asset      = asset_rn
    ca.campaign   = campaign_rn
    ca.field_type = getattr(client.enums.AssetFieldTypeEnum, field_type_name)
    svc.mutate_campaign_assets(customer_id=CUSTOMER_ID, operations=[op])


def add_extensions(client, all_campaign_rns: list) -> None:
    print("\n── Adding Extensions ──")

    # Sitelinks
    sl_rns = []
    for sl in SITELINKS:
        rn = _create_sitelink_asset(client, sl)
        sl_rns.append(rn)
    print(f"  ✅ {len(sl_rns)} sitelink assets created")

    # Callouts
    co_rns = []
    for text in CALLOUTS:
        rn = _create_callout_asset(client, text)
        co_rns.append(rn)
    print(f"  ✅ {len(co_rns)} callout assets created")

    # Structured snippets
    ss_rns = []
    for snippet in STRUCTURED_SNIPPETS:
        rn = _create_snippet_asset(client, snippet)
        ss_rns.append(rn)
    print(f"  ✅ {len(ss_rns)} structured snippet assets created")

    # Link to all campaigns
    for camp_rn in all_campaign_rns:
        for rn in sl_rns:
            _link_asset_to_campaign(client, rn, camp_rn, "SITELINK")
        for rn in co_rns:
            _link_asset_to_campaign(client, rn, camp_rn, "CALLOUT")
        for rn in ss_rns:
            _link_asset_to_campaign(client, rn, camp_rn, "STRUCTURED_SNIPPET")
        print(f"  ✅ Extensions linked to: {camp_rn.split('/')[-1]}")

    print(f"  ✅ {len(sl_rns)} sitelinks + {len(co_rns)} callouts + "
          f"{len(ss_rns)} snippets → {len(all_campaign_rns)} campaigns")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n═══════════════════════════════════════════════════════════════════")
    print("  CORT Hiring Event — Bolingbrook, IL — Apr 23, 2026")
    print("  Search + P.Max + App  |  $50/day each  |  $1,350 total")
    print("═══════════════════════════════════════════════════════════════════\n")

    # ── Phase 1: Discover BAU campaigns ──────────────────────────────────────
    print("── Phase 1: Discovering Chicago BAU campaigns ──")

    bau_search_id = discover_bau_search(client)
    bau_app_id    = discover_bau_app(client)
    bau_pmax_id   = discover_bau_pmax(client)

    if bau_search_id:
        source_search = fetch_campaign(client, bau_search_id)
        print(f"  ✅ BAU Search: {source_search.name}")
        geo_targets = fetch_geo_targets(client, bau_search_id)
        print(f"  ✅ {len(geo_targets)} geo target(s) fetched from BAU Search")
    else:
        print("  ⚠️  No Chicago BAU Search found — using default network settings")
        print("  ⚠️  Geo targets: add Bolingbrook, IL manually in Google Ads UI after launch")
        # Fetch any search campaign for network settings
        source_search = fetch_campaign(client, FALLBACK_APP_CAMPAIGN_ID)
        # Override network_settings to Search defaults
        source_search.network_settings.target_google_search  = True
        source_search.network_settings.target_search_network = False
        source_search.network_settings.target_content_network = False
        source_search.network_settings.target_partner_search_network = False
        geo_targets = []

    if bau_app_id:
        source_app = fetch_campaign(client, bau_app_id)
        print(f"  ✅ BAU App: {source_app.name}")
    else:
        print(f"  ℹ️  No Chicago BAU App found — using Nashville fallback ({FALLBACK_APP_CAMPAIGN_ID})")
        source_app = fetch_campaign(client, FALLBACK_APP_CAMPAIGN_ID)
        print(f"  ✅ Fallback App: {source_app.name}")

    visual_assets = []
    if bau_pmax_id:
        source_pmax = fetch_campaign(client, bau_pmax_id)
        print(f"  ✅ BAU P.Max: {source_pmax.name}")
        ag_rn = fetch_pmax_asset_group(client, bau_pmax_id)
        if ag_rn:
            visual_assets = fetch_visual_assets(client, ag_rn)
            print(f"  ✅ {len(visual_assets)} visual asset(s) fetched from BAU P.Max")
        else:
            print("  ⚠️  No asset group on BAU P.Max — using account logos only")
    else:
        print("  ℹ️  No Chicago BAU P.Max found — P.Max will use account logos + text only")

    # ── Phase 2: Create campaigns ─────────────────────────────────────────────
    print("\n── Phase 2: Creating campaigns ──")

    search_budget_rn = create_budget(client, "Search")
    search_rn        = create_search_campaign(client, search_budget_rn, source_search, geo_targets)
    create_search_ad_groups(client, search_rn)

    pmax_budget_rn = create_budget(client, "PMax")
    pmax_rn        = create_pmax_campaign(client, pmax_budget_rn, geo_targets, visual_assets)

    app_budget_rn = create_budget(client, "App")
    app_rn        = create_app_campaign(client, app_budget_rn, source_app, geo_targets)

    # ── Phase 3: Add extensions ───────────────────────────────────────────────
    add_extensions(client, [search_rn, pmax_rn, app_rn])

    # ── Summary ───────────────────────────────────────────────────────────────
    search_id = search_rn.split("/")[-1]
    pmax_id   = pmax_rn.split("/")[-1]
    app_id    = app_rn.split("/")[-1]

    print("\n" + "═" * 67)
    print("  ✅ ALL 3 CAMPAIGNS LIVE")
    print("═" * 67)
    print(f"  Search : {SEARCH_NAME}")
    print(f"           ID: {search_id}")
    print(f"  P.Max  : {PMAX_NAME}")
    print(f"           ID: {pmax_id}")
    print(f"  App    : {APP_NAME}")
    print(f"           ID: {app_id}")
    print()
    print("  BAU CAMPAIGNS: untouched and running")
    print()
    if not bau_search_id or not geo_targets:
        print("  ⚠️  MANUAL: Add Bolingbrook, IL + Chicago metro geo targets via Google Ads UI")
        print()
    print("  POST-EVENT (Apr 23 after 3pm):")
    print(f"    Pause: Search ({search_id}) + P.Max ({pmax_id}) + App ({app_id})")
    print("═" * 67 + "\n")


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
