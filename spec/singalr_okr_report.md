# **Spec: SignalR Service and Web PubSub Service OKR Report**

Version: 1.0
Content-Type: markdown
Authoring-Mode: ai

---

## **1. Purpose**

This spec defines the structure and requirements for generating an **OKR (Objectives and Key Results) Report** for SignalR Service and Web PubSub Service.
The report analyzes OKR performance using predefined KQL queries to collect metrics and supporting data, then generates insights, learnings, and a comprehensive summary of OKR achievement.
The expected output is a data-driven, analytical report suitable for leadership review, quarterly business reviews, and strategic planning.

---

## **2. Audience**

* **Primary audience:** Product managers, engineering leadership, business stakeholders
* **Secondary audience:** Executives, cross-functional teams, finance/planning teams
* **Expertise level:** Intermediate–Expert
* **Expected reading context:** Quarterly business review presentations, email summaries, markdown documentation (GitHub/SharePoint), PDF exports, executive dashboards

---

## **3. Tone & Style Guidelines**

* **Voice:** Professional, analytical, data-driven, executive-summary style
* **Point of view:** Third-person
* **Reading level:** Professional/executive level (explain technical metrics when necessary)
* **Prohibited styles:**

  * Speculative or unsubstantiated claims
  * Overly technical jargon without context
  * Narrative storytelling without data backing
  * Defensive or excuse-making language
  * Excessive optimism or pessimism not supported by data
* **Examples:**

  * Good: "Customer engagement increased 23% QoQ, driven by 45% growth in active connections and 18% improvement in message throughput."
  * Bad: "We think customers are probably happier this quarter and usage seems better."

---

## **4. Required Inputs**

### **4.1 User-Provided Inputs**
Inputs that must be collected from the user before proceeding:

**Mandatory:**
- Service scope: One or both of:
  - SignalR Service
  - Web PubSub Service
- Reporting period: One of the following:
  - Quarter (e.g., `2025 Q1`, `FY25 Q3`)
  - Custom date range (e.g., `2025-01-01` to `2025-03-31`)
  - Fiscal period identifier
- OKR definition source: Location of OKR definitions (file path, SharePoint URL, or manual entry)

**Optional:**
- KQL query definitions: Path to predefined KQL queries or query definitions
- Database/data source connection: Kusto cluster, Application Insights, Log Analytics workspace details
- Previous period comparison: Whether to include QoQ or YoY comparison
- Focus areas: Specific OKRs or key results to emphasize
- Output file path: Where to save the generated report
- Stakeholder notes: Additional context or callouts for specific OKRs

### **4.2 Agent-Gathered Inputs**
Inputs the agent must collect via tools or retrieval before writing:

**Mandatory:**
- OKR definitions for the reporting period:
  - Objectives (text descriptions)
  - Key Results (with target values and measurement units)
  - Owners for each objective and key result
  - Priority/weighting if available
- Actual performance data via KQL queries:
  - Current values for each key result
  - Achievement percentage vs. target
  - Trend data (weekly/monthly progression)
  - Comparison to previous periods
- Supporting operational metrics:
  - Service availability/uptime
  - Customer count (active/new/churned)
  - Connection metrics (peak, average, growth rate)
  - Message throughput (volume, latency, success rate)
  - Error rates and incident counts
  - Cost metrics (if relevant to OKRs)
  - Feature adoption metrics

**Optional:**
- Qualitative data and context:
  - Customer feedback or NPS data
  - Support ticket trends related to OKRs
  - Major feature launches or changes
  - External factors (market conditions, competition)
  - Engineering investment (resources allocated)
- Historical OKR performance:
  - Previous quarters' achievement rates
  - Trend analysis across multiple periods
  - Pattern recognition (seasonal variations)
- Risk and blocker information:
  - Issues that impacted OKR achievement
  - Dependencies that affected results
- Success stories and wins:
  - Notable customer wins
  - Significant improvements
  - Recognition or awards

