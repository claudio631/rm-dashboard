#!/usr/bin/env python3
"""
Dallas Hospitality — Add Broad Ad Groups
Campaign: p-b2c-google-serach-us-bofu-bau-dallas-hospitality-eg (20992848464)

Adds 5 broad hospitality ad groups modeled from top performers in
p-b2c-google-search-us-bofu-bau-dallas-hospitality-eg (23043020861):
  - generic_temp (314 conv), generic_immediate (308), recruitment_agency (222),
    agency_temp (202), hospitality_general (196), part_time (130)

Each ad group: 3 RSAs (Urgency / Pay & Benefits / Process) + PHRASE keywords
Final URL: same SERP URL as existing enabled ad groups in campaign 20992848464
"""

import sys
sys.path.insert(0, '/Users/claudio.santos/RM-Team-Ai')

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"
CAMPAIGN_RN = "customers/7236100723/campaigns/20992848464"

FINAL_URL = (
    "https://indeedflex.com/job-search/?search"
    "&area_name=Dallas"
    "&search_lat=32.7766642&search_lon=-96.79698789999999"
    "&top_lon=-96.46375805411307&top_lat=33.0237920649461"
    "&bot_lon=-96.9993469629029&bot_lat=32.6175369971454"
)

PATH1 = "Hospitality-Job"   # 15 chars max
PATH2 = "Dallas-TX"

# ── RSA Variants (3 per ad group, different angles) ───────────────────────────

RSA_URGENCY = {
    "headlines": [
        "{KeyWord:Flexible Jobs Dallas}",
        "Hiring Now in Dallas TX",
        "Apply Today Start This Week",
        "Immediate Openings Dallas",
        "Don't Miss Out Apply Now",
        "Same Day Pay Available Now",
        "Hospitality Jobs Dallas TX",
        "Work Starts This Week",
        "Get Hired Fast in Dallas",
        "Temp Work in Dallas TX",
        "No Experience Required",
        "Find Flexible Jobs",
        "Flexible Hospitality Roles",
        "Work When You Want",
        "Easy Sign Up",
    ],
    "descriptions": [
        "Hiring now for hospitality jobs in Dallas, TX. Flexible shifts. Apply in minutes.",
        "Start working this week! Indeed Flex is hiring hospitality workers in Dallas, TX.",
        "No resume required. Apply for hospitality jobs in Dallas and book an interview today!",
        "Immediate start available. Indeed Flex is hiring for flexible hospitality roles in Dallas.",
    ],
}

RSA_PAY = {
    "headlines": [
        "{KeyWord:Flexible Jobs Dallas}",
        "Same Day Pay Available Now",
        "Choose When You Get Paid",
        "Flexible Schedules Dallas",
        "Hospitality Jobs Dallas TX",
        "Work on Your Own Terms",
        "Choose Your Schedule",
        "Get Paid Same Day",
        "No Experience Needed",
        "Your App for Flexible Work",
        "Temp Work in Dallas TX",
        "Choose Where & How to Work",
        "Manage Your Own Schedule",
        "Find Flexible Jobs",
        "Health Benefits Available",
    ],
    "descriptions": [
        "Indeed Flex offers job seekers a fast way to find work that fits their lifestyle.",
        "Choose your employer and manage your own work schedule with Indeed Flex.",
        "Get same-day pay for every shift. Join Indeed Flex for hospitality jobs in Dallas.",
        "Flexible hospitality jobs in Dallas, TX. Pick your shifts and get paid the same day.",
    ],
}

RSA_PROCESS = {
    "headlines": [
        "{KeyWord:Flexible Jobs Dallas}",
        "Your App for Temporary Work",
        "Unlock Job Opportunities",
        "No Resume Required",
        "Choose Where & How to Work",
        "Manage Your Own Schedule",
        "Easy Sign Up",
        "Work Your Way",
        "Get Instant Job Offers",
        "Hospitality Jobs Dallas TX",
        "Book an Interview Today",
        "Apply in Minutes",
        "Indeed Flex Apply Now",
        "Flexible Hospitality Roles",
        "Work That Suits Your Life",
    ],
    "descriptions": [
        "Indeed Flex offers job seekers a fast way to find work that fits their lifestyle.",
        "No resume required - Apply today! Book an interview to get started.",
        "Join Indeed Flex with flexible, well-paying hospitality jobs in Dallas.",
        "Choose where and how you work. Indeed Flex makes finding flex jobs in Dallas easy.",
    ],
}

RSA_VARIANTS = [RSA_URGENCY, RSA_PAY, RSA_PROCESS]
RSA_NAMES    = ["Urgency", "Pay & Benefits", "Process & Brand"]

# ── Ad group definitions ───────────────────────────────────────────────────────

