#!/usr/bin/env python3
"""
Mt. Juliet / Nashville Hiring Event — Duplicate Campaign Launch
- Duplicates BAU Nashville Search + App campaigns (BAU stays live and untouched)
- Sets $50/day budget + April 9 end date on duplicates
- Expands geo-targeting to include Mt. Juliet, TN
- Creates 3 RSAs per ad group (urgency / pay & benefits / process angles)
- Adds event-specific ad group + keywords

BEFORE RUNNING: Set SOURCE_SEARCH_CAMPAIGN_ID and SOURCE_APP_CAMPAIGN_ID
below — find them in Google Ads for campaigns matching:
  p-b2c-google-search-us-bofu-bau-nashville-*--eg--
  p-b2c-google-app-us-bofu-bau-nashville-*--eg--

Run: python3 scripts/google-ads-mt-juliet-hiring-event.py
"""
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Source BAU campaign IDs — CONFIRM IN GOOGLE ADS BEFORE RUNNING ───────
SOURCE_SEARCH_CAMPAIGN_ID = "TODO"   # p-b2c-google-search-us-bofu-bau-nashville-*--eg--
SOURCE_APP_CAMPAIGN_ID    = "TODO"   # p-b2c-google-app-us-bofu-bau-nashville-*--eg--

# ── Event config ──────────────────────────────────────────────────────────
DAILY_BUDGET_MICROS = 50_000_000  # $50/day
EVENT_END_DATE      = "20260409"  # YYYYMMDD
FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/500463"
    "&employer=NA"
    "&metro=nashville"
    "&role=event-staff"
    "&utm_campaign=us-hiring-event-goodwill-mt-juliet"
)
# Mt. Juliet, TN geo target constant (Google Ads canonical ID)
# Fetched at runtime via GeoTargetConstantService — no hardcoding needed
MT_JULIET_GEO_QUERY = "Mt. Juliet"

SEARCH_EVENT_NAME = (
    "p-b2c-google-search-us-bofu-bau-nashville-hiring-event-04092026"
)
APP_EVENT_NAME = (
    "p-b2c-google-app-us-bofu-bau-nashville-hiring-event-04092026"
)

# ── RSA copy — 3 variants per ad group ───────────────────────────────────
RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Hiring-Event",
        "path2": "Mt-Juliet",
        "headlines": [
            "Hiring Event — April 9th",
            "Mt. Juliet, TN · Thu Apr 9",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Register Before Spots Fill Up",
            "Get Hired Today — Apr 9",
            "Meet Recruiters Face to Face",
            "Indeed Flex Hiring Event",
            "Warehouse & Event Staff $16+",
            "Multiple Roles Available",
            "Goodwill Career Center April 9",
            "Limited Spots — Register Now",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "$16–$18/Hr + Bonuses",
        ],
        "descriptions": [
            "Join us Apr 9, 10am–2pm at 1985 Providence Pkwy, Mt. Juliet TN. Get hired on the spot!",
            "No long process. Meet our recruiters & get an instant offer on April 9. Sign up free.",
            "Walk in, interview live, and walk out with a job offer on April 9 in Mt. Juliet, TN.",
            "Limited spots left. Register today for the Indeed Flex hiring event on April 9th, 2026.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Hiring-Event",
        "path2": "Apply-Now",
        "headlines": [
            "Warehouse & Event Staff $16+",
            "$16–$18/Hr + Special Bonuses",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Health & Vision Benefits",
            "Multiple Roles $16–$18/Hr",
            "Full-Time Potential Available",
            "Hiring Event — April 9th",
            "Mt. Juliet, TN · Thu Apr 9",
            "Get Paid Same Day or Next Day",
            "Health & Dental Coverage",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Flex & Long-Term Shifts Open",
            "Competitive Pay + Benefits",
        ],
        "descriptions": [
            "Warehouse, event staff & hospitality jobs $16–$18/hr. Same Day Pay. Apply now.",
            "Earn $75 per referral, Same Day Pay & full health benefits. Join us April 9th in TN.",
            "Competitive pay $16–$18/hr, health/dental/vision & Same Day Pay. Join us April 9th.",
            "Come to our Apr 9 hiring event. Leave with a $16–$18/hr offer + full-time potential.",
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
            "Start Working This Week",
            "Full-Time Potential Available",
            "Warehouse & Hospitality Roles",
            "Hiring Event — April 9th",
            "Mt. Juliet, TN · Thu Apr 9",
            "Walk In, Walk Out Employed",
            "Indeed Flex Hiring Event",
            "$16–$18/Hr + Bonuses",
            "Apply in Minutes on Site",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Flex & Long-Term Shifts Open",
        ],
        "descriptions": [
            "Indeed Flex hiring event — walk in & get a job offer. Flex shifts + long-term work.",
            "Skip the wait. Interview live with recruiters on April 9 & start working this week.",
            "Warehouse, event staff & hospitality roles open. Walk in Apr 9, leave with an offer.",
            "Multiple openings at 1985 Providence Pkwy, Mt. Juliet TN. Walk in April 9 & get hired.",
        ],
    },
]

