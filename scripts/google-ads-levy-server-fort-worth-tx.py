#!/usr/bin/env python3
"""
BAU Search + P.Max + App campaigns for Event Server role in Fort Worth, TX.
Client: Levy Restaurants (not mentioned in ads)
8-ad-group structure (Phoenix BAU model)

Run: python3 scripts/google-ads-levy-server-fort-worth-tx.py
"""

import urllib.request, urllib.parse, json, time
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/server/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/500267"
    "&employer=levy-restaurants"
    "&metro=dallas"
    "&role=server"
    "&utm_campaign=server-levy-fort-worth-tx"
)

SOURCE_APP_ID   = "23062774690"
SOURCE_PMAX_ID  = "23043219989"
DAILY_BUDGET    = 30_000_000  # $30/day

# ═══════════════════════════════════════════════════════════════════════════
# GEO — 20-mile radius from Fort Worth TX 76103
# ═══════════════════════════════════════════════════════════════════════════
def geocode(address):
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json&limit=1"
    req = urllib.request.Request(url, headers={"User-Agent": "IndeedFlex-GeoScript/1.0"})
    resp = json.loads(urllib.request.urlopen(req).read())
    return float(resp[0]["lat"]), float(resp[0]["lon"])

# ═══════════════════════════════════════════════════════════════════════════
# AD GROUPS — 8-group Phoenix BAU model
# ═══════════════════════════════════════════════════════════════════════════
AD_GROUPS = [
    {
        "name": "Event Server — Fort Worth TX",
        "cpc_bid_micros": 2_500_000,
        "keywords": [
            ("event server jobs fort worth", "PHRASE"),
            ("banquet server jobs fort worth", "PHRASE"),
            ("catering server fort worth tx", "PHRASE"),
            ("event server jobs dallas fort worth", "PHRASE"),
            ("fine dining server jobs fort worth", "PHRASE"),
            ("upscale event server fort worth", "PHRASE"),
            ("server jobs fort worth tx", "PHRASE"),
        ],
    },
    {
        "name": "Server Jobs — Fort Worth Dallas",
        "cpc_bid_micros": 2_500_000,
        "keywords": [
            ("server jobs fort worth", "PHRASE"),
            ("server jobs dallas area", "PHRASE"),
            ("server hiring now fort worth", "PHRASE"),
            ("restaurant server jobs fort worth", "PHRASE"),
            ("server jobs near me fort worth", "PHRASE"),
            ("part time server jobs fort worth", "PHRASE"),
        ],
    },
    {
        "name": "Hospitality Jobs — Fort Worth TX",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("hospitality jobs fort worth", "PHRASE"),
            ("hospitality jobs hiring now fort worth", "PHRASE"),
            ("hospitality work fort worth tx", "PHRASE"),
            ("hospitality temp jobs fort worth", "PHRASE"),
            ("event staff jobs fort worth", "PHRASE"),
            ("banquet staff jobs fort worth", "PHRASE"),
        ],
    },
    {
        "name": "p---generic_immediate--",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("immediate start jobs", "PHRASE"),
            ("immediate start jobs fort worth", "PHRASE"),
            ("jobs hiring immediately near me", "PHRASE"),
            ("hiring immediately hospitality", "PHRASE"),
            ("start work this week", "PHRASE"),
            ("jobs you can start immediately", "PHRASE"),
        ],
    },
    {
        "name": "p---temp_keywords-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("temp agency", "PHRASE"),
            ("temp work agency", "PHRASE"),
            ("temping agencies", "PHRASE"),
            ("temping agency", "PHRASE"),
            ("temporary recruitment agency", "PHRASE"),
            ("temp staffing agency fort worth", "PHRASE"),
            ("temp jobs fort worth tx", "PHRASE"),
        ],
    },
    {
        "name": "p-hospitality---server",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("server temporary jobs", "PHRASE"),
            ("part time server jobs", "PHRASE"),
            ("server flexible shifts", "PHRASE"),
            ("hospitality temporary jobs", "PHRASE"),
            ("part time hospitality jobs", "PHRASE"),
            ("weekend server jobs", "PHRASE"),
            ("temporary hospitality jobs fort worth", "PHRASE"),
            ("event staff hiring now", "PHRASE"),
        ],
    },
    {
        "name": "p---generic-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("temp jobs", "PHRASE"),
            ("temporary jobs", "PHRASE"),
            ("weekend jobs", "PHRASE"),
            ("flexible jobs fort worth", "PHRASE"),
            ("part time jobs fort worth tx", "PHRASE"),
            ("temporary jobs fort worth", "PHRASE"),
        ],
    },
    {
        "name": "p---agency_keywords-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("job agency", "PHRASE"),
            ("employment agency", "PHRASE"),
            ("recruitment agency", "PHRASE"),
            ("staffing agency fort worth", "PHRASE"),
            ("job agency fort worth tx", "PHRASE"),
            ("agency jobs", "PHRASE"),
        ],
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# RSA VARIANTS — 3 angles based on top Dallas/Austin hospitality performers
# ═══════════════════════════════════════════════════════════════════════════
RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Hospitality",
        "path2": "Fort-Worth-TX",
        "headlines": [
            "Hospitality Jobs Hiring Now",
            "Event Server — Apply Today",
            "Fort Worth · Start This Week",
            "Flex Jobs in Fort Worth TX",
            "Server Jobs — Hiring Now",
            "Choose Where & How to Work",
            "Upscale Events Near You",
            "Indeed Flex Hiring Now",
            "$18–$25/Hr Event Server",
            "Manage Your Own Schedule",
            "Work That Suits Your Lifestyle",
            "Same Day Pay Available",
            "No Long Application Process",
            "Limited Spots — Apply Now",
            "Event Staff — Fort Worth",
        ],
        "descriptions": [
            "Hospitality jobs $18–$25/hr · Fort Worth TX. Flexible event server shifts. Apply now.",
            "Pick your shifts, work upscale events & get paid same day. Server roles available now.",
            "Indeed Flex connects you to top hospitality events in Fort Worth. Start working this week.",
            "Flexible server roles near you. $18–$25/hr, same day pay & health benefits available.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Server-Jobs",
        "path2": "Fort-Worth-TX",
        "headlines": [
            "$18–$25/Hr Event Server Jobs",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Health & Vision Benefits",
            "Flex Jobs in Fort Worth TX",
            "Choose Where & How to Work",
            "Hospitality Jobs Hiring Now",
            "Manage Your Own Schedule",
            "Earn $18–$25/Hr This Week",
            "Get Paid Same or Next Day",
            "Health & Dental Coverage",
            "Work That Suits Your Lifestyle",
            "Upscale Events Near Fort Worth",
            "Flexible Shifts Available",
            "Indeed Flex Hiring Now",
        ],
        "descriptions": [
            "Server roles $18–$25/hr. Same Day Pay & health benefits. Apply on Indeed Flex today.",
            "$75 per referral, Same Day Pay & full health benefits. Pick your shifts in Fort Worth.",
            "Competitive pay $18–$25/hr, flexible scheduling & Same Day Pay. Apply in minutes.",
            "Top hospitality pay in Fort Worth. $18–$25/hr + health, dental & vision benefits.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "path1": "Hospitality",
        "path2": "Fort-Worth",
        "headlines": [
            "No Long Application Process",
            "Apply in Minutes on the App",
            "Choose Where & How to Work",
            "Work Upscale Events Near You",
            "Flex Jobs in Fort Worth TX",
            "Manage Your Own Schedule",
            "Hospitality Jobs Hiring Now",
            "Work That Suits Your Lifestyle",
            "Server Jobs — Start This Week",
            "$18–$25/Hr · Fort Worth TX",
            "Indeed Flex Hiring Now",
            "Same Day Pay Available",
            "Flexible 1st & 2nd Shifts",
            "Full-Time Potential Available",
            "Event Server — Fort Worth",
        ],
        "descriptions": [
            "Indeed Flex: pick your shifts, work great events & get paid fast. Apply in minutes.",
            "Skip the wait. Browse server jobs in Fort Worth & start working this week.",
            "Flexible opportunities at upscale venues. Choose your own schedule. Apply now.",
            "Full-time potential with flexible scheduling. $18–$25/hr in Fort Worth area.",
        ],
    },
]

