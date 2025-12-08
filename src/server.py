import json
import os
from typing import Optional

import requests
import uvicorn
import yaml
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Spec Fetcher")

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "../spec")
PROMPT_DIR = os.path.join(DOCS_DIR, "../prompts")
TOOL_SPEC_DIR = os.path.join(BASE_DIR, "../tool_specs")

INDEX_FILE = os.path.join(DOCS_DIR, "index.yml")
PROMPT_FILE = os.path.join(PROMPT_DIR, "system_prompts.md")
TOOL_MANIFEST_FILE = os.path.join(TOOL_SPEC_DIR, "manifest.yml")
REPO_BASE_URL = "https://raw.githubusercontent.com/Azure/PMAgent-Spec/main"


def _load_tool_manifest():
    """Load the tool manifest (local preferred, remote fallback)."""

    data = None
    if os.path.exists(TOOL_MANIFEST_FILE):
        try:
            with open(TOOL_MANIFEST_FILE, "r") as f:
                data = yaml.safe_load(f)
        except Exception:
            data = None

    if not data:
        url = f"{REPO_BASE_URL}/tool_specs/manifest.yml"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = yaml.safe_load(response.text)
        except Exception:
            pass

    return data

@mcp.tool()
def content_generation_best_practice() -> str:
    """**ALWAYS CALL THIS FIRST** when generating any documentation, README, release notes, reports, or content.
    
    Returns essential best practices and system prompts for spec-driven content generation including:
    - Workflow rules and input validation requirements
    - Task planning and quality checklist criteria  
    - Output formatting standards
    
    Use before: README generation, revision history, product status reports, release notes, or any documentation task.
    """
    try:
        with open(PROMPT_FILE, 'r') as f:
            prompts = f.read()
            return prompts.strip()
    except Exception:
        return "Error: Could not read system prompts for best practice."

@mcp.tool()
def list_specs() -> str:
    """List all available content specification templates (SDK README, Revision History, Product Status Report, etc.).
    
    Use this to discover which specs are available before generating content.
    Returns spec names with descriptions to help choose the right template for your documentation task.
    
    Call this after content_generation_best_practice and before fetch_spec.
    """
    try:
        # Try local index first
        if os.path.exists(INDEX_FILE):
            try:
                with open(INDEX_FILE, 'r') as f:
                    data = yaml.safe_load(f)
            except Exception:
                data = None
        else:
            data = None
            
        # If local failed or empty, try remote
        if not data:
             url = f"{REPO_BASE_URL}/spec/index.yml"
             try:
                 response = requests.get(url)
                 if response.status_code == 200:
                     data = yaml.safe_load(response.text)
             except Exception:
                 pass

        if not data:
            return "No specifications found (checked local and remote)."

        result = "Available Specifications:\n"
        for item in data:
            name = item.get('name', 'Unknown')
            desc = item.get('description', 'No description')
            result += f"- {name}: {desc}\n"
        
        return result
    except Exception as e:
        return f"Error reading index: {str(e)}"


def _lookup_tool_entry(manifest: dict, name: str) -> Optional[dict]:
    for tool in manifest.get("tools", []):
        if tool.get("name") == name:
            return tool
    return None


@mcp.tool()
def get_tool_manifest(name: Optional[str] = None) -> str:
    """Return machine-readable metadata describing reusable tool specs.

    Use this to understand which MCP servers/toolsets (GitHub, Azure DevOps, etc.)
    are documented, along with their capabilities, fallback plans, and example
    sequences. Hosts should call this before planning cross-server automation.

    Args:
        name: Optional tool spec name. When omitted, returns the entire manifest.
    """

    manifest = _load_tool_manifest()

    if not manifest:
        return "Error: Could not load tool manifest (local or remote)."

    if name:
        entry = _lookup_tool_entry(manifest, name)
        if entry:
            return json.dumps(entry, indent=2)
        return f"Error: Tool spec '{name}' not found in manifest."

    return json.dumps(manifest, indent=2)


@mcp.tool()
def fetch_tool_spec(name: str) -> str:
    """Fetch the markdown tool spec referenced by content specs.

    Args:
        name: Tool spec name from the tool manifest (e.g., 'github_mcp').
    """

    manifest = _load_tool_manifest()
    if not manifest:
        return "Error: Could not load tool manifest (local or remote)."

    entry = _lookup_tool_entry(manifest, name)
    if not entry:
        return f"Error: Tool spec '{name}' not found in manifest."

    spec_file = entry.get("spec_file")
    if not spec_file:
        return f"Error: Tool spec '{name}' does not define a spec_file."

    normalized_path = os.path.normpath(spec_file)
    local_path = os.path.join(TOOL_SPEC_DIR, normalized_path)

    if os.path.exists(local_path):
        try:
            with open(local_path, "r") as f:
                return f.read()
        except Exception:
            pass

    url = f"{REPO_BASE_URL}/tool_specs/{normalized_path}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        if response.status_code == 404:
            return (
                f"Error: Tool spec file '{normalized_path}' not found locally or remotely (404).\n"
                f"URL: {url}"
            )
        return f"Error: Failed to fetch tool spec. Status code: {response.status_code}"
    except Exception as exc:
        return f"Error fetching tool spec: {str(exc)}"

@mcp.tool()
def fetch_spec(name: str) -> str:
    """Fetch a complete specification template defining structure, sections, inputs, and quality criteria for content generation.
    
    Use this after calling list_specs to get the full spec for your chosen documentation type.
    The spec includes: required inputs, section structure, tone guidelines, task planning rules, and quality checklist.
    
    Args:
        name: The name of the spec as shown in list_specs.
    """
    try:
        # 1. Get Index Data (Local or Remote)
        data = None
        if os.path.exists(INDEX_FILE):
            try:
                with open(INDEX_FILE, 'r') as f:
                    data = yaml.safe_load(f)
            except Exception:
                data = None
        
        if not data:
             url = f"{REPO_BASE_URL}/spec/index.yml"
             try:
                 response = requests.get(url)
                 if response.status_code == 200:
                     data = yaml.safe_load(response.text)
             except Exception:
                 pass
        
        if not data:
             return "Error: Could not load index file (local or remote)."

        # Find the file associated with the name
        target_file = None
        for item in data:
            if item.get('name') == name:
                target_file = item.get('file')
                break
        
        if not target_file:
            return f"Error: Spec '{name}' not found in index."
        
        normalized_path = os.path.normpath(target_file)

        # 2. Try Fetching Local File
        local_file_path = os.path.join(DOCS_DIR, normalized_path)
        if os.path.exists(local_file_path):
            try:
                with open(local_file_path, 'r') as f:
                    return f.read()
            except Exception:
                pass # Fall through to remote
        
        # 3. Try Fetching Remote File
        url = f"{REPO_BASE_URL}/spec/{normalized_path}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            return f"Error: Spec file '{normalized_path}' not found locally or in public repository (404).\nURL: {url}"
        else:
            return f"Error: Failed to fetch spec. Status code: {response.status_code}"

    except Exception as e:
        return f"Error fetching spec: {str(e)}"

if __name__ == "__main__":
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=8100)
