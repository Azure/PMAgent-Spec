# GitHub Copilot agent template for PMAgent MCP

This folder gives your users a ready-made `.agent.md` profile that locks GitHub Copilot (or VS Code Copilot Chat) onto the PMAgent MCP server even when many other MCP servers are registered.

## What is inside?

```
./.github/agents/pmagent-spec.agent.md
```

The file defines a **PMAgent Spec Orchestrator** agent that:

- Pins Copilot to the `pmagent-spec` MCP server tools (list specs, fetch specs, load tool manifests).  
- Teaches the agent to call `content_generation_best_practice → list_specs → fetch_spec → get_tool_manifest` before drafting anything.  
- Forces the final answer to explain which spec and tool manifests were used and to flag missing telemetry.

## How to use it in a repository

1. Ensure the PMAgent MCP server is already available to your users (for example by installing the `PMAgent Spec MCP` VS Code extension or by adding the server to their `~/.mcp` config).  
2. Copy the `.github/agents` folder from this template into the root of the target repository (create the folder if it does not exist).  
3. Commit the `pmagent-spec.agent.md` file so GitHub Copilot and IDEs can discover it. GitHub looks for custom agents under `.github/agents`, while VS Code/JetBrains let you edit the same file locally.  
4. Ask users to open Copilot Chat, open the agent dropdown, and choose **PMAgent Spec Orchestrator**. They can also use **Configure Custom Agents → Create New** to edit the template in-place.

## Customizing the template

- Update the `model` property if your organization prefers a different chat model.  
- Add more MCP tools (for example `github/*` or `azure-devops/*`) to the `tools` list if you want this agent to gather telemetry on its own.  
- Expand the instructions section to encode team-specific review rules or formatting requirements.

For background on how `.agent.md` files are loaded see:
- Visual Studio Code docs: [Custom agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- GitHub docs: [Creating custom agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
