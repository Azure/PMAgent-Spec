# Spec: ADX Telemetry Knowledge Documentation
Version: 1.0
Content-Type: technical-documentation
Authoring-Mode: hybrid

---

## 1. Purpose
This spec defines how to create an **Azure Data Explorer (ADX) dashboard telemetry knowledge** document by analyzing an **ADX dashboard JSON export** and extracting the queries, their intent, and the expected output schema.

The expected output is a single Markdown knowledge article that:
- Lists product overview (name/description/abbreviations).
- Documents each dashboard query (KQL) and what it is used for.
- Provides a best-effort query result schema table (columns, types, examples/format, notes, and whether a column is suitable as an analysis dimension).
- Captures key usage patterns for cohort analysis.

The output MUST follow the formatting and section structure defined in Section 12, which mirrors `templates/ADX_telemetry_knowledge_template.md`.

---

## 2. Audience
- Primary audience: Product managers, data analysts, and engineers using ADX dashboards for product telemetry
- Secondary audience: Leadership stakeholders reviewing telemetry trends and OKR signals
- Expertise level: Intermediate (assumes familiarity with KQL fundamentals and dashboard concepts)
- Expected reading context: Internal knowledge base / wiki / Markdown documentation

---

## 3. Tone & Style Guidelines
- Voice: Technical, precise, and instructional
- Point of view: Third-person objective documentation style
- Reading level target: Technical professional (no marketing language)
- Prohibited styles:
  - Conversational filler
  - Speculation presented as fact
  - Ambiguous terms (e.g., “probably”, “maybe”) unless explicitly marking uncertainty
- Content rules:
  - Prefer concrete descriptions of what a query returns and how it is used
  - If the dashboard JSON does not contain a piece of information, mark it as **Unknown** and explain how to obtain it (don’t hallucinate)

---

## 4. Required Inputs

### 4.1 User-Provided Inputs
Inputs that must be collected from the user before proceeding:

**Mandatory:**
- Product Name: Official product name to document
- ADX Dashboard JSON: The ADX dashboard export as a JSON file, or the raw JSON content
- Dashboard/Report Link: URL (or internal link) to the dashboard being documented

**Optional:**
- Product Description: Short description of the product; if omitted, the agent may attempt a best-effort description from local docs or user context
- Product Abbreviations/Acronyms: If omitted, the agent should list abbreviations observed in the dashboard (query/table names, metric prefixes) and leave unknown items blank
- Scope guidance: What to prioritize (e.g., “only queries in tab X”, “focus on reliability metrics”, “exclude deprecated tiles”)

### 4.2 Agent-Gathered Inputs
Inputs the agent must derive from the provided dashboard JSON (or workspace context) before writing:

**Mandatory:**
- Query inventory: Unique list of queries used by the dashboard (including reused queries)
- Per-query metadata: Query name (or generated stable name), tile(s) using it, and a short description of intent
- KQL text: The full KQL for each query
- Best-effort output schema: Column names and likely types/roles inferred from the KQL and visualization bindings

**Optional:**
- Example formats: Time formats (e.g., `yyyy-MM-dd`), ID patterns, common value domains (if visible in JSON)
- Category/Area: Derived from dashboard folder/tab/tile names, or explicit metadata if present

Inputs may come from:
- Local files in current workspace (the JSON export and any adjacent docs)
- Built-in file reading and parsing capabilities

---

## 5. Data Requirements
Detail the structured data the agent must extract from the dashboard JSON.

- **Name**: `dashboard_metadata`
  - **Description**: High-level dashboard identity for documentation context
  - **Source Preference**: Dashboard JSON
  - **Fields Needed**: Dashboard title/name, tabs/pages, tile names, any embedded links
  - **Update cadence**: Current export

- **Name**: `queries`
  - **Description**: Canonical query list and mappings to tiles/visuals
  - **Source Preference**: Dashboard JSON
  - **Fields Needed**: Query text (KQL), query identifier/name if present, parameters, time filters, referenced tables
  - **Update cadence**: Current export

- **Name**: `query_result_schema`
  - **Description**: Best-effort output schema for each query, enabling downstream cohort analysis
  - **Source Preference**: Infer from KQL (e.g., `project`, `extend`, `summarize`, `join`) + visualization bindings
  - **Fields Needed**: Column names, likely type (if inferable), format/example (if inferable), notes, IsAnalysisDimension
  - **Update cadence**: Current export

- **Name**: `analysis_dimensions`
  - **Description**: Candidate fields for slicing/breakdowns (cohorts)
  - **Source Preference**: Derived from grouping keys in `summarize by`, binning, and categorical fields used in charts
  - **Fields Needed**: Dimension column names, why they are dimensions, and typical usage
  - **Update cadence**: Current export

---

## 6. Tool Dependencies
Tool Dependencies:
- (none)

---

## 7. Fallback Plan
Explain how to proceed when the dashboard JSON is missing, incomplete, or does not contain query text.

**Detection Logic:**
- Dashboard JSON missing or unreadable: file cannot be opened or JSON parse fails
- Query text absent: no KQL found for any tile/data source
- Schema cannot be inferred: query text present but result columns are not determinable (e.g., dynamic projection or external function)

