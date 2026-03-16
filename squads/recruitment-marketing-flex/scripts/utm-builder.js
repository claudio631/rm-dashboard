/**
 * UTM Builder — Recruitment Marketing Flex
 *
 * Generates consistent UTM parameters following Indeed Flex naming conventions.
 * Ensures all campaign links use standardized tracking taxonomy.
 *
 * Naming Convention:
 *   utm_source   = channel (indeed, google, meta, bing, reddit, craigslist)
 *   utm_medium   = type (cpc, cpm, social, email, organic, referral)
 *   utm_campaign = {channel}-{market}-{category}-{objective}-{date}
 *   utm_content  = variant identifier (ad copy, creative, placement)
 *   utm_term     = keyword (search campaigns only)
 *
 * @module utm-builder
 * @squad recruitment-marketing-flex
 */

const VALID_SOURCES = [
  'indeed', 'google', 'meta', 'bing', 'reddit',
  'craigslist', 'linkedin', 'appcast', 'joveo', 'pandologic',
  'email', 'sms', 'direct'
];

const VALID_MEDIUMS = [
  'cpc', 'cpm', 'social', 'email', 'sms', 'organic',
  'referral', 'display', 'video', 'native', 'programmatic'
];

const VALID_OBJECTIVES = [
  'acquisition', 'awareness', 'retargeting', 'retention', 'referral', 'branding'
];

/**
 * Build a UTM parameter string from structured inputs.
 *
 * @param {Object} params
 * @param {string} params.source - Traffic source (channel name)
 * @param {string} params.medium - Marketing medium type
 * @param {string} params.market - Geographic market (city or metro code)
 * @param {string} params.category - Job category (warehouse, delivery, etc.)
 * @param {string} params.objective - Campaign objective
 * @param {string} params.date - Campaign date identifier (e.g., 2026q1, 202603)
 * @param {string} [params.content] - Ad variant identifier
 * @param {string} [params.term] - Keyword (search campaigns)
 * @returns {string} Formatted UTM query string
 */
function buildUTM(params) {
  const { source, medium, market, category, objective, date, content, term } = params;

  // Validate required fields
  if (!source || !medium || !market || !category || !objective || !date) {
    throw new Error('Missing required UTM fields: source, medium, market, category, objective, date');
  }

  // Normalize to lowercase kebab-case
  const normalize = (str) => str.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');

  const normalizedSource = normalize(source);
  const normalizedMedium = normalize(medium);

  // Validate source
  if (!VALID_SOURCES.includes(normalizedSource)) {
    console.warn(`Warning: "${normalizedSource}" is not a standard source. Valid: ${VALID_SOURCES.join(', ')}`);
  }

  // Validate medium
  if (!VALID_MEDIUMS.includes(normalizedMedium)) {
    console.warn(`Warning: "${normalizedMedium}" is not a standard medium. Valid: ${VALID_MEDIUMS.join(', ')}`);
  }

  // Build campaign name
  const campaignName = [normalizedSource, normalize(market), normalize(category), normalize(objective), normalize(date)].join('-');

  // Build UTM object
  const utm = {
    utm_source: normalizedSource,
    utm_medium: normalizedMedium,
    utm_campaign: campaignName,
  };

  if (content) utm.utm_content = normalize(content);
  if (term) utm.utm_term = normalize(term);

  // Convert to query string
  const queryString = Object.entries(utm)
    .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
    .join('&');

  return queryString;
}

/**
 * Build a full URL with UTM parameters.
 *
 * @param {string} baseUrl - The landing page URL
 * @param {Object} params - UTM parameters (same as buildUTM)
 * @returns {string} Full URL with UTM parameters
 */
function buildTrackedURL(baseUrl, params) {
  const utmString = buildUTM(params);
  const separator = baseUrl.includes('?') ? '&' : '?';
  return `${baseUrl}${separator}${utmString}`;
}

/**
 * Generate UTMs for multiple ad variants in a campaign.
 *
 * @param {Object} baseParams - Base UTM parameters (without content)
 * @param {string[]} variants - Array of variant names
 * @returns {Object[]} Array of { variant, utm, url } objects
 */
function buildVariantUTMs(baseParams, variants, baseUrl) {
  return variants.map((variant) => ({
    variant,
    utm: buildUTM({ ...baseParams, content: variant }),
    url: baseUrl ? buildTrackedURL(baseUrl, { ...baseParams, content: variant }) : null,
  }));
}

/**
 * Parse an existing UTM string back into structured parameters.
 *
 * @param {string} utmString - UTM query string or full URL
 * @returns {Object} Parsed UTM parameters
 */
function parseUTM(utmString) {
  const queryPart = utmString.includes('?') ? utmString.split('?')[1] : utmString;
  const params = new URLSearchParams(queryPart);
  const result = {};
  for (const [key, value] of params) {
    if (key.startsWith('utm_')) {
      result[key] = decodeURIComponent(value);
    }
  }
  return result;
}

module.exports = {
  buildUTM,
  buildTrackedURL,
  buildVariantUTMs,
  parseUTM,
  VALID_SOURCES,
  VALID_MEDIUMS,
  VALID_OBJECTIVES,
};
