/**
 * Budget Pacer — Recruitment Marketing Flex
 *
 * Calculates daily budget pacing and alerts on over/underspend.
 * Helps ensure Indeed Flex campaigns spend evenly across the period.
 *
 * @module budget-pacer
 * @squad recruitment-marketing-flex
 */

/**
 * Calculate pacing status for a campaign or channel.
 *
 * @param {Object} params
 * @param {number} params.totalBudget - Total budget for the period
 * @param {number} params.spent - Amount spent so far
 * @param {number} params.daysElapsed - Days elapsed in the period
 * @param {number} params.totalDays - Total days in the period
 * @returns {Object} Pacing analysis
 */
function calculatePacing(params) {
  const { totalBudget, spent, daysElapsed, totalDays } = params;

  if (totalDays <= 0 || totalBudget <= 0) {
    throw new Error('totalDays and totalBudget must be positive');
  }

  const dailyBudget = totalBudget / totalDays;
  const expectedSpend = dailyBudget * daysElapsed;
  const remaining = totalBudget - spent;
  const daysRemaining = totalDays - daysElapsed;
  const requiredDailySpend = daysRemaining > 0 ? remaining / daysRemaining : 0;
  const pacingRatio = expectedSpend > 0 ? spent / expectedSpend : 0;
  const utilizationRate = (spent / totalBudget) * 100;

  // Determine status
  let status;
  let severity;
  if (pacingRatio >= 0.9 && pacingRatio <= 1.1) {
    status = 'ON_PACE';
    severity = 'ok';
  } else if (pacingRatio > 1.1 && pacingRatio <= 1.25) {
    status = 'SLIGHTLY_OVER';
    severity = 'warning';
  } else if (pacingRatio > 1.25) {
    status = 'OVERSPENDING';
    severity = 'critical';
  } else if (pacingRatio >= 0.75 && pacingRatio < 0.9) {
    status = 'SLIGHTLY_UNDER';
    severity = 'warning';
  } else {
    status = 'UNDERSPENDING';
    severity = 'critical';
  }

  return {
    totalBudget,
    spent,
    remaining,
    dailyBudget: round(dailyBudget),
    expectedSpend: round(expectedSpend),
    variance: round(spent - expectedSpend),
    variancePercent: round(((spent - expectedSpend) / expectedSpend) * 100),
    pacingRatio: round(pacingRatio),
    utilizationRate: round(utilizationRate),
    requiredDailySpend: round(requiredDailySpend),
    daysElapsed,
    daysRemaining,
    totalDays,
    status,
    severity,
    recommendation: getRecommendation(status, requiredDailySpend, dailyBudget),
  };
}

/**
 * Calculate pacing across multiple channels.
 *
 * @param {Object[]} channels - Array of { name, totalBudget, spent }
 * @param {number} daysElapsed
 * @param {number} totalDays
 * @returns {Object} Multi-channel pacing report
 */
function calculateMultiChannelPacing(channels, daysElapsed, totalDays) {
  const results = channels.map((ch) => ({
    name: ch.name,
    ...calculatePacing({
      totalBudget: ch.totalBudget,
      spent: ch.spent,
      daysElapsed,
      totalDays,
    }),
  }));

  const totalBudget = channels.reduce((sum, ch) => sum + ch.totalBudget, 0);
  const totalSpent = channels.reduce((sum, ch) => sum + ch.spent, 0);

  return {
    channels: results,
    summary: calculatePacing({
      totalBudget,
      spent: totalSpent,
      daysElapsed,
      totalDays,
    }),
    alerts: results.filter((r) => r.severity === 'critical'),
    warnings: results.filter((r) => r.severity === 'warning'),
  };
}

/**
 * Generate a pacing recommendation based on status.
 */
function getRecommendation(status, requiredDailySpend, dailyBudget) {
  const recommendations = {
    ON_PACE: 'Budget is pacing well. No action needed.',
    SLIGHTLY_OVER: `Slightly overspending. Consider reducing daily spend to $${requiredDailySpend} (from $${dailyBudget}).`,
    OVERSPENDING: `Significantly overspending. Reduce daily budget to $${requiredDailySpend} immediately or pause low-performing campaigns.`,
    SLIGHTLY_UNDER: `Slightly underspending. Increase daily spend to $${requiredDailySpend} or expand targeting.`,
    UNDERSPENDING: `Significantly underspending. Increase budget to $${requiredDailySpend}/day, add new keywords/audiences, or reallocate to higher-performing channels.`,
  };
  return recommendations[status] || 'Review campaign pacing manually.';
}

function round(num) {
  return Math.round(num * 100) / 100;
}

module.exports = {
  calculatePacing,
  calculateMultiChannelPacing,
};