Inputs may come from:
- Built-in tools for GitHub Copilot VS Code
- MCP tools (Azure/Kusto for KQL queries, SharePoint for OKR definitions, GitHub for release notes)
- Large Language Model tools for GitHub Copilot VS Code
- Context/State (extract from conversation or previous state)
- Local files (files in current workspace, query definitions, OKR documents)
- Database queries via Kusto/Application Insights APIs
- Azure Monitor, Log Analytics, or custom telemetry systems

---

## **5. Section Structure**

The Output MUST follow this exact structure:

1. **Title**
2. **Executive Summary**

   * Overall OKR achievement rate
   * Health status (On Track / At Risk / Off Track)
   * Top achievements
   * Major gaps or misses
3. **OKR Overview**

   * Summary table of all objectives and key results
   * Achievement status for each
   * Visual indicators (✅ Met, ⚠️ Partially Met, ❌ Not Met)
4. **Detailed OKR Analysis**

   * For each Objective:
     * Objective statement
     * Strategic context
     * Key results with targets vs. actuals
     * Supporting metrics and trends
     * Analysis and commentary
5. **Supporting Metrics Dashboard**

   * Core service health metrics
   * Customer and usage metrics
   * Operational excellence metrics
   * Trend visualizations (tables/charts)
6. **Key Learnings**

   * What worked well
   * What didn't work
   * Surprises or unexpected outcomes
   * Root cause analysis for misses
7. **Contributing Factors**

   * Internal factors (features, investments, team changes)
   * External factors (market, competition, economic)
   * Dependencies and partnerships
8. **Insights & Recommendations**

   * Strategic insights from the data
   * Recommended adjustments for next period
   * Process improvements
   * Resource allocation recommendations
9. **Comparison to Previous Periods (Optional)**

   * Quarter-over-quarter trends
   * Year-over-year comparisons
   * Achievement rate trends
10. **Risks & Challenges**

    * Current risks to future OKRs
    * Lessons learned
    * Mitigation strategies
11. **Next Period Preview (Optional)**

    * Proposed OKRs for next period
    * Carry-over items
    * New focus areas
12. **Appendix**

    * Raw data tables
    * KQL queries used
    * Detailed metric definitions
    * Methodology notes

---

## **6. Detailed Section Requirements**

### **Section: Title**

* **Objective:** Provide a clear, specific report title.
* **Expected length:** 1-2 lines
* **Required elements:** 
  * Service name(s)
  * Reporting period
  * Report type (OKR Report)
* **Mandatory details:** Must include quarter/period and year
* **External sources:** None
* **Example:** "SignalR Service & Web PubSub Service OKR Report — Q1 2025"

---

### **Section: Executive Summary**

* **Objective:** Provide a high-level summary of OKR performance for leadership.
* **Expected length:** 4-6 sentences
* **Required elements:**

  * Overall achievement rate (percentage)
  * Health indicator (On Track / At Risk / Off Track)
  * 2-3 top achievements with specific numbers
  * 1-2 major gaps or misses with impact
  * One-sentence outlook
* **Mandatory details:** All numbers must come from actual KQL query results
* **If referencing external sources:** Must cite data source

---

### **Section: OKR Overview**

* **Objective:** Present a complete view of all OKRs at a glance.
* **Expected length:** Summary table + 1-2 paragraph overview
* **Required elements:**

  * Table with columns:
    * Objective
    * Key Result
    * Target
    * Actual
    * Achievement %
    * Status (✅/⚠️/❌)
    * Owner
  * Summary statistics (total OKRs, % achieved, % at risk, % missed)
* **Mandatory details:** 
  * Achievement percentage must be calculated from target vs. actual
  * Status icons must follow consistent criteria (e.g., ✅ ≥90%, ⚠️ 70-89%, ❌ <70%)
* **If referencing external sources:** Validate that targets match official OKR documents

---

### **Section: Detailed OKR Analysis**

* **Objective:** Provide deep analysis for each objective and its key results.
* **Expected length:** 1-2 pages per objective
* **Required elements:**

  For each Objective:
  * **Objective Statement:** Full text of the objective
  * **Strategic Context:** Why this objective matters (1-2 sentences)
  * **Overall Achievement:** Aggregate score across key results
  
  For each Key Result under the objective:
  * **Key Result Statement:** Full text
  * **Target vs. Actual:** Numbers with units
  * **Achievement %:** Calculated percentage
  * **Trend Data:** Weekly or monthly progression (table or description)
  * **Supporting Metrics:** Related operational metrics from KQL queries
  * **Analysis:** 2-4 sentences explaining:
    * What drove the result
    * Why target was met/missed
    * Notable events or changes
    * Quality of the result (not just quantity)
