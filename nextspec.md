# Next-Generation PMAgent Spec Architecture

## 1. Problem Statement

The current MCP server (`src/server.py`) bundles static spec distribution **and** bespoke data-ingestion logic (e.g., GitHub API fetches). This approach limits extensibility because:

- Every new data source requires modifying and redeploying the spec server.
- VS Code/Cursor users already have other MCP servers (GitHub, Azure DevOps) registered; we should exploit them instead of duplicating functionality.
- Monday Minutes (and similar specs) should orchestrate across **multiple** MCP servers/tools at runtime without tight coupling.

Goal: design an architecture where the PMAgent Spec MCP remains lightweight (serving specs + prompts), while content-generation agents dynamically compose additional MCP servers (GitHub, Azure DevOps, custom) to collect required signals.

## 2. Guiding Principles

1. **Single Responsibility** – The PMAgent Spec MCP focuses on distributing specs, prompts, and metadata. It does not reach out to GitHub/Azure.
2. **Composable MCP Graph** – Users can register any set of MCP servers; specs describe *what data* is needed, not *how to fetch it*. The agent picks the best MCP tool available in the session.
3. **Spec-Driven Orchestration** – Specs enumerate required inputs, recommended tool calls, and fallback strategies. They never hardcode HTTP endpoints.
4. **Zero Coupling in Extension** – The VS Code extension only bootstraps the PMAgent Spec MCP connection. Users can add other MCP servers via their own settings.
5. **Progressive Enhancement** – Support for richer automation (like GitHub activity synthesis) should be optional: if another MCP isn’t installed, the agent requests the user to provide data manually.

## 3. Architectural Overview

```
┌─────────────────────────┐          ┌────────────────────────────┐
│ VS Code / Cursor Client │─────────▶│ MCP Host (OpenAI/Copilot) │
└──────────┬──────────────┘          └───────────┬────────────────┘
           │                                     │
     registers MCP servers                 multiplexes MCP calls
           │                                     │
   ┌───────▼─────────┐                ┌──────────▼─────────┐
   │ PMAgent Spec MCP│                │ Other MCP Servers  │
   │ (this repo)     │                │ (GitHub, Azure, ...)│
   ├─────────────────┤                ├─────────────────────┤
   │ list_specs      │                │ github.search_issues │
   │ fetch_spec      │                │ ado.query_workitems  │
   │ best_practices  │        ...     │ custom.*             │
   └─────────────────┘                └─────────────────────┘
```

*Agents interact solely with the MCP host. To build Monday Minutes, the agent orchestrates calls like:*

1. `content_generation_best_practice` (PMAgent Spec MCP)
2. `list_specs` / `fetch_spec('monday_minutes')`
3. Inspect spec section “Required Inputs” + the machine-readable **Tool Dependencies** block → detect which external MCP capabilities are required
4. Call external MCP server tool, e.g., `github.list_recent_activity`, `ado.fetch_work_items`
5. Merge inputs → craft final Monday Minutes output per spec

## 4. PMAgent Spec MCP Responsibilities

| Capability | Description |
|------------|-------------|
| Spec catalog | Serve curated specs (Markdown) via `list_specs` / `fetch_spec`.
| Prompt best practices | Provide system prompts describing workflow, tool selection, validation.
| Tool specs catalog | (New) Serve per-tool YAML files under `tool_specs/<tool>.yml` that map spec signals to MCP calls (capabilities, fields, discovery helpers, fallback). `get_tool_manifest('<tool>')` simply returns the raw YAML so hosts (and LLMs) can read it directly; no JSON manifest or secondary Markdown is maintained.
| Versioning | Report spec versions so clients can detect updates.

No other outbound network requests should exist in this server. Any domain integration happens elsewhere.

## 5. Spec Enhancements

Add the following sections to each spec (starting with Monday Minutes):

1. **Data Requirements** – enumerate structured inputs (GitHub PRs, issues, ADO work items, metrics dashboards).
2. **Tool Dependencies** – A short list that names the required tool specs (e.g., `github`, `azure_devops`). Capability details stay inside the tool spec; the list simply tells the host which YAML files to load.
3. **Fallback Plan** – instructions for asking the user when tools are unavailable or return insufficient data.

Each tool spec is a single YAML file (e.g., `tool_specs/github.yml`) that already includes required toolsets, capability helpers (with recommended call sequences), fallback prompts, and example orchestrations. Eliminating the old `manifest + markdown` split keeps the content machine-first and makes it easier for other orgs to drop in their own MCP mappings without editing the PMAgent server. The capability helpers are advisory overlays—they highlight proven workflows but do not restrict callers from using any other MCP function.

Specs no longer copy capability IDs or call snippets; they only cite the tool name. The `content_creation_best_practice` prompt now reminds agents to call `get_tool_manifest('<tool>')` for every dependency and treat the listed capabilities as guidance (they can still call any other MCP function as needed).

Because every entry is standalone YAML, contributors (or downstream tenants) can add new mappings—`tool_specs/my_github_clone.yml`, `tool_specs/ado.yml`, etc.—without touching the MCP codebase; the server automatically discovers any `*.yml` under `tool_specs/` when responding to `get_tool_manifest`.

## 6. Extension Story

Current extension behavior: auto-register PMAgent Spec MCP at startup by editing `mcp.servers` in VS Code settings. Future approach:

- **No change** to current functionality (backward compatible).
- Provide documentation within the extension README (and marketplace listing) explaining how to add companion MCP servers (GitHub MCP, Azure DevOps MCP, Slack MCP, etc.).
- Optionally, include a command palette entry: “Open MCP Settings” to guide users toward installing recommended MCP servers.

## 7. Agent Orchestration Flow (Monday Minutes example)

1. Agent loads Monday Minutes spec → sees required data + the `Tool Dependencies` list naming `github`.
2. Agent calls `get_tool_manifest('github')` to load the YAML describing discovery steps, toolsets, and example sequences.
3. Host enumerates available MCP servers and enables the referenced toolsets if available.
4. If `github.*` tools exist → run queries per **tool spec** guidance.
5. If not: follow the spec’s fallback prompts and gather data manually.
6. Combine data + produce Monday Minutes per structure.

## 8. Open Questions

1. Should PMAgent Spec MCP provide example prompts/tool-call scripts for orchestrators (JSON schema) to reduce agent reasoning overhead?
2. How do we version/control spec dependencies so agents know when recommended MCP tools change?
3. Is there value in a lightweight “spec runner” MCP that simply sequences recommended tool calls and returns structured context (still separate from PMAgent Spec MCP)?

---

This design keeps the PMAgent Spec MCP focused, enables drop-in MCP composability, and gives Monday Minutes (and future specs) the guidance they need to leverage users’ existing GitHub/ADO MCP deployments without embedding custom logic.
