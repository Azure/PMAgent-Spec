# PMAgent Spec MCP VSCode Extension

[![Install in VS Code](https://img.shields.io/badge/Install%20in%20VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=pmagent.pmagent-spec-mcp)

This VSCode extension automatically registers the PMAgent Spec MCP server at `http://localhost:8100/mcp`.

## Features

- Automatically registers the PMAgent Spec MCP server on activation
- Bundles the PMAgent Copilot agent template and drops it into `.github/agents/pmagent.agent.md` when a workspace is open (skips if you already have one)
- Configurable server URL via VSCode settings
- Updates registration when configuration changes

## Configuration

You can configure the MCP server URL in VSCode settings:

```json
{
  "pmagentSpecMcp.serverUrl": "http://localhost:8100/mcp"
}
```

## Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Compile the extension:
   ```bash
   npm run compile
   ```

3. Press F5 to run the extension in a new Extension Development Host window

4. Package the extension:
   ```bash
   vsce package
   ```

## Installation

1. Install the extension from the `.vsix` file:
   - Open VSCode
   - Go to Extensions view
   - Click "..." menu → "Install from VSIX..."
   - Select the `.vsix` file

2. The extension will automatically register the MCP server on activation.