**Alternative Approaches:**
- Ask the user to export the dashboard again including query definitions (or provide the workbook/dashboard definition that contains KQL)
- Ask for the ADX cluster/database and a small set of sample query outputs (CSV or screenshot) to derive schema

**User Questions for Missing Data:**
1. “Can you provide the ADX dashboard JSON export that includes the underlying KQL queries?”
2. “If queries are stored separately, can you share the KQL files or the query library they reference?”
3. “Do you have a sample result for each query (first 10 rows) so I can document schema and formats accurately?”

**Minimal Data Requirements:**
- At least 1 dashboard link and product name
- At least 3 queries with KQL text
- At least 1 query with clearly projected columns

---

## 8. Section Structure
Define the exact sections and structure of the output.

### Structure:
1. **Azure Data Explorer (ADX) Dashboard (Telemetry) Knowledge**
   1. **Overview**
      - Product Overview
   2. **Queries**
      - One subsection per query

Each section MUST be generated exactly as structured in Section 12.

---

## 9. Detailed Section Requirements

### Section: Overview → Product Overview
- Objective: Provide product context for interpreting telemetry
- Required elements:
  - Product name
  - Product description (or **Unknown**)
  - Abbreviations list (or **Unknown**)

### Section: Queries → Query: <NAME>
For EACH query used by the dashboard, provide:
- Query Name
- Description (what it measures and why it exists)
- Category/Area (derived from dashboard structure; if unavailable, use **Unknown**)
- Dashboard/Report link (the user-provided dashboard link)

#### KQL Query
- Must include the full query as a fenced `kql` block
- Preserve original formatting where possible
- If the query is parameterized, document parameters in-line in the description (do not invent defaults)

#### Query Result Schema
- Provide a table with columns:
  - Column
  - Type
  - Format / Example
  - Notes
  - IsAnalysisDimension

#### Query Filters
For EACH filter defined as varibale in the query, provide: 
- Filter Name
- Description 
- Values and Default Values
- IsAnalysisDimension

**Schema inference rules (do not hallucinate):**
- Prefer columns explicitly created or selected via: `project`, `project-away`, `extend`, `summarize by`, `join` keys, `bin()` results.
- If types are explicit (e.g., `todatetime()`, `toint()`, `tostring()`), use those.
- If types are not explicit, infer conservatively:
  - `*Time*`, `Timestamp`, `Date*` → `datetime` (if used in time operations) else **Unknown**
  - IDs/keys used in joins → likely `string` unless casted
  - `count`, `dcount`, `sum`, `avg` results → `long`/`real` depending on function/casts (or **Unknown**)
- If the query output is dynamic/unbounded (e.g., `bag_unpack`, `dynamic` projections), mark Type as **Unknown** and explain.

**IsAnalysisDimension rules:**
- Mark **Yes** for filters that are:
  - Used in `summarize ... by <field>`
  - Used as categorical axes/legends in visuals (if identifiable)
  - Boolean/enum flags (scenario/experiment/status)
  - Stable categorical columns suitable for slicing
- Mark **No** for:
  - High-cardinality IDs (userId/sessionId/traceId) unless explicitly used for cohort slicing
  - Metric/value columns (counts, rates, durations)
  - Primary timestamps (still critical, but not a cohort dimension by default)

#### Key Usage Patterns
- Provide 2–5 bullets describing typical analysis usage, for example:
  - Breakdowns by key dimensions (region, SKU, scenario, internal/external)
  - Trend analysis over time (daily/weekly)
  - How to interpret spikes/drops
- If a query is meant to be filtered (time range, environment), document that.

---

## 10. Task Planning Rules for Agent
For this spec, the agent must do the following tasks:
1. Validate that mandatory inputs are present (product name, dashboard link, dashboard JSON)
2. Parse the dashboard JSON and identify:
   - tiles/pages and their names
   - data sources and embedded KQL queries
3. Deduplicate and normalize queries:
   - If multiple tiles share identical KQL, document it once and list all tile names in the Description
   - If a query lacks a name, generate a stable name derived from the tile name (e.g., `TileName - Query`)
4. For each query:
   - Write a description of purpose
   - Extract KQL into the `kql` code block
   - Infer output schema conservatively; mark unknowns explicitly
   - Identify analysis dimensions and usage patterns
5. Ensure the final document matches Section 12 formatting exactly
6. Perform self-review against Quality Checklist

---

## 11. Quality Checklist
The final content MUST satisfy all criteria:

### Structure
- Uses the exact heading structure and ordering from Section 12
- Contains Overview and Queries sections
- Contains one query subsection per unique query

### Content Quality
- No invented dashboard links, query names, KQL, or schema
- Descriptions are specific (what it measures and why), not generic
- Schema tables list real columns from the query (or explicitly mark unknowns)

### Completeness
- Documents all queries referenced by the dashboard JSON (or explicitly states what could not be found)
- Includes at least 2 usage pattern bullets per query (unless query is too opaque; then explain)

### Technical Accuracy
- KQL is copied verbatim from JSON
- Inferred types are justified by explicit casts or usage; otherwise set to **Unknown**
- IsAnalysisDimension flags follow the rules in Section 9

If any criteria fail → revise before final output.

---

## 12. Final Output Format
The final output **MUST** be delivered as a markdown document following this exact structure:

```markdown
{{adx_telemetry_knowledge_template.md}}
```
