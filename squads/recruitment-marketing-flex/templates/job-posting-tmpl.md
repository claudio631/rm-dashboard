# {{job_title}} — Indeed Flex

## Job Details

| Field | Value |
|-------|-------|
| **Title** | {{job_title}} |
| **Category** | {{job_category}} |
| **Location** | {{city}}, {{state}} |
| **Pay Rate** | ${{pay_min}} - ${{pay_max}} / hour |
| **Shift Type** | {{shift_type}} (Day / Night / Weekend / Flexible) |
| **Duration** | {{duration}} (Ongoing / Temporary / Seasonal) |

---

## SEO-Optimized Job Title

**Primary:** {{seo_title}}
**Alternatives tested:** {{alt_title_1}} | {{alt_title_2}}

---

## Job Description

### About the Role

Join Indeed Flex as a **{{job_title}}** in **{{city}}, {{state}}**! We're looking for {{candidate_description}} to join our flexible workforce.

**Pay: ${{pay_min}} - ${{pay_max}}/hour** | **{{shift_type}} shifts available**

### What You'll Do

- {{responsibility_1}}
- {{responsibility_2}}
- {{responsibility_3}}
- {{responsibility_4}}

### What You'll Need

- {{requirement_1}}
- {{requirement_2}}
- {{requirement_3}}

### Nice to Have

- {{preferred_1}}
- {{preferred_2}}

### Why Indeed Flex?

- **Flexible scheduling** — Pick shifts that fit your life
- **Weekly pay** — Get paid every week
- **No experience required** — We provide training for many roles
- **Benefits available** — Health, dental, and vision for eligible workers
- **Easy app** — Find and claim shifts from your phone

### How to Apply

1. Download the Indeed Flex app or apply online
2. Complete your profile (takes ~5 minutes)
3. Start picking up shifts in your area!

---

## Google for Jobs Schema

```json
{
  "@context": "https://schema.org/",
  "@type": "JobPosting",
  "title": "{{seo_title}}",
  "description": "{{meta_description}}",
  "datePosted": "{{date_posted}}",
  "validThrough": "{{valid_through}}",
  "employmentType": "{{employment_type}}",
  "hiringOrganization": {
    "@type": "Organization",
    "name": "Indeed Flex",
    "sameAs": "https://www.indeedflex.com",
    "logo": "{{logo_url}}"
  },
  "jobLocation": {
    "@type": "Place",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "{{street}}",
      "addressLocality": "{{city}}",
      "addressRegion": "{{state}}",
      "postalCode": "{{zip}}",
      "addressCountry": "US"
    }
  },
  "baseSalary": {
    "@type": "MonetaryAmount",
    "currency": "USD",
    "value": {
      "@type": "QuantitativeValue",
      "minValue": {{pay_min}},
      "maxValue": {{pay_max}},
      "unitText": "HOUR"
    }
  }
}
```

## Meta Tags

```html
<title>{{seo_title}} - Indeed Flex | {{city}}, {{state}}</title>
<meta name="description" content="{{meta_description}}" />
```

## UTM for Promotion

```
?utm_source={{source}}&utm_medium={{medium}}&utm_campaign={{campaign}}&utm_content={{job_id}}
```

---
*Template: job-posting-tmpl.md | Squad: recruitment-marketing-flex*