NEGATIVE_KEYWORDS = [
    "indeed flex jobs", "indeed flex app", "indeed flex login",
    "indeedflex", "full time", "manager", "supervisor",
    "bartender", "cook", "chef", "dishwasher",
]

SITELINKS = [
    ("Browse Server Jobs",     "Find event server shifts near Fort Worth, TX",
     FINAL_URL),
    ("Download the App",       "Get the Indeed Flex app to find & manage shifts",
     "https://indeedflex.com/download-app/"),
    ("$18–$25/Hr Pay",         "Competitive hourly pay for upscale event servers",
     FINAL_URL),
    ("Same Day Pay Info",      "Get paid the same or next day after your shift",
     "https://indeedflex.com/same-day-pay/"),
    ("How It Works",           "Pick your shifts, work events, get paid fast",
     "https://indeedflex.com/how-it-works/"),
    ("Benefits Overview",      "Health, dental & vision coverage for eligible workers",
     "https://indeedflex.com/benefits/"),
]

CALLOUTS = [
    "Same Day Pay Available",
    "$18–$25/Hr Event Server",
    "Flexible Shift Scheduling",
    "$75 Referral Bonus",
    "Health & Dental Benefits",
    "No Experience Barrier",
]

STRUCTURED_SNIPPETS = [
    ("Types",           ["Event Server", "Banquet Server", "Catering Staff", "Hospitality Staff"]),
    ("Service catalog", ["Same-Day Pay", "Health Benefits", "Flexible Shifts", "$75 Referral Bonus"]),
    ("Styles",          ["Weekday Lunches", "Weekend Evenings", "Special Events", "Upscale Venues"]),
]

