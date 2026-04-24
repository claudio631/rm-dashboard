#!/usr/bin/env python3
"""
TikTok Ads Manager — Read, manage, and report on TikTok ad campaigns.

Usage:
    python3 scripts/tiktok-ads-manager.py auth                       # OAuth2 flow (browser)
    python3 scripts/tiktok-ads-manager.py test                       # Test connection
    python3 scripts/tiktok-ads-manager.py accounts                   # List advertisers
    python3 scripts/tiktok-ads-manager.py campaigns                  # List campaigns
    python3 scripts/tiktok-ads-manager.py adgroups <campaign_id>     # List ad groups
    python3 scripts/tiktok-ads-manager.py ads <adgroup_id>           # List ads
    python3 scripts/tiktok-ads-manager.py insights [campaign_id]     # Performance (last 30d)
    python3 scripts/tiktok-ads-manager.py dashboard                  # HTML dashboard
    python3 scripts/tiktok-ads-manager.py pause <campaign_id>        # Pause campaign
    python3 scripts/tiktok-ads-manager.py resume <campaign_id>       # Resume campaign
    python3 scripts/tiktok-ads-manager.py budget <campaign_id> <usd> # Update daily budget

Setup:
    1. Create a TikTok developer app at https://business-api.tiktok.com/portal
       (request scopes: Ad Account Management, Campaign Management, Ad Group Management,
        Ad Management, Creative Management, Reporting, Audience Management)
    2. Wait for TikTok approval (1-5 business days)
    3. Add credentials to .env:
       TIKTOK_APP_ID=your_app_id
       TIKTOK_APP_SECRET=your_app_secret
       TIKTOK_REDIRECT_URI=http://localhost:3000/tiktok/callback
       TIKTOK_ADVERTISER_ID=your_advertiser_id
    4. Run: python3 scripts/tiktok-ads-manager.py auth
       (one-time — exchanges auth code for long-lived access token)
    5. pip install requests

Sandbox mode:
    Add TIKTOK_SANDBOX=true to .env to point at sandbox-ads.tiktok.com
    Sandbox tokens are issued instantly in the developer portal — no OAuth needed.
"""

import os
import sys
import json
import webbrowser
import urllib.parse
from datetime import date, timedelta

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

DOTENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
TOKEN_CACHE = os.path.join(os.path.dirname(__file__), '..', '.tiktok-token.json')

PROD_BASE_URL = "https://business-api.tiktok.com/open_api/v1.3"
SANDBOX_BASE_URL = "https://sandbox-ads.tiktok.com/open_api/v1.3"

AUTH_URL = "https://business-api.tiktok.com/portal/auth"

USER_AGENT = "RM-Team-AI/1.0 (Indeed Flex)"


def load_env():
    """Load credentials from .env file."""
    env = {}
    if os.path.exists(DOTENV_PATH):
        with open(DOTENV_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env[key.strip()] = val.strip()
    return env


def get_config():
    """Get TikTok API config from .env."""
    env = load_env()
    app_id = os.environ.get('TIKTOK_APP_ID', env.get('TIKTOK_APP_ID', ''))
    app_secret = os.environ.get('TIKTOK_APP_SECRET', env.get('TIKTOK_APP_SECRET', ''))
    redirect_uri = os.environ.get('TIKTOK_REDIRECT_URI', env.get('TIKTOK_REDIRECT_URI', 'http://localhost:3000/tiktok/callback'))
    advertiser_id = os.environ.get('TIKTOK_ADVERTISER_ID', env.get('TIKTOK_ADVERTISER_ID', ''))
    sandbox = os.environ.get('TIKTOK_SANDBOX', env.get('TIKTOK_SANDBOX', 'false')).lower() == 'true'
    sandbox_token = os.environ.get('TIKTOK_SANDBOX_TOKEN', env.get('TIKTOK_SANDBOX_TOKEN', ''))

    if not app_id or not app_secret:
        print("ERROR: TikTok API credentials not configured.")
        print("  Add to .env:")
        print("    TIKTOK_APP_ID=your_app_id")
        print("    TIKTOK_APP_SECRET=your_app_secret")
        print("    TIKTOK_REDIRECT_URI=http://localhost:3000/tiktok/callback")
        print("    TIKTOK_ADVERTISER_ID=your_advertiser_id")
        print()
        print("  Get these from https://business-api.tiktok.com/portal")
        sys.exit(1)

    return {
        'app_id': app_id,
        'app_secret': app_secret,
        'redirect_uri': redirect_uri,
        'advertiser_id': advertiser_id,
        'sandbox': sandbox,
        'sandbox_token': sandbox_token,
        'base_url': SANDBOX_BASE_URL if sandbox else PROD_BASE_URL,
    }


# =============================================================================
# AUTH — OAuth2 Authorization Code Flow
# =============================================================================

def get_access_token(config):
    """Get a valid access token from cache, sandbox env, or fail with auth instructions."""
    if config['sandbox'] and config['sandbox_token']:
        return config['sandbox_token']

    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, 'r') as f:
            token_data = json.load(f)
        if token_data.get('access_token'):
            return token_data['access_token']

    print("ERROR: No valid token found. Run auth first:")
    print("  python3 scripts/tiktok-ads-manager.py auth")
    sys.exit(1)