# ── App ad copy — 3 variants ──────────────────────────────────────────────
APP_AD_VARIANTS = [
    {
        "label": "Urgency",
        "headlines": [
            "Download App & Attend Apr 9",
            "Hiring Event — April 9th",
            "Warehouse & Event Staff $16+",
            "Limited Spots — Register Now",
            "Get Hired at Our Live Event",
        ],
        "descriptions": [
            "Download Indeed Flex & register for our Apr 9 hiring event in Mt. Juliet, TN.",
            "Warehouse, event staff & hospitality roles. Walk in Apr 9, 10am–2pm. Get hired.",
            "Limited spots available. Download the app & register for our Apr 9 event in TN.",
            "No long process. Download, sign up & attend our hiring event on April 9th.",
            "Get hired on April 9 in Mt. Juliet, TN. Download the Indeed Flex app now.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "headlines": [
            "Warehouse & Event Staff $16+",
            "$16–$18/Hr + Special Bonuses",
            "Same Day Pay Available",
            "Multiple Roles Nashville Area",
            "$75 Referral Bonus",
        ],
        "descriptions": [
            "Warehouse & event staff $16–$18/hr. Same Day Pay & $75 referral bonus. Download app.",
            "Download Indeed Flex, register for Apr 9 hiring event & earn $16–$18/hr in TN.",
            "$75 referral bonus, Same Day Pay & health benefits. Come to our Apr 9 event.",
            "Competitive pay + benefits. Download Indeed Flex & attend hiring event April 9.",
            "Same Day Pay, health/dental/vision. Join us Apr 9 at Goodwill Career Center, TN.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "headlines": [
            "Download App & Attend Apr 9",
            "Get Hired at Our Live Event",
            "Full-Time Potential Available",
            "No Long Interview Process",
            "Hiring Event — April 9th",
        ],
        "descriptions": [
            "Download Indeed Flex & come to our Apr 9 event. Walk in, get hired, start this week.",
            "Skip the wait — attend our live hiring event Apr 9 at Goodwill Career Center, TN.",
            "Warehouse, event staff & hospitality roles open. Download app, register, attend Apr 9.",
            "No lengthy process. Interview live Apr 9 in Mt. Juliet, TN. Download Indeed Flex today.",
            "Walk in on April 9, meet our recruiters & leave with a $16–$18/hr offer. Download now.",
        ],
    },
]

# ── Keywords ──────────────────────────────────────────────────────────────
HIRING_EVENT_KEYWORDS = [
    ("hiring event mt juliet", "EXACT"),
    ("hiring event nashville", "EXACT"),
    ("job fair nashville tennessee", "EXACT"),
    ("hiring event near me", "EXACT"),
    ("warehouse hiring event nashville", "EXACT"),
    ("hiring event mt juliet tn", "PHRASE"),
    ("hiring event nashville", "PHRASE"),
    ("job fair near me nashville", "PHRASE"),
    ("warehouse jobs mt juliet tn", "PHRASE"),
    ("event staff jobs nashville", "PHRASE"),
    ("immediate hire nashville warehouse", "PHRASE"),
    ("warehouse hiring event nashville tennessee", "BROAD"),
    ("get hired on the spot nashville", "BROAD"),
]

