"""
Google Ads — Washington DC Hospitality — Sitelinks + Structured Snippets
Created: 2026-04-07

Adds to all 3 DC campaigns (Search, P.Max, Display):
  Sitelinks (4):
    1. Hospitality Jobs
    2. Same Day Pay
    3. Find Jobs in DC       ← DC-specific
    4. About Us

  Structured Snippets (2):
    1. Types     → job roles available in DC
    2. Service catalog → Indeed Flex benefits

Benchmarks: B2C Search campaigns (Austin, Atlanta, Chicago, Charlotte)
"""

import sys
sys.path.insert(0, '/Users/claudio.santos/RM-Team-Ai')

from google.ads.googleads.client import GoogleAdsClient

CUSTOMER_ID = "7236100723"

DC_SEARCH_URL = (
    "https://indeedflex.com/job-search/?search"
    "&area_name=Washington+DC"
    "&search_lat=38.9072&search_lon=-77.0369"
    "&top_lon=-76.9094&top_lat=38.9948"
    "&bot_lon=-77.1198&bot_lat=38.7916"
)

CAMPAIGNS = {
    "Search":  "customers/7236100723/campaigns/23732428286",
    "P.Max":   "customers/7236100723/campaigns/23727227430",
    "Display": "customers/7236100723/campaigns/23732445044",
}

# ── Sitelinks ─────────────────────────────────────────────────────────────────
SITELINKS = [
    {
        "link_text":    "Hospitality Jobs",
        "description1": "Join the Buzz of the Hospitality",
        "description2": "Wide Range of Temporary Jobs",
        "final_url":    DC_SEARCH_URL,
    },
    {
        "link_text":    "Same Day Pay",
        "description1": "Get paid fast with Same Day Pay.",
        "description2": "Work for Indeed Flex!",
        "final_url":    DC_SEARCH_URL,
    },
    {
        "link_text":    "Find Jobs in DC",
        "description1": "Browse Hospitality Jobs in DC",
        "description2": "Apply Today — No Resume Needed",
        "final_url":    DC_SEARCH_URL,
    },
    {
        "link_text":    "About Us",
        "description1": "Find out about our mission.",
        "description2": "Learn more about Indeed Flex.",
        "final_url":    "https://indeedflex.com/about/",
    },
]

# ── Structured Snippets ───────────────────────────────────────────────────────
STRUCTURED_SNIPPETS = [
    {
        "header": "Types",
        "values": [
            "Barista",
            "Server",
            "Cashier",
            "Prep Cook",
            "Line Cook",
            "Dishwasher",
            "Hospitality General",
        ],
    },
    {
        "header": "Service catalog",
        "values": [
            "Same-Day Pay",
            "Flexible Shifts",
            "Instant Booking",
            "No Resume Needed",
            "Weekly Pay Options",
        ],
    },
]


def get_client():
    return GoogleAdsClient.load_from_storage('/Users/claudio.santos/RM-Team-Ai/google-ads.yaml')


def create_sitelink_asset(client, sitelink):
    """Create a SitelinkAsset and return its resource name."""
    asset_service = client.get_service("AssetService")
    asset_op = client.get_type("AssetOperation")
    asset = asset_op.create
    sl = asset.sitelink_asset
    sl.link_text = sitelink["link_text"]
    sl.description1 = sitelink["description1"]
    sl.description2 = sitelink["description2"]
    asset.final_urls.append(sitelink["final_url"])
    resp = asset_service.mutate_assets(customer_id=CUSTOMER_ID, operations=[asset_op])
    return resp.results[0].resource_name


def create_snippet_asset(client, snippet):
    """Create a StructuredSnippetAsset and return its resource name."""
    asset_service = client.get_service("AssetService")
    asset_op = client.get_type("AssetOperation")
    asset = asset_op.create
    ss = asset.structured_snippet_asset
    ss.header = snippet["header"]
    for v in snippet["values"]:
        ss.values.append(v)
    resp = asset_service.mutate_assets(customer_id=CUSTOMER_ID, operations=[asset_op])
    return resp.results[0].resource_name


def link_asset_to_campaign(client, asset_rn, campaign_rn, field_type_name):
    """Link an asset to a campaign."""
    ca_service = client.get_service("CampaignAssetService")
    ca_op = client.get_type("CampaignAssetOperation")
    ca = ca_op.create
    ca.asset = asset_rn
    ca.campaign = campaign_rn
    ca.field_type = getattr(client.enums.AssetFieldTypeEnum, field_type_name)
    ca_service.mutate_campaign_assets(customer_id=CUSTOMER_ID, operations=[ca_op])


def main():
    client = get_client()

    print("=" * 60)
    print("Washington DC Hospitality — Sitelinks + Structured Snippets")
    print("=" * 60)

    # ── Step 1: Create all assets once ────────────────────────────────────────
    print("\n── Creating assets ──")

    sl_rns = []
    for sl in SITELINKS:
        rn = create_sitelink_asset(client, sl)
        sl_rns.append(rn)
        print(f"  ✅ Sitelink: \"{sl['link_text']}\"  →  {rn}")

    ss_rns = []
    for ss in STRUCTURED_SNIPPETS:
        rn = create_snippet_asset(client, ss)
        ss_rns.append(rn)
        print(f"  ✅ Snippet: \"{ss['header']}\"  →  {rn}")

    # ── Step 2: Link assets to each campaign ──────────────────────────────────
    print("\n── Linking to campaigns ──")

    for camp_name, camp_rn in CAMPAIGNS.items():
        print(f"\n  {camp_name} ({camp_rn.split('/')[-1]}):")

        for sl_rn, sl in zip(sl_rns, SITELINKS):
            link_asset_to_campaign(client, sl_rn, camp_rn, "SITELINK")
            print(f"    ✅ Sitelink linked: \"{sl['link_text']}\"")

        for ss_rn, ss in zip(ss_rns, STRUCTURED_SNIPPETS):
            link_asset_to_campaign(client, ss_rn, camp_rn, "STRUCTURED_SNIPPET")
            print(f"    ✅ Snippet linked: \"{ss['header']}\"")

    print("\n" + "=" * 60)
    print("✅ DONE")
    print("=" * 60)
    print("  • 4 sitelinks × 3 campaigns = 12 links")
    print("  • 2 structured snippets × 3 campaigns = 6 links")
    print("\n  Sitelinks:")
    for sl in SITELINKS:
        print(f"    - {sl['link_text']}")
    print("\n  Structured Snippets:")
    for ss in STRUCTURED_SNIPPETS:
        print(f"    - {ss['header']}: {', '.join(ss['values'])}")


if __name__ == "__main__":
    main()
