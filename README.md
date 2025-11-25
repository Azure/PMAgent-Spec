# PMAgent-Spec MCP Server

An MCP (Model Context Protocol) server for fetching PMAgent specifications.

## Quick Start

1.  **Install the Extension**: Install the `PMAgent Spec MCP` extension in VS Code or Cursor.
2.  **Ready to Use**: The extension automatically configures your MCP settings to connect to the remote production server. You can immediately start using tools like `list_specs()` and `fetch_spec()`.

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

## Deployment

This repository uses GitHub Actions for Continuous Deployment.

*   **Trigger**: Pushes to the `main` branch.
*   **Action**: Builds the Docker image and deploys it to Azure Container Apps.
*   **Result**: The remote MCP server is automatically updated with the latest code and specs.

## Available Tools

-   `list_specs()` - List all available specifications from the index.
-   `fetch_spec(name: str)` - Fetch the content of a specification by its name.
