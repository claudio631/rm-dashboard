/**
 * Cost-per-Hire Calculator — Recruitment Marketing Flex
 *
 * Calculate cost-per-hire (CPH) across the full Indeed Flex funnel.
 * The funnel maps to the actual worker journey:
 *   Indeed Ad → Click → Apply Start → RSVP → Account Created → Verified →
 *   Platform Verified → Shift Booked → Shift Completed (= Hire)
 *
 * @module cpa-calculator
 * @squad recruitment-marketing-flex
 */

/**
 * Calculate cost-per-hire.
 *
 * A "hire" in Indeed Flex = a worker who completes their first shift.
 *
 * @param {number} spend - Total marketing spend
 * @param {number} hires - Workers who completed first shift
 * @returns {number} Cost per hire
 */
function costPerHire(spend, hires) {
  if (hires <= 0) return Infinity;
  return round(spend / hires);
}

/**
 * Calculate cost at each funnel stage.
 *
 * @param {number} spend - Total spend
 * @param {number} count - Count at that stage
 * @returns {number|null} Cost per unit at that stage
 */
function costPerStage(spend, count) {
  if (!count || count <= 0) return null;
  return round(spend / count);
}

/**
 * Full Indeed Flex funnel cost analysis.
 *
 * Stages:
 *   1. Impressions (Indeed ad shown)
 *   2. Clicks (worker clicks ad)
 *   3. Apply Starts (worker begins application)
 *   4. RSVPs (worker RSVPs for AI interview in FHS)
 *   5. Accounts Created (worker creates account in Tableau OB funnel)
 *   6. Role Verified (worker completes AI interview + verification)
 *   7. Platform Verified (worker fully verified on platform)
 *   8. Shift Booked (worker books first shift)
 *   9. Shift Completed (worker completes first shift = HIRE)
 *
 * @param {Object} data
 * @param {number} data.spend - Total Indeed spend
 * @param {number} data.impressions - Ad impressions
 * @param {number} data.clicks - Ad clicks
 * @param {number} data.applyStarts - Workers who started application
 * @param {number} data.rsvps - Workers who RSVP'd (FHS)
 * @param {number} data.accountsCreated - Accounts created (Tableau)
 * @param {number} data.roleVerified - 1st Role Verified (Tableau)
 * @param {number} data.platformVerified - Platform Verified (Tableau)
 * @param {number} data.shiftBooked - 1st Shift Booked (Tableau)
 * @param {number} data.shiftCompleted - 1st Shift Completed = HIRE (Tableau)
 * @returns {Object} Full funnel cost and conversion metrics
 */
