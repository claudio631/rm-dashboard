#!/usr/bin/env python3
"""
Google Ads — Stord Hiring Event — Hebron, KY (Apr 28, 2026)
Campaigns: Search ($50/day) + Performance Max ($50/day) + App ($50/day)
Flight:    Apr 17–28, 2026  |  Total daily: $150  |  Total: ~$1,650

Search : 8 ad groups × 3 RSAs = 24 RSAs (3 event + 5 Phoenix BAU broad)
P.Max  : 1 asset group — visual assets from Hebron BAU P.Max
App    : 3 ad groups × 1 UAC ad = 3 app ads

Run: python3 scripts/google-ads-stord-hiring-event-hebron-ky.py
"""

from typing import Optional
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Source BAU campaign IDs (Hebron Industrial) ────────────────────────────
SOURCE_SEARCH_CAMPAIGN_ID = "23051289962"   # p-b2c-google-search-us-bofu-bau-hebron-industrial--eg--
SOURCE_APP_CAMPAIGN_ID    = "23051328869"   # p-b2c-google-app-us-bofu-bau-hebron-industrial--eg--
SOURCE_PMAX_CAMPAIGN_ID   = "23045206287"   # p-b2c-google-p_max-us-bofu-bau-hebron-industrial-eg

DAILY_BUDGET_MICROS = 50_000_000
EVENT_END_DATE_TIME = "2026-04-28 23:59:59"
FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/504349"
    "&employer=stord-inc&metro=erlanger-ky"
    "&role=warehouse-operative"
    "&utm_campaign=hiring-event-stord-hebron-ky"
)

SEARCH_NAME = "p-b2c-google-search-us-bofu-bau-hebron-industrial-hiring-event-04282026"
PMAX_NAME   = "p-b2c-google-pmax-us-bofu-bau-hebron-industrial-hiring-event-04282026"
APP_NAME    = "p-b2c-google-app-us-bofu-bau-hebron-industrial-hiring-event-04282026"

VISUAL_FIELD_TYPE_NAMES = {
    "MARKETING_IMAGE", "SQUARE_MARKETING_IMAGE", "PORTRAIT_MARKETING_IMAGE",
    "LOGO", "LANDSCAPE_LOGO",
}

# ═══════════════════════════════════════════════════════════════════════════
# SEARCH — 8 Ad Groups (3 event + 5 Phoenix BAU broad)
# ═══════════════════════════════════════════════════════════════════════════