def cmd_auth(config):
    """Run OAuth2 authorization flow to get access token."""
    if config['sandbox']:
        print("Sandbox mode is enabled (TIKTOK_SANDBOX=true).")
        print("Sandbox uses a long-lived token issued in the developer portal.")
        print("Add TIKTOK_SANDBOX_TOKEN=<token> to .env — no OAuth flow needed.")
        return

    import secrets
    state = secrets.token_urlsafe(16)

    auth_params = urllib.parse.urlencode({
        'app_id': config['app_id'],
        'state': state,
        'redirect_uri': config['redirect_uri'],
    })
    auth_url = f"{AUTH_URL}?{auth_params}"

    print("Opening browser for TikTok authorization...")
    print(f"  URL: {auth_url}")
    print()
    print("After authorizing, you'll be redirected. Copy the FULL redirect URL")
    print("and paste it below (it will contain ?auth_code=... in the URL).")
    print()

    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    redirect_response = input("Paste the redirect URL here: ").strip()

    parsed = urllib.parse.urlparse(redirect_response)
    params = urllib.parse.parse_qs(parsed.query)

    if 'error' in params:
        print(f"ERROR: Authorization denied — {params['error'][0]}")
        sys.exit(1)

    auth_code = params.get('auth_code', params.get('code', [None]))[0]
    if not auth_code:
        print("ERROR: No auth_code found in URL.")
        sys.exit(1)

    returned_state = params.get('state', [None])[0]
    if returned_state and returned_state != state:
        print("WARNING: State mismatch — possible CSRF. Proceeding anyway.")

    # Exchange auth_code for access_token
    token_url = f"{config['base_url']}/oauth2/access_token/"
    resp = requests.post(token_url, json={
        'app_id': config['app_id'],
        'secret': config['app_secret'],
        'auth_code': auth_code,
    }, headers={'User-Agent': USER_AGENT})

    if resp.status_code != 200:
        print(f"ERROR: Token exchange HTTP {resp.status_code}")
        print(f"  {resp.text}")
        sys.exit(1)

    body = resp.json()
    if body.get('code') != 0:
        print(f"ERROR: Token exchange failed — {body.get('message', 'Unknown error')}")
        print(f"  Full response: {json.dumps(body, indent=2)}")
        sys.exit(1)

    data = body.get('data', {})
    token_data = {
        'access_token': data.get('access_token'),
        'advertiser_ids': data.get('advertiser_ids', []),
        'scope': data.get('scope', []),
    }

    with open(TOKEN_CACHE, 'w') as f:
        json.dump(token_data, f, indent=2)

    print()
    print("Authorization successful! Token saved.")
    print(f"  Token cache: {TOKEN_CACHE}")
    print(f"  Authorized advertisers: {token_data['advertiser_ids']}")
    print(f"  Scopes granted: {token_data['scope']}")
    print()
    print("  You can now use all other commands.")


# =============================================================================
# API HELPERS
# =============================================================================

def _check_response(resp):
    """Check TikTok API response — code == 0 means success."""
    if resp.status_code == 401:
        print("ERROR: Token expired or invalid. Re-run auth:")
        print("  python3 scripts/tiktok-ads-manager.py auth")
        sys.exit(1)
    resp.raise_for_status()
    body = resp.json()
    if body.get('code') != 0:
        msg = body.get('message', 'Unknown error')
        print(f"ERROR: TikTok API returned code {body.get('code')} — {msg}")
        if body.get('request_id'):
            print(f"  request_id: {body['request_id']}")
        sys.exit(1)
    return body