# PMax image assets from Dallas hospitality (categorised by ratio)
PMAX_IMAGES = {
    "MARKETING_IMAGE": [        # 1.91:1 landscape
        288919633267, 288933458070, 288933458130,
        288933459582, 288933460908, 289540062732,
    ],
    "SQUARE_MARKETING_IMAGE": [ # 1:1 square
        288919672387, 288919674808, 288933453255,
        289522940611, 289540128777, 290462572331,
        290547064534, 291706642784, 291706644254,
    ],
    "PORTRAIT_MARKETING_IMAGE": [ # 4:5 portrait
        289522856428, 290462520782, 290547143980,
    ],
}

PMAX_TEXT = {
    "headlines": [
        "Hospitality Jobs Hiring Now",
        "Event Server — Fort Worth TX",
        "Flex Jobs in Fort Worth TX",
        "$18–$25/Hr Server Roles",
        "Choose Where & How to Work",
        "Work Upscale Events Near You",
        "Manage Your Own Schedule",
        "Same Day Pay Available",
        "Apply in Minutes on the App",
        "Server Jobs — Start This Week",
        "Work That Suits Your Lifestyle",
        "Indeed Flex Hiring Now",
        "$75 Referral Bonus",
        "Flexible Shifts Available",
        "Top Hospitality Pay — Apply",
    ],
    "long_headlines": [
        "Event Server Jobs in Fort Worth TX — $18–$25/Hr, Flexible Shifts",
        "Hospitality Jobs Hiring Now in Fort Worth — Choose Your Own Schedule",
        "Find Server Roles at Upscale Events Near Fort Worth, Texas",
        "Work Upscale Events & Get Paid Same Day — Fort Worth Hospitality",
        "Indeed Flex: Pick Your Shifts, Work Events, Earn $18–$25/Hr",
    ],
    "descriptions": [
        "Server jobs $18–$25/hr near Fort Worth TX. Same Day Pay & health benefits. Apply now.",
        "Pick your own shifts at upscale events. Earn $18–$25/hr. Same Day Pay available.",
        "Flexible server roles at top venues near Fort Worth, TX. Apply on the Indeed Flex app.",
        "Hospitality jobs hiring now in Fort Worth. $18–$25/hr + benefits + $75 referral bonus.",
        "Choose when and where you work. Event server roles available across Fort Worth, TX.",
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════
def add_proximity(crit_svc, client, campaign_rn, lat, lon, radius=20):
    op   = client.get_type("CampaignCriterionOperation")
    c    = op.create
    c.campaign = campaign_rn
    c.status   = client.enums.CampaignCriterionStatusEnum.ENABLED
    prox = c.proximity
    prox.geo_point.latitude_in_micro_degrees  = int(lat * 1_000_000)
    prox.geo_point.longitude_in_micro_degrees = int(lon * 1_000_000)
    prox.radius       = radius
    prox.radius_units = client.enums.ProximityRadiusUnitsEnum.MILES
    crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=[op])


def add_negative_keywords(crit_svc, client, campaign_rn):
    ops = []
    for kw in NEGATIVE_KEYWORDS:
        op = client.get_type("CampaignCriterionOperation")
        c  = op.create
        c.campaign             = campaign_rn
        c.negative             = True
        c.keyword.text         = kw
        c.keyword.match_type   = client.enums.KeywordMatchTypeEnum.PHRASE
        ops.append(op)
    crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)


