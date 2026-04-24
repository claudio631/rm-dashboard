#!/usr/bin/env python3
"""
Batch fix — add Mon-Sun 06:00-23:00 ad schedule to all campaigns
that have NO schedule at all (Group B from audit).

Run: python3 scripts/google-ads-fix-add-schedule-group-b.py
"""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

YAML_PATH   = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"

CAMPAIGNS = {
    # Search
    "23527110120": "B2C - US - Search - Hebron - Forklift - Stord",
    "23562449642": "US-Indeed-Flex-DSA",
    "23672936776": "b2c-test-client+role-search-cort",
    "23673372364": "b2c-test-client+role-search-ctdi",
    "23665705877": "b2c-test-client+role-search-ontrac",
    "23668436570": "b2c-test-client+role-search-stord",
    "21155925037": "p-b2c-google-search-us-bofu-competitor",
    "21190791291": "IndeedFlex - US - Dallas - B2B - Search",
    "23752430763": "p-b2c-google-search-us-bofu-bau-chicago-hiring-event-04232026",
    "23766291989": "p-b2c-google-search-us-bofu-bau-hebron-hiring-event-04282026",
    "23744408536": "p-b2c-google-search-us-bofu-bau-lebanon-warehouse-ontrac",
    "23721569237": "p-b2c-google-search-us-bofu-bau-nashville-hospitality-event-04252026",
    "23749457730": "p-b2c-google-search-us-bofu-bau-nashville-hospitality-lettuce",
    "23737661476": "p-b2c-google-search-us-bofu-bau-orlando-hiring-event-04202026",
    "23770830412": "p-b2c-google-search-us-bofu-bau-smyrna-hiring-event-04242026",
    "23732428286": "p-b2c-google-search-us-bofu-bau-washington_DC-hospitality",
    # PMax
    "23047596904": "p-b2c-google-p_max-us-bofu-bau-austin-hospitality",
    "23056169032": "p-b2c-google-p_max-us-bofu-bau-columbus-industrial",
    "23055860312": "p-b2c-google-p_max-us-bofu-bau-flower_mound-industrial",
    "23656289007": "p-b2c-google-p_max-us-bofu-bau-haslet-tx-industrial",
    "23045206287": "p-b2c-google-p_max-us-bofu-bau-hebron-industrial",
    "23647906683": "p-b2c-google-p_max-us-bofu-bau-houston-industrial",
    "23061322749": "p-b2c-google-p_max-us-bofu-bau-las_vegas-industrial",
    "23040335514": "p-b2c-google-p_max-us-bofu-bau-middleburg_heights-industrial",
    "23027498528": "p-b2c-google-p_max-us-bofu-bau-phoenix-industrial",
    "23061200115": "p-b2c-google-p_max-us-bofu-bau-reno-industrial",
    "23045524773": "p-b2c-google-p_max-us-bofu-bau-romeoville-industrial",
    "23727227430": "p-b2c-google-p_max-us-bofu-bau-washington_DC-hospitality",
    "23762398936": "p-b2c-google-pmax-us-bofu-bau-chicago-hiring-event-04232026",
    "23766292319": "p-b2c-google-pmax-us-bofu-bau-hebron-hiring-event-04282026",
    "23744446240": "p-b2c-google-pmax-us-bofu-bau-lebanon-warehouse-ontrac",
    "23721572363": "p-b2c-google-pmax-us-bofu-bau-nashville-hospitality-hiring-event-04252026",
    "23754779417": "p-b2c-google-pmax-us-bofu-bau-nashville-hospitality-lettuce",
    "23728073994": "p-b2c-google-pmax-us-bofu-bau-orlando-hiring-event-04202026",
    "23760904947": "p-b2c-google-pmax-us-bofu-bau-smyrna-hiring-event-04242026",
    "23045947347": "p-b2c-google_p_max-chicago-industrial",
    "23043219989": "p-b2c-google_p_max-dallas-hospitality",
    "23124333050": "p-b2c-google_p_max-logan_township-industrial",
    "23124159593": "p-b2c-google_p_max-paulsboro-industrial",
    "23284191774": "p-b2c-google_p_max-south_brunswick-industrial",
    "22314245660": "p-us-b2c-tofu-chicago-pmax",
    # Display
    "22790044558": "p-b2c-google-display-us-bau-chicago-industrial",
    "23656327893": "p-b2c-google-display-us-bau-haslet-tx-industrial",
    "23728073943": "p-b2c-google-display-us-bofu-bau-orlando-hiring-event-04202026",
    "23062815319": "p-b2c-google-display-us-rmk-bau-middleburg_heights-industrial",
    "23052892689": "p-b2c-google-display-us-rmk-bau-orlando-industrial",
    "23051640155": "p-b2c-google-display-us-rmk-bau-romeoville-industrial",
    "23128161346": "p-b2c-google_display-us-bofu-bau-logan_township-industrial",
    "23289450437": "p-b2c-google_display-us-bofu-bau-paulsboro-industrial",
    "23124251438": "p-b2c-google_display-us-bofu-bau-south_brunswick-industrial-rmk",
    "23732445044": "p-b2c-google_display-us-bofu-bau-washington_DC-hospitality",
    # Video
    "23743450442": "US-B2C-Hospitality-FIFA-Youtube-Dallas-TX",
}

DAYS = [
    "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY",
    "FRIDAY", "SATURDAY", "SUNDAY",
]


def add_schedule(client, crit_svc, cid):
    campaign_rn = f"customers/{CUSTOMER_ID}/campaigns/{cid}"
    ops = []
    dow_enum    = client.enums.DayOfWeekEnum
    minute_enum = client.enums.MinuteOfHourEnum
    for day in DAYS:
        op  = client.get_type("CampaignCriterionOperation")
        c   = op.create
        c.campaign = campaign_rn
        c.status   = client.enums.CampaignCriterionStatusEnum.ENABLED
        s = c.ad_schedule
        s.day_of_week  = getattr(dow_enum, day)
        s.start_hour   = 6
        s.start_minute = minute_enum.ZERO
        s.end_hour     = 23
        s.end_minute   = minute_enum.ZERO
        ops.append(op)
    crit_svc.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=ops)


def main():
    client   = GoogleAdsClient.load_from_storage(YAML_PATH)
    crit_svc = client.get_service("CampaignCriterionService")

    print(f"\n{'='*70}")
    print(f"  Batch fix — Add Mon–Sun 06:00–23:00 schedule ({len(CAMPAIGNS)} campaigns)")
    print(f"{'='*70}\n")

    ok = 0
    skipped = []

    for cid, name in CAMPAIGNS.items():
        try:
            add_schedule(client, crit_svc, cid)
            print(f"  ✅ [{cid}] {name}")
            ok += 1
        except GoogleAdsException as ex:
            err = ex.failure.errors[0]
            code = err.error_code
            print(f"  ⚠️  [{cid}] {name}")
            print(f"       SKIP: {err.message.strip()}")
            skipped.append((cid, name, err.message.strip()))

    print(f"\n{'='*70}")
    print(f"  Done: {ok} fixed, {len(skipped)} skipped")
    if skipped:
        print(f"\n  Skipped campaigns:")
        for cid, name, msg in skipped:
            print(f"    [{cid}] {name} — {msg}")
    print()


if __name__ == "__main__":
    main()
