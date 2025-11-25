# Spec: SDK README Generator
Version: 1.0  
Content-Type: SDK Documentation  
Authoring-Mode: AI

---

## 1. Purpose
This spec defines how the agent should generate a **complete, production-quality README.md** for a software development kit (SDK). The README must be generated directly from the SDK’s codebase, including:

- Exposed public functions, classes, and modules  
- Dependencies  
- Installation instructions  
- Usage examples  
- Best practices  
- Versioning information  

The SDK may reside in:
- A GitHub repository (via GitHub MCP server)  
- A local workspace (via local file system MCP server)

The final README must follow a consistent, professional format suitable for GitHub or package managers.

---

## 2. Audience
- Developers integrating or evaluating the SDK  
- Open-source contributors  
- Engineering teams using the SDK internally  
- Technical PMs and architects

**Expertise level:** Intermediate developer  
**Reading context:** GitHub README, package registry (npm, pip, etc.), internal documentation portal

---

## 3. Tone & Style Guidelines
- Professional, concise, developer-friendly  
- Use **second person** (“You can…”)  
- Favor clarity, technical accuracy, and code-first explanations  
- Avoid promotional or marketing tone  
- Provide runnable, verified code blocks  

**Prohibited:**
- Hallucinated APIs or behaviors  
- Overly vague or fluffy descriptions  
- Incorrect file or module names  
- Speculative content not backed by actual code

---

## 4. Required Inputs
The agent must gather the following inputs before generating the README:

### From the SDK Codebase
- List of exported modules and namespaces  
- Public classes, interfaces, methods, and functions  
- Constructor signatures and argument lists  
- Parameter types, return values, and default parameters  
- Runtime dependencies  
- Supported platforms/environments  
- Entry points or main modules  
- Public constants or configuration objects (if any)

### From Examples / Samples
- Code samples located in `/examples`, `/sample`, `/demo`, or similar directories  
- End-to-end runnable examples  
- Example usage patterns or tests that demonstrate intended SDK usage  

### From Metadata Files
- SDK name and description  
- Installation instructions derived from:
  - `package.json`, `pyproject.toml`, `setup.py`, `go.mod`, or similar  
- Licensing information from `LICENSE`  
- Repository links  
- Release notes or CHANGELOG if available  

### Supported Sources via MCP Tools
- **GitHub MCP**: repository files, directories, tags, releases, metadata  
- **Local FileSystem MCP**: local code, examples, manifests  
- **Optional**: web search or package registry lookup for validation

If critical inputs are missing, the agent must ask the user for clarification or alternate paths.

---

## 5. Section Structure
The final README **must** contain the following sections in order:

1. **Title & Description**  
2. **Key Features**  
3. **Installation**  
4. **Quick Start**  
5. **API Overview**  
    - Modules  
    - Classes  
    - Functions  
6. **Examples**  
7. **Dependency Graph**  
8. **Supported Environments**  
9. **Versioning & Release Notes (Optional)**  
10. **Contributing**  
11. **License**

---

## 6. Detailed Section Requirements

### Title & Description
- Title equals the SDK name  
- Description must reflect the SDK’s actual purpose  
- Can include badges (build, version, license) if available  
- Must not include invented features

---

### Key Features
- 3–7 bullet points summarizing primary SDK capabilities  
- Must be derived from actual code structure and APIs  
- No invented or speculative capabilities  

---

### Installation
- Provide real installation commands based on metadata files. 
- Must includes: 
  - Package manager commands
  - Manual installation (if applicable)
  - Runtime language versions required  
  - OS or environment constraints  

Examples (per language):

```shell
npm install <package>
pip install <package>
go get <module>
```

---

### Quick Start
- Provide a **minimal, runnable code example**  
- Must import real modules and call real functions  
- Must compile or run if copied into a user project  

---

### API Overview
For each module or namespace:

#### Module Summary
- Module name  
- One-line description  
- What it contains (classes, functions)

#### API Tables
For each API item:

- Name  
- Signature  
- Parameters  
- Return type  
- Description  
- Notes (optional)  

Example:

| Name | Parameters | Returns | Description |
|------|------------|---------|-------------|

---

### Examples
- Extract from `examples/`, `samples/`, or similar directories  
- Provide runnable snippets  
- Highlight common patterns or best practices  

---

### Dependency Graph
Extracted from project metadata:

- Runtime dependencies  
- Development dependencies  
- Optional / peer dependencies  
- External services or APIs the SDK communicates with  

Format:
- Markdown list  
- or simple ASCII dependency diagram  

---

### Supported Environments
Include:
- OS compatibility  
- Runtime versions (Node, Python, Go, browser)  
- Any known limitations  

---

### Versioning & Release Notes (Optional)
- Summarize the latest release  
- Extract from CHANGELOG or GitHub releases  
- Include semantic version rules if available  

---

### Contributing
- Link to CONTRIBUTING.md if present  
- Instructions for filing issues and PRs  
- Development environment setup  
- Code of Conduct link if present  

---

### License
- Extract exact license name from `LICENSE` file  
- Provide a direct link to the license in the repo  

---

## 7. Task Planning Rules for Agent
To fulfill this spec, the agent must:

1. Detect whether SDK source is from GitHub or local file system  
2. Retrieve all required files from appropriate locations  
3. Build internal representations:  
   - API list  
   - Modules and functions  
   - Examples  
   - Dependencies  
4. Identify missing data and request user input if essential  
5. Summarize and normalize retrieved content  
6. Generate README sections in the exact order defined  
7. Validate the content against the Quality Checklist  
8. Regenerate sections that fail validation  
9. Produce final README.md

---

## 8. Required Tools (MCP)
- **GitHub MCP Tool**  
  - Read files  
  - Read directories  
  - Get tags, releases, branches  

- **Local FileSystem MCP Tool**  
  - Access code and examples in local workspace  

- **Optional: Package Registry or Search Tools**  
  - Validate installation commands  
  - Fetch metadata  

---

## 9. Quality Checklist

### Structure
- All required sections present  
- Sections appear in correct order  
- Markdown headings are valid and well formatted  

### Content Accuracy
- APIs match real code exactly  
- Examples use real modules and functions  
- Parameter names and signatures are correct  
- Dependencies accurately reflect manifest files  
- Installation commands are valid  
- No hallucinated APIs, fields, or features  

### Tone & Style
- Developer-friendly  
- Concise, technical  
- Avoid vague or promotional phrasing  

If any requirement is not met, regenerate or fix the section.

---

## 10. Final Output Format
Produce the final result as a **complete README.md** file.

Example skeleton:

```markdown
# <SDK Name>

<Description>

## Key Features
- ...

## Installation
<instructions>

## Quick Start
```

(Continue through all sections)

All sections must be filled exactly as defined.

## 11. Metadata

Spec version: 1.0

Tags: sdk, documentation, readme, developer-docs

Compatible repos: GitHub, local workspace




