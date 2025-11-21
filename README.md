# PMAgent-Spec MCP Server

An MCP (Model Context Protocol) server for fetching PMAgent specifications.

## Starting the MCP Server Locally

If you need to run the server locally for development or testing:

1. Navigate to the `src` directory:
   ```bash
   cd src
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   python server.py
   ```

The server will start on `http://localhost:8100` and be accessible via SSE.

## VSCode Configuration

To connect to this MCP server in VSCode with Cursor or other MCP-compatible editors via SSE:

1. Open your VSCode settings (or Cursor settings)
2. Add the following configuration to your settings.json:

```json
{
  "mcp.servers": {
    "spec-fetcher": {
      "url": "http://localhost:8100"
    }
  }
}
```

3. Restart VSCode/Cursor for the changes to take effect.

The server should already be running and accessible via SSE on port 8100.

## Available Tools

- `list_specs()` - List all available specifications from the index
- `fetch_spec(name: str)` - Fetch the content of a specification by its name