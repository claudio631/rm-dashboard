/**
 * Ad Copy Generator — Recruitment Marketing Flex
 *
 * AI-assisted recruitment ad copy generation with variants
 * for Indeed Flex campaigns across all channels.
 *
 * @module ad-copy-generator
 * @squad recruitment-marketing-flex
 */

/**
 * Ad copy templates organized by channel and format.
 */
const TEMPLATES = {
  google_search: {
    headlines: {
      max_length: 30,
      count: 15,
      patterns: [
        '{jobTitle} Jobs - {location}',
        'Hiring {jobTitle}s Now',
        '{payRate}/hr - {jobTitle}',
        'Flexible {jobTitle} Jobs',
        'Indeed Flex - Apply Today',
        'No Experience Needed',
        'Weekly Pay - {jobTitle}',
        'Start This Week',
        '{jobTitle} - {shiftType} Shift',
        'Earn ${payMin}-${payMax}/hr',
        'Pick Your Own Schedule',
        'Temp {jobTitle} Jobs',
        '{location} - Hiring Now',
        'Apply in 5 Minutes',
        'Flexible Work Schedule',
      ],
    },
    descriptions: {
      max_length: 90,
      count: 4,
      patterns: [
        'Join Indeed Flex as a {jobTitle} in {location}. ${payMin}-${payMax}/hr. Flexible schedule, weekly pay. Apply now!',
        'Looking for {jobTitle} work? Indeed Flex has {shiftType} shifts available in {location}. No long-term commitment. Apply today.',
        'Earn ${payMin}-${payMax}/hr as a {jobTitle}. Choose your shifts with Indeed Flex. Weekly pay & benefits available.',
        '{jobTitle} positions open in {location}. Flexible hours, competitive pay. Download the Indeed Flex app to get started.',
      ],
    },
  },
  meta: {
    primary_text: {
      max_length: 125,
      patterns: [
        'Looking for flexible work? Indeed Flex is hiring {jobTitle}s in {location}. Pick your shifts, get paid weekly.',
        'Earn ${payMin}-${payMax}/hr as a {jobTitle} with Indeed Flex. No long-term commitment — work when you want.',
        '{jobTitle} jobs available NOW in {location}. Flexible scheduling + weekly pay. Tap Apply to get started.',
      ],
    },
    headline: {
      max_length: 40,
      patterns: [
        'Flexible {jobTitle} Jobs',
        'Work When You Want',
        'Hiring {jobTitle}s Now',
      ],
    },
    description: {
      max_length: 30,
      patterns: [
        'Apply in minutes',
        'Weekly pay available',
        'No experience needed',
      ],
    },
  },
  reddit: {
    title: {
      max_length: 300,
      patterns: [
        'Looking for flexible {jobTitle} work in {location}? Indeed Flex lets you pick your own shifts',
        'Indeed Flex is hiring {jobTitle}s - ${payMin}-${payMax}/hr, choose when you work, get paid weekly',
        'Anyone tried flexible shift work? We\'re hiring {jobTitle}s in {location} with Indeed Flex',
      ],
    },
  },
  indeed: {
    sponsored_title: {
      max_length: 80,
      patterns: [
        '{jobTitle} - Flexible Schedule - ${payMin}-${payMax}/hr',
        '{jobTitle} - Indeed Flex - {location}',
        '{jobTitle} - Weekly Pay - No Experience Required',
      ],
    },
  },
};

/**
 * Generate ad copy variants for a specific channel.
 *
 * @param {Object} params
 * @param {string} params.channel - Target channel (google_search, meta, reddit, indeed)
 * @param {string} params.jobTitle - Job title
 * @param {string} params.location - Target location
 * @param {number} params.payMin - Minimum pay rate
 * @param {number} params.payMax - Maximum pay rate
 * @param {string} [params.shiftType='Flexible'] - Shift type
 * @returns {Object} Generated ad copy variants by format
 */
function generateAdCopy(params) {
  const { channel, jobTitle, location, payMin, payMax, shiftType = 'Flexible' } = params;

  const template = TEMPLATES[channel];
  if (!template) {
    throw new Error(`Unknown channel: ${channel}. Available: ${Object.keys(TEMPLATES).join(', ')}`);
  }

  const variables = { jobTitle, location, payMin, payMax, shiftType, payRate: `$${payMin}-$${payMax}` };
  const result = {};

  for (const [format, config] of Object.entries(template)) {
    result[format] = config.patterns.map((pattern) => {
      let text = pattern;
      for (const [key, value] of Object.entries(variables)) {
        text = text.replace(new RegExp(`\\{${key}\\}`, 'g'), value);
        text = text.replace(new RegExp(`\\$\\{${key}\\}`, 'g'), value);
      }
      return {
        text,
        length: text.length,
        withinLimit: text.length <= config.max_length,
        maxLength: config.max_length,
      };
    });
  }

  return { channel, ...result };
}

/**
 * Generate ad copy across all channels at once.
 *
 * @param {Object} params - Same as generateAdCopy (without channel)
 * @returns {Object} Ad copy for all channels
 */
function generateAllChannels(params) {
  return Object.keys(TEMPLATES).reduce((acc, channel) => {
    acc[channel] = generateAdCopy({ ...params, channel });
    return acc;
  }, {});
}

/**
 * Validate ad copy against channel limits.
 *
 * @param {string} text - Ad copy text
 * @param {string} channel - Channel name
 * @param {string} format - Format type (headline, description, etc.)
 * @returns {Object} Validation result
 */
function validateCopy(text, channel, format) {
  const template = TEMPLATES[channel];
  if (!template || !template[format]) {
    return { valid: false, error: 'Unknown channel or format' };
  }

  const maxLength = template[format].max_length;
  return {
    valid: text.length <= maxLength,
    length: text.length,
    maxLength,
    remaining: maxLength - text.length,
    truncated: text.length > maxLength ? text.substring(0, maxLength) : null,
  };
}

module.exports = {
  generateAdCopy,
  generateAllChannels,
  validateCopy,
  TEMPLATES,
};
