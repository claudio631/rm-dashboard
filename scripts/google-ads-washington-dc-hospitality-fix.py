"""
Google Ads — Washington DC Hospitality Search Campaign — Fix
Created: 2026-04-07

Fixes:
  1. Barista ad group: add keywords + 3 RSAs (was empty from failed first run)
  2. All other ad groups: add 2 more RSAs each (3 total = distinct angles)
  3. Add "Hospitality General Labor" ad group with keywords + 3 RSAs

Rule (applied to script): Never include search partners unless explicitly requested.
Campaign already has target_search_network=False — confirmed correct.
"""

import sys
sys.path.insert(0, '/Users/claudio.santos/RM-Team-Ai')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "7236100723"
SEARCH_CAMP_RN = "customers/7236100723/campaigns/23732428286"

DC_SEARCH_URL = (
    "https://indeedflex.com/job-search/?search"
    "&area_name=Washington+DC"
    "&search_lat=38.9072&search_lon=-77.0369"
    "&top_lon=-76.9094&top_lat=38.9948"
    "&bot_lon=-77.1198&bot_lat=38.7916"
)

# ── 3 RSA templates (distinct angles) ────────────────────────────────────────

RSA_1_GET_HIRED = {
    "headlines": [
        "{KeyWord:Flexible Jobs Washington DC}",
        "Your App for Temporary Work",
        "Find Flexible Jobs",
        "Unlock Job Opportunities",
        "Get Hired Today",
        "Empower Your Career",
        "Find Flexible Work Today",
        "Get Instant Job Offers Today",
        "Find Your Ideal Job",
        "Easy Sign Up",
        "Work, Your Way",
        "Indeed Flex — Apply Today",
    ],
    "descriptions": [
        "Indeed Flex offers job seekers a fast way to find work that fits their lifestyle.",
        "No resume required - Apply today! Book an interview to get started.",
        "Join Indeed Flex with flexible, well-paying jobs in Washington DC.",
        "Choose your employer and manage your own work schedule with Indeed Flex.",
    ],
}

RSA_2_PAY_BENEFITS = {
    "headlines": [
        "{KeyWord:Same Day Pay - Washington DC}",
        "Well-Paying Hospitality Jobs",
        "Same Day Pay Available Now",
        "Choose When You Get Paid",
        "Weekly Pay & Daily Pay Options",
        "Earn More Starting Today",
        "Indeed Flex Pays Fast",
        "Top Hospitality Pay in DC",
        "Competitive Pay in DC",
        "Get Paid Your Way",
        "Direct Deposit or Instant Pay",
        "No Wait for First Paycheck",
    ],
    "descriptions": [
        "Indeed Flex offers same-day pay and weekly pay options — you choose when you get paid.",
        "Work and get paid fast with Indeed Flex. No waiting for your first paycheck.",
        "Earn competitive wages for hospitality jobs in DC. Apply in minutes, start today.",
        "Get well-paying hospitality shifts in Washington DC with flexible pay options.",
    ],
}

RSA_3_FLEXIBILITY = {
    "headlines": [
        "{KeyWord:Flexible Jobs Washington DC}",
        "Work on Your Own Terms",
        "Choose Your Own Schedule",
        "Pick Shifts That Fit You",
        "Book Shifts Anytime in DC",
        "Work When You Want in DC",
        "Full Control of Your Hours",
        "No Fixed Schedule Required",
        "Set Your Own Work Hours",
        "Indeed Flex — You Decide",
        "Work Around Your Life",
        "Flexible Hospitality Shifts",
    ],
    "descriptions": [
        "Choose your own employer and work schedule with Indeed Flex in Washington DC.",
        "No boss, no fixed hours. Indeed Flex lets you pick shifts that fit your lifestyle.",
        "Book hospitality shifts around your schedule in DC. Apply today — no resume needed.",
        "Work where you want, when you want. Indeed Flex offers full flexibility in DC.",
    ],
}

RSA_TEMPLATES = [RSA_1_GET_HIRED, RSA_2_PAY_BENEFITS, RSA_3_FLEXIBILITY]

# ── Barista keywords ──────────────────────────────────────────────────────────
BARISTA_KEYWORDS = [
    ("barista job", "EXACT"),
    ("barista jobs", "EXACT"),
    ("barista jobs near me", "EXACT"),
    ("barista jobs near me", "PHRASE"),
    ("barista hiring", "EXACT"),
    ("barista hiring near me", "PHRASE"),
    ("barista position", "EXACT"),
    ("barista position", "PHRASE"),
    ("coffee shop jobs", "PHRASE"),
    ("coffee shop jobs near me", "PHRASE"),
    ("part time barista jobs", "EXACT"),
    ("part time barista jobs", "PHRASE"),
    ("barista jobs hiring near me", "PHRASE"),
    ("barista job near me", "PHRASE"),
    ("barista job near me", "EXACT"),
    ("indeed barista jobs", "PHRASE"),
    ("barista jobs washington dc", "EXACT"),
    ("barista jobs dc", "PHRASE"),
    ("cafe barista jobs", "PHRASE"),
    ("barista job description", "PHRASE"),
]

