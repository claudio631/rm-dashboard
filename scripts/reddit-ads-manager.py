#!/usr/bin/env python3
"""
Reddit Ads Manager — Create, manage, and report on Reddit ad campaigns.

Usage:
    python3 scripts/reddit-ads-manager.py test                    # Test connection
    python3 scripts/reddit-ads-manager.py accounts                # List ad accounts
    python3 scripts/reddit-ads-manager.py campaigns               # List campaigns
    python3 scripts/reddit-ads-manager.py create <brief.yaml>     # Create campaign from brief
    python3 scripts/reddit-ads-manager.py pause <campaign_id>     # Pause a campaign
    python3 scripts/reddit-ads-manager.py resume <campaign_id>    # Resume a campaign
    python3 scripts/reddit-ads-manager.py insights <campaign_id>  # Get campaign performance
    python3 scripts/reddit-ads-manager.py dashboard               # Generate HTML dashboard

Setup:
    1. Create a Reddit app at https://ads.reddit.com/developer-applications
    2. Add credentials to .env:
       REDDIT_CLIENT_ID=your_client_id
       REDDIT_CLIENT_SECRET=your_client_secret
       REDDIT_REDIRECT_URI=https://www.indeedflex.com/
    3. Run: python3 scripts/reddit-ads-manager.py auth
       (first time only — generates refresh token)
    4. pip install requests
"""

import os
import sys
import json
import webbrowser
import http.server
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

TOKEN_CACHE = os.path.join(os.path.dirname(__file__), '..', '.reddit-token.json')

BASE_URL = "https://ads-api.reddit.com/api/v3"
AUTH_URL = "https://www.reddit.com/api/v1/authorize"
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
SCOPES = "ads_read ads_manage"

USER_AGENT = "PPC-Manager-AI/1.0 (by Indeed Flex)"


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
    """Get Reddit API config from .env."""
    env = load_env()
    client_id = os.environ.get('REDDIT_CLIENT_ID', env.get('REDDIT_CLIENT_ID', ''))
    client_secret = os.environ.get('REDDIT_CLIENT_SECRET', env.get('REDDIT_CLIENT_SECRET', ''))
    redirect_uri = os.environ.get('REDDIT_REDIRECT_URI', env.get('REDDIT_REDIRECT_URI', ''))

    if not client_id or not client_secret:
        print("ERROR: Reddit API credentials not configured.")
        print("  Add to .env:")
        print("    REDDIT_CLIENT_ID=your_client_id")
        print("    REDDIT_CLIENT_SECRET=your_client_secret")
        print("    REDDIT_REDIRECT_URI=https://www.indeedflex.com/")
        sys.exit(1)

    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
    }


# =============================================================================
# AUTH — OAuth2 Authorization Code Flow
# =============================================================================

def get_access_token(config):
    """Get a valid access token, refreshing if needed."""
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, 'r') as f:
            token_data = json.load(f)

        # Try refresh if we have a refresh token
        if token_data.get('refresh_token'):
            new_token = refresh_access_token(config, token_data['refresh_token'])
            if new_token:
                return new_token

    print("ERROR: No valid token found. Run auth first:")
    print("  python3 scripts/reddit-ads-manager.py auth")
    sys.exit(1)


def refresh_access_token(config, refresh_token):
    """Refresh the access token."""
    resp = requests.post(TOKEN_URL, auth=(config['client_id'], config['client_secret']),
                         data={'grant_type': 'refresh_token', 'refresh_token': refresh_token},
                         headers={'User-Agent': USER_AGENT})
    if resp.status_code == 200:
        data = resp.json()
        # Save updated tokens
        token_data = {
            'access_token': data['access_token'],
            'refresh_token': data.get('refresh_token', refresh_token),
            'token_type': data.get('token_type', 'bearer'),
        }
        with open(TOKEN_CACHE, 'w') as f:
            json.dump(token_data, f)
        return data['access_token']
    return None


