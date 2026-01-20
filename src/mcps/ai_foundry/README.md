# AI Foundry MCP Proxy

Thin MCP server that forwards a prompt to a single Azure AI Foundry agent. The endpoint and agent name are chosen when the server starts; each MCP call just passes the prompt through unchanged.

## Prerequisites
- Python 3.11+
- Install deps (uses the prerelease Azure AI Projects SDK): `pip install -r src/requirements.txt --pre`
- `DefaultAzureCredential` must work for the project endpoint (set `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`, or login with `az login`).

## Configure
- `AI_FOUNDRY_ENDPOINT`: Project endpoint (e.g., `https://.../api/projects/<project-name>`).
- `AI_FOUNDRY_AGENT_NAME`: Agent to target.
- Optional: `AI_FOUNDRY_HOST` (default `0.0.0.0`) and `AI_FOUNDRY_PORT` (default `8110`).

You can also pass `--endpoint`, `--agent`, `--host`, and `--port` on the command line. Missing `endpoint` or `agent` will abort startup.

## Run
- Package path: `python -m mcps.ai_foundry.server --endpoint <endpoint> --agent <agent-name>`
- Hyphenated path helper: `python src/mcps/ai-foundry/server.py --endpoint <endpoint> --agent <agent-name>`

## MCP tool
- `invoke_ai_foundry(prompt: str) -> str`: sends the prompt as a single user message to the configured agent and returns `response.output_text`.

Register with an MCP client (example):
```json
{
  "mcpServers": {
    "ai-foundry": {
      "transport": { "type": "http", "url": "http://localhost:8110/mcp" }
    }
  }
}
```
