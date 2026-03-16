/**
 * Keyword Expander — Recruitment Marketing Flex
 *
 * Expands seed keywords into location + job type combinations
 * for Indeed Flex recruitment campaigns.
 *
 * @module keyword-expander
 * @squad recruitment-marketing-flex
 */

/**
 * Default job category seed keywords for Indeed Flex.
 */
const DEFAULT_JOB_SEEDS = {
  warehouse: ['warehouse jobs', 'warehouse worker', 'picker packer', 'forklift operator', 'warehouse associate'],
  delivery: ['delivery driver', 'delivery jobs', 'courier jobs', 'driver jobs', 'last mile delivery'],
  retail: ['retail jobs', 'cashier jobs', 'retail associate', 'store associate', 'sales associate'],
  hospitality: ['hotel jobs', 'housekeeping jobs', 'front desk jobs', 'hospitality jobs', 'banquet server'],
  food_service: ['restaurant jobs', 'line cook jobs', 'dishwasher jobs', 'food prep jobs', 'server jobs'],
  general_labor: ['general labor jobs', 'temp jobs', 'day labor', 'manual labor jobs', 'labor jobs'],
  event_staffing: ['event staff jobs', 'event jobs', 'event setup jobs', 'catering jobs', 'convention staff'],
  cleaning: ['cleaning jobs', 'janitor jobs', 'janitorial jobs', 'office cleaning', 'commercial cleaning'],
};

/**
 * Common location modifiers.
 */
const LOCATION_MODIFIERS = ['near me', 'hiring now', 'immediate start', 'no experience', 'weekly pay', 'flexible hours', 'temp', 'part time'];

/**
 * Common shift modifiers.
 */
const SHIFT_MODIFIERS = ['night shift', 'day shift', 'weekend', 'overnight', 'morning shift', 'evening shift'];

/**
 * Expand seed keywords with locations and modifiers.
 *
 * @param {Object} params
 * @param {string[]} params.seeds - Base seed keywords
 * @param {string[]} params.locations - Target locations (cities, states)
 * @param {boolean} [params.includeModifiers=true] - Add common modifiers
 * @param {boolean} [params.includeShifts=false] - Add shift modifiers
 * @param {string} [params.brand='indeed flex'] - Brand name to include
 * @returns {Object} Expanded keyword lists
 */
function expandKeywords(params) {
  const {
    seeds,
    locations,
    includeModifiers = true,
    includeShifts = false,
    brand = 'indeed flex',
  } = params;

  const expanded = {
    exact: [],
    phrase: [],
    broad: [],
    negative_suggestions: [],
  };

  for (const seed of seeds) {
    // Base keyword
    expanded.phrase.push(seed);

    // Location combinations
    for (const location of locations) {
      expanded.phrase.push(`${seed} ${location}`);
      expanded.phrase.push(`${seed} in ${location}`);
      expanded.exact.push(`${seed} ${location}`);
    }

    // Modifier combinations
    if (includeModifiers) {
      for (const mod of LOCATION_MODIFIERS) {
        expanded.broad.push(`${seed} ${mod}`);
      }
    }

    // Shift combinations
    if (includeShifts) {
      for (const shift of SHIFT_MODIFIERS) {
        expanded.broad.push(`${seed} ${shift}`);
      }
    }

    // Brand combinations
    if (brand) {
      expanded.phrase.push(`${brand} ${seed}`);
    }
  }

  // Deduplicate
  expanded.exact = [...new Set(expanded.exact)];
  expanded.phrase = [...new Set(expanded.phrase)];
  expanded.broad = [...new Set(expanded.broad)];

  // Suggest negatives
  expanded.negative_suggestions = generateNegativeSuggestions(seeds);

  return {
    ...expanded,
    stats: {
      exact: expanded.exact.length,
      phrase: expanded.phrase.length,
      broad: expanded.broad.length,
      total: expanded.exact.length + expanded.phrase.length + expanded.broad.length,
    },
  };
}

/**
 * Expand keywords for a specific job category using built-in seeds.
 *
 * @param {string} category - Job category key from DEFAULT_JOB_SEEDS
 * @param {string[]} locations - Target locations
 * @param {Object} [options] - Additional options
 * @returns {Object} Expanded keywords
 */
function expandByCategory(category, locations, options = {}) {
  const seeds = DEFAULT_JOB_SEEDS[category];
  if (!seeds) {
    throw new Error(`Unknown category: ${category}. Available: ${Object.keys(DEFAULT_JOB_SEEDS).join(', ')}`);
  }
  return expandKeywords({ seeds, locations, ...options });
}

/**
 * Generate common negative keyword suggestions for recruitment.
 */
function generateNegativeSuggestions(seeds) {
  const commonNegatives = [
    'salary', 'full time permanent', 'remote only', 'work from home',
    'internship', 'volunteer', 'unpaid', 'free', 'training program',
    'career advice', 'resume', 'interview tips', 'how to',
    'jobs abroad', 'overseas', 'visa sponsorship',
  ];
  return commonNegatives;
}

/**
 * Get all available job categories.
 *
 * @returns {string[]} Category names
 */
function getCategories() {
  return Object.keys(DEFAULT_JOB_SEEDS);
}

module.exports = {
  expandKeywords,
  expandByCategory,
  getCategories,
  DEFAULT_JOB_SEEDS,
  LOCATION_MODIFIERS,
  SHIFT_MODIFIERS,
};
