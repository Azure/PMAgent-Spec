# **Spec: Monday Minutes – Team Update**

Version: 1.0
Content-Type: markdown
Authoring-Mode: ai

---

## **1. Purpose**

This spec defines the structure and requirements for generating a **single team’s Monday Minutes update**.

Each team update is a self-contained section that can be aggregated into a broader Monday Minutes post. The update is structured around:

* A team/group header
* One or more **sub-areas** (e.g., Direct Models, Efficiency, MaaP)
* For each sub-area: **DRI, TLDR, Highlights, Risks + Blockers, Upcoming**

The expected output is a clear, concise weekly update that can be directly pasted into the Monday Minutes thread.

---

## **2. Audience**

* **Primary audience:** Org/area owners, product leaders, engineering managers, program managers
* **Secondary audience:** Cross-org partners, strategy & operations, leadership reviewers
* **Expertise level:** Intermediate–Expert in the domain
* **Reading context:** Internal GitHub/DevOps markdown threads, internal wikis, email digests

---

## **3. Tone & Style Guidelines**

* **Voice:** Professional, concise, factual, “status update” style
* **Point of view:** Third-person or neutral (“Team X shipped…”, “We delivered…”)
* **Reading level:** Mid-level professional; internal acronyms allowed if common
* **Priorities:**

  * Call out **what changed this week**, not background
  * Include **numbers / dates / concrete outcomes** where possible
* **Prohibited styles:**

  * Storytelling or narrative intros
  * Vague statements without content (“made good progress”)
  * Hype and marketing language
  * Casual jokes or fillers

**Example (good):**
“gpt-5.2 is on track for 12/9 release; capacity risk remains open pending GB200 allocation.”

**Example (bad):**
“Lots of exciting things happening and we’re feeling great about progress!”

---

## **4. Required Inputs**

### **4.1 Team-Provided Inputs (Mandatory)**

For each **team update**, the following must be provided:

* **Group name:**
  The logical team or area name shown as the top-level heading.
  Examples:

  * `GitHub Minutes`
  * `Foundry Models & Training`
  * `Agentic DevOps – Azure Developer CLI`

* **Sub-areas list:**
  One or more sub-areas within the group, each with:

  * Sub-area name (e.g., `Direct Models`, `Deployment templates`, `Efficiency`)
  * DRI (Directly Responsible Individual) for that sub-area
    * If not provided, **ask the user for the DRI before drafting**. If the user cannot provide it, use the primary author/owner from the week’s PRs/issues as a provisional DRI and label it clearly (e.g., `DRI (provisional): <name>`).

* **Per sub-area weekly content:**

  * TLDR (1–3 sentences)
  * Highlights (3–8 bullets)
  * Risks + Blockers (0–5 bullets, can be explicitly “None”)
  * Upcoming (2–6 bullets)

### **4.2 Optional Inputs**

* **Time**
  By default it should be only ONE week, the last week. But if the date is not very clear, ask user to clarify.

Per team or per sub-area:

* **Ships this week / Ships next week:**

  * Short lists of concrete ships or planned ships
* **Links:**

  * Release notes, dashboards, blog posts, design docs
* **Metrics:**

  * Usage numbers, capacity data, savings, traffic, or adoption metrics. These metrics may come from PowerBI dashboards (via the PowerBI MCP) or ADX (Kusto) queries executed through the ADO MCP. Provide dataset/workspace names or the query text + date window when requesting metrics so the agent can pull the right slices.

---

## **5. Data Requirements**

Monday Minutes should combine human-provided talking points with live engineering telemetry (see referenced tool specs) before drafting the update:

**Telemetry source selection:**

- If the user’s prompt explicitly asks for Azure DevOps (ADO) data—or references Boards, pipelines, or work items—load the `azure_devops` tool spec instead of (or in addition to) GitHub.
- When the user wants both sources, run both specs and merge the resulting signals per sub-area, calling out the origin (GitHub vs ADO) when helpful.
- If the user requests dashboard/scorecard metrics, load the `powerbi` tool spec and use the PowerBI MCP to fetch the figures (ask for workspace/report/dataset names or a saved view when unclear).
- If the user requests ADX/Kusto metrics, run the Kusto-capable tools in the ADO MCP (after calling `get_tool_manifest('azure_devops')`) with the provided query text/time window and label the source as Kusto/ADX.
- **Never issue unauthenticated HTTP (e.g., `curl https://api.github.com/...`) to GitHub.** Always use the GitHub MCP server (after calling `get_tool_manifest('github')`). If the GitHub MCP server or auth is unavailable, escalate to user.

