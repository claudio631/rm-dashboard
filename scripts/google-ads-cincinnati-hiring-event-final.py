#!/usr/bin/env python3
"""
Cincinnati Hiring Event — Final Campaign Changes
- Create "Hiring Event — Cincinnati" ad group with 12 keywords + RSA
- Add picker packer keywords to p---warehouse-- and p---generic_immediate--
- Replace App campaign UAC copy with 5 event headlines + 5 descriptions

Run: python3 scripts/google-ads-cincinnati-hiring-event-final.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"
MANAGER_ID = "6531650309"

SEARCH_CAMPAIGN_ID = "23058669077"
APP_CAMPAIGN_ID = "23062774690"
APP_AD_GROUP_ID = "189068902554"

AG_WAREHOUSE_ID = "186723660235"
AG_GENERIC_IMMEDIATE_ID = "186723659995"

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/497086"
    "&employer=tennant-solutions&metro=cincinnati"
    "&role=picker-packer&utm_campaign=hiring-event-tennant"
)

# ── RSA Copy (same applied to all search ad groups) ──────────────────────

RSA_HEADLINES = [
    "Hiring Event — April 9th",
    "Hamilton, OH · Thu Apr 9",
    "Warehouse Jobs $14–$15/Hr",
    "Instant Job Offer on the Spot",
    "Picker Packer Hiring Now",
    "Walk In, Walk Out Employed",
    "Same Day Pay Available",
    "$250 Attendance Bonus",
    "Meet Recruiters Face to Face",
    "Indeed Flex Hiring Event",
    "Warehouse Work Near Cincinnati",
    "1st & 2nd Shift Available",
    "Get Hired Today — Apr 9",
    "$75 Referral Bonus",
    "Limited Spots — Register Now",
]

RSA_DESCRIPTIONS = [
    "Join us Apr 9, 10am–2pm at 101 Knightsbridge Dr, Hamilton, OH. Get hired on the spot!",
    "Picker Packer roles $14–$15/hr. Same Day Pay, $250 bonus & health benefits. Apply now.",
    "Indeed Flex hiring event — walk in & leave with a job offer. 1st & 2nd shift openings.",
    "No long process. Meet our recruiters & get an instant offer on April 9th. Sign up free.",
]

# ── Hiring Event ad group keywords ───────────────────────────────────────

HIRING_EVENT_KEYWORDS = [
    # (text, match_type_enum_value)
    ("hiring event cincinnati", "EXACT"),
    ("job fair cincinnati ohio", "EXACT"),
    ("hiring event near me", "EXACT"),
    ("walk in job fair", "EXACT"),
    ("warehouse hiring event", "EXACT"),
    ("hiring event cincinnati", "PHRASE"),
    ("job fair near me cincinnati", "PHRASE"),
    ("warehouse job fair ohio", "PHRASE"),
    ("hiring event hamilton ohio", "PHRASE"),
    ("immediate hire warehouse cincinnati", "PHRASE"),
    ("warehouse hiring event cincinnati ohio", "BROAD"),
    ("get hired on the spot cincinnati", "BROAD"),
]

# ── Keywords to add to p---generic_immediate-- ────────────────────────────

GENERIC_IMMEDIATE_KEYWORDS = [
    ("immediate warehouse jobs cincinnati", "PHRASE"),
    ("warehouse jobs hiring now cincinnati", "PHRASE"),
    ("picker packer jobs cincinnati", "PHRASE"),
    ("warehouse jobs hamilton ohio", "PHRASE"),
    ("picker packer cincinnati", "EXACT"),
]

# ── Keywords to add to p---warehouse-- ───────────────────────────────────

WAREHOUSE_KEYWORDS = [
    ("warehouse jobs cincinnati ohio", "PHRASE"),
    ("picker packer jobs near me", "PHRASE"),
    ("warehouse worker cincinnati", "EXACT"),
    ("warehouse jobs hamilton oh", "PHRASE"),
]

# ── App campaign UAC copy ─────────────────────────────────────────────────

APP_HEADLINES = [
    "Download App & Attend Apr 9",
    "Hiring Event — April 9th",
    "Warehouse Jobs $14–$15/Hr",
    "Picker Packer Jobs Cincinnati",
    "Get Hired at Our Live Event",
]

APP_DESCRIPTIONS = [
    "Download Indeed Flex & register for our Apr 9 hiring event in Hamilton, OH.",
    "Warehouse roles $14–$15/hr. Walk in April 9, 10am–2pm. Get hired on the spot.",
    "Download the app, sign up & come to our hiring event. Instant offers on April 9.",
    "Same Day Pay, $250 bonus, health benefits. Attend our hiring event Apr 9 in OH.",
    "Indeed Flex is hiring Picker Packers in Hamilton, OH. Register via app today.",
]


def campaign_resource(customer_id: str, campaign_id: str) -> str:
    return f"customers/{customer_id}/campaigns/{campaign_id}"


def ad_group_resource(customer_id: str, ad_group_id: str) -> str:
    return f"customers/{customer_id}/adGroups/{ad_group_id}"


# ── Step 1: Create "Hiring Event — Cincinnati" ad group ──────────────────

def create_hiring_event_ad_group(client, customer_id: str) -> str:
    """Creates the new ad group; returns its resource name."""
    ag_service = client.get_service("AdGroupService")
    ag_operation = client.get_type("AdGroupOperation")
    ag = ag_operation.create

    ag.name = "Hiring Event — Cincinnati"
    ag.campaign = campaign_resource(customer_id, SEARCH_CAMPAIGN_ID)
    ag.status = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    # CPC bid — target ~$1.50 (1_500_000 micros) as a baseline
    ag.cpc_bid_micros = 1_500_000

    response = ag_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[ag_operation],
    )
    resource_name = response.results[0].resource_name
    print(f"  ✅ Ad group created: {resource_name}")
    return resource_name


# ── Step 2: Add keywords to an ad group ──────────────────────────────────

def add_keywords(client, customer_id: str, ad_group_resource_name: str, keywords: list) -> int:
    """Adds keywords to the given ad group. Returns count added."""
    criterion_service = client.get_service("AdGroupCriterionService")
    operations = []

    match_enum = client.enums.KeywordMatchTypeEnum

    for text, match_type_str in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        criterion = op.create
        criterion.ad_group = ad_group_resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = text
        criterion.keyword.match_type = getattr(match_enum, match_type_str)
        operations.append(op)

    response = criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations,
    )
    count = len(response.results)
    print(f"  ✅ {count} keyword(s) added to {ad_group_resource_name.split('/')[-1]}")
    return count


# ── Step 3: Add RSA to an ad group ───────────────────────────────────────

def add_rsa(client, customer_id: str, ad_group_resource_name: str) -> str:
    """Creates an RSA in the given ad group; returns resource name."""
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_ad_op = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_op.create

    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = ad_group_ad.ad
    ad.final_urls.append(FINAL_URL)

    rsa = ad.responsive_search_ad
    for hl in RSA_HEADLINES:
        asset = client.get_type("AdTextAsset")
        asset.text = hl
        rsa.headlines.append(asset)

    for desc in RSA_DESCRIPTIONS:
        asset = client.get_type("AdTextAsset")
        asset.text = desc
        rsa.descriptions.append(asset)

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=[ad_group_ad_op],
    )
    resource_name = response.results[0].resource_name
    print(f"  ✅ RSA added: {resource_name}")
    return resource_name


# ── Step 4: Replace App campaign ad copy ─────────────────────────────────

def list_app_ads(client, customer_id: str, ad_group_id: str) -> list:
    """Returns list of (ad_group_ad_resource_name, ad_id) for the app ad group."""
    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            ad_group_ad.resource_name,
            ad_group_ad.ad.id
        FROM ad_group_ad
        WHERE ad_group_ad.ad_group = '{ad_group_resource(customer_id, ad_group_id)}'
          AND ad_group_ad.status != 'REMOVED'
    """
    response = ga_service.search(customer_id=customer_id, query=query)
    results = []
    for row in response:
        results.append(row.ad_group_ad.resource_name)
    return results


