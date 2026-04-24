#!/usr/bin/env python3
"""
Hebron Hiring Event — Update Address in All Ad Copy
Campaign: p-b2c-google-search-us-bofu-bau-hebron-industrial-hiring-event-04282026 (23766291989)
PMax:     p-b2c-google-pmax-us-bofu-bau-hebron-industrial-hiring-event-04282026  (23766292319)

Old venue: Kentucky Career Center, Hebron, KY
New venue: 1324 Madison Ave., Covington KY 41011 (Kentucky Career Center - Covington)

Changes applied:
  Headlines: "Hebron KY · Mon Apr 28"         → "Covington KY · Apr 28"
  Desc:      "...Career Center, Hebron, KY"   → "...Career Center, Covington, KY"
  Desc:      "...Career Center CVG, Hebron"   → "...Career Center, Covington KY"
  Desc:      "in Hebron, KY"                  → "in Covington, KY"
  Desc:      "April 28th in Hebron, KY"       → "April 28 in Covington, KY"

Strategy:
  - RSA headlines/descriptions are IMMUTABLE — create new RSA, pause old one
  - PMax text_asset.text is also IMMUTABLE — create new asset, relink, remove old link
"""

import sys
sys.path.insert(0, '/Users/claudio.santos/RM-Team-Ai')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf import field_mask_pb2

YAML_PATH    = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID  = "7236100723"
SEARCH_CAMP  = "23766291989"
PMAX_CAMP    = "23766292319"

HEADLINE_SUBS = [
    ("Hebron KY · Mon Apr 28",       "Covington KY · Apr 28"),
]
DESC_SUBS = [
    ("April 28th in Hebron, KY",          "April 28 in Covington, KY"),
    ("Kentucky Career Center CVG, Hebron","Kentucky Career Center, Covington KY"),
    ("Kentucky Career Center, Hebron, KY","Kentucky Career Center, Covington, KY"),
    ("in Hebron, KY",                     "in Covington, KY"),
    ("Hebron, KY",                        "Covington, KY"),
    ("Hebron KY",                         "Covington KY"),
]


def apply_subs(text, subs):
    for old, new in subs:
        text = text.replace(old, new)
    return text


def validate_lengths(headlines, descriptions, ad_label):
    errors = []
    for i, h in enumerate(headlines):
        if len(h) > 30:
            errors.append(f"  Headline[{i}] too long ({len(h)} chars): {h}")
    for i, d in enumerate(descriptions):
        if len(d) > 90:
            errors.append(f"  Description[{i}] too long ({len(d)} chars): {d}")
    if errors:
        print(f"\n  ⚠️  Length violations in {ad_label}:")
        for e in errors:
            print(e)
        return False
    return True


def update_search_ads(client, ga_service):
    print("\n" + "─" * 60)
    print("  SEARCH — Replace RSAs (create new + pause old)")
    print("─" * 60)

    q = f"""
        SELECT ad_group.id, ad_group.name, ad_group.resource_name,
               ad_group_ad.resource_name,
               ad_group_ad.ad.id,
               ad_group_ad.ad.resource_name,
               ad_group_ad.ad.responsive_search_ad.headlines,
               ad_group_ad.ad.responsive_search_ad.descriptions,
               ad_group_ad.ad.responsive_search_ad.path1,
               ad_group_ad.ad.responsive_search_ad.path2,
               ad_group_ad.ad.final_urls,
               ad_group_ad.status
        FROM ad_group_ad
        WHERE campaign.id = {SEARCH_CAMP}
          AND ad_group_ad.status != 'REMOVED'
    """
    rows = list(ga_service.search(customer_id=CUSTOMER_ID, query=q))
    print(f"  Found {len(rows)} active RSAs")

    ad_service = client.get_service("AdGroupAdService")
    created = 0
    skipped = 0

    for row in rows:
        ada      = row.ad_group_ad
        ada_rn   = ada.resource_name       # adGroupAds/{ag_id}~{ad_id} — used for remove
        ad       = ada.ad
        rsa      = ad.responsive_search_ad
        ag_rn    = row.ad_group.resource_name
        ad_label = f"Ad {ad.id} in [{row.ad_group.name}]"

        old_headlines = [h.text for h in rsa.headlines]
        old_descs     = [d.text for d in rsa.descriptions]
        new_headlines = [apply_subs(h, HEADLINE_SUBS) for h in old_headlines]
        new_descs     = [apply_subs(d, DESC_SUBS)     for d in old_descs]

        if new_headlines == old_headlines and new_descs == old_descs:
            skipped += 1
            continue

        if not validate_lengths(new_headlines, new_descs, ad_label):
            print(f"  ❌ SKIPPED {ad_label} — fix length errors above")
            skipped += 1
            continue

        # Step 1 — Remove old RSA (frees the slot so the new one can be created)
        remove_op = client.get_type("AdGroupAdOperation")
        remove_op.remove = ada_rn
        ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[remove_op])

        # Step 2 — Create new RSA with updated copy
        create_op = client.get_type("AdGroupAdOperation")
        new_ada   = create_op.create
        new_ada.ad_group = ag_rn
        new_ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED

        new_ad = new_ada.ad
        for url in ad.final_urls:
            new_ad.final_urls.append(url)

        new_rsa        = new_ad.responsive_search_ad
        new_rsa.path1  = rsa.path1
        new_rsa.path2  = rsa.path2

        for h_text in new_headlines:
            h = client.get_type("AdTextAsset")
            h.text = h_text
            new_rsa.headlines.append(h)

        for d_text in new_descs:
            d = client.get_type("AdTextAsset")
            d.text = d_text
            new_rsa.descriptions.append(d)

        ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[create_op])

        created += 1
        print(f"\n  ✅ {ad_label}")
        changed_hls = [(o, n) for o, n in zip(old_headlines, new_headlines) if o != n]
        changed_ds  = [(o, n) for o, n in zip(old_descs,     new_descs)     if o != n]
        for old, new in changed_hls:
            print(f"     HL: '{old}' → '{new}'")
        for old, new in changed_ds:
            print(f"     D:  '{old}'")
            print(f"      →  '{new}'")
        print(f"     (old ad {ad.id} removed — {ada_rn})")

    print(f"\n  RSAs replaced: {created} | Unchanged/no-match: {skipped}")
    return created


def update_pmax_assets(client, ga_service):
    print("\n" + "─" * 60)
    print("  PMAX — Replace text assets (create new + relink)")
    print("─" * 60)

    # Get asset group resource names
    q = f"""
        SELECT asset_group.id, asset_group.name, asset_group.resource_name
        FROM asset_group
        WHERE campaign.id = {PMAX_CAMP}
          AND asset_group.status != 'REMOVED'
    """
    ag_rows = list(ga_service.search(customer_id=CUSTOMER_ID, query=q))
    if not ag_rows:
        print("  No asset groups found — skipping PMax")
        return 0

    ag_rn_map = {r.asset_group.resource_name: r.asset_group.name for r in ag_rows}
    for ag_rn, ag_name in ag_rn_map.items():
        print(f"  Asset group: {ag_name}")

    # Query text assets
    q2 = f"""
        SELECT asset.id, asset.resource_name, asset.text_asset.text,
               asset_group_asset.field_type,
               asset_group_asset.resource_name,
               asset_group.resource_name
        FROM asset_group_asset
        WHERE campaign.id = {PMAX_CAMP}
          AND asset.type = 'TEXT'
    """
    asset_rows = list(ga_service.search(customer_id=CUSTOMER_ID, query=q2))
    print(f"  Found {len(asset_rows)} text assets")

    asset_svc    = client.get_service("AssetService")
    aga_svc      = client.get_service("AssetGroupAssetService")
    updated = 0

    for row in asset_rows:
        asset    = row.asset
        original = asset.text_asset.text
        updated_text = apply_subs(apply_subs(original, HEADLINE_SUBS), DESC_SUBS)

        if updated_text == original:
            continue

        if len(updated_text) > 90:
            print(f"  ⚠️  SKIPPED asset {asset.id} — too long ({len(updated_text)} chars): {updated_text}")
            continue

        field_type = row.asset_group_asset.field_type
        ag_rn_for_asset = row.asset_group.resource_name
        old_aga_rn = row.asset_group_asset.resource_name

        # Step 1 — Remove old asset group link (frees the slot)
        remove_op = client.get_type("AssetGroupAssetOperation")
        remove_op.remove = old_aga_rn
        aga_svc.mutate_asset_group_assets(customer_id=CUSTOMER_ID, operations=[remove_op])

        # Step 2 — Create new text asset
        create_op = client.get_type("AssetOperation")
        create_op.create.text_asset.text = updated_text
        create_resp = asset_svc.mutate_assets(customer_id=CUSTOMER_ID, operations=[create_op])
        new_asset_rn = create_resp.results[0].resource_name

        # Step 3 — Link new asset to asset group
        link_op = client.get_type("AssetGroupAssetOperation")
        link     = link_op.create
        link.asset_group  = ag_rn_for_asset
        link.asset        = new_asset_rn
        link.field_type   = field_type
        aga_svc.mutate_asset_group_assets(customer_id=CUSTOMER_ID, operations=[link_op])

        updated += 1
        field_name = field_type.name if hasattr(field_type, 'name') else str(field_type)
        print(f"  ✅ [{field_name}] '{original}'")
        print(f"            → '{updated_text}'")

    print(f"  PMax assets updated: {updated}")
    return updated