* **Mandatory details:** 
  * Must not fabricate explanations
  * Analysis must be grounded in supporting metrics
  * Include data visualization if helpful (table format acceptable)
* **If referencing external sources:** Must verify metrics against source data

---

### **Section: Supporting Metrics Dashboard**

* **Objective:** Provide operational context for OKR performance.
* **Expected length:** 1-2 pages of tables and metrics
* **Required elements:**

  Categories of metrics:
  * **Service Health:**
    * Availability/SLA compliance
    * Incident count and MTTR
    * Performance metrics (latency, throughput)
  * **Customer & Usage:**
    * Total customers
    * Active connections (peak, average)
    * Message volume
    * Growth rates
  * **Operational Excellence:**
    * Deployment frequency
    * Change success rate
    * Time to mitigate issues
* **Mandatory details:** All metrics must come from KQL queries or verified sources
* **Format:** Tables with period-over-period comparison where applicable

---

### **Section: Key Learnings**

* **Objective:** Extract actionable insights from OKR performance.
* **Expected length:** 3-5 bullet points per category
* **Required elements:**

  * **What Worked Well:**
    * Successful strategies or initiatives
    * Positive surprises
    * Effective investments
  * **What Didn't Work:**
    * Failed approaches
    * Missed expectations
    * Inefficient efforts
  * **Surprises/Unexpected Outcomes:**
    * Unanticipated results (positive or negative)
    * External impacts
  * **Root Causes:**
    * Analysis of why misses occurred
    * Systemic issues identified
* **Mandatory details:** Must be specific and tied to data, not generic observations
* **Prohibited:** Vague statements like "need to improve communication"

---

### **Section: Contributing Factors**

* **Objective:** Identify what influenced OKR achievement.
* **Expected length:** Categorized list (8-12 total items)
* **Required elements:**

  * **Internal Factors:**
    * Feature releases and their impact
    * Team capacity or changes
    * Engineering investments
    * Process improvements
  * **External Factors:**
    * Market conditions
    * Customer behavior changes
    * Competitive landscape
    * Economic impacts
  * **Dependencies:**
    * Platform or service dependencies
    * Partner integrations
    * Cross-team deliverables
* **Mandatory details:** Each factor should include impact assessment (positive/negative, magnitude)

---

### **Section: Insights & Recommendations**

* **Objective:** Provide strategic guidance based on OKR analysis.
* **Expected length:** 6-10 recommendations
* **Required elements:**

  * **Strategic Insights:**
    * Patterns observed in the data
    * Market or customer trend implications
    * Opportunities identified
  * **Recommendations for Next Period:**
    * OKR adjustments (what to continue, change, add, remove)
    * Target recalibration guidance
    * Priority shifts
  * **Process Improvements:**
    * How to improve OKR tracking
    * Better metric selection
    * Enhanced data collection
  * **Resource Allocation:**
    * Investment recommendations
    * Team focus areas
    * Capability gaps to address
* **Mandatory details:** Each recommendation must be specific, actionable, and tied to data insights

---

### **Section: Comparison to Previous Periods (Optional)**

* **Objective:** Show trends over time.
* **Expected length:** 1 page with comparison tables
* **Required elements:**

  * Quarter-over-quarter comparison table
  * Year-over-year comparison if available
  * Achievement rate trends (improving/declining)
  * Commentary on trend direction (1-2 paragraphs)
* **Mandatory details:** Must use actual historical data, not estimates

---

### **Section: Risks & Challenges**

* **Objective:** Identify forward-looking risks.
* **Expected length:** 4-8 risk items
* **Required elements:**

  * **Risk Description:** Clear statement of the risk
  * **Impact:** What could happen if unmitigated
  * **Likelihood:** Assessment of probability
  * **Mitigation Strategy:** Specific actions to address
  * **Owner:** Who is responsible for mitigation
