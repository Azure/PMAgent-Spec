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
- Power BI Remote MCP: The remote Power BI MCP server enables AI agents to query Power BI semantic models using natural language.  (e.g., OKR or Monday Minutes KPIs). [Repo](https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-get-started)
- Kusto/ADX MCP: Use [Azure MCP](https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server)

## Use with GitHub Copilot in VS Code

1. Use `F1` to open vscode command and run `PMAgent: Install agent into Workspace`
2. In Copilot Chat, choose the **pmagent-orchestrator** agent (the extension adds `.github/agents/pmagent.agent.md` for you).
3. Describe the deliverable plus telemetry sources (GitHub vs ADO vs Power BI) and the repos/projects/date range.

## Supported scenarios (specs)

- `monday_minutes`: Generate Monday Minutes updates for a team or project.
- `revision_history`: Create revision history / release notes from GitHub PRs and Azure DevOps work items tied to a release.
- `product_status_report`: Summarize product/release health with progress, risks, bugs, dependencies, and next steps.
- `feature_history_traker`: Turn commits/PRs/work items into a narrative feature history grouped by phases/workstreams.
- `sdk_readme`: Generate or update an SDK README from source code, APIs, dependencies, and samples.
- `powerbi_telemetry_knowledge`: Generate knowledge of PowerBI Semantic Model Schema and product-specific OKRs.
- `adx_telemetry_knowledge`: Generate knowledge from ADX (Azure Data Explorer) dashboard json file including predefined queries and filters.
- `okr_report`: Produce a report with OKR and corresponding analysis/insights from PowerBI semantic model or ADX KQL queries.
- `spec_creation`: Collect user inputs per `templates/spec_template.md` and generate a new spec that matches that structure.
- Template injection: Specs can embed `{{template_name.md}}` placeholders; `fetch_spec` will inline the matching file under `templates/` (local first, remote fallback) before returning.

### OKR Report 

- Chat with **pmagent-orchestrator** agent in Copilot to build your product-specific knowledge:
  - PowerBI Semantic Model Schema and OKRs Knowledge: Copilot will use `Power BI Modeling MCP` and `powerbi_telemetry_knowledge` spec from PM Agent to help you generate the initial knowledge draft.
  - ADX Kusto Query Knowledge: Copilot will use Kusto tools from `Azure MCP` and `adx_telemetry_knowledge` spec from PM Agent to help you generate the initial knowledge draft.

```text
create a new PowerBI telemetry knowledge markdown file for <your-product-full-name> based on <links-to-your-product-dashboard>
```

- PM Agent cannot doscover OKRs from the dashboard directly. Therefore, you may also need to revise the product-specific knowledge in these areas:
  - `IsAnalysisDimension` for each column: If a column is tagged Yes in IsAnalysisDimension, the column should be treated as a primary candidate for cohort analysis and can be safely used to break results down into slices (segments) for comparisons across groups.
  - Entity Relationships
  - Definiation of each OKR(s), including `Time Semantics`, `Telemetry Scope and Filters`, `Metric Calculation Logic`, `Targets, Thresholds, and Guardrails` and `Recommended Breakdowns and Dimensions`. 

- Chat with **pmagent-orchestrator** agent in Copilot to generate a new OKR report for your product. Copilot will use `Power BI Modeling MCP` or `Azure MCP (with Kusto)` and `okr_report` spec from PM Agent to help retrive real data from PowerBI dashboard or Kusto queries and generate OKR report. 

```text
generate new okr report for <your-product-name>> based on <your-product-specific-knwoledge-on-local> and write into a new markdown file
```

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
