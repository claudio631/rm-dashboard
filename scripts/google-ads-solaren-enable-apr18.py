#!/usr/bin/env python3
"""
Enable all 3 Solaren Event Staff Nashville campaigns on April 18, 2026.
Scheduled to run automatically at 8:03am on Apr 18.
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

CAMPAIGNS = [
    ("customers/7236100723/campaigns/23721569237", "p-b2c-google-search-us-bofu-bau-nashville-hospitality-hiring-event-04252026"),
    ("customers/7236100723/campaigns/23721572363", "p-b2c-google-pmax-us-bofu-bau-nashville-hospitality-hiring-event-04252026"),
    ("customers/7236100723/campaigns/23721955376", "p-b2c-google-app-us-bofu-bau-nashville-hospitality-hiring-event-04252026"),
]


def enable_campaign(client, customer_id: str, campaign_rn: str, name: str) -> None:
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.update
    c.resource_name = campaign_rn
    c.status        = client.enums.CampaignStatusEnum.ENABLED
    op.update_mask.paths.append("status")
    svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    print(f"  ✅ ENABLED: {name}")


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n══════════════════════════════════════════════════════════════════")
    print("  Solaren Event Staff Nashville — ENABLING campaigns (Apr 18)")
    print("══════════════════════════════════════════════════════════════════\n")

    for rn, name in CAMPAIGNS:
        enable_campaign(client, CUSTOMER_ID, rn, name)

    print("\n  All 3 campaigns now ENABLED and serving.")
    print("  BAU campaigns remain untouched.")
    print("  Post-event: campaigns will be paused automatically on Apr 25.")
    print("══════════════════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"\n❌ Google Ads API error: {ex}")
        for error in ex.failure.errors:
            print(f"   {error.message}")
        raise SystemExit(1)
