#!/usr/bin/env python3
"""
RESUME: Tennant Solutions Hiring Event Cincinnati (Apr 16, 2026)
  - Search already live (ID: 23749176468)
  - P.Max campaign created (ID: 23749177674) but asset group missing
  - App campaign not yet created

This script:
  1. Creates P.Max asset group for existing campaign (YouTube excluded)
  2. Creates App campaign from scratch

Run: python3 scripts/google-ads-tennant-hiring-event-apr16-resume.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.saints/RM-Team-Ai/google-ads.yaml"
YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Already-created IDs ────────────────────────────────────────────────────
EXISTING_PMAX_CAMPAIGN_ID = "23749177674"
SOURCE_APP_CAMPAIGN_ID    = "23062774690"
SOURCE_PMAX_CAMPAIGN_ID   = "16868661589"   # p-us-b2c-brand-Eg-cincinnati-none-pmax-pmax
PMAX_BUDGET_RN            = "customers/7236100723/campaignBudgets/15504571128"

APP_NAME    = "p-b2c-google-app-us-bofu-bau-cincinnati-industrial-hiring-event-04162026"
EVENT_END_DATE_TIME = "2026-04-16 23:59:59"
DAILY_BUDGET_MICROS = 50_000_000   # $50/day

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/497086"
    "&employer=tennant-solutions&metro=cincinnati"
    "&role=picker-packer&utm_campaign=hiring-event-tennant"
)

# Exclude YOUTUBE_VIDEO — deleted video in BAU causes API error
VISUAL_FIELD_TYPE_NAMES = {
    "MARKETING_IMAGE", "SQUARE_MARKETING_IMAGE", "PORTRAIT_MARKETING_IMAGE",
    "LOGO", "LANDSCAPE_LOGO",
}

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


def fetch_campaign(client, campaign_id: str):
    ga_svc = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT
            campaign.id, campaign.name,
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


def fetch_pmax_asset_group(client, pmax_campaign_id: str):
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


def create_pmax_asset_group(client, camp_rn: str, visual_assets: list) -> str:
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


def create_app_campaign(client, source, geo_targets: list) -> str:
    print("\n── Creating App Campaign ──")

    bsvc = client.get_service("CampaignBudgetService")
    bop  = client.get_type("CampaignBudgetOperation")
    b    = bop.create
    b.name              = "Tennant Cincinnati HE App 20260416"
    b.amount_micros     = DAILY_BUDGET_MICROS
    b.delivery_method   = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    budget_rn = bsvc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[bop]).results[0].resource_name
    print(f"  ✅ Budget: ${DAILY_BUDGET_MICROS // 1_000_000}/day  →  {budget_rn}")

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
    print(f"  ✅ App campaign: {APP_NAME}  (ID: {camp_rn.split('/')[-1]})")

    # Copy geo targets
    if geo_targets:
        crit_svc = client.get_service("CampaignCriterionService")
        ops = []
        for gt in geo_targets:
            gop = client.get_type("CampaignCriterionOperation")
            cc  = gop.create
            cc.campaign                     = camp_rn
            cc.location.geo_target_constant = gt["geo_target_constant"]
            cc.negative                     = gt["negative"]
            if gt["bid_modifier"] and gt["bid_modifier"] != 1.0:
                cc.bid_modifier = gt["bid_modifier"]
            ops.append(gop)
        crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
        print(f"  ✅ {len(ops)} geo target(s) copied")

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


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n═══════════════════════════════════════════════════════════════")
    print("  RESUME — Tennant Cincinnati Hiring Event Apr 16")
    print("  P.Max asset group + App campaign")
    print("═══════════════════════════════════════════════════════════════\n")

    # Fetch BAU visual assets (no YouTube)
    print("── Fetching P.Max visual assets (YouTube excluded) ──")
    ag_rn = fetch_pmax_asset_group(client, SOURCE_PMAX_CAMPAIGN_ID)
    visual_assets = []
    if ag_rn:
        visual_assets = fetch_visual_assets(client, ag_rn)
        print(f"  ✅ {len(visual_assets)} visual asset(s) (no video)")
    else:
        print("  ⚠️  No BAU asset group found — using account logos only")

    # Fetch geo targets from existing event Search campaign
    geo_targets = fetch_geo_targets(client, "23749176468")
    print(f"  ✅ {len(geo_targets)} geo target(s) from Search campaign")

    # Step 1: P.Max asset group
    print("\n── Step 1: Creating P.Max asset group ──")
    pmax_camp_rn = f"customers/{CUSTOMER_ID}/campaigns/{EXISTING_PMAX_CAMPAIGN_ID}"
    create_pmax_asset_group(client, pmax_camp_rn, visual_assets)

    # Step 2: App campaign
    source_app = fetch_campaign(client, SOURCE_APP_CAMPAIGN_ID)
    app_rn = create_app_campaign(client, source_app, geo_targets)

    print("\n" + "═" * 63)
    print("  ✅ RESUME COMPLETE — ALL 3 CAMPAIGNS LIVE")
    print("═" * 63)
    print(f"  Search  : 23749176468  (already running)")
    print(f"  P.Max   : {EXISTING_PMAX_CAMPAIGN_ID}  (asset group now added)")
    print(f"  App     : {app_rn.split('/')[-1]}")
    print()
    print("  MANUAL STEPS — Google Ads UI:")
    print("  Sitelinks (min 6), Callouts (min 4), Structured Snippets (min 3)")
    print("  POST-EVENT (Apr 16 after 2pm): pause all 3 event campaigns")
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
