#!/usr/bin/env python3
"""
Google Ads — Account-Wide RSA Copy Sweep
Created: 2026-04-15

Finds and removes all RSA headlines and descriptions containing
"no experience needed" across all campaigns (policy change).

Strategy: RSA ad copy is immutable via UPDATE in the Google Ads API.
Approach: pause old RSA → create new RSA with cleaned copy → verify.
"""

import sys
sys.path.insert(0, '/Users/claudio.santos/RM-Team-Ai')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf import field_mask_pb2

CUSTOMER_ID = "7236100723"
GOOGLE_ADS_YAML = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
BANNED_PHRASE = "no experience needed"


def contains_banned(text):
    return BANNED_PHRASE in text.lower()


def find_matching_ads(ga_service):
    """Query all active RSAs and return those with banned copy."""
    query = """
        SELECT
            ad_group_ad.ad.id,
            ad_group_ad.ad.resource_name,
            ad_group_ad.resource_name,
            ad_group_ad.ad.final_urls,
            ad_group_ad.ad.final_mobile_urls,
            ad_group_ad.ad.tracking_url_template,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.ad.responsive_search_ad.path1,
            ad_group_ad.ad.responsive_search_ad.path2,
            ad_group_ad.status,
            ad_group.resource_name,
            ad_group.name,
            campaign.name
        FROM ad_group_ad
        WHERE ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'
          AND ad_group_ad.status != 'REMOVED'
        ORDER BY campaign.name, ad_group.name
    """
    matches = []
    total_scanned = 0

    for row in ga_service.search(customer_id=CUSTOMER_ID, query=query):
        total_scanned += 1
        ada = row.ad_group_ad
        ad = ada.ad
        rsa = ad.responsive_search_ad

        bad_headlines = [h for h in rsa.headlines if contains_banned(h.text)]
        bad_descriptions = [d for d in rsa.descriptions if contains_banned(d.text)]

        if bad_headlines or bad_descriptions:
            matches.append({
                "ad_group_ad_rn": ada.resource_name,
                "ad_rn": ad.resource_name,
                "ad_id": ad.id,
                "campaign": row.campaign.name,
                "ad_group_rn": row.ad_group.resource_name,
                "ad_group": row.ad_group.name,
                "status": ada.status.name,
                "final_urls": list(ad.final_urls),
                "final_mobile_urls": list(ad.final_mobile_urls),
                "tracking_url_template": ad.tracking_url_template,
                "path1": rsa.path1,
                "path2": rsa.path2,
                "all_headlines": list(rsa.headlines),
                "all_descriptions": list(rsa.descriptions),
                "bad_headlines": bad_headlines,
                "bad_descriptions": bad_descriptions,
            })

    return matches, total_scanned


def pause_old_ad(client, ad_service, match):
    """Pause the old RSA so it stops serving immediately."""
    op = client.get_type("AdGroupAdOperation")
    op.update.resource_name = match["ad_group_ad_rn"]
    op.update.status = client.enums.AdGroupAdStatusEnum.PAUSED
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))
    try:
        ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[op])
        return True
    except GoogleAdsException as e:
        for err in e.failure.errors:
            print(f"    ❌ Pause error: {err.message}")
        return False


def create_clean_ad(client, ad_service, match, clean_headlines, clean_descriptions):
    """Create a new RSA with the banned copy removed."""
    op = client.get_type("AdGroupAdOperation")
    new_ada = op.create
    new_ada.ad_group = match["ad_group_rn"]
    new_ada.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = new_ada.ad
    ad.final_urls.extend(match["final_urls"])
    if match["final_mobile_urls"]:
        ad.final_mobile_urls.extend(match["final_mobile_urls"])
    if match["tracking_url_template"]:
        ad.tracking_url_template = match["tracking_url_template"]

    rsa = ad.responsive_search_ad
    rsa.path1 = match["path1"]
    rsa.path2 = match["path2"]

    for h in clean_headlines:
        asset = client.get_type("AdTextAsset")
        asset.text = h.text
        if h.pinned_field != client.enums.ServedAssetFieldTypeEnum.UNSPECIFIED:
            asset.pinned_field = h.pinned_field
        rsa.headlines.append(asset)

    for d in clean_descriptions:
        asset = client.get_type("AdTextAsset")
        asset.text = d.text
        if d.pinned_field != client.enums.ServedAssetFieldTypeEnum.UNSPECIFIED:
            asset.pinned_field = d.pinned_field
        rsa.descriptions.append(asset)

    try:
        response = ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[op])
        new_rn = response.results[0].resource_name
        return True, new_rn
    except GoogleAdsException as e:
        for err in e.failure.errors:
            print(f"    ❌ Create error: {err.message}")
        return False, None


