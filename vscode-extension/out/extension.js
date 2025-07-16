"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const cp = require("child_process");
function activate(context) {
    const outputChannel = vscode.window.createOutputChannel('AutoDocGen');
    const disposable = vscode.commands.registerCommand('autodocgen.run', () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace is open.');
            return;
        }
        const workspacePath = workspaceFolders[0].uri.fsPath;
        outputChannel.clear(); // Optional: clear previous logs
        outputChannel.show(true); // Focus the output panel
        outputChannel.appendLine(`📦 Running AutoDocGen in: ${workspacePath}`);
        const outputPath = `${workspacePath}/__autodocs__`;
        const args = ['-m', 'autodocgen', 'run', '--path', workspacePath, '--output-dir', outputPath, '--use-ai', '--inject-docs'];
        const python = cp.spawn('python', args);
        python.stdout.on('data', (data) => {
            outputChannel.appendLine(`🟢 ${data.toString()}`);
        });
        python.stderr.on('data', (data) => {
            outputChannel.appendLine(`🔴 ${data.toString()}`);
            vscode.window.showErrorMessage('AutoDocGen encountered an error. See output for details.');
        });
        python.on('close', (code) => {
            outputChannel.appendLine(`✅ AutoDocGen finished with exit code ${code}`);
            vscode.window.showInformationMessage(`AutoDocGen finished with code ${code}`);
        });
    });
    context.subscriptions.push(disposable);
    const guiDisposable = vscode.commands.registerCommand('autodocgen.runGui', () => {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            vscode.window.showErrorMessage('No workspace is open.');
            return;
        }
        const workspacePath = workspaceFolders[0].uri.fsPath;
        outputChannel.clear(); // Optional: clear previous logs
        outputChannel.show(true); // Focus the output panel
        outputChannel.appendLine(`📊 Launching AutoDocGen GUI in: ${workspacePath}`);
        const args = ['-m', 'autodocgen', 'gui'];
        const python = cp.spawn('python', args);
        python.stdout.on('data', (data) => {
            outputChannel.appendLine(`🟢 ${data.toString()}`);
        });
        python.stderr.on('data', (data) => {
            outputChannel.appendLine(`🔴 ${data.toString()}`);
            vscode.window.showErrorMessage('AutoDocGen GUI encountered an error. See output for details.');
        });
        python.on('close', (code) => {
            outputChannel.appendLine(`✅ AutoDocGen GUI finished with exit code ${code}`);
            vscode.window.showInformationMessage(`AutoDocGen GUI finished with code ${code}`);
        });
    });
    context.subscriptions.push(guiDisposable);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map