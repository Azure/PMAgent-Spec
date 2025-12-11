import * as vscode from 'vscode';

// Create an output channel to see logs in the "Output" tab
const outputChannel = vscode.window.createOutputChannel("PMAgent MCP");

export function activate(context: vscode.ExtensionContext) {
    outputChannel.show(true); // Show the channel immediately
    outputChannel.appendLine('PMAgent Spec MCP extension is activating...');

    // Get the MCP server URL from our extension's configuration
    const config = vscode.workspace.getConfiguration('pmagentSpecMcp');
    const serverUrl = config.get<string>('serverUrl');
    if (!serverUrl) {
        outputChannel.appendLine('Error: No serverUrl configured.');
        return;
    }
    outputChannel.appendLine(`Read configuration serverUrl: ${serverUrl}`);

    // Register via settings.json (Stable API)
    updateMcpSettings(serverUrl);

    // Place the Copilot agent template into the workspace if needed
    void ensureAgentTemplate(context);

    // Listen for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('pmagentSpecMcp.serverUrl')) {
                outputChannel.appendLine('Configuration changed, updating settings...');
                const newUrl = vscode.workspace.getConfiguration('pmagentSpecMcp')
                    .get<string>('serverUrl');
                if (newUrl) {
                    updateMcpSettings(newUrl);
                }
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
        const desiredConfig = { type: "http", url };
        const currentConfig = servers['pmagent-spec'];
        if (currentConfig && currentConfig.url === url && currentConfig.type === desiredConfig.type) {
            outputChannel.appendLine('Server already configured correctly in one of the scopes. No changes made.');
            return; // No change needed
        }

        // Update the server configuration
        servers['pmagent-spec'] = desiredConfig;

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

async function ensureAgentTemplate(context: vscode.ExtensionContext) {
    const workspaces = vscode.workspace.workspaceFolders;
    if (!workspaces || workspaces.length === 0) {
        outputChannel.appendLine('No workspace open; skipping agent template copy.');
        return;
    }

    const templateUri = vscode.Uri.joinPath(context.extensionUri, 'resources', 'pmagent.agent.md');
    let templateContent: Uint8Array;
    try {
        templateContent = await vscode.workspace.fs.readFile(templateUri);
    } catch (error) {
        outputChannel.appendLine(`Error reading bundled agent template: ${error}`);
        return;
    }

    for (const workspace of workspaces) {
        const agentsDir = vscode.Uri.joinPath(workspace.uri, '.github', 'agents');
        const targetUri = vscode.Uri.joinPath(agentsDir, 'pmagent.agent.md');

        try {
            await vscode.workspace.fs.stat(targetUri);
            outputChannel.appendLine(`Agent template already exists at ${targetUri.fsPath}; leaving it untouched.`);
            continue;
        } catch (error) {
            if (!(error instanceof vscode.FileSystemError) || error.code !== 'FileNotFound') {
                outputChannel.appendLine(`Could not check for existing agent at ${targetUri.fsPath}: ${error}`);
                continue;
            }
        }

        try {
            await vscode.workspace.fs.createDirectory(agentsDir);
            await vscode.workspace.fs.writeFile(targetUri, templateContent);
            outputChannel.appendLine(`Copied PMAgent Copilot agent template to ${targetUri.fsPath}`);
        } catch (error) {
            outputChannel.appendLine(`Failed to copy agent template to ${targetUri.fsPath}: ${error}`);
        }
    }
}

export function deactivate() {}
