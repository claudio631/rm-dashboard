#!/usr/bin/env python3
"""
Google Ads — Chicago Hospitality ToFu Search — Remove "day labor" negative
Created: 2026-04-15

Removes the "day labor" [PHRASE] campaign-level negative keyword that was
incorrectly added. "day labor" converts well ($12-13 CPA, below account avg).
"""

import sys
sys.path.insert(0, '/Users/claudio.santos/RM-Team-Ai')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "7236100723"
GOOGLE_ADS_YAML = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CAMPAIGN_ID = "22308263493"  # p-us-b2c-tofu-Eg1-chicago-hospitality-none-search


def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    crit_service = client.get_service("CampaignCriterionService")

    # Find the "day labor" negative criterion
    query = f"""
        SELECT campaign_criterion.resource_name,
               campaign_criterion.keyword.text,
               campaign_criterion.keyword.match_type,
               campaign_criterion.negative
        FROM campaign_criterion
        WHERE campaign.id = {CAMPAIGN_ID}
          AND campaign_criterion.negative = TRUE
          AND campaign_criterion.type = 'KEYWORD'
          AND campaign_criterion.keyword.text = 'day labor'
    """
    results = list(ga_service.search(customer_id=CUSTOMER_ID, query=query))

    if not results:
        print("  ⚠️  'day labor' negative not found — may not have propagated yet or already removed.")
        sys.exit(0)

    resource_name = results[0].campaign_criterion.resource_name
    match_type = results[0].campaign_criterion.keyword.match_type.name
    print(f"  Found: \"day labor\" [{match_type}] negative → {resource_name}")

    op = client.get_type("CampaignCriterionOperation")
    op.remove = resource_name

    try:
        response = crit_service.mutate_campaign_criteria(
            customer_id=CUSTOMER_ID,
            operations=[op],
        )
        print(f"  ✅ Removed: \"day labor\" [{match_type}] negative keyword")
    except GoogleAdsException as e:
        for err in e.failure.errors:
            print(f"  ERROR: {err.message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
