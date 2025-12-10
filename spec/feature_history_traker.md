# Spec: Feature History Tracker
Version: 1.0
Content-Type: Markdown report
Authoring-Mode: ai

---

## 1. Purpose
Define how the agent generates a **feature history report** that explains how a feature evolved over time. The spec instructs the agent to mine commits, PRs, and work items; cluster changes into phases and workstreams; identify DRIs and contributors; and produce a narrative Markdown that goes beyond a commit list by grouping changes into meaningful milestones, themes, and components.

---

## 2. Audience
- Primary audience: New engineers onboarding to a feature; PMs needing context
- Secondary audience: Tech leads, EMs, architects, support/CS
- Expertise level: Intermediate technical
- Expected reading context: Repo docs (`/docs` or `/notes`), team wiki, onboarding handoff, PR templates

---

## 3. Tone & Style Guidelines
- Voice: Analytical, concise, factual, PM/eng-review style
- Point of view: Third-person; use neutral statements backed by evidence
- Reading level target: Mid-level engineer; avoid unexplained acronyms
- Prohibited styles: Marketing language, speculation without evidence, raw commit dumps, narrative fluff
- Examples:
  - Good: “Phase 2 (Mar–Apr): Messaging stack refactor centralized queue handling; 12 commits by A/B, risk reduced by shared retry policy.”
  - Bad: “Lots happened recently; seems stable now.”

---

## 4. Required Inputs

### 4.1 User-Provided Inputs
Inputs that must be collected from the user before proceeding:

**Mandatory:**
- Feature identifier: Name/keywords, epic or feature ID, and/or primary component paths that define scope.
- Repository scope: Repo URL or local path plus branch/tag or commit range to analyze (default: default branch history). If not provided, **prompt the user explicitly for the repo to enable PR linkage and PR URLs**.

**Optional:**
- Time window focus: Date span or release anchors (e.g., `v1.0..v1.3`) to bound the analysis.
- Component focus: Directories/files to prioritize (e.g., `services/chat`, `ui/chat`).
- Known milestones: Launch dates, migrations, or major refactors to treat as anchors.
- Known DRIs/teams: Names/aliases to validate against authorship.
- Output destination and length: Where to save and whether a long- or short-form narrative is desired.

### 4.2 Agent-Gathered Inputs
Inputs the agent must collect via tools or retrieval before writing:

**Mandatory:**
- Commit history scoped to the feature: Messages, authors, timestamps, files touched, and diffs sufficient to classify themes. If user tell you you're in the local repo, you can try user local git to accelerate the collection
- Pull request metadata relevant to the feature: Titles, descriptions, authors/reviewers, merge dates, linked issues, labels/tags, files changed, and **PR URLs**. If the repo is not specified or PR data is unavailable, prompt the user to provide the repo URL/path so PR linkage can be attempted.

**Optional:**
- Work items/issues linked to the feature (if available): IDs, titles, states, parent/child hierarchy, tags, iteration/area path, and links to PRs/commits.
- Hotspot analysis: File/component frequency, insertions/deletions per phase.
- Release anchors: Tags, branches, or deployment events that segment the history.
- Contributor metrics: Commit counts per phase, reviewer frequency, and handoff points.
- Documentation/notes: CHANGELOG excerpts, design docs, ADRs, or wiki pages that reference the feature.

Inputs may come from:
- Built-in tools for GitHub Copilot VS Code
- Local Git
- MCP tools (GitHub MCP for commits/PRs in Github, Azure DevOps MCP for commits/PRs in Github)
- Context/State (conversation hints, prior outputs)
- Local files (repo history, docs, changelogs)

---

## 5. Data Requirements
For each requirement include Name, Description, Source Preference, Filters, Fields Needed, and Update cadence.

- **Name:** `feature_commits`  
  **Description:** Commits matching feature keywords/paths to map chronology and intent.  
  **Source Preference:** Local Git, GitHub MCP for source in Github; Azure DevOps MCP for sources in Azure Devops
  **Filters:** Branch/range, path filters, keyword search in messages/diffs.  
  **Fields Needed:** SHA, author, author_email, date, message, files, insertions/deletions, linked PR.  
  **Update cadence:** Latest as of generation time.

- **Name:** `commit_phases`  
  **Description:** Time- or theme-based clusters (e.g., initial build, refactor, hardening) derived from commit density and keyword shifts.  
  **Source Preference:** Derived from `feature_commits`.  
  **Filters:** Sliding windows or change-point detection by date/label.  
  **Fields Needed:** Phase label, date span, representative commits, dominant topics.  
  **Update cadence:** Derived per run.

