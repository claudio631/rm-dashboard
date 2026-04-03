#!/usr/bin/env python3
"""
Cincinnati Hiring Event — Fix display paths + add 2 more RSA variants per ad group.

Ad groups:
  203495826188  Hiring Event — Cincinnati
  186723659995  p---generic_immediate--
  186723660235  p---warehouse--

Copy designed by @copywriter (Quill), implemented by @ppc-paid-media-specialist (Parker).
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.protobuf import field_mask_pb2

YAML_PATH = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/497086"
    "&employer=tennant-solutions&metro=cincinnati"
    "&role=picker-packer&utm_campaign=hiring-event-tennant"
)

# ── Existing ad IDs (queried live) ────────────────────────────────────────
EXISTING_ADS = {
    "203495826188": {"ad_id": "803684166429", "resource": "customers/7236100723/adGroupAds/203495826188~803684166429"},
    "186723659995": {"ad_id": "803795902277", "resource": "customers/7236100723/adGroupAds/186723659995~803795902277"},
    "186723660235": {"ad_id": "803795902286", "resource": "customers/7236100723/adGroupAds/186723660235~803795902286"},
}

# ══════════════════════════════════════════════════════════════════════════
# COPY — designed by @copywriter (Quill)
# Each ad group gets 3 variants with distinct angle / narrative / CTA
# ══════════════════════════════════════════════════════════════════════════

AD_GROUPS = {

    # ── Hiring Event — Cincinnati ─────────────────────────────────────────
    "203495826188": {
        "name": "Hiring Event — Cincinnati",
        "path1": "Hiring-Event",
        "path2": "Cincinnati",
        "variants": [
            # Variant 2 — Pay & Benefits angle (Quill: money-first hook)
            {
                "label": "Pay & Benefits",
                "headlines": [
                    "$14–$15/Hr Warehouse Roles",
                    "Same Day Pay Available",
                    "$250 Bonus After 30 Days",
                    "Health & Dental Included",
                    "Walk In — Get Hired Apr 9",
                    "1st & 2nd Shift Open Now",
                    "Picker Packer Cincinnati OH",
                    "No Resume Required — Apply",
                    "Earn More With Indeed Flex",
                    "Immediate Warehouse Offers",
                    "$75 Referral Bonus Too",
                    "Benefits From Day One",
                    "Hamilton OH Hiring Apr 9",
                    "Steady Pay, Flex Schedule",
                    "Sign Up Free — Start Apr 9",
                ],
                "descriptions": [
                    "$14-$15/hr Picker Packer + Same Day Pay & $250 bonus. Walk in April 9, Hamilton OH.",
                    "Health, dental & vision from day one. Hiring event Hamilton, OH — Thu Apr 9. Apply free.",
                    "Real pay, real benefits. Visit us April 9, 10am-2pm, Hamilton OH. Get hired on the spot.",
                    "1st shift $14/hr or 2nd shift $15/hr. You choose. Get hired April 9 on the spot.",
                ],
            },
            # Variant 3 — Scarcity / FOMO angle (Quill: urgency, limited spots)
            {
                "label": "Scarcity / FOMO",
                "headlines": [
                    "Spots Filling Fast — Apr 9",
                    "Register Before It's Too Late",
                    "Last Chance — April 9 Event",
                    "Limited Warehouse Openings",
                    "Don't Miss This Hiring Event",
                    "Walk In, Leave Employed",
                    "Instant Offer — This Thursday",
                    "Warehouse Jobs $14–$15/Hr",
                    "Hiring Event — Register Now",
                    "Thu Apr 9 · Hamilton OH",
                    "Same Day Pay Available",
                    "$250 Bonus — Start This Week",
                    "Beat the Crowd — Sign Up Now",
                    "Jobs Gone by Friday — Act Now",
                    "Meet Recruiters Face to Face",
                ],
                "descriptions": [
                    "Limited spots at our April 9 hiring event. Register now and walk in ready to start.",
                    "Don't wait — warehouse jobs fill fast. 101 Knightsbridge Dr, Hamilton OH. This Thursday.",
                    "Walk in April 9, 10am-2pm and walk out with a job offer. No long application process.",
                    "Picker Packer openings closing fast. Same Day Pay + $250 bonus. Register free today.",
                ],
            },
        ],
    },

    # ── p---generic_immediate-- ───────────────────────────────────────────
    "186723659995": {
        "name": "p---generic_immediate--",
        "path1": "Jobs-Hiring-Now",
        "path2": "Cincinnati",
        "variants": [
            # Variant 2 — Speed / Ease angle (Quill: skip the process, fastest hire)
            {
                "label": "Speed & Ease",
                "headlines": [
                    "Hired in Minutes — Not Days",
                    "Skip the Long Application",
                    "Instant Job Offer Apr 9",
                    "Walk In, Work Tomorrow",
                    "Same Day Pay Warehouse Jobs",
                    "Picker Packer — Start Fast",
                    "No Resume? No Problem",
                    "Get Hired On the Spot",
                    "Immediate Warehouse Work",
                    "Cincinnati OH Hiring Now",
                    "$14–$15/Hr — Apply Today",
                    "1st & 2nd Shift Available",
                    "$250 Bonus After 30 Days",
                    "Indeed Flex Hires Fast",
                    "Meet Us April 9 Hamilton OH",
                ],
                "descriptions": [
                    "Skip the application. Walk in April 9 and get hired on the spot at our Cincinnati event.",
                    "Picker Packer jobs $14-$15/hr + Same Day Pay. Meet recruiters face to face. Start ASAP.",
                    "No long hiring process. Get you working fast — Thu April 9, 10am-2pm, Hamilton OH.",
                    "Immediate warehouse work. $250 attendance bonus + health benefits. Sign up free today.",
                ],
            },
            # Variant 3 — Lifestyle / Empowerment angle (Quill: you're in control)
            {
                "label": "Empowerment",
                "headlines": [
                    "Work That Works for You",
                    "Warehouse Jobs, Your Schedule",
                    "Choose Your Shift Cincinnati",
                    "1st or 2nd Shift — You Pick",
                    "Flexible Warehouse Work OH",
                    "Same Day Pay Every Week",
                    "$14–$15/Hr + Real Benefits",
                    "Picker Packer Near Cincinnati",
                    "Start This Week in Cincinnati",
                    "Job Offer in One Visit",
                    "April 9 Hiring Event — OH",
                    "Hamilton OH — Join Us",
                    "Work With Top Employers",
                    "$250 Bonus After 30 Days",
                    "Your Job, Your Terms",
                ],
                "descriptions": [
                    "Choose 1st or 2nd shift warehouse work in Cincinnati. $14-$15/hr with Same Day Pay.",
                    "Work on your terms. Picker Packer roles with flexible shifts & $250 attendance bonus.",
                    "Join Indeed Flex and take control. Hiring event April 9, Hamilton OH. Free to register.",
                    "Warehouse jobs that fit your life — instant offers, Same Day Pay. See us this Thursday.",
                ],
            },
        ],
    },

    # ── p---warehouse-- ───────────────────────────────────────────────────
    "186723660235": {
        "name": "p---warehouse--",
        "path1": "Warehouse-Jobs",
        "path2": "Cincinnati",
        "variants": [
            # Variant 2 — Shift Options angle (Quill: two shifts, you choose)
            {
                "label": "Shift Options",
                "headlines": [
                    "1st Shift 7AM–3:30PM Open",
                    "2nd Shift 3PM–Midnight Too",
                    "Pick Your Hours Cincinnati",
                    "Warehouse Work — Any Shift",
                    "Day or Night Shift Available",
                    "Picker Packer $14–$15/Hr",
                    "April 9 Hiring Event OH",
                    "Hamilton OH Warehouse Jobs",
                    "Get Hired Thu Apr 9",
                    "Same Day Pay Warehouse",
                    "Walk In — Leave Employed",
                    "2 Shifts · 1 Hiring Event",
                    "$250 Bonus After 30 Days",
                    "Indeed Flex Is Hiring Now",
                    "Apply at 101 Knightsbridge Dr",
                ],
                "descriptions": [
                    "1st shift (7am-3:30pm) $14/hr. 2nd shift (3pm-midnight) $15/hr. Get hired April 9.",
                    "Both shifts open at Tennant Solutions, Hamilton OH. Walk in April 9 for an instant offer.",
                    "Day or night — pick the shift that fits. Picker Packer + Same Day Pay. Hiring event Apr 9.",
                    "Two shifts, two pay rates. $14-$15/hr warehouse work near Cincinnati. Event is April 9.",
                ],
            },
            # Variant 3 — Trust / Employer Brand angle (Quill: credibility + stability)
            {
                "label": "Employer Trust",
                "headlines": [
                    "Work With Tennant Solutions",
                    "Trusted Employer Cincinnati",
                    "Stable Warehouse Work — OH",
                    "Full Benefits From Day One",
                    "Health, Dental & Vision OH",
                    "$14–$15/Hr Warehouse Roles",
                    "$250 Attendance Bonus",
                    "$75 Referral Bonus Too",
                    "Real Pay. Real Benefits.",
                    "Hiring Event This Thursday",
                    "April 9 · Hamilton OH",
                    "Same Day Pay Available",
                    "Instant Job Offer On Site",
                    "Mon–Fri Warehouse Schedule",
                    "Walk In, Walk Out Hired",
                ],
                "descriptions": [
                    "Work with Tennant Solutions, a trusted employer in Hamilton OH. Full benefits + $250 bonus.",
                    "Stable Mon-Fri warehouse work — $14-$15/hr, health insurance & Same Day Pay. Apply April 9.",
                    "Tennant Solutions + Indeed Flex: walk in April 9, meet the team, leave with a job offer.",
                    "Real warehouse jobs with real benefits — health, dental, vision. Instant offers on April 9.",
                ],
            },
        ],
    },
}


# ── Helpers ───────────────────────────────────────────────────────────────

def ad_resource(customer_id: str, ad_id: str) -> str:
    return f"customers/{customer_id}/ads/{ad_id}"


def ad_group_resource(customer_id: str, ag_id: str) -> str:
    return f"customers/{customer_id}/adGroups/{ag_id}"


# ── Step 1: Fix display paths on existing RSAs ────────────────────────────

def fix_display_paths(client, customer_id: str):
    """Updates path1/path2 on the 3 existing RSAs."""
    ad_service = client.get_service("AdService")
    operations = []

    for ag_id, config in AD_GROUPS.items():
        ad_id = EXISTING_ADS[ag_id]["ad_id"]
        op = client.get_type("AdOperation")
        ad = op.update
        ad.resource_name = ad_resource(customer_id, ad_id)
        ad.responsive_search_ad.path1 = config["path1"]
        ad.responsive_search_ad.path2 = config["path2"]
        op.update_mask.CopyFrom(
            field_mask_pb2.FieldMask(
                paths=["responsive_search_ad.path1", "responsive_search_ad.path2"]
            )
        )
        operations.append(op)
        print(f"   Queuing path fix: {config['name']} → path1='{config['path1']}' path2='{config['path2']}'")

    response = ad_service.mutate_ads(customer_id=customer_id, operations=operations)
    for result in response.results:
        print(f"   ✅ Paths updated: {result.resource_name}")


# ── Step 2: Create 2 new RSA variants per ad group ────────────────────────

def create_variant(client, customer_id: str, ag_id: str, config: dict, variant: dict) -> str:
    """Creates one RSA variant; returns resource name."""
    ad_group_ad_service = client.get_service("AdGroupAdService")
    op = client.get_type("AdGroupAdOperation")
    aga = op.create

    aga.ad_group = ad_group_resource(customer_id, ag_id)
    aga.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = aga.ad
    ad.final_urls.append(FINAL_URL)

    rsa = ad.responsive_search_ad
    rsa.path1 = config["path1"]
    rsa.path2 = config["path2"]

    for hl in variant["headlines"]:
        asset = client.get_type("AdTextAsset")
        asset.text = hl
        rsa.headlines.append(asset)

    for desc in variant["descriptions"]:
        asset = client.get_type("AdTextAsset")
        asset.text = desc
        rsa.descriptions.append(asset)

    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=[op],
    )
    return response.results[0].resource_name


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)

    print("\n══════════════════════════════════════════════════════")
    print("  Cincinnati — Fix Paths + 3-Variant Copy Per Ad Group")
    print("══════════════════════════════════════════════════════\n")

    # Step 1 — paths already fixed in previous run; skipping
    # fix_display_paths(client, CUSTOMER_ID)

    # Step 2 — create 2 new variants per ad group
    print("▶ Create 2 copy variants per ad group")
    for ag_id, config in AD_GROUPS.items():
        print(f"\n  ── {config['name']} (AG: {ag_id})")
        for variant in config["variants"]:
            rn = create_variant(client, CUSTOMER_ID, ag_id, config, variant)
            print(f"   ✅ [{variant['label']}] RSA created: {rn}")

    print("\n══════════════════════════════════════════════════════")
    print("  ✅ Done — each ad group now has 3 RSAs + display paths")
    print()
    print("  Ad Group                    | Ads | path1          | path2")
    print("  ──────────────────────────────────────────────────────────")
    print("  Hiring Event — Cincinnati   |  3  | Hiring-Event   | Cincinnati")
    print("  p---generic_immediate--     |  3  | Jobs-Hiring-Now| Cincinnati")
    print("  p---warehouse--             |  3  | Warehouse-Jobs | Cincinnati")
    print("══════════════════════════════════════════════════════\n")


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
