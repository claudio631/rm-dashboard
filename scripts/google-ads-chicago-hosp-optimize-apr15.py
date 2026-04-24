#!/usr/bin/env python3
"""
Google Ads — Chicago Hospitality ToFu Search — CPA Optimization
Created: 2026-04-15

Actions:
  1. Pause busser ad group (0 conversions, $35.07 wasted)
  2. Pause "dish washing jobs" EXACT keyword (61% CTR, 0 conversions)
  3. Pull general_labor search term report (last 30 days)
  4. Add campaign-level negative keywords for non-hospitality queries

Campaign: p-us-b2c-tofu-Eg1-chicago-hospitality-none-search
"""

import sys
sys.path.insert(0, '/Users/claudio.santos/RM-Team-Ai')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf import field_mask_pb2

CUSTOMER_ID = "7236100723"
GOOGLE_ADS_YAML = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CAMPAIGN_NAME = "p-us-b2c-tofu-Eg1-chicago-hospitality-none-search"
BUSSER_AG_NAME = "chicago-illinois-hospitality-none-busser-none"
DISHWASHER_AG_NAME = "chicago-illinois-hospitality-none-dishwasher-none"
GENERAL_LABOR_AG_NAME = "chicago-illinois-hospitality-none-general_labor-none"

# Non-hospitality negatives to add at campaign level
NON_HOSPITALITY_NEGATIVES = [
    "warehouse",
    "forklift",
    "construction",
    "landscaping",
    "manufacturing",
    "assembly line",
    "factory",
    "industrial",
    "moving company",
    "day labor",
    "yard work",
    "janitorial",
    "temp agency",
    "staffing agency",
    "maintenance",
    "warehouse worker",
    "warehouse jobs",
    "forklift operator",
    "construction worker",
    "labor day",
]


def log(msg):
    print(msg)


def get_campaign_resource(client, ga_service, campaign_name):
    query = f"""
        SELECT campaign.id, campaign.name, campaign.resource_name, campaign.status
        FROM campaign
        WHERE campaign.name = '{campaign_name}'
    """
    results = list(ga_service.search(customer_id=CUSTOMER_ID, query=query))
    if not results:
        raise ValueError(f"Campaign not found: {campaign_name}")
    c = results[0].campaign
    log(f"  Found campaign: [{c.status.name}] {c.name} (ID: {c.id})")
    return c.resource_name, c.id


def pause_ad_group(client, ga_service, campaign_name, ad_group_name):
    log(f"\n[1] Pausing ad group: {ad_group_name}")
    query = f"""
        SELECT ad_group.id, ad_group.name, ad_group.resource_name, ad_group.status
        FROM ad_group
        WHERE campaign.name = '{campaign_name}'
          AND ad_group.name = '{ad_group_name}'
    """
    results = list(ga_service.search(customer_id=CUSTOMER_ID, query=query))
    if not results:
        log(f"  ERROR: Ad group not found: {ad_group_name}")
        return False

    ag = results[0].ad_group
    log(f"  BEFORE: [{ag.status.name}] {ag.name} (ID: {ag.id})")

    ag_service = client.get_service("AdGroupService")
    op = client.get_type("AdGroupOperation")
    op.update.resource_name = ag.resource_name
    op.update.status = client.enums.AdGroupStatusEnum.PAUSED
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))

    try:
        ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
    except GoogleAdsException as e:
        for err in e.failure.errors:
            log(f"  ERROR: {err.message}")
        return False

    # Verify
    results2 = list(ga_service.search(customer_id=CUSTOMER_ID, query=query))
    ag2 = results2[0].ad_group
    icon = "✅" if ag2.status.name == "PAUSED" else "❌"
    log(f"  AFTER:  {icon} [{ag2.status.name}] {ag2.name}")
    return ag2.status.name == "PAUSED"


def pause_keyword(client, ga_service, campaign_name, ad_group_name, keyword_text, match_type="EXACT"):
    log(f"\n[2] Pausing keyword: \"{keyword_text}\" [{match_type}] in {ad_group_name}")
    query = f"""
        SELECT ad_group_criterion.criterion_id,
               ad_group_criterion.keyword.text,
               ad_group_criterion.keyword.match_type,
               ad_group_criterion.status,
               ad_group_criterion.resource_name,
               ad_group.name
        FROM ad_group_criterion
        WHERE campaign.name = '{campaign_name}'
          AND ad_group.name = '{ad_group_name}'
          AND ad_group_criterion.keyword.text = '{keyword_text}'
          AND ad_group_criterion.keyword.match_type = '{match_type}'
          AND ad_group_criterion.type = 'KEYWORD'
    """
    results = list(ga_service.search(customer_id=CUSTOMER_ID, query=query))
    if not results:
        log(f"  ERROR: Keyword not found: \"{keyword_text}\" [{match_type}]")
        return False

    crit = results[0].ad_group_criterion
    log(f"  BEFORE: [{crit.status.name}] \"{crit.keyword.text}\" [{crit.keyword.match_type.name}]")

    crit_service = client.get_service("AdGroupCriterionService")
    op = client.get_type("AdGroupCriterionOperation")
    op.update.resource_name = crit.resource_name
    op.update.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))

    try:
        crit_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=[op])
    except GoogleAdsException as e:
        for err in e.failure.errors:
            log(f"  ERROR: {err.message}")
        return False

    # Verify
    results2 = list(ga_service.search(customer_id=CUSTOMER_ID, query=query))
    crit2 = results2[0].ad_group_criterion
    icon = "✅" if crit2.status.name == "PAUSED" else "❌"
    log(f"  AFTER:  {icon} [{crit2.status.name}] \"{crit2.keyword.text}\"")
    return crit2.status.name == "PAUSED"


