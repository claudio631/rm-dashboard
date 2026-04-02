#!/usr/bin/env python3
"""
Meta Ads Manager — Create, manage, and report on Meta (Facebook/Instagram) ad campaigns.

Usage:
    python3 scripts/meta-ads-manager.py test                    # Test connection
    python3 scripts/meta-ads-manager.py campaigns               # List active campaigns
    python3 scripts/meta-ads-manager.py create <brief.yaml>     # Create campaign from brief
    python3 scripts/meta-ads-manager.py pause <campaign_id>      # Pause a campaign
    python3 scripts/meta-ads-manager.py resume <campaign_id>     # Resume a campaign
    python3 scripts/meta-ads-manager.py insights <campaign_id>   # Get campaign performance
    python3 scripts/meta-ads-manager.py dashboard                # Generate HTML dashboard
"""

import os
import sys
import yaml
import json
from datetime import datetime, date, timedelta

# =============================================================================
# CONFIGURATION
# =============================================================================

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'meta-ads.yaml')


def load_config():
    """Load Meta Ads config from yaml file."""
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)['meta_ads']

    # Allow env var override for access token
    token = os.environ.get('META_ADS_ACCESS_TOKEN', config.get('access_token', ''))
    if not token:
        print("ERROR: No access token configured.")
        print("  Option 1: Set META_ADS_ACCESS_TOKEN environment variable")
        print("  Option 2: Add token to meta-ads.yaml")
        print()
        print("  Get a token at: https://developers.facebook.com/tools/explorer/")
        print("  Required permissions: ads_management, ads_read")
        sys.exit(1)

    config['access_token'] = token
    return config


def get_api(config):
    """Initialize the Meta Marketing API."""
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount

    api = FacebookAdsApi.init(
        app_id=config.get('app_id', ''),
        app_secret=config.get('app_secret', ''),
        access_token=config['access_token'],
        api_version=config.get('api_version', 'v21.0'),
    )

    account = AdAccount(f"act_{config['ad_account_id']}")
    return api, account


# =============================================================================
# COMMANDS
# =============================================================================

def cmd_test(config):
    """Test the API connection."""
    print("Testing Meta Ads API connection...")
    print(f"  Ad Account ID: act_{config['ad_account_id']}")

    try:
        api, account = get_api(config)
        info = account.api_get(fields=[
            'name', 'account_status', 'currency', 'timezone_name',
            'amount_spent', 'balance', 'business_name',
        ])
        print(f"  Connection: OK")
        print(f"  Account Name: {info.get('name', 'N/A')}")
        print(f"  Business: {info.get('business_name', 'N/A')}")
        print(f"  Status: {_account_status(info.get('account_status', 0))}")
        print(f"  Currency: {info.get('currency', 'N/A')}")
        print(f"  Timezone: {info.get('timezone_name', 'N/A')}")
        spent = int(info.get('amount_spent', 0)) / 100
        print(f"  Total Spent (lifetime): ${spent:,.2f}")
        print()
        print("Meta Ads API connected successfully!")
        return True
    except Exception as e:
        print(f"  Connection: FAILED")
        print(f"  Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Check your access token is valid")
        print("  2. Ensure token has ads_management + ads_read permissions")
        print(f"  3. Verify ad account ID: {config['ad_account_id']}")
        return False


def cmd_campaigns(config):
    """List active campaigns."""
    api, account = get_api(config)
    from facebook_business.adobjects.campaign import Campaign

    campaigns = account.get_campaigns(fields=[
        Campaign.Field.name,
        Campaign.Field.status,
        Campaign.Field.objective,
        Campaign.Field.daily_budget,
        Campaign.Field.lifetime_budget,
        Campaign.Field.start_time,
        Campaign.Field.stop_time,
        Campaign.Field.created_time,
    ])

    active = [c for c in campaigns if c.get('status') == 'ACTIVE']
    paused = [c for c in campaigns if c.get('status') == 'PAUSED']
    other = [c for c in campaigns if c.get('status') not in ('ACTIVE', 'PAUSED')]

    print(f"\nMeta Ads Campaigns — act_{config['ad_account_id']}")
    print(f"{'='*70}")

    for label, group in [("ACTIVE", active), ("PAUSED", paused)]:
        if not group:
            continue
        print(f"\n  {label} ({len(group)})")
        print(f"  {'-'*60}")
        for c in group:
            name = c.get('name', 'Unnamed')
            objective = c.get('objective', 'N/A')
            daily = int(c.get('daily_budget', 0)) / 100 if c.get('daily_budget') else None
            lifetime = int(c.get('lifetime_budget', 0)) / 100 if c.get('lifetime_budget') else None
            budget_str = f"${daily:.0f}/day" if daily else f"${lifetime:.0f} lifetime" if lifetime else "N/A"
            print(f"    [{c['id']}] {name}")
            print(f"      Objective: {objective} | Budget: {budget_str}")

    print(f"\n  Total: {len(active)} active, {len(paused)} paused, {len(other)} archived/deleted")
    return campaigns


