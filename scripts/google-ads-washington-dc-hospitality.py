"""
Google Ads — Washington DC Hospitality BAU Campaigns
Created: 2026-04-07

Campaigns (all start PAUSED):
  1. Search  — p-b2c-google-search-us-bofu-bau-washington_DC-hospitality--eg--   $40/day
  2. P.Max   — p-b2c-google-p_max-us-bofu-bau-washington_DC-hospitality--eg--    $40/day
  3. Display — p-b2c-google_display-us-bofu-bau-washington_DC-hospitality-eg     $40/day

Roles: Barista, Server, Cashier, Prep Cook, Line Cook, Dishwasher
Assets copied from: Dallas hospitality search, Austin P.Max hospitality, Chicago display
"""

import sys
sys.path.insert(0, '/Users/claudio.santos/RM-Team-Ai')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "7236100723"
DAILY_BUDGET_MICROS = 40_000_000  # $40/day

# Washington DC geo constants
DC_SEARCH_URL = (
    "https://indeedflex.com/job-search/?search"
    "&area_name=Washington+DC"
    "&search_lat=38.9072&search_lon=-77.0369"
    "&top_lon=-76.9094&top_lat=38.9948"
    "&bot_lon=-77.1198&bot_lat=38.7916"
)
DC_PMAX_URL = (
    "https://indeedflex.com/find-jobs/lp/hospitality-general-labor/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/"
    "&metro=washington-dc&role=hospitality-general-labor"
    "&utm_campaign=EVG-Washington-DC"
)
DC_DISPLAY_URL = DC_SEARCH_URL

# Washington DC geo target constants
GEO_DC_CITY = "geoTargetConstants/1014895"    # Washington, DC (city)
GEO_DC_DMA  = "geoTargetConstants/200511"     # Washington DC DMA (metro area)

# Campaign names
SEARCH_CAMPAIGN_NAME = "p-b2c-google-search-us-bofu-bau-washington_DC-hospitality--eg--"
PMAX_CAMPAIGN_NAME   = "p-b2c-google-p_max-us-bofu-bau-washington_DC-hospitality--eg--"
DISPLAY_CAMPAIGN_NAME = "p-b2c-google_display-us-bofu-bau-washington_DC-hospitality-eg"

# ── Asset resource names to reuse (from Austin P.Max hospitality) ─────────────
PMAX_LOGO_ASSETS = [
    "customers/7236100723/assets/56893637546",
    "customers/7236100723/assets/56893637654",
]
PMAX_LANDSCAPE_LOGO_ASSETS = [
    "customers/7236100723/assets/56894244206",
    "customers/7236100723/assets/56938308459",
]
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
PMAX_VIDEO_ASSETS = [
    "customers/7236100723/assets/289151280210",  # PdOcqYzcM3Y
    "customers/7236100723/assets/289151280213",  # VHtQjtm6iIE
    "customers/7236100723/assets/289151280216",  # nQ28UpGww7Q
]

# ── Display image assets (from Chicago display) ───────────────────────────────
DISPLAY_LANDSCAPE_IMAGES = [
    "customers/7236100723/assets/57266992600",
    "customers/7236100723/assets/57049714005",
    "customers/7236100723/assets/57267614870",
    "customers/7236100723/assets/57267410318",
]
DISPLAY_SQUARE_IMAGES = [
    "customers/7236100723/assets/57005716753",
    "customers/7236100723/assets/57267994867",
    "customers/7236100723/assets/57312737502",
    "customers/7236100723/assets/57267410954",
]
DISPLAY_LOGOS = [
    "customers/7236100723/assets/56938308459",
    "customers/7236100723/assets/56894244206",
]

