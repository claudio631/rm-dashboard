#!/usr/bin/env python3
"""
Google Ads — CORT Hiring Event Orlando, FL
4 Campaigns: Search ($50) + Display ($30) + Performance Max ($50) + App ($50)
Flight: Apr 14–21, 2026  |  Total daily: $180  |  Total: ~$1,440

BAU Budget Reduction (runs before campaign creation):
  Finds active BAU Orlando industrial campaigns and reduces budgets to 50%.
  RESTORE on Apr 22: restore budgets and pause event campaigns.

BEFORE RUNNING — set the three source BAU campaign IDs below:
  Find them in Google Ads > Campaigns matching:
    p-b2c-google-search-us-bofu-bau-orlando-industrial--eg--
    p-b2c-google-pmax-us-bofu-bau-orlando-industrial--eg--   (or SKIP)
    p-b2c-google-app-us-bofu-bau-orlando-industrial--eg--

Run: python3 scripts/google-ads-cort-hiring-event-orlando-fl.py
"""

import time
from typing import Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Source BAU campaign IDs ──────────────────────────────────────────────────
SOURCE_SEARCH_CAMPAIGN_ID = "22987289513"   # p-b2c-google-search-us-bofu-bau-orlando---eg-- (PAUSED $5 — used for geo targets)
SOURCE_PMAX_CAMPAIGN_ID   = "23021275670"   # p-b2c-google-p_max-us-bofu-bau-orlando-industrial-eg (PAUSED $5)
SOURCE_APP_CAMPAIGN_ID    = "23369869887"   # p-b2c-google-app-us-bofu-bau-orlando-industrial-eg (ENABLED $50)

# ── Active BAU campaigns to reduce during event flight ───────────────────────
# Only reduce ENABLED campaigns; PAUSED BAU campaigns are left untouched
BAU_TO_REDUCE = {
    "23052892689": "p-b2c-google-display-us-rmk-bau-orlando-industrial--eg--",  # ENABLED $30 → $15
    "23369869887": "p-b2c-google-app-us-bofu-bau-orlando-industrial-eg",         # ENABLED $50 → $25
}

# ── Event budgets ─────────────────────────────────────────────────────────────
SEARCH_BUDGET_MICROS  = 50_000_000   # $50/day
PMAX_BUDGET_MICROS    = 50_000_000   # $50/day
DISPLAY_BUDGET_MICROS = 30_000_000   # $30/day
APP_BUDGET_MICROS     = 50_000_000   # $50/day

EVENT_END_DATE_TIME = "2026-04-21 23:59:59"   # campaigns auto-stop; enable manually Apr 14

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/501764"
    "&employer=cort&metro=orlando&role=loader--crew"
    "&utm_campaign=us-cort-hiring-event-orlando-fl"
)

SEARCH_NAME  = "p-b2c-google-search-us-bofu-bau-orlando-industrial-hiring-event-04202026"
PMAX_NAME    = "p-b2c-google-pmax-us-bofu-bau-orlando-industrial-hiring-event-04202026"
DISPLAY_NAME = "p-b2c-google-display-us-bofu-bau-orlando-industrial-hiring-event-04202026"
APP_NAME     = "p-b2c-google-app-us-bofu-bau-orlando-industrial-hiring-event-04202026"

# ── Visual asset field types to copy from BAU P.Max ──────────────────────────
VISUAL_FIELD_TYPE_NAMES = {
    "MARKETING_IMAGE", "SQUARE_MARKETING_IMAGE", "PORTRAIT_MARKETING_IMAGE",
    "LOGO", "LANDSCAPE_LOGO", "YOUTUBE_VIDEO",
}