def api_get(config, endpoint, params=None):
    """Make an authenticated GET request to TikTok Marketing API."""
    token = get_access_token(config)
    headers = {
        'Access-Token': token,
        'User-Agent': USER_AGENT,
    }
    url = f"{config['base_url']}{endpoint}"
    resp = requests.get(url, headers=headers, params=params)
    return _check_response(resp)


def api_post(config, endpoint, data=None):
    """Make an authenticated POST request to TikTok Marketing API."""
    token = get_access_token(config)
    headers = {
        'Access-Token': token,
        'User-Agent': USER_AGENT,
        'Content-Type': 'application/json',
    }
    url = f"{config['base_url']}{endpoint}"
    resp = requests.post(url, headers=headers, json=data)
    return _check_response(resp)


# =============================================================================
# COMMANDS
# =============================================================================

def cmd_test(config):
    """Test the API connection."""
    print("Testing TikTok Marketing API connection...")
    print(f"  App ID: {config['app_id'][:8]}...")
    print(f"  Mode: {'SANDBOX' if config['sandbox'] else 'PRODUCTION'}")
    print(f"  Base URL: {config['base_url']}")

    if not config['advertiser_id']:
        print("  WARNING: TIKTOK_ADVERTISER_ID not set in .env")
        print("  Set it before running other commands.")

    try:
        body = api_get(config, "/advertiser/info/", params={
            'advertiser_ids': json.dumps([config['advertiser_id']]) if config['advertiser_id'] else '[]',
        })
        advertisers = body.get('data', {}).get('list', [])
        print(f"  Connection: OK")
        if advertisers:
            adv = advertisers[0]
            print(f"  Advertiser: {adv.get('name', 'N/A')} ({adv.get('advertiser_id', 'N/A')})")
            print(f"  Currency: {adv.get('currency', 'N/A')} | Status: {adv.get('status', 'N/A')}")
        print()
        print("TikTok Marketing API connected successfully!")
        return True
    except SystemExit:
        raise
    except Exception as e:
        print(f"  Connection: FAILED")
        print(f"  Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Run auth first: python3 scripts/tiktok-ads-manager.py auth")
        print("  2. Check TIKTOK_APP_ID, TIKTOK_APP_SECRET, TIKTOK_ADVERTISER_ID in .env")
        print("  3. Verify scopes were granted at https://business-api.tiktok.com/portal")
        return False


def cmd_accounts(config):
    """List advertisers accessible by this token."""
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, 'r') as f:
            token_data = json.load(f)
        advertiser_ids = token_data.get('advertiser_ids', [])
    else:
        advertiser_ids = [config['advertiser_id']] if config['advertiser_id'] else []

    if not advertiser_ids:
        print("No advertiser IDs found. Run auth first.")
        return []

    body = api_get(config, "/advertiser/info/", params={
        'advertiser_ids': json.dumps(advertiser_ids),
    })
    advertisers = body.get('data', {}).get('list', [])

    print(f"\nTikTok Ad Accounts")
    print(f"{'='*70}")

    for adv in advertisers:
        print(f"  [{adv.get('advertiser_id')}] {adv.get('name', 'Unnamed')}")
        print(f"    Currency: {adv.get('currency', 'N/A')} | Status: {adv.get('status', 'N/A')}")
        print(f"    Country: {adv.get('country', 'N/A')} | Timezone: {adv.get('timezone', 'N/A')}")

    print(f"\n  Total: {len(advertisers)} advertiser(s)")
    return advertisers


def cmd_campaigns(config):
    """List campaigns for the configured advertiser."""
    if not config['advertiser_id']:
        print("ERROR: TIKTOK_ADVERTISER_ID not set in .env")
        sys.exit(1)

    body = api_get(config, "/campaign/get/", params={
        'advertiser_id': config['advertiser_id'],
        'page_size': 100,
    })
    campaigns = body.get('data', {}).get('list', [])

    print(f"\nTikTok Campaigns — Advertiser: {config['advertiser_id']}")
    print(f"{'='*70}")

    enabled = [c for c in campaigns if c.get('operation_status') == 'ENABLE']
    disabled = [c for c in campaigns if c.get('operation_status') == 'DISABLE']

    for label, group in [("ENABLED", enabled), ("DISABLED", disabled)]:
        if not group:
            continue
        print(f"\n  {label} ({len(group)})")
        print(f"  {'-'*68}")
        for c in group:
            name = c.get('campaign_name', 'Unnamed')
            objective = c.get('objective_type', 'N/A')
            budget_mode = c.get('budget_mode', 'N/A')
            budget = c.get('budget', 0)
            if budget_mode == 'BUDGET_MODE_DAY':
                budget_str = f"${budget:.2f}/day"
            elif budget_mode == 'BUDGET_MODE_TOTAL':
                budget_str = f"${budget:.2f} total"
            else:
                budget_str = f"{budget_mode}"
            print(f"    [{c.get('campaign_id')}] {name}")
            print(f"      Objective: {objective} | Budget: {budget_str}")

    print(f"\n  Total: {len(enabled)} enabled, {len(disabled)} disabled")
    return campaigns


