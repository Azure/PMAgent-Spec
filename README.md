# PMAgent-Spec MCP Server

[![Install in VS Code](https://img.shields.io/badge/Install%20in%20VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=pmagent.pmagent-spec-mcp)

PMAgent-Spec is an MCP (Model Context Protocol) server that delivers PMAgent content specs (Monday Minutes, revision histories, OKR reports, SDK READMEs, etc.) to GitHub Copilot or any MCP-capable client. The companion VS Code extension auto-registers the hosted server and drops the `pmagent-orchestrator` agent template into your repo so Copilot can immediately call the PMAgent tools.

## Install in VS Code

1. Open the Extensions view (`Cmd/Ctrl+Shift+X`).
2. Search for **“PMAgent Spec MCP”** and install.
3. The extension registers `https://pmagent-spec.nicesmoke-219d4124.eastus2.azurecontainerapps.io/mcp` automatically. Check the **PMAgent MCP** output channel for confirmation.

## MCP helpers to pair with

- GitHub MCP: Use when repos and PRs live in GitHub (merged PRs, blockers, milestones, upcoming project items). [Repo](https://github.com/github/github-mcp-server)
- Azure DevOps MCP: Use when telemetry lives in ADO (Boards, pipelines/releases, blockers, upcoming backlog items). [Repo](https://github.com/microsoft/azure-devops-mcp)
- Power BI Modeling MCP: Use when a spec needs dashboard or semantic model metrics (e.g., OKR or Monday Minutes KPIs). [Repo](https://github.com/microsoft/powerbi-modeling-mcp)

## Use with GitHub Copilot in VS Code

1. In Copilot Chat, choose the **pmagent-orchestrator** agent (the extension adds `.github/agents/pmagent.agent.md` for you).
2. Describe the deliverable plus telemetry sources (GitHub vs ADO vs Power BI) and the repos/projects/date range.

## Supported scenarios (specs)

- `monday_minutes`: Generate Monday Minutes updates for a team or project.
- `revision_history`: Create revision history / release notes from GitHub PRs and Azure DevOps work items tied to a release.
- `product_status_report`: Summarize product/release health with progress, risks, bugs, dependencies, and next steps.
- `okr_report`: Produce OKR performance reports (SignalR/Web PubSub) with predefined KQL queries and insights.
- `feature_history_traker`: Turn commits/PRs/work items into a narrative feature history grouped by phases/workstreams.
- `sdk_readme`: Generate or update an SDK README from source code, APIs, dependencies, and samples.

## Remote MCP config (manual)

If you are not using the extension, register the hosted server in your MCP client (e.g., `~/.config/github-copilot/mcp.json`):

```json
{
  "mcpServers": {
    "pmagent-spec": {
      "transport": {
        "type": "http",
        "url": "https://pmagent-spec.nicesmoke-219d4124.eastus2.azurecontainerapps.io/mcp"
      }
    }
  }
}
```

Add your other MCP servers (GitHub, Azure DevOps, Power BI) to the same file per their docs so the manifests in `tool_specs/` can be used.

## What it does

- Serves spec templates and writing guardrails through `content_generation_best_practice`, `list_specs`, and `fetch_spec`.
- Documents telemetry helpers through `get_tool_manifest`, mapping each spec to the right GitHub, Azure DevOps, or Power BI MCP calls.
- Provides an extension that registers the remote server at activation (no manual JSON edits required).

## Local development

1. Optional: create a virtual environment in `src/` (`python -m venv .venv && source .venv/bin/activate`).
2. Install dependencies: `pip install -r src/requirements.txt`.
3. Start the MCP server: `python src/server.py` (listens on `http://0.0.0.0:8100/mcp`).
4. Point your MCP config or the VS Code setting `pmagentSpecMcp.serverUrl` to `http://localhost:8100/mcp`, then reload the client.

## Contributing

See `CONTRIBUTING.md`.
