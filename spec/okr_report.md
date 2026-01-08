# Spec: OKR / KR Telemetry Report
Version: 1.0
Content-Type: Analytical OKR Report
Authoring-Mode: AI

---

## 1. Purpose
Define how the agent generates a telemetry-backed OKR/KR report using knowledge-sourced definitions (time semantics, thresholds, filters) and recent data. The report must enumerate all OKRs/KRs from the knowledge source, show latest N time windows per OKR/KR, assess volume thresholds, analyze trends/structural changes, perform cohort comparisons, drill into errors, and summarize insights and risks.

---

## 2. Audience
- Primary audience: PMs/engineering leads owning OKRs
- Secondary audience: Data/telemetry analysts supporting PMs
- Expertise level: Intermediate; expects familiarity with metrics and cohorts
- Expected reading context: Markdown delivered via chat or docs, viewable on web/desktop/mobile

---

## 3. Tone & Style Guidelines
- Voice: Analytical, concise, confident; PM-style with crisp bullets
- Point of view: Third-person, neutral and evidence-driven
- Reading level target: Clear to technical stakeholders; avoid jargon without context
- Prohibited styles: Marketing tone, speculation without data, filler

---

## 4. Required Inputs

### 4.1 User-Provided Inputs
Inputs that must be collected from the user before proceeding:

**Mandatory:**
- OKR knowledge source location: Path/URL to the OKR knowledge file that defines OKR/KR names, time semantics, targets, volume thresholds, global filters, and recommended dimensions.
- Scope identifiers: Product/client/service name(s) to focus on if the knowledge covers multiple scopes.

**Optional:**
- Reporting anchor date: Defaults to "today" in UTC; used to resolve "latest N completed windows".
- Override for number of windows `N`: Defaults to the value specified per OKR/KR in knowledge.
- Additional global filters: Extra filters (e.g., region, release channel) to apply consistently.

### 4.2 Agent-Gathered Inputs
Inputs the agent must collect via tools or retrieval before writing:

**Mandatory:**
- OKR/KR catalog: Names, descriptions, targets, default time window definitions (calendar vs rolling), default number of windows `N`, volume thresholds, and global filters from the OKR knowledge file.
- Telemetry schema + analysis dimensions: Tables/measures, timestamp fields, and columns tagged as analysis dimensions (or equivalents) from the knowledge file.
- Latest OKR/KR values: Metric values and underlying volumes for each OKR/KR for the latest `N` windows based on each OKR's default time semantics.
- Volume sufficiency check: Compare latest period volumes against the OKR-specific thresholds from knowledge.
- Cohort slices: Breakdowns for the last two completed windows across key dimensions (from knowledge tags plus obvious dimensions such as client version, scenario/project type, error category).
- Error drilldown data: Top errors for the last two completed windows, plus the same errors sliced by key analysis dimensions.

**Optional:**
- User notes or risk callouts for interpretation.
- Additional dimensions present in telemetry but not tagged in knowledge when they materially improve insight density.

Inputs may come from:
- PowerBI Remote MCP Server (preferred) using the knowledge-defined semantic model/tables.
- Azure Data Explorer (ADX or kusto) MCP Server using the knowledge-defined queries.
- Local files in the workspace (knowledge documents, query definitions).
- Context/state from the ongoing conversation.

---

## 5. Data Requirements
Detail the structured data the agent must gather (beyond user inputs) before writing.

- **okr_definitions**: Full list of OKRs/KRs, descriptions, targets, volume thresholds, default window type, default `N`, global filters. Source: OKR knowledge file. Fields: name, description, target, threshold definition, window type (calendar/rolling + grain), default N, table/measure references, filters.
- **time_windows**: Resolved list of the latest `N` completed windows per OKR based on its window definition (e.g., last 6 completed calendar months, last 2 rolling 28-day windows). Fields: window label, start_date, end_date, completeness flag. Update cadence: computed at run time.
- **okr_values_by_window**: For each OKR and time window: numerator, denominator, metric value, applied filters, time label. Source: Power BI MCP queries. Update cadence: latest available data.
- **volume_checks**: For the latest completed window per OKR: volume vs threshold, pass/fail flag, rationale. Source: Power BI MCP queries + thresholds from knowledge.
- **trend_series**: Metric and volume time series for the latest `N` windows per OKR to detect structural changes. Fields: value, numerator, denominator, period label. Update cadence: same as okr_values_by_window.
- **analysis_dimensions**: Candidate cohort dimensions from knowledge (`IsAnalysisDimension = Yes`) plus common telemetry fields (e.g., scenario/project type, client version, region, error category). Source: knowledge + semantic model or knowledge + kusto queries.
- **cohort_slices_last_two**: For each dimension, slices for the last two completed windows: slice label, numerator, denominator, metric value, delta vs previous window. Source: Power BI MCP queries.
- **top_errors_last_two**: Top errors by impact for the last two completed windows, respecting OKR filters. Fields: error code/category, projects/users impacted, events, contribution to failures. Source: Power BI MCP queries.
- **error_slices_last_two**: Top errors sliced by key dimensions (e.g., client version, scenario) for the last two completed windows. Fields: slice label, error code, projects impacted, events. Source: Power BI MCP queries.

