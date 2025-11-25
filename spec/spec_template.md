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

## 5. Section Structure
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

## 6. Detailed Section Requirements
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

## 7. Task Planning Rules for Agent
For this spec, the agent must do the following tasks:
1. Identify missing inputs  
2. For each missing input, choose a tool or ask user  
3. Retrieve resources  
4. Summarize and normalize materials  
5. Fill in the sections in order  
6. Perform self-review against Quality Checklist  
7. Rewrite if criteria fail

---

## 8. Required Tools (MCP)
List tools to use and what they provide:
- GitHub: read files, commit history, repo content  
- SharePoint: access documents and folders  
- SQL DB: retrieve metrics or logs  
- Web Search: background research  
- Custom tools: …

---

## 9. Quality Checklist
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

## 10. Final Output Format
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