# ── Keywords per ad group ─────────────────────────────────────────────────────
KEYWORDS = {
    "Barista": [
        ("barista job", "EXACT"),
        ("barista jobs", "EXACT"),
        ("barista jobs near me", "EXACT"),
        ("barista jobs near me", "PHRASE"),
        ("barista hiring", "EXACT"),
        ("barista hiring near me", "PHRASE"),
        ("barista position", "EXACT"),
        ("barista position", "PHRASE"),
        ("coffee shop jobs", "PHRASE"),
        ("coffee shop jobs near me", "PHRASE"),
        ("part time barista jobs", "EXACT"),
        ("part time barista jobs", "PHRASE"),
        ("barista jobs hiring near me", "PHRASE"),
        ("barista job near me", "PHRASE"),
        ("barista job near me", "EXACT"),
        ("indeed barista jobs", "PHRASE"),
        ("barista jobs washington dc", "EXACT"),
        ("barista jobs dc", "PHRASE"),
        ("cafe barista jobs", "PHRASE"),
        ("barista job description", "PHRASE"),
    ],
    "Server": [
        ("server jobs", "PHRASE"),
        ("server jobs near me", "PHRASE"),
        ("server jobs hiring near me", "PHRASE"),
        ("restaurant server", "EXACT"),
        ("restaurant server", "PHRASE"),
        ("waitress jobs", "PHRASE"),
        ("waiter job", "PHRASE"),
        ("waiter jobs near me", "EXACT"),
        ("serving jobs", "PHRASE"),
        ("banquet server", "PHRASE"),
        ("banquet server jobs", "PHRASE"),
        ("event server", "PHRASE"),
        ("event server jobs", "PHRASE"),
        ("part time server jobs", "EXACT"),
        ("part time server jobs", "PHRASE"),
        ("servers hiring near me", "PHRASE"),
        ("restaurants hiring servers near me", "PHRASE"),
        ("indeed server jobs", "PHRASE"),
        ("server jobs washington dc", "EXACT"),
        ("banquet jobs near me", "PHRASE"),
    ],
    "Cashier": [
        ("cashier jobs", "EXACT"),
        ("cashier jobs near me", "EXACT"),
        ("cashier jobs near me", "PHRASE"),
        ("cashier job", "EXACT"),
        ("cashier job", "PHRASE"),
        ("cashier hiring near me", "PHRASE"),
        ("cashier position", "EXACT"),
        ("cashier position", "PHRASE"),
        ("part time cashier jobs", "EXACT"),
        ("part time cashier jobs", "PHRASE"),
        ("cashier jobs hiring near me", "PHRASE"),
        ("restaurant cashier job", "PHRASE"),
        ("food service cashier", "PHRASE"),
        ("cashier no experience", "PHRASE"),
        ("indeed cashier jobs", "PHRASE"),
        ("cashier jobs dc", "PHRASE"),
        ("cashier jobs washington dc", "EXACT"),
        ("front counter jobs", "PHRASE"),
    ],
    "Prep Cook": [
        ("prep cook jobs near me", "PHRASE"),
        ("prep cook", "PHRASE"),
        ("prep cook jobs", "BROAD"),
        ("prep cook jobs hiring near me", "PHRASE"),
        ("part time prep cook jobs near me", "PHRASE"),
        ("kitchen prep jobs near me", "PHRASE"),
        ("prep cook hiring near me", "PHRASE"),
        ("indeed prep cook", "PHRASE"),
        ("prep cook job", "EXACT"),
        ("prep cook position", "PHRASE"),
        ("prep cook washington dc", "EXACT"),
        ("kitchen jobs near me", "PHRASE"),
    ],
    "Line Cook": [
        ("line cook", "PHRASE"),
        ("line cook job", "PHRASE"),
        ("line cook jobs near me", "PHRASE"),
        ("line cook hiring", "PHRASE"),
        ("line cook jobs hiring near me", "PHRASE"),
        ("line cook indeed", "PHRASE"),
        ("indeed line cook", "PHRASE"),
        ("line cook position", "PHRASE"),
        ("line cook washington dc", "EXACT"),
        ("restaurant cook jobs near me", "PHRASE"),
        ("cook jobs near me", "PHRASE"),
        ("cook jobs hiring", "PHRASE"),
    ],
    "Dishwasher": [
        ("dishwasher job", "EXACT"),
        ("dishwasher job", "PHRASE"),
        ("dishwasher jobs hiring", "EXACT"),
        ("dishwasher jobs hiring", "PHRASE"),
        ("restaurant dishwasher", "EXACT"),
        ("restaurant dishwasher", "PHRASE"),
        ("restaurant dishwasher job", "EXACT"),
        ("restaurant dishwasher job", "PHRASE"),
        ("dishwasher hiring", "EXACT"),
        ("dishwasher hiring", "PHRASE"),
        ("dishwasher position", "EXACT"),
        ("dishwasher position", "PHRASE"),
        ("dish washing jobs", "EXACT"),
        ("dish washing jobs", "PHRASE"),
        ("part time dishwasher jobs", "EXACT"),
        ("part time dishwasher jobs", "PHRASE"),
        ("dishwasher job washington dc", "EXACT"),
        ("indeed dishwasher jobs", "PHRASE"),
    ],
}