function fullFunnelAnalysis(data) {
  const {
    spend, impressions, clicks, applyStarts, rsvps,
    accountsCreated, roleVerified, platformVerified,
    shiftBooked, shiftCompleted,
  } = data;

  const stages = [
    { stage: 'Impressions', count: impressions, source: 'Indeed' },
    { stage: 'Clicks', count: clicks, source: 'Indeed' },
    { stage: 'Apply Starts', count: applyStarts, source: 'Indeed' },
    { stage: 'RSVPs', count: rsvps, source: 'FHS' },
    { stage: 'Accounts Created', count: accountsCreated, source: 'Tableau' },
    { stage: 'Role Verified', count: roleVerified, source: 'Tableau' },
    { stage: 'Platform Verified', count: platformVerified, source: 'Tableau' },
    { stage: 'Shift Booked', count: shiftBooked, source: 'Tableau' },
    { stage: 'Shift Completed (Hire)', count: shiftCompleted, source: 'Tableau' },
  ];

  // Add cost-per and conversion rates
  for (let i = 0; i < stages.length; i++) {
    const s = stages[i];
    s.costPer = costPerStage(spend, s.count);
    s.stageConversion = i > 0 && stages[i - 1].count > 0
      ? round((s.count / stages[i - 1].count) * 100)
      : null;
    s.cumulativeConversion = impressions > 0 && s.count > 0
      ? round((s.count / impressions) * 100)
      : null;
    s.dropoff = i > 0 && stages[i - 1].count > 0
      ? stages[i - 1].count - s.count
      : null;
  }

  return {
    costs: {
      cpm: costPerStage(spend * 1000, impressions),
      cpc: costPerStage(spend, clicks),
      costPerApplyStart: costPerStage(spend, applyStarts),
      costPerRSVP: costPerStage(spend, rsvps),
      costPerAccountCreated: costPerStage(spend, accountsCreated),
      costPerVerified: costPerStage(spend, roleVerified),
      costPerPlatformVerified: costPerStage(spend, platformVerified),
      costPerShiftBooked: costPerStage(spend, shiftBooked),
      costPerHire: costPerStage(spend, shiftCompleted),
    },
    conversions: {
      ctr: impressions > 0 ? round((clicks / impressions) * 100) : null,
      applyStartRate: clicks > 0 ? round((applyStarts / clicks) * 100) : null,
      applyToRSVP: applyStarts > 0 ? round((rsvps / applyStarts) * 100) : null,
      accountCreatedRate: rsvps > 0 ? round((accountsCreated / rsvps) * 100) : null,
      verificationRate: accountsCreated > 0 ? round((roleVerified / accountsCreated) * 100) : null,
      platformVerifiedRate: roleVerified > 0 ? round((platformVerified / roleVerified) * 100) : null,
      bookingRate: platformVerified > 0 ? round((shiftBooked / platformVerified) * 100) : null,
      completionRate: shiftBooked > 0 ? round((shiftCompleted / shiftBooked) * 100) : null,
      endToEnd: impressions > 0 ? round((shiftCompleted / impressions) * 100) : null,
    },
    funnel: stages,
    spend,
    hires: shiftCompleted,
    costPerHire: costPerStage(spend, shiftCompleted),
  };
}

/**
 * Compare cost-per-hire across clients or locations.
 *
 * @param {Object[]} entries - Array of { name, spend, rsvps, accountsCreated, roleVerified, shiftBooked, shiftCompleted }
 * @returns {Object} Comparison with rankings by cost-per-hire
 */
function compareByLocation(entries) {
  const analyzed = entries.map((e) => ({
    name: e.name,
    spend: e.spend,
    rsvps: e.rsvps || 0,
    accountsCreated: e.accountsCreated || 0,
    roleVerified: e.roleVerified || 0,
    shiftBooked: e.shiftBooked || 0,
    hires: e.shiftCompleted || 0,
    costPerRSVP: costPerStage(e.spend, e.rsvps),
    costPerVerified: costPerStage(e.spend, e.roleVerified),
    costPerHire: costPerStage(e.spend, e.shiftCompleted),
    spendShare: null,
  }));

  const totalSpend = analyzed.reduce((sum, e) => sum + e.spend, 0);
  analyzed.forEach((e) => {
    e.spendShare = totalSpend > 0 ? round((e.spend / totalSpend) * 100) : 0;
  });

  // Rank by cost-per-hire (lowest = best, Infinity = worst)
  const rankedByCPH = [...analyzed]
    .filter((e) => e.hires > 0)
    .sort((a, b) => a.costPerHire - b.costPerHire);

  const totalHires = analyzed.reduce((sum, e) => sum + e.hires, 0);

  return {
    locations: analyzed,
    rankedByCostPerHire: rankedByCPH,
    bestCPH: rankedByCPH[0] || null,
    worstCPH: rankedByCPH[rankedByCPH.length - 1] || null,
    totalSpend,
    totalHires,
    blendedCPH: costPerHire(totalSpend, totalHires),
  };
}

function round(num) {
  return Math.round(num * 100) / 100;
}

module.exports = {
  costPerHire,
  costPerStage,
  fullFunnelAnalysis,
  compareByLocation,
};
