# Spec: Release Revision History Generator
Version: 1.0  
Content-Type: Product Release Documentation  
Authoring-Mode: AI

---

## 1. Purpose
This spec defines how the agent should generate a **comprehensive Release Revision History** using:

- GitHub Pull Requests  
- Azure DevOps Work Items  
- Work item hierarchies (Epic → Feature → User Story → Task/Bug)  
- Metadata (iteration, tags, area paths, custom fields)  
- Code repository structure (branches or release-specific folders)

The revision history must provide:
- High-level release summary  
- Major features and enhancements  
- Fixed bugs  
- Breaking changes  
- Engineering improvements (refactoring, infra, CI/CD, etc.)  
- Links to PRs and work items  
- Structured content suitable for Release Notes, Product Docs, or Engineering Review

---

## 2. Audience
- Engineering teams  
- Product managers  
- Customer-facing documentation teams  
- Stakeholders reviewing a release  

Expertise Level: Intermediate to advanced (technical familiarity expected).

---

## 3. Tone & Style Guidelines
- Professional, factual, concise  
- Group related changes logically  
- Avoid marketing tone  
- Emphasize clarity and technical accuracy  
- Use consistent Markdown formatting  
- Prefer short summaries for PRs and work items  

**Prohibited:**
- Hallucinating work items or PR details  
- Overstating impact or inventing features  
- Using vague non-technical language  

---

## 4. Required Inputs

### Release Definition (Code Base)
The release may be defined by:
- A GitHub branch (e.g., `release/v1.0`)  
- Git tags  
- A commit range  
- A release branch naming convention  

The agent must detect PRs associated with:
- The target branch  
- The commit range  
- Merged PRs between two tags  

### Release Definition (DevOps Tooling)
The release may be defined by one or more of:
- **Iteration Path** (e.g., `2025/Q1`)  
- **Area Path** (e.g., `Product/SDK`)  
- **Tags** (e.g., `Release-1.0`, `Hotfix`, `Customer-Request`)  
- **Work Item Types** (Epic, Feature, Story, Task, Bug)  
- **Custom fields** (Release ID, Milestone, etc.)

### Required Work Item Data
- ID  
- Title  
- Description (if relevant)  
- State (Done, Closed, Resolved)  
- Parent-child hierarchy  
  - Epic → Feature → User Story → Task  
- Linked PRs  
- Linked commits  
- Tags / Iteration / Area Path  
- Priority / Severity (for bugs)

### Required PR Data (GitHub)
- PR number  
- Title  
- Description  
- Labels  
- Files changed  
- Linked issues / work items  
- Author & reviewers  
- Merge date  
- Associated branch  
- Breaking change labels (if any)  

---

## 5. Section Structure of Final Revision History

1. **Release Overview**  
2. **Highlights (Major Improvements)**  
3. **New Features**  
4. **Enhancements**  
5. **Bug Fixes**  
6. **Breaking Changes (If Any)**  
7. **Engineering Improvements (Infra / Refactoring)**  
8. **Work Item Summary (Hierarchy Format)**  
9. **Pull Request Summary**  
10. **Full Change Log (Optional)**  
11. **Appendix: Data Sources & Technical Details**

---

## 6. Detailed Section Requirements

### 6.1 Release Overview
Include:
- Release name  
- Version  
- Release date (if available)  
- Code branch or iteration path  
- Number of PRs and work items included  
- High-level goals of the release (based on Epics/Features)  

---

### 6.2 Highlights (Major Improvements)
Summarize the top 3–8 improvements using:
- Epic/Feature titles  
- Major PRs  
- Customer-impacting changes  
- Cross-team initiatives  

---

### 6.3 New Features
Extract from:
- Features work items  
- User Stories marked as "new"  
- PRs labeled "feature" or "enhancement"

For each feature:
- Title  
- One-line summary  
- Linked work items and PRs  

---

### 6.4 Enhancements
For incremental improvements to existing features:
- Performance boosts  
- UX/UI improvements  
- Behavior refinements  
- Better validation, logging, error handling  

