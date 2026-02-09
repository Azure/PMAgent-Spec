---
name: pmagent-spec
description: Use PMAgent-Spec MCP to fetch PMAgent content specs (Monday Minutes, revision histories, OKR reports, SDK READMEs, etc.) and the tool manifests that map specs to telemetry MCP servers.
---

# PMAgent-Spec

## When to use

Use this skill whenever you need:
- PMAgent writing guardrails (`content_generation_best_practice`)
- A list of available specs (`list_specs`)
- A spec template/body to follow (`fetch_spec`)
- The telemetry call mapping for a spec (`get_tool_manifest`)

## Quick start

1. Call `content_generation_best_practice`
2. Call `list_specs` to find the right spec name
3. Call `fetch_spec` for the spec and follow it
4. If the spec needs telemetry, call `get_tool_manifest(<spec>)` and then use the referenced MCP servers/tools
