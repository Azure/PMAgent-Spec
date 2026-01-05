# Spec: Power BI Telemetry Knowledge Documentation
Version: 1.0
Content-Type: technical-documentation
Authoring-Mode: hybrid

---

## 1. Purpose
This spec defines how to create comprehensive Power BI telemetry knowledge documentation that serves as a reference for understanding semantic models, OKRs, and data relationships within Power BI environments. The expected output is a structured markdown document that enables stakeholders to understand telemetry data sources, metrics calculations, and analysis patterns.

---

## 2. Audience
- Primary audience: Data analysts, product managers, and engineers working with Power BI telemetry
- Secondary audience: Leadership teams reviewing OKR metrics and business stakeholders
- Expertise level: Intermediate to advanced technical knowledge of Power BI and data analysis
- Expected reading context: Documentation reference, web-based knowledge base, technical specifications

---

## 3. Tone & Style Guidelines
- Voice: Technical, precise, and instructional
- Point of view: Third-person objective documentation style
- Reading level target: Technical professional (assumes familiarity with Power BI concepts)
- Prohibited styles: Conversational tone, marketing language, ambiguous statements
- Examples: Include concrete examples for table schemas, DAX measures, and filter expressions

---

## 4. Required Inputs

### 4.1 User-Provided Inputs
Inputs that must be collected from the user before proceeding:

**Mandatory:**
- Product Name: Official name of the product being documented
- Dashboard/Report Links: URLs to relevant Power BI dashboards or reports which could link to Semantic Model.

**Optional:**
- Specific OKR Names: If targeting specific OKRs, provide their names and priorities
- Analysis Timeframes: Default time windows for analysis (defaults to last 6 months if not provided)

### 4.2 Agent-Gathered Inputs
Inputs the agent must collect via tools or retrieval before writing:

**Mandatory:**
- Product Abbreviations: Common abbreviations or acronyms used for the product. Comes from web search. 
- Semantic Model Name: Name of the Power BI semantic model.
- Semantic Model Schema: Complete table structures, columns, data types, and relationships
- Existing Measures: DAX measures, calculations, and their purposes
- Table Relationships: Foreign keys, cardinality, and join patterns
- OKR Definitions: Current OKRs, their targets, and calculation methodologies

**Optional:**
- Product Description: Brief description of the product's purpose and functionality. Come from web search.
- Historical OKR Performance: Past performance data for context
- Common Analysis Patterns: Frequently used breakdowns and dimensions
- Filter Patterns: Standard filters applied across analyses

Inputs may come from:
- Power BI MCP tools for schema inspection and measure definitions
- SharePoint or documentation repositories for existing OKR definitions
- Team knowledge bases or wikis for analysis patterns
- Direct Power BI semantic model inspection via available tools

---

## 5. Data Requirements
Detail the structured data the agent must gather (beyond user inputs) before writing.

For each requirement include:
- **Name**: `semantic_model_schema`
- **Description**: Complete schema including all tables, columns, data types, and measures within the Power BI semantic model
- **Source Preference**: Power BI MCP server - schema inspection tools
- **Filters**: Focus on active tables and measures, exclude deprecated or unused elements
- **Fields Needed**: Table names, column names, data types, relationships, measure definitions, descriptions
- **Update cadence**: Schema must be current within 7 days

- **Name**: `okr_definitions`
- **Description**: Formal OKR definitions including targets, calculation methods, and measurement windows
- **Source Preference**: SharePoint MCP or local files containing OKR documentation
- **Filters**: Active OKRs for current quarter/year
- **Fields Needed**: OKR names, descriptions, targets, formulas, time semantics, scope filters
- **Update cadence**: Must reflect current quarter's OKRs

- **Name**: `analysis_dimensions`
- **Description**: Columns and fields commonly used for cohort analysis and data slicing
- **Source Preference**: Power BI MCP - column metadata and usage patterns
- **Filters**: Columns marked as dimensions or frequently used in breakdowns
- **Fields Needed**: Column names, cardinality, common values, analysis usage patterns
- **Update cadence**: Updated monthly or when new analysis patterns emerge

---

## 6. Tool Dependencies
Tool Dependencies:
- powerbi
- github (optional)
- web (optional)

---

## 7. Fallback Plan
Explain how to proceed when the recommended MCP server/tool call is unavailable, errors out, or returns insufficient data.