def cmd_auth(config):
    """Run OAuth2 authorization flow to get initial tokens."""
    import secrets
    state = secrets.token_urlsafe(16)

    auth_params = urllib.parse.urlencode({
        'client_id': config['client_id'],
        'response_type': 'code',
        'state': state,
        'redirect_uri': config['redirect_uri'],
        'duration': 'permanent',
        'scope': SCOPES,
    })
    auth_url = f"{AUTH_URL}?{auth_params}"

    print("Opening browser for Reddit authorization...")
    print(f"  URL: {auth_url}")
    print()
    print("After authorizing, you'll be redirected. Copy the FULL redirect URL")
    print("and paste it below (it will contain ?code=... in the URL).")
    print()

    webbrowser.open(auth_url)

    redirect_response = input("Paste the redirect URL here: ").strip()

    # Parse the authorization code from the redirect URL
    parsed = urllib.parse.urlparse(redirect_response)
    params = urllib.parse.parse_qs(parsed.query)

    if 'error' in params:
        print(f"ERROR: Authorization denied — {params['error'][0]}")
        sys.exit(1)

    code = params.get('code', [None])[0]
    if not code:
        print("ERROR: No authorization code found in URL.")
        sys.exit(1)

    returned_state = params.get('state', [None])[0]
    if returned_state != state:
        print("WARNING: State mismatch — possible CSRF. Proceeding anyway.")

    # Exchange code for tokens
    resp = requests.post(TOKEN_URL, auth=(config['client_id'], config['client_secret']),
                         data={
                             'grant_type': 'authorization_code',
                             'code': code,
                             'redirect_uri': config['redirect_uri'],
                         },
                         headers={'User-Agent': USER_AGENT})

    if resp.status_code != 200:
        print(f"ERROR: Token exchange failed ({resp.status_code})")
        print(f"  {resp.text}")
        sys.exit(1)

    data = resp.json()
    token_data = {
        'access_token': data['access_token'],
        'refresh_token': data.get('refresh_token', ''),
        'token_type': data.get('token_type', 'bearer'),
    }

    with open(TOKEN_CACHE, 'w') as f:
        json.dump(token_data, f)

    print()
    print("Authorization successful! Token saved.")
    print(f"  Token cache: {TOKEN_CACHE}")
    print("  You can now use all other commands.")


# =============================================================================
# API HELPERS
# =============================================================================

def api_get(config, endpoint, params=None):
    """Make an authenticated GET request to Reddit Ads API."""
    token = get_access_token(config)
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': USER_AGENT,
    }
    url = f"{BASE_URL}{endpoint}"
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 401:
        print("ERROR: Token expired or invalid. Re-run auth:")
        print("  python3 scripts/reddit-ads-manager.py auth")
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


def api_post(config, endpoint, data=None):
    """Make an authenticated POST request to Reddit Ads API."""
    token = get_access_token(config)
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': USER_AGENT,
        'Content-Type': 'application/json',
    }
    url = f"{BASE_URL}{endpoint}"
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code == 401:
        print("ERROR: Token expired or invalid. Re-run auth:")
        print("  python3 scripts/reddit-ads-manager.py auth")
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


def api_put(config, endpoint, data=None):
    """Make an authenticated PUT request to Reddit Ads API."""
    token = get_access_token(config)
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': USER_AGENT,
        'Content-Type': 'application/json',
    }
    url = f"{BASE_URL}{endpoint}"
    resp = requests.put(url, headers=headers, json=data)
    if resp.status_code == 401:
        print("ERROR: Token expired or invalid. Re-run auth:")
        print("  python3 scripts/reddit-ads-manager.py auth")
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


# =============================================================================
# COMMANDS
# =============================================================================

def cmd_test(config):
    """Test the API connection."""
    print("Testing Reddit Ads API connection...")
    print(f"  Client ID: {config['client_id'][:8]}...")

    try:
        data = api_get(config, "/me")
        print(f"  Connection: OK")
        print(f"  Account: {data.get('data', {}).get('name', 'N/A')}")
        print()
        print("Reddit Ads API connected successfully!")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"  Connection: FAILED")
        print(f"  Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Run auth first: python3 scripts/reddit-ads-manager.py auth")
        print("  2. Check client ID and secret in .env")
        return False
    except Exception as e:
        print(f"  Connection: FAILED")
        print(f"  Error: {e}")
        return False


def cmd_accounts(config):
    """List ad accounts."""
    data = api_get(config, "/me/accounts")
    accounts = data.get('data', [])

    print(f"\nReddit Ad Accounts")
    print(f"{'='*60}")

    for acct in accounts:
        print(f"  [{acct.get('id', '?')}] {acct.get('name', 'Unnamed')}")
        print(f"    Status: {acct.get('status', 'N/A')} | Currency: {acct.get('currency', 'USD')}")

    if not accounts:
        print("  No ad accounts found.")

    print(f"\n  Total: {len(accounts)} account(s)")
    return accounts


