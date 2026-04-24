#!/usr/bin/env python3
"""
Add Phoenix BAU-style broad ad groups to the Smyrna Industrial Hiring Event Search campaign.
Adds 5 new ad groups with broader keyword themes (BROAD + PHRASE mix) + 3 RSAs each.

Target campaign: p-b2c-google-search-us-bofu-bau-smyrna-industrial-hiring-event-04242026
Campaign ID: 23770830412

Run: python3 scripts/google-ads-smyrna-hiring-event-add-adgroups.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"
CAMPAIGN_ID = "23770830412"
CAMPAIGN_RN = f"customers/{CUSTOMER_ID}/campaigns/{CAMPAIGN_ID}"

FINAL_URL = (
    "https://indeedflex.com/find-jobs/lp/hiring-event/"
    "?utm_source=google&utm_medium=cpc"
    "&link_value=syft://jobs/browse/504297"
    "&employer=NA&metro=nashville"
    "&role=warehouse-operative"
    "&utm_campaign=ontrac-ingram-hiring-event-smyrna-tn"
)

# ═══════════════════════════════════════════════════════════════════════════
# NEW AD GROUPS — Phoenix BAU model
# ═══════════════════════════════════════════════════════════════════════════

NEW_AD_GROUPS = [
    {
        "name": "p---generic_immediate--",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("immediate start jobs", "PHRASE"),
            ("immediate start jobs nashville", "PHRASE"),
            ("immediate start jobs smyrna tn", "PHRASE"),
            ("jobs hiring immediately near me", "PHRASE"),
            ("hiring immediately warehouse", "PHRASE"),
            ("start work this week", "PHRASE"),
            ("jobs you can start immediately", "PHRASE"),
        ],
    },
    {
        "name": "p---temp_keywords-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("temp agency", "BROAD"),
            ("temp agency", "PHRASE"),
            ("temp agency", "EXACT"),
            ("temp work agency", "PHRASE"),
            ("temping agencies", "PHRASE"),
            ("temping agency", "PHRASE"),
            ("temping agency", "EXACT"),
            ("temporary recruitment agency", "PHRASE"),
            ("temporary recruitment agency", "EXACT"),
            ("temp staffing agency nashville", "PHRASE"),
            ("temp jobs nashville tn", "PHRASE"),
        ],
    },
    {
        "name": "p-industrial---warehouse",
        "cpc_bid_micros": 2_000_000,
        "keywords": [
            ("warehouse temporary jobs", "BROAD"),
            ("warehouse temporary jobs", "PHRASE"),
            ("part time warehouse jobs", "BROAD"),
            ("part time warehouse jobs", "PHRASE"),
            ("Warehouse Operative job", "PHRASE"),
            ("Warehouse Operative flexible", "PHRASE"),
            ("Warehouse Operative temp", "PHRASE"),
            ("Warehouse Associate job", "PHRASE"),
            ("warehouse weekend jobs", "PHRASE"),
            ("temporary warehouse jobs nashville", "PHRASE"),
            ("warehouse jobs hiring now tn", "PHRASE"),
        ],
    },
    {
        "name": "p---generic-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("temp jobs", "PHRASE"),
            ("temporary jobs", "PHRASE"),
            ("temporary work", "EXACT"),
            ("weekend jobs", "PHRASE"),
            ("weekend temp work", "PHRASE"),
            ("flexible jobs nashville", "PHRASE"),
            ("temporary jobs nashville tn", "PHRASE"),
        ],
    },
    {
        "name": "p---agency_keywords-",
        "cpc_bid_micros": 1_500_000,
        "keywords": [
            ("agency jobs", "EXACT"),
            ("agency work", "EXACT"),
            ("job agency", "PHRASE"),
            ("employment agency", "PHRASE"),
            ("recruitment agency", "PHRASE"),
            ("agency recruitment", "PHRASE"),
            ("staffing agency nashville", "PHRASE"),
            ("job agency nashville tn", "PHRASE"),
        ],
    },
]

# RSA variants — same 3-angle strategy adapted for broader themes
RSA_VARIANTS = [
    {
        "label": "Urgency",
        "path1": "Hiring-Event",
        "path2": "Smyrna-TN",
        "headlines": [
            "Hiring Event — April 24th",
            "Smyrna TN · Thu Apr 24",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Register Before Spots Fill Up",
            "Get Hired Today — Apr 24",
            "Meet Recruiters Face to Face",
            "Indeed Flex Hiring Event",
            "Warehouse Jobs Hiring Now",
            "Work Near La Vergne TN",
            "1st & 2nd Shift Available",
            "Same Day Pay Available",
            "This Thursday — Apr 24",
            "$75 Referral Bonus",
            "Limited Spots — Register Now",
        ],
        "descriptions": [
            "Join us Apr 24, 9am-3pm at Courtyard Marriott, Smyrna TN. Get hired on the spot!",
            "No long process. Meet our recruiters & get an instant offer on April 24th. Sign up free.",
            "Walk in, interview live, and leave with a job offer on April 24 in Smyrna, TN.",
            "Limited spots left. Register today for the Indeed Flex hiring event on April 24th, 2026.",
        ],
    },
    {
        "label": "Pay & Benefits",
        "path1": "Warehouse-Jobs",
        "path2": "Smyrna-TN",
        "headlines": [
            "Warehouse Jobs $17–$18/Hr",
            "Same Day Pay Available",
            "$75 Referral Bonus",
            "Health & Vision Benefits",
            "Warehouse Work $17.50/Hr",
            "Full-Time Potential Available",
            "Hiring Event — April 24th",
            "Smyrna TN · Thu Apr 24",
            "Get Paid Same Day or Next Day",
            "Health & Dental Coverage",
            "Instant Job Offer on the Spot",
            "Walk In, Walk Out Employed",
            "Long & Short-Term Work",
            "Competitive Pay + Benefits",
            "Indeed Flex Hiring Event",
        ],
        "descriptions": [
            "Warehouse roles $17.50-$18/hr. Same Day Pay & health benefits. Apply now.",
            "$75 per referral, Same Day Pay & full health benefits. Join us April 24th.",
            "Competitive pay $17.50-$18/hr, health/dental/vision & Same Day Pay. Join us Apr 24.",
            "Come to our Apr 24 hiring event. Leave with a $17.50-$18/hr offer + full benefits.",
        ],
    },
    {
        "label": "Process & Opportunity",
        "path1": "Warehouse-Jobs",
        "path2": "Nashville-TN",
        "headlines": [
            "No Long Application Process",
            "Get Hired in One Day",
            "Meet Recruiters Face to Face",
            "Start Working This Week",
            "Full-Time Potential Available",
            "Warehouse Jobs Hiring Now",
            "Flexible 1st & 2nd Shifts",
            "Hiring Event — April 24th",
            "Smyrna TN · Thu Apr 24",
            "Walk In, Walk Out Employed",
            "Indeed Flex Hiring Event",
            "Warehouse Jobs $17–$18/Hr",
            "Apply in Minutes on Site",
            "Same Day Pay Available",
            "This Thursday — Apr 24",
        ],
        "descriptions": [
            "Indeed Flex hiring event — walk in & leave with a job offer. 1st & 2nd shift openings.",
            "Skip the wait. Interview live with recruiters on April 24 & start working this week.",
            "Full-time opportunities available. Attend Apr 24 at Courtyard Marriott, Smyrna, TN.",
            "Warehouse roles open now. Walk in on April 24 & leave with a job offer. No wait.",
        ],
    },
]


def main():
    client = GoogleAdsClient.load_from_storage(YAML_PATH)
    ag_svc   = client.get_service("AdGroupService")
    ad_svc   = client.get_service("AdGroupAdService")
    crit_svc = client.get_service("AdGroupCriterionService")
    me       = client.enums.KeywordMatchTypeEnum

    print("\n═══════════════════════════════════════════════════════════════")
    print("  Smyrna Hiring Event — Adding Broad Ad Groups (Phoenix model)")
    print(f"  Campaign ID: {CAMPAIGN_ID}")
    print("═══════════════════════════════════════════════════════════════\n")

    for ag_data in NEW_AD_GROUPS:
        print(f"── Ad Group: {ag_data['name']} ──")

        # Create ad group
        ag_op = client.get_type("AdGroupOperation")
        ag    = ag_op.create
        ag.name           = ag_data["name"]
        ag.campaign       = CAMPAIGN_RN
        ag.status         = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_          = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ag.cpc_bid_micros = ag_data["cpc_bid_micros"]
        ag_resp = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
        ag_rn   = ag_resp.results[0].resource_name
        ag_id   = ag_rn.split("/")[-1]
        print(f"  ✅ Ad group created: {ag_id}")

        # 3 RSAs
        for variant in RSA_VARIANTS:
            ad_op = client.get_type("AdGroupAdOperation")
            ada   = ad_op.create
            ada.ad_group = ag_rn
            ada.status   = client.enums.AdGroupAdStatusEnum.ENABLED
            rsa          = ada.ad.responsive_search_ad
            rsa.path1    = variant["path1"]
            rsa.path2    = variant["path2"]
            ada.ad.final_urls.append(FINAL_URL)
            for hl in variant["headlines"]:
                asset      = client.get_type("AdTextAsset")
                asset.text = hl
                rsa.headlines.append(asset)
            for desc in variant["descriptions"]:
                asset      = client.get_type("AdTextAsset")
                asset.text = desc
                rsa.descriptions.append(asset)
            ad_svc.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
            print(f"  ✅ RSA [{variant['label']}]: {variant['path1']}/{variant['path2']}")

        # Keywords
        kw_ops = []
        for kw_text, match_type in ag_data["keywords"]:
            kw_op = client.get_type("AdGroupCriterionOperation")
            kw    = kw_op.create
            kw.ad_group           = ag_rn
            kw.status             = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw.keyword.text       = kw_text
            kw.keyword.match_type = getattr(me, match_type)
            kw_ops.append(kw_op)
        crit_svc.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=kw_ops)
        print(f"  ✅ {len(kw_ops)} keywords added ({ag_data['name']})\n")

    print("═══════════════════════════════════════════════════════════════")
    print("  ✅ ALL AD GROUPS ADDED")
    print("═══════════════════════════════════════════════════════════════")
    print(f"\n  Campaign now has 8 ad groups total:")
    print(f"    3 original (event-focused) + 5 new (broad BAU-style)")
    print(f"    Each with 3 RSAs = 24 total RSAs\n")


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
