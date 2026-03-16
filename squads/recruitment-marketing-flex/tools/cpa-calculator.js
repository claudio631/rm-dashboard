/**
 * CPA Calculator — Recruitment Marketing Flex
 *
 * Calculate cost-per-apply (CPA) and cost-per-hire (CPH) across channels.
 * Supports full-funnel cost analysis from impression to hire.
 *
 * @module cpa-calculator
 * @squad recruitment-marketing-flex
 */

/**
 * Calculate cost-per-apply for a campaign or channel.
 *
 * @param {number} spend - Total spend
 * @param {number} applications - Total applications
 * @returns {number} Cost per application
 */
function costPerApply(spend, applications) {
  if (applications <= 0) return Infinity;
  return round(spend / applications);
}

/**
 * Calculate cost-per-hire across the full funnel.
 *
 * @param {number} spend - Total marketing spend
 * @param {number} hires - Total hires attributed to marketing
 * @returns {number} Cost per hire
 */
function costPerHire(spend, hires) {
  if (hires <= 0) return Infinity;
  return round(spend / hires);
}

/**
 * Full funnel cost analysis.
 *
 * @param {Object} data
 * @param {number} data.spend - Total spend
 * @param {number} data.impressions - Total impressions
 * @param {number} data.clicks - Total clicks
 * @param {number} data.applications - Total applications
 * @param {number} data.screens - Candidates passing initial screen
 * @param {number} data.interviews - Candidates interviewed
 * @param {number} data.hires - Total hires
 * @returns {Object} Full funnel cost and conversion metrics
 */
function fullFunnelAnalysis(data) {
  const { spend, impressions, clicks, applications, screens, interviews, hires } = data;

  return {
    costs: {
      cpm: impressions > 0 ? round((spend / impressions) * 1000) : null,
      cpc: clicks > 0 ? round(spend / clicks) : null,
      cpa: applications > 0 ? round(spend / applications) : null,
      costPerScreen: screens > 0 ? round(spend / screens) : null,
      costPerInterview: interviews > 0 ? round(spend / interviews) : null,
      costPerHire: hires > 0 ? round(spend / hires) : null,
    },
    conversions: {
      ctr: impressions > 0 ? round((clicks / impressions) * 100) : null,
      applyRate: clicks > 0 ? round((applications / clicks) * 100) : null,
      screenRate: applications > 0 ? round((screens / applications) * 100) : null,
      interviewRate: screens > 0 ? round((interviews / screens) * 100) : null,
      hireRate: interviews > 0 ? round((hires / interviews) * 100) : null,
      overallConversion: impressions > 0 ? round((hires / impressions) * 100) : null,
    },
    funnel: [
      { stage: 'Impressions', count: impressions, dropoff: null },
      { stage: 'Clicks', count: clicks, dropoff: impressions > 0 ? round(((impressions - clicks) / impressions) * 100) : null },
      { stage: 'Applications', count: applications, dropoff: clicks > 0 ? round(((clicks - applications) / clicks) * 100) : null },
      { stage: 'Screens', count: screens, dropoff: applications > 0 ? round(((applications - screens) / applications) * 100) : null },
      { stage: 'Interviews', count: interviews, dropoff: screens > 0 ? round(((screens - interviews) / screens) * 100) : null },
      { stage: 'Hires', count: hires, dropoff: interviews > 0 ? round(((interviews - hires) / interviews) * 100) : null },
    ],
    spend,
  };
}

/**
 * Compare CPA/CPH across multiple channels.
 *
 * @param {Object[]} channels - Array of { name, spend, applications, hires }
 * @returns {Object} Comparison with rankings
 */
function compareChannels(channels) {
  const analyzed = channels.map((ch) => ({
    name: ch.name,
    spend: ch.spend,
    applications: ch.applications,
    hires: ch.hires || 0,
    cpa: costPerApply(ch.spend, ch.applications),
    cph: ch.hires ? costPerHire(ch.spend, ch.hires) : null,
    applyRate: ch.clicks ? round((ch.applications / ch.clicks) * 100) : null,
    spendShare: null, // calculated below
  }));

  const totalSpend = analyzed.reduce((sum, ch) => sum + ch.spend, 0);
  analyzed.forEach((ch) => {
    ch.spendShare = round((ch.spend / totalSpend) * 100);
  });

  // Rank by CPA (lowest = best)
  const rankedByCPA = [...analyzed].sort((a, b) => a.cpa - b.cpa);

  return {
    channels: analyzed,
    rankedByCPA,
    bestCPA: rankedByCPA[0],
    worstCPA: rankedByCPA[rankedByCPA.length - 1],
    totalSpend,
    totalApplications: analyzed.reduce((sum, ch) => sum + ch.applications, 0),
    totalHires: analyzed.reduce((sum, ch) => sum + ch.hires, 0),
    blendedCPA: costPerApply(totalSpend, analyzed.reduce((sum, ch) => sum + ch.applications, 0)),
    blendedCPH: costPerHire(totalSpend, analyzed.reduce((sum, ch) => sum + ch.hires, 0)),
  };
}

function round(num) {
  return Math.round(num * 100) / 100;
}

module.exports = {
  costPerApply,
  costPerHire,
  fullFunnelAnalysis,
  compareChannels,
};
