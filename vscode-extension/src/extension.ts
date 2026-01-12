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

    // Commands to manage the agent template on demand
    context.subscriptions.push(
        vscode.commands.registerCommand('pmagentSpecMcp.installAgent', () => installAgentTemplate(context)),
        vscode.commands.registerCommand('pmagentSpecMcp.removeAgent', removeAgentTemplate)
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

type WorkspacePickItem = vscode.QuickPickItem & { folder: vscode.WorkspaceFolder };

async function pickWorkspaceFolder(placeHolder: string): Promise<vscode.WorkspaceFolder | undefined> {
    const workspaces = vscode.workspace.workspaceFolders;
    if (!workspaces || workspaces.length === 0) {
        outputChannel.appendLine('No workspace open; cannot manage agent template.');
        vscode.window.showWarningMessage('Open a workspace before managing the PMAgent agent.');
        return undefined;
    }

    if (workspaces.length === 1) {
        return workspaces[0];
    }

    const selection = await vscode.window.showQuickPick(
        workspaces.map<WorkspacePickItem>(folder => ({
            label: folder.name,
            description: folder.uri.fsPath,
            folder
        })),
        { placeHolder }
    );

    return selection?.folder;
}

async function readBundledTemplate(context: vscode.ExtensionContext): Promise<Uint8Array | undefined> {
    const templateUri = vscode.Uri.joinPath(context.extensionUri, 'resources', 'pmagent.agent.md');
    try {
        return await vscode.workspace.fs.readFile(templateUri);
    } catch (error) {
        outputChannel.appendLine(`Error reading bundled agent template: ${error}`);
        vscode.window.showErrorMessage('Failed to read bundled PMAgent agent template.');
        return undefined;
    }
}

async function installAgentTemplate(context: vscode.ExtensionContext) {
    const workspace = await pickWorkspaceFolder('Select a workspace to install the PMAgent agent template');
    if (!workspace) {
        return;
    }

    const templateContent = await readBundledTemplate(context);
    if (!templateContent) {
        return;
    }

    const agentsDir = vscode.Uri.joinPath(workspace.uri, '.github', 'agents');
    const targetUri = vscode.Uri.joinPath(agentsDir, 'pmagent.agent.md');

    let shouldWrite = true;
    try {
        await vscode.workspace.fs.stat(targetUri);
        const choice = await vscode.window.showWarningMessage(
            `pmagent.agent.md already exists in ${workspace.name}. Replace it?`,
            { modal: true },
            'Replace'
        );
        shouldWrite = choice === 'Replace';
    } catch (error) {
        if (!(error instanceof vscode.FileSystemError) || error.code !== 'FileNotFound') {
            outputChannel.appendLine(`Could not check for existing agent at ${targetUri.fsPath}: ${error}`);
            vscode.window.showErrorMessage('Could not verify existing PMAgent agent file.');
            return;
        }
    }

    if (!shouldWrite) {
        outputChannel.appendLine('Install aborted by user; existing agent left untouched.');
        return;
    }

    try {
        await vscode.workspace.fs.createDirectory(agentsDir);
        await vscode.workspace.fs.writeFile(targetUri, templateContent);
        outputChannel.appendLine(`Copied PMAgent Copilot agent template to ${targetUri.fsPath}`);
        vscode.window.showInformationMessage(`PMAgent agent installed to ${workspace.name}.`);
    } catch (error) {
        outputChannel.appendLine(`Failed to copy agent template to ${targetUri.fsPath}: ${error}`);
        vscode.window.showErrorMessage('Failed to install PMAgent agent template.');
    }
}

async function removeAgentTemplate() {
    const workspace = await pickWorkspaceFolder('Select a workspace to remove the PMAgent agent template');
    if (!workspace) {
        return;
    }

    const targetUri = vscode.Uri.joinPath(workspace.uri, '.github', 'agents', 'pmagent.agent.md');

    try {
        await vscode.workspace.fs.stat(targetUri);
    } catch (error) {
        if (error instanceof vscode.FileSystemError && error.code === 'FileNotFound') {
            vscode.window.showInformationMessage('No PMAgent agent file found to remove.');
            outputChannel.appendLine(`No agent file at ${targetUri.fsPath}; nothing to remove.`);
            return;
        }
        outputChannel.appendLine(`Could not check for existing agent at ${targetUri.fsPath}: ${error}`);
        vscode.window.showErrorMessage('Could not verify existing PMAgent agent file.');
        return;
    }

    const confirmation = await vscode.window.showWarningMessage(
        `Remove pmagent.agent.md from ${workspace.name}?`,
        { modal: true },
        'Remove'
    );
    if (confirmation !== 'Remove') {
        outputChannel.appendLine('Remove aborted by user.');
        return;
    }

    try {
        await vscode.workspace.fs.delete(targetUri);
        outputChannel.appendLine(`Removed PMAgent agent template from ${targetUri.fsPath}`);
        vscode.window.showInformationMessage(`PMAgent agent removed from ${workspace.name}.`);
    } catch (error) {
        outputChannel.appendLine(`Failed to remove agent template from ${targetUri.fsPath}: ${error}`);
        vscode.window.showErrorMessage('Failed to remove PMAgent agent template.');
    }
}

export function deactivate() {}