def add_sitelinks(ga_svc, client, campaign_rn):
    ops = []
    for title, desc, url in SITELINKS:
        asset_op  = client.get_type("MutateOperation")
        sl        = asset_op.asset_operation.create
        sl.sitelink_asset.link_text  = title
        sl.sitelink_asset.description1 = desc[:35]
        sl.sitelink_asset.description2 = "Apply on Indeed Flex today"
        sl.final_urls.append(url)
        ops.append(asset_op)
    resp = ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=ops)
    asset_rns = [r.asset_result.resource_name for r in resp.mutate_operation_responses]

    link_ops = []
    for rn in asset_rns:
        op = client.get_type("MutateOperation")
        ca = op.campaign_asset_operation.create
        ca.campaign   = campaign_rn
        ca.asset      = rn
        ca.field_type = client.enums.AssetFieldTypeEnum.SITELINK
        link_ops.append(op)
    ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=link_ops)
    return len(asset_rns)


def add_callouts(ga_svc, client, campaign_rn):
    ops = []
    for text in CALLOUTS:
        op = client.get_type("MutateOperation")
        a  = op.asset_operation.create
        a.callout_asset.callout_text = text
        ops.append(op)
    resp     = ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=ops)
    asset_rns = [r.asset_result.resource_name for r in resp.mutate_operation_responses]
    link_ops = []
    for rn in asset_rns:
        op = client.get_type("MutateOperation")
        ca = op.campaign_asset_operation.create
        ca.campaign   = campaign_rn
        ca.asset      = rn
        ca.field_type = client.enums.AssetFieldTypeEnum.CALLOUT
        link_ops.append(op)
    ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=link_ops)


def add_snippets(ga_svc, client, campaign_rn):
    ops = []
    for header, values in STRUCTURED_SNIPPETS:
        op = client.get_type("MutateOperation")
        a  = op.asset_operation.create
        a.structured_snippet_asset.header = header
        a.structured_snippet_asset.values.extend(values)
        ops.append(op)
    resp     = ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=ops)
    asset_rns = [r.asset_result.resource_name for r in resp.mutate_operation_responses]
    link_ops = []
    for rn in asset_rns:
        op = client.get_type("MutateOperation")
        ca = op.campaign_asset_operation.create
        ca.campaign   = campaign_rn
        ca.asset      = rn
        ca.field_type = client.enums.AssetFieldTypeEnum.STRUCTURED_SNIPPET
        link_ops.append(op)
    ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=link_ops)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════
