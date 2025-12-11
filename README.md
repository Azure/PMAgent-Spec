# PMAgent-Spec MCP Server

[![Install in VS Code](https://img.shields.io/badge/Install%20in%20VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=pmagent.pmagent-spec-mcp)

An MCP (Model Context Protocol) server for fetching PMAgent specifications.

## What does this extension do?

This VS Code / Cursor extension **automatically registers the PMAgent MCP server** for you.

Instead of manually configuring JSON files or connection strings, simply installing this extension will add the PMAgent server to your MCP configuration, making tools like `fetch_spec` immediately available to your AI assistant.

## Installation

The extension is available on the **Visual Studio Marketplace**.

1.  Open the **Extensions** view in VS Code or Cursor (`Cmd+Shift+X` or `Ctrl+Shift+X`).
2.  Search for **"PMAgent Spec MCP"**.
3.  Click **Install**.

That's it! The extension will automatically register the server connection. You can check your Output panel ("PMAgent MCP" channel) to see the confirmation.

## Configuration

By default, the extension connects to the remote Azure-hosted server. You can change this URL (e.g., for local development) in the extension settings:

1.  Open **Settings** (`Cmd+,` or `Ctrl+,`).
2.  Search for **"PMAgent"**.
3.  Update the **Server Url**.
    *   Remote (Default): `https://.../mcp`
    *   Local: `http://localhost:8100/mcp`

## Local Development

If you want to run the server locally and test changes:

1.  **Install Dependencies**:
    ```bash
    cd src
    pip install -r requirements.txt
    ```

2.  **Start the Server**:
    ```bash
    python server.py
    ```
    The server will listen for MCP Streamable HTTP on `http://0.0.0.0:8100/mcp`.

3.  **Connect Extension**:
    Update the extension setting (as above) to `http://localhost:8100/mcp` and reload the window.

    ```json
        {
            "servers": {
                "spec-fetcher": {
                    "type": "http",
                    "url": "http://localhost:8100/mcp"
                }
            }
        }
    ```

## Deployment

This repository uses GitHub Actions for Continuous Deployment.

*   **Trigger**: Pushes to the `main` branch.
*   **Action**: Builds the Docker image and deploys it to Azure Container Apps.
*   **Result**: The remote MCP server is automatically updated with the latest code and specs.

## Available Tools

-   `content_generation_best_practice()` - Learn the best practice of content generation.
-   `list_specs()` - List all available specifications from the index.
-   `fetch_spec(name: str)` - Fetch the content of a specification by its name.
-   `get_tool_manifest(name?: str)` - Return tool spec YAML (when a `name` is provided) or list all tool specs discovered under `tool_specs/`.

## Tool Specs & GitHub Copilot Flow

- Each tool spec is a single YAML file under `tool_specs/` (e.g., `tool_specs/github.yml`) exposed through `get_tool_manifest`.
- Every entry enumerates:
  - Required toolsets and discovery helpers (e.g., GitHub MCP `pull_requests`, `issues`, `projects`)
  - Capability helpers (merged PRs, blockers, roadmap items) with recommended MCP tool calls
  - Example call sequences and fallback prompts when telemetry is unavailable
- Capability helpers are additive; you can still use any other MCP tool if it better satisfies the spec.
- Inside GitHub Copilot, the host can now:
  1. Call `list_specs` / `fetch_spec('monday_minutes')` for the narrative structure.
  2. Call `get_tool_manifest('github')` to load the YAML describing how to gather GitHub telemetry (capabilities, required toolsets, fallback).
  3. Use the GitHub MCP server to collect merged PRs, blockers, and upcoming project items before drafting the update per the spec.

### Adding or Referencing Tool Specs

1. Create `tool_specs/<tool>.yml` following the same schema (metadata, `toolsets`, `capabilities`, `fallback`, `example_sequences`).
2. Update any content spec's **Tool Dependencies** section to list the tool name (e.g., `- github`). No additional metadata is required inside the spec.
3. The system prompt instructs agents to call `get_tool_manifest('<tool>')` whenever a dependency is present, so no further server changes are needed.

### Azure DevOps Telemetry

- `tool_specs/azure_devops.yml` mirrors the GitHub manifest but targets the [microsoft/azure-devops-mcp](https://github.com/microsoft/azure-devops-mcp) server. Enable the `core`, `repositories`, `work`, and `work-items` domains (plus `pipelines`/`search` when release data is needed) before invoking its capability helpers.
- `spec/monday_minutes.md` now inspects the user's prompt for a telemetry preference: GitHub is the default source, but if the user asks for Azure DevOps (Boards, pipelines, work items, etc.), the agent must call `get_tool_manifest('azure_devops')` and satisfy each capability (`merged_prs_last_week`, `open_blocker_issues`, ...) with the ADO tools.
- When a user wants mixed telemetry, load both manifests and merge the resulting signals; annotate Highlights/Risks with the source when it aids reviewers.

## Useful MCP Servers 

- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [Azure DevOps MCP Server](https://github.com/microsoft/azure-devops-mcp)