* **Mandatory details:** Must be forward-looking, not rehashing past issues
* **Format:** Table or structured list

---

### **Section: Next Period Preview (Optional)**

* **Objective:** Look ahead to future OKRs.
* **Expected length:** 3-5 bullet points
* **Required elements:**

  * Proposed new objectives or key results
  * Items carrying over from current period
  * New focus areas based on learnings
* **Mandatory details:** Should connect to current period insights

---

### **Section: Appendix**

* **Objective:** Provide supporting technical details.
* **Required elements:**

  * **Raw Data Tables:** Complete data sets used in analysis
  * **KQL Queries:** Full query text for each metric
  * **Metric Definitions:** Precise definition of how each metric is calculated
  * **Methodology Notes:** Data collection approach, time ranges, filters applied
  * **Data Quality Notes:** Any caveats or limitations in the data
* **Format:** Code blocks for queries, tables for data, structured lists for definitions

---

## **7. Task Planning Rules for Agent**

The agent MUST follow these rules:

1. **Identify missing inputs:**
   * Confirm service scope (SignalR, Web PubSub, or both)
   * Confirm reporting period
   * Locate OKR definitions
   * Locate KQL query definitions
2. **For each missing input:**
   * Check local workspace for files
   * Check if user has provided via conversation
   * Ask user if critical information is unavailable
3. **Execute KQL queries:**
   * Load predefined queries from provided location
   * Execute queries against specified data source
   * Collect results for each key result metric
   * Gather supporting operational metrics
   * Validate data completeness and quality
4. **Retrieve OKR definitions:**
   * Load objectives and key results for the period
   * Extract targets, owners, and priorities
   * Validate structure and completeness
5. **Calculate achievement metrics:**
   * Compute achievement percentage for each key result
   * Aggregate by objective
   * Calculate overall achievement rate
   * Identify status (met/at risk/missed) based on thresholds
6. **Analyze and synthesize:**
   * Compare actuals vs. targets
   * Identify trends and patterns
   * Determine contributing factors
   * Extract learnings
   * Formulate insights and recommendations
7. **Fill in sections in exact order:**
   * Follow section structure exactly as defined
   * Ensure all required elements are included
   * Use actual data, no fabrication
8. **Self-review against Quality Checklist:**
   * Verify structure completeness
   * Validate data accuracy
   * Check tone and style
9. **Rewrite sections if criteria fail**
10. **Generate final output**

---

## **8. Required Tools (MCP)**

* **Azure Data Explorer / Kusto MCP:**
  * Execute KQL queries against specified clusters
  * Retrieve telemetry and operational metrics
  * Access SignalR and Web PubSub service data

* **SharePoint MCP:**
  * Retrieve OKR definition documents
  * Access strategic planning materials
  * Fetch historical OKR reports for comparison

* **GitHub MCP:**
  * Read local workspace files (query definitions, OKR docs)
  * Access release notes and feature documentation
  * Retrieve engineering metrics if tracked in repos

* **Application Insights / Azure Monitor APIs:**
  * Service health metrics
  * Performance telemetry
  * Error and exception data

* **Custom Data APIs (if available):**
  * Customer metrics
  * Financial data
  * NPS/satisfaction scores

* **Built-in LLM Tools:**
  * Trend analysis
  * Pattern recognition
  * Insight generation from data
  * Recommendation formulation

---

## **9. Quality Checklist**

### **Structure**

- [ ] All required sections included
- [ ] Section order strictly followed
- [ ] Markdown formatting correct and consistent
- [ ] Headers at appropriate levels
- [ ] Tables properly formatted

### **Content Quality**

- [ ] All metrics backed by actual KQL query results
- [ ] OKR definitions match official source documents
- [ ] Achievement percentages correctly calculated
- [ ] No assumptions or hallucinations
- [ ] All tables fully populated with real data
- [ ] All mandatory details included in each section
- [ ] Supporting metrics align with key results
- [ ] Learnings and insights are specific and data-driven
- [ ] Recommendations are actionable and tied to analysis
- [ ] Historical comparisons use actual historical data