def cmd_campaigns(config):
    """List campaigns for the first ad account."""
    accounts = api_get(config, "/me/accounts").get('data', [])
    if not accounts:
        print("No ad accounts found.")
        return []

    account_id = accounts[0]['id']
    data = api_get(config, f"/accounts/{account_id}/campaigns")
    campaigns = data.get('data', [])

    print(f"\nReddit Campaigns — Account: {accounts[0].get('name', account_id)}")
    print(f"{'='*70}")

    active = [c for c in campaigns if c.get('configured_status') == 'ACTIVE']
    paused = [c for c in campaigns if c.get('configured_status') == 'PAUSED']

    for label, group in [("ACTIVE", active), ("PAUSED", paused)]:
        if not group:
            continue
        print(f"\n  {label} ({len(group)})")
        print(f"  {'-'*60}")
        for c in group:
            name = c.get('name', 'Unnamed')
            objective = c.get('objective', 'N/A')
            budget = c.get('budget_total_amount_micros')
            daily = c.get('budget_daily_amount_micros')
            if daily:
                budget_str = f"${int(daily) / 1_000_000:.0f}/day"
            elif budget:
                budget_str = f"${int(budget) / 1_000_000:.0f} total"
            else:
                budget_str = "N/A"
            print(f"    [{c['id']}] {name}")
            print(f"      Objective: {objective} | Budget: {budget_str}")

    print(f"\n  Total: {len(active)} active, {len(paused)} paused, {len(campaigns) - len(active) - len(paused)} other")
    return campaigns


def cmd_insights(config, campaign_id=None):
    """Get campaign performance insights."""
    accounts = api_get(config, "/me/accounts").get('data', [])
    if not accounts:
        print("No ad accounts found.")
        return

    account_id = accounts[0]['id']
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    params = {
        'starts_at': start_date.isoformat(),
        'ends_at': end_date.isoformat(),
    }

    if campaign_id:
        endpoint = f"/campaigns/{campaign_id}/reports"
    else:
        endpoint = f"/accounts/{account_id}/reports"

    data = api_get(config, endpoint, params=params)
    rows = data.get('data', [])

    print(f"\nReddit Ads Performance — Last 30 Days")
    print(f"{'='*70}")

    total_spend = total_clicks = total_impressions = 0

    for row in rows:
        name = row.get('campaign_name', row.get('campaign_id', 'Total'))
        impressions = int(row.get('impressions', 0))
        clicks = int(row.get('clicks', 0))
        spend_micros = int(row.get('spend_amount_micros', 0))
        spend = spend_micros / 1_000_000

        total_spend += spend
        total_clicks += clicks
        total_impressions += impressions

        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (spend / clicks) if clicks > 0 else 0

        print(f"\n  {name}")
        print(f"    Spend: ${spend:,.2f} | Impressions: {impressions:,}")
        print(f"    Clicks: {clicks:,} | CTR: {ctr:.2f}% | CPC: ${cpc:.2f}")

    if not rows:
        print("  No data for this period.")

    return rows


def cmd_create(config, brief_path):
    """Create a campaign from a YAML brief."""
    try:
        import yaml
    except ImportError:
        print("ERROR: pyyaml not installed. Run: pip install pyyaml")
        sys.exit(1)

    with open(brief_path, 'r') as f:
        brief = yaml.safe_load(f)

    accounts = api_get(config, "/me/accounts").get('data', [])
    if not accounts:
        print("No ad accounts found.")
        return
    account_id = accounts[0]['id']

    camp = brief.get('campaign', {})
    print(f"\nCreating Reddit campaign: {camp.get('name', 'Unnamed')}")
    print(f"  Objective: {camp.get('objective', 'CONVERSIONS')}")

    # Create campaign
    campaign_data = {
        'name': camp['name'],
        'objective': camp.get('objective', 'CONVERSIONS'),
        'configured_status': 'PAUSED',
        'is_paid': True,
    }

    if camp.get('daily_budget'):
        campaign_data['budget_daily_amount_micros'] = int(camp['daily_budget'] * 1_000_000)
    if camp.get('total_budget'):
        campaign_data['budget_total_amount_micros'] = int(camp['total_budget'] * 1_000_000)
    if camp.get('start_date'):
        campaign_data['start_at'] = camp['start_date']
    if camp.get('end_date'):
        campaign_data['end_at'] = camp['end_date']

    result = api_post(config, f"/accounts/{account_id}/campaigns", campaign_data)
    campaign_id = result.get('data', {}).get('id')
    print(f"  Campaign created: {campaign_id} (PAUSED)")

    # Create ad groups
    for ag_brief in brief.get('ad_groups', []):
        ag_data = {
            'name': ag_brief['name'],
            'campaign_id': campaign_id,
            'configured_status': 'PAUSED',
            'bid_strategy': ag_brief.get('bid_strategy', 'CPM'),
        }

        if ag_brief.get('bid_amount'):
            ag_data['bid_amount_micros'] = int(ag_brief['bid_amount'] * 1_000_000)

        # Targeting
        targeting = ag_brief.get('targeting', {})
        if targeting:
            ag_data['targeting'] = targeting

        ag_result = api_post(config, f"/accounts/{account_id}/adgroups", ag_data)
        ag_id = ag_result.get('data', {}).get('id')
        print(f"  Ad Group created: {ag_id} — {ag_brief['name']}")

    print(f"\nCampaign ready! Created in PAUSED state.")
    print(f"  Campaign ID: {campaign_id}")
    print(f"  Review at: https://ads.reddit.com/")
    print(f"  To launch: python3 scripts/reddit-ads-manager.py resume {campaign_id}")
    return campaign_id