### **5.1 Delivery Signals (Weekly)**

- **`merged_prs_last_week`** – Merged pull requests (state=`merged`) across the team’s tracked repositories during the previous Monday→Sunday window. Capture: title, PR number + URL, author, reviewers, merged_at, labels/tags describing scope, and whether the change shipped externally.
- **`recent_releases_or_tags`** – Releases or tags published in the same window to highlight hard launches.

### **5.2 Risk + Blocker Signals**

- **`open_blocker_issues`** – Open issues/PRs labeled `blocker`, `risk`, or matching the team’s severity labels. Capture title, owner, severity label, last updated timestamp, and explicit unblock actions.
- **`failing_work_items`** (optional) – Open PRs flagged by reviewers or workflows; summarize failure reason + ETA.

### **5.3 Upcoming + Planning Signals**

- **`project_items_upcoming`** – Items in program boards (GitHub Projects or equivalents) categorized as `Upcoming`, `Ready`, or `Next`. Capture item title, owner/DRI, target date, and blocking dependencies.
- **`milestone_target_dates`** – Milestones due within the next 2 weeks for each repo.

### **5.4 Metric Signals (PowerBI/ADX)**

- Use the PowerBI MCP for dashboard- or scorecard-sourced metrics; confirm the workspace/report/dataset plus the measure/view to pull, and note the date grain and window.
- Use the ADO MCP’s Kusto-capable tools when the user provides ADX/Kusto query text; pass the requested date window and surface the output in Highlights/Risks/Upcoming with source + timeframe.
- Metric bullets should cite the source (PowerBI vs Kusto/ADO) and the reporting window; avoid invented metrics if the query or dataset is missing—ask for the exact metric instead.

### **5.5 Manual Inputs**

Some orgs still provide spreadsheets or ad-hoc context. When GitHub/ADO/PowerBI data is missing or incomplete, ask for:

- Explicit highlights/risks/upcoming bullets per sub-area
- DRI for each sub-area; if unavailable, set a provisional DRI from the primary PR/issue author and mark it as provisional.
- Links to dashboards or docs supporting the claims
- Confirmation that no GitHub telemetry is available, so the agent can skip tool calls per the fallback plan
- Date range for Monday minutes

Document which data sources were used so reviewers know whether the update came from GitHub telemetry or manual inputs.

---

## **6. Tool Dependencies**

```
Tool Dependencies:
- github
- azure_devops
- powerbi
```

Hosts must call `get_tool_manifest('github')` and/or `get_tool_manifest('azure_devops')` and, when metrics are requested from dashboards, `get_tool_manifest('powerbi')` (per the list above) before planning telemetry calls so the agent can ingest the capability helpers, required toolsets, and fallback steps.

---

## **7. Fallback Plan**

If a referenced tool spec cannot be satisfied:

1. **Defer to the tool spec fallback** (e.g., the `github` tool spec lists detection rules for missing servers/tools).
2. **Prompt the user** with focused questions per missing signal, for example:
   - “Please list the top merged PRs (title, link, owners) for each sub-area last week.”
   - “Share any open Sev0/Sev1 risks, the owner, and the mitigation ETA.”
   - “Provide upcoming launches or milestones with dates for the next two weeks.”
   - “Provide the PowerBI dashboard/report link or the ADX/Kusto query + parameters for the metrics you want pulled.”
3. **Collect DRIs**: Ask for a DRI per sub-area; if the user cannot provide one, set a provisional DRI from the primary PR/issue author and label it as provisional.
4. **Accept minimal datasets** if necessary: TLDR + 3 highlights + explicit risks per sub-area.
5. **Document gaps** in the final output (e.g., “GitHub/ADO/PowerBI telemetry unavailable; content based on manual inputs from <user>”).

When some but not all tools from a referenced spec are available, use a hybrid approach: pull whatever telemetry you can, then ask the user to fill the remaining sections.

---

## **8. Section Structure**

The output for **one team** MUST follow this structure:

1. **Group Header**
2. **Sub-Area Sections** (one or more)

   * Sub-area title
   * DRI line
   * TLDR
   * Highlights
   * Risks + Blockers
   * Upcoming
   * Optional ships lists

   Use the icon headings exactly as written (`**📝 TLDR**`, `**🎯 Highlights**`, `**⚠️ Risks + Blockers**`, `**🔜 Upcoming**`) so downstream posts render consistently.