GENERIC_IMMEDIATE_KEYWORDS = [
    ("immediate warehouse jobs nashville", "PHRASE"),
    ("warehouse jobs hiring now nashville", "PHRASE"),
    ("warehouse jobs mt juliet tennessee", "PHRASE"),
    ("hospitality jobs nashville hiring now", "PHRASE"),
    ("warehouse worker nashville", "EXACT"),
]

WAREHOUSE_KEYWORDS = [
    ("warehouse jobs nashville tennessee", "PHRASE"),
    ("warehouse jobs near me nashville", "PHRASE"),
    ("warehouse worker mt juliet", "EXACT"),
    ("warehouse jobs wilson county tn", "PHRASE"),
]

EVENT_KEYWORD_TARGETS = {
    "p---generic_immediate--": GENERIC_IMMEDIATE_KEYWORDS,
    "p---warehouse--": WAREHOUSE_KEYWORDS,
}


# ── Resource helpers ──────────────────────────────────────────────────────

def ag_res(customer_id: str, ag_id: str) -> str:
    return f"customers/{customer_id}/adGroups/{ag_id}"


# ── Geo: find Mt. Juliet constant ─────────────────────────────────────────

def find_mt_juliet_geo_constant(client) -> str | None:
    """Returns the geo_target_constant resource name for Mt. Juliet, TN."""
    svc     = client.get_service("GeoTargetConstantService")
    request = client.get_type("SuggestGeoTargetConstantsRequest")
    request.locale       = "en"
    request.country_code = "US"
    request.location_names.names.append(MT_JULIET_GEO_QUERY)
    response = svc.suggest_geo_target_constants(request=request)
    for suggestion in response.geo_target_constant_suggestions:
        gtc = suggestion.geo_target_constant
        # Prefer city-level match for Mt. Juliet
        if "juliet" in gtc.name.lower():
            return gtc.resource_name
    return None


def add_geo_target(client, customer_id: str, campaign_rn: str, geo_constant_rn: str) -> None:
    svc = client.get_service("CampaignCriterionService")
    op  = client.get_type("CampaignCriterionOperation")
    cc  = op.create
    cc.campaign                       = campaign_rn
    cc.location.geo_target_constant   = geo_constant_rn
    cc.negative                       = False
    svc.mutate_campaign_criteria(customer_id=customer_id, operations=[op])
    print(f"  ✅ Mt. Juliet geo target added: {geo_constant_rn}")


# ── Budget ────────────────────────────────────────────────────────────────

def create_budget(client, customer_id: str, label: str) -> str:
    svc = client.get_service("CampaignBudgetService")
    op  = client.get_type("CampaignBudgetOperation")
    b   = op.create
    b.name            = f"Hiring Event Nashville {label} {EVENT_END_DATE}"
    b.amount_micros   = DAILY_BUDGET_MICROS
    b.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    result = svc.mutate_campaign_budgets(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ Budget created: {rn}")
    return rn


# ── Campaign fetch ────────────────────────────────────────────────────────

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
            "bid_modifier": cc.bid_modifier,
            "negative": cc.negative,
        })
    return results


# ── Campaign create ───────────────────────────────────────────────────────

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
    c.name            = name
    c.campaign_budget = budget_rn
    c.status          = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    c.end_date        = EVENT_END_DATE
    c.network_settings.target_google_search          = source.network_settings.target_google_search
    c.network_settings.target_search_network         = source.network_settings.target_search_network
    c.network_settings.target_content_network        = source.network_settings.target_content_network
    c.network_settings.target_partner_search_network = source.network_settings.target_partner_search_network
    _apply_bidding(client, c, source)
    result = svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ Search campaign created: {rn}")
    return rn


def create_app_campaign(client, customer_id: str, source, budget_rn: str, name: str) -> str:
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name            = name
    c.campaign_budget = budget_rn
    c.status          = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type     = client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL
    c.advertising_channel_sub_type = client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN
    c.end_date = EVENT_END_DATE
    c.app_campaign_setting.app_id                     = source.app_campaign_setting.app_id
    c.app_campaign_setting.app_store                  = source.app_campaign_setting.app_store
    c.app_campaign_setting.bidding_strategy_goal_type = (
        source.app_campaign_setting.bidding_strategy_goal_type
    )
    _apply_bidding(client, c, source)
    result = svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    rn = result.results[0].resource_name
    print(f"  ✅ App campaign created: {rn}")
    return rn