def verify(ga_service):
    print("\n" + "─" * 60)
    print("  VERIFICATION — Checking ENABLED ads for remaining 'Hebron'")
    print("─" * 60)

    hebron_found = False

    q = f"""
        SELECT ad_group_ad.ad.responsive_search_ad.headlines,
               ad_group_ad.ad.responsive_search_ad.descriptions,
               ad_group.name
        FROM ad_group_ad
        WHERE campaign.id = {SEARCH_CAMP}
          AND ad_group_ad.status = 'ENABLED'
    """
    for row in ga_service.search(customer_id=CUSTOMER_ID, query=q):
        rsa = row.ad_group_ad.ad.responsive_search_ad
        for h in rsa.headlines:
            if "hebron" in h.text.lower():
                print(f"  ⚠️  Still has 'Hebron' in headline: [{row.ad_group.name}] '{h.text}'")
                hebron_found = True
        for d in rsa.descriptions:
            if "hebron" in d.text.lower():
                print(f"  ⚠️  Still has 'Hebron' in description: [{row.ad_group.name}] '{d.text}'")
                hebron_found = True

    if not hebron_found:
        print("  ✅ No 'Hebron' in any ENABLED Search RSAs")

    q2 = f"""
        SELECT asset.text_asset.text, asset_group_asset.field_type
        FROM asset_group_asset
        WHERE campaign.id = {PMAX_CAMP}
          AND asset.type = 'TEXT'
    """
    for row in ga_service.search(customer_id=CUSTOMER_ID, query=q2):
        if "hebron" in row.asset.text_asset.text.lower():
            print(f"  ⚠️  PMax still has 'Hebron': [{row.asset_group_asset.field_type.name}] '{row.asset.text_asset.text}'")
            hebron_found = True

    if not hebron_found:
        print("  ✅ No 'Hebron' in any PMax text assets")


def main():
    client     = GoogleAdsClient.load_from_storage(YAML_PATH)
    ga_service = client.get_service("GoogleAdsService")

    print("=" * 60)
    print("  Hebron HE — Address Update")
    print("  Old: Kentucky Career Center, Hebron, KY")
    print("  New: 1324 Madison Ave., Covington KY 41011")
    print("       (Kentucky Career Center - Covington)")
    print("=" * 60)

    search_updated = update_search_ads(client, ga_service)
    pmax_updated   = update_pmax_assets(client, ga_service)
    verify(ga_service)

    print("\n" + "=" * 60)
    print(f"  ✅ DONE — Search RSAs replaced: {search_updated} | PMax assets updated: {pmax_updated}")
    print("=" * 60 + "\n")


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