SEARCH_AD_GROUPS = [
    # ── EVENT-FOCUSED ────────────────────────────────────────────────────
    {
        "name": "Hiring Event — Hebron KY",
        "cpc_bid_micros": 2_500_000,
        "keywords": [
            ("hiring event hebron ky", "PHRASE"),
            ("hiring event near me", "PHRASE"),
            ("job fair hebron kentucky", "PHRASE"),
            ("walk in job fair cincinnati", "PHRASE"),
            ("warehouse hiring event near me", "PHRASE"),
            ("job fair near cvg airport", "PHRASE"),
            ("immediate hire warehouse kentucky", "PHRASE"),
            ("warehouse hiring event cincinnati", "PHRASE"),
            ("hiring event erlanger ky", "PHRASE"),
        ],
    },
    {
        "name": "Warehouse Jobs — Hebron Cincinnati",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("warehouse jobs hebron ky", "PHRASE"),
            ("warehouse jobs near me", "PHRASE"),
            ("warehouse worker hebron kentucky", "PHRASE"),
            ("warehouse jobs cincinnati area", "PHRASE"),
            ("warehouse jobs hiring now kentucky", "PHRASE"),
            ("warehouse jobs erlanger ky", "PHRASE"),
            ("general labor jobs hebron ky", "PHRASE"),
            ("entry level warehouse jobs kentucky", "PHRASE"),
            ("industrial jobs hebron ky", "PHRASE"),
        ],
    },
    {
        "name": "Forklift Jobs — Hebron KY",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("forklift jobs hebron ky", "PHRASE"),
            ("forklift operator jobs near me", "PHRASE"),
            ("forklift driver jobs kentucky", "PHRASE"),
            ("forklift jobs cincinnati", "PHRASE"),
            ("forklift jobs hiring now", "PHRASE"),
            ("forklift operator hiring near me", "PHRASE"),
            ("warehouse forklift jobs erlanger", "PHRASE"),
        ],
    },
    # ── PHOENIX BAU BROAD GROUPS ─────────────────────────────────────────
    {
        "name": "p---generic_immediate--",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("immediate start jobs", "PHRASE"),
            ("immediate start jobs cincinnati", "PHRASE"),
            ("immediate start jobs hebron ky", "PHRASE"),
            ("jobs hiring immediately near me", "PHRASE"),
            ("hiring immediately warehouse", "PHRASE"),
            ("start work this week", "PHRASE"),
            ("jobs you can start immediately", "PHRASE"),
        ],
    },
    {
        "name": "p---temp_keywords-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("temp agency", "BROAD"),
            ("temp agency", "PHRASE"),
            ("temp agency", "EXACT"),
            ("temp work agency", "PHRASE"),
            ("temping agencies", "PHRASE"),
            ("temping agency", "PHRASE"),
            ("temping agency", "EXACT"),
            ("temporary recruitment agency", "PHRASE"),
            ("temporary recruitment agency", "EXACT"),
            ("temp staffing agency cincinnati", "PHRASE"),
            ("temp jobs cincinnati ky", "PHRASE"),
        ],
    },
    {
        "name": "p-industrial---warehouse",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("warehouse temporary jobs", "BROAD"),
            ("warehouse temporary jobs", "PHRASE"),
            ("part time warehouse jobs", "BROAD"),
            ("part time warehouse jobs", "PHRASE"),
            ("Warehouse Operative job", "PHRASE"),
            ("Warehouse Operative flexible", "PHRASE"),
            ("Warehouse Operative temp", "PHRASE"),
            ("Warehouse Associate job", "PHRASE"),
            ("warehouse weekend jobs", "PHRASE"),
            ("temporary warehouse jobs cincinnati", "PHRASE"),
            ("warehouse jobs hiring now ky", "PHRASE"),
        ],
    },
    {
        "name": "p---generic-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("temp jobs", "PHRASE"),
            ("temporary jobs", "PHRASE"),
            ("temporary work", "EXACT"),
            ("weekend jobs", "PHRASE"),
            ("weekend temp work", "PHRASE"),
            ("flexible jobs cincinnati", "PHRASE"),
            ("temporary jobs hebron ky", "PHRASE"),
        ],
    },
    {
        "name": "p---agency_keywords-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("agency jobs", "EXACT"),
            ("agency work", "EXACT"),
            ("job agency", "PHRASE"),
            ("employment agency", "PHRASE"),
            ("recruitment agency", "PHRASE"),
            ("agency recruitment", "PHRASE"),
            ("staffing agency cincinnati", "PHRASE"),
            ("job agency hebron ky", "PHRASE"),
        ],
    },
]

RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Hiring-Event",
        "path2": "Hebron-KY",
        "headlines": [
            "Hiring Event — April 28th",
            "Hebron KY · Mon Apr 28",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Register Before Spots Fill Up",
            "Get Hired Today — Apr 28",
            "Meet Recruiters Face to Face",
            "Indeed Flex Hiring Event",
            "Warehouse Jobs Hiring Now",
            "Work Near Cincinnati KY",
            "1st & 2nd Shift Available",
            "Same Day Pay Available",
            "This Monday — Apr 28",
            "$75 Referral Bonus",
            "Limited Spots — Register Now",
        ],
        "descriptions": [
            "Join us Apr 28, 10am-2pm at Kentucky Career Center CVG, Hebron. Get hired on the spot!",
            "No long process. Meet our recruiters & get an instant offer on April 28th. Sign up free.",
            "Walk in, interview live, and leave with a job offer on April 28 in Hebron, KY.",
            "Limited spots left. Register today for the Indeed Flex hiring event on April 28th, 2026.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Warehouse-Jobs",
        "path2": "Hebron-KY",
        "headlines": [
            "Warehouse Jobs $15–$17/Hr",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Health & Vision Benefits",
            "Forklift Roles $17.50/Hr",
            "Full-Time Potential Available",
            "Hiring Event — April 28th",
            "Hebron KY · Mon Apr 28",
            "Get Paid Same Day or Next Day",
            "Health & Dental Coverage",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Long & Short-Term Work",
            "Competitive Pay + Benefits",
            "Indeed Flex Hiring Event",
        ],
        "descriptions": [
            "Warehouse $15.50/hr & Forklift $17.50/hr. Same Day Pay & health benefits. Apply now.",
            "$75 per referral, Same Day Pay & full health benefits. Join us April 28th in Hebron, KY.",
            "Warehouse & forklift roles. Health/dental/vision & Same Day Pay. Join us Apr 28.",
            "Come to our Apr 28 hiring event. Leave with a $15.50-$17.50/hr offer + full benefits.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "path1": "Warehouse-Jobs",
        "path2": "Cincinnati",
        "headlines": [
            "No Long Application Process",
            "Get Hired in One Day",
            "Meet Recruiters Face to Face",
            "Start Working This Week",
            "Full-Time Potential Available",
            "Warehouse Jobs Hiring Now",
            "Flexible 1st & 2nd Shifts",
            "Hiring Event — April 28th",
            "Hebron KY · Mon Apr 28",
            "Walk In, Walk Out Employed",
            "Indeed Flex Hiring Event",
            "Warehouse Jobs $15–$17/Hr",
            "Apply in Minutes on Site",
            "Same Day Pay Available",
            "This Monday — Apr 28",
        ],
        "descriptions": [
            "Indeed Flex hiring event — walk in & leave with a job offer. 1st & 2nd shift openings.",
            "Skip the wait. Interview live with recruiters on April 28 & start working this week.",
            "Full-time opportunities available. Attend Apr 28 at Kentucky Career Center, Hebron, KY.",
            "Warehouse & forklift roles open now. Walk in on April 28, leave with a job offer.",
        ],
    },
]

