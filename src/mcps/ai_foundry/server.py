import argparse
import logging
import os
from dataclasses import dataclass
from typing import Optional

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class Settings:
    """Configuration for the AI Foundry MCP proxy."""

    endpoint: str
    agent_name: str
    host: str = "0.0.0.0"
    port: int = 8110

    @classmethod
    def from_env_and_cli(cls) -> "Settings":
        parser = argparse.ArgumentParser(
            description="Thin MCP proxy that forwards prompts to an Azure AI Foundry agent."
        )
        parser.add_argument(
            "--endpoint",
            default=os.getenv("AI_FOUNDRY_ENDPOINT"),
            help="AI Foundry project endpoint (env: AI_FOUNDRY_ENDPOINT)",
        )
        parser.add_argument(
            "--agent",
            dest="agent_name",
            default=os.getenv("AI_FOUNDRY_AGENT_NAME"),
            help="AI Foundry agent name (env: AI_FOUNDRY_AGENT_NAME)",
        )
        parser.add_argument(
            "--host",
            default=os.getenv("AI_FOUNDRY_HOST", "0.0.0.0"),
            help="Host for the MCP HTTP server (env: AI_FOUNDRY_HOST)",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=int(os.getenv("AI_FOUNDRY_PORT", "8110")),
            help="Port for the MCP HTTP server (env: AI_FOUNDRY_PORT)",
        )

        args = parser.parse_args()

        missing = []
        if not args.endpoint:
            missing.append("--endpoint or AI_FOUNDRY_ENDPOINT")
        if not args.agent_name:
            missing.append("--agent or AI_FOUNDRY_AGENT_NAME")

        if missing:
            parser.error("Missing required config: " + ", ".join(missing))

        return cls(
            endpoint=args.endpoint,
            agent_name=args.agent_name,
            host=args.host,
            port=args.port,
        )


class AgentProxy:
    """Minimal wrapper around the AI Foundry agent invocation."""

    def __init__(self, settings: Settings, credential: Optional[DefaultAzureCredential] = None):
        self.settings = settings
        self.credential = credential or DefaultAzureCredential()

        logger.info("Connecting to AI Foundry project at %s", settings.endpoint)
        self.project_client = AIProjectClient(endpoint=settings.endpoint, credential=self.credential)
        self.agent = self.project_client.agents.get(agent_name=settings.agent_name)
        logger.info("Using agent '%s'", self.agent.name)

        # Reuse the OpenAI-compatible client for all calls.
        self.openai_client = self.project_client.get_openai_client()

    def invoke_agent(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("prompt is required")

        logger.info("Forwarding prompt to agent '%s'", self.agent.name)
        response = self.openai_client.responses.create(
            input=[{"role": "user", "content": prompt}],
            extra_body={"agent": {"name": self.agent.name, "type": "agent_reference"}},
        )

        # response.output_text is present for text responses; fall back to the raw object otherwise.
        return getattr(response, "output_text", str(response))


def build_mcp(proxy: AgentProxy) -> FastMCP:
    mcp = FastMCP("AI Foundry Agent Proxy", host=proxy.settings.host, port=proxy.settings.port)

    @mcp.tool()
    def invoke_ai_foundry(prompt: str) -> str:
        """Send a user prompt to the configured AI Foundry agent and return the text output."""
        try:
            return proxy.invoke_agent(prompt)
        except Exception as exc:
            logger.exception("Failed to invoke AI Foundry agent")
            return f"Error calling AI Foundry agent: {exc}"

    return mcp


def main():
    settings = Settings.from_env_and_cli()
    proxy = AgentProxy(settings=settings)
    server = build_mcp(proxy)

    logger.info(
        "Starting MCP server on %s:%s for agent '%s'",
        settings.host,
        settings.port,
        settings.agent_name,
    )
    server.run(transport="streamable-http")


if __name__ == "__main__":
    main()
