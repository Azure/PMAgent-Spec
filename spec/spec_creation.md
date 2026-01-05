# Spec: Custom Spec Creation (Template-Driven)
Version: 1.0
Content-Type: markdown
Authoring-Mode: ai

---

## 1. Purpose
This spec instructs the agent to collect all inputs needed to author a new PMAgent-ready spec with template, validate completeness, and then generate the final spec strictly following that template. Work in two phases: gather/confirm inputs first, then draft only after mandatory details are satisfied.

---

## 2. Audience
- Primary audience: PMs, doc writers, enablement owners requesting a new spec.
- Secondary audience: AI agents orchestrating spec creation.
- Expertise level: Intermediate-Advanced.
- Expected reading context: Markdown files in repos, PRs, or internal docs.

---

## 3. Tone & Style Guidelines
- Voice: Directive, concise, professional.
- Point of view: Neutral/second-person when asking questions; neutral third-person in the final spec.
- Reading level: Professional; assume PM/engineer familiarity.
- Prohibited styles: Marketing hype, filler, generic instructions without specifics, hallucinated tool names.
- Examples: Offer short, concrete examples when clarifying options (e.g., section names, data signals).

---

## 4. Required Inputs

### 4.1 User-Provided Inputs
**Mandatory before drafting:**
- Spec metadata: `spec_name`, `content_type` (markdown/json/etc.), desired version (default 1.0)t.
- Purpose and deliverable description.
- Audience profile: primary/secondary audiences, expertise level, reading context.
- Tone & style rules: voice, POV, reading level target, prohibited styles, examples.
- Required inputs for the new spec:
  - Mandatory user-provided inputs for the target deliverable.
  - Optional user-provided inputs and defaults when missing.
  - Mandatory agent-gathered inputs and their purpose.
  - Optional agent-gathered inputs and defaults when missing.
- Data requirements for the target deliverable (see Section 5 structure).
- Tool dependencies list (tool spec filenames under `tool_specs/`).
- Fallback plan preferences and acceptable manual overrides.
- Section structure for the target deliverable plus section names/headings.
- Per-section requirements: objectives, required elements, mandatory details, citation/verification rules, expected length.
- Quality checklist items specific to the new spec.
- Final output format: markdown skeleton/JSON schema/plain text; if markdown, confirm exact heading skeleton.

**Optional (collect if available):**
- Examples of "good"/"bad" outputs for the target deliverable.
- Links to existing docs/dashboards/repos that should inform the spec.
- Default time windows, scopes, or filters to bake into data requirements.
- Known constraints (security, privacy, compliance) that must be reflected.

### 4.2 Agent-Gathered Inputs
**Mandatory:**
- Extract implicit signals from the user prompt/history (e.g., target product, data sources, preferred tools).
- Detect contradictions or gaps across provided inputs.

**Optional:**
- Review user-provided files/links for terminology or section patterns when explicitly shared.
- Suggest default assumptions only when the user agrees; mark them as defaults.

Inputs may come from conversation context or explicitly shared local files; do not assume access to external systems.

---

## 5. Data Requirements
Capture structured requirements for the new spec before drafting:

- **`spec_metadata`**  
  - Category: User-provided  
  - Description: Name, content type, version, authoring mode.  
  - Source Preference: User confirmation.  
  - Filters: N/A  
  - Fields Needed: `name`, `content_type`, `version`, `authoring_mode`.  
  - Update cadence: Static for the spec version.

- **`purpose_statement`**  
  - Category: User-provided  
  - Description: What the spec produces and why.  
  - Source Preference: User-provided text.  
  - Filters: Keep concise (3-6 lines).  
  - Fields Needed: Goal, scope, expected output.  
  - Update cadence: Static.

- **`audience_profile`**  
  - Category: User-provided  
  - Description: Primary/secondary audience, expertise, reading context.  
  - Source Preference: User; infer from links only if confirmed.  
  - Fields Needed: audience roles, expertise level, context.  
  - Update cadence: Static.

- **`tone_style_rules`**  
  - Category: User-provided  
  - Description: Voice, POV, reading level, prohibited styles, examples.  
  - Source Preference: User.  
  - Fields Needed: voice, POV, reading level, prohibited styles, sample phrases/examples.  
  - Update cadence: Static.

- **`input_matrix`**  
  - Category: User-provided  
  - Description: Mandatory/optional user inputs and agent-gathered inputs for the target deliverable.  
  - Source Preference: User + confirmation.  
  - Fields Needed: input name, type (user/agent), mandatory vs optional, purpose, default behavior if missing.  
  - Update cadence: Static.

- **`data_signals`**  
  - Category: Mixed  
  - Description: Structured signals the agent must gather (names, sources, filters, fields, freshness).  
  - Source Preference: User for required signals; agent can propose defaults but must confirm.  
  - Fields Needed: name, category (`User-provided` or `Agent-derivable`), description, source preference (tool or manual), filters, fields needed, update cadence.  
  - Update cadence: As defined per signal.

- **`tool_dependencies`**  
  - Category: User-provided  
  - Description: Tool spec filenames needed to satisfy data collection.  
  - Source Preference: User; validate names exist under `tool_specs`.  
  - Fields Needed: tool name, optional/required flag.  
  - Update cadence: Static.

- **`fallback_rules`**  
  - Category: User-provided  
  - Description: Detection logic, alternate tools, user questions, minimal data.  
  - Source Preference: User; agent can suggest defaults for confirmation.  
  - Fields Needed: failure conditions, alternatives, user questions, minimal dataset.  
  - Update cadence: Static.