NEGATIVE_KEYWORDS = [
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
    ("internship", "PHRASE"),
    ("volunteer", "PHRASE"),
]

# ═══════════════════════════════════════════════════════════════════════════
# PERFORMANCE MAX — Text Assets
# ═══════════════════════════════════════════════════════════════════════════

PMAX_HEADLINES = [
    "Hiring Event — April 28th",
    "Hebron KY · Mon Apr 28",
    "Warehouse Jobs $15–$17/Hr",
    "Instant Job Offer on the Spot",
    "Warehouse Jobs Hiring Now",
    "Walk In, Walk Out Employed",
    "Same Day Pay Available",
    "This Monday — Apr 28",
    "Meet Recruiters Face to Face",
    "Indeed Flex Hiring Event",
    "Work Near Cincinnati KY",
    "1st & 2nd Shift Available",
    "Get Hired Today — Apr 28",
    "$75 Referral Bonus",
    "Limited Spots — Register Now",
]

PMAX_LONG_HEADLINES = [
    "Join our April 28 hiring event in Hebron, KY. Warehouse jobs $15.50-$17.50/hr.",
    "Walk in, walk out employed. Indeed Flex warehouse & forklift jobs near Cincinnati, KY.",
    "This Monday only. Warehouse hiring event April 28 in Hebron, KY — apply free.",
    "Same Day Pay. Hiring Warehouse Workers & Forklift Drivers in Hebron, KY. Get hired Apr 28.",
    "No experience barrier. 1st & 2nd shifts available. Get hired on the spot April 28.",
]

PMAX_DESCRIPTIONS = [
    "Hiring event Apr 28, 10am-2pm in Hebron, KY. Warehouse $15.50 & Forklift $17.50/hr.",
    "Warehouse & forklift roles. Same Day Pay & health benefits. Apply now.",
    "Indeed Flex hiring event — walk in & leave with a job offer. 1st & 2nd shift openings.",
    "No long process. Meet our recruiters & get an instant offer on April 28th. Sign up free.",
    "$15.50-$17.50/hr warehouse & forklift roles near Cincinnati. Get hired Apr 28.",
]

# ═══════════════════════════════════════════════════════════════════════════
# APP CAMPAIGN — 3 Ad Groups
# ═══════════════════════════════════════════════════════════════════════════