def cmd_insights(config, campaign_id=None):
    """Get campaign performance insights."""
    api, account = get_api(config)

    # Default: last 30 days for the account
    params = {
        'time_range': {
            'since': (date.today() - timedelta(days=30)).isoformat(),
            'until': date.today().isoformat(),
        },
        'level': 'campaign',
    }

    fields = [
        'campaign_name', 'campaign_id', 'impressions', 'clicks',
        'spend', 'cpc', 'cpm', 'ctr', 'reach',
        'actions', 'cost_per_action_type',
    ]

    if campaign_id:
        from facebook_business.adobjects.campaign import Campaign
        campaign = Campaign(campaign_id)
        insights = campaign.get_insights(fields=fields, params=params)
    else:
        insights = account.get_insights(fields=fields, params=params)

    print(f"\nMeta Ads Performance — Last 30 Days")
    print(f"{'='*70}")

    for row in insights:
        name = row.get('campaign_name', 'Account Total')
        impressions = int(row.get('impressions', 0))
        clicks = int(row.get('clicks', 0))
        spend = float(row.get('spend', 0))
        cpc = float(row.get('cpc', 0))
        ctr = float(row.get('ctr', 0))
        reach = int(row.get('reach', 0))

        print(f"\n  {name}")
        print(f"    Spend: ${spend:,.2f} | Impressions: {impressions:,} | Reach: {reach:,}")
        print(f"    Clicks: {clicks:,} | CTR: {ctr:.2f}% | CPC: ${cpc:.2f}")

        # Parse actions (leads, app installs, etc.)
        actions = row.get('actions', [])
        if actions:
            print(f"    Actions:")
            for a in actions:
                print(f"      {a['action_type']}: {a['value']}")

    return insights


