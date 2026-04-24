#!/usr/bin/env python3
"""
Nashville, TN — Lettuce Dishwasher/Busser BAU Launch (Search + P.Max)
$30/day each | Maximize Conversions | Ongoing BAU (no end date)

Campaigns:
  Search — p-b2c-google-search-us-bofu-bau-nashville-hospitality-lettuce--eg--
  P.Max  — p-b2c-google-pmax-us-bofu-bau-nashville-hospitality-lettuce--eg--

Run: python3 scripts/google-ads-lettuce-dishwasher-nashville-tn.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Geo: copy from Nashville BAU Industrial Search ────────────────────────────
SOURCE_GEO_CAMPAIGN_ID = "23059952812"

# ── Budget ────────────────────────────────────────────────────────────────────
DAILY_BUDGET_MICROS = 30_000_000  # $30/day

# ── Campaign names ────────────────────────────────────────────────────────────
SEARCH_CAMPAIGN_NAME = "p-b2c-google-search-us-bofu-bau-nashville-hospitality-lettuce--eg--"
PMAX_CAMPAIGN_NAME   = "p-b2c-google-pmax-us-bofu-bau-nashville-hospitality-lettuce--eg--"

# ── Final URL ─────────────────────────────────────────────────────────────────
FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/dishwasher/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/500633"
    "&employer=NA"
    "&metro=nashville"
    "&role=dishwasher"
    "&utm_campaign=lettuce-dishwasher-nashville-tn"
)

# ── P.Max image assets (hospitality — Austin P.Max, same account) ─────────────
PMAX_SQUARE_IMAGE_ASSETS = [
    "customers/7236100723/assets/291706642784",
    "customers/7236100723/assets/291706644254",
    "customers/7236100723/assets/291706656743",
    "customers/7236100723/assets/291708559532",
    "customers/7236100723/assets/291708597794",
]
PMAX_LANDSCAPE_IMAGE_ASSETS = [
    "customers/7236100723/assets/291720404264",
    "customers/7236100723/assets/291720637037",
    "customers/7236100723/assets/291720641393",
    "customers/7236100723/assets/291720641555",
    "customers/7236100723/assets/291720643124",
]
PMAX_PORTRAIT_IMAGE_ASSETS = [
    "customers/7236100723/assets/291708597920",
    "customers/7236100723/assets/291708604025",
]
PMAX_LOGO_ASSETS = [
    "customers/7236100723/assets/56893637546",   # Square logo RGB
    "customers/7236100723/assets/56893637654",   # Square logo alt
]
PMAX_LANDSCAPE_LOGO_ASSETS = [
    "customers/7236100723/assets/56894244206",   # Landscape logo RGB
    "customers/7236100723/assets/56938308459",   # Landscape logo alt
]

# ── Business Name asset (campaign-level link for Search) ─────────────────────
BUSINESS_NAME_ASSET_RN = "customers/7236100723/assets/11226590211"

# ── Ad groups (3) ─────────────────────────────────────────────────────────────
AD_GROUPS = [
    {
        "name": "p---dishwasher_jobs--",
        "keywords": [
            ("dishwasher jobs nashville", "PHRASE"),
            ("dishwasher jobs nashville tn", "PHRASE"),
            ("dishwasher work nashville", "PHRASE"),
            ("dishwasher positions nashville", "PHRASE"),
            ("dishwasher hiring nashville tn", "PHRASE"),
            ("dishwasher jobs near me", "PHRASE"),
            ("dishwasher roles nashville", "PHRASE"),
            ("dishwasher employment nashville", "PHRASE"),
        ],
    },
    {
        "name": "p---kitchen_jobs--",
        "keywords": [
            ("kitchen jobs nashville tn", "PHRASE"),
            ("kitchen worker jobs nashville", "PHRASE"),
            ("kitchen staff hiring nashville", "PHRASE"),
            ("back of house jobs nashville", "PHRASE"),
            ("kitchen aide jobs nashville tn", "PHRASE"),
            ("kitchen help jobs nashville", "PHRASE"),
            ("kitchen work nashville", "PHRASE"),
            ("food prep jobs nashville tn", "PHRASE"),
        ],
    },
    {
        "name": "p---restaurant_jobs--",
        "keywords": [
            ("restaurant jobs nashville tn", "PHRASE"),
            ("restaurant work nashville", "PHRASE"),
            ("food service jobs nashville", "PHRASE"),
            ("hospitality jobs nashville tn", "PHRASE"),
            ("restaurant staff jobs nashville", "PHRASE"),
            ("restaurant jobs hiring now nashville", "PHRASE"),
            ("restaurant worker nashville tn", "PHRASE"),
        ],
    },
]

# ── Campaign-level negative keywords (18) ────────────────────────────────────
NEGATIVE_KEYWORDS = [
    "cook", "chef", "server", "bartender", "cashier", "manager",
    "supervisor", "host", "hostess", "delivery driver", "remote",
    "work from home", "fast food", "free dishwasher", "buy dishwasher",
    "used dishwasher", "dishwasher repair", "dishwasher machine",
]

# ── RSA variants (3) — applied to all 3 ad groups ────────────────────────────
RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Kitchen-Jobs",
        "path2": "Nashville-TN",
        "headlines": [
            "Dishwasher Jobs Nashville TN",
            "Hiring Now \u2014 Start This Week",
            "Restaurant Jobs Hiring Fast",
            "$18/Hr Kitchen Work",
            "Apply Today and Start Soon",
            "Same Day Pay Available",
            "Upscale Restaurant Openings",
            "No Experience Required",
            "Limited Spots Available",
            "Get Hired This Week",
            "Indeed Flex Hiring Now",
            "Dishwasher Shifts Open",
            "Nashville Kitchen Jobs",
            "Flexible Hours Available",
            "Apply Free in Minutes",
        ],
        "descriptions": [
            "Dishwasher jobs at upscale Nashville restaurants. $18/hr and Same Day Pay. Apply free now.",
            "Kitchen jobs hiring now in Nashville, TN. $18/hr, flexible shifts, no experience required.",
            "Upscale Nashville restaurants hiring dishwashers. Flexible hours, $18/hr, temp to perm.",
            "Get hired this week. Dishwasher and busser roles open in Nashville. No resume needed.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Kitchen-Jobs",
        "path2": "Nashville-TN",
        "headlines": [
            "$18/Hr Dishwasher Work",
            "Same Day Pay Available",
            "Temp to Perm Opportunity",
            "Health Benefits Included",
            "$75 Referral Bonus",
            "Competitive Pay Plus Benefits",
            "Get Paid the Same Day",
            "Dishwasher Jobs Nashville",
            "Kitchen Roles Paying $18/Hr",
            "Weekly or Daily Pay Options",
            "Health Dental Vision Plans",
            "Upscale Restaurant Roles",
            "No Experience Needed",
            "Apply Free \u2014 Work This Week",
            "Full Benefits Available",
        ],
        "descriptions": [
            "Earn $18/hr at upscale Nashville restaurants. Same Day Pay, health benefits. Apply free.",
            "Dishwasher role. $18/hr, $75 referral bonus, Same Day Pay, health, dental, and vision.",
            "Temp-to-perm dishwasher jobs in Nashville. $18/hr with comprehensive health benefits.",
            "Choose daily or weekly pay. Dishwasher and busser roles in Nashville, TN. Start this week.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "path1": "Kitchen-Jobs",
        "path2": "Nashville-TN",
        "headlines": [
            "Apply in Under 2 Minutes",
            "No Long Application",
            "Start Working This Week",
            "Dishwasher Jobs Near Me",
            "Temp to Perm in Nashville",
            "No Experience Needed",
            "Kitchen Work Near Nashville",
            "$18/Hr Quick Hire",
            "Free to Apply Today",
            "Same Day Pay Option",
            "Grow Your Kitchen Career",
            "Flexible Kitchen Schedule",
            "Indeed Flex Nashville TN",
            "Restaurant Jobs Apply Free",
            "Get Hired This Week",
        ],
        "descriptions": [
            "Apply in minutes for dishwasher roles at upscale Nashville restaurants. $18/hr. No resume.",
            "No experience needed. Dishwasher and busser roles in Nashville, TN. Could become perm.",
            "Pick your own kitchen shifts in Nashville. Get paid daily or weekly. $18/hr. Apply free.",
            "Temp-to-perm kitchen opportunity in Nashville. $18/hr, flexible hours. Grow your career.",
        ],
    },
]

# ── P.Max text assets ─────────────────────────────────────────────────────────
PMAX_HEADLINES = [
    "Dishwasher Jobs Nashville TN",
    "Hiring Now \u2014 Start This Week",
    "Restaurant Jobs Hiring Fast",
    "$18/Hr Kitchen Work",
    "Apply Today and Start Soon",
    "Same Day Pay Available",
    "Upscale Restaurant Openings",
    "No Experience Required",
    "Limited Spots Available",
    "Get Hired This Week",
    "Indeed Flex Hiring Now",
    "Dishwasher Shifts Open",
    "Nashville Kitchen Jobs",
    "Flexible Hours Available",
    "Apply Free in Minutes",
]

PMAX_LONG_HEADLINES = [
    "Dishwasher jobs in Nashville, TN. $18/hr, Same Day Pay, and health benefits.",
    "Hiring Dishwashers for upscale Nashville restaurants. $18/hr. No experience required.",
    "Temp-to-perm Dishwasher roles in Nashville, TN. $18/hr, Same Day Pay, health benefits.",
    "Pick your kitchen shifts in Nashville. Get paid daily. $18/hr. Apply free today.",
    "No experience needed. Dishwasher and busser jobs in Nashville TN. Start this week.",
]

PMAX_DESCRIPTIONS = [
    "Dishwasher jobs at upscale Nashville restaurants. $18/hr and Same Day Pay. Apply free now.",
    "Upscale Nashville restaurants hiring now. $18/hr, flexible hours. No resume needed.",
    "Get Same Day Pay, a $75 referral bonus, and health benefits. Start dishwashing this week.",
    "Temp-to-perm in Nashville. Flexible scheduling, no experience needed. Start ASAP.",
    "Choose your shifts. Get paid daily. Dishwasher and busser jobs in Nashville, TN.",
]

# ── Ad Extensions ─────────────────────────────────────────────────────────────
SITELINKS = [
    {
        "link_text":    "Browse Dishwasher Jobs",
        "description1": "See all kitchen roles near you",
        "description2": "Apply free on Indeed Flex",
        "final_url":    FINAL_URL,
    },
    {
        "link_text":    "Download the App",
        "description1": "Get the Indeed Flex app",
        "description2": "Pick your shifts from your phone",
        "final_url":    "https://indeedflex.com/",
    },
    {
        "link_text":    "Same Day Pay",
        "description1": "Get paid the same day you work",
        "description2": "Choose daily or weekly pay",
        "final_url":    "https://indeedflex.com/",
    },
    {
        "link_text":    "Health Benefits",
        "description1": "Health, dental and vision",
        "description2": "Plus $75 referral bonus",
        "final_url":    "https://indeedflex.com/",
    },
    {
        "link_text":    "Flexible Schedules",
        "description1": "Work when it works for you",
        "description2": "Choose shifts that fit you",
        "final_url":    "https://indeedflex.com/",
    },
    {
        "link_text":    "Temp to Perm Jobs",
        "description1": "Start temp, build a career",
        "description2": "Dishwasher to permanent roles",
        "final_url":    FINAL_URL,
    },
]

CALLOUTS = [
    "$18/Hr Kitchen Work",
    "Same Day Pay Available",
    "No Experience Required",
    "$75 Referral Bonus",
    "Health Benefits Included",
    "Temp to Perm Opportunity",
]

STRUCTURED_SNIPPETS = [
    {
        "header": "Types",
        "values": ["Dishwasher", "Busser", "Kitchen Helper", "Food Service Worker"],
    },
    {
        "header": "Amenities",
        "values": ["Same-Day Pay", "Health Benefits", "Flexible Scheduling", "$75 Referral Bonus"],
    },
    {
        "header": "Service catalog",
        "values": ["Morning Shifts", "Evening Shifts", "Weekend Shifts", "Weekday Shifts"],
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def create_budget(client, label):
    svc = client.get_service("CampaignBudgetService")
    op  = client.get_type("CampaignBudgetOperation")
    b   = op.create
    b.name              = f"BAU Nashville Dishwasher {label}"
    b.amount_micros     = DAILY_BUDGET_MICROS
    b.delivery_method   = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    rn = svc.mutate_campaign_budgets(
        customer_id=CUSTOMER_ID, operations=[op]
    ).results[0].resource_name
    print(f"  \u2705 Budget created: {rn}")
    return rn


def fetch_geo_targets(client):
    """Copy geo target constants from Nashville BAU Industrial Search campaign."""
    ga_svc = client.get_service("GoogleAdsService")
    query = f"""
        SELECT campaign_criterion.location.geo_target_constant
        FROM campaign_criterion
        WHERE campaign.id = {SOURCE_GEO_CAMPAIGN_ID}
          AND campaign_criterion.type = 'LOCATION'
          AND campaign_criterion.negative = FALSE
    """
    geo_rns = []
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=query):
        geo_rns.append(row.campaign_criterion.location.geo_target_constant)
    print(f"  \u2705 {len(geo_rns)} geo target(s) fetched from Nashville BAU")
    return geo_rns


def set_geo_targets(client, campaign_rn, geo_rns):
    svc = client.get_service("CampaignCriterionService")
    ops = []
    for geo_rn in geo_rns:
        op = client.get_type("CampaignCriterionOperation")
        cc = op.create
        cc.campaign = campaign_rn
        cc.location.geo_target_constant = geo_rn
        cc.negative = False
        ops.append(op)
    svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f"  \u2705 {len(ops)} geo target(s) applied")


def add_campaign_negative_keywords(client, campaign_rn, negatives):
    svc = client.get_service("CampaignCriterionService")
    ops = []
    for text in negatives:
        op = client.get_type("CampaignCriterionOperation")
        cc = op.create
        cc.campaign            = campaign_rn
        cc.negative            = True
        cc.keyword.text        = text
        cc.keyword.match_type  = client.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
    svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f"  \u2705 {len(ops)} campaign-level negative keywords added")


def create_search_ad_group(client, campaign_rn, name):
    svc = client.get_service("AdGroupService")
    op  = client.get_type("AdGroupOperation")
    ag  = op.create
    ag.name           = name
    ag.campaign       = campaign_rn
    ag.status         = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_          = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag.cpc_bid_micros = 2_500_000  # $2.50 max CPC
    return svc.mutate_ad_groups(
        customer_id=CUSTOMER_ID, operations=[op]
    ).results[0].resource_name


def add_keywords(client, ag_rn, keywords):
    svc = client.get_service("AdGroupCriterionService")
    ops = []
    for text, match in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        c  = op.create
        c.ad_group           = ag_rn
        c.status             = client.enums.AdGroupCriterionStatusEnum.ENABLED
        c.keyword.text       = text
        c.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match)
        ops.append(op)
    svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f"    \u2705 {len(ops)} keywords added")


def add_rsa(client, ag_rn, variant):
    svc = client.get_service("AdGroupAdService")
    op  = client.get_type("AdGroupAdOperation")
    ada = op.create
    ada.ad_group = ag_rn
    ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
    ad           = ada.ad
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
    return svc.mutate_ad_group_ads(
        customer_id=CUSTOMER_ID, operations=[op]
    ).results[0].resource_name


# ── Extension asset creators ──────────────────────────────────────────────────

def create_sitelink_asset(client, sitelink):
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    sl    = asset.sitelink_asset
    sl.link_text    = sitelink["link_text"]
    sl.description1 = sitelink["description1"]
    sl.description2 = sitelink["description2"]
    asset.final_urls.append(sitelink["final_url"])
    return svc.mutate_assets(
        customer_id=CUSTOMER_ID, operations=[op]
    ).results[0].resource_name


def create_callout_asset(client, callout_text):
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    asset.callout_asset.callout_text = callout_text
    return svc.mutate_assets(
        customer_id=CUSTOMER_ID, operations=[op]
    ).results[0].resource_name


def create_snippet_asset(client, snippet):
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    ss    = asset.structured_snippet_asset
    ss.header = snippet["header"]
    for v in snippet["values"]:
        ss.values.append(v)
    return svc.mutate_assets(
        customer_id=CUSTOMER_ID, operations=[op]
    ).results[0].resource_name


def link_asset_to_campaign(client, asset_rn, campaign_rn, field_type_name):
    svc = client.get_service("CampaignAssetService")
    op  = client.get_type("CampaignAssetOperation")
    ca  = op.create
    ca.asset      = asset_rn
    ca.campaign   = campaign_rn
    ca.field_type = getattr(client.enums.AssetFieldTypeEnum, field_type_name)
    svc.mutate_campaign_assets(customer_id=CUSTOMER_ID, operations=[op])


def create_and_link_extensions(client, search_camp_rn, pmax_camp_rn):
    """Create all extension assets once and link to both campaigns."""
    print("\n  \u2500\u2500 Creating extension assets \u2500\u2500")

    sl_rns = []
    for sl in SITELINKS:
        rn = create_sitelink_asset(client, sl)
        sl_rns.append(rn)
        print(f"  \u2705 Sitelink: \"{sl['link_text']}\"")

    co_rns = []
    for co in CALLOUTS:
        rn = create_callout_asset(client, co)
        co_rns.append(rn)
        print(f"  \u2705 Callout: \"{co}\"")

    ss_rns = []
    for ss in STRUCTURED_SNIPPETS:
        rn = create_snippet_asset(client, ss)
        ss_rns.append(rn)
        print(f"  \u2705 Snippet: \"{ss['header']}\"")

    print("\n  \u2500\u2500 Linking extensions to campaigns \u2500\u2500")
    for camp_label, camp_rn in [("Search", search_camp_rn), ("P.Max", pmax_camp_rn)]:
        print(f"\n  {camp_label} ({camp_rn.split('/')[-1]}):")
        for sl_rn, sl in zip(sl_rns, SITELINKS):
            link_asset_to_campaign(client, sl_rn, camp_rn, "SITELINK")
            print(f"    \u2705 Sitelink: \"{sl['link_text']}\"")
        for co_rn, co in zip(co_rns, CALLOUTS):
            link_asset_to_campaign(client, co_rn, camp_rn, "CALLOUT")
            print(f"    \u2705 Callout: \"{co}\"")
        for ss_rn, ss in zip(ss_rns, STRUCTURED_SNIPPETS):
            link_asset_to_campaign(client, ss_rn, camp_rn, "STRUCTURED_SNIPPET")
            print(f"    \u2705 Snippet: \"{ss['header']}\"")

    # Business Name — Search campaign only (graceful for P.Max which has it via asset group)
    try:
        link_asset_to_campaign(client, BUSINESS_NAME_ASSET_RN, search_camp_rn, "BUSINESS_NAME")
        print(f"\n  \u2705 Business Name linked to Search campaign")
    except GoogleAdsException:
        print(f"\n  \u26a0\ufe0f  Business Name already linked or not supported \u2014 skipped")


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 1: SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

def build_search_campaign(client, geo_rns):
    print("\n\u25b6  SEARCH CAMPAIGN\n")

    budget_rn = create_budget(client, "Search")

    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name            = SEARCH_CAMPAIGN_NAME
    c.campaign_budget = budget_rn
    c.status          = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type                        = client.enums.AdvertisingChannelTypeEnum.SEARCH
    c.network_settings.target_google_search           = True
    c.network_settings.target_search_network          = True
    c.network_settings.target_content_network         = False
    c.network_settings.target_partner_search_network  = False
    c.maximize_conversions.target_cpa_micros           = 0
    c.contains_eu_political_advertising                = 3  # DOES_NOT_CONTAIN
    camp_rn = svc.mutate_campaigns(
        customer_id=CUSTOMER_ID, operations=[op]
    ).results[0].resource_name
    print(f"  \u2705 Search campaign: {camp_rn}")

    print(f"  Setting geo targets...")
    set_geo_targets(client, camp_rn, geo_rns)

    print(f"  Adding campaign-level negative keywords...")
    add_campaign_negative_keywords(client, camp_rn, NEGATIVE_KEYWORDS)

    print(f"\n  \u2500\u2500 Ad Groups \u2500\u2500")
    for ag_def in AD_GROUPS:
        print(f"\n  \u2192 {ag_def['name']}")
        ag_rn = create_search_ad_group(client, camp_rn, ag_def["name"])
        add_keywords(client, ag_rn, ag_def["keywords"])
        for i, variant in enumerate(RSA_VARIANTS, 1):
            rsa_rn = add_rsa(client, ag_rn, variant)
            print(f"    \u2705 RSA {i} [{variant['label']}]: {rsa_rn.split('/')[-1]}")

    return camp_rn


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 2: PERFORMANCE MAX
# ═══════════════════════════════════════════════════════════════════════════════

def build_pmax_campaign(client, geo_rns):
    print("\n\u25b6  PERFORMANCE MAX CAMPAIGN\n")

    budget_rn = create_budget(client, "PMax")

    # Step 1: Create P.Max campaign
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.create
    c.name                               = PMAX_CAMPAIGN_NAME
    c.campaign_budget                    = budget_rn
    c.status                             = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type           = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    c.maximize_conversions.target_cpa_micros = 0
    c.brand_guidelines_enabled           = False
    c.contains_eu_political_advertising  = 3  # DOES_NOT_CONTAIN
    camp_rn = svc.mutate_campaigns(
        customer_id=CUSTOMER_ID, operations=[op]
    ).results[0].resource_name
    print(f"  \u2705 P.Max campaign: {camp_rn}")

    # Step 2: Geo targets
    print(f"  Setting geo targets...")
    set_geo_targets(client, camp_rn, geo_rns)

    # Step 3: Atomic batch — asset group + text assets + image links
    print(f"  Building asset group batch...")
    ga_svc  = client.get_service("GoogleAdsService")
    AGA     = client.enums.AssetFieldTypeEnum
    ag_tmp  = f"customers/{CUSTOMER_ID}/assetGroups/-1"
    counter = [-1]
    create_ops = []
    link_ops   = []

    # Asset group
    ag_op = client.get_type("MutateOperation")
    ag    = ag_op.asset_group_operation.create
    ag.resource_name = ag_tmp
    ag.campaign      = camp_rn
    ag.name          = "Dishwasher / Busser \u2014 Nashville TN"
    ag.final_urls.append(FINAL_URL)
    ag.status        = client.enums.AssetGroupStatusEnum.ENABLED
    create_ops.append(ag_op)

    def add_text_asset(text, field_type_enum):
        counter[0] -= 1
        asset_tmp = f"customers/{CUSTOMER_ID}/assets/{counter[0]}"
        a_op = client.get_type("MutateOperation")
        a    = a_op.asset_operation.create
        a.resource_name   = asset_tmp
        a.text_asset.text = text
        create_ops.append(a_op)
        aga_op = client.get_type("MutateOperation")
        aga    = aga_op.asset_group_asset_operation.create
        aga.asset_group = ag_tmp
        aga.asset       = asset_tmp
        aga.field_type  = field_type_enum
        link_ops.append(aga_op)

    def link_existing_asset(asset_rn, field_type_enum):
        aga_op = client.get_type("MutateOperation")
        aga    = aga_op.asset_group_asset_operation.create
        aga.asset_group = ag_tmp
        aga.asset       = asset_rn
        aga.field_type  = field_type_enum
        link_ops.append(aga_op)

    # Text assets
    add_text_asset("Indeed Flex", AGA.BUSINESS_NAME)
    for h in PMAX_HEADLINES:
        add_text_asset(h, AGA.HEADLINE)
    for lh in PMAX_LONG_HEADLINES:
        add_text_asset(lh, AGA.LONG_HEADLINE)
    for d in PMAX_DESCRIPTIONS:
        add_text_asset(d, AGA.DESCRIPTION)

    # Image assets
    for rn in PMAX_LOGO_ASSETS:
        link_existing_asset(rn, AGA.LOGO)
    for rn in PMAX_LANDSCAPE_LOGO_ASSETS:
        link_existing_asset(rn, AGA.LANDSCAPE_LOGO)
    for rn in PMAX_SQUARE_IMAGE_ASSETS:
        link_existing_asset(rn, AGA.SQUARE_MARKETING_IMAGE)
    for rn in PMAX_LANDSCAPE_IMAGE_ASSETS:
        link_existing_asset(rn, AGA.MARKETING_IMAGE)
    for rn in PMAX_PORTRAIT_IMAGE_ASSETS:
        link_existing_asset(rn, AGA.PORTRAIT_MARKETING_IMAGE)

    all_ops = create_ops + link_ops
    print(f"  Batch: {len(create_ops)} creates + {len(link_ops)} links = {len(all_ops)} ops")
    response = ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=all_ops)

    for r in response.mutate_operation_responses:
        kind = r.WhichOneof("response")
        if kind == "asset_group_result":
            print(f"  \u2705 Asset group: {r.asset_group_result.resource_name}")

    print(f"  \u2705 {len(PMAX_HEADLINES)} headlines + {len(PMAX_LONG_HEADLINES)} long headlines + {len(PMAX_DESCRIPTIONS)} descriptions loaded")
    img_count = (len(PMAX_LOGO_ASSETS) + len(PMAX_LANDSCAPE_LOGO_ASSETS) +
                 len(PMAX_SQUARE_IMAGE_ASSETS) + len(PMAX_LANDSCAPE_IMAGE_ASSETS) +
                 len(PMAX_PORTRAIT_IMAGE_ASSETS))
    print(f"  \u2705 {img_count} image/logo assets linked")

    return camp_rn


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n" + "\u2550" * 65)
    print("  Nashville, TN \u2014 Lettuce Dishwasher/Busser BAU Launch")
    print("  Search + P.Max | $30/day each | Maximize Conversions")
    print("\u2550" * 65 + "\n")

    # Fetch geo targets from Nashville BAU (shared by both campaigns)
    print("\u25b6  Fetching geo targets from Nashville BAU Industrial Search...\n")
    geo_rns = fetch_geo_targets(client)

    # Build campaigns
    search_camp_rn = build_search_campaign(client, geo_rns)
    pmax_camp_rn   = build_pmax_campaign(client, geo_rns)

    # Extensions — create once, link to both
    print("\n\u25b6  EXTENSIONS\n")
    create_and_link_extensions(client, search_camp_rn, pmax_camp_rn)

    # Summary
    search_id = search_camp_rn.split("/")[-1]
    pmax_id   = pmax_camp_rn.split("/")[-1]

    print("\n" + "\u2550" * 65)
    print("  \u2705 LAUNCH COMPLETE")
    print("\u2550" * 65)
    print(f"  Search:  {SEARCH_CAMPAIGN_NAME}")
    print(f"  ID:      {search_id}")
    print(f"  P.Max:   {PMAX_CAMPAIGN_NAME}")
    print(f"  ID:      {pmax_id}")
    print(f"  Budget:  $30/day each ($60/day total)")
    print(f"  Geo:     Nashville, TN (copied from BAU)")
    print(f"  Status:  ENABLED (live)")
    print(f"  Ad groups: 3 | RSAs: 9 | Keywords: 23 (PHRASE) | Negatives: 18")
    print(f"  Extensions: 6 sitelinks + 6 callouts + 3 snippets + Business Name")
    print(f"  P.Max assets: 15 HL + 5 LH + 5 Desc + {len(PMAX_SQUARE_IMAGE_ASSETS)+len(PMAX_LANDSCAPE_IMAGE_ASSETS)+len(PMAX_PORTRAIT_IMAGE_ASSETS)} images + logos")
    print("\u2550" * 65 + "\n")


if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"\n\u274c Google Ads API error:")
        for error in ex.failure.errors:
            print(f"  [{error.error_code}] {error.message}")
            if error.location:
                for fv in error.location.field_path_elements:
                    print(f"    Field: {fv.field_name} (index {fv.index})")
        raise SystemExit(1)
