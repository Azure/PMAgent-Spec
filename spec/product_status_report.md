
# **Spec: Product Status Report**

Version: 1.0
Content-Type: markdown
Authoring-Mode: ai

---

## **1. Purpose**

This spec defines the structure and requirements for generating a **Product Status Report**.
The report summarizes the current state of a product or release, including progress, risks, dependencies, bugs, engineering health, and next steps.
The expected output is a clear, concise, data-backed status update suitable for leadership and engineering stakeholders.

---

## **2. Audience**

* **Primary audience:** Product managers, engineering leads, program managers
* **Secondary audience:** Executives, cross-functional partners
* **Expertise level:** Intermediate–Expert
* **Expected reading context:** Email, markdown wiki (GitHub/DevOps), PDF exports, dashboards

---

## **3. Tone & Style Guidelines**

* **Voice:** Professional, concise, objective, PM-style
* **Point of view:** Third-person
* **Reading level:** Mid-level professional (no jargon without explanation)
* **Prohibited styles:**

  * Narrative storytelling
  * Speculation or guesses
  * Overly casual language
  * Excessive adjectives
* **Examples:**

  * Good: “Feature A is 72% complete and on track.”
  * Bad: “Looks like Feature A is probably almost done!”

---

## **4. Required Inputs**

### **4.1 User-Provided Inputs**
Inputs that must be collected from the user before proceeding:

**Mandatory:**
- Product name: Name of the product or project
- Reporting period: One of the following:
  - Iteration/Sprint name (e.g., `2025/Q1`, `Sprint 42`)
  - Date range (e.g., `2025-01-01` to `2025-01-31`)
  - Release identifier (branch, tag, or version)

**Optional:**
- Area Path: Azure DevOps area path for filtering work items (e.g., `Product/SDK`)
- Team name: Specific team to report on
- Custom filters: Additional work item queries or tags
- Output file path: Where to save the generated report
- Report focus: Specific features or areas to emphasize

### **4.2 Agent-Gathered Inputs**
Inputs the agent must collect via tools or retrieval before writing:

**Mandatory:**
- Work items for the reporting period:
  - Epics, Features, Stories, Tasks by type
  - Work item states and completion status
  - Work item owners and assignments
- Feature progress metrics:
  - Planned vs completed work items
  - Completion percentages per feature
  - Story/task burndown data
- Bug data:
  - Bug count by severity (Critical, High, Medium, Low)
  - Bug status (Active, Resolved, Closed)
  - Bug owners and age
  - Bug trends (increasing/decreasing)

**Optional:**
- Pull requests merged in the reporting period:
  - PR count, titles, and merge dates
  - PR authors and reviewers
- Dependency information:
  - Internal/external dependencies
  - Dependency status and owners
  - Blocked items
- Build/test/CI health metrics:
  - Build success rate
  - Test pass/fail rates
  - Code coverage metrics
  - Performance indicators
- Release goals and timeline from project documentation
- Risk and blocker information from work items or comments
- Previous report data for trend analysis

Inputs may come from:
- Built-in tools for GitHub Copilot VS Code
- MCP tools (GitHub MCP for PRs/commits, Azure DevOps MCP for work items, SharePoint for documentation)
- Large Language Model tools for GitHub Copilot VS Code
- Context/State (extract from conversation or previous state)
- Local files (files in current workspace)
- Internal APIs for build/test metrics

---

## **5. Section Structure**

The Output MUST follow this exact structure:

1. **Title**
2. **Executive Summary**

   * Current status
   * High-level trends
   * Overall health (Green / Yellow / Red)
3. **Feature Progress Overview**

   * Feature completion table
   * Narrative summary
4. **Completion Metrics**

   * Story/task progress
   * Burndown or completion overview
5. **Dependency Status**

   * Table of dependencies
   * Risks or delays
6. **Bug / Issue Summary**

   * Severity counts
   * Trend analysis
   * Table of key bugs
7. **Risks & Blockers**

   * Description
   * Impact
   * Mitigation plan
8. **Engineering Health (optional)**

   * Build quality
   * Test results
   * Performance or reliability indicators
9. **Forecast & Next Steps**

   * Expected timeline
   * Priorities for next iteration
10. **Appendix (optional)**

    * Raw data summaries
    * PR lists
    * Work item lists

---

## **6. Detailed Section Requirements**

### **Section: Title**