def cmd_create_campaign(config, brief_path):
    """Create a campaign from a YAML brief file."""
    api, account = get_api(config)
    from facebook_business.adobjects.campaign import Campaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.ad import Ad
    from facebook_business.adobjects.adcreative import AdCreative

    with open(brief_path, 'r') as f:
        brief = yaml.safe_load(f)

    camp = brief.get('campaign', {})
    print(f"\nCreating Meta campaign: {camp.get('name', 'Unnamed')}")
    print(f"  Objective: {camp.get('objective', 'OUTCOME_LEADS')}")
    print(f"  Daily Budget: ${camp.get('daily_budget', 0)}")

    # Step 1: Create Campaign
    campaign = Campaign(parent_id=f"act_{config['ad_account_id']}")
    campaign.update({
        Campaign.Field.name: camp['name'],
        Campaign.Field.objective: camp.get('objective', 'OUTCOME_LEADS'),
        Campaign.Field.status: Campaign.Status.paused,  # Always create paused
        Campaign.Field.special_ad_categories: camp.get('special_ad_categories', ['EMPLOYMENT']),
    })
    campaign.remote_create()
    campaign_id = campaign['id']
    print(f"  Campaign created: {campaign_id} (PAUSED)")

    # Step 2: Create Ad Sets
    for adset_brief in brief.get('adsets', []):
        adset = AdSet(parent_id=f"act_{config['ad_account_id']}")
        adset_params = {
            AdSet.Field.name: adset_brief['name'],
            AdSet.Field.campaign_id: campaign_id,
            AdSet.Field.daily_budget: int(adset_brief.get('daily_budget', camp.get('daily_budget', 20)) * 100),
            AdSet.Field.billing_event: adset_brief.get('billing_event', 'IMPRESSIONS'),
            AdSet.Field.optimization_goal: adset_brief.get('optimization_goal', 'LINK_CLICKS'),
            AdSet.Field.bid_strategy: adset_brief.get('bid_strategy', 'LOWEST_COST_WITHOUT_CAP'),
            AdSet.Field.status: AdSet.Status.paused,
            AdSet.Field.targeting: adset_brief.get('targeting', {}),
        }

        if adset_brief.get('start_time'):
            adset_params[AdSet.Field.start_time] = adset_brief['start_time']
        if adset_brief.get('end_time'):
            adset_params[AdSet.Field.end_time] = adset_brief['end_time']

        adset.update(adset_params)
        adset.remote_create()
        adset_id = adset['id']
        print(f"  Ad Set created: {adset_id} — {adset_brief['name']}")

        # Step 3: Create Ads for each Ad Set
        for ad_brief in adset_brief.get('ads', []):
            # Create Creative
            creative = AdCreative(parent_id=f"act_{config['ad_account_id']}")
            creative_params = {
                AdCreative.Field.name: ad_brief.get('name', adset_brief['name'] + ' Creative'),
                AdCreative.Field.object_story_spec: {
                    'page_id': brief.get('page_id', ''),
                    'link_data': {
                        'link': ad_brief.get('url', ''),
                        'message': ad_brief.get('primary_text', ''),
                        'name': ad_brief.get('headline', ''),
                        'description': ad_brief.get('description', ''),
                        'call_to_action': {
                            'type': ad_brief.get('cta', 'APPLY_NOW'),
                            'value': {'link': ad_brief.get('url', '')},
                        },
                    },
                },
            }
            if ad_brief.get('image_hash'):
                creative_params[AdCreative.Field.object_story_spec]['link_data']['image_hash'] = ad_brief['image_hash']

            creative.update(creative_params)
            creative.remote_create()

            # Create Ad
            ad = Ad(parent_id=f"act_{config['ad_account_id']}")
            ad.update({
                Ad.Field.name: ad_brief.get('name', 'Ad'),
                Ad.Field.adset_id: adset_id,
                Ad.Field.creative: {'creative_id': creative['id']},
                Ad.Field.status: Ad.Status.paused,
            })
            ad.remote_create()
            print(f"    Ad created: {ad['id']} — {ad_brief.get('name', 'Ad')}")

    print(f"\nCampaign ready! All components created in PAUSED state.")
    print(f"  Campaign ID: {campaign_id}")
    print(f"  Review at: https://business.facebook.com/adsmanager/manage/campaigns?act={config['ad_account_id']}")
    print(f"  To launch: python3 scripts/meta-ads-manager.py resume {campaign_id}")
    return campaign_id


def cmd_pause(config, campaign_id):
    """Pause a campaign."""
    api, account = get_api(config)
    from facebook_business.adobjects.campaign import Campaign

    campaign = Campaign(campaign_id)
    campaign.update({Campaign.Field.status: Campaign.Status.paused})
    campaign.remote_update()
    print(f"Campaign {campaign_id} paused.")


def cmd_resume(config, campaign_id):
    """Resume a campaign."""
    api, account = get_api(config)
    from facebook_business.adobjects.campaign import Campaign

    campaign = Campaign(campaign_id)
    campaign.update({Campaign.Field.status: Campaign.Status.active})
    campaign.remote_update()
    print(f"Campaign {campaign_id} resumed (ACTIVE).")


