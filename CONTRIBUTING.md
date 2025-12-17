# Contributing to PMAgent-Spec

Thanks for helping improve the PMAgent spec server and extension! This guide keeps contributions predictable and easy to review.

## How to contribute

- **Propose a change**: File an issue or start a discussion with the problem you are solving and the spec(s) or tool manifests it touches.
- **Work in a branch**: Create a feature branch and keep commits focused on a single concern.
- **Align with specs**: When adding or updating specs or tool manifests, ensure names are listed in `spec/index.yml` and include clear descriptions.

## Development checklist

- Set up Python dependencies in `src/` with `pip install -r requirements.txt`.
- For VS Code extension changes, run `npm install && npm run compile` in `vscode-extension/`.
- Exercise the MCP server locally via `python src/server.py` and point your MCP client to `http://localhost:8100/mcp`.

## Before opening a PR

- Run any relevant checks (linters, formatters, or smoke tests for the server/extension).
- Update documentation when behaviors or endpoints change.
- Keep diffs minimal; avoid reformatting unrelated files.

Questions or ideas? Open an issue so we can discuss early.