def copy_geo_targets(client, customer_id: str, geo_targets: list, campaign_rn: str) -> int:
    if not geo_targets:
        print("  ⚠️  No geo targets on source campaign — skipping")
        return 0
    svc = client.get_service("CampaignCriterionService")
    ops = []
    for gt in geo_targets:
        op = client.get_type("CampaignCriterionOperation")
        cc = op.create
        cc.campaign                       = campaign_rn
        cc.location.geo_target_constant   = gt["geo_target_constant"]
        cc.negative                       = gt["negative"]
        if gt["bid_modifier"] and gt["bid_modifier"] != 1.0:
            cc.bid_modifier = gt["bid_modifier"]
        ops.append(op)
    svc.mutate_campaign_criteria(customer_id=customer_id, operations=ops)
    print(f"  ✅ {len(ops)} geo target(s) copied from BAU")
    return len(ops)


# ── Ad group ──────────────────────────────────────────────────────────────

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
            "id": str(ag.id),
            "name": ag.name,
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


# ── Keywords ──────────────────────────────────────────────────────────────

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


# ── Ads ───────────────────────────────────────────────────────────────────

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


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    # Guard: source IDs must be set before running
    if "TODO" in (SOURCE_SEARCH_CAMPAIGN_ID, SOURCE_APP_CAMPAIGN_ID):
        print("\n❌ Set SOURCE_SEARCH_CAMPAIGN_ID and SOURCE_APP_CAMPAIGN_ID before running.")
        print("   Find them in Google Ads for campaigns matching:")
        print("   p-b2c-google-search-us-bofu-bau-nashville-*--eg--")
        print("   p-b2c-google-app-us-bofu-bau-nashville-*--eg--\n")
        raise SystemExit(1)

    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    cid    = CUSTOMER_ID

    print("\n══════════════════════════════════════════════════════════════")
    print("  Mt. Juliet / Nashville Hiring Event — Duplicate Campaign Launch")
    print("══════════════════════════════════════════════════════════════\n")

    # Look up Mt. Juliet geo target constant
    print("  Looking up Mt. Juliet, TN geo target constant...")
    mt_juliet_geo = find_mt_juliet_geo_constant(client)
    if mt_juliet_geo:
        print(f"  ✅ Found: {mt_juliet_geo}")
    else:
        print("  ⚠️  Mt. Juliet geo constant not found — geo expansion skipped")

    # ─────────────────────────────────────────────────────────────────────
    # SEARCH CAMPAIGN
    # ─────────────────────────────────────────────────────────────────────
    print("\n▶ SEARCH CAMPAIGN\n")

    print("  [1/4] Fetching BAU search campaign settings...")
    src_search  = fetch_campaign(client, cid, SOURCE_SEARCH_CAMPAIGN_ID)
    geo_targets = fetch_geo_targets(client, cid, SOURCE_SEARCH_CAMPAIGN_ID)

    print("\n  [2/4] Creating $50/day budget...")
    search_budget_rn = create_budget(client, cid, "Search")

    print("\n  [3/4] Creating duplicate search campaign...")
    search_campaign_rn = create_search_campaign(
        client, cid, src_search, search_budget_rn, SEARCH_EVENT_NAME
    )

    print(f"\n  [4/4] Copying {len(geo_targets)} geo target(s) + expanding to Mt. Juliet...")
    copy_geo_targets(client, cid, geo_targets, search_campaign_rn)
    if mt_juliet_geo:
        add_geo_target(client, cid, search_campaign_rn, mt_juliet_geo)

    print("\n  ── Ad Groups ──")
    source_ad_groups = fetch_ad_groups(client, cid, SOURCE_SEARCH_CAMPAIGN_ID)
    print(f"  Found {len(source_ad_groups)} source ad group(s)\n")

    for src_ag in source_ad_groups:
        print(f"  → {src_ag['name']}")
        new_ag_rn = create_search_ad_group(
            client, cid, search_campaign_rn, src_ag["name"], src_ag["cpc_bid_micros"]
        )
        keywords = fetch_keywords(client, cid, src_ag["id"])
        if keywords:
            print(f"    Copying {len(keywords)} keyword(s) from source...")
            add_keywords(client, cid, new_ag_rn, keywords)
        if src_ag["name"] in EVENT_KEYWORD_TARGETS:
            extra = EVENT_KEYWORD_TARGETS[src_ag["name"]]
            print(f"    Adding {len(extra)} event keyword(s)...")
            add_keywords(client, cid, new_ag_rn, extra)
        print("    Adding 3 RSA variants...")
        for i, variant in enumerate(RSA_VARIANTS, 1):
            rsa_rn = add_rsa(client, cid, new_ag_rn, variant)
            print(f"    ✅ RSA {i} [{variant['label']}]: {rsa_rn}")

    # New hiring event ad group
    print("\n  → Hiring Event — Mt. Juliet  (new)")
    hiring_ag_rn = create_search_ad_group(
        client, cid, search_campaign_rn, "Hiring Event — Mt. Juliet", 1_500_000
    )
    print(f"    Adding {len(HIRING_EVENT_KEYWORDS)} event keywords...")
    add_keywords(client, cid, hiring_ag_rn, HIRING_EVENT_KEYWORDS)
    print("    Adding 3 RSA variants...")
    for i, variant in enumerate(RSA_VARIANTS, 1):
        rsa_rn = add_rsa(client, cid, hiring_ag_rn, variant)
        print(f"    ✅ RSA {i} [{variant['label']}]: {rsa_rn}")

    # ─────────────────────────────────────────────────────────────────────
    # APP CAMPAIGN
    # ─────────────────────────────────────────────────────────────────────
    print("\n\n▶ APP CAMPAIGN\n")

    print("  [1/4] Fetching BAU app campaign settings...")
    src_app     = fetch_campaign(client, cid, SOURCE_APP_CAMPAIGN_ID)
    app_geo     = fetch_geo_targets(client, cid, SOURCE_APP_CAMPAIGN_ID)
    src_app_ags = fetch_ad_groups(client, cid, SOURCE_APP_CAMPAIGN_ID)

    print("\n  [2/4] Creating $50/day budget...")
    app_budget_rn = create_budget(client, cid, "App")

    print("\n  [3/4] Creating duplicate app campaign...")
    app_campaign_rn = create_app_campaign(
        client, cid, src_app, app_budget_rn, APP_EVENT_NAME
    )

    print(f"\n  [4/4] Copying {len(app_geo)} geo target(s) + expanding to Mt. Juliet...")
    copy_geo_targets(client, cid, app_geo, app_campaign_rn)
    if mt_juliet_geo:
        add_geo_target(client, cid, app_campaign_rn, mt_juliet_geo)

    ag_name = src_app_ags[0]["name"] if src_app_ags else "App Ads — Nashville Hiring Event"
    print(f"\n  Creating app ad group: {ag_name}")
    app_ag_rn = create_app_ad_group(client, cid, app_campaign_rn, ag_name)

    print("  Adding 3 app ad variants...")
    for i, variant in enumerate(APP_AD_VARIANTS, 1):
        ad_rn = add_app_ad(client, cid, app_ag_rn, variant)
        print(f"  ✅ App ad {i} [{variant['label']}]: {ad_rn}")

    # ─────────────────────────────────────────────────────────────────────
    print("\n══════════════════════════════════════════════════════════════")
    print("  ✅ Done! Both event campaigns are LIVE.")
    print(f"  Search : {SEARCH_EVENT_NAME}")
    print(f"  App    : {APP_EVENT_NAME}")
    print("  BAU campaigns remain untouched.")
    print("  Event  : April 9, 2026 · 10am–2pm · Goodwill Career Center, Mt. Juliet TN")
    print("  Post-event: Pause both event campaigns on April 9.")
    print("══════════════════════════════════════════════════════════════\n")


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