---

## **9. Detailed Section Requirements**

### **9.1 Group Header**

**Objective:** Identify which team/area this update belongs to.

* Heading:
  `# <Group Name>`

* Optional one-line intro (only if truly useful, e.g., if the whole team is skipping detailed updates that week).

**Examples:**

```markdown
# Foundry Models & Training
# GitHub Minutes
# Agentic DevOps – Azure Developer CLI
```

---

### **9.2 Sub-Area Section**

Each sub-area under the group follows the same pattern.

#### 9.2.1 Sub-Area Title & DRI

* Sub-area heading (level 2):
  `## <Sub-Area Name>`

* DRI line immediately below:
  `DRI: <Full name or alias>`

**Example:**

```markdown
## Direct Models
DRI: Naomi Moneypenny
```

---

#### 9.2.2 📝 TLDR

**Objective:** Provide a 1–3 sentence summary of the week for this sub-area.

**Requirements:**

* Must focus on **this week**: key ships, key movements, or overall status.
* Should reflect the main points that later appear in Highlights/Risks/Upcoming.
* Avoid repeating the group name or obvious context.

**Example:**

```markdown
**📝 TLDR**  
Cohere Embed v4 and Command A launched as Direct models on Azure; gpt-5.2 remains on track for 12/9 but capacity allocation is still in progress.
```

---

#### 9.2.3 🎯 Highlights

**Objective:** List concrete, notable events and outcomes.

**Format:**

* Heading: `**🎯 Highlights**`
* 3–8 bullet points.

Each bullet should:

* Describe a **specific** event, change, or result.
* Include numbers / dates when available (e.g., MAU, token growth, percentage improvements).
* Avoid generic “working on X” without any outcome.
* When referencing a PR/issue, include the PR number and hyperlink (e.g., `PR #123 [Fix login bug](https://github.com/org/repo/pull/123)`), and include the author when available.

**Example:**

```markdown
**🎯 Highlights**

- Cohere Embed v4 and Command A launched as Direct from Azure models; Rerank 4 simships next.
- gpt-5.x usage increased 72% MoM; total platform tokens reached 153T in November (4.3x YoY).
- High-demand quota requests continue for Grok and Sora; load-balancing work in progress for fallback scenarios.
```

---

#### 9.2.4 ⚠️ Risks + Blockers

**Objective:** Call out material risks and blockers for this sub-area.

**Format:**

* Heading: `**⚠️ Risks + Blockers**`
* 0–5 bullet points.
* If there are **no meaningful risks**, explicitly write `- None.`

Each bullet should:

* Start with a **short label** and then elaborate.
* Mention **impact** and **current mitigation** when known.

**Examples:**

```markdown
**⚠️ Risks + Blockers**

- Capacity: gpt-5.2 and shallotpeat chat require GB200/GB300 capacity; allocation for 12/9 release still pending.
- Neutrino v6: BOM from OAI is not available yet; new architecture and IO surface creates high onboarding risk with no assets in hand.
```

or, if no risks:

```markdown
**⚠️ Risks + Blockers**

- None.
```

---

#### 9.2.5 🔜 Upcoming

**Objective:** Show near-term next steps and important dates.

**Format:**

* Heading: `**🔜 Upcoming**`
* 2–6 bullet points.

Each bullet should:

* Be a **specific** upcoming event, release, or milestone.
* Include a **date/target window** whenever possible.

**Example:**

```markdown
**🔜 Upcoming**

- gpt-5.1-codex-max API release on 12/4 or 12/10.
- gpt-5.2 and shallotpeat chat releases targeted for 12/9.
- Neutrino v6 release targeted around 12/17, dependent on BOM and asset readiness.
```

---

#### 9.2.6 Optional: Ships Lists

Some teams (e.g., GitHub) may prefer explicit “ships last week / ships this week” lists inside a sub-area.

**Structure (optional block inside a sub-area):**

```markdown
**Ships last week**

- <Product/Area>: <Ship title> — <1-line description>

**Ships this week**

- <Product/Area>: <Planned ship> — <1-line description>
```

Use this only when it adds clarity beyond Highlights.

---

## **10. Task Planning Rules for Agent**

When the agent generates a **team’s Monday Minutes update**, it MUST：

