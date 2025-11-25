# PMAgent Spec MCP VSCode Extension

This VSCode extension automatically registers the PMAgent Spec MCP server at `http://localhost:8080/mcp`.

## Features

- Automatically registers the PMAgent Spec MCP server on activation
- Configurable server URL via VSCode settings
- Updates registration when configuration changes

## Configuration

You can configure the MCP server URL in VSCode settings:

```json
{
  "pmagentSpecMcp.serverUrl": "http://localhost:8080/mcp"
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