- **`section_blueprint`**  
  - Category: User-provided  
  - Description: Ordered list of final deliverable sections.  
  - Source Preference: User; agent can propose for confirmation.  
  - Fields Needed: section name, ordering, brief content notes.  
  - Update cadence: Static.

- **`section_requirements`**  
  - Category: User-provided  
  - Description: Per-section objectives, required elements, mandatory details, citation rules, expected length.  
  - Source Preference: User; agent can propose defaults for confirmation.  
  - Update cadence: Static.

- **`quality_checklist`**  
  - Category: User-provided  
  - Description: Structure/content/tone checks for final deliverable.  
  - Source Preference: User; agent can provide defaults.  
  - Update cadence: Static.

- **`output_format`**  
  - Category: User-provided  
  - Description: Delivery format and skeleton (markdown/JSON/plain text).  
  - Source Preference: User; default to markdown.  
  - Fields Needed: format, skeleton, required headings/fields.  
  - Update cadence: Static.

---

## 6. Tool Dependencies

Tool Dependencies:
- (none; rely on conversation context and provided files)

---

## 7. Fallback Plan
- Detect gaps: missing mandatory inputs (Section 4), undefined data signals, missing section structure, or conflicting instructions.
- Clarify: ask targeted questions grouped by topic (metadata, audience, tone, inputs, data signals, tool dependencies, section list). Avoid drafting until mandatory fields are confirmed.
- Propose defaults: offer concise defaults for common spec types (e.g., report, README) but mark them as `[Default, user to confirm]`.
- Minimal dataset: require at least `spec_metadata`, `purpose_statement`, `audience_profile`, `tone_style_rules`, a first-pass `section_blueprint`, and one `section_requirements` entry before generating.
- If user declines details: deliver a skeleton spec using placeholders prefixed with `TODO:` and explicitly request follow-up inputs.

---

## 8. Section Structure
The final output MUST follow the spec exactly:

```markdown
{{spec_template.md}}
```

Do not add extra top-level sections; honor the numbering.

---

## 9. Detailed Section Requirements
- **Section: Spec Header**  
  - Objective: Provide name/version/content type (and optional Authoring-Mode).  
  - Expected length: 2-4 lines.  
  - Required elements: Title line, version, content type; include Authoring-Mode if provided.  

- **Section: Purpose**  
  - Objective: Explain what the target deliverable is and its expected output.  
  - Expected length: 3-6 sentences or bullets.  
  - Mandatory details: Scope, intended outcome, what "good" looks like.

- **Section: Audience**  
  - Objective: Identify who will read/use the deliverable.  
  - Expected length: Short bullets.  
  - Mandatory details: Primary/secondary audiences, expertise level, reading context.

- **Section: Tone & Style Guidelines**  
  - Objective: Capture voice/POV/reading level and banned styles.  
  - Expected length: Bullets.  
  - Mandatory details: Voice, POV, reading level, prohibited styles, examples if provided.

- **Section: Required Inputs**  
  - Objective: Enumerate mandatory/optional inputs from user and agent.  
  - Expected length: Bullets under 4.1 and 4.2.  
  - Mandatory details: Input name, description/purpose, default behavior if missing (for optional).

- **Section: Data Requirements**  
  - Objective: List structured signals needed to satisfy the deliverable.  
  - Expected length: Bulleted entries with the fields from Section 5.  
  - Mandatory details: Name, category, description, source preference, filters, fields needed, update cadence.

- **Section: Tool Dependencies**  
  - Objective: Name required tool specs.  
  - Expected length: Short list.  
  - Mandatory details: Tool names with optional/required flag.

- **Section: Fallback Plan**  
  - Objective: Define detection, alternatives, questions, and minimal dataset when tools/data are missing.  
  - Expected length: 4-8 bullets.  
  - Mandatory details: Detection logic, alternative sources, user questions, minimal data to continue.

- **Section: Section Structure**  
  - Objective: Provide the ordered headings for the target deliverable.  
  - Expected length: Numbered list.  
  - Mandatory details: Section names and any nested sub-sections.

- **Section: Detailed Section Requirements**  
  - Objective: For each section from Section Structure, state objective, expected length, required elements, mandatory details, citation/verification rules.  
  - Expected length: Sub-section per section, 3-6 bullets each.

- **Section: Quality Checklist**  
  - Objective: Define structure/content/tone checks the final deliverable must pass.  
  - Expected length: Bullets grouped by Structure/Content/Tone.  
  - Mandatory details: Clear pass/fail criteria; note that failure requires revision.

- **Section: Final Output Format**  
  - Objective: Specify delivery format and skeleton.  
  - Expected length: Short paragraph plus fenced skeleton if markdown.  
  - Mandatory details: Format type, exact heading skeleton, any special delivery instructions.

---

## 10. Quality Checklist
- Structure: All template sections (1-11) present, ordered, and populated; headings match `spec_template.md`.
- Inputs: All mandatory inputs collected/confirmed; optional inputs handled with defaults or TODO markers.
- Content: No placeholders left unmarked; required fields for each data signal captured.
- Tone: Follows Section 3 rules; no filler, no hallucinated tools or data.
- Final format: Matches chosen format skeleton; numbering and subheadings consistent.

---

## 11. Final Output Format
- Deliver a Markdown spec following the exact skeleton from Section 8.  
- Include fenced code block skeleton if the user requested one; otherwise write the filled spec directly.  
- If data is missing, include `TODO:` markers and a short follow-up questions list beneath the relevant sections.

---
