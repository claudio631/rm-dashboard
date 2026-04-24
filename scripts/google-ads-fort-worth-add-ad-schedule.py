#!/usr/bin/env python3
"""
Add ad schedule (Mon-Sun 06:00-23:00) to Fort Worth Hospitality BAU campaigns.
Search: 23766390416  |  P.Max: 23766391346  |  App: 23766403193

Run: python3 scripts/google-ads-fort-worth-add-ad-schedule.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

CAMPAIGN_IDS = {
    "Search": "23766390416",
    "P.Max":  "23766391346",
    "App":    "23766403193",
}

DAYS = [
    "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY",
    "FRIDAY", "SATURDAY", "SUNDAY",
]


def add_ad_schedule(client, crit_svc, campaign_rn):
    ops = []
    dow_enum    = client.enums.DayOfWeekEnum
    minute_enum = client.enums.MinuteOfHourEnum

    for day in DAYS:
        op  = client.get_type("CampaignCriterionOperation")
        c   = op.create
        c.campaign = campaign_rn
        c.status   = client.enums.CampaignCriterionStatusEnum.ENABLED
        sched = c.ad_schedule
        sched.day_of_week  = getattr(dow_enum, day)
        sched.start_hour   = 6
        sched.start_minute = minute_enum.ZERO
        sched.end_hour     = 23
        sched.end_minute   = minute_enum.ZERO
        ops.append(op)

    crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)
    return len(ops)


def main():
    client   = GoogleAdsClient.load_from_storage(YAML_PATH)
    crit_svc = client.get_service("CampaignCriterionService")

    print("\n═══════════════════════════════════════════════════════════════")
    print("  Fort Worth Hospitality — Add Ad Schedule (06:00–23:00)")
    print("═══════════════════════════════════════════════════════════════\n")

    for label, cid in CAMPAIGN_IDS.items():
        campaign_rn = f"customers/{CUSTOMER_ID}/campaigns/{cid}"
        n = add_ad_schedule(client, crit_svc, campaign_rn)
        print(f"  ✅ {label} ({cid}): {n} day schedules set (Mon–Sun 06:00–23:00)")

    print(f"\n  All 3 campaigns now running 06:00–23:00 only.\n")


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
