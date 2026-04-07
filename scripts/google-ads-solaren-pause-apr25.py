#!/usr/bin/env python3
"""
Pause all 3 Solaren Event Staff Nashville campaigns on April 25, 2026 (post-event).
Scheduled to run automatically at 3:07pm on Apr 25 (shift ends at 2pm).
BAU campaigns are NOT touched.
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


def pause_campaign(client, customer_id: str, campaign_rn: str, name: str) -> None:
    svc = client.get_service("CampaignService")
    op  = client.get_type("CampaignOperation")
    c   = op.update
    c.resource_name = campaign_rn
    c.status        = client.enums.CampaignStatusEnum.PAUSED
    op.update_mask.paths.append("status")
    svc.mutate_campaigns(customer_id=customer_id, operations=[op])
    print(f"  ✅ PAUSED: {name}")


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n══════════════════════════════════════════════════════════════════")
    print("  Solaren Event Staff Nashville — PAUSING campaigns (Apr 25 post-event)")
    print("══════════════════════════════════════════════════════════════════\n")

    for rn, name in CAMPAIGNS:
        pause_campaign(client, CUSTOMER_ID, rn, name)

    print("\n  All 3 event campaigns now PAUSED.")
    print("  BAU Nashville hospitality campaigns remain running untouched.")
    print("══════════════════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"\n❌ Google Ads API error: {ex}")
        for error in ex.failure.errors:
            print(f"   {error.message}")
        raise SystemExit(1)