### **Data Accuracy**

- [ ] Numbers add up correctly
- [ ] Percentages calculated accurately
- [ ] Trends correctly interpreted
- [ ] Data sources properly cited
- [ ] Query results validated
- [ ] Units of measurement specified
- [ ] Time periods clearly stated

### **Tone & Style**

- [ ] Professional, analytical, executive-appropriate
- [ ] No defensive or excuse-making language
- [ ] Balanced view of successes and misses
- [ ] Data-driven statements, not speculation
- [ ] No jargon without explanation
- [ ] No filler or redundancy
- [ ] Clear, concise language

### **Completeness**

- [ ] All OKRs from the period covered
- [ ] All key results analyzed
- [ ] Supporting metrics provided for each OKR
- [ ] Learnings extracted
- [ ] Recommendations provided
- [ ] Appendix includes queries and definitions

If any criteria fail → revise before final output.

---

## **10. Final Output Format**

The final output MUST be in **markdown** using this skeleton:

```markdown
# <Service Name(s)> OKR Report — <Period>

## Executive Summary
<Overall achievement rate, health status, top achievements, major gaps, outlook>

## OKR Overview
<Summary table of all objectives and key results with status>
<Summary statistics>

## Detailed OKR Analysis

### Objective 1: <Objective Statement>
**Strategic Context:** <Why this matters>
**Overall Achievement:** <Aggregate score>

#### Key Result 1.1: <Key Result Statement>
- **Target:** <Target value with units>
- **Actual:** <Actual value with units>
- **Achievement:** <Percentage>
- **Status:** <✅/⚠️/❌>

**Trend Data:**
<Table or description of progression>

**Supporting Metrics:**
<Related operational metrics>

**Analysis:**
<What drove the result, why target was met/missed, notable events>

#### Key Result 1.2: <Key Result Statement>
<Same structure as 1.1>

### Objective 2: <Objective Statement>
<Same structure as Objective 1>

## Supporting Metrics Dashboard

### Service Health Metrics
<Table of availability, incidents, performance>

### Customer & Usage Metrics
<Table of customers, connections, messages, growth>

### Operational Excellence Metrics
<Table of deployment, changes, issue resolution>

## Key Learnings

### What Worked Well
- <Learning 1>
- <Learning 2>
- <Learning 3>

### What Didn't Work
- <Learning 1>
- <Learning 2>

### Surprises/Unexpected Outcomes
- <Item 1>
- <Item 2>

### Root Causes for Misses
- <Analysis 1>
- <Analysis 2>

## Contributing Factors

### Internal Factors
- <Factor 1>
- <Factor 2>

### External Factors
- <Factor 1>
- <Factor 2>

### Dependencies
- <Dependency 1>
- <Dependency 2>

## Insights & Recommendations

### Strategic Insights
- <Insight 1>
- <Insight 2>

### Recommendations for Next Period
- <Recommendation 1>
- <Recommendation 2>

### Process Improvements
- <Improvement 1>
- <Improvement 2>

### Resource Allocation
- <Recommendation 1>
- <Recommendation 2>

## Comparison to Previous Periods
<QoQ and YoY comparison tables>
<Trend commentary>

## Risks & Challenges
<Table or list of risks with impact, likelihood, and mitigation>

## Next Period Preview
- <Preview item 1>
- <Preview item 2>

## Appendix

### Raw Data Tables
<Complete data sets>

### KQL Queries
```kql
// Query 1: <Description>
<Query text>

// Query 2: <Description>
<Query text>
```

### Metric Definitions
- **Metric 1:** <Definition and calculation method>
- **Metric 2:** <Definition and calculation method>

### Methodology Notes
<Data collection approach, time ranges, filters, caveats>
```

---

## **11. Metadata**

**Spec version:** 1.0

**Tags:** okr, objectives, key-results, performance-report, analytics, signalr, web-pubsub, kql, quarterly-review

**Compatible data sources:** Azure Data Explorer, Kusto, Application Insights, Log Analytics, Custom APIs

**Related specs:** product_status_report.md

**Last updated:** 2025-12-03

---
