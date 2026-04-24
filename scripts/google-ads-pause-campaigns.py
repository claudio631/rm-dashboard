#!/usr/bin/env python3
"""
Pause Google Ads campaigns by ID.

Usage:
    python3 google-ads-pause-campaigns.py --label "Orlando 04/20" --ids 23728216794 23728073943 23728073994 23737661476

Used by launchd jobs for automatic post-event pausing of hiring event campaigns.
Logs results to /Users/claudio.santos/RM-Team-Ai/logs/google-ads-pause.log
"""

import argparse
import datetime
import sys
from pathlib import Path

from google.ads.googleads.client import GoogleAdsClient
from google.protobuf import field_mask_pb2

GOOGLE_ADS_YAML = "/Users/claudio.santos/RM-Team-Ai/google-ads.yaml"
CUSTOMER_ID = "7236100723"
LOG_DIR = Path("/Users/claudio.santos/RM-Team-Ai/logs")
LOG_FILE = LOG_DIR / "google-ads-pause.log"


def log(message):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z").strip()
    line = f"[{ts}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def pause_campaigns(label, campaign_ids):
    log(f"=== {label} — pausing {len(campaign_ids)} campaigns ===")

    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    campaign_service = client.get_service("CampaignService")
    ga = client.get_service("GoogleAdsService")

    # Pre-check status
    ids_str = ",".join(str(i) for i in campaign_ids)
    q = f"""
        SELECT campaign.id, campaign.name, campaign.status
        FROM campaign
        WHERE campaign.id IN ({ids_str})
    """
    pre = {}
    for row in ga.search(customer_id=CUSTOMER_ID, query=q):
        pre[row.campaign.id] = (row.campaign.name, row.campaign.status.name)
        log(f"  BEFORE: [{row.campaign.status.name}] {row.campaign.name}")

    # Build pause operations
    operations = []
    for cid in campaign_ids:
        op = client.get_type("CampaignOperation")
        campaign = op.update
        campaign.resource_name = campaign_service.campaign_path(CUSTOMER_ID, cid)
        campaign.status = client.enums.CampaignStatusEnum.PAUSED
        op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))
        operations.append(op)

    # Execute
    try:
        response = campaign_service.mutate_campaigns(
            customer_id=CUSTOMER_ID,
            operations=operations,
        )
        log(f"  Mutate sent: {len(response.results)} results")
    except Exception as e:
        log(f"  ERROR: {e}")
        return False

    # Verify
    for row in ga.search(customer_id=CUSTOMER_ID, query=q):
        icon = "✅" if row.campaign.status.name == "PAUSED" else "❌"
        log(f"  AFTER: {icon} [{row.campaign.status.name}] {row.campaign.name}")

    log(f"=== {label} — done ===\n")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True, help="Event label for logging")
    parser.add_argument("--ids", nargs="+", type=int, required=True, help="Campaign IDs")
    args = parser.parse_args()

    ok = pause_campaigns(args.label, args.ids)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