# ── RSA copy (DC-adapted from Dallas hospitality) ─────────────────────────────
RSA_HEADLINES = [
    "{KeyWord:Flexible Jobs Washington DC}",
    "Your App for Temporary Work",
    "Find Flexible Jobs",
    "Unlock Job Opportunities",
    "Work on Your Own Terms",
    "Get Hired Today",
    "Empower Your Career",
    "Find Flexible Work Today",
    "Get Instant Job Offers Today",
    "Choose Where & How to Work",
    "Find Your Ideal Job",
    "Easy Sign Up",
    "Work, Your Way",
    "Same Day Pay Available Now",
    "Choose When You Get Paid",
]
RSA_DESCRIPTIONS = [
    "Indeed Flex offers job seekers a fast way to find work that fits their lifestyle.",
    "Choose your employer and manage your own work schedule with Indeed Flex.",
    "No resume required - Apply today! Book an interview to get started.",
    "Join Indeed Flex with flexible, well-paying jobs.",
]

# ── P.Max text assets (DC-adapted from Austin P.Max) ─────────────────────────
PMAX_HEADLINES = [
    "Direct Access to Flexible Jobs",
    "Hiring Now: Hospitality Jobs",
    "Find Jobs Near You Now",
    "Indeed Flex - Get Hired Fast",
    "Flexible Hospitality Roles",
    "Apply For New Hospitality Jobs",
    "Hospitality Jobs in DC",
    "Join Indeed Flex in DC",
    "New Jobs in Washington DC",
]
PMAX_LONG_HEADLINES = [
    "Indeed Flex is Your Temporary Work App - No Resume Required, Apply and Interview Today",
    "Indeed Flex is hiring now in DC. Apply for hospitality jobs with flexible shifts.",
    "Get hired fast for hospitality jobs in DC. Indeed Flex is offering flexible roles.",
    "Apply for a hospitality job today in Washington DC with Indeed Flex. Apply in minutes.",
    "Join Indeed Flex for hospitality roles in DC. Start working fast with same-day-pay.",
]
PMAX_DESCRIPTIONS = [
    "Indeed Flex offers hospitality job seekers a fast way to find work in Washington DC",
    "Hiring fast in DC! Find flexible hospitality jobs with Indeed Flex now.",
    "No resume required - Apply for hospitality jobs in DC and book an interview today!",
    "Looking for work in Washington DC? Apply for hospitality jobs today with Indeed Flex.",
    "Hospitality roles in DC are hiring! Indeed Flex offers same-day-pay & flexibility.",
]
PMAX_BUSINESS_NAME = "Indeed Flex"


def get_client():
    return GoogleAdsClient.load_from_storage('/Users/claudio.santos/RM-Team-Ai/google-ads.yaml')


def create_budget(client, name):
    campaign_budget_service = client.get_service("CampaignBudgetService")
    op = client.get_type("CampaignBudgetOperation")
    budget = op.create
    budget.name = name
    budget.amount_micros = DAILY_BUDGET_MICROS
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    budget.explicitly_shared = False
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=CUSTOMER_ID, operations=[op]
    )
    rn = response.results[0].resource_name
    print(f"  ✅ Budget created: {rn}")
    return rn


def add_geo_target(client, campaign_rn):
    service = client.get_service("CampaignCriterionService")
    ops = []
    for geo_rn, label in [(GEO_DC_CITY, "Washington DC city"), (GEO_DC_DMA, "DC metro DMA")]:
        op = client.get_type("CampaignCriterionOperation")
        cc = op.create
        cc.campaign = campaign_rn
        cc.location.geo_target_constant = geo_rn
        ops.append(op)
    service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    print(f"  ✅ Geo targets added: Washington DC city + metro DMA")


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 1: SEARCH
# ═══════════════════════════════════════════════════════════════════════════════

