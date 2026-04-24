#!/usr/bin/env python3
"""
Fix: Link Business Name + Logo to Search and App campaigns
Tennant Solutions Hiring Event Cincinnati — Apr 16, 2026

P.Max (23749177674): already has BUSINESS_NAME + LOGO in asset group.
Search (23749176468): missing campaign-level brand assets.
App    (23754489494): missing campaign-level brand assets.

Run: python3 scripts/google-ads-tennant-apr16-link-brand-assets.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# Campaign resource names to fix
CAMPAIGNS = {
    "Search (23749176468)": "customers/7236100723/campaigns/23749176468",
    "App (23754489494)":    "customers/7236100723/campaigns/23754489494",
}

# Account-level brand assets
BRAND_ASSETS = [
    {
        "asset":      "customers/7236100723/assets/11226590211",
        "field_type": "BUSINESS_NAME",
        "label":      "Business Name: Indeed Flex",
    },
    {
        "asset":      "customers/7236100723/assets/56893637546",
        "field_type": "LOGO",
        "label":      "Square Logo (RGB)",
    },
    {
        "asset":      "customers/7236100723/assets/336730299860",
        "field_type": "LOGO",
        "label":      "Square Logo (Icon)",
    },
]


def link_brand_assets(client, campaign_name: str, campaign_rn: str) -> None:
    ft_enum = client.enums.AssetFieldTypeEnum
    svc     = client.get_service("CampaignAssetService")
    ops     = []

    for ba in BRAND_ASSETS:
        op             = client.get_type("CampaignAssetOperation")
        ca             = op.create
        ca.campaign    = campaign_rn
        ca.asset       = ba["asset"]
        ca.field_type  = getattr(ft_enum, ba["field_type"])
        ops.append(op)

    svc.mutate_campaign_assets(customer_id=CUSTOMER_ID, operations=ops)

    for ba in BRAND_ASSETS:
        print(f"    ✅ {ba['label']}")


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n═══════════════════════════════════════════════════════════════")
    print("  Link Brand Assets — Tennant Cincinnati HE Apr 16")
    print("  BUSINESS_NAME + LOGO → Search + App campaigns")
    print("═══════════════════════════════════════════════════════════════\n")

    for camp_name, camp_rn in CAMPAIGNS.items():
        print(f"  {camp_name}")
        link_brand_assets(client, camp_name, camp_rn)

    print("\n  ✅ Done — Business Name and Logo linked to both campaigns.")
    print("  P.Max: already set in asset group — no action needed.")
    print("═══════════════════════════════════════════════════════════════\n")


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