def cmd_adgroups(config, campaign_id):
    """List ad groups for a campaign."""
    if not config['advertiser_id']:
        print("ERROR: TIKTOK_ADVERTISER_ID not set in .env")
        sys.exit(1)

    filtering = json.dumps({'campaign_ids': [campaign_id]})
    body = api_get(config, "/adgroup/get/", params={
        'advertiser_id': config['advertiser_id'],
        'filtering': filtering,
        'page_size': 100,
    })
    adgroups = body.get('data', {}).get('list', [])

    print(f"\nAd Groups — Campaign: {campaign_id}")
    print(f"{'='*70}")

    for ag in adgroups:
        name = ag.get('adgroup_name', 'Unnamed')
        status = ag.get('operation_status', 'N/A')
        budget_mode = ag.get('budget_mode', 'N/A')
        budget = ag.get('budget', 0)
        opt_goal = ag.get('optimization_goal', 'N/A')
        placements = ', '.join(ag.get('placements', []))

        if budget_mode == 'BUDGET_MODE_DAY':
            budget_str = f"${budget:.2f}/day"
        elif budget_mode == 'BUDGET_MODE_TOTAL':
            budget_str = f"${budget:.2f} total"
        else:
            budget_str = f"{budget_mode}"

        print(f"  [{ag.get('adgroup_id')}] {name}")
        print(f"    Status: {status} | Budget: {budget_str} | Goal: {opt_goal}")
        if placements:
            print(f"    Placements: {placements}")

    print(f"\n  Total: {len(adgroups)} ad group(s)")
    return adgroups


def cmd_ads(config, adgroup_id):
    """List ads in an ad group."""
    if not config['advertiser_id']:
        print("ERROR: TIKTOK_ADVERTISER_ID not set in .env")
        sys.exit(1)

    filtering = json.dumps({'adgroup_ids': [adgroup_id]})
    body = api_get(config, "/ad/get/", params={
        'advertiser_id': config['advertiser_id'],
        'filtering': filtering,
        'page_size': 100,
    })
    ads = body.get('data', {}).get('list', [])

    print(f"\nAds — Ad Group: {adgroup_id}")
    print(f"{'='*70}")

    for ad in ads:
        name = ad.get('ad_name', 'Unnamed')
        status = ad.get('operation_status', 'N/A')
        ad_format = ad.get('ad_format', 'N/A')
        ad_text = ad.get('ad_text', '')[:80]
        cta = ad.get('call_to_action', 'N/A')

        print(f"  [{ad.get('ad_id')}] {name}")
        print(f"    Status: {status} | Format: {ad_format} | CTA: {cta}")
        if ad_text:
            print(f"    Text: {ad_text}")

    print(f"\n  Total: {len(ads)} ad(s)")
    return ads


