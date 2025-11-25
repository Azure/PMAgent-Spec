# Microsoft Agent Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![.NET Version](https://img.shields.io/badge/.NET-8.0%2B-purple)](https://dotnet.microsoft.com/)

A comprehensive framework for building AI agents with support for multiple programming languages, AI providers, and advanced agent capabilities. The Agent Framework provides a unified, production-ready foundation for creating intelligent agents that can reason, use tools, and orchestrate complex workflows.

## 🌟 Overview

The Microsoft Agent Framework is designed to simplify the development of AI agents by providing:

- **Multi-language Support**: Native implementations in Python and C#/.NET
- **Provider Agnostic**: Works with OpenAI, Azure OpenAI, Anthropic, and other AI providers
- **Agent-to-Agent Communication**: Built-in support for A2A protocol
- **Workflow Orchestration**: Tools for building complex multi-agent systems
- **Extensible Architecture**: Plugin system for tools, guardrails, and custom components
- **Enterprise Ready**: Observability, persistence, and hosting capabilities

## 🏗️ Repository Structure

```
agent-framework/
├── python/                    # Python implementation
│   ├── packages/
│   │   ├── core/             # Core agent framework
│   │   ├── azure-ai/         # Azure AI integration
│   │   ├── anthropic/        # Anthropic integration
│   │   ├── a2a/              # Agent-to-Agent protocol
│   │   ├── ag-ui/            # Agent UI support
│   │   ├── chatkit/          # Chat interface utilities
│   │   ├── copilotstudio/    # Copilot Studio integration
│   │   ├── devui/            # Developer UI
│   │   ├── mem0/             # Memory integration
│   │   ├── purview/          # Purview integration
│   │   └── redis/            # Redis integration
│   ├── samples/              # Python code samples
│   └── tests/                # Python tests
├── dotnet/                   # .NET implementation
│   ├── src/
│   │   ├── Microsoft.Agents.AI/                 # Core AI agents
│   │   ├── Microsoft.Agents.AI.A2A/             # A2A support
│   │   ├── Microsoft.Agents.AI.AGUI/            # Agent UI
│   │   ├── Microsoft.Agents.AI.AzureAI/         # Azure AI integration
│   │   ├── Microsoft.Agents.AI.OpenAI/          # OpenAI integration
│   │   ├── Microsoft.Agents.AI.CopilotStudio/   # Copilot Studio
│   │   ├── Microsoft.Agents.AI.Workflows/       # Workflow orchestration
│   │   ├── Microsoft.Agents.AI.Hosting/         # Hosting infrastructure
│   │   └── ...
│   ├── samples/              # .NET code samples
│   └── tests/                # .NET tests
├── docs/                     # Documentation
├── agent-samples/            # Cross-language agent samples (YAML)
├── workflow-samples/         # Workflow examples (YAML)
└── schemas/                  # JSON schemas
```

## 🚀 Quick Start

### Python

#### Installation

```bash
# Install the complete framework
pip install agent-framework

# Or install core only
pip install agent-framework-core

# Or install with specific providers
pip install agent-framework-core[openai]
pip install agent-framework-azure-ai
```

#### Basic Example

```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

# Create a chat client
chat_client = OpenAIChatClient()

# Create an agent
agent = ChatAgent(
    name="assistant",
    chat_client=chat_client,
    instructions="You are a helpful assistant."
)

# Run the agent
response = await agent.run("What's the weather like?")
print(response.content)
```

For detailed setup instructions, see [Python Dev Setup](python/DEV_SETUP.md).

### .NET

#### Installation

```bash
dotnet add package Microsoft.Agents.AI
```

#### Basic Example

```csharp
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;

// Create a chat client
var chatClient = new OpenAIChatClient(endpoint, apiKey);

// Create an agent
var agent = new ChatClientAgent(
    chatClient,
    name: "assistant",
    instructions: "You are a helpful assistant."
);

// Run the agent
var response = await agent.InvokeAsync("What's the weather like?");
Console.WriteLine(response.Content);
```

## 📦 Key Features

### Core Capabilities

- **Chat Agents**: Build conversational AI agents with memory and context
- **Tool Integration**: Enable agents to call functions and use external tools
- **Streaming Responses**: Support for real-time streaming of agent responses
- **Multi-turn Conversations**: Maintain conversation history and context
- **Observability**: Built-in OpenTelemetry instrumentation for monitoring

### Advanced Features

