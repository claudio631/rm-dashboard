/**
 * Channel Comparator — Recruitment Marketing Flex
 *
 * Compare performance metrics across advertising channels side-by-side.
 * Generates formatted comparison tables and recommendations.
 *
 * @module channel-comparator
 * @squad recruitment-marketing-flex
 */

/**
 * Compare channels side-by-side on key metrics.
 *
 * @param {Object[]} channels - Array of channel data objects
 * @param {string} channels[].name - Channel name
 * @param {number} channels[].spend - Total spend
 * @param {number} channels[].impressions - Total impressions
 * @param {number} channels[].clicks - Total clicks
 * @param {number} channels[].applications - Total applications
 * @param {number} [channels[].hires] - Total hires
 * @returns {Object} Comparison result with rankings and recommendations
 */
function compare(channels) {
  const analyzed = channels.map((ch) => {
    const ctr = ch.impressions > 0 ? round((ch.clicks / ch.impressions) * 100) : 0;
    const cpc = ch.clicks > 0 ? round(ch.spend / ch.clicks) : 0;
    const cpa = ch.applications > 0 ? round(ch.spend / ch.applications) : Infinity;
    const cph = ch.hires > 0 ? round(ch.spend / ch.hires) : null;
    const applyRate = ch.clicks > 0 ? round((ch.applications / ch.clicks) * 100) : 0;
    const hireRate = ch.applications > 0 && ch.hires ? round((ch.hires / ch.applications) * 100) : null;

    return {
      name: ch.name,
      spend: ch.spend,
      impressions: ch.impressions,
      clicks: ch.clicks,
      applications: ch.applications,
      hires: ch.hires || 0,
      ctr,
      cpc,
      cpa,
      cph,
      applyRate,
      hireRate,
    };
  });

  // Rankings (1 = best)
  const rankings = {};
  const metrics = ['cpa', 'cpc', 'cph']; // lower is better
  const metricsHigherBetter = ['ctr', 'applyRate', 'hireRate']; // higher is better

  for (const metric of metrics) {
    const sorted = [...analyzed].filter((ch) => ch[metric] !== null && ch[metric] !== Infinity).sort((a, b) => a[metric] - b[metric]);
    rankings[metric] = sorted.map((ch, i) => ({ name: ch.name, rank: i + 1, value: ch[metric] }));
  }

  for (const metric of metricsHigherBetter) {
    const sorted = [...analyzed].filter((ch) => ch[metric] !== null).sort((a, b) => b[metric] - a[metric]);
    rankings[metric] = sorted.map((ch, i) => ({ name: ch.name, rank: i + 1, value: ch[metric] }));
  }

  // Efficiency score (composite)
  const efficiencyScores = analyzed.map((ch) => {
    let score = 0;
    for (const metric of metrics) {
      const rank = rankings[metric]?.find((r) => r.name === ch.name);
      if (rank) score += rank.rank;
    }
    for (const metric of metricsHigherBetter) {
      const rank = rankings[metric]?.find((r) => r.name === ch.name);
      if (rank) score += rank.rank;
    }
    return { name: ch.name, score, avgRank: round(score / 6) };
  }).sort((a, b) => a.score - b.score);

  // Budget recommendations
  const recommendations = generateRecommendations(analyzed, efficiencyScores);

  return {
    channels: analyzed,
    rankings,
    efficiencyScores,
    recommendations,
    totals: {
      spend: round(analyzed.reduce((s, ch) => s + ch.spend, 0)),
      impressions: analyzed.reduce((s, ch) => s + ch.impressions, 0),
      clicks: analyzed.reduce((s, ch) => s + ch.clicks, 0),
      applications: analyzed.reduce((s, ch) => s + ch.applications, 0),
      hires: analyzed.reduce((s, ch) => s + ch.hires, 0),
    },
  };
}

/**
 * Generate markdown comparison table.
 *
 * @param {Object} comparisonResult - Output from compare()
 * @returns {string} Markdown table
 */
function toMarkdownTable(comparisonResult) {
  const { channels } = comparisonResult;
  const headers = ['Channel', 'Spend', 'Clicks', 'Apps', 'Hires', 'CTR', 'CPC', 'CPA', 'CPH', 'Apply Rate'];
  const separator = headers.map(() => '---').join(' | ');
  const headerRow = headers.join(' | ');

  const rows = channels.map((ch) =>
    [
      ch.name,
      `$${ch.spend.toLocaleString()}`,
      ch.clicks.toLocaleString(),
      ch.applications.toLocaleString(),
      ch.hires.toLocaleString(),
      `${ch.ctr}%`,
      `$${ch.cpc}`,
      ch.cpa === Infinity ? 'N/A' : `$${ch.cpa}`,
      ch.cph ? `$${ch.cph}` : 'N/A',
      `${ch.applyRate}%`,
    ].join(' | ')
  );

  return `| ${headerRow} |\n| ${separator} |\n${rows.map((r) => `| ${r} |`).join('\n')}`;
}

function generateRecommendations(channels, efficiencyScores) {
  const recs = [];
  const best = efficiencyScores[0];
  const worst = efficiencyScores[efficiencyScores.length - 1];

  if (best) {
    recs.push({
      type: 'increase',
      channel: best.name,
      message: `${best.name} is the most efficient channel. Consider increasing budget allocation.`,
    });
  }

  if (worst && worst.name !== best?.name) {
    recs.push({
      type: 'decrease',
      channel: worst.name,
      message: `${worst.name} is the least efficient channel. Review performance or reduce budget.`,
    });
  }

  // Find channels with high CPA
  for (const ch of channels) {
    if (ch.cpa > 100 && ch.cpa !== Infinity) {
      recs.push({
        type: 'optimize',
        channel: ch.name,
        message: `${ch.name} CPA ($${ch.cpa}) is high. Optimize targeting, creatives, or bid strategy.`,
      });
    }
  }

  return recs;
}

function round(num) {
  return Math.round(num * 100) / 100;
}

module.exports = {
  compare,
  toMarkdownTable,
};