def cmd_dashboard(config):
    """Generate an HTML dashboard of Meta Ads performance."""
    api, account = get_api(config)

    # Get campaigns with insights
    params = {
        'time_range': {
            'since': (date.today() - timedelta(days=30)).isoformat(),
            'until': date.today().isoformat(),
        },
        'level': 'campaign',
    }

    fields = [
        'campaign_name', 'campaign_id', 'impressions', 'clicks',
        'spend', 'cpc', 'cpm', 'ctr', 'reach',
        'actions', 'cost_per_action_type',
    ]

    insights = account.get_insights(fields=fields, params=params)
    today_str = date.today().strftime("%Y-%m-%d")

    # Build HTML
    rows_html = ""
    total_spend = total_clicks = total_impressions = 0

    for row in insights:
        name = row.get('campaign_name', '—')
        impressions = int(row.get('impressions', 0))
        clicks = int(row.get('clicks', 0))
        spend = float(row.get('spend', 0))
        cpc = float(row.get('cpc', 0)) if row.get('cpc') else 0
        ctr = float(row.get('ctr', 0)) if row.get('ctr') else 0
        reach = int(row.get('reach', 0))

        total_spend += spend
        total_clicks += clicks
        total_impressions += impressions

        rows_html += f"""<tr>
            <td style="text-align:left">{name}</td>
            <td>${spend:,.2f}</td>
            <td>{impressions:,}</td>
            <td>{reach:,}</td>
            <td>{clicks:,}</td>
            <td>{ctr:.2f}%</td>
            <td>${cpc:.2f}</td>
        </tr>\n"""

    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    avg_ctr = total_clicks / total_impressions * 100 if total_impressions > 0 else 0

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Meta Ads Dashboard — {today_str}</title>
<style>
    body {{ font-family: -apple-system, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
    h1 {{ border-bottom: 3px solid #1877F2; padding-bottom: 8px; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0; }}
    .kpi {{ background: #f0f2f5; border-radius: 8px; padding: 16px; text-align: center; }}
    .kpi .value {{ font-size: 28px; font-weight: bold; color: #1877F2; }}
    .kpi .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
    th {{ background: #1877F2; color: white; padding: 10px; text-align: center; }}
    th:first-child {{ text-align: left; }}
    td {{ padding: 8px 10px; border-bottom: 1px solid #eee; text-align: center; }}
    td:first-child {{ text-align: left; }}
    tr:hover {{ background: #f5f7fa; }}
</style></head><body>
<h1>Meta Ads Dashboard</h1>
<p>Period: Last 30 days | Generated: {today_str} | Account: act_{config['ad_account_id']}</p>
<div class="kpi-grid">
    <div class="kpi"><div class="value">${total_spend:,.2f}</div><div class="label">Total Spend</div></div>
    <div class="kpi"><div class="value">{total_clicks:,}</div><div class="label">Total Clicks</div></div>
    <div class="kpi"><div class="value">{avg_ctr:.2f}%</div><div class="label">Avg CTR</div></div>
    <div class="kpi"><div class="value">${avg_cpc:.2f}</div><div class="label">Avg CPC</div></div>
</div>
<table>
<tr><th>Campaign</th><th>Spend</th><th>Impressions</th><th>Reach</th><th>Clicks</th><th>CTR</th><th>CPC</th></tr>
{rows_html}
</table>
</body></html>"""

    output_path = os.path.expanduser(f"~/RM-Team-Ai/docs/reports/meta-ads-dashboard-{today_str}.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html)
    print(f"Dashboard saved: {output_path}")
    return output_path


# =============================================================================
# HELPERS
# =============================================================================

def _account_status(code):
    statuses = {1: 'ACTIVE', 2: 'DISABLED', 3: 'UNSETTLED', 7: 'PENDING_RISK_REVIEW',
                8: 'PENDING_SETTLEMENT', 9: 'IN_GRACE_PERIOD', 100: 'PENDING_CLOSURE',
                101: 'CLOSED', 201: 'ANY_ACTIVE', 202: 'ANY_CLOSED'}
    return statuses.get(code, f'UNKNOWN ({code})')


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1].lower()
    config = load_config()

    if command == 'test':
        cmd_test(config)
    elif command == 'campaigns':
        cmd_campaigns(config)
    elif command == 'insights':
        cid = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_insights(config, cid)
    elif command == 'create':
        if len(sys.argv) < 3:
            print("Usage: meta-ads-manager.py create <brief.yaml>")
            sys.exit(1)
        cmd_create_campaign(config, sys.argv[2])
    elif command == 'pause':
        if len(sys.argv) < 3:
            print("Usage: meta-ads-manager.py pause <campaign_id>")
            sys.exit(1)
        cmd_pause(config, sys.argv[2])
    elif command == 'resume':
        if len(sys.argv) < 3:
            print("Usage: meta-ads-manager.py resume <campaign_id>")
            sys.exit(1)
        cmd_resume(config, sys.argv[2])
    elif command == 'dashboard':
        cmd_dashboard(config)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