def cmd_insights(config, campaign_id=None):
    """Get campaign performance insights for the last 30 days."""
    if not config['advertiser_id']:
        print("ERROR: TIKTOK_ADVERTISER_ID not set in .env")
        sys.exit(1)

    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    params = {
        'advertiser_id': config['advertiser_id'],
        'report_type': 'BASIC',
        'data_level': 'AUCTION_CAMPAIGN',
        'dimensions': json.dumps(['campaign_id']),
        'metrics': json.dumps([
            'campaign_name', 'spend', 'impressions', 'clicks',
            'ctr', 'cpc', 'cpm', 'conversion', 'cost_per_conversion',
            'conversion_rate',
        ]),
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'page_size': 100,
    }

    if campaign_id:
        params['filtering'] = json.dumps([{
            'field_name': 'campaign_ids',
            'filter_type': 'IN',
            'filter_value': json.dumps([campaign_id]),
        }])

    body = api_get(config, "/report/integrated/get/", params=params)
    rows = body.get('data', {}).get('list', [])

    print(f"\nTikTok Ads Performance — Last 30 Days")
    print(f"{'='*70}")

    total_spend = total_clicks = total_impressions = total_conversions = 0.0

    for row in rows:
        metrics = row.get('metrics', {})
        dimensions = row.get('dimensions', {})

        name = metrics.get('campaign_name', dimensions.get('campaign_id', 'Total'))
        spend = float(metrics.get('spend', 0))
        impressions = int(float(metrics.get('impressions', 0)))
        clicks = int(float(metrics.get('clicks', 0)))
        conversions = float(metrics.get('conversion', 0))
        ctr = float(metrics.get('ctr', 0))
        cpc = float(metrics.get('cpc', 0))
        cpa = float(metrics.get('cost_per_conversion', 0))

        total_spend += spend
        total_clicks += clicks
        total_impressions += impressions
        total_conversions += conversions

        print(f"\n  {name}")
        print(f"    Spend: ${spend:,.2f} | Impressions: {impressions:,}")
        print(f"    Clicks: {clicks:,} | CTR: {ctr:.2f}% | CPC: ${cpc:.2f}")
        print(f"    Conversions: {conversions:.0f} | CPA: ${cpa:.2f}")

    if rows:
        print(f"\n  TOTAL")
        print(f"    Spend: ${total_spend:,.2f} | Impressions: {total_impressions:,}")
        print(f"    Clicks: {total_clicks:,} | Conversions: {total_conversions:.0f}")
    else:
        print("  No data for this period.")

    return rows