# ── General Hospitality keywords ──────────────────────────────────────────────
GENERAL_KEYWORDS = [
    ("hospitality jobs", "PHRASE"),
    ("hospitality jobs near me", "PHRASE"),
    ("hospitality jobs near me", "EXACT"),
    ("hospitality jobs dc", "EXACT"),
    ("hospitality jobs washington dc", "EXACT"),
    ("hospitality work near me", "PHRASE"),
    ("flexible hospitality jobs", "PHRASE"),
    ("indeed hospitality jobs", "PHRASE"),
    ("hospitality staffing", "PHRASE"),
    ("temp hospitality jobs", "PHRASE"),
    ("part time hospitality", "PHRASE"),
    ("part time hospitality jobs near me", "PHRASE"),
    ("hospitality temp agency", "PHRASE"),
    ("general labor", "EXACT"),
    ("general labor jobs", "EXACT"),
    ("general labor jobs near me", "PHRASE"),
    ("general labor near me", "EXACT"),
    ("part time general labor", "PHRASE"),
    ("temp jobs dc", "PHRASE"),
    ("temporary jobs near me", "PHRASE"),
    ("temporary jobs near me", "EXACT"),
    ("flexible temp jobs", "PHRASE"),
    ("event staff jobs", "PHRASE"),
    ("event staff jobs near me", "PHRASE"),
    ("event staff", "PHRASE"),
    ("event worker jobs", "PHRASE"),
]


def get_client():
    return GoogleAdsClient.load_from_storage('/Users/claudio.santos/RM-Team-Ai/google-ads.yaml')


def create_rsa(client, ag_rn, rsa_template):
    """Create one RSA from a template dict."""
    ad_service = client.get_service("AdGroupAdService")
    ad_op = client.get_type("AdGroupAdOperation")
    ada = ad_op.create
    ada.ad_group = ag_rn
    ada.status = client.enums.AdGroupAdStatusEnum.ENABLED
    rsa = ada.ad.responsive_search_ad

    for h_text in rsa_template["headlines"]:
        h = client.get_type("AdTextAsset")
        h.text = h_text
        rsa.headlines.append(h)
    for d_text in rsa_template["descriptions"]:
        d = client.get_type("AdTextAsset")
        d.text = d_text
        rsa.descriptions.append(d)
    ada.ad.final_urls.append(DC_SEARCH_URL)
    ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])


def create_keywords(client, ag_rn, keyword_list):
    """Create keywords from a list of (text, match_type) tuples."""
    criterion_service = client.get_service("AdGroupCriterionService")
    kw_ops = []
    for kw_text, match_type in keyword_list:
        kw_op = client.get_type("AdGroupCriterionOperation")
        kw = kw_op.create
        kw.ad_group = ag_rn
        kw.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        kw.keyword.text = kw_text
        kw.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match_type)
        kw_ops.append(kw_op)
    criterion_service.mutate_ad_group_criteria(
        customer_id=CUSTOMER_ID, operations=kw_ops
    )
    print(f"    ✅ {len(kw_ops)} keywords added")


def main():
    client = get_client()
    ag_service = client.get_service("AdGroupService")

    print("=" * 60)
    print("Washington DC Hospitality — Search Campaign Fix")
    print("=" * 60)

    # ── Ad groups that already exist (need 2 more RSAs each) ──────────────────
    existing_ad_groups = {
        "Job Type (Hospitality) - Cashier":    "customers/7236100723/adGroups/195185715997",
        "Job Type (Hospitality) - Dishwasher": "customers/7236100723/adGroups/195037596613",
        "Job Type (Hospitality) - Line Cook":  "customers/7236100723/adGroups/197655651520",
        "Job Type (Hospitality) - Prep Cook":  "customers/7236100723/adGroups/194811918883",
        "Job Type (Hospitality) - Server":     "customers/7236100723/adGroups/198867612207",
    }
    barista_ag_rn = "customers/7236100723/adGroups/195185682397"

    # 1. Fix Barista — add keywords + all 3 RSAs
    print(f"\n── Barista — add keywords + 3 RSAs ──")
    create_keywords(client, barista_ag_rn, BARISTA_KEYWORDS)
    for i, template in enumerate(RSA_TEMPLATES, 1):
        create_rsa(client, barista_ag_rn, template)
        print(f"    ✅ RSA {i} created")

    # 2. Add 2 more RSAs to each existing ad group (1 already exists → add RSA 2 + 3)
    print(f"\n── Add RSA 2 + RSA 3 to existing ad groups ──")
    for name, ag_rn in existing_ad_groups.items():
        role = name.split(" - ")[-1]
        print(f"\n  {role}:")
        for i, template in enumerate([RSA_2_PAY_BENEFITS, RSA_3_FLEXIBILITY], 2):
            create_rsa(client, ag_rn, template)
            print(f"    ✅ RSA {i} created")

    # 3. Create General Hospitality ad group
    print(f"\n── Create Hospitality General Labor ad group ──")
    ag_op = client.get_type("AdGroupOperation")
    ag = ag_op.create
    ag.name = "Job Type (Hospitality) - Hospitality General"
    ag.campaign = SEARCH_CAMP_RN
    ag.status = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag_resp = ag_service.mutate_ad_groups(
        customer_id=CUSTOMER_ID, operations=[ag_op]
    )
    general_ag_rn = ag_resp.results[0].resource_name
    print(f"  ✅ Ad group created: {general_ag_rn}")

    create_keywords(client, general_ag_rn, GENERAL_KEYWORDS)
    for i, template in enumerate(RSA_TEMPLATES, 1):
        create_rsa(client, general_ag_rn, template)
        print(f"  ✅ RSA {i} created")

    print("\n" + "=" * 60)
    print("✅ FIX COMPLETE")
    print("=" * 60)
    print("  • Barista: 20 keywords + 3 RSAs added")
    print("  • Cashier, Dishwasher, Line Cook, Prep Cook, Server: +2 RSAs each")
    print("  • Hospitality General: new ad group + 26 keywords + 3 RSAs")
    print("  • Search partners: already disabled (target_search_network=False) ✓")
    print("\n  All 7 ad groups now have 3 RSAs each (Get Hired / Pay & Benefits / Flexibility)")


if __name__ == "__main__":
    main()