def create_search_campaign(client):
    print("\n── Creating Search Campaign ──")
    # Budget already created (ID 15483720947) — reuse it
    budget_rn = "customers/7236100723/campaignBudgets/15483720947"
    print(f"  ✅ Budget reused: {budget_rn}")

    service = client.get_service("CampaignService")
    op = client.get_type("CampaignOperation")
    camp = op.create
    camp.name = SEARCH_CAMPAIGN_NAME
    camp.status = client.enums.CampaignStatusEnum.PAUSED
    camp.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    camp.campaign_budget = budget_rn
    camp.maximize_conversions.target_cpa_micros = 0
    camp.contains_eu_political_advertising = 3  # DOES_NOT_CONTAIN

    # Network settings
    camp.network_settings.target_google_search = True
    camp.network_settings.target_search_network = True
    camp.network_settings.target_content_network = False

    response = service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[op])
    camp_rn = response.results[0].resource_name
    print(f"  ✅ Search campaign: {camp_rn}")

    add_geo_target(client, camp_rn)
    return camp_rn


def create_search_ad_groups(client, campaign_rn):
    ad_group_service = client.get_service("AdGroupService")
    ad_group_ad_service = client.get_service("AdGroupAdService")
    criterion_service = client.get_service("AdGroupCriterionService")

    SKIP_CREATED = {"Barista"}  # already created in previous run
    for role_name, keywords in KEYWORDS.items():
        if role_name in SKIP_CREATED:
            print(f"\n  Ad Group: {role_name} [SKIPPED — already created]")
            continue
        print(f"\n  Ad Group: {role_name}")

        # Create ad group
        ag_op = client.get_type("AdGroupOperation")
        ag = ag_op.create
        ag.name = f"Job Type (Hospitality) - {role_name}"
        ag.campaign = campaign_rn
        ag.status = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ag_resp = ad_group_service.mutate_ad_groups(
            customer_id=CUSTOMER_ID, operations=[ag_op]
        )
        ag_rn = ag_resp.results[0].resource_name
        print(f"    ✅ Ad group created: {ag_rn.split('/')[-1]}")

        # Create RSA
        ad_op = client.get_type("AdGroupAdOperation")
        ad = ad_op.create
        ad.ad_group = ag_rn
        ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        rsa = ad.ad.responsive_search_ad

        for h_text in RSA_HEADLINES:
            h = client.get_type("AdTextAsset")
            h.text = h_text
            rsa.headlines.append(h)
        for d_text in RSA_DESCRIPTIONS:
            d = client.get_type("AdTextAsset")
            d.text = d_text
            rsa.descriptions.append(d)
        ad.ad.final_urls.append(DC_SEARCH_URL)

        ad_group_ad_service.mutate_ad_group_ads(
            customer_id=CUSTOMER_ID, operations=[ad_op]
        )
        print(f"    ✅ RSA created")

        # Create keywords
        kw_ops = []
        for kw_text, match_type in keywords:
            kw_op = client.get_type("AdGroupCriterionOperation")
            kw = kw_op.create
            kw.ad_group = ag_rn
            kw.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw.keyword.text = kw_text
            kw.keyword.match_type = getattr(
                client.enums.KeywordMatchTypeEnum, match_type
            )
            kw_ops.append(kw_op)
        criterion_service.mutate_ad_group_criteria(
            customer_id=CUSTOMER_ID, operations=kw_ops
        )
        print(f"    ✅ {len(kw_ops)} keywords created")


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 2: PERFORMANCE MAX
# ═══════════════════════════════════════════════════════════════════════════════