def pull_search_terms(ga_service, campaign_name, ad_group_name):
    log(f"\n[3] Search term report: {ad_group_name} (last 30 days)")
    query = f"""
        SELECT search_term_view.search_term,
               search_term_view.status,
               metrics.impressions,
               metrics.clicks,
               metrics.cost_micros,
               metrics.conversions
        FROM search_term_view
        WHERE campaign.name = '{campaign_name}'
          AND ad_group.name = '{ad_group_name}'
          AND segments.date DURING LAST_30_DAYS
        ORDER BY metrics.impressions DESC
        LIMIT 50
    """
    results = list(ga_service.search(customer_id=CUSTOMER_ID, query=query))
    log(f"  {'Search Term':<45} {'Impr':>6} {'Clicks':>6} {'Cost':>8} {'Conv':>6}")
    log(f"  {'-'*45} {'-'*6} {'-'*6} {'-'*8} {'-'*6}")
    for row in results:
        st = row.search_term_view
        m = row.metrics
        cost = m.cost_micros / 1_000_000
        log(f"  {st.search_term:<45} {m.impressions:>6} {m.clicks:>6} {cost:>8.2f} {m.conversions:>6.1f}")
    log(f"\n  Total search terms found: {len(results)}")
    return results


def add_campaign_negative_keywords(client, ga_service, campaign_resource_name, campaign_id, negatives):
    log(f"\n[4] Adding {len(negatives)} negative keywords at campaign level")

    # Check existing negatives to avoid dupes
    query = f"""
        SELECT campaign_criterion.keyword.text,
               campaign_criterion.keyword.match_type,
               campaign_criterion.negative
        FROM campaign_criterion
        WHERE campaign.id = {campaign_id}
          AND campaign_criterion.negative = TRUE
          AND campaign_criterion.type = 'KEYWORD'
    """
    existing = set()
    for row in ga_service.search(customer_id=CUSTOMER_ID, query=query):
        existing.add(row.campaign_criterion.keyword.text.lower())

    log(f"  Existing negatives: {len(existing)}")

    crit_service = client.get_service("CampaignCriterionService")
    operations = []
    skipped = []
    adding = []

    for neg_text in negatives:
        if neg_text.lower() in existing:
            skipped.append(neg_text)
            continue
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = campaign_resource_name
        criterion.negative = True
        criterion.keyword.text = neg_text
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        operations.append(op)
        adding.append(neg_text)

    if skipped:
        log(f"  Skipped (already exist): {', '.join(skipped)}")

    if not operations:
        log("  Nothing new to add.")
        return True

    try:
        response = crit_service.mutate_campaign_criteria(
            customer_id=CUSTOMER_ID,
            operations=operations,
        )
        log(f"  ✅ Added {len(response.results)} negative keywords:")
        for neg in adding:
            log(f"     — \"{neg}\" [PHRASE] (negative)")
        return True
    except GoogleAdsException as e:
        for err in e.failure.errors:
            log(f"  ERROR: {err.message}")
        return False


def main():
    log("=" * 60)
    log("Chicago Hospitality ToFu — CPA Optimization — 2026-04-15")
    log("=" * 60)

    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    # Get campaign resource name
    log(f"\n[0] Looking up campaign: {CAMPAIGN_NAME}")
    try:
        campaign_rn, campaign_id = get_campaign_resource(client, ga_service, CAMPAIGN_NAME)
    except ValueError as e:
        log(f"FATAL: {e}")
        sys.exit(1)

    results = {}

    # 1. Pause busser ad group
    results["busser_ag_paused"] = pause_ad_group(
        client, ga_service, CAMPAIGN_NAME, BUSSER_AG_NAME
    )

    # 2. Pause "dish washing jobs" EXACT keyword
    results["kw_paused"] = pause_keyword(
        client, ga_service, CAMPAIGN_NAME, DISHWASHER_AG_NAME,
        keyword_text="dish washing jobs", match_type="EXACT"
    )

    # 3. Pull general_labor search terms
    pull_search_terms(ga_service, CAMPAIGN_NAME, GENERAL_LABOR_AG_NAME)

    # 4. Add campaign-level negative keywords
    results["negatives_added"] = add_campaign_negative_keywords(
        client, ga_service, campaign_rn, campaign_id, NON_HOSPITALITY_NEGATIVES
    )

    # Summary
    log("\n" + "=" * 60)
    log("SUMMARY")
    log("=" * 60)
    log(f"  Busser ad group paused:          {'✅' if results['busser_ag_paused'] else '❌'}")
    log(f"  dish washing jobs EXACT paused:  {'✅' if results['kw_paused'] else '❌'}")
    log(f"  Campaign negatives added:        {'✅' if results['negatives_added'] else '❌'}")

    all_ok = all(results.values())
    log(f"\n  Overall: {'✅ All actions completed' if all_ok else '⚠️  Some actions failed — review above'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