# ── Keywords by ad group ──────────────────────────────────────────────────────
AD_GROUPS = {
    "AG1 - Hiring Event": {
        "cpc_bid_micros": 2_500_000,
        "keywords": [
            ("hiring event near me", "PHRASE"),
            ("job fair orlando", "PHRASE"),
            ("hiring event orlando fl", "PHRASE"),
            ("walk in hiring event near me", "PHRASE"),
            ("hiring event april 2026", "PHRASE"),
            ("job fair near me today", "PHRASE"),
            ("get hired on the spot orlando", "PHRASE"),
            ("walk in hiring", "PHRASE"),
            ("hiring event this weekend", "PHRASE"),
            ("hiring event florida", "PHRASE"),
        ],
        "rsa": {
            "path1": "hiring-event",
            "path2": "orlando-fl",
            "headlines": [
                ("Two-Day Hiring Event", 1),
                ("Apr 20-21 Orlando FL", 2),
                ("$16.50/Hr Loader Jobs", None),
                ("Get Hired on the Spot", None),
                ("Loader/Crew Jobs Orlando", None),
                ("Walk In Walk Out Employed", None),
                ("Same Day Pay Available", None),
                ("9AM-2PM Both Days", None),
                ("Meet Recruiters In Person", None),
                ("Indeed Flex Hiring Event", None),
                ("No Experience Needed", None),
                ("Start Working This Week", None),
                ("Furniture & Event Crew", None),
                ("Register Now Free Event", None),
                ("Limited Spots Available", None),
            ],
            "descriptions": [
                "Hiring event Apr 20-21, 9am-2pm in Orlando. Loader jobs $16.50/hr. Get hired on the spot!",
                "CORT hiring event Apr 20-21. Loader/Crew $16.50/hr. Same Day Pay. Register free today!",
                "Loader/Crew jobs $16.50/hr near Orlando Airport. Walk in and get hired. Register free!",
                "Two-day event, no experience needed. Come either day, 9am-2pm. Apply in under 2 minutes!",
            ],
        },
    },
    "AG2 - Loader Crew Jobs": {
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("loader jobs orlando fl", "PHRASE"),
            ("crew jobs orlando", "PHRASE"),
            ("loader jobs near me", "PHRASE"),
            ("furniture mover jobs orlando", "PHRASE"),
            ("loader jobs hiring now", "PHRASE"),
            ("warehouse loader jobs orlando fl", "PHRASE"),
            ("loader crew jobs florida", "PHRASE"),
            ("crew jobs near me", "PHRASE"),
            ("loader jobs no experience", "PHRASE"),
            ("mover jobs orlando fl", "PHRASE"),
        ],
        "rsa": {
            "path1": "loader-jobs",
            "path2": "orlando-fl",
            "headlines": [
                ("Loader/Crew Jobs Orlando", 1),
                ("$16.50/Hr Loader Jobs", 2),
                ("Two-Day Hiring Event", None),
                ("No Experience Needed", None),
                ("Get Hired on the Spot", None),
                ("Same Day Pay Available", None),
                ("Furniture & Event Crew", None),
                ("Walk In Walk Out Employed", None),
                ("Orlando Airport Area Jobs", None),
                ("Hiring Event Apr 20-21", None),
                ("Start Working This Week", None),
                ("Entry Level Loader Jobs", None),
                ("Meet Recruiters In Person", None),
                ("Indeed Flex Is Hiring", None),
                ("Apply Today Start Monday", None),
            ],
            "descriptions": [
                "Loader/Crew jobs in Orlando FL. $16.50/hr, Same Day Pay, no experience needed. Apply now!",
                "Walk-in hiring event Apr 20-21 at Courtyard Orlando Airport. Get hired on the spot. Free!",
                "Load and unload furniture for CORT events. $16.50/hr. Active, physical work. Apply today.",
                "Two-day hiring event. Come either day, 9am-2pm. Loader/Crew roles. Register in 2 minutes.",
            ],
        },
    },
    "AG3 - General Jobs": {
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("jobs near me orlando fl", "PHRASE"),
            ("jobs hiring now orlando", "PHRASE"),
            ("entry level jobs orlando", "PHRASE"),
            ("jobs near 32812", "PHRASE"),
            ("manual labor jobs orlando", "PHRASE"),
            ("jobs near me orlando", "PHRASE"),
            ("entry level jobs near me", "PHRASE"),
        ],
        "rsa": {
            "path1": "jobs-hiring",
            "path2": "orlando-fl",
            "headlines": [
                ("Jobs Hiring Now Orlando FL", 1),
                ("$16.50/Hr Pay", 2),
                ("Hiring Event Apr 20-21", None),
                ("No Experience Required", None),
                ("Get Hired on the Spot", None),
                ("Orlando Airport Area Jobs", None),
                ("Two-Day Hiring Event", None),
                ("Walk In Hiring Event", None),
                ("Start Working This Week", None),
                ("Entry Level No Exp Needed", None),
                ("Same Day Pay Available", None),
                ("Jobs Near 32812", None),
                ("Loader Jobs Orlando FL", None),
                ("Free Hiring Event Apr 20", None),
                ("Indeed Flex Is Hiring", None),
            ],
            "descriptions": [
                "Jobs hiring now in Orlando FL. $16.50/hr. No experience needed. Hiring event Apr 20-21!",
                "Hiring event at Courtyard Orlando Airport. Walk in, get hired same day. Apply free today.",
                "Entry-level jobs near Orlando Airport. Good pay, flexible shifts. Start working this week.",
                "Two-day hiring event Apr 20-21, 9am-2pm. Physical work, great pay. Register in 2 minutes.",
            ],
        },
    },
}