APP_AD_GROUPS = [
    {
        "name": "Hebron HE - Urgency",
        "headlines": [
            "Download App & Attend Apr 28",
            "Hiring Event — April 28th",
            "Warehouse Jobs $15–$17/Hr",
            "Limited Spots — Register Now",
            "Get Hired at Our Live Event",
        ],
        "descriptions": [
            "Download Indeed Flex & register for our Apr 28 hiring event in Hebron, KY.",
            "Walk in April 28, 10am-2pm. Get hired on the spot. Register via app today.",
            "Limited spots available. Download the app & register for Apr 28 event in KY.",
            "No long process. Download, sign up & attend our hiring event on April 28th.",
            "Get hired on April 28 in Hebron, KY. Download the Indeed Flex app now.",
        ],
    },
    {
        "name": "Hebron HE - Pay & Benefits",
        "headlines": [
            "Warehouse Jobs $15–$17/Hr",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Warehouse Jobs Near Cincinnati",
            "Health Benefits Included",
        ],
        "descriptions": [
            "Warehouse $15.50/hr & Forklift $17.50/hr. Same Day Pay & benefits. Download app.",
            "Download Indeed Flex, register for Apr 28 hiring event & earn $15.50-$17.50/hr.",
            "Same Day Pay, $75 referral & health benefits. Come to our Apr 28 event.",
            "Competitive pay + benefits. Download Indeed Flex & attend hiring event April 28.",
            "Same Day Pay, health/dental/vision. Join us Apr 28 in Hebron, KY.",
        ],
    },
    {
        "name": "Hebron HE - Process",
        "headlines": [
            "Download App & Attend Apr 28",
            "Get Hired at Our Live Event",
            "Full-Time Potential Available",
            "No Long Interview Process",
            "Hiring Event — April 28th",
        ],
        "descriptions": [
            "Download Indeed Flex & come to our Apr 28 event. Walk in, get hired, start this week.",
            "Skip the wait — attend our live hiring event. Get an instant job offer on April 28.",
            "Full-time opportunities available. Download app, register & attend Apr 28 event.",
            "No lengthy process. Interview live Apr 28 in Hebron, KY. Download Indeed Flex today.",
            "Walk in April 28, meet our recruiters & leave with a $15.50-$17.50/hr offer.",
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
    b.name              = f"Hebron Industrial HE {label} 20260428"
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
        print(f"    ✅ {len(kw_ops)} keywords added")


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
    ag.name          = "Warehouse Workers — Hebron KY"
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

    ft_enum = client.enums.AssetFieldTypeEnum
    seen_ft = set()
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
# CAMPAIGN 3: APP
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
    print("  Stord Hiring Event — Hebron, KY — Apr 28, 2026")
    print("  Search + P.Max + App  |  $50/day each  |  ~$1,650 total")
    print("═══════════════════════════════════════════════════════════════\n")

    print("── Phase 1: Fetching BAU Hebron Industrial data ──")
    source_search = fetch_campaign(client, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  ✅ BAU Search: {source_search.name}")

    source_app = fetch_campaign(client, SOURCE_APP_CAMPAIGN_ID)
    print(f"  ✅ BAU App: {source_app.name}")

    geo_targets = fetch_geo_targets(client, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  ✅ {len(geo_targets)} geo target(s) fetched from BAU Search")

    source_pmax = fetch_campaign(client, SOURCE_PMAX_CAMPAIGN_ID)
    print(f"  ✅ BAU P.Max: {source_pmax.name}")
    ag_rn = fetch_pmax_asset_group(client, SOURCE_PMAX_CAMPAIGN_ID)
    visual_assets = []
    if ag_rn:
        visual_assets = fetch_visual_assets(client, ag_rn)
        print(f"  ✅ {len(visual_assets)} visual asset(s) fetched from BAU P.Max")
    else:
        print("  ⚠️  No asset group on BAU P.Max — using account logos only")

    print("\n── Phase 2: Creating campaigns ──")

    search_budget_rn = create_budget(client, "Search")
    search_rn        = create_search_campaign(client, search_budget_rn, source_search, geo_targets)
    create_search_ad_groups(client, search_rn)

    pmax_budget_rn = create_budget(client, "PMax")
    pmax_rn        = create_pmax_campaign(client, pmax_budget_rn, geo_targets, visual_assets)

    app_budget_rn = create_budget(client, "App")
    app_rn        = create_app_campaign(client, app_budget_rn, source_app, geo_targets)

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
    print("    1. Event Details | Apr 28, 10am-2pm, Kentucky Career Center CVG, Hebron KY")
    print("    2. Download the App | Get the Indeed Flex app to register")
    print("    3. Warehouse & Forklift Shifts | $15.50-$17.50/hr — start this week")
    print("    4. Same Day Pay Info | Get paid the same or next day")
    print("    5. Benefits Overview | Health, dental, vision coverage")
    print("    6. Browse All Jobs | See all available jobs near you")
    print()
    print("  Callouts (min 4):")
    print("    - Hired on the Spot | $15.50-$17.50/Hr | No Long Process")
    print("    - Same Day Pay Available | $75 Referral Bonus")
    print()
    print("  Structured Snippets (min 3):")
    print("    - Job Types: Warehouse Worker, Forklift Driver, Picker Packer, General Labor")
    print("    - Benefits: Same-Day Pay, Health Benefits, Flexible Scheduling")
    print("    - Shifts: 1st Shift, 2nd Shift, Weekday")
    print()
    print(f"  POST-EVENT (Apr 28 after 2pm):")
    print(f"    python3 scripts/google-ads-pause-campaigns.py \\")
    print(f"      --label 'Hebron Industrial HE 04282026' \\")
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