AD_GROUPS = [
    {
        "name": "Broad Hospitality — Temp Jobs",
        "keywords": [
            "temp jobs",
            "temporary jobs",
            "weekend jobs",
            "temp work",
            "temp jobs dallas",
            "temporary work dallas",
            "weekend temp work",
        ],
    },
    {
        "name": "Broad Hospitality — Immediate Start",
        "keywords": [
            "immediate start jobs",
            "immediate start jobs dallas",
            "jobs start immediately",
            "start immediately jobs",
            "jobs hiring immediately",
            "immediate hire",
        ],
    },
    {
        "name": "Broad Hospitality — Hospitality General",
        "keywords": [
            "hospitality jobs",
            "hospitality job",
            "hospitality jobs hiring now",
            "hospitality temp job",
            "hospitality temporary jobs",
            "part time hospitality jobs",
            "temporary hospitality jobs",
            "hospitality jobs dallas",
            "hospitality part time",
            "hospitality weekend jobs",
        ],
    },
    {
        "name": "Broad Hospitality — Temp Agency",
        "keywords": [
            "temp agency",
            "temping agency",
            "employment agency",
            "job agency",
            "recruitment agency",
            "temporary work agency",
            "temp recruitment agency",
        ],
    },
    {
        "name": "Broad Hospitality — Part Time",
        "keywords": [
            "part time jobs dallas",
            "flexible jobs dallas",
            "indeed temporary jobs",
            "part time work",
            "flexible work",
            "part time jobs",
            "indeed temp jobs",
        ],
    },
]


def build_rsa(client, ag_rn, variant, ad_name):
    ad_op = client.get_type("AdGroupAdOperation")
    ada   = ad_op.create
    ada.ad_group = ag_rn
    ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED

    ad  = ada.ad
    ad.name = ad_name
    ad.final_urls.append(FINAL_URL)

    rsa = ad.responsive_search_ad
    rsa.path1 = PATH1
    rsa.path2 = PATH2

    for h_text in variant["headlines"]:
        h = client.get_type("AdTextAsset")
        h.text = h_text
        rsa.headlines.append(h)

    for d_text in variant["descriptions"]:
        d = client.get_type("AdTextAsset")
        d.text = d_text
        rsa.descriptions.append(d)

    return ad_op


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    ag_svc   = client.get_service("AdGroupService")
    ad_svc   = client.get_service("AdGroupAdService")
    kw_svc   = client.get_service("AdGroupCriterionService")

    print("\n" + "═" * 65)
    print("  Dallas Hospitality — Add Broad Ad Groups")
    print(f"  Campaign: 20992848464")
    print("═" * 65)

    results = []

    # Ad group 1 was already created on prior run (RSA failed on path1 length)
    EXISTING_AG = {
        "Broad Hospitality — Temp Jobs": "customers/7236100723/adGroups/196770063498",
    }

    for ag_def in AD_GROUPS:
        print(f"\n▶  Ad Group: {ag_def['name']}")

        if ag_def["name"] in EXISTING_AG:
            ag_rn = EXISTING_AG[ag_def["name"]]
            ag_id = ag_rn.split("/")[-1]
            print(f"     ✅ Ad group reused: {ag_id}")
        else:
            # Create ad group
            ag_op = client.get_type("AdGroupOperation")
            ag    = ag_op.create
            ag.name      = ag_def["name"]
            ag.campaign  = CAMPAIGN_RN
            ag.status    = client.enums.AdGroupStatusEnum.ENABLED
            ag.type_     = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

            ag_resp = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
            ag_rn   = ag_resp.results[0].resource_name
            ag_id   = ag_rn.split("/")[-1]
            print(f"     ✅ Ad group: {ag_id}")

        # Create 3 RSAs
        rsa_ops = [
            build_rsa(client, ag_rn, RSA_VARIANTS[i], f"{ag_def['name']} — {RSA_NAMES[i]}")
            for i in range(3)
        ]
        ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=rsa_ops)
        print(f"     ✅ 3 RSAs created (Urgency / Pay & Benefits / Process & Brand)")

        # Add keywords — PHRASE match only
        kw_ops = []
        for kw_text in ag_def["keywords"]:
            kw_op = client.get_type("AdGroupCriterionOperation")
            kw    = kw_op.create
            kw.ad_group            = ag_rn
            kw.status              = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw.keyword.text        = kw_text
            kw.keyword.match_type  = client.enums.KeywordMatchTypeEnum.PHRASE
            kw_ops.append(kw_op)

        kw_svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=kw_ops)
        print(f"     ✅ {len(kw_ops)} keywords (PHRASE)")

        results.append({"name": ag_def["name"], "id": ag_id, "kw_count": len(kw_ops)})

    # Summary
    print("\n" + "═" * 65)
    print("  ✅ ALL 5 AD GROUPS ADDED")
    print("═" * 65)
    for r in results:
        print(f"  {r['id']} — {r['name']} ({r['kw_count']} kw)")
    print(f"\n  Campaign: p-b2c-google-serach-us-bofu-bau-dallas-hospitality-eg")
    print(f"  RSAs/group: 3  |  Match type: PHRASE  |  Status: ENABLED")
    print("═" * 65 + "\n")


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