- **Agent-to-Agent (A2A)**: Enable agents to communicate and collaborate
- **Workflow Orchestration**: Define complex multi-agent workflows
- **Persistent Agents**: Save and restore agent state
- **Guardrails**: Content filtering and safety controls
- **Vector Search**: Semantic search and RAG capabilities
- **Durable Tasks**: Long-running agent operations

### Integrations

#### AI Providers
- OpenAI (GPT-4, GPT-3.5, etc.)
- Azure OpenAI
- Anthropic (Claude)
- Azure AI Foundry
- Ollama (local models)

#### Hosting Platforms
- Azure Functions
- ASP.NET Core
- Standalone applications

#### Services
- Microsoft Copilot Studio
- Azure AI Search
- Redis
- Mem0
- Microsoft Purview

## 📚 Documentation

- [FAQs](docs/FAQS.md)
- [Architecture Decision Records](docs/decisions/)
- [Design Specifications](docs/specs/)
- [Python Development Guide](python/DEV_SETUP.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🎯 Sample Projects

### Python Samples
Located in `python/samples/`, including:
- Getting started examples
- Tool usage patterns
- Multi-agent systems
- Streaming responses
- Azure integration

### .NET Samples
Located in `dotnet/samples/`, including:
- **GettingStarted**: Basic agent setup and usage
- **A2AClientServer**: Agent-to-Agent communication
- **AGUIClientServer**: Agent UI integration
- **AzureFunctions**: Serverless agent hosting
- **HostedAgents**: ASP.NET Core hosting
- **M365Agent**: Microsoft 365 integration
- **Purview**: Data governance integration

### Agent Samples (YAML)
Pre-configured agent examples in `agent-samples/`:
- Azure OpenAI agents
- OpenAI assistants
- Copilot Studio integration
- Persistent agents

### Workflow Samples (YAML)
Multi-agent workflow examples in `workflow-samples/`:
- Customer support workflows
- Deep research patterns
- Marketing automation
- Math chat systems

## 🛠️ Development

### Prerequisites

**Python:**
- Python 3.10 or higher
- uv (for dependency management)

**C#/.NET:**
- .NET 8.0 SDK or higher
- Visual Studio 2022 or VS Code

### Building from Source

**Python:**
```bash
cd python
uv venv --python 3.13
uv sync --all-extras --dev
uv run poe setup
```

**C#/.NET:**
```bash
cd dotnet
dotnet build
dotnet test
```

### Running Tests

**Python:**
```bash
cd python
uv run poe test
```

**C#/.NET:**
```bash
cd dotnet
dotnet test
```

### Code Quality

**Python:**
```bash
# Format code
uv run poe fmt

# Lint
uv run poe lint

# Type checking
uv run poe pyright

# Run all checks
uv run poe check
```

**C#/.NET:**
```bash
# Format code
dotnet format

# Build and analyze
dotnet build
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Reporting issues
- Submitting pull requests
- Coding standards
- Development workflow

### Key Contribution Guidelines

- Follow language-specific coding conventions ([.NET](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions) / [Python](https://pypi.org/project/black/))
- Include tests with new features
- Add XML/docstring documentation for public APIs
- Use pre-commit hooks for code quality
- Start discussions for breaking changes

## 📋 Project Governance

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Community Guidelines](COMMUNITY.md)
- [Security Policy](SECURITY.md)
- [Support Resources](SUPPORT.md)
- [Transparency FAQ](TRANSPARENCY_FAQ.md)

## 🔧 Nightly Builds

Nightly builds are available for early access to new features. See [FAQs](docs/FAQS.md#how-do-i-get-access-to-nightly-builds) for instructions on accessing nightly builds.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌐 Links

- **Homepage**: [aka.ms/agent-framework](https://aka.ms/agent-framework)
- **Source Code**: [github.com/microsoft/agent-framework](https://github.com/microsoft/agent-framework)
- **Python Package**: [pypi.org/project/agent-framework](https://pypi.org/project/agent-framework/)
- **NuGet Packages**: [nuget.org](https://www.nuget.org/packages?q=Microsoft.Agents.AI)
- **Issues**: [GitHub Issues](https://github.com/microsoft/agent-framework/issues)

## 🙏 Acknowledgments

The Microsoft Agent Framework is built on top of and integrates with many excellent open-source projects and services:

- OpenTelemetry for observability
- Semantic Kernel for AI orchestration
- Microsoft.Extensions.AI for AI abstractions
- Pydantic for Python data validation
- And many more...

---

**Made with ❤️ by Microsoft**
