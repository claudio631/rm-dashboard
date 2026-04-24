#!/usr/bin/env python3
"""
Nashville Dishwasher — Step 4: Extensions only
Search: 23749457730 | P.Max: 23754779417
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

SEARCH_CAMPAIGN_RN = "customers/7236100723/campaigns/23749457730"
PMAX_CAMPAIGN_RN   = "customers/7236100723/campaigns/23754779417"
BUSINESS_NAME_ASSET_RN = "customers/7236100723/assets/11226590211"

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/dishwasher/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/500633"
    "&employer=NA"
    "&metro=nashville"
    "&role=dishwasher"
    "&utm_campaign=lettuce-dishwasher-nashville-tn"
)

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


def create_callout_asset(client, text):
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    asset.callout_asset.callout_text = text
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


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n" + "═" * 60)
    print("  Nashville Dishwasher — Step 4: Extensions")
    print("  Search: 23749457730 | P.Max: 23754779417")
    print("═" * 60 + "\n")

    print("Creating assets...")
    sl_rns = [create_sitelink_asset(client, sl) for sl in SITELINKS]
    print(f"  ✅ {len(sl_rns)} sitelinks created")
    co_rns = [create_callout_asset(client, co) for co in CALLOUTS]
    print(f"  ✅ {len(co_rns)} callouts created")
    ss_rns = [create_snippet_asset(client, ss) for ss in STRUCTURED_SNIPPETS]
    print(f"  ✅ {len(ss_rns)} snippets created")

    print("\nLinking to campaigns...")
    for label, camp_rn in [("Search", SEARCH_CAMPAIGN_RN), ("P.Max", PMAX_CAMPAIGN_RN)]:
        camp_id = camp_rn.split("/")[-1]
        print(f"  {label} ({camp_id}):")
        for sl_rn in sl_rns:
            link_asset_to_campaign(client, sl_rn, camp_rn, "SITELINK")
        print(f"    ✅ {len(sl_rns)} sitelinks linked")
        for co_rn in co_rns:
            link_asset_to_campaign(client, co_rn, camp_rn, "CALLOUT")
        print(f"    ✅ {len(co_rns)} callouts linked")
        for ss_rn in ss_rns:
            link_asset_to_campaign(client, ss_rn, camp_rn, "STRUCTURED_SNIPPET")
        print(f"    ✅ {len(ss_rns)} snippets linked")

    try:
        link_asset_to_campaign(client, BUSINESS_NAME_ASSET_RN, SEARCH_CAMPAIGN_RN, "BUSINESS_NAME")
        print(f"\n  ✅ Business Name linked to Search")
    except GoogleAdsException:
        print(f"\n  ⚠️  Business Name already linked or incompatible — skipped")

    print("\n" + "═" * 60)
    print("  ✅ EXTENSIONS COMPLETE")
    print("  6 sitelinks + 6 callouts + 3 snippets — both campaigns")
    print("═" * 60 + "\n")


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
