# Spec: <SPEC_NAME>
Version: 1.0
Content-Type: <content type>
Authoring-Mode: <human|ai|hybrid>

---

## 1. Purpose
Describe what this spec is for, what type of content it defines, and the expected output.

---

## 2. Audience
- Primary audience:
- Secondary audience:
- Expertise level:
- Expected reading context (email, web, PDF, doc, etc.):

---

## 3. Tone & Style Guidelines
- Voice (e.g., formal, expert, friendly, PM-style, executive-summary)
- Point of view (e.g., first-person, third-person)
- Reading level target
- Prohibited styles
- Examples (optional)

---

## 4. Required Inputs

### 4.1 User-Provided Inputs
Inputs that must be collected from the user before proceeding:

**Mandatory:**
- <Input name>: <Description and purpose>
- <Input name>: <Description and purpose>

**Optional:**
- <Input name>: <Description, purpose, and default behavior if not provided>
- <Input name>: <Description, purpose, and default behavior if not provided>

### 4.2 Agent-Gathered Inputs
Inputs the agent must collect via tools or retrieval before writing:

**Mandatory:**
- <Input name>: <Description and purpose>
- <Input name>: <Description and purpose>

**Optional:**
- <Input name>: <Description, purpose, and default behavior if not provided>
- <Input name>: <Description, purpose, and default behavior if not provided>

Inputs may come from:
- Built-in tools for GitHub Copilot VS Code.
- MCP tools (GitHub, SharePoint, DB, API, etc.)
- Large Language Model tools for GitHub Copilot VS Code.
- Context/State (extract from conversation or previous state)
- Local files (files in current workspace)

---

## 5. Data Requirements
Detail the structured data the agent must gather (beyond user inputs) before writing.

For each requirement include:
- **Name**: Short identifier for the signal (e.g., `merged_prs_last_week`).
- **Description**: What insight it provides and why it matters for the spec.
- **Source Preference**: Which MCP server/toolset should be used (e.g., `GitHub MCP – pull_requests`).
- **Filters**: Time windows, labels, states, or repo scopes to apply.
- **Fields Needed**: Exact attributes (title, number, merged_at, labels, reviewers, etc.).
- **Update cadence**: How fresh the data must be.

---

## 6. Tool Dependencies
List the tool spec filenames (matching `tool_specs/<name>.yml`) that this spec expects the host to load before planning.

Format the section as:

```
Tool Dependencies:
- github
- azure_devops (optional)
```

Guidelines:
- Tool names must match files under `tool_specs/<tool>.yml`.
- Keep the list limited to tool names; do **not** restate capability details.
- Agents must call `get_tool_manifest('<tool>')` for each required tool to inspect capabilities, helpers, and fallbacks.
- If a dependency is optional, label it `(optional)` in the list.

---

## 7. Fallback Plan
Explain how to proceed when the recommended MCP server/tool call is unavailable, errors out, or returns insufficient data.

Outline:
- Detection logic (e.g., `github` server missing, tool not in `available_tools`, response empty).
- Alternative MCP servers/tools, if any.
- Exact questions to ask the user to manually provide the missing signals.
- Minimal data needed from the user to continue.

---

## 8. Section Structure
Define the exact sections and structure of the output.

### Example Structure:
1. **Title**
2. **Introduction**  
   - Purpose  
   - Context  
3. **Main Sections**  
   - <Section Name>  
     - Required content  
     - Required examples  
4. **Conclusion / Recommendations**
5. **Appendix (optional)**

Each section MUST be generated exactly as structured here.

---

## 9. Detailed Section Requirements
### Section: <Section Name>
- Objective:
- Expected length:
- Required elements:
- Mandatory details:
- If referencing external sources:
  - Required citation form:
  - Required verification steps:

(Repeat for each section)

---

## 10. Task Planning Rules for Agent
For this spec, the agent must do the following tasks:
1. Identify missing inputs  
2. For each missing input, choose a tool or ask user  
3. Retrieve resources  
4. Summarize and normalize materials  
5. Fill in the sections in order  
6. Perform self-review against Quality Checklist  
7. Rewrite if criteria fail

---

## 11. Quality Checklist
The final content MUST satisfy all criteria:

### Structure
- All required sections included  
- Section order is correct  
- Formatting follows this spec exactly  

### Content Quality
- Content is accurate  
- Examples are relevant  
- No missing mandatory fields  
- No hallucinations

### Tone
- Tone follows section 3  
- No contradictions  
- No filler or redundancy  

If any criteria fail → revise before final output.

---

## 12. Final Output Format
Specify how the final output must be delivered:
- Markdown template  
- JSON schema  
- Plain text hierarchy  
- HTML  

If Markdown:  
Provide an exact skeleton:

```markdown
# <Title>

## Introduction
<content>

## <Section Name>
<content>

## Conclusion
<content>