---

## 6. Tool Dependencies

Tool Dependencies:
- powerbi
- kusto

---

## 7. Fallback Plan
- Detect missing data: knowledge file unavailable, `powerbi` server missing, `kusto` server missing, query errors, or empty query results.
- Alternatives:
  - If `powerbi` unavailable: ask user to setup [PowerBI Remote MCP Server](https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-get-started) which supports to query Power BI semantic models using natural language, retrieve model schemas, generate DAX queries, and execute queries to deliver insights from data.
  - If `kusto` unavailable: ask user to setup [Azure MCP server](https://github.com/Azure/azure-mcp) which contains the kusto capabilities. 
  - If knowledge missing fields: ask user for OKR targets, thresholds, default window definitions, recommended dimensions, and filters.
- Questions to ask the user:
  - Provide OKR definitions (name, target, window type, default N, filters).
  - Provide volume thresholds per OKR.
  - Provide latest `N` metric values with numerator/denominator per window.
  - Provide cohort slices for last two windows and top errors with slices.
- Minimal data to proceed:
  - OKR names + metric formulas + targets + window type + default N.
  - Latest two windows of metric values with volumes.
  - At least one breakdown dimension and top errors for the last window.

---

## 8. Section Structure
1. **Title & Metadata**
2. **Global Filters & Time Window Definition**
3. **OKR/KR Values — Latest N Windows**
4. **Latest Window Volume & Target Check**
5. **Trend Analysis**
6. **Cohort Analysis (Last Two Completed Windows)**
7. **Error Drilldown (Last Two Completed Windows)**
8. **Summary & Next Actions**

Each section MUST be generated exactly as structured here.

---

## 9. Detailed Section Requirements

### Section: Title & Metadata
- Objective: Establish context for the report.
- Expected length: 2–4 lines.
- Required elements: Report date, OKR scope/name(s), time window definition (default per knowledge), data currency, global filters in brief.
- Mandatory details: Cite the knowledge source used and the anchor date for resolving windows.

### Section: Global Filters & Time Window Definition
- Objective: Make filters/time semantics explicit to ensure reproducibility.
- Expected length: Short bullets.
- Required elements: Tables/measures used, global filters from knowledge, default time window type per OKR/KR, default number of windows `N`, treatment of internal vs external, channel/release filters.
- Mandatory details: Note any user-specified overrides to defaults.

### Section: OKR/KR Values — Latest N Windows
- Objective: List metric values for each OKR/KR across the latest `N` completed windows.
- Expected length: Tables per OKR/KR.
- Required elements: Time window label, numerator/denominator (volumes), metric value, target value, pass/fail vs target.
- Mandatory details: Use the OKR-specific default `N` and time semantics from knowledge unless overridden.

### Section: Latest Window Volume & Target Check
- Objective: Confirm that the latest completed window meets volume thresholds and compare to target.
- Expected length: 3–6 bullets per OKR/KR.
- Required elements: Latest window dates, volume vs threshold (pass/fail), metric vs target (pass/fail), commentary on volume stability/sufficiency.
- Mandatory details: Threshold definitions from knowledge and explicit pass/fail flags.

### Section: Trend Analysis
- Objective: Explain meaningful structural changes in the metric over the latest `N` windows (what changed, when it changed, and whether it persisted).
- Expected length: 3–5 insights per OKR/KR, prioritizing signal over completeness.
- Scope & approach (flexible):
  - Start from the headline time series and reason holistically before segmenting.
  - Treat a trend as a pattern across windows, not a single data point.
  - Adapt the method to signal strength, volatility, and volume.
- Reference patterns (guidance, not a checklist; apply only when supported by data): sustained shifts, step changes, dips/recoveries, acceleration/deceleration, stability vs. volatility, and volume-supported vs. volume-artifact movement.
- Required elements per insight:
  - State what changed and when (cite specific windows/periods).
  - Indicate whether the change appears structural (persistent) or transient.
  - Add brief volume context (stable/growing/shrinking; numerator/denominator shifts for rates when relevant).
- Guardrails:
  - Avoid speculation/causal claims unless directly supported.
  - Do not restate raw metrics; interpret patterns.
  - If no meaningful structural change exists, explicitly state the series is stable / within expected variance.

### Section: Cohort Analysis (Last Two Completed Windows)
- Objective: Explain what drove change in the baseline OKR/KR values.
- Expected length: 2–5 insights total plus compact tables for the highest-signal cohorts.
- Baseline: Use the OKR/KR metric values (and their numerator/denominator volumes) as the headline; cohort analysis explains the delta between the last two completed windows.
- Cohort formation:
  - Choose segmentation dimensions based on context and signal (from knowledge + telemetry, try at least 3-5 dimensions or bundle of dimensions).
  - Prefer mutually exclusive cohorts when doing attribution; allow overlaps for exploratory insights.
  - Adjust granularity dynamically to avoid fragmentation/noise.
- Measure change and impact (per cohort, when possible): current value, previous value, absolute change (Δ).
  - Rank/group cohorts by impact; favor absolute change over percentages.
  - Use metrics appropriate to context; for rates/ratios, also show numerator and denominator deltas.
- Attribute contribution (when well-defined):
  - If overall delta is meaningful: `ContributionPct = Δ(cohort) / Δ(overall)`.
  - If overall delta is zero/unclear: describe offsetting cohort movements instead of forcing a percentage.
- Drill down selectively: deepen analysis only for high-impact or high-signal cohorts; use multi-dimensional intersections sparingly.
- Reconcile and validate: cohort-level changes should reconcile to the headline metric; treat mismatches as definition/dedup/filter issues before behavioral interpretation.
- Interpretation guardrails:
  - Treat undefined/infinite % changes as “starting from near zero.”
  - Avoid percentage-only narratives; include absolute values and deltas.
  - Don’t confuse biggest % change with biggest contribution; check overlap/dedup if cohort results conflict with headline.

### Section: Error Drilldown (Last Two Completed Windows)
- Objective: Identify top errors and where they concentrate.
- Expected length: Tables plus 2–4 insights.
- Required elements: Top errors by impact for last two completed windows; slices of top errors by key dimensions (e.g., client version, scenario); note contributions to failure volume.
- Mandatory details: Apply OKR global filters; highlight whether error patterns are stable or shifting between the two windows.

### Section: Summary & Next Actions
- Objective: Summarize findings and propose follow-ups.
- Expected length: 4–6 bullets.
- Required elements: Key OKR status (at/above/below target), main trend takeaway, highest-urgency cohorts/errors, volume sufficiency statement, 2–3 suggested actions/owners if available.
- Mandatory details: Call out data gaps or assumptions if any fallback data was used.

---

## 10. Task Planning Rules for Agent
For this spec, the agent must do the following tasks:
1. Identify missing inputs from the user (knowledge source, scope, overrides).
2. Load OKR knowledge and extract definitions, time semantics, thresholds, and dimensions.
3. Retrieve telemetry for OKR/KR values across the latest `N` windows using default time semantics per OKR.
4. Compute volume checks for the latest completed window per OKR.
5. Generate trend analysis with structural change detection and volume stability notes.
6. Pull cohort slices for the last two completed windows across key dimensions and compare deltas.
7. Perform error drilldown for the last two completed windows, including slices by key dimensions.
8. Draft the report following Section Structure, then self-review against the Quality Checklist.
9. If required data is missing, ask the user for the minimal fields outlined in the Fallback Plan and mark gaps in the draft.

---

## 11. Quality Checklist
The final content MUST satisfy all criteria:

### Structure
- All required sections included in the specified order.
- Tables include volumes (numerator/denominator) alongside percentages.
- Latest window clearly identified and based on completed periods only.

### Content Quality
- Uses OKR definitions, time semantics, targets, thresholds, and filters from the knowledge source.
- Trend analysis includes structural changes and volume sufficiency statements.
- Cohort and error sections compare the last two completed windows with deltas.
- No hallucinated data; all insights tied to retrieved telemetry.

### Tone
- Analytical, concise, and evidence-driven.
- No marketing language or filler.
- Clear pass/fail statements for targets and thresholds.

If any criteria fail → revise before final output.

---

## 12. Final Output Format
Deliver the report in Markdown using the exact skeleton below:

```markdown
# <OKR 1 Report Title>

**Report date:** <YYYY-MM-DD>  

| OKR/KR Name | OKR Scope | Time Window | Global filters applied | 
|------------:|:----------|:------------|:-----------------------|
| <NAME_OF_OKR> | <Product/Client/Service/Feature> | <Default window description and N> | <Filter 1>; <Filter 2>; ... | 

## 1. OKR/KR Values — Latest N Windows
<Tables per OKR/KR>

## 2. Latest Window Volume & Target Check
<Bullets per OKR/KR>

## 3. Trend Analysis
<3–5 insights per OKR/KR; note volume stability>

## 4. Cohort Analysis (Last Two Completed Windows)
<Tables and insights per OKR/KR by key dimensions>

## 5. Error Drilldown (Last Two Completed Windows)
<Top errors and slices per OKR/KR by key dimensions>

## 6. Summary & Next Actions
<4–6 bullets with status, risks, and actions per OKR/KR>


```