def cmd_pause(config, campaign_id):
    """Pause a campaign."""
    api_put(config, f"/campaigns/{campaign_id}", {'configured_status': 'PAUSED'})
    print(f"Campaign {campaign_id} paused.")


def cmd_resume(config, campaign_id):
    """Resume a campaign."""
    api_put(config, f"/campaigns/{campaign_id}", {'configured_status': 'ACTIVE'})
    print(f"Campaign {campaign_id} resumed (ACTIVE).")


def cmd_dashboard(config):
    """Generate an HTML dashboard of Reddit Ads performance."""
    accounts = api_get(config, "/me/accounts").get('data', [])
    if not accounts:
        print("No ad accounts found.")
        return
    account_id = accounts[0]['id']
    account_name = accounts[0].get('name', account_id)

    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    data = api_get(config, f"/accounts/{account_id}/reports", params={
        'starts_at': start_date.isoformat(),
        'ends_at': end_date.isoformat(),
    })
    rows = data.get('data', [])

    today_str = date.today().strftime("%Y-%m-%d")
    rows_html = ""
    total_spend = total_clicks = total_impressions = 0

    for row in rows:
        name = row.get('campaign_name', '—')
        impressions = int(row.get('impressions', 0))
        clicks = int(row.get('clicks', 0))
        spend = int(row.get('spend_amount_micros', 0)) / 1_000_000

        total_spend += spend
        total_clicks += clicks
        total_impressions += impressions

        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (spend / clicks) if clicks > 0 else 0

        rows_html += f"""<tr>
            <td style="text-align:left">{name}</td>
            <td>${spend:,.2f}</td>
            <td>{impressions:,}</td>
            <td>{clicks:,}</td>
            <td>{ctr:.2f}%</td>
            <td>${cpc:.2f}</td>
        </tr>\n"""

    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    avg_ctr = total_clicks / total_impressions * 100 if total_impressions > 0 else 0

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>Reddit Ads Dashboard — {today_str}</title>
<style>
    body {{ font-family: -apple-system, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
    h1 {{ border-bottom: 3px solid #FF4500; padding-bottom: 8px; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0; }}
    .kpi {{ background: #f8f9fa; border-radius: 8px; padding: 16px; text-align: center; }}
    .kpi .value {{ font-size: 28px; font-weight: bold; color: #FF4500; }}
    .kpi .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
    th {{ background: #FF4500; color: white; padding: 10px; text-align: center; }}
    th:first-child {{ text-align: left; }}
    td {{ padding: 8px 10px; border-bottom: 1px solid #eee; text-align: center; }}
    td:first-child {{ text-align: left; }}
    tr:hover {{ background: #fff5f0; }}
</style></head><body>
<h1>Reddit Ads Dashboard</h1>
<p>Period: Last 30 days | Generated: {today_str} | Account: {account_name}</p>
<div class="kpi-grid">
    <div class="kpi"><div class="value">${total_spend:,.2f}</div><div class="label">Total Spend</div></div>
    <div class="kpi"><div class="value">{total_clicks:,}</div><div class="label">Total Clicks</div></div>
    <div class="kpi"><div class="value">{avg_ctr:.2f}%</div><div class="label">Avg CTR</div></div>
    <div class="kpi"><div class="value">${avg_cpc:.2f}</div><div class="label">Avg CPC</div></div>
</div>
<table>
<tr><th>Campaign</th><th>Spend</th><th>Impressions</th><th>Clicks</th><th>CTR</th><th>CPC</th></tr>
{rows_html}
</table>
</body></html>"""

    output_path = os.path.expanduser(f"~/RM-Team-Ai/docs/reports/reddit-ads-dashboard-{today_str}.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html)
    print(f"Dashboard saved: {output_path}")
    return output_path


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
    elif command == 'insights':
        cid = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_insights(config, cid)
    elif command == 'create':
        if len(sys.argv) < 3:
            print("Usage: reddit-ads-manager.py create <brief.yaml>")
            sys.exit(1)
        cmd_create(config, sys.argv[2])
    elif command == 'pause':
        if len(sys.argv) < 3:
            print("Usage: reddit-ads-manager.py pause <campaign_id>")
            sys.exit(1)
        cmd_pause(config, sys.argv[2])
    elif command == 'resume':
        if len(sys.argv) < 3:
            print("Usage: reddit-ads-manager.py resume <campaign_id>")
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
