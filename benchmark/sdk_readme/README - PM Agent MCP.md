# Agent Framework

A comprehensive, open-source framework for building AI agents in both .NET and Python. Agent Framework provides a unified set of abstractions and tools for creating sophisticated agentic applications that work seamlessly across local and cloud environments.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Key Features

- **Unified Multi-Language Support**: Build AI agents in both .NET (C#) and Python with consistent APIs and abstractions
- **Flexible Agent Orchestration**: Compose complex multi-agent workflows with sequential, concurrent, and conditional orchestration patterns
- **Cloud-Native Integration**: First-class support for Azure AI Foundry, Azure OpenAI, OpenAI, Anthropic, and other AI services
- **Framework Interoperability**: Seamless integration with Semantic Kernel, AutoGen, and Azure AI Projects SDK
- **Durable Execution**: Built-in support for long-running agent operations with Azure Durable Functions
- **Protocol Support**: Native support for Agent-to-Agent (A2A), AG-UI, and Model Context Protocol (MCP)
- **Production-Ready Tools**: Comprehensive tooling for observability, tracing (OpenTelemetry), evaluation, and testing

## Installation

### Python

Agent Framework for Python requires Python 3.10 or later.

```bash
# Install the complete framework with all optional packages
pip install agent-framework

# Or install core package only
pip install agent-framework-core

# Install specific integrations
pip install agent-framework-azure-ai
pip install agent-framework-anthropic
pip install agent-framework-azurefunctions
```

### .NET

Agent Framework for .NET supports .NET 8.0, .NET 9.0, and .NET 10.0.

```bash
# Core abstractions and agent framework
dotnet add package Microsoft.Agents.AI

# Azure AI integration
dotnet add package Microsoft.Agents.AI.AzureAI

# Azure Functions integration
dotnet add package Microsoft.Agents.AI.Hosting.AzureFunctions

# Durable Task orchestration
dotnet add package Microsoft.Agents.AI.DurableTask
```

For nightly builds, see the [FAQ](docs/FAQS.md#how-do-i-get-access-to-nightly-builds).

## Quick Start

### Python

```python
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential

# Create a chat client
chat_client = AzureOpenAIChatClient(
    endpoint="https://YOUR-ENDPOINT.openai.azure.com/",
    deployment_name="gpt-4o",
    credential=DefaultAzureCredential()
)

# Create an agent
agent = ChatAgent(
    chat_client=chat_client,
    name="Assistant",
    description="A helpful AI assistant"
)

# Run the agent
response = await agent.run("Tell me a joke about programming")
print(response.text)
```

### .NET

```csharp
using Microsoft.Agents.AI;
using Microsoft.Extensions.AI;
using Azure.AI.OpenAI;
using Azure.Identity;

// Create a chat client
var chatClient = new AzureOpenAIClient(
    new Uri("https://YOUR-ENDPOINT.openai.azure.com/"),
    new DefaultAzureCredential())
    .AsChatClient("gpt-4o");

// Create an agent
var agent = new ChatClientAgent(chatClient, new ChatClientAgentOptions
{
    Name = "Assistant",
    Description = "A helpful AI assistant"
});

// Run the agent
var response = await agent.RunAsync("Tell me a joke about programming");
Console.WriteLine(response.Text);
```

## API Overview

### Core Abstractions

Both Python and .NET implementations share consistent core abstractions:

#### AIAgent / AgentProtocol

The base abstraction for all agents. Provides methods for:
- **RunAsync** / **run**: Execute the agent with input messages
- **RunStreamingAsync** / **run_stream**: Execute with streaming responses
- **GetNewThread** / **get_new_thread**: Create new conversation threads

#### AgentThread

Manages conversation state and history:
- Thread-based conversation management
- Message history tracking
- State persistence for long-running conversations

#### AgentRunResponse

Contains the results from agent execution:
- **Messages**: Collection of response messages
- **Text**: Concatenated text content
- **Usage**: Token usage and resource metrics
- **ContinuationToken**: For background/async operations

### Agent Types

| Agent Type | Description | Python | .NET |
|------------|-------------|--------|------|
| **ChatAgent / ChatClientAgent** | General-purpose chat agent using IChatClient | ✓ | ✓ |
| **AzureOpenAIChatClient** | Azure OpenAI integration | ✓ | ✓ |
| **OpenAIChatClient** | OpenAI integration | ✓ | ✓ |
| **AzureOpenAIAssistantsClient** | Azure OpenAI Assistants API | ✓ | ✓ |
| **AnthropicChatClient** | Anthropic Claude integration | ✓ | ✓ |

### Orchestration Patterns

| Pattern | Description | Python | .NET |
|---------|-------------|--------|------|
| **SequentialOrchestration** | Run agents in sequence | ✓ | ✓ |
| **ConcurrentOrchestration** | Run agents in parallel | ✓ | ✓ |
| **ConditionalOrchestration** | Route to agents based on conditions | ✓ | ✓ |
| **DeclarativeWorkflow** | Define workflows declaratively | ✓ | ✓ |

### Tools and Middleware

- **Code Interpreter**: Execute code in sandboxed environments
- **File Search**: Search and retrieve from vector stores
- **Function Calling**: Connect agents to custom functions
- **MCP Tools**: Model Context Protocol integration
- **Filtering Middleware**: Transform or filter agent inputs/outputs

## Examples

### Multi-Agent Orchestration

```python
from agent_framework import SequentialOrchestration
from agent_framework.azure import AzureOpenAIChatClient

# Create multiple specialized agents
analyst = ChatAgent(chat_client, name="Analyst", 
    instructions="Extract key concepts from product descriptions")
writer = ChatAgent(chat_client, name="Writer",
    instructions="Write compelling marketing copy")
editor = ChatAgent(chat_client, name="Editor",
    instructions="Polish and format the final copy")

# Orchestrate them sequentially
orchestration = SequentialOrchestration(analyst, writer, editor)

# Execute the workflow
result = await orchestration.run(
    "An eco-friendly water bottle that keeps drinks cold for 24 hours"
)
print(result.text)
```

### Using Azure Functions for Durable Orchestration

```python
from agent_framework.azure import AgentFunctionApp, AzureOpenAIChatClient
from azure.durable_functions import DurableOrchestrationContext

# Create agent
agent = ChatAgent(chat_client, name="WriterAgent")

# Create function app
app = AgentFunctionApp(agents=[agent])

# Define orchestration
@app.orchestration_trigger(context_name="context")
def single_agent_orchestration(context: DurableOrchestrationContext):
    writer = app.get_agent(context, "WriterAgent")
    thread = writer.get_new_thread()
    
    # Chain multiple runs
    response1 = yield writer.run("Write a haiku about coding", thread=thread)
    response2 = yield writer.run("Now add emojis to it", thread=thread)
    
    return response2
```

### Working with Azure AI Foundry

```csharp
using Azure.AI.Projects;
using Azure.Identity;

// Create Foundry client
var persistentAgentsClient = new PersistentAgentsClient(
    new Uri("https://YOUR-PROJECT.api.azureml.ms"),
    new DefaultAzureCredential());

// Create an agent using Foundry SDK
AIAgent agent = await persistentAgentsClient.CreateAIAgentAsync(
    model: "gpt-4o",
    name: "Assistant",
    instructions: "You are a helpful assistant");

// Use in Agent Framework orchestrations
var orchestration = new SequentialOrchestration(agent, otherAgent);
var result = await orchestration.RunAsync("Hello!");

// Cleanup
await persistentAgentsClient.Administration.DeleteAgentAsync(agent.Id);
```

## Dependency Graph

### Python Dependencies

**Core Runtime:**
- Python ≥ 3.10
- Microsoft Extensions AI abstractions
- OpenTelemetry (observability)
- Pydantic (data validation)

**Optional Integrations:**
- `azure-ai-projects` - Azure AI Foundry integration
- `azure-identity` - Azure authentication
- `openai` - OpenAI API client
- `anthropic` - Anthropic API client
- `azure-functions` - Azure Functions runtime
- `redis` - Redis state management
- `mem0` - Memory management

### .NET Dependencies

**Core Runtime:**
- .NET 8.0, 9.0, or 10.0
- Microsoft.Extensions.AI (10.0+)
- System.Text.Json
- OpenTelemetry packages

**Optional Integrations:**
- Azure.AI.Projects - Azure AI Foundry SDK
- Azure.AI.OpenAI - Azure OpenAI client
- OpenAI - OpenAI .NET SDK
- Microsoft.DurableTask - Durable orchestration
- Microsoft.Azure.Functions.Worker - Azure Functions

## Supported Environments

### Python
- **Operating Systems**: Windows, Linux, macOS
- **Python Versions**: 3.10, 3.11, 3.12, 3.13, 3.14
- **Deployment**: Azure Functions, Azure Container Apps, Kubernetes, standalone

### .NET
- **Operating Systems**: Windows, Linux, macOS
- **Target Frameworks**: .NET 8.0, .NET 9.0, .NET 10.0
- **Deployment**: Azure Functions, ASP.NET Core, Azure Container Apps, Kubernetes, standalone

## Documentation

- **[FAQ](docs/FAQS.md)**: Frequently asked questions
- **[Design Specifications](docs/specs/)**: Architecture decision records and design specs
- **[Python Samples](python/samples/)**: Comprehensive Python examples
- **[.NET Samples](dotnet/samples/)**: Comprehensive .NET examples
- **[Agent Samples](agent-samples/)**: YAML-based agent definitions
- **[Workflow Samples](workflow-samples/)**: Declarative workflow examples

### Key Specifications
- [Foundry SDK Alignment](docs/specs/001-foundry-sdk-alignment.md) - Integration with Azure AI Foundry
- [Agent Run Response](docs/decisions/0001-agent-run-response.md) - Response design patterns
- [OpenTelemetry Instrumentation](docs/decisions/0003-agent-opentelemetry-instrumentation.md) - Observability strategy
- [Python Naming Conventions](docs/decisions/0005-python-naming-conventions.md) - API design for Python

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Code of conduct
- Development setup
- Coding standards
- Pull request process

### Development Setup

**Python:**
```bash
# Clone the repository
git clone https://github.com/microsoft/agent-framework.git
cd agent-framework/python

# Run setup
poe setup

# Run tests
poe test
```

**.NET:**
```bash
# Clone the repository  
git clone https://github.com/microsoft/agent-framework.git
cd agent-framework/dotnet

# Build
dotnet build

# Run tests
dotnet test
```

For detailed development instructions:
- Python: See [python/DEV_SETUP.md](python/DEV_SETUP.md)
- .NET: Build with `dotnet build`, test with `dotnet test`, format with `dotnet format`

## Community

- **Report Issues**: [GitHub Issues](https://github.com/microsoft/agent-framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/microsoft/agent-framework/discussions)
- **Security**: See [SECURITY.md](SECURITY.md) for reporting security vulnerabilities
- **Support**: See [SUPPORT.md](SUPPORT.md) for getting help

## Versioning & Release Notes

Agent Framework follows semantic versioning:
- **Python**: Current version tracked in `python/pyproject.toml`
- **.NET**: Package versions managed via `dotnet/Directory.Packages.props`

**Latest Releases:**
- Python releases: [PyPI](https://pypi.org/project/agent-framework/)
- .NET packages: [NuGet](https://www.nuget.org/packages?q=Microsoft.Agents.AI)
- Release notes: [GitHub Releases](https://github.com/microsoft/agent-framework/releases)
- Nightly builds: [GitHub Packages](https://github.com/orgs/microsoft/packages?repo_name=agent-framework)

## License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) Microsoft Corporation.

---

**Links:**
- Homepage: https://aka.ms/agent-framework
- Documentation: https://github.com/microsoft/agent-framework
- Source Code: https://github.com/microsoft/agent-framework
- Issue Tracker: https://github.com/microsoft/agent-framework/issues
