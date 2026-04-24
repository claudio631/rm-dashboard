#!/usr/bin/env python3
"""
Tennant Solutions Hiring Event Cincinnati Apr 16 — Ad Extensions Fix
Adds to all 3 event campaigns (Search + P.Max + App):
  - Business Name (BUSINESS_NAME) → Search only (incompatible with App/P.Max at campaign level)
  - Sitelinks (6)
  - Callouts (6)
  - Structured Snippets (3)

Run: python3 scripts/google-ads-tennant-apr16-extensions.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

# ── Event campaigns ────────────────────────────────────────────────────────
CAMPAIGNS = {
    "Search": "customers/7236100723/campaigns/23749176468",
    "P.Max":  "customers/7236100723/campaigns/23749177674",
    "App":    "customers/7236100723/campaigns/23754489494",
}

BUSINESS_NAME_ASSET_RN = "customers/7236100723/assets/11226590211"

HIRING_EVENT_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/497086"
    "&employer=tennant-solutions&metro=cincinnati"
    "&role=picker-packer&utm_campaign=hiring-event-tennant"
)
BROWSE_JOBS_URL = (
    "https://indeedflex.com/find-jobs/"
    "?search&area_name=Cincinnati+OH"
)
INDEEDFLEX_URL = "https://indeedflex.com/"

# ── Sitelinks (6) ──────────────────────────────────────────────────────────
SITELINKS = [
    {
        "link_text":    "Event Details",
        "description1": "Apr 16, 10am–2pm in Hamilton, OH",
        "description2": "101 Knightsbridge Dr, Suite 1228",
        "final_url":    HIRING_EVENT_URL,
    },
    {
        "link_text":    "Download the App",
        "description1": "Get the Indeed Flex app",
        "description2": "Register for the hiring event",
        "final_url":    INDEEDFLEX_URL,
    },
    {
        "link_text":    "Picker Packer Shifts",
        "description1": "1st & 2nd shift available",
        "description2": "$14–$15/hr — start this week",
        "final_url":    HIRING_EVENT_URL,
    },
    {
        "link_text":    "Same Day Pay",
        "description1": "Get paid the same or next day",
        "description2": "Work for Indeed Flex",
        "final_url":    INDEEDFLEX_URL,
    },
    {
        "link_text":    "Health Benefits",
        "description1": "Health, dental & vision coverage",
        "description2": "Plus $75 referral bonus",
        "final_url":    INDEEDFLEX_URL,
    },
    {
        "link_text":    "Browse Jobs Cincinnati",
        "description1": "See all jobs near you",
        "description2": "No resume needed — apply today",
        "final_url":    BROWSE_JOBS_URL,
    },
]

# ── Callouts (6) ──────────────────────────────────────────────────────────
CALLOUTS = [
    "Hired on the Spot",
    "$14–$15/Hr",
    "No Experience Needed",
    "Same Day Pay Available",
    "$75 Referral Bonus",
    "Health Benefits Included",
]

# ── Structured Snippets (3) ───────────────────────────────────────────────
STRUCTURED_SNIPPETS = [
    {
        "header": "Types",
        "values": ["Picker Packer", "Warehouse Worker", "General Labor", "Order Fulfillment"],
    },
    {
        "header": "Amenities",
        "values": ["Same-Day Pay", "Health Benefits", "Flexible Scheduling", "$75 Referral Bonus"],
    },
    {
        "header": "Service catalog",
        "values": ["1st Shift 7am-3:30pm", "2nd Shift 3pm-12am", "Monday-Friday"],
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# ASSET CREATORS
# ═══════════════════════════════════════════════════════════════════════════

def create_sitelink_asset(client, sitelink: dict) -> str:
    svc    = client.get_service("AssetService")
    op     = client.get_type("AssetOperation")
    asset  = op.create
    sl     = asset.sitelink_asset
    sl.link_text    = sitelink["link_text"]
    sl.description1 = sitelink["description1"]
    sl.description2 = sitelink["description2"]
    asset.final_urls.append(sitelink["final_url"])
    return svc.mutate_assets(customer_id=CUSTOMER_ID, operations=[op]).results[0].resource_name


def create_callout_asset(client, callout_text: str) -> str:
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    asset.callout_asset.callout_text = callout_text
    return svc.mutate_assets(customer_id=CUSTOMER_ID, operations=[op]).results[0].resource_name


def create_snippet_asset(client, snippet: dict) -> str:
    svc   = client.get_service("AssetService")
    op    = client.get_type("AssetOperation")
    asset = op.create
    ss    = asset.structured_snippet_asset
    ss.header = snippet["header"]
    for v in snippet["values"]:
        ss.values.append(v)
    return svc.mutate_assets(customer_id=CUSTOMER_ID, operations=[op]).results[0].resource_name


def link_to_campaign(client, asset_rn: str, campaign_rn: str, field_type_name: str) -> None:
    svc = client.get_service("CampaignAssetService")
    op  = client.get_type("CampaignAssetOperation")
    ca  = op.create
    ca.asset      = asset_rn
    ca.campaign   = campaign_rn
    ca.field_type = getattr(client.enums.AssetFieldTypeEnum, field_type_name)
    svc.mutate_campaign_assets(customer_id=CUSTOMER_ID, operations=[op])


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n═══════════════════════════════════════════════════════════════")
    print("  Tennant Cincinnati HE Apr 16 — Extensions Fix")
    print("  Business Name + Sitelinks + Callouts + Snippets")
    print("═══════════════════════════════════════════════════════════════\n")

    # ── Step 1: Business Name → Search campaign only ─────────────────────
    print("── Step 1: Business Name ──")
    search_rn = CAMPAIGNS["Search"]
    try:
        link_to_campaign(client, BUSINESS_NAME_ASSET_RN, search_rn, "BUSINESS_NAME")
        print(f"  ✅ Business Name linked → Search")
    except GoogleAdsException as ex:
        print(f"  ⚠️  Business Name not supported for Search campaign type — skipped")
        for err in ex.failure.errors:
            print(f"     {err.message}")

    # ── Step 2: Create all assets once ───────────────────────────────────
    print("\n── Step 2: Creating assets ──")

    sl_rns = []
    for sl in SITELINKS:
        rn = create_sitelink_asset(client, sl)
        sl_rns.append(rn)
        print(f"  ✅ Sitelink: \"{sl['link_text']}\"")

    co_rns = []
    for co in CALLOUTS:
        rn = create_callout_asset(client, co)
        co_rns.append(rn)
        print(f"  ✅ Callout: \"{co}\"")

    ss_rns = []
    for ss in STRUCTURED_SNIPPETS:
        rn = create_snippet_asset(client, ss)
        ss_rns.append(rn)
        print(f"  ✅ Snippet: \"{ss['header']}: {', '.join(ss['values'][:2])}...\"")

    # ── Step 3: Link to all 3 campaigns ──────────────────────────────────
    print("\n── Step 3: Linking to campaigns ──")

    for camp_name, camp_rn in CAMPAIGNS.items():
        print(f"\n  {camp_name} ({camp_rn.split('/')[-1]}):")

        for sl_rn, sl in zip(sl_rns, SITELINKS):
            link_to_campaign(client, sl_rn, camp_rn, "SITELINK")
            print(f"    ✅ Sitelink: \"{sl['link_text']}\"")

        for co_rn, co in zip(co_rns, CALLOUTS):
            link_to_campaign(client, co_rn, camp_rn, "CALLOUT")
            print(f"    ✅ Callout: \"{co}\"")

        for ss_rn, ss in zip(ss_rns, STRUCTURED_SNIPPETS):
            link_to_campaign(client, ss_rn, camp_rn, "STRUCTURED_SNIPPET")
            print(f"    ✅ Snippet: \"{ss['header']}\"")

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n" + "═" * 63)
    print("  ✅ DONE")
    print("═" * 63)
    print(f"  {len(SITELINKS)} sitelinks × 3 campaigns = {len(SITELINKS) * 3} links")
    print(f"  {len(CALLOUTS)} callouts × 3 campaigns = {len(CALLOUTS) * 3} links")
    print(f"  {len(STRUCTURED_SNIPPETS)} snippets × 3 campaigns = {len(STRUCTURED_SNIPPETS) * 3} links")
    print()
    print("  NOTE: LOGO on Search/App campaigns is not supported by the Google Ads")
    print("  API (LOGO field type is P.Max-only). The P.Max asset group already has")
    print("  8 visual assets including logos. Search ads will show logos automatically")
    print("  if the account has a Business Profile linked with a verified logo.")
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