- **Name:** `component_hotspots`  
  **Description:** Components/files most affected by the feature to explain scope and architectural touch points.  
  **Source Preference:** Aggregated from commit file lists.  
  **Filters:** Paths under provided components; exclude vendored/generated files.  
  **Fields Needed:** Path, touches count, authors, first/last touch dates.  
  **Update cadence:** Derived per run.

- **Name:** `pr_summary_by_feature`  
  **Description:** PRs implementing the feature, capturing intent, review context, and merge order.  
  **Source Preference:** GitHub MCP for source in Github; Azure DevOps MCP for sources in Azure Devops – pull_requests.  
  **Filters:** Labels/keywords, linked issues, branch range.  
  **Fields Needed:** Number, title, description, author, reviewers, merge date, labels, linked work items, files changed, **PR URL**.  
  **Update cadence:** Latest merged PRs in scope.

- **Name:** `work_item_hierarchy`  
  **Description:** Epics/Features/Stories/Tasks related to the feature to align code changes to planned work.  
  **Source Preference:** Azure DevOps MCP – work items.  
  **Filters:** Feature ID/keywords, area/iteration paths.  
  **Fields Needed:** ID, title, type, state, parent/child links, tags, assigned_to, linked commits/PRs.  
  **Update cadence:** Latest state during report generation.

- **Name:** `release_landmarks`  
  **Description:** Tags, releases, deployments, or launch notes that serve as narrative anchors.  
  **Source Preference:** GitHub MCP – releases/tags; local git tags.  
  **Filters:** Date range, feature keywords in release notes.  
  **Fields Needed:** Tag/release name, date, notes summary, related PRs.  
  **Update cadence:** Latest as of generation.

- **Name:** `authorship_by_phase`  
  **Description:** Key contributors per phase to identify DRIs and handoffs.  
  **Source Preference:** Aggregated from commits/PRs.  
  **Filters:** Phase windows.  
  **Fields Needed:** Author, contribution counts, primary components, first/last activity dates.  
  **Update cadence:** Derived per run.

- **Name:** `phase_deltas`  
  **Description:** Add/modify/remove summaries per phase to explain how each phase differs from the prior one.  
  **Source Preference:** Derived from commit/PR diffs per phase.  
  **Filters:** Phase windows aligned to `commit_phases`.  
  **Fields Needed:** Added files/areas, removed files/areas, major modifications, notable API/behavior changes.  
  **Update cadence:** Derived per run.

- **Name:** `commit_pr_correlation`  
  **Description:** Mapping of commits to their PRs with URLs for hyperlinking and traceability.  
  **Source Preference:** PR data + commit metadata.  
  **Filters:** Scope-limited commits and PRs only.  
  **Fields Needed:** PR number, PR URL, representative commit SHAs, phase tags.  
  **Update cadence:** Derived per run.

---

## 6. Tool Dependencies
Tool Dependencies:
- github (optional)
- azure_devops (optional)
- local git
---

## 7. Fallback Plan
- Detect issues: Missing `github`/`azure_devops` in `available_tools`, tool call errors, or empty responses for commits/PRs/work items.
- Alternatives:
  - Use local git history (`git log`, `git show`) when MCP calls are unavailable.
  - If work items are unavailable, rely on commit/PR metadata and ask for user-supplied issue context.
- If PR metadata cannot be fetched (repo unknown or API unavailable), prompt the user to provide the repo URL/path or paste PR lists for linkage.
- Questions to ask the user when data is missing:
  - Provide feature keywords/paths and commit range?
  - Supply a list of relevant PR numbers or a CSV of commits?
  - Confirm known milestones or releases for anchors?
  - Share DRI names or teams to validate authorship?
- Minimal data to continue: feature keywords, repository/branch or commit range, and at least a short list of representative commits or PRs to ground the narrative.

---

## 8. Section Structure
The output MUST follow this exact structure:
1. **Title**
2. **TLDR**
3. **Scope & Method**
4. **DRI & Contributors**
5. **Feature Evolution Timeline**
6. **Workstreams & Components**
7. **Appendix (Data & Filters)**

---

## 9. Detailed Section Requirements
### Section: Title
- Objective: State feature name and scope in one line.
- Expected length: 1 line.
- Required elements: Feature name/ID, repo or branch, date generated.
- Mandatory details: Scope boundary (branch/range or releases).
- If referencing external sources: None.

### Section: TLDR
- Objective: Provide a crisp summary of the feature history.
- Expected length: 3–5 sentences or bullets.
- Required elements: Current status, 2–4 major milestones, primary DRI(s); include inline PR anchors with links for at least the major milestones.
- Mandatory details: Evidence-backed statements only; avoid speculation.
- If referencing external sources: Cite PR/commit numbers inline (e.g., `PR #123`, `commit abc123`).