def process_matches(client, matches):
    ad_service = client.get_service("AdGroupAdService")
    results = []

    for match in matches:
        print(f"\n  Campaign: {match['campaign']}")
        print(f"  Ad Group: {match['ad_group']}")
        print(f"  Ad ID:    {match['ad_id']} [{match['status']}]")

        for h in match["bad_headlines"]:
            print(f"    Removing headline:    \"{h.text}\"")
        for d in match["bad_descriptions"]:
            print(f"    Removing description: \"{d.text}\"")

        clean_headlines = [h for h in match["all_headlines"] if not contains_banned(h.text)]
        clean_descriptions = [d for d in match["all_descriptions"] if not contains_banned(d.text)]

        if len(clean_headlines) < 3:
            print(f"    ⚠️  SKIP: Only {len(clean_headlines)} headlines remain (min 3). Manual replacement needed.")
            results.append({"ad_id": match["ad_id"], "status": "SKIPPED_MIN_ASSETS",
                            "campaign": match["campaign"], "ad_group": match["ad_group"]})
            continue

        if len(clean_descriptions) < 2:
            print(f"    ⚠️  SKIP: Only {len(clean_descriptions)} descriptions remain (min 2). Manual replacement needed.")
            results.append({"ad_id": match["ad_id"], "status": "SKIPPED_MIN_ASSETS",
                            "campaign": match["campaign"], "ad_group": match["ad_group"]})
            continue

        # Step 1: Pause old ad
        paused = pause_old_ad(client, ad_service, match)
        if not paused:
            results.append({"ad_id": match["ad_id"], "status": "ERROR"})
            continue
        print(f"    ✅ Old RSA paused (ID: {match['ad_id']})")

        # Step 2: Create clean replacement
        created, new_rn = create_clean_ad(client, ad_service, match, clean_headlines, clean_descriptions)
        if created:
            print(f"    ✅ New RSA created: {new_rn}")
            print(f"       Headlines: {len(clean_headlines)} | Descriptions: {len(clean_descriptions)}")
            results.append({"ad_id": match["ad_id"], "status": "REPLACED"})
        else:
            print(f"    ⚠️  Old RSA paused but new RSA creation failed — review manually.")
            results.append({"ad_id": match["ad_id"], "status": "PAUSED_CREATE_FAILED"})

    return results


def main():
    print("=" * 65)
    print("Google Ads — RSA Sweep: Remove 'no experience needed'")
    print("=" * 65)

    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    print("\n[1] Scanning all RSAs across account...")
    matches, total = find_matching_ads(ga_service)
    print(f"  Scanned: {total} RSAs")
    print(f"  Matched: {len(matches)} ads with banned copy")

    if not matches:
        print("\n  ✅ No ads found containing 'no experience needed'. Account is clean.")
        sys.exit(0)

    print(f"\n[2] Processing {len(matches)} ad(s): pause old → create clean replacement...")
    results = process_matches(client, matches)

    replaced = sum(1 for r in results if r["status"] == "REPLACED")
    skipped = sum(1 for r in results if r["status"] == "SKIPPED_MIN_ASSETS")
    paused_fail = sum(1 for r in results if r["status"] == "PAUSED_CREATE_FAILED")
    errors = sum(1 for r in results if r["status"] == "ERROR")

    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"  RSAs scanned:          {total}")
    print(f"  Matches found:         {len(matches)}")
    print(f"  ✅ Replaced:           {replaced}  (old paused, clean RSA live)")
    print(f"  ⚠️  Skipped:           {skipped}  (too few assets — manual action needed)")
    print(f"  ⚠️  Paused/no create:  {paused_fail}  (old paused, new creation failed)")
    print(f"  ❌ Errors:             {errors}")

    skipped_list = [r for r in results if r["status"] == "SKIPPED_MIN_ASSETS"]
    if skipped_list:
        print("\n  ADS REQUIRING MANUAL ACTION (min asset count too low):")
        for r in skipped_list:
            print(f"    — {r['campaign']} / {r['ad_group']} (Ad ID: {r['ad_id']})")
        print("  Add a replacement headline/description in Google Ads UI, then re-run.")

    all_ok = (errors == 0 and paused_fail == 0)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
