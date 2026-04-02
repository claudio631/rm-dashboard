# Indeed Flex — SOP: Indeed Ad Request Process

> Source: `SOP - Indeed Recruitment Request.docx` — imported 2026-03-17

## Team

| Name | Role | Country |
|------|------|---------|
| Claudio Santos | Recruitment Marketing Specialist | US |
| Craig Freeman | Recruitment Marketing Specialist | US |
| Olivia Smith | Recruitment Marketing Manager | UK |

## Key Definitions

| Term | Definition |
|------|-----------|
| **Dummy Shift** | A shift created in ACP to allow FHS ads to appear in the Indeed Flex app. Not a real shift — used as a bridge to connect Indeed Ads with the app. |
| **FHS** | The ATS (Applicant Tracking System) used by Indeed Flex for sourcing requisitions |
| **Evergreen** | A role that Indeed Flex constantly recruits for — building a permanent pool of workers |
| **LFDTW** | "Leave Flexers Do The Work" |
| **RSVPs (in FHS)** | Actually = how many AI interviews have been reviewed (interview outcomes, not event RSVPs) |
| **Cobranding** | When a client (e.g., Stord) allows Indeed Flex to use their name/logo in advertising |
| **ATS** | Applicant Tracking System — manages the hiring pipeline electronically |

## End-to-End Ad Request Flow

### Step 1: New Recruitment Request

**Trigger:** Slack notification or email → Monday.com board

**Required information (minimum):**
- Pay rate
- Client name
- Job type (e.g., prep cook, assembler, forklift operator)
- Job location (specific metro area)
- Shift start and end date
- Desired number of employees (headcount)
- Role requirements (certifications, degrees, experience, background check)

**If info missing:** Reach out to the requester for clarification.

### Step 2: Job Description Creation

1. Copy job description from the request
2. Use AI to generate a professional version (using Job Description template)
3. OR look for same role/company in FHS for an existing model
4. Can duplicate an existing ad in FHS

### Step 3: UTM Link Creation

**Critical for measurement.** Use:
1. **W2A Worker Journey Project** spreadsheet — find the correct landing page matching the role and country
2. **Advertising UTM Link Generator** spreadsheet — use your personal tab
3. Fill out correctly; if employer not registered, put "NA"

### Step 4: Create Dummy Shift in ACP (if needed)

**Why:** A dummy shift must exist in ACP for Indeed ads to appear in the Indeed Flex app.

**Process:**
1. Open `https://admin.indeedflex.com/dashboard`
2. Go to Employers tab → search "indeed flex application"
3. Login as Employer → Post a Job
4. Select venue by industry + metro area
5. Set a **long date range** (months) — short periods cause ads to stop running
6. Select industry, role, competencies
7. Add job title, hourly rate, job description, uniform
8. **Always select "Individual flexors"** (avoid spending on other options)
9. **Always flag OFF "Maximize Fulfillment"**
10. After creation → **Stop Job Offers** immediately (it's a dummy, not real)
11. **Copy the Job ID** — needed for creating ads in FHS

**Standard dummy shift job description:**
> "Sign up here for your Indeed Flex onboarding interview. In this virtual interview, we will be reviewing and verifying your skills as an _{role}_. Once you are verified, you will be able to book _{shift type}_ in the app."

**Uniform guidance:**
- Hospitality → standard hospitality uniform
- Industrial → reflective vests

### Step 5: Create Ad in FHS

**Required inputs:**
- Landing page link (with UTM)
- Job description
- Pay rate
- Evaluation link (if client requests)
- For hiring events: in-person session with time slots

**Campaign naming convention:**

```
{Country} - {Market Type} - {Industry} - {Client Name} - {Role} - {Metro} - {State} - {Period}
```

| Segment | Description | Examples |
|---------|-------------|---------|
| Country | Country code | US, UK |
| Market Type | Business model | B2C, B2B |
| Industry | Client industry vertical | Hospitality, Industrial, Logistics, Events |
| Client Name | Client company name | Culinaire, CORT, Stord, OnTrac |
| Role | Job title being recruited | Servers, Loader / Crew, Warehouse Operative, Picker Packer |
| Metro | Metro area / city | DFW, Las Vegas, Chicago, Austin |
| State | State abbreviation | TX, NV, IL, OH |
| Period | Campaign date range (Month Day to Month Day, Year) | March 16 to March 30, 2026 |

**Example:**
`US - B2C - Hospitality - Culinaire - Servers - DFW - TX - March 16 to March 30, 2026`

**Rules:**
- Use hyphens ` - ` (space-hyphen-space) as separators
- Metro should match the market name used in funnel reports
- Period always includes start date, end date, and year
- For evergreen campaigns, use "Evergreen" as the period

**For Hiring Events:**
- Create in-person hiring session
- Time slots: top of every hour (e.g., 10am, 11am, 12pm, 1pm)
- 20 candidates per slot
- Prevents onsite team overwhelm

### Step 6: Create Indeed Campaign

**Naming:** `{Country} - {Market Type} - {Industry} - {Client Name} - {Role} - {Metro} - {State} - {Period}`
(see Step 5 for full convention and examples)

### Step 7: Update Campaign Spreadsheet

Track in the Indeed Budget Request and Campaign Performance spreadsheet.

## Systems & URLs

| System | URL | Purpose |
|--------|-----|---------|
| **FHS (ATS)** | `joinflex.indeed.com/us/sourcing/requisitions` | Manage requisitions and ads |
| **Indeed Employer** | `employers.indeed.com/reporting/ads` | Campaign reporting |
| **Indeed Budget Control** | Google Sheets (shared) | Budget tracking and campaign performance |
| **ACP** | `admin.indeedflex.com/dashboard` | Shift management, dummy shifts |
| **IF App Portal** | `portal.indeedflex.com/schedule` | Dummy shift scheduling |

## Quality Control

1. Check `Indeed.com` to verify ad is showing up
2. Check both Indeed.com AND QA inside the Indeed Flex app
3. Verify the full flow — ad → landing page → app (no dead ends)
4. Note: Loader/Crew gets verified for Warehouse Op but **not** the other way around

## Opportunities / Pain Points

- To track ad performance **per zip code**, a separate dummy shift must be created for each one
- Dummy shift expiration causes ads to stop — must monitor
- Manual process across multiple systems (Monday → ACP → FHS → Indeed → Spreadsheet)

## Automation Opportunities for RM Team AI

| Current Manual Step | Automation Potential |
|--------------------|---------------------|
| Check Monday.com for new requests | Webhook/API integration |
| Create UTM links manually in spreadsheet | UTM Builder tool (already built in squad) |
| Create dummy shifts in ACP | API automation if ACP has endpoints |
| Create ads in FHS | API integration with FHS |
| Create Indeed campaigns | Indeed Ads API |
| Update campaign spreadsheet | Auto-populate from campaign data |
| QA check (ad showing in app) | Automated flow verification |
| Monitor dummy shift expiration | Alert system |