### Section: Scope & Method
- Objective: Explain what was analyzed and how.
- Expected length: 4–6 bullets.
- Required elements: Repository URL, branch/range, time window, filters/keywords, data sources used (commits, PRs, work items), exclusions.
- Mandatory details: Timeframe and components included/excluded.
- If referencing external sources: Mention tools used; no deep citations required.

### Section: DRI & Contributors
- Objective: Identify accountable individuals and major contributors.
- Expected length: 4–8 bullets or short table.
- Required elements: Primary DRI(s), phase-level contributors, reviewer highlights, ownership changes/handoffs; include emails/aliases when available; cite supporting commits/PR links for key ownership claims.
- Mandatory details: Derive from authorship stats; avoid guessing titles/roles.
- If referencing external sources: Cite representative commits/PRs per contributor when clarifying ownership.

### Section: Feature Evolution Timeline
- Objective: Narrate the feature history by phases (not raw commit lists) with concrete code deltas. This is the main part.
- Expected length: better less then 10 phases (unless it's really a huge history) with 3–6 bullets each.
- Required elements: Phase name, date span, intent, key changes, supporting evidence (commit/PR/work item references with links), and **delta vs previous phase** (what was added, removed, or substantially modified).
- Mandatory details: Group by milestones (e.g., initial build, refactor, stabilization, rollout); highlight dependencies or migrations; describe meaningful code changes (APIs, components, behavior) unless commit summaries are sufficiently detailed. Avoid shallow listing—explain what the code now does that it did not before, referencing files/components touched when possible.
- If referencing external sources: Use inline refs (`PR #`, `WI #`, `commit <shortsha>`).

### Section: Workstreams & Components
- Objective: Map changes to subsystems/components.
- Expected length: 3–6 bullets or a compact table.
- Required elements: Component/path, change theme, dominant contributors, impact (e.g., perf, reliability, UX), and representative commits/PR links.
- Mandatory details: Base on hotspot analysis; avoid inventing components.
- If referencing external sources: Cite paths and representative commits/PRs.

### Section: Appendix (Data & Filters)
- Objective: Show supporting data and filters used.
- Expected length: As needed (tables or bullet lists).
- Required elements: Filters/keywords (repo URL, branch, time window), and something you're not clear during history collection.

---

## 10. Task Planning Rules for Agent
For this spec, the agent must do the following tasks:
1. Validate required inputs (feature identifier, repo scope) and confirm optional anchors (timeframe, components, DRIs).  
2. If repo scope is missing, **prompt the user for the repo URL/path to enable PR linkage**, then choose tools to collect commits, PRs, and work items; apply filters and paths to scope data.  
3. Derive phases, phase deltas (add/remove/modify), hotspots, and authorship stats; tag items by phase/workstream.  
4. Summarize findings into the defined sections in order, focusing on code-level changes rather than raw commit dumps; include commit–PR correlation with links in the Appendix.  
5. Perform self-review against the Quality Checklist and adjust narrative/structure as needed.  
6. Save or return the Markdown in the Final Output Format.

---

## 11. Quality Checklist
### Structure
- All sections 1–7 present and ordered correctly.  
- Timeline phases include delta vs previous phase.  
- Inline references use IDs (PR #, WI #, short SHA) with links where possible.

### Content Quality
- Statements are evidence-backed; no hallucinated ownership or timelines.  
- Phases are grouped logically (time or theme) and not just chronological commits; each phase explains adds/removes/major modifications.  
- DRI/contributors align with authorship data; handoffs noted when visible.  
- Components/workstreams reflect actual file touchpoints.  
- Avoid shallow commit lists; describe what the code now does that it did not before.
- Appendix includes Filters/anchors used and something you're not clear during history collection.

### Tone
- Analytical, concise, non-marketing.  
- No filler or speculative language.  
- Clarity prioritized over flourish.

---

## 12. Final Output Format
Output as Markdown using this skeleton:

```markdown
# <Feature Name> – Feature History

## TLDR
- <3–5 bullets with PR links for major milestones>

## Scope & Method
- Scope: <repo URL>, <branch/range, paths>
- Data: <commits/PRs/work items used>
- Filters: <keywords/anchors>

## DRI & Contributors
- Primary DRI: <name(s)>
- Key contributors: <names with phase/component notes>
- Ownership shifts: <if any>

## Feature Evolution Timeline
- Phase 1 (<dates>): <intent + key code changes + delta vs prev + refs/PR links>
- Phase 2 (<dates>): <intent + key code changes + delta vs prev + refs/PR links>
- Phase 3 (<dates>): <intent + key code changes + delta vs prev + refs/PR links>

## Workstreams & Components
- <component/path>: <theme, impact, refs/PR links>

## Appendix (Data & Filters)
- Filters/anchors used: <list>
- Concern / Not clear part in history collection.
```
