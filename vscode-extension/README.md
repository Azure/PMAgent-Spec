# PMAgent Spec MCP VSCode Extension

[![Install in VS Code](https://img.shields.io/badge/Install%20in%20VS%20Code-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=pmagent.pmagent-spec-mcp)

This VSCode extension automatically registers the PMAgent Spec MCP server at `https://pmagent-spec.nicesmoke-219d4124.eastus2.azurecontainerapps.io/mcp`.

## Features

- Automatically registers the PMAgent Spec MCP server on activation
- Adds a command to install the PMAgent Copilot agent template into `.github/agents/pmagent.agent.md` only when you request it
- Adds a command to remove the installed agent template from your workspace
- Configurable server URL via VSCode settings
- Updates registration when configuration changes

## Commands

- `PMAgent: Install agent into Workspace` — copies the bundled agent template into `.github/agents/pmagent.agent.md` in the selected workspace (prompts before overwriting).
- `PMAgent: Remove agent from Workspace` — deletes the agent file from the selected workspace (prompts for confirmation).

## Configuration

You can configure the MCP server URL in VSCode settings:

```json
{
  "pmagentSpecMcp.serverUrl": "https://pmagent-spec.nicesmoke-219d4124.eastus2.azurecontainerapps.io/mcp"
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
