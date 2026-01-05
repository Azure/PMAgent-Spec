import logging
import re
from pathlib import Path
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

# Define paths (cross-platform)
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
DOCS_DIR = ROOT_DIR / "spec"
PROMPT_DIR = ROOT_DIR / "prompts"
TOOL_SPEC_DIR = ROOT_DIR / "tool_specs"
TEMPLATE_DIR = ROOT_DIR / "templates"

INDEX_FILE = DOCS_DIR / "index.yml"
PROMPT_FILE = PROMPT_DIR / "system_prompts.md"
REPO_BASE_URL = "https://raw.githubusercontent.com/Azure/PMAgent-Spec/main"


def _tool_spec_candidates(name: str):
    """Return possible filenames for the requested tool spec."""
    base = name.strip()
    return [f"{base}.yml", f"{base}.yaml"]


def _read_tool_spec_text(name: str) -> Optional[str]:
    """Load a tool spec file (local preferred, remote fallback)."""

    for candidate in _tool_spec_candidates(name):
        local_path = TOOL_SPEC_DIR / candidate
        if local_path.exists():
            try:
                with local_path.open("r", encoding="utf-8") as f:
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

    if not TOOL_SPEC_DIR.is_dir():
        return []

    names = []
    for path in TOOL_SPEC_DIR.iterdir():
        if path.suffix.lower() in (".yml", ".yaml"):
            names.append(path.stem)
    return sorted(set(names))


def _load_template_file_by_name(name: str) -> Optional[str]:
    """Load a template by explicit filename (local preferred, remote fallback)."""
    candidates = [name]
    if not name.lower().endswith(".md"):
        candidates.append(f"{name}.md")

    seen = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)

        local_path = TEMPLATE_DIR / candidate
        if local_path.exists():
            try:
                with local_path.open("r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logger.exception("Failed to read template from %s: %s", local_path, e)

        url = f"{REPO_BASE_URL}/templates/{candidate}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            logger.exception("Failed to fetch template from %s: %s", url, e)

    return None


def _inject_template_placeholders(spec_text: str):
    """Replace placeholders like {{filename.md}} with the contents of templates/filename.md."""
    placeholder_pattern = re.compile(r"\{\{\s*([^\{\}\s]+)\s*\}\}")
    used_templates = set()

    def _replace(match: re.Match):
        token = match.group(1).strip()
        content = _load_template_file_by_name(token)
        if content is None:
            return match.group(0)  # leave placeholder untouched
        used_templates.add(token if token.lower().endswith(".md") else f"{token}.md")
        return content.strip()

    replaced_text = placeholder_pattern.sub(_replace, spec_text)
    return replaced_text, used_templates


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
        with PROMPT_FILE.open('r', encoding="utf-8") as f:
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
        if INDEX_FILE.exists():
            try:
                with INDEX_FILE.open('r', encoding="utf-8") as f:
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
        if INDEX_FILE.exists():
            try:
                with INDEX_FILE.open('r', encoding="utf-8") as f:
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
        
        normalized_path = Path(target_file)

        # 2. Try Fetching Local File
        local_file_path = DOCS_DIR / normalized_path
        spec_text = None
        if local_file_path.exists():
            try:
                with local_file_path.open('r', encoding="utf-8") as f:
                    spec_text = f.read()
            except Exception as e:
                logger.exception("Failed to read spec from %s: %s", local_file_path, e)
                spec_text = None  # Fall through to remote
        
        # 3. Try Fetching Remote File
        normalized_remote_path = normalized_path.as_posix()
        url = f"{REPO_BASE_URL}/spec/{normalized_remote_path}"
        
        if spec_text is None:
            response = requests.get(url)
            
            if response.status_code == 200:
                spec_text = response.text
            elif response.status_code == 404:
                return f"Error: Spec file '{normalized_remote_path}' not found locally or in public repository (404).\nURL: {url}"
            else:
                return f"Error: Failed to fetch spec. Status code: {response.status_code}"

        # 4. Inject template placeholders if present
        spec_text, _ = _inject_template_placeholders(spec_text)

        return spec_text

    except Exception as e:
        logger.exception("Unhandled error while fetching spec")
        return f"Error fetching spec: {str(e)}"

if __name__ == "__main__":
    # Run with the MCP Streamable HTTP transport (chunked responses over POST)
    mcp.run(transport="streamable-http")