* **Objective:** Provide a clear report title.
* **Expected length:** 1 line
* **Required elements:** Product name + iteration or release
* **Mandatory details:** Version or date
* **External sources:** None

---

### **Section: Executive Summary**

* **Objective:** Summarize overall product health and major changes.
* **Expected length:** 3–5 sentences
* **Required elements:**

  * Health indicator (Green/Yellow/Red)
  * Biggest risks or progress highlights
  * High-level trends
* **Mandatory details:** No assumptions; must be backed by inputs.

---

### **Section: Feature Progress Overview**

* **Objective:** Communicate feature completion status.
* **Expected length:** Table + short paragraph
* **Required elements:**

  * Feature name
  * Owner
  * Progress %
  * Status (On Track / At Risk / Blocked)
  * Notes
* **Mandatory details:** Must compute completion % from work items.

---

### **Section: Completion Metrics**

* **Objective:** Quantify overall progress.
* **Expected length:** 2–4 bullet points
* **Required elements:**

  * Planned vs completed work
  * Story/task burndown or equivalent
* **If referencing external sources:** Validate numerical consistency.

---

### **Section: Dependency Status**

* **Objective:** Show health of external/internal dependencies.
* **Expected length:** Table
* **Required elements:**

  * Dependency name
  * Owner
  * Status
  * Risk level
  * Notes

---

### **Section: Bug / Issue Summary**

* **Objective:** Give an accurate picture of product quality.
* **Expected length:** Table + 1–2 paragraphs
* **Required elements:**

  * Bug count by severity
  * Trend (increasing/decreasing)
  * Key bug details
* **Mandatory details:** Severity must be taken from source.

---

### **Section: Risks & Blockers**

* **Objective:** Identify threats to delivery.
* **Expected length:** List of 3–10 items
* **Required elements:**

  * Risk description
  * Impact
  * Mitigation plan
* **Mandatory details:** Must not fabricate risks.

---

### **Section: Engineering Health (Optional)**

* **Objective:** Show engineering stability.
* **Expected length:** Short list
* **Required elements:**

  * Build success rate
  * Test coverage or failures
  * Performance signal if available

---

### **Section: Forecast & Next Steps**

* **Objective:** Provide forward-looking guidance.
* **Expected length:** 4–6 bullet points
* **Required elements:**

  * Upcoming milestones
  * Prioritized work
  * Expected completion dates

---

### **Section: Appendix (Optional)**

* **Objective:** Provide raw supporting data.
* **Required elements:**

  * Work item exports
  * PR lists
  * Additional metrics

---

## **7. Task Planning Rules for Agent**

The agent MUST follow these rules:

1. Identify missing inputs.
2. For each missing input, choose a tool or ask the user.
3. Retrieve all work items, PRs, bugs, metrics, dependencies.
4. Normalize, summarize, and validate retrieved data.
5. Fill in each section **in the exact order shown in Section Structure**.
6. Perform self-review using the Quality Checklist.
7. Rewrite if any criteria fail.

---

## **8. Required Tools (MCP)**

* **GitHub MCP:**

  * Read repo files
  * Retrieve PRs, branches, commits
* **Azure DevOps MCP:**

  * Fetch work items, bugs, iterations, area paths
* **SharePoint MCP:**

  * Retrieve documents or supplementary context
* **Web Search (optional):**

  * Background research on standards or definitions
* **Custom internal tools:**

  * Build metrics
  * Test results
  * Dependency health APIs

---

## **9. Quality Checklist**

### **Structure**

* [ ] All required sections included
* [ ] Section order strictly followed
* [ ] Markdown formatting matches this spec

### **Content Quality**

* [ ] All metrics backed by real data
* [ ] No assumptions or hallucinations
* [ ] All tables fully populated
* [ ] All mandatory details included

### **Tone**

* [ ] Professional, concise, PM-style
* [ ] No exaggeration or emotional language
* [ ] No filler or redundancy

If anything fails → revise before delivering output.

---

## **10. Final Output Format**

The final output MUST be in **markdown** using this skeleton:

```markdown
# <Product Name> — Status Report (Iteration / Release)

## Executive Summary
<content>

## Feature Progress Overview
<content>

## Completion Metrics
<content>

## Dependency Status
<content>

## Bug / Issue Summary
<content>

## Risks & Blockers
<content>

## Engineering Health
<content>

## Forecast & Next Steps
<content>

## Appendix
<content>
```

---