1. **Identify the team/group name**

 * Use the user-provided name as `<Group Name>`.

2. **Detect telemetry source**

  * Read the latest user prompt for explicit instructions (e.g., `source=ado`, “use Azure DevOps Boards”, “pull GitHub activity”).
  * Default to GitHub when the source is unspecified; call `get_tool_manifest('github')` to inspect capabilities before planning tool calls.
  * When the user requests Azure DevOps data (or GitHub telemetry is unavailable), also call `get_tool_manifest('azure_devops')` and map each capability (`merged_prs_last_week`, etc.) to the Azure DevOps tools.
  * When the user asks for dashboard/PowerBI metrics, call `get_tool_manifest('powerbi')` and plan PowerBI MCP pulls (confirm workspace/report/dataset + measure names).
  * When the user asks for ADX/Kusto metrics, treat them as ADO data: call `get_tool_manifest('azure_devops')`, use the Kusto-capable tools with the provided query text + time window, and avoid inventing queries.
  * If both sources are requested, gather data from each and label notable bullets with the source when it aids clarity.
  * Do **not** call GitHub via unauthenticated curl/HTTP. Use GitHub MCP tools; if unavailable, switch to the fallback plan and ask the user for data.

3. **Identify sub-areas**

  * Either use explicit input (`Direct Models`, `Efficiency`, etc.)
  * Or, if only one block is provided, treat the whole team as a single sub-area with a meaningful name.

4. **For each sub-area:**

   * Determine DRI from inputs; if missing, prompt the user once for it. When no DRI is provided but telemetry includes an author/owner, set that as a provisional DRI and label it accordingly.
   * Summarize into a 1–3 sentence TLDR.
   * Extract 3–8 concrete Highlights.
   * Extract 0–5 Risks + Blockers; if none exist, emit `None`.
   * Extract 2–6 Upcoming items.

5. **Normalize:**

   * Use consistent heading levels and icon headings (`📝`, `🎯`, `⚠️`, `🔜`).
   * Remove duplicated statements between TLDR and Highlights.

6. **Self-review:**

   * Check that every sub-area has **DRI, TLDR, Highlights, Risks, Upcoming**.
   * Ensure risks are real and grounded in the inputs, not invented.

---

## **11. Quality Checklist**

### **Structure**

* [ ] `# <Group Name>` present.
* [ ] At least one `## <Sub-Area Name>` present.
* [ ] For each sub-area:

  * [ ] DRI line present.
  * [ ] TLDR block present.
  * [ ] Highlights block present.
  * [ ] Risks + Blockers block present.
  * [ ] Upcoming block present.

### **Content**

* [ ] TLDR matches the main points from Highlights/Risks/Upcoming.
* [ ] Highlights are concrete and specific.
* [ ] PR-related highlights include PR numbers and clickable URLs.
* [ ] Risks are clearly stated and not fabricated.
* [ ] Upcoming items have clear actions or milestones.
* [ ] DRIs are provided; any inferred/provisional DRIs are labeled as such.
* [ ] Metrics cite source + timeframe (PowerBI vs ADX/Kusto) and were pulled via the relevant MCP or documented as manual.
* [ ] GitHub telemetry came from the GitHub MCP tools (or documented manual fallback), not unauthenticated curl/HTTP calls.

### **Tone**

* [ ] Professional, concise, no hype.
* [ ] No vague “progress” bullets without content.
* [ ] Minimal redundancy.

If any checklist item fails → revise before returning the team update.

---

## **12. Final Output Format (Team-Level Skeleton)**

The final output for **one team** MUST be markdown in this shape:

```markdown
# <Group Name>

## <Sub-Area Name 1>
DRI: <Name or alias>

**📝 TLDR**  
<1–3 sentences>

**🎯 Highlights**

- <highlight 1>
- <highlight 2>
- <highlight 3>

**⚠️ Risks + Blockers**

- <risk 1>
- <risk 2>

**🔜 Upcoming**

- <upcoming 1>
- <upcoming 2>

---

## <Sub-Area Name 2>
DRI: <Name or alias>

**📝 TLDR**  
<1–3 sentences>

**🎯 Highlights**

- <highlight 1>
- <highlight 2>

**⚠️ Risks + Blockers**

- <risk or “None.”>

**🔜 Upcoming**

- <upcoming item>

---

<!-- Add more sub-areas as needed -->
```