# ── Negative keywords (campaign level) ───────────────────────────────────────
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
    ("indeed", "EXACT"),
    ("cort careers", "PHRASE"),
    ("amazon", "EXACT"),
    ("ups", "EXACT"),
    ("fedex", "EXACT"),
    ("driver", "PHRASE"),
    ("internship", "PHRASE"),
    ("volunteer", "PHRASE"),
    ("resume tips", "PHRASE"),
    ("interview tips", "PHRASE"),
]

# ── P.Max text assets ─────────────────────────────────────────────────────────
PMAX_HEADLINES = [
    "Two-Day Hiring Event",
    "Apr 20-21 Orlando FL",
    "$16.50/Hr Loader Jobs",
    "Get Hired on the Spot",
    "Loader/Crew Jobs Orlando",
    "Walk In Walk Out Employed",
    "Same Day Pay Available",
    "9AM-2PM Both Days",
    "Meet Recruiters In Person",
    "Indeed Flex Hiring Event",
    "No Experience Needed",
    "Start Working This Week",
    "Furniture & Event Crew",
    "Register Now Free Event",
    "Limited Spots Available",
]

PMAX_LONG_HEADLINES = [
    "Join our April 20-21 hiring event in Orlando. Loader/Crew $16.50/hr.",
    "Walk in, walk out employed. Indeed Flex loader jobs pay $16.50/hr in Orlando, FL.",
    "Work for CORT as a Loader/Crew. Two-day hiring event April 20-21 in Orlando, FL.",
    "Same Day Pay. We're hiring Loader/Crew for CORT in Orlando, FL. Event Apr 20-21.",
    "No experience needed. Reliable loaders wanted for CORT in Orlando. Get hired April 20-21.",
]

PMAX_DESCRIPTIONS = [
    "Hiring event Apr 20-21, 9am-2pm in Orlando. Loader jobs $16.50/hr. Get hired on the spot!",
    "CORT hiring event Apr 20-21. Loader/Crew $16.50/hr. Same Day Pay. Register free today!",
    "Loader/Crew jobs $16.50/hr near Orlando Airport. Walk in and get hired. Register free!",
    "Two-day event, no experience needed. Come either day, 9am-2pm. Apply in under 2 minutes!",
    "Load furniture and event equipment for CORT. $16.50/hr. Hiring event Apr 20-21 in Orlando.",
]

# ── Display Responsive Display Ad copy ───────────────────────────────────────
DISPLAY_HEADLINES = [
    "Loader Jobs $16.50/hr",
    "Hiring Event Apr 20-21",
    "Get Hired on the Spot",
    "Same Day Pay Available",
    "Orlando FL Hiring Now",
]
DISPLAY_LONG_HEADLINES = [
    "Loader/Crew jobs $16.50/hr in Orlando. Hiring event April 20-21. Get hired on the spot!",
    "Same Day Pay. No experience needed. Walk into our hiring event Apr 20-21 in Orlando, FL.",
]
DISPLAY_DESCRIPTIONS = [
    "Two-day hiring event April 20-21, 9am-2pm. Loader/Crew $16.50/hr. Apply in 2 minutes!",
    "Walk in and walk out with a job offer. CORT Loader/Crew roles in Orlando. Register free.",
]