def remove_app_ads(client, customer_id: str, resource_names: list) -> int:
    """Removes existing app ads."""
    if not resource_names:
        return 0
    ad_group_ad_service = client.get_service("AdGroupAdService")
    operations = []
    for rn in resource_names:
        op = client.get_type("AdGroupAdOperation")
        op.remove = rn
        operations.append(op)
    ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=operations,
    )
    print(f"  ✅ Removed {len(operations)} existing app ad(s)")
    return len(operations)


def create_app_ad(client, customer_id: str, ad_group_id: str) -> str:
    """Creates a new AppAd with event copy; returns resource name."""
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_ad_op = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_op.create

    ad_group_ad.ad_group = ad_group_resource(customer_id, ad_group_id)
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = ad_group_ad.ad
    app_ad = ad.app_ad

    for hl in APP_HEADLINES:
        asset = client.get_type("AdTextAsset")
        asset.text = hl
        app_ad.headlines.append(asset)

    for desc in APP_DESCRIPTIONS:
        asset = client.get_type("AdTextAsset")
        asset.text = desc
        app_ad.descriptions.append(asset)

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=[ad_group_ad_op],
    )
    resource_name = response.results[0].resource_name
    print(f"  ✅ New app ad created: {resource_name}")
    return resource_name


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    customer_id = CUSTOMER_ID

    print("\n══════════════════════════════════════════════════")
    print("  Cincinnati Hiring Event — Final Campaign Changes")
    print("══════════════════════════════════════════════════\n")

    # ── SEARCH CAMPAIGN ──────────────────────────────────────────────────

    print("▶ STEP 1: Create 'Hiring Event — Cincinnati' ad group")
    hiring_event_ag = create_hiring_event_ad_group(client, customer_id)

    print("\n▶ STEP 2: Add 12 event keywords to Hiring Event ad group")
    add_keywords(client, customer_id, hiring_event_ag, HIRING_EVENT_KEYWORDS)

    print("\n▶ STEP 3: Add RSA to Hiring Event ad group")
    add_rsa(client, customer_id, hiring_event_ag)

    print("\n▶ STEP 4: Add picker packer keywords to p---generic_immediate--")
    add_keywords(
        client, customer_id,
        ad_group_resource(customer_id, AG_GENERIC_IMMEDIATE_ID),
        GENERIC_IMMEDIATE_KEYWORDS,
    )

    print("\n▶ STEP 5: Add picker packer keywords to p---warehouse--")
    add_keywords(
        client, customer_id,
        ad_group_resource(customer_id, AG_WAREHOUSE_ID),
        WAREHOUSE_KEYWORDS,
    )

    # ── APP CAMPAIGN ──────────────────────────────────────────────────────

    print("\n▶ STEP 6: Replace App campaign UAC copy")
    existing_ads = list_app_ads(client, customer_id, APP_AD_GROUP_ID)
    print(f"  Found {len(existing_ads)} existing app ad(s)")
    remove_app_ads(client, customer_id, existing_ads)
    create_app_ad(client, customer_id, APP_AD_GROUP_ID)

    print("\n══════════════════════════════════════════════════")
    print("  ✅ All changes applied successfully!")
    print("  Campaign is LIVE for Tennant Solutions Hiring Event")
    print("  Event: April 9, 2026 · 10am–2pm · Hamilton, OH")
    print("══════════════════════════════════════════════════\n")


if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"\n❌ Google Ads API error: {ex}")
        for error in ex.failure.errors:
            print(f"   Error: {error.message}")
            if error.location:
                for field_path in error.location.field_path_elements:
                    print(f"   Field: {field_path.field_name}")
        raise SystemExit(1)
