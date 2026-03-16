/**
 * Audience Builder — Recruitment Marketing Flex
 *
 * Define and export audience segments for campaign targeting
 * across Indeed Flex advertising channels.
 *
 * @module audience-builder
 * @squad recruitment-marketing-flex
 */

/**
 * Pre-built audience templates for Indeed Flex.
 */
const AUDIENCE_TEMPLATES = {
  warehouse_workers: {
    name: 'Warehouse Workers',
    description: 'People interested in warehouse, fulfillment, and distribution jobs',
    demographics: { age: '18-55', gender: 'all' },
    interests: ['warehouse jobs', 'logistics', 'fulfillment', 'manual labor', 'forklift'],
    behaviors: ['job seekers', 'recently searched warehouse jobs'],
    exclusions: ['current warehouse managers', 'logistics directors'],
    locations: [],
    channels: {
      google: { audiences: ['in-market: jobs & education', 'custom intent: warehouse keywords'] },
      meta: { interests: ['Warehouse work', 'Amazon warehouse', 'UPS'], behaviors: ['Job seekers (recent)'] },
      reddit: { subreddits: ['r/warehouse', 'r/AmazonFC', 'r/jobs'] },
    },
  },
  delivery_drivers: {
    name: 'Delivery Drivers',
    description: 'People interested in delivery, courier, and driving opportunities',
    demographics: { age: '21-60', gender: 'all' },
    interests: ['delivery jobs', 'courier', 'driving', 'gig economy', 'DoorDash', 'Uber'],
    behaviors: ['gig workers', 'rideshare drivers', 'delivery app users'],
    exclusions: ['CDL truck drivers', 'long haul drivers'],
    locations: [],
    channels: {
      google: { audiences: ['in-market: delivery jobs', 'custom intent: delivery driver keywords'] },
      meta: { interests: ['Delivery driver', 'DoorDash', 'Instacart', 'Gig economy'], behaviors: ['Job seekers'] },
      reddit: { subreddits: ['r/couriersofreddit', 'r/doordash_drivers', 'r/gigwork'] },
    },
  },
  flex_seekers: {
    name: 'Flexible Work Seekers',
    description: 'People actively looking for flexible, part-time, or temporary work',
    demographics: { age: '18-65', gender: 'all' },
    interests: ['flexible work', 'part time jobs', 'temp work', 'gig economy', 'side hustle'],
    behaviors: ['job seekers', 'part-time workers', 'multiple job holders'],
    exclusions: ['full-time professionals', 'executives'],
    locations: [],
    channels: {
      google: { audiences: ['in-market: part-time jobs', 'custom intent: flexible work keywords'] },
      meta: { interests: ['Part-time work', 'Flexible jobs', 'Side hustle'], behaviors: ['Job seekers'] },
      reddit: { subreddits: ['r/sidehustle', 'r/WorkOnline', 'r/beermoney'] },
    },
  },
  retargeting_applicants: {
    name: 'Past Applicants (Retargeting)',
    description: 'People who started but did not complete an application',
    demographics: { age: 'all', gender: 'all' },
    interests: [],
    behaviors: ['visited apply page', 'started application', 'did not complete'],
    exclusions: ['completed application', 'active workers'],
    locations: [],
    channels: {
      google: { audiences: ['remarketing: apply page visitors (7-30 days)'] },
      meta: { audiences: ['custom audience: website visitors - apply page', 'exclude: converters'] },
    },
  },
  lookalike_top_workers: {
    name: 'Lookalike: Top Workers',
    description: 'People similar to Indeed Flex workers with highest shift completion rates',
    demographics: { age: 'all', gender: 'all' },
    interests: [],
    behaviors: ['modeled from top 10% workers by shift count and ratings'],
    exclusions: ['current active workers'],
    locations: [],
    channels: {
      google: { audiences: ['similar audiences: top worker CRM list'] },
      meta: { audiences: ['lookalike 1-3%: top workers seed list'] },
    },
  },
};

/**
 * Build a custom audience segment.
 *
 * @param {Object} params
 * @param {string} params.name - Audience name
 * @param {string} params.description - Audience description
 * @param {Object} [params.demographics] - Age, gender filters
 * @param {string[]} [params.interests] - Interest targeting
 * @param {string[]} [params.behaviors] - Behavioral targeting
 * @param {string[]} [params.exclusions] - Exclusion criteria
 * @param {string[]} [params.locations] - Geographic targeting
 * @returns {Object} Audience definition
 */
function buildAudience(params) {
  const {
    name,
    description,
    demographics = { age: 'all', gender: 'all' },
    interests = [],
    behaviors = [],
    exclusions = [],
    locations = [],
  } = params;

  if (!name) throw new Error('Audience name is required');

  return {
    id: name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, ''),
    name,
    description,
    demographics,
    interests,
    behaviors,
    exclusions,
    locations,
    estimatedSize: null,
    createdAt: new Date().toISOString(),
  };
}

/**
 * Get a pre-built audience template.
 *
 * @param {string} templateName - Template key from AUDIENCE_TEMPLATES
 * @param {string[]} [locations] - Override locations
 * @returns {Object} Audience definition
 */
function fromTemplate(templateName, locations = []) {
  const template = AUDIENCE_TEMPLATES[templateName];
  if (!template) {
    throw new Error(`Unknown template: ${templateName}. Available: ${Object.keys(AUDIENCE_TEMPLATES).join(', ')}`);
  }
  return { ...template, locations, id: templateName };
}

/**
 * List all available audience templates.
 *
 * @returns {Object[]} Template summaries
 */
function listTemplates() {
  return Object.entries(AUDIENCE_TEMPLATES).map(([key, val]) => ({
    key,
    name: val.name,
    description: val.description,
  }));
}

/**
 * Combine multiple audiences into a combined targeting spec.
 *
 * @param {Object[]} audiences - Array of audience definitions
 * @param {string} logic - 'OR' (any audience) or 'AND' (all audiences)
 * @returns {Object} Combined audience
 */
function combineAudiences(audiences, logic = 'OR') {
  return {
    type: 'combined',
    logic,
    audiences: audiences.map((a) => ({ id: a.id, name: a.name })),
    combinedInterests: [...new Set(audiences.flatMap((a) => a.interests))],
    combinedBehaviors: [...new Set(audiences.flatMap((a) => a.behaviors))],
    combinedExclusions: [...new Set(audiences.flatMap((a) => a.exclusions))],
  };
}

module.exports = {
  buildAudience,
  fromTemplate,
  listTemplates,
  combineAudiences,
  AUDIENCE_TEMPLATES,
};