def main():
    client   = GoogleAdsClient.load_from_storage(YAML_PATH)
    ga_svc   = client.get_service("GoogleAdsService")
    bud_svc  = client.get_service("CampaignBudgetService")
    camp_svc = client.get_service("CampaignService")
    ag_svc   = client.get_service("AdGroupService")
    ad_svc   = client.get_service("AdGroupAdService")
    crit_svc = client.get_service("AdGroupCriterionService")
    c_crit   = client.get_service("CampaignCriterionService")


    print("\n═══════════════════════════════════════════════════════════════")
    print("  Fort Worth Hospitality — Event Server BAU")
    print("  Search + P.Max + App  |  $30/day each")
    print("═══════════════════════════════════════════════════════════════\n")

    # ── Geocode ──
    print("── Geocoding Fort Worth TX 76103 ──")
    lat, lon = geocode("Fort Worth, TX 76103")
    print(f"  lat={lat}  lon={lon}\n")
    time.sleep(1)

    # ── Source App settings ──
    q = f"""
        SELECT campaign.app_campaign_setting.app_id,
               campaign.app_campaign_setting.app_store,
               campaign.app_campaign_setting.bidding_strategy_goal_type
        FROM campaign WHERE campaign.id = {SOURCE_APP_ID}
    """
    app_row = list(ga_svc.search(customer_id=CUSTOMER_ID, query=q))[0]
    app_setting = app_row.campaign.app_campaign_setting

    # ── Source PMax images ──
    q2 = f"""
        SELECT asset.id, asset.image_asset.full_size.width_pixels,
               asset.image_asset.full_size.height_pixels
        FROM asset_group_asset
        WHERE campaign.id = {SOURCE_PMAX_ID} AND asset.type = 'IMAGE'
    """
    seen = set()
    pmax_assets = {"MARKETING_IMAGE": [], "SQUARE_MARKETING_IMAGE": [], "PORTRAIT_MARKETING_IMAGE": []}
    for row in ga_svc.search(customer_id=CUSTOMER_ID, query=q2):
        aid = row.asset.id
        if aid in seen: continue
        seen.add(aid)
        w, h = row.asset.image_asset.full_size.width_pixels, row.asset.image_asset.full_size.height_pixels
        ratio = w / h if h else 0
        if 1.85 <= ratio <= 1.95:
            pmax_assets["MARKETING_IMAGE"].append(aid)
        elif 0.75 <= ratio <= 0.85:
            pmax_assets["PORTRAIT_MARKETING_IMAGE"].append(aid)
        elif 0.9 <= ratio <= 1.1:
            pmax_assets["SQUARE_MARKETING_IMAGE"].append(aid)
    print(f"── PMax images from source: {sum(len(v) for v in pmax_assets.values())} assets ──")
    if sum(len(v) for v in pmax_assets.values()) < 5:
        print("  ⚠ Supplementing with known Dallas hospitality assets")
        for ft, ids in PMAX_IMAGES.items():
            for aid in ids:
                if aid not in pmax_assets[ft]:
                    pmax_assets[ft].append(aid)
    print(f"  Landscape={len(pmax_assets['MARKETING_IMAGE'])}  Square={len(pmax_assets['SQUARE_MARKETING_IMAGE'])}  Portrait={len(pmax_assets['PORTRAIT_MARKETING_IMAGE'])}\n")

    # ════════════════════════════════════════════════════════════════════
    # SEARCH CAMPAIGN
    # ════════════════════════════════════════════════════════════════════
    print("── Creating Search Campaign ──")
    bud_op = client.get_type("CampaignBudgetOperation")
    b = bud_op.create
    b.name              = "BAU Fort Worth Hospitality Search"
    b.amount_micros     = DAILY_BUDGET
    b.explicitly_shared = False
    bud_rn = bud_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[bud_op]).results[0].resource_name

    camp_op = client.get_type("CampaignOperation")
    c = camp_op.create
    c.name                              = "p-b2c-google-search-us-bofu-bau-fort_worth-hospitality-eg"
    c.advertising_channel_type          = client.enums.AdvertisingChannelTypeEnum.SEARCH
    c.status                            = client.enums.CampaignStatusEnum.ENABLED
    c.campaign_budget                   = bud_rn
    c.contains_eu_political_advertising = 3
    c.maximize_conversions.target_cpa_micros = 0
    c.network_settings.target_google_search  = True
    c.network_settings.target_search_network = True
    c.network_settings.target_content_network = False
    search_rn = camp_svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[camp_op]).results[0].resource_name
    search_id = search_rn.split("/")[-1]
    print(f"  ✅ Search campaign: {c.name}  (ID: {search_id})")

    add_proximity(c_crit, client, search_rn, lat, lon)
    print(f"  ✅ 20-mile radius geo target set")
    add_negative_keywords(c_crit, client, search_rn)
    print(f"  ✅ {len(NEGATIVE_KEYWORDS)} negative keywords added")

    n_sitelinks = add_sitelinks(ga_svc, client, search_rn)
    print(f"  ✅ {n_sitelinks} sitelinks added")
    add_callouts(ga_svc, client, search_rn)
    print(f"  ✅ {len(CALLOUTS)} callouts added")
    add_snippets(ga_svc, client, search_rn)
    print(f"  ✅ {len(STRUCTURED_SNIPPETS)} structured snippets added")

    me = client.enums.KeywordMatchTypeEnum
    for ag_data in AD_GROUPS:
        ag_op = client.get_type("AdGroupOperation")
        ag    = ag_op.create
        ag.name           = ag_data["name"]
        ag.campaign       = search_rn
        ag.status         = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_          = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ag.cpc_bid_micros = ag_data["cpc_bid_micros"]
        ag_rn = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op]).results[0].resource_name
        ag_id = ag_rn.split("/")[-1]

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
                asset = client.get_type("AdTextAsset"); asset.text = hl; rsa.headlines.append(asset)
            for desc in variant["descriptions"]:
                asset = client.get_type("AdTextAsset"); asset.text = desc; rsa.descriptions.append(asset)
            ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])

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
        print(f"  ✅ [{ag_id}] {ag_data['name']} — 3 RSAs + {len(kw_ops)} keywords")

    # ════════════════════════════════════════════════════════════════════
    # PERFORMANCE MAX CAMPAIGN
    # ════════════════════════════════════════════════════════════════════
    print("\n── Creating Performance Max Campaign ──")
    bud_op2 = client.get_type("CampaignBudgetOperation")
    b2 = bud_op2.create
    b2.name              = "BAU Fort Worth Hospitality PMax"
    b2.amount_micros     = DAILY_BUDGET
    b2.explicitly_shared = False
    bud_rn2 = bud_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[bud_op2]).results[0].resource_name

    ASSET_IDS = {
        "BUSINESS_NAME":   "11226590211",
        "LOGO":           ["56893637546", "336730299860"],
        "LANDSCAPE_LOGO":  "56894244206",
    }
    CAMP_TMP  = f"customers/{CUSTOMER_ID}/campaigns/-1"
    AG_TMP    = f"customers/{CUSTOMER_ID}/assetGroups/-2"

    batch = []
    # Campaign
    c_op = client.get_type("MutateOperation")
    c2   = c_op.campaign_operation.create
    c2.resource_name                    = CAMP_TMP
    c2.name                             = "p-b2c-google-pmax-us-bofu-bau-fort_worth-hospitality-eg"
    c2.advertising_channel_type         = client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    c2.status                           = client.enums.CampaignStatusEnum.ENABLED
    c2.campaign_budget                  = bud_rn2
    c2.contains_eu_political_advertising= 3
    c2.maximize_conversions.target_cpa_micros = 0
    batch.append(c_op)
    # Brand assets
    for asset_id in [ASSET_IDS["BUSINESS_NAME"]] + ASSET_IDS["LOGO"] + [ASSET_IDS["LANDSCAPE_LOGO"]]:
        ft = ("BUSINESS_NAME" if asset_id == ASSET_IDS["BUSINESS_NAME"]
              else "LANDSCAPE_LOGO" if asset_id == ASSET_IDS["LANDSCAPE_LOGO"]
              else "LOGO")
        op = client.get_type("MutateOperation")
        ca = op.campaign_asset_operation.create
        ca.campaign   = CAMP_TMP
        ca.asset      = f"customers/{CUSTOMER_ID}/assets/{asset_id}"
        ca.field_type = getattr(client.enums.AssetFieldTypeEnum, ft)
        batch.append(op)
    # Geo (proximity)
    geo_op = client.get_type("MutateOperation")
    gc     = geo_op.campaign_criterion_operation.create
    gc.campaign = CAMP_TMP
    gc.status   = client.enums.CampaignCriterionStatusEnum.ENABLED
    gc.proximity.geo_point.latitude_in_micro_degrees  = int(lat * 1_000_000)
    gc.proximity.geo_point.longitude_in_micro_degrees = int(lon * 1_000_000)
    gc.proximity.radius       = 20
    gc.proximity.radius_units = client.enums.ProximityRadiusUnitsEnum.MILES
    batch.append(geo_op)

    resp    = ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=batch)
    pmax_rn = resp.mutate_operation_responses[0].campaign_result.resource_name
    pmax_id = pmax_rn.split("/")[-1]
    print(f"  ✅ PMax campaign: p-b2c-google-pmax-us-bofu-bau-fort_worth-hospitality-eg  (ID: {pmax_id})")

    # Text assets
    text_ops = []
    for hl in PMAX_TEXT["headlines"]:
        op = client.get_type("MutateOperation"); a = op.asset_operation.create
        a.text_asset.text = hl; text_ops.append(op)
    for lh in PMAX_TEXT["long_headlines"]:
        op = client.get_type("MutateOperation"); a = op.asset_operation.create
        a.text_asset.text = lh; text_ops.append(op)
    for desc in PMAX_TEXT["descriptions"]:
        op = client.get_type("MutateOperation"); a = op.asset_operation.create
        a.text_asset.text = desc; text_ops.append(op)
    text_resp  = ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=text_ops)
    text_asset_rns = [r.asset_result.resource_name for r in text_resp.mutate_operation_responses]
    hl_rns   = text_asset_rns[:15]
    lh_rns   = text_asset_rns[15:20]
    desc_rns = text_asset_rns[20:]

    # Asset group + all assets (atomic)
    ag_batch = []
    ag_op2 = client.get_type("MutateOperation")
    agg    = ag_op2.asset_group_operation.create
    agg.resource_name = AG_TMP
    agg.campaign      = pmax_rn
    agg.name          = "Event Server — Fort Worth TX"
    agg.final_urls.append(FINAL_URL)
    agg.status        = client.enums.AssetGroupStatusEnum.ENABLED
    ag_batch.append(ag_op2)

    FT = client.enums.AssetFieldTypeEnum
    def link(asset_rn, field_type):
        op = client.get_type("MutateOperation")
        l  = op.asset_group_asset_operation.create
        l.asset_group = AG_TMP; l.asset = asset_rn; l.field_type = field_type
        ag_batch.append(op)

    for rn in hl_rns:   link(rn, FT.HEADLINE)
    for rn in lh_rns:   link(rn, FT.LONG_HEADLINE)
    for rn in desc_rns: link(rn, FT.DESCRIPTION)
    for aid in pmax_assets["MARKETING_IMAGE"]:
        link(f"customers/{CUSTOMER_ID}/assets/{aid}", FT.MARKETING_IMAGE)
    for aid in pmax_assets["SQUARE_MARKETING_IMAGE"]:
        link(f"customers/{CUSTOMER_ID}/assets/{aid}", FT.SQUARE_MARKETING_IMAGE)
    for aid in pmax_assets["PORTRAIT_MARKETING_IMAGE"]:
        link(f"customers/{CUSTOMER_ID}/assets/{aid}", FT.PORTRAIT_MARKETING_IMAGE)

    ga_svc.mutate(customer_id=CUSTOMER_ID, mutate_operations=ag_batch)
    total_imgs = sum(len(v) for v in pmax_assets.values())
    print(f"  ✅ Asset group created with {len(hl_rns)} headlines + {len(lh_rns)} long headlines + {len(desc_rns)} descriptions + {total_imgs} images")

    # ════════════════════════════════════════════════════════════════════
    # APP CAMPAIGN
    # ════════════════════════════════════════════════════════════════════
    print("\n── Creating App Campaign ──")
    bud_op3 = client.get_type("CampaignBudgetOperation")
    b3 = bud_op3.create
    b3.name              = "BAU Fort Worth Hospitality App"
    b3.amount_micros     = DAILY_BUDGET
    b3.explicitly_shared = False
    bud_rn3 = bud_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[bud_op3]).results[0].resource_name

    camp_op3 = client.get_type("CampaignOperation")
    c3 = camp_op3.create
    c3.name                              = "p-b2c-google-app-us-bofu-bau-fort_worth-hospitality-eg"
    c3.advertising_channel_type          = client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL
    c3.advertising_channel_sub_type      = client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN
    c3.status                            = client.enums.CampaignStatusEnum.ENABLED
    c3.campaign_budget                   = bud_rn3
    c3.contains_eu_political_advertising = 3
    c3.app_campaign_setting.app_id       = app_setting.app_id
    c3.app_campaign_setting.app_store    = app_setting.app_store
    c3.app_campaign_setting.bidding_strategy_goal_type = app_setting.bidding_strategy_goal_type
    c3.target_cpa.target_cpa_micros      = 2_000_000
    app_rn = camp_svc.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[camp_op3]).results[0].resource_name
    app_id = app_rn.split("/")[-1]
    print(f"  ✅ App campaign: {c3.name}  (ID: {app_id})")
    add_proximity(c_crit, client, app_rn, lat, lon)
    print(f"  ✅ 20-mile radius geo target set")

    APP_VARIANTS = [
        {
            "name": "Fort Worth Hosp - Urgency",
            "headlines": ["Hospitality Jobs Hiring Now", "Event Server — Apply Today",
                          "Flex Jobs Fort Worth TX", "Choose Your Own Shifts", "Same Day Pay"],
            "descriptions": [
                "Server jobs $18–$25/hr in Fort Worth. Flexible shifts for upscale events.",
                "Pick your own shifts at upscale events. Same Day Pay available.",
                "Indeed Flex: apply in minutes, work great events in Fort Worth TX.",
                "Earn $18–$25/hr as an event server. Start working this week in Fort Worth.",
            ],
        },
        {
            "name": "Fort Worth Hosp - Pay & Benefits",
            "headlines": ["$18–$25/Hr Server Jobs", "Same Day Pay Available",
                          "Health & Vision Benefits", "Flex Jobs Fort Worth TX", "$75 Referral Bonus"],
            "descriptions": [
                "Server roles $18–$25/hr with Same Day Pay & health benefits. Apply now.",
                "$75 referral bonus + health/dental/vision. Work Fort Worth area events.",
                "Top hospitality pay in Fort Worth. Same Day Pay + benefits. Apply today.",
                "Earn $18–$25/hr + health benefits at upscale events near Fort Worth, TX.",
            ],
        },
        {
            "name": "Fort Worth Hosp - Process",
            "headlines": ["No Long Application Process", "Apply in Minutes on the App",
                          "Work Upscale Events Near You", "Flex Jobs Fort Worth TX", "Start This Week"],
            "descriptions": [
                "Browse server jobs in Fort Worth & start working this week. Apply in minutes.",
                "Skip the long process. Pick shifts at upscale venues near Fort Worth, TX.",
                "Flexible server opportunities at top venues. Apply now on Indeed Flex.",
                "Event server roles available now. Choose your own schedule in Fort Worth.",
            ],
        },
    ]

    for variant in APP_VARIANTS:
        ag_op4 = client.get_type("AdGroupOperation")
        ag4    = ag_op4.create
        ag4.name     = variant["name"]
        ag4.campaign = app_rn
        ag4.status   = client.enums.AdGroupStatusEnum.ENABLED
        ag_rn4 = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op4]).results[0].resource_name

        ad_op4 = client.get_type("AdGroupAdOperation")
        ada4   = ad_op4.create
        ada4.ad_group = ag_rn4
        ada4.status   = client.enums.AdGroupAdStatusEnum.ENABLED
        app_ad = ada4.ad.app_ad
        for hl in variant["headlines"]:
            a = client.get_type("AdTextAsset"); a.text = hl; app_ad.headlines.append(a)
        for desc in variant["descriptions"]:
            a = client.get_type("AdTextAsset"); a.text = desc; app_ad.descriptions.append(a)
        ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op4])
        print(f"  ✅ App ad group: {variant['name']}")

    # ════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ════════════════════════════════════════════════════════════════════
    print(f"\n═══════════════════════════════════════════════════════════════")
    print(f"  ✅ ALL 3 CAMPAIGNS LIVE — Fort Worth Hospitality BAU")
    print(f"═══════════════════════════════════════════════════════════════")
    print(f"  Search : p-b2c-google-search-us-bofu-bau-fort_worth-hospitality-eg")
    print(f"           ID: {search_id}")
    print(f"  P.Max  : p-b2c-google-pmax-us-bofu-bau-fort_worth-hospitality-eg")
    print(f"           ID: {pmax_id}")
    print(f"  App    : p-b2c-google-app-us-bofu-bau-fort_worth-hospitality-eg")
    print(f"           ID: {app_id}")
    print(f"\n  Geo    : 20-mile radius from Fort Worth TX 76103")
    print(f"  Budget : $30/day × 3 = $90/day")
    print(f"  Groups : 8 ad groups × 3 RSAs = 24 RSAs (Search)")
    print(f"═══════════════════════════════════════════════════════════════\n")
    return search_id, pmax_id, app_id


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
