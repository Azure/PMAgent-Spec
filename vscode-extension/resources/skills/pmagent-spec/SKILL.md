---
name: pmagent-spec
description: Spec-driven PM workflows using PMAgent MCP tools (Monday Minutes, OKRs, product status reports, SDK README, revision history). Use when generating or updating PMAgent specs and related docs.
---

# PMAgent Spec Workflows

## When to use

- You are creating or updating PMAgent specification-driven documents (SDK README, revision history, Monday Minutes, OKR reports, product status reports).
- You need to follow the spec templates in this repo and avoid inventing structure.
- You need telemetry-derived content (GitHub, Azure DevOps, Kusto, Power BI) and should rely on the PMAgent MCP tooling first.

## Required workflow

1. Start by running the PMAgent MCP best-practices tool (content generation best practice) before you draft a plan.
2. If a spec template exists for the deliverable, follow it exactly (section names, required inputs, tone guidance, quality criteria).
3. Prefer data-backed statements. If data is missing, explicitly ask for the missing inputs or state the assumption.
4. Keep output concise, scannable, and aligned with the repository’s formatting conventions.

## Inputs checklist

- Deliverable type (e.g., Monday Minutes, Product Status Report, SDK README, Revision History)
- Timeframe / iteration
- Telemetry sources in scope (GitHub, Azure DevOps, Kusto, Power BI)
- Known blockers / risks

## Notes

- This skill is intended to be used together with the PMAgent MCP server and the repo’s spec templates under `spec/`.
