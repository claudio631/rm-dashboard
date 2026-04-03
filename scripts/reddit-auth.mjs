#!/usr/bin/env node
/**
 * Reddit OAuth2 Manual Authorization Script
 * ==========================================
 * One-time script to authorize Reddit API access and store tokens in the DB.
 *
 * STEP 1: Run with --url to get the authorization link
 *   node scripts/reddit-auth.mjs --url
 *
 * STEP 2: Open the URL in browser, authorize the app.
 *   Reddit will redirect to https://www.indeedflex.com/?code=XXX&state=YYY
 *   Copy the value of the `code` parameter from the URL.
 *
 * STEP 3: Run with --exchange to exchange the code for tokens
 *   node scripts/reddit-auth.mjs --exchange CODE_FROM_URL
 *
 * STEP 4: Verify connection
 *   node scripts/reddit-auth.mjs --status
 */

import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import Database from "better-sqlite3";
import crypto from "crypto";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

// Load .env manually (no dotenv dependency needed)
function loadEnv() {
  const envPath = resolve(ROOT, ".env");
  const lines = readFileSync(envPath, "utf-8").split("\n");
  const env = {};
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const [key, ...rest] = trimmed.split("=");
    if (key && rest.length > 0) {
      env[key.trim()] = rest.join("=").trim();
    }
  }
  return env;
}

const env = loadEnv();
const CLIENT_ID = env.REDDIT_CLIENT_ID;
const CLIENT_SECRET = env.REDDIT_CLIENT_SECRET;
const REDIRECT_URI = env.REDDIT_REDIRECT_URI;
const SCOPES = ["identity", "read", "adsread"];

if (!CLIENT_ID || !CLIENT_SECRET || !REDIRECT_URI) {
  console.error("❌ Missing Reddit credentials in .env");
  process.exit(1);
}

// ── DB helpers ──────────────────────────────────────────────────────────────
function getDb() {
  const db = new Database(resolve(ROOT, "local.db"));
  db.pragma("journal_mode = WAL");
  return db;
}

function storeTokens(db, data) {
  const expiresAt = new Date(Date.now() + data.expires_in * 1000).toISOString();
  const now = new Date().toISOString();
  db.exec(`CREATE TABLE IF NOT EXISTS reddit_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    access_token TEXT NOT NULL,
    refresh_token TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    scope TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
  )`);
  db.prepare("DELETE FROM reddit_tokens").run();
  db.prepare(`
    INSERT INTO reddit_tokens (access_token, refresh_token, expires_at, scope, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
  `).run(data.access_token, data.refresh_token, expiresAt, data.scope, now, now);
}

// ── Commands ─────────────────────────────────────────────────────────────────
async function printAuthUrl() {
  const state = crypto.randomBytes(16).toString("hex");
  const params = new URLSearchParams({
    client_id: CLIENT_ID,
    response_type: "code",
    state,
    redirect_uri: REDIRECT_URI,
    duration: "permanent",
    scope: SCOPES.join(" "),
  });
  const url = `https://www.reddit.com/api/v1/authorize?${params}`;
  console.log("\n✅ Open this URL in your browser:\n");
  console.log(url);
  console.log("\nAfter authorizing, you will be redirected to:");
  console.log(`  ${REDIRECT_URI}?code=XXXX&state=${state}`);
  console.log("\nCopy the value of the `code` parameter and run:");
  console.log("  node scripts/reddit-auth.mjs --exchange <CODE>\n");
}