# ── App (UAC) copy ────────────────────────────────────────────────────────────
APP_HEADLINES = [
    "Download App & Attend Apr 20",
    "2-Day Hiring Event Orlando",
    "Loader Jobs $16.50/Hr",
    "Orlando FL, Apr 20-21",
    "Get Hired at Our Live Event",
]
APP_DESCRIPTIONS = [
    "Download Indeed Flex, register for our Apr 20-21 loader crew event in Orlando, FL.",
    "Loader/Crew $16.50/hr. Two-day hiring event Apr 20-21, 9am-2pm near Orlando Airport.",
    "Download the app, sign up and attend our 2-day event. Get hired on the spot in Orlando.",
    "Same Day Pay available. CORT loader/crew event Apr 20-21. Attend and walk out employed.",
    "Indeed Flex is hiring Loader/Crew in Orlando, FL. Register for Apr 20-21 today.",
]


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def get_client():
    return GoogleAdsClient.load_from_storage(YAML_PATH)


def create_budget(client, label: str, amount_micros: int) -> str:
    svc = client.get_service("CampaignBudgetService")
    op  = client.get_type("CampaignBudgetOperation")
    b   = op.create
    b.name              = f"CORT Orlando HE {label} {int(time.time())}"
    b.amount_micros     = amount_micros
    b.delivery_method   = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    result = svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ Budget created: ${amount_micros // 1_000_000}/day  →  {rn}")
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
            campaign.bidding_strategy,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.network_settings.target_google_search,
            campaign.network_settings.target_search_network,
            campaign.network_settings.target_content_network,
            campaign.network_settings.target_partner_search_network,
            campaign.app_campaign_setting.app_id,
            campaign.app_campaign_setting.app_store,
            campaign.app_campaign_setting.bidding_strategy_goal_type,
            campaign.campaign_budget
        FROM campaign
        WHERE campaign.id = {campaign_id}
        LIMIT 1
    """
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        return row.campaign
    raise ValueError(f"Campaign {campaign_id} not found")


def fetch_budget_amount(client, campaign_id: str) -> tuple:
    """Returns (budget_resource_name, amount_micros)."""
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT
            campaign_budget.resource_name,
            campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.id = {campaign_id}
        LIMIT 1
    """
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        b = row.campaign_budget
        return b.resource_name, b.amount_micros
    raise ValueError(f"Budget not found for campaign {campaign_id}")


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
    print(f"  ✅ {len(ops)} geo target(s) copied from BAU Search")
    return len(ops)


def add_negative_keywords(client, campaign_rn: str) -> None:
    svc = client.get_service("CampaignCriterionService")
    me  = client.enums.KeywordMatchTypeEnum
    ops = []
    for kw_text, match in NEGATIVE_KEYWORDS:
        op = client.get_type("CampaignCriterionOperation")
        cc = op.create
        cc.campaign              = campaign_rn
        cc.negative              = True
        cc.keyword.text          = kw_text
        cc.keyword.match_type    = getattr(me, match)
        ops.append(op)
    svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f"  ✅ {len(ops)} negative keywords added")


# ═══════════════════════════════════════════════════════════════════════════════
# BAU BUDGET REDUCTION
# ═══════════════════════════════════════════════════════════════════════════════

def reduce_bau_budgets(client) -> dict:
    """Reduces active BAU Display and App budgets to 50%.
    Search and P.Max are already paused at $5/day — left untouched.
    Returns a restore map: {campaign_id: (budget_rn, original_micros)}
    """
    print("\n── BAU Budget Reduction (50%) ──")
    budget_svc  = client.get_service("CampaignBudgetService")
    restore_map = {}

    for cid, cname in BAU_TO_REDUCE.items():
        budget_rn, current_micros = fetch_budget_amount(client, cid)
        new_micros = max(current_micros // 2, 1_000_000)  # floor at $1/day

        op = client.get_type("CampaignBudgetOperation")
        b  = op.update
        b.resource_name = budget_rn
        b.amount_micros = new_micros
        op.update_mask.paths.append("amount_micros")
        budget_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[op])

        restore_map[cid] = (budget_rn, current_micros)
        print(f"  ✅ {cname}")
        print(f"     ${current_micros // 1_000_000}/day → ${new_micros // 1_000_000}/day")

    print(f"\n  ⚠️  RESTORE on Apr 22:")
    for cid, (_, orig) in restore_map.items():
        print(f"     {BAU_TO_REDUCE[cid]}: ${orig // 1_000_000}/day")
    return restore_map


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 1: SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

