# Tool Spec: GitHub MCP Telemetry

Version: 1.0
Content-Type: markdown
Authoring-Mode: ai

---

## 1. Purpose

This tool spec documents how content-generation agents should leverage the **GitHub MCP server** (remote or local) to gather telemetry for specs such as Monday Minutes, revision histories, or launch reports. It focuses on read-heavy workloads (merged PRs, blockers, releases, roadmap items) that inform PM-style narratives without embedding API logic inside the PMAgent Spec MCP.

---

## 2. MCP Registration & Discovery

1. Confirm the host registers a server named `github`. Remote default: `https://api.githubcopilot.com/mcp/`.
2. Enumerate tool availability via `mcp.list_tools`.
3. If the server supports dynamic enablement, call:
   - `github.list_available_toolsets`
   - `github.get_toolset_tools`
   - `github.enable_toolset` (per toolset: `pull_requests`, `issues`, `repos`, `projects`).
4. Respect read-only headers/flags; these instructions only rely on read operations.

---

## 3. Required Toolsets

| Toolset | Why it matters |
|---------|----------------|
| `pull_requests` | Inspect merged PRs, review states, and CI status. |
| `issues` | Retrieve blockers, Sev0/Sev1 items, and tracking bugs. |
| `repos` | List releases, tags, and milestones. |
| `projects` | Extract roadmap items (Upcoming/Ready) and owners. |

Discovery helpers (`list_available_toolsets`, `get_toolset_tools`, `enable_toolset`) must remain available even before toolsets are enabled.

---

## 4. Data Capabilities

### 4.1 Delivery Signals – `merged_prs_last_week`

Use either `github.list_pull_requests` (per repo) or `github.search_pull_requests` (multi-repo) to capture:
- PR title, number, URL
- Author + reviewers
- `merged_at`
- Labels describing scope (`launch`, `customer`, `infra`, etc.)

**Example call:**
```json
{
  "tool": "github.search_pull_requests",
  "arguments": {
    "query": "repo:azure/pmagent-spec is:pr is:merged merged:>=2024-11-18",
    "perPage": 50
  }
}
```
Normalize results by week and map them to spec sub-areas.

### 4.2 Releases & Tags – `recent_releases_or_tags`

`github.list_releases` (per repo) or `github.get_release_by_tag` provide release names, tags, and publish dates. Include release URLs when summarizing Highlights.

### 4.3 Risks & Blockers – `open_blocker_issues`

Leverage `github.search_issues` with label filters:
- `org:<org> is:open label:blocker`
- Add aliases such as `label:"Sev0"` or `label:risk`.
Return title, owner, severity label, last updated timestamp, and mitigation notes if available.

### 4.4 Workflow / Review Failures – `failing_work_items`

Call `github.pull_request_read` with `method="get_status"` to inspect workflow status for critical PRs. Surfaced data feeds the Risks section of consuming specs.

### 4.5 Roadmap Items – `project_items_upcoming` & `milestone_target_dates`

- `github.list_project_items` with `query: "status:Upcoming"` or similar board-specific filters. Capture item title, DRI, due date, and blocking dependencies.
- `github.list_milestones` (per repo, `state="open"`) to harvest milestone names and due dates.

---

## 5. Example Call Sequence (Host-Orchestrated)

```yaml
- tool: mcp.list_tools
  purpose: Detect the `github` server and discovery helpers.
- tool: github.list_available_toolsets
- tool: github.enable_toolset
  arguments: { toolset: pull_requests }
- tool: github.enable_toolset
  arguments: { toolset: issues }
- tool: github.list_pull_requests
  arguments:
    owner: azure
    repo: pmagent-spec
    state: closed
    sort: updated
    direction: desc
    perPage: 30
- tool: github.search_issues
  arguments:
    query: "repo:azure/pmagent-spec label:blocker is:issue is:open updated:>=2024-11-18"
- tool: github.list_project_items
  arguments:
    org: azure
    project_number: 42
    query: "status:Upcoming"
```

Hosts should normalize timestamps immediately, bucket the data per spec sub-area, and persist the structured context for reuse.

---

## 6. Fallback & Manual Inputs

Detect gaps when:
- The `github` server is absent from `mcp.list_tools`.
- Discovery tools exist but `list_pull_requests` / `search_issues` are missing.
- Tool calls return empty payloads for the requested time window.

In these cases, consuming specs (e.g., Monday Minutes) must ask the user for:
1. Merged PRs last week (title, link, owner).
2. Sev0/Sev1 or blocker issues plus mitigation / ETA.
3. Upcoming launches or milestones with target dates.
New data should be marked as manual in the final narrative.

---

## 7. Referencing Specs

| Spec | Usage |
|------|-------|
| `monday_minutes` | Weekly updates pull delivery, risk, and roadmap signals from GitHub before drafting Highlights/Risks/Upcoming. |

Add future specs to this table as they start relying on GitHub telemetry.