def create_pmax_campaign(client, existing_camp_rn=None):
    print("\n── Creating Performance Max Campaign ──")
    ga_service = client.get_service("GoogleAdsService")

    if existing_camp_rn:
        camp_rn = existing_camp_rn
        print(f"  ✅ Reusing existing P.Max campaign: {camp_rn}")
    else:
        # Create budget + campaign
        budget_rn = create_budget(client, f"Budget - {PMAX_CAMPAIGN_NAME}")
        camp_service = client.get_service("CampaignService")
        camp_op = client.get_type("CampaignOperation")
        c = camp_op.create
        c.name = PMAX_CAMPAIGN_NAME
        c.status = client.enums.CampaignStatusEnum.PAUSED
        c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
        c.campaign_budget = budget_rn
        c.maximize_conversions.target_cpa_micros = 0
        c.brand_guidelines_enabled = False
        c.contains_eu_political_advertising = 3
        camp_resp = camp_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[camp_op])
        camp_rn = camp_resp.results[0].resource_name
        print(f"  ✅ P.Max campaign: {camp_rn}")
        add_geo_target(client, camp_rn)

    # Step 2: Batch mutate — asset group + assets only
    # Key: creates ops first, link ops last (Nashville pattern)
    ag_tmp = f"customers/{CUSTOMER_ID}/assetGroups/-1"
    create_ops = []   # asset group + text asset creates
    link_ops = []     # AssetGroupAsset links (all at the end)
    counter = [-1]    # first asset gets -2 (no collision with ag_tmp -1)

    # Asset group
    ag_op = client.get_type("MutateOperation")
    ag = ag_op.asset_group_operation.create
    ag.resource_name = ag_tmp
    ag.campaign = camp_rn
    ag.name = "washington-dc-hospitality-all"
    ag.final_urls.append(DC_PMAX_URL)
    ag.status = client.enums.AssetGroupStatusEnum.ENABLED
    create_ops.append(ag_op)

    # Text assets: create goes to create_ops, link goes to link_ops
    AGA = client.enums.AssetFieldTypeEnum

    def add_text_asset(text, field_type_enum):
        counter[0] -= 1
        asset_tmp = f"customers/{CUSTOMER_ID}/assets/{counter[0]}"
        a_op = client.get_type("MutateOperation")
        a = a_op.asset_operation.create
        a.resource_name = asset_tmp
        a.text_asset.text = text
        create_ops.append(a_op)
        aga_op = client.get_type("MutateOperation")
        aga = aga_op.asset_group_asset_operation.create
        aga.asset_group = ag_tmp
        aga.asset = asset_tmp
        aga.field_type = field_type_enum
        link_ops.append(aga_op)

    def link_existing_asset(asset_rn, field_type_enum):
        aga_op = client.get_type("MutateOperation")
        aga = aga_op.asset_group_asset_operation.create
        aga.asset_group = ag_tmp
        aga.asset = asset_rn
        aga.field_type = field_type_enum
        link_ops.append(aga_op)

    add_text_asset(PMAX_BUSINESS_NAME, AGA.BUSINESS_NAME)
    for h in PMAX_HEADLINES:
        add_text_asset(h, AGA.HEADLINE)
    for lh in PMAX_LONG_HEADLINES:
        add_text_asset(lh, AGA.LONG_HEADLINE)
    for d in PMAX_DESCRIPTIONS:
        add_text_asset(d, AGA.DESCRIPTION)

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
    for rn in PMAX_VIDEO_ASSETS:
        link_existing_asset(rn, AGA.YOUTUBE_VIDEO)

    all_ops = create_ops + link_ops
    print(f"  Batch: {len(create_ops)} creates + {len(link_ops)} links = {len(all_ops)} ops")
    response = ga_service.mutate(customer_id=CUSTOMER_ID, mutate_operations=all_ops)
    print(f"  ✅ P.Max campaign + asset group created ({len(all_ops)} operations)")
    for r in response.mutate_operation_responses:
        kind = r.WhichOneof("response")
        if kind == "campaign_result":
            print(f"  ✅ Campaign: {r.campaign_result.resource_name}")
        elif kind == "asset_group_result":
            print(f"  ✅ Asset group: {r.asset_group_result.resource_name}")


# ═══════════════════════════════════════════════════════════════════════════════
# CAMPAIGN 3: DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════

def create_display_campaign(client):
    print("\n── Creating Display Campaign ──")
    budget_rn = create_budget(client, f"Budget - {DISPLAY_CAMPAIGN_NAME}")

    # Campaign
    camp_service = client.get_service("CampaignService")
    camp_op = client.get_type("CampaignOperation")
    c = camp_op.create
    c.name = DISPLAY_CAMPAIGN_NAME
    c.status = client.enums.CampaignStatusEnum.PAUSED
    c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.DISPLAY
    c.campaign_budget = budget_rn
    c.maximize_conversions.target_cpa_micros = 0
    c.network_settings.target_content_network = True
    c.contains_eu_political_advertising = 3  # DOES_NOT_CONTAIN

    camp_resp = camp_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[camp_op])
    camp_rn = camp_resp.results[0].resource_name
    print(f"  ✅ Display campaign: {camp_rn}")

    add_geo_target(client, camp_rn)

    # Ad groups (3 audience segments)
    ag_service = client.get_service("AdGroupService")
    ad_service = client.get_service("AdGroupAdService")

    audience_segments = [
        "site_visitors",
        "verified_users",
        "app_download_not_verified",
    ]

    for segment in audience_segments:
        ag_name = f"washington_DC_none_none_none_{segment}"

        ag_op = client.get_type("AdGroupOperation")
        ag = ag_op.create
        ag.name = ag_name
        ag.campaign = camp_rn
        ag.status = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_ = client.enums.AdGroupTypeEnum.DISPLAY_STANDARD

        ag_resp = ag_service.mutate_ad_groups(
            customer_id=CUSTOMER_ID, operations=[ag_op]
        )
        ag_rn = ag_resp.results[0].resource_name
        print(f"  ✅ Display ad group: {ag_name}")

        # Responsive Display Ad
        ad_op = client.get_type("AdGroupAdOperation")
        ada = ad_op.create
        ada.ad_group = ag_rn
        ada.status = client.enums.AdGroupAdStatusEnum.ENABLED

        rda = ada.ad.responsive_display_ad
        rda.business_name = "Indeed Flex"
        rda.long_headline.text = "Indeed Flex is the #1 Temp job solution for flexible hospitality roles."

        for h_text in [
            "Apply for Flex Jobs Now",
            "No Experience Required",
            "Hospitality Jobs in DC",
            "Book an Interview Today",
            "Start Booking Shifts",
        ]:
            h = client.get_type("AdTextAsset")
            h.text = h_text
            rda.headlines.append(h)

        for d_text in [
            "Join Indeed Flex to take control of your work schedule and choose your own employer.",
            "No resume or experience needed - book an interview today!",
            "Get well-paying, flexible hospitality jobs with Indeed Flex in Washington DC.",
            "No experience required! Apply and book an interview today.",
        ]:
            d = client.get_type("AdTextAsset")
            d.text = d_text
            rda.descriptions.append(d)

        for rn in DISPLAY_LANDSCAPE_IMAGES:
            img = client.get_type("AdImageAsset")
            img.asset = rn
            rda.marketing_images.append(img)
        for rn in DISPLAY_SQUARE_IMAGES:
            img = client.get_type("AdImageAsset")
            img.asset = rn
            rda.square_marketing_images.append(img)
        for rn in DISPLAY_LOGOS:
            logo = client.get_type("AdImageAsset")
            logo.asset = rn
            rda.logo_images.append(logo)

        ada.ad.final_urls.append(DC_DISPLAY_URL)

        ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
        print(f"    ✅ Responsive Display Ad created for {segment}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("Washington DC Hospitality — Campaign Creation")
    print("=" * 60)

    client = get_client()

    try:
        # 1. Search — DONE (campaign 23732428286, geo + 6 ad groups complete)
        print("\n── Search Campaign ── ALREADY COMPLETE (23732428286)")

        # 2. P.Max — DONE (campaign 23727227430, asset group 6697567319, 39 assets linked)
        print("\n── P.Max Campaign ── ALREADY COMPLETE (23727227430 / ag 6697567319)")

        # 3. Display
        create_display_campaign(client)

        print("\n" + "=" * 60)
        print("✅ ALL 3 CAMPAIGNS CREATED (PAUSED)")
        print("=" * 60)
        print(f"  Search:  {SEARCH_CAMPAIGN_NAME}")
        print(f"  P.Max:   {PMAX_CAMPAIGN_NAME}")
        print(f"  Display: {DISPLAY_CAMPAIGN_NAME}")
        print(f"  Budget:  $40/day each")
        print(f"  Geo:     Washington DC")
        print(f"  Roles:   Barista, Server, Cashier, Prep Cook, Line Cook, Dishwasher")
        print(f"  Status:  PAUSED — enable manually when ready")

    except GoogleAdsException as ex:
        print(f"\n❌ Google Ads API error:")
        for error in ex.failure.errors:
            print(f"  [{error.error_code}] {error.message}")
            if error.location:
                for fv in error.location.field_path_elements:
                    print(f"    Field: {fv.field_name} (index {fv.index})")
        raise


if __name__ == "__main__":
    main()