def cmd_dashboard(config):
    """Generate an HTML dashboard of TikTok Ads performance."""
    if not config['advertiser_id']:
        print("ERROR: TIKTOK_ADVERTISER_ID not set in .env")
        sys.exit(1)

    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    body = api_get(config, "/report/integrated/get/", params={
        'advertiser_id': config['advertiser_id'],
        'report_type': 'BASIC',
        'data_level': 'AUCTION_CAMPAIGN',
        'dimensions': json.dumps(['campaign_id']),
        'metrics': json.dumps([
            'campaign_name', 'spend', 'impressions', 'clicks',
            'ctr', 'cpc', 'conversion', 'cost_per_conversion',
        ]),
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'page_size': 100,
    })
    rows = body.get('data', {}).get('list', [])

    today_str = date.today().strftime("%Y-%m-%d")
    rows_html = ""
    total_spend = total_clicks = total_impressions = total_conversions = 0.0

    for row in rows:
        metrics = row.get('metrics', {})
        name = metrics.get('campaign_name', '—')
        spend = float(metrics.get('spend', 0))
        impressions = int(float(metrics.get('impressions', 0)))
        clicks = int(float(metrics.get('clicks', 0)))
        conversions = float(metrics.get('conversion', 0))
        ctr = float(metrics.get('ctr', 0))
        cpc = float(metrics.get('cpc', 0))
        cpa = float(metrics.get('cost_per_conversion', 0))

        total_spend += spend
        total_clicks += clicks
        total_impressions += impressions
        total_conversions += conversions

        rows_html += f"""<tr>
            <td style="text-align:left">{name}</td>
            <td>${spend:,.2f}</td>
            <td>{impressions:,}</td>
            <td>{clicks:,}</td>
            <td>{ctr:.2f}%</td>
            <td>${cpc:.2f}</td>
            <td>{conversions:.0f}</td>
            <td>${cpa:.2f}</td>
        </tr>\n"""

    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    avg_ctr = total_clicks / total_impressions * 100 if total_impressions > 0 else 0
    avg_cpa = total_spend / total_conversions if total_conversions > 0 else 0

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>TikTok Ads Dashboard — {today_str}</title>
<style>
    body {{ font-family: -apple-system, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
    h1 {{ border-bottom: 3px solid #FE2C55; padding-bottom: 8px; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin: 20px 0; }}
    .kpi {{ background: #f8f9fa; border-radius: 8px; padding: 16px; text-align: center; }}
    .kpi .value {{ font-size: 24px; font-weight: bold; color: #FE2C55; }}
    .kpi .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
    th {{ background: #FE2C55; color: white; padding: 10px; text-align: center; }}
    th:first-child {{ text-align: left; }}
    td {{ padding: 8px 10px; border-bottom: 1px solid #eee; text-align: center; }}
    td:first-child {{ text-align: left; }}
    tr:hover {{ background: #fff5f7; }}
</style></head><body>
<h1>TikTok Ads Dashboard</h1>
<p>Period: Last 30 days | Generated: {today_str} | Advertiser: {config['advertiser_id']}</p>
<div class="kpi-grid">
    <div class="kpi"><div class="value">${total_spend:,.2f}</div><div class="label">Total Spend</div></div>
    <div class="kpi"><div class="value">{total_clicks:,}</div><div class="label">Clicks</div></div>
    <div class="kpi"><div class="value">{avg_ctr:.2f}%</div><div class="label">Avg CTR</div></div>
    <div class="kpi"><div class="value">${avg_cpc:.2f}</div><div class="label">Avg CPC</div></div>
    <div class="kpi"><div class="value">${avg_cpa:.2f}</div><div class="label">Avg CPA</div></div>
</div>
<table>
<tr><th>Campaign</th><th>Spend</th><th>Impressions</th><th>Clicks</th><th>CTR</th><th>CPC</th><th>Conv.</th><th>CPA</th></tr>
{rows_html}
</table>
</body></html>"""

    output_path = os.path.expanduser(f"~/RM-Team-Ai/docs/reports/tiktok-ads-dashboard-{today_str}.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html)
    print(f"Dashboard saved: {output_path}")
    return output_path


def cmd_pause(config, campaign_id):
    """Pause a campaign."""
    if not config['advertiser_id']:
        print("ERROR: TIKTOK_ADVERTISER_ID not set in .env")
        sys.exit(1)

    api_post(config, "/campaign/status/update/", {
        'advertiser_id': config['advertiser_id'],
        'campaign_ids': [campaign_id],
        'operation_status': 'DISABLE',
    })
    print(f"Campaign {campaign_id} paused (DISABLE).")


def cmd_resume(config, campaign_id):
    """Resume a campaign."""
    if not config['advertiser_id']:
        print("ERROR: TIKTOK_ADVERTISER_ID not set in .env")
        sys.exit(1)

    api_post(config, "/campaign/status/update/", {
        'advertiser_id': config['advertiser_id'],
        'campaign_ids': [campaign_id],
        'operation_status': 'ENABLE',
    })
    print(f"Campaign {campaign_id} resumed (ENABLE).")


def cmd_budget(config, campaign_id, amount_usd):
    """Update a campaign's daily budget (USD)."""
    if not config['advertiser_id']:
        print("ERROR: TIKTOK_ADVERTISER_ID not set in .env")
        sys.exit(1)

    try:
        amount = float(amount_usd)
    except ValueError:
        print(f"ERROR: Invalid budget amount: {amount_usd}")
        sys.exit(1)

    if amount < 50:
        print(f"WARNING: TikTok minimum daily campaign budget is $50/day. You set: ${amount:.2f}")

    api_post(config, "/campaign/update/", {
        'advertiser_id': config['advertiser_id'],
        'campaign_id': campaign_id,
        'budget': amount,
        'budget_mode': 'BUDGET_MODE_DAY',
    })
    print(f"Campaign {campaign_id} daily budget updated to ${amount:.2f}.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1].lower()
    config = get_config()

    if command == 'auth':
        cmd_auth(config)
    elif command == 'test':
        cmd_test(config)
    elif command == 'accounts':
        cmd_accounts(config)
    elif command == 'campaigns':
        cmd_campaigns(config)
    elif command == 'adgroups':
        if len(sys.argv) < 3:
            print("Usage: tiktok-ads-manager.py adgroups <campaign_id>")
            sys.exit(1)
        cmd_adgroups(config, sys.argv[2])
    elif command == 'ads':
        if len(sys.argv) < 3:
            print("Usage: tiktok-ads-manager.py ads <adgroup_id>")
            sys.exit(1)
        cmd_ads(config, sys.argv[2])
    elif command == 'insights':
        cid = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_insights(config, cid)
    elif command == 'dashboard':
        cmd_dashboard(config)
    elif command == 'pause':
        if len(sys.argv) < 3:
            print("Usage: tiktok-ads-manager.py pause <campaign_id>")
            sys.exit(1)
        cmd_pause(config, sys.argv[2])
    elif command == 'resume':
        if len(sys.argv) < 3:
            print("Usage: tiktok-ads-manager.py resume <campaign_id>")
            sys.exit(1)
        cmd_resume(config, sys.argv[2])
    elif command == 'budget':
        if len(sys.argv) < 4:
            print("Usage: tiktok-ads-manager.py budget <campaign_id> <usd_amount>")
            sys.exit(1)
        cmd_budget(config, sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