def create_search_campaign(client, budget_rn: str, geo_targets: list) -> str:
    print("\n── Creating Search Campaign ──")
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                                            = SEARCH_NAME
    c.campaign_budget                                 = budget_rn
    c.status                                          = client.enums.CampaignStatusEnum.PAUSED
    c.advertising_channel_type                        = client.enums.AdvertisingChannelTypeEnum.SEARCH
    c.end_date_time                                       = EVENT_END_DATE_TIME

    c.contains_eu_political_advertising               = 3  # DOES_NOT_CONTAIN
    c.network_settings.target_google_search           = True
    c.network_settings.target_search_network          = False
    c.network_settings.target_content_network         = False
    c.network_settings.target_partner_search_network  = False
    # Maximize Clicks (target_spend) to start; switch to Maximize Conversions on Day 3 (Apr 16)
    c.target_spend.cpc_bid_ceiling_micros = 3_000_000  # $3.00 max CPC cap
    result = svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    camp_rn = result.results[0].resource_name
    print(f"  ✅ Search campaign: {camp_rn}")

    copy_geo_targets(client, geo_targets, camp_rn)
    add_negative_keywords(client, camp_rn)
    return camp_rn


def create_search_ad_groups(client, campaign_rn: str) -> None:
    ag_svc   = client.get_service("AdGroupService")
    ad_svc   = client.get_service("AdGroupAdService")
    crit_svc = client.get_service("AdGroupCriterionService")
    me       = client.enums.KeywordMatchTypeEnum
    SAFT     = client.enums.ServedAssetFieldTypeEnum

    for ag_name, ag_data in AD_GROUPS.items():
        print(f"\n  Ad Group: {ag_name}")

        # Create ad group
        ag_op = client.get_type("AdGroupOperation")
        ag    = ag_op.create
        ag.name           = ag_name
        ag.campaign       = campaign_rn
        ag.status         = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_          = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ag.cpc_bid_micros = ag_data["cpc_bid_micros"]
        ag_resp = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
        ag_rn   = ag_resp.results[0].resource_name
        print(f"    ✅ Ad group created: {ag_rn.split('/')[-1]}")

        # Create RSA
        rsa_data = ag_data["rsa"]
        ad_op    = client.get_type("AdGroupAdOperation")
        ada      = ad_op.create
        ada.ad_group = ag_rn
        ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
        rsa          = ada.ad.responsive_search_ad
        rsa.path1    = rsa_data["path1"]
        rsa.path2    = rsa_data["path2"]

        PIN_MAP = {1: SAFT.HEADLINE_1, 2: SAFT.HEADLINE_2}
        for hl_text, pin_pos in rsa_data["headlines"]:
            asset = client.get_type("AdTextAsset")
            asset.text = hl_text
            if pin_pos in PIN_MAP:
                asset.pinned_field = PIN_MAP[pin_pos]
            rsa.headlines.append(asset)

        for desc_text in rsa_data["descriptions"]:
            asset = client.get_type("AdTextAsset")
            asset.text = desc_text
            rsa.descriptions.append(asset)

        ada.ad.final_urls.append(FINAL_URL)
        ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
        print(f"    ✅ RSA created (path: {rsa_data['path1']}/{rsa_data['path2']})")

        # Create keywords (PHRASE MATCH ONLY)
        kw_ops = []
        for kw_text, match_type in ag_data["keywords"]:
            kw_op = client.get_type("AdGroupCriterionOperation")
            kw    = kw_op.create
            kw.ad_group          = ag_rn
            kw.status            = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw.keyword.text      = kw_text
            kw.keyword.match_type = getattr(me, match_type)
            kw_ops.append(kw_op)
        crit_svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=kw_ops)
        print(f"    ✅ {len(kw_ops)} phrase-match keywords added")


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 2: DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def create_display_campaign(
    client, budget_rn: str, geo_targets: list, visual_assets: list
) -> str:
    print("\n── Creating Display Campaign ──")
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                            = DISPLAY_NAME
    c.campaign_budget                 = budget_rn
    c.status                          = client.enums.CampaignStatusEnum.PAUSED
    c.advertising_channel_type        = client.enums.AdvertisingChannelTypeEnum.DISPLAY
    c.end_date_time                                       = EVENT_END_DATE_TIME

    c.contains_eu_political_advertising = 3
    c.network_settings.target_content_network = True
    c.maximize_conversions.target_cpa_micros  = 0  # no tCPA at creation; set in UI after launch
    result  = svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    camp_rn = result.results[0].resource_name
    print(f"  ✅ Display campaign: {camp_rn}")

    copy_geo_targets(client, geo_targets, camp_rn)

    # Separate visual assets by field type for RDA
    landscape_imgs = []
    square_imgs    = []
    logos          = []
    ft_enum        = client.enums.AssetFieldTypeEnum
    for va in visual_assets:
        ft_name = ft_enum(va["field_type"]).name
        if ft_name in ("MARKETING_IMAGE",):
            landscape_imgs.append(va["asset"])
        elif ft_name in ("SQUARE_MARKETING_IMAGE",):
            square_imgs.append(va["asset"])
        elif ft_name in ("LOGO", "LANDSCAPE_LOGO"):
            logos.append(va["asset"])

    # 3 audience-based ad groups
    ag_svc = client.get_service("AdGroupService")
    ad_svc = client.get_service("AdGroupAdService")

    for segment in ("site_visitors", "verified_users", "app_download_not_verified"):
        ag_name = f"orlando_industrial_none_none_none_{segment}"
        ag_op   = client.get_type("AdGroupOperation")
        ag      = ag_op.create
        ag.name     = ag_name
        ag.campaign = camp_rn
        ag.status   = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_    = client.enums.AdGroupTypeEnum.DISPLAY_STANDARD
        ag_resp = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
        ag_rn   = ag_resp.results[0].resource_name
        print(f"  ✅ Display ad group: {ag_name}")

        ad_op = client.get_type("AdGroupAdOperation")
        ada   = ad_op.create
        ada.ad_group = ag_rn
        ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
        rda = ada.ad.responsive_display_ad
        rda.business_name       = "Indeed Flex"
        rda.long_headline.text  = DISPLAY_LONG_HEADLINES[0]

        for h_text in DISPLAY_HEADLINES:
            h = client.get_type("AdTextAsset")
            h.text = h_text
            rda.headlines.append(h)
        for d_text in DISPLAY_DESCRIPTIONS:
            d = client.get_type("AdTextAsset")
            d.text = d_text
            rda.descriptions.append(d)

        for rn in landscape_imgs[:5]:
            img = client.get_type("AdImageAsset")
            img.asset = rn
            rda.marketing_images.append(img)
        for rn in square_imgs[:5]:
            img = client.get_type("AdImageAsset")
            img.asset = rn
            rda.square_marketing_images.append(img)
        for rn in logos[:2]:
            logo = client.get_type("AdImageAsset")
            logo.asset = rn
            rda.logo_images.append(logo)

        ada.ad.final_urls.append(FINAL_URL)
        ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
        print(f"    ✅ Responsive Display Ad created for {segment}")

    return camp_rn


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 3: PERFORMANCE MAX
# ═══════════════════════════════════════════════════════════════════════════════

