import logging
import os
from typing import Optional

import requests
import yaml
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Spec Fetcher", host="0.0.0.0", port=8100)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "../spec")
PROMPT_DIR = os.path.join(DOCS_DIR, "../prompts")
TOOL_SPEC_DIR = os.path.join(BASE_DIR, "../tool_specs")

INDEX_FILE = os.path.join(DOCS_DIR, "index.yml")
PROMPT_FILE = os.path.join(PROMPT_DIR, "system_prompts.md")
REPO_BASE_URL = "https://raw.githubusercontent.com/Azure/PMAgent-Spec/main"


def _tool_spec_candidates(name: str):
    """Return possible filenames for the requested tool spec."""
    base = name.strip()
    return [f"{base}.yml", f"{base}.yaml"]


def _read_tool_spec_text(name: str) -> Optional[str]:
    """Load a tool spec file (local preferred, remote fallback)."""

    for candidate in _tool_spec_candidates(name):
        local_path = os.path.join(TOOL_SPEC_DIR, candidate)
        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logger.exception("Failed to read tool spec from %s: %s", local_path, e)

        url = f"{REPO_BASE_URL}/tool_specs/{candidate}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logger.exception("Failed to fetch tool spec from %s: %s", url, e)

    return None


def _list_available_tool_specs():
    """List tool spec names discovered locally."""

    if not os.path.isdir(TOOL_SPEC_DIR):
        return []

    names = []
    for filename in os.listdir(TOOL_SPEC_DIR):
        if filename.lower().endswith((".yml", ".yaml")):
            names.append(os.path.splitext(filename)[0])
    return sorted(set(names))


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
        with open(PROMPT_FILE, 'r', encoding="utf-8") as f:
            prompts = f.read()
            return prompts.strip()
    except Exception as e:
        logger.exception("Failed to read system prompts from %s: %s", PROMPT_FILE, e)
        return f"Error: Could not read system prompts for best practice: {str(e)}"

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
                with open(INDEX_FILE, 'r', encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            except Exception as e:
                data = None
                logger.exception("Failed to read local index file %s: %s", INDEX_FILE, e)
        else:
            data = None
            
        # If local failed or empty, try remote
        if not data:
             url = f"{REPO_BASE_URL}/spec/index.yml"
             try:
                 response = requests.get(url)
                 if response.status_code == 200:
                     data = yaml.safe_load(response.text)
             except Exception as e:
                 logger.exception("Failed to fetch index from %s: %s", url, e)

        if not data:
            return "No specifications found (checked local and remote)."

        result = "Available Specifications:\n"
        for item in data:
            name = item.get('name', 'Unknown')
            desc = item.get('description', 'No description')
            result += f"- {name}: {desc}\n"
        
        return result
    except Exception as e:
        logger.exception("Unhandled error while listing specs")
        return f"Error reading index: {str(e)}"


@mcp.tool()
def get_tool_manifest(name: Optional[str] = None) -> str:
    """Get a tool helpers that defined in a specific spec. 
    
    If spec have tool dependencies, use this after fetch_spec to get tools usage helper.
    If no name is provided, list all available tool specs."""

    if name:
        text = _read_tool_spec_text(name)
        if text:
            return text
        return f"Error: Tool spec '{name}' not found, try directly use '{name}' mcp tools."

    specs = _list_available_tool_specs()
    if not specs:
        return "Error: No tool specs found. try directly use '{name}' mcp tools."

    joined = "\n".join(f"- {spec_name}" for spec_name in specs)
    return f"Available tool specs:\n{joined}"

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
                with open(INDEX_FILE, 'r', encoding="utf-8") as f:
                    data = yaml.safe_load(f)
            except Exception as e:
                data = None
                logger.exception("Failed to read local index file %s: %s", INDEX_FILE, e)
        
        if not data:
             url = f"{REPO_BASE_URL}/spec/index.yml"
             try:
                 response = requests.get(url)
                 if response.status_code == 200:
                     data = yaml.safe_load(response.text)
             except Exception as e:
                 logger.exception("Failed to fetch index from %s: %s", url, e)
        
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
                with open(local_file_path, 'r', encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logger.exception("Failed to read spec from %s: %s", local_file_path, e)
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
        logger.exception("Unhandled error while fetching spec")
        return f"Error fetching spec: {str(e)}"

if __name__ == "__main__":
    # Run with the MCP Streamable HTTP transport (chunked responses over POST)
    mcp.run(transport="streamable-http")