async function exchangeCode(code) {
  console.log("\n🔄 Exchanging code for tokens...\n");
  const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString("base64");

  const response = await fetch("https://www.reddit.com/api/v1/access_token", {
    method: "POST",
    headers: {
      Authorization: `Basic ${credentials}`,
      "Content-Type": "application/x-www-form-urlencoded",
      "User-Agent": "RM-Team-AI/1.0",
    },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      redirect_uri: REDIRECT_URI,
    }),
  });

  const data = await response.json();

  if (!response.ok || data.error) {
    console.error("❌ Token exchange failed:");
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  const db = getDb();
  storeTokens(db, data);

  console.log("✅ Tokens stored successfully!\n");
  console.log(`  Access token : ${data.access_token.substring(0, 20)}...`);
  console.log(`  Refresh token: ${data.refresh_token.substring(0, 20)}...`);
  console.log(`  Scope        : ${data.scope}`);
  console.log(`  Expires in   : ${data.expires_in}s (${Math.round(data.expires_in / 60)} minutes)`);
  console.log("\nRun `node scripts/reddit-auth.mjs --status` to verify.\n");
}

async function checkStatus() {
  const db = getDb();
  let rows;
  try {
    rows = db.prepare("SELECT * FROM reddit_tokens ORDER BY id DESC LIMIT 1").all();
  } catch {
    rows = [];
  }

  if (rows.length === 0) {
    console.log("\n❌ Not connected — no tokens stored.\n");
    console.log("Run: node scripts/reddit-auth.mjs --url\n");
    return;
  }

  const token = rows[0];
  const expiresAt = new Date(token.expires_at);
  const now = new Date();
  const minutesLeft = Math.round((expiresAt - now) / 60000);
  const isExpired = expiresAt < now;

  console.log("\n✅ Reddit connection status:\n");
  console.log(`  Connected    : true`);
  console.log(`  Scopes       : ${token.scope}`);
  console.log(`  Expires at   : ${token.expires_at}`);
  console.log(`  Status       : ${isExpired ? "⚠️  EXPIRED (will auto-refresh on next API call)" : `✅ Valid (${minutesLeft} min remaining)`}`);

  // Test a live API call
  console.log("\n🔄 Testing live API call to Reddit /api/v1/me ...\n");
  const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString("base64");

  let accessToken = token.access_token;
  if (isExpired) {
    console.log("  Token expired — refreshing...");
    const refreshResp = await fetch("https://www.reddit.com/api/v1/access_token", {
      method: "POST",
      headers: {
        Authorization: `Basic ${credentials}`,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "RM-Team-AI/1.0",
      },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: token.refresh_token,
      }),
    });
    const refreshData = await refreshResp.json();
    if (!refreshResp.ok) {
      console.error("  ❌ Refresh failed:", refreshData);
      return;
    }
    if (!refreshData.refresh_token) refreshData.refresh_token = token.refresh_token;
    storeTokens(db, refreshData);
    accessToken = refreshData.access_token;
    console.log("  ✅ Token refreshed\n");
  }

  const meResp = await fetch("https://oauth.reddit.com/api/v1/me", {
    headers: {
      Authorization: `bearer ${accessToken}`,
      "User-Agent": "RM-Team-AI/1.0",
    },
  });

  if (meResp.ok) {
    const me = await meResp.json();
    console.log(`  ✅ Authenticated as: u/${me.name}`);
    console.log(`  Account ID         : ${me.id}`);
  } else {
    const err = await meResp.text();
    console.error(`  ❌ API call failed (${meResp.status}): ${err}`);
  }
  console.log();
}

// ── Main ─────────────────────────────────────────────────────────────────────
const [,, flag, value] = process.argv;

switch (flag) {
  case "--url":
    await printAuthUrl();
    break;
  case "--exchange":
    if (!value) {
      console.error("Usage: node scripts/reddit-auth.mjs --exchange <CODE>");
      process.exit(1);
    }
    await exchangeCode(value);
    break;
  case "--status":
    await checkStatus();
    break;
  default:
    console.log(`
Reddit Auth Script — Usage:

  node scripts/reddit-auth.mjs --url              Generate authorization URL
  node scripts/reddit-auth.mjs --exchange <CODE>  Exchange code for tokens
  node scripts/reddit-auth.mjs --status           Check connection status
`);
}