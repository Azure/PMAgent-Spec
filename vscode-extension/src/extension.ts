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

    // Place the Copilot skill into the workspace if needed
    void ensureSkillTemplate(context, { overwrite: false });

    context.subscriptions.push(
        vscode.commands.registerCommand('pmagentSpecMcp.installSkill', async () => {
            await ensureSkillTemplate(context, { overwrite: true, showNotifications: true });
        })
    );

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

async function ensureSkillTemplate(
    context: vscode.ExtensionContext,
    options: { overwrite: boolean; showNotifications?: boolean }
) {
    const workspaces = vscode.workspace.workspaceFolders;
    if (!workspaces || workspaces.length === 0) {
        outputChannel.appendLine('No workspace open; skipping skill copy.');
        if (options.showNotifications) {
            vscode.window.showWarningMessage('No workspace is open; cannot install Copilot skill.');
        }
        return;
    }

    const templateUri = vscode.Uri.joinPath(
        context.extensionUri,
        'resources',
        'skills',
        'pmagent-spec',
        'SKILL.md'
    );

    let templateContent: Uint8Array;
    try {
        templateContent = await vscode.workspace.fs.readFile(templateUri);
    } catch (error) {
        outputChannel.appendLine(`Error reading bundled skill template: ${error}`);
        if (options.showNotifications) {
            vscode.window.showErrorMessage(`Failed to read bundled skill template: ${error}`);
        }
        return;
    }

    let installedCount = 0;
    let skippedCount = 0;
    let failedCount = 0;

    for (const workspace of workspaces) {
        const skillsDir = vscode.Uri.joinPath(workspace.uri, '.github', 'skills', 'pmagent-spec');
        const targetUri = vscode.Uri.joinPath(skillsDir, 'SKILL.md');

        if (!options.overwrite) {
            try {
                await vscode.workspace.fs.stat(targetUri);
                outputChannel.appendLine(`Skill already exists at ${targetUri.fsPath}; leaving it untouched.`);
                skippedCount++;
                continue;
            } catch (error) {
                if (!(error instanceof vscode.FileSystemError) || error.code !== 'FileNotFound') {
                    outputChannel.appendLine(`Could not check for existing skill at ${targetUri.fsPath}: ${error}`);
                    failedCount++;
                    continue;
                }
            }
        }

        try {
            await vscode.workspace.fs.createDirectory(skillsDir);
            await vscode.workspace.fs.writeFile(targetUri, templateContent);
            outputChannel.appendLine(`Installed PMAgent Copilot skill to ${targetUri.fsPath}`);
            installedCount++;
        } catch (error) {
            outputChannel.appendLine(`Failed to install skill to ${targetUri.fsPath}: ${error}`);
            failedCount++;
        }
    }

    if (options.showNotifications) {
        if (failedCount > 0) {
            vscode.window.showWarningMessage(
                `Installed Copilot skill to ${installedCount} workspace(s); ${skippedCount} unchanged; ${failedCount} failed.`
            );
        } else {
            vscode.window.showInformationMessage(
                `Installed Copilot skill to ${installedCount} workspace(s); ${skippedCount} unchanged.`
            );
        }
    }
}

export function deactivate() {}