**Detection Logic:**
- If `powerbi` server missing or returns empty schema: Detect via empty response from schema inspection calls
- If OKR definitions unavailable: Check for empty responses from documentation sources
- If measure definitions incomplete: Validate against expected measure count or required measures list

**Alternative Approaches:**
- Manual schema inspection: Ask user to provide Power BI .pbix file or manual schema export
- Documentation review: Request existing documentation files or screenshots of schema
- Guided collection: Present structured questions to collect table/column information interactively

**User Questions for Missing Data:**
1. "Please provide the table names and their primary purposes in your Power BI model"
2. "What are the key measures (KPIs) calculated in your model and their DAX formulas?"
3. "Which columns are typically used for filtering and grouping in your analyses?"
4. "What are your current OKRs and their target values?"

**Minimal Data Requirements:**
- At least 3-5 main tables with their primary columns
- 2-3 key measures with basic calculation logic
- 1-2 OKRs with target definitions
- Basic relationship information between main tables

---

## 8. Section Structure
Define the exact sections and structure of the output.

### Structure:
1. **Power BI Semantic Model Schema Knowledge**
   1.1. **Overview**
       - Product Overview
       - Power BI Semantic Model Schema Overview
   1.2. **Semantic Model Schema**
       - Table documentation (one subsection per table)
   1.3. **Entity Relationships (Conceptual)**

2. **OKR(KR) Knowledge**
   2.1. **Overview**
   2.2. **OKRs** (one subsection per OKR)

3. **Notes and Conventions**

Each section MUST be generated exactly as structured here.

---

## 9. Detailed Section Requirements

### Section: Overview
- Objective: Provide high-level context about the product and its Power BI implementation
- Expected length: 2-3 paragraphs per subsection
- Required elements: Product name, description, abbreviations, semantic model name, dashboard links
- Mandatory details: Direct links to dashboards, complete table list with purposes

### Section: Semantic Model Schema
- Objective: Document detailed table structures, columns, measures, and usage patterns
- Expected length: 1-2 pages per major table
- Required elements: Column specifications table, measures table, key usage patterns
- Mandatory details: Data types, IsAnalysisDimension flags, measure formulas, relationship descriptions
- Required citation form: Direct references to Power BI objects using standard notation (Table[Column])

### Section: Entity Relationships
- Objective: Explain conceptual relationships between tables
- Expected length: 1-2 paragraphs
- Required elements: Foreign key relationships, cardinality descriptions
- Mandatory details: Direction of relationships, join conditions

### Section: OKR Knowledge
- Objective: Document OKR calculations, targets, and analysis approaches
- Expected length: 1-2 pages per OKR
- Required elements: Time semantics, telemetry scope, calculation logic, targets, recommended breakdowns
- Mandatory details: Exact filter expressions, metric formulas, target values, measurement windows
- Required verification steps: Validate formulas against actual Power BI measures

---

## 10. Task Planning Rules for Agent
For this spec, the agent must do the following tasks:
1. Collect product information from user inputs
2. Inspect Power BI semantic model schema using available tools
3. Gather OKR definitions from documentation sources or user input
4. Map relationships between tables and identify key dimensions
5. Document each table following the specified format
6. Create OKR documentation with calculation details
7. Generate usage patterns and analysis recommendations
8. Perform quality validation against checklist
9. Format final output according to markdown template

---

## 11. Quality Checklist
The final content MUST satisfy all criteria:

### Structure
- All required sections included in correct order
- Each table documented with columns, measures, and usage patterns
- OKRs include complete calculation methodology
- Proper markdown formatting with consistent heading levels

### Content Quality
- All table schemas accurately reflect Power BI model
- Measure formulas are syntactically correct DAX
- OKR calculations are mathematically sound
- No references to non-existent tables or columns
- IsAnalysisDimension flags are properly assigned

### Completeness
- All major tables documented (minimum 80% coverage)
- Key measures include DAX formulas
- OKRs include targets and measurement windows
- Relationships section explains major join patterns
- Usage patterns provide actionable guidance

### Technical Accuracy
- Column data types are correct
- Relationship cardinalities are accurate
- Filter expressions use proper Power BI syntax
- Time semantic definitions are precise and unambiguous

If any criteria fail → revise before final output.

---

## 12. Final Output Format
The final output **MUST** be delivered as a markdown document following this exact structure:

```markdown
{{powerbi_telemetry_knowledge_template.md}}
```