def create_pmax_campaign(client, budget_rn: str, geo_targets: list, visual_assets: list) -> str:
    print("\n── Creating Performance Max Campaign ──")
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                            = PMAX_NAME
    c.campaign_budget                 = budget_rn
    c.status                          = client.enums.CampaignStatusEnum.PAUSED
    c.advertising_channel_type        = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    c.end_date_time                                       = EVENT_END_DATE_TIME

    c.contains_eu_political_advertising = 3
    c.brand_guidelines_enabled          = False
    c.maximize_conversions.target_cpa_micros = 0
    result  = svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    camp_rn = result.results[0].resource_name
    print(f"  ✅ P.Max campaign: {camp_rn}")

    copy_geo_targets(client, geo_targets, camp_rn)
    _create_pmax_asset_group(client, camp_rn, visual_assets)
    return camp_rn


def _create_pmax_asset_group(client, camp_rn: str, visual_assets: list) -> str:
    ga_svc  = client.get_service("GoogleAdsService")
    ft      = client.enums.AssetFieldTypeEnum
    ag_tmp  = f"customers/{CUSTOMER_ID}/assetGroups/-1"
    ops     = []    # asset group + text asset creates
    lk_ops  = []    # asset group asset links
    counter = [-1]

    # Asset group
    ag_op = client.get_type("MutateOperation")
    ag    = ag_op.asset_group_operation.create
    ag.resource_name = ag_tmp
    ag.campaign      = camp_rn
    ag.name          = "Loader Crew - Orlando"
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
        aga.asset        = temp_rn
        aga.field_type   = field_type
        lk_ops.append(lop)

    def link_existing(asset_rn: str, field_type) -> None:
        lop = client.get_type("MutateOperation")
        aga = lop.asset_group_asset_operation.create
        aga.asset_group = ag_tmp
        aga.asset        = asset_rn
        aga.field_type   = field_type
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

    # BAU P.Max has no LOGO — add shared Indeed Flex logo (same account)
    if "LOGO" not in seen_ft:
        link_existing("customers/7236100723/assets/56893637546", ft.LOGO)
    if "LANDSCAPE_LOGO" not in seen_ft:
        link_existing("customers/7236100723/assets/56894244206", ft.LANDSCAPE_LOGO)

    all_ops = ops + lk_ops
    print(f"  Batch: 1 asset group + {-counter[0] - 1} text assets + "
          f"{len(visual_assets)} BAU visual assets = {len(all_ops)} ops")
    response = ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=all_ops)

    for res in response.mutate_operation_responses:
        kind = res._pb.WhichOneof("response")
        if kind == "asset_group_result":
            rn = res.asset_group_result.resource_name
            print(f"  ✅ Asset group created: {rn}")
            return rn
    raise ValueError("Asset group resource name not found in mutate response")


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 4: APP (UAC)
# ═══════════════════════════════════════════════════════════════════════════════

def create_app_campaign(client, source, budget_rn: str, geo_targets: list) -> str:
    print("\n── Creating App Campaign ──")
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                           = APP_NAME
    c.campaign_budget                = budget_rn
    c.status                         = client.enums.CampaignStatusEnum.PAUSED
    c.advertising_channel_type       = client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL
    c.advertising_channel_sub_type   = client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN
    c.end_date_time                                       = EVENT_END_DATE_TIME

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
    print(f"  ✅ App campaign: {camp_rn}")

    copy_geo_targets(client, geo_targets, camp_rn)

    # App ad group + 3 UAC ads
    ag_svc = client.get_service("AdGroupService")
    ad_svc = client.get_service("AdGroupAdService")

    ag_op = client.get_type("AdGroupOperation")
    ag    = ag_op.create
    ag.name     = "CORT Orlando HE - UAC"
    ag.campaign = camp_rn
    ag.status   = client.enums.AdGroupStatusEnum.ENABLED
    ag_resp = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
    ag_rn   = ag_resp.results[0].resource_name
    print(f"  ✅ App ad group: {ag_rn.split('/')[-1]}")

    for idx, (label, headlines, descriptions) in enumerate([
        ("Urgency",           APP_HEADLINES, APP_DESCRIPTIONS[:4]),
        ("Pay & Benefits",    APP_HEADLINES, [APP_DESCRIPTIONS[1], APP_DESCRIPTIONS[3],
                                              APP_DESCRIPTIONS[4], APP_DESCRIPTIONS[0]]),
        ("Download Process",  APP_HEADLINES, [APP_DESCRIPTIONS[2], APP_DESCRIPTIONS[4],
                                              APP_DESCRIPTIONS[0], APP_DESCRIPTIONS[1]]),
    ], 1):
        ad_op  = client.get_type("AdGroupAdOperation")
        ada    = ad_op.create
        ada.ad_group = ag_rn
        ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
        app_ad = ada.ad.app_ad
        for h in headlines:
            asset = client.get_type("AdTextAsset")
            asset.text = h
            app_ad.headlines.append(asset)
        for d in descriptions:
            asset = client.get_type("AdTextAsset")
            asset.text = d
            app_ad.descriptions.append(asset)
        ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
        print(f"    ✅ UAC ad variant {idx} created: {label}")

    return camp_rn


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    client = get_client()
    skip_pmax_source = SOURCE_PMAX_CAMPAIGN_ID == "SKIP"

    print("\n══════════════════════════════════════════════════════════════════")
    print("  CORT Hiring Event Orlando FL — 4-Campaign Launch")
    print("  Search + Display + Performance Max + App   |   Apr 14–21, 2026")
    print("══════════════════════════════════════════════════════════════════\n")

    # ── Phase 1: Fetch BAU data ──────────────────────────────────────────────
    print("── Phase 1: Fetching BAU data ──")
    source_search = fetch_campaign(client, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  ✅ BAU Search: {source_search.name}")

    source_app = fetch_campaign(client, SOURCE_APP_CAMPAIGN_ID)
    print(f"  ✅ BAU App: {source_app.name}")

    geo_targets = fetch_geo_targets(client, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  ✅ {len(geo_targets)} geo target(s) fetched from BAU Search")

    visual_assets = []
    if not skip_pmax_source:
        source_pmax = fetch_campaign(client, SOURCE_PMAX_CAMPAIGN_ID)
        print(f"  ✅ BAU P.Max: {source_pmax.name}")
        ag_rn = fetch_pmax_asset_group(client, SOURCE_PMAX_CAMPAIGN_ID)
        if ag_rn:
            visual_assets = fetch_visual_assets(client, ag_rn)
            print(f"  ✅ {len(visual_assets)} visual asset(s) fetched from BAU P.Max")
        else:
            print("  ⚠️  No asset group found on BAU P.Max — text-only P.Max")
    else:
        print("  ℹ️  P.Max source set to SKIP — will create P.Max with text assets only")

    # ── Phase 2: BAU budget reduction — ALREADY DONE (Display $15, App $25) ──
    restore_map = {"23052892689": (None, 30_000_000), "23369869887": (None, 50_000_000)}

    # ── Phase 3: Create event campaigns ─────────────────────────────────────
    # Reuse budgets from last run to avoid orphaned budget objects
    app_budget_rn     = "customers/7236100723/campaignBudgets/15484219349"   # $50 App

    # Search campaign already created — skip re-creation
    search_rn  = "customers/7236100723/campaigns/23737661476"
    print("\n── Search Campaign ── ALREADY COMPLETE (23737661476)")

    # Display campaign already created — skip re-creation
    display_rn = "customers/7236100723/campaigns/23728073943"
    print("\n── Display Campaign ── ALREADY COMPLETE (23728073943)")

    # P.Max campaign already created — just build the asset group
    pmax_rn = "customers/7236100723/campaigns/23728073994"
    print("\n── P.Max Campaign ── ALREADY CREATED (23728073994) — building asset group")
    _create_pmax_asset_group(client, pmax_rn, visual_assets)
    copy_geo_targets(client, geo_targets, pmax_rn)

    app_rn     = create_app_campaign(client, source_app, app_budget_rn, geo_targets)

    # ── Summary ──────────────────────────────────────────────────────────────
    print("\n" + "═" * 62)
    print("  ✅ ALL 4 CAMPAIGNS CREATED (PAUSED)")
    print("═" * 62)
    print(f"  Search:  {SEARCH_NAME}")
    print(f"           {search_rn}")
    print(f"  Display: {DISPLAY_NAME}")
    print(f"           {display_rn}")
    print(f"  P.Max:   {PMAX_NAME}")
    print(f"           {pmax_rn}")
    print(f"  App:     {APP_NAME}")
    print(f"           {app_rn}")
    print()
    print("  NEXT STEPS:")
    print("  1. Review all 4 campaigns in Google Ads UI")
    print("  2. Enable all 4 on Apr 14 at 6am ET")
    print("  3. Apr 16 (Day 3): Switch Search → Maximize Conversions, tCPA $8")
    print("  4. Apr 21 at 2pm: Pause all 4 campaigns")
    print("  5. Apr 22: Restore BAU budgets:")
    for cid, (_, orig) in restore_map.items():
        print(f"     Campaign {cid} → ${orig // 1_000_000}/day")
    print()
    print("  MANUAL STEPS (Google Ads UI):")
    print("  - Add sitelinks: Event Details, Download the App, See Loader/Crew Shifts, Browse All Jobs")
    print("  - Add callouts: Hired on the Spot, $16.50/Hr, No Experience Needed, Same Day Pay Available")
    print("  - Add structured snippets: Types (Loader, Crew, Furniture Handler, Event Setup)")
    print("  - Demographics (Search + Display): 25-34 +15%, 35-44 +10%, 18-24 +10%")
    print("  - Add P.Max images if BAU P.Max had no visual assets")


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
        raise
