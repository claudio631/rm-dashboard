/**
 * Report Aggregator — Recruitment Marketing Flex
 *
 * Merges campaign data from multiple channel exports into a unified view.
 * Supports Indeed, Google Ads, Meta, Bing, Reddit, and Craigslist data formats.
 *
 * @module report-aggregator
 * @squad recruitment-marketing-flex
 */

/**
 * Normalize channel-specific data into a unified format.
 *
 * @param {string} channel - Channel name
 * @param {Object[]} rawData - Raw data rows from channel export
 * @returns {Object[]} Normalized rows
 */
function normalizeChannelData(channel, rawData) {
  const normalizers = {
    indeed: normalizeIndeed,
    google: normalizeGoogle,
    meta: normalizeMeta,
    bing: normalizeBing,
    reddit: normalizeReddit,
    craigslist: normalizeCraigslist,
  };

  const normalizer = normalizers[channel.toLowerCase()];
  if (!normalizer) {
    throw new Error(`Unknown channel: ${channel}. Supported: ${Object.keys(normalizers).join(', ')}`);
  }

  return rawData.map((row) => ({
    ...normalizer(row),
    channel: channel.toLowerCase(),
    normalizedAt: new Date().toISOString(),
  }));
}

function normalizeIndeed(row) {
  return {
    date: row.date || row.Date,
    campaign: row.campaign_name || row['Campaign Name'] || 'Sponsored Jobs',
    impressions: toNum(row.impressions || row.Impressions),
    clicks: toNum(row.clicks || row.Clicks),
    spend: toNum(row.spend || row.Spend || row.cost),
    applications: toNum(row.applies || row.Applications || row.conversions),
    cpc: toNum(row.cpc || row.CPC),
    ctr: toNum(row.ctr || row.CTR),
    cpa: null, // calculated
  };
}

function normalizeGoogle(row) {
  return {
    date: row.Day || row.date || row.Date,
    campaign: row.Campaign || row.campaign,
    impressions: toNum(row.Impressions || row.impressions || row.Impr),
    clicks: toNum(row.Clicks || row.clicks),
    spend: toNum(row.Cost || row.cost || row.spend),
    applications: toNum(row.Conversions || row.conversions || row.Conv),
    cpc: toNum(row['Avg. CPC'] || row.avg_cpc || row.cpc),
    ctr: toNum(row.CTR || row.ctr),
    cpa: null,
  };
}

function normalizeMeta(row) {
  return {
    date: row['Reporting starts'] || row.date_start || row.date,
    campaign: row['Campaign name'] || row.campaign_name,
    impressions: toNum(row.Impressions || row.impressions),
    clicks: toNum(row['Link clicks'] || row.clicks || row.inline_link_clicks),
    spend: toNum(row['Amount spent (USD)'] || row.spend),
    applications: toNum(row.Results || row.leads || row.conversions || row.actions),
    cpc: toNum(row['Cost per result'] || row.cpc),
    ctr: toNum(row['CTR (link click-through rate)'] || row.ctr),
    cpa: null,
  };
}

function normalizeBing(row) {
  return {
    date: row.TimePeriod || row.date || row.Date,
    campaign: row.CampaignName || row.Campaign || row.campaign,
    impressions: toNum(row.Impressions || row.impressions),
    clicks: toNum(row.Clicks || row.clicks),
    spend: toNum(row.Spend || row.spend || row.Cost),
    applications: toNum(row.Conversions || row.conversions),
    cpc: toNum(row.AverageCpc || row.cpc),
    ctr: toNum(row.Ctr || row.ctr),
    cpa: null,
  };
}

function normalizeReddit(row) {
  return {
    date: row.date || row.Date,
    campaign: row.campaign_name || row.Campaign,
    impressions: toNum(row.impressions || row.Impressions),
    clicks: toNum(row.clicks || row.Clicks),
    spend: toNum(row.spend || row.Spend),
    applications: toNum(row.conversions || row.Conversions),
    cpc: toNum(row.ecpc || row.cpc),
    ctr: toNum(row.ctr || row.CTR),
    cpa: null,
  };
}

function normalizeCraigslist(row) {
  return {
    date: row.date || row.Date || row.posted_date,
    campaign: row.title || row.posting_title || 'Job Posting',
    impressions: toNum(row.views || row.Views || 0),
    clicks: toNum(row.clicks || row.Clicks || row.replies || 0),
    spend: toNum(row.cost || row.Cost || row.fee || 0),
    applications: toNum(row.applies || row.Applications || row.responses || 0),
    cpc: null,
    ctr: null,
    cpa: null,
  };
}

/**
 * Aggregate normalized data into summary metrics.
 *
 * @param {Object[]} normalizedData - Array of normalized rows
 * @returns {Object} Aggregated metrics
 */
function aggregate(normalizedData) {
  const totals = normalizedData.reduce(
    (acc, row) => ({
      impressions: acc.impressions + (row.impressions || 0),
      clicks: acc.clicks + (row.clicks || 0),
      spend: acc.spend + (row.spend || 0),
      applications: acc.applications + (row.applications || 0),
    }),
    { impressions: 0, clicks: 0, spend: 0, applications: 0 }
  );

  return {
    ...totals,
    spend: round(totals.spend),
    ctr: totals.impressions > 0 ? round((totals.clicks / totals.impressions) * 100) : 0,
    cpc: totals.clicks > 0 ? round(totals.spend / totals.clicks) : 0,
    cpa: totals.applications > 0 ? round(totals.spend / totals.applications) : 0,
    applyRate: totals.clicks > 0 ? round((totals.applications / totals.clicks) * 100) : 0,
    rows: normalizedData.length,
  };
}

/**
 * Aggregate by channel for cross-channel comparison.
 *
 * @param {Object[]} normalizedData
 * @returns {Object} Metrics grouped by channel
 */
function aggregateByChannel(normalizedData) {
  const grouped = {};
  for (const row of normalizedData) {
    if (!grouped[row.channel]) grouped[row.channel] = [];
    grouped[row.channel].push(row);
  }

  const result = {};
  for (const [channel, rows] of Object.entries(grouped)) {
    result[channel] = aggregate(rows);
  }

  result._total = aggregate(normalizedData);
  return result;
}

function toNum(val) {
  if (val === null || val === undefined || val === '') return 0;
  const cleaned = String(val).replace(/[,$%]/g, '');
  const num = parseFloat(cleaned);
  return isNaN(num) ? 0 : num;
}

function round(num) {
  return Math.round(num * 100) / 100;
}

module.exports = {
  normalizeChannelData,
  aggregate,
  aggregateByChannel,
};
