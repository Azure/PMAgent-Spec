import * as vscode from 'vscode';

// Create an output channel to see logs in the "Output" tab
const outputChannel = vscode.window.createOutputChannel("PMAgent MCP");

export function activate(context: vscode.ExtensionContext) {
    outputChannel.show(true); // Show the channel immediately
    outputChannel.appendLine('PMAgent Spec MCP extension is activating...');

    // Get the MCP server URL from our extension's configuration
    const config = vscode.workspace.getConfiguration('pmagentSpecMcp');
    const serverUrl = config.get<string>('serverUrl', 'http://localhost:8080/mcp');
    outputChannel.appendLine(`Read configuration serverUrl: ${serverUrl}`);

    // Register via settings.json (Stable API)
    updateMcpSettings(serverUrl);

    // Listen for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('pmagentSpecMcp.serverUrl')) {
                outputChannel.appendLine('Configuration changed, updating settings...');
                const newUrl = vscode.workspace.getConfiguration('pmagentSpecMcp')
                    .get<string>('serverUrl', 'http://localhost:8080/mcp');
                updateMcpSettings(newUrl);
            }
        })
    );
}

async function updateMcpSettings(url: string) {
    try {
        outputChannel.appendLine(`Attempting to update MCP settings with URL: ${url}`);
        
        // Get the global 'mcp' configuration
        const mcpConfig = vscode.workspace.getConfiguration('mcp');
        
        // Inspect where the setting is coming from
        const inspection = mcpConfig.inspect('servers');
        outputChannel.appendLine(`DEBUG INSPECTION: Global Value: ${JSON.stringify(inspection?.globalValue)}`);
        outputChannel.appendLine(`DEBUG INSPECTION: Workspace Value: ${JSON.stringify(inspection?.workspaceValue)}`);
        outputChannel.appendLine(`DEBUG INSPECTION: Default Value: ${JSON.stringify(inspection?.defaultValue)}`);

        const servers = mcpConfig.get<any>('servers') || {};

        // Optimization: Check if the server is already configured correctly
        if (servers['pmagent-spec'] && servers['pmagent-spec'].url === url) {
            outputChannel.appendLine('Server already configured correctly in one of the scopes. No changes made.');
            return; // No change needed
        }

        // Update the server configuration
        servers['pmagent-spec'] = {
            url: url
        };

        // Write back to Global settings (User settings)
        outputChannel.appendLine('Writing to Global settings...');
        await mcpConfig.update('servers', servers, vscode.ConfigurationTarget.Global);
        
        outputChannel.appendLine(`Success: PMAgent Spec MCP configured at ${url}`);
        vscode.window.showInformationMessage(`PMAgent Spec MCP configured at ${url}`);
    } catch (error) {
        outputChannel.appendLine(`Error: Failed to configure MCP server: ${error}`);
        console.error(error);
        vscode.window.showErrorMessage(`Failed to configure MCP server: ${error}`);
    }
}

export function deactivate() {}
