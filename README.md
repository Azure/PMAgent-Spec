# PMAgent-Spec MCP Server

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
    *   Remote (Default): `https://.../sse`
    *   Local: `http://localhost:8100/sse`

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
    The server will listen on `http://0.0.0.0:8100`.

3.  **Connect Extension**:
    Update the extension setting (as above) to `http://localhost:8100/sse` and reload the window.

    ```json
        {
            "servers": {
                "spec-fetcher": {
                    "type": "sse",
                    "url": "http://localhost:8100/sse"
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
-   `get_tool_manifest(name?: str)` - Return machine-readable metadata for reusable tool specs (e.g., GitHub MCP, Azure DevOps MCP) including capabilities, required toolsets, fallback prompts, and example sequences.
-   `fetch_tool_spec(name: str)` - Fetch the markdown instructions for a specific tool spec referenced by content specs.

## Tool Specs & GitHub Copilot Flow

- Tool specs live under `tool_specs/` with a manifest served via `get_tool_manifest`.
- Each entry (starting with `github_mcp`) enumerates:
  - Required toolsets and discovery helpers (e.g., GitHub MCP `pull_requests`, `issues`, `projects`)
  - Capabilities (merged PRs, blockers, roadmap items) with recommended MCP tool calls
  - Example call sequences and fallback prompts when telemetry is unavailable
- Inside GitHub Copilot, the host can now:
  1. Call `list_specs` / `fetch_spec('monday_minutes')` for the narrative structure.
  2. Call `get_tool_manifest('github_mcp')` (and optionally `fetch_tool_spec('github_mcp')`) to learn exactly how to gather GitHub telemetry.
  3. Use the GitHub MCP server to collect merged PRs, blockers, and upcoming project items before drafting the update per the spec.

## Useful MCP Servers 

- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [Azure DevOps MCP Server](https://github.com/microsoft/azure-devops-mcp)