---

### 6.5 Bug Fixes
Collect from:
- Bug-type work items  
- PRs labeled `bug`, `fix`, or containing keywords (fix, resolve, issue #)

Include:
- Severity (if available)  
- Impact (high-level)  
- Short description  

---

### 6.6 Breaking Changes
Must capture:
- API changes  
- Behavior changes  
- Deprecations or removals  
- Required migration steps (if available)  

Source:
- PR descriptions  
- Work items with breaking-change tags  
- Commit messages mentioning breaking changes  

---

### 6.7 Engineering Improvements (Internal / Non-user-facing)
Examples:
- Refactoring  
- CI/CD improvements  
- Test coverage  
- Code cleanup  
- Infrastructure updates  

---

### 6.8 Work Item Summary (Hierarchy Format)

Work items must be grouped by hierarchy:

Epic
├─ Feature
│ ├─ User Story
│ ├─ Task
│ └─ Bug


Each item must include:
- ID  
- Title  
- Short summary sentence  
- Direct link  
- Status  
- Associated PRs  

If hierarchy is incomplete, still show available parent/child relationships.

---

### 6.9 Pull Request Summary
Summaries must include:
- PR number  
- Title  
- Short description  
- Labels  
- Files changed (optional)  
- Linked work items  
- Category classification (Feature, Bug Fix, Enhancement, etc.)

Group PRs by category automatically.

---

### 6.10 Full Change Log (Optional)
- Exhaustive list of PR titles sorted by merge date  
- Exhaustive list of work items sorted by type  

---

### 6.11 Appendix: Data Sources
List:
- Branch or commit range  
- Iteration or area path filters  
- Work item queries used  
- Tools used (GitHub API, Azure DevOps API)  

---

## 7. Task Planning Rules for Agent
To generate the revision history, the agent must:

1. Interpret how user defines the release (branch, iteration, tag, etc.).  
2. Use MCP Tools to collect all PRs and work items.  
3. Build parent-child hierarchy for work items.  
4. Map PRs → related work items → features → epics.  
5. Categorize changes (features, bugs, enhancements).  
6. Identify breaking changes.  
7. Write each section according to the structure.  
8. Validate for accuracy using Quality Checklist.  
9. Regenerate missing or incorrect sections.  
10. Produce final markdown output.  

---

## 8. Required Tools (MCP)

### GitHub MCP Tool
- Read PRs  
- Read branch commits  
- Read labels  
- Read linked issues  
- Fetch merged PRs by range  

### Azure DevOps MCP Tool
- Query work items using:
  - Iteration path  
  - Area path  
  - Tags  
  - Work item IDs  
  - Linked PRs  
- Retrieve hierarchy (Epic → Feature → Story → Task/Bug)

### Optional Tools
- Web search (for release notes references)  
- File system (for local repos)  

---

## 9. Quality Checklist

### Structural Quality
- All required sections included  
- Correct section ordering  
- Markdown formatting valid  

### Content Quality
- No hallucinated PRs or work items  
- All IDs, titles, and links correct  
- Hierarchy relationships preserved  
- Feature summaries accurate  
- Breaking changes identified correctly  
- No invented functionality  

### Tone Quality
- Clear, concise, technical  
- No marketing tone  
- No speculative language  

If any section fails validation → regenerate affected sections.

---

## 10. Final Output Format

The final result must be a **complete revision-history markdown document**, starting with:

```markdown
# Release Revision History — <Release Name>

## Release Overview
...

## Highlights
...

## New Features
...

## Enhancements
...

## Bug Fixes
...

## Breaking Changes
...

## Engineering Improvements
...

## Work Item Summary
...

## Pull Request Summary
...

## Full Change Log (Optional)
...
```

## 11. Metadata

Spec version: 1.0

Tags: release, changelog, revision-history, github, azure-devops

Compatible tools: GitHub MCP, Azure DevOps MCP, local repo analysis