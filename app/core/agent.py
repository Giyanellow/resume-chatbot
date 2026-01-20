"""
Factory for creating and managing AI agents with configurable models and providers.

This module provides a centralized factory pattern for instantiating pydantic-ai agents
with support for different LLM providers (currently Ollama). It handles model
initialization, configuration management, and provides testing utilities.
"""

from typing import Optional
from pydantic_ai import Agent, AgentRunResult
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.config.config import get_settings

settings = get_settings()


class AgentFactory:
    """
    Factory class for creating and configuring AI agents.

    This factory manages the lifecycle of AI agents, handling model initialization
    and configuration from application settings. It supports creating multiple agents
    with different system prompts while sharing the same underlying model instance.

    Attributes:
        model_name (str): The name of the LLM model to use (e.g., 'llama2', 'mistral').
        ollama_base_url (str): Base URL for the Ollama API endpoint.
        model (OpenAIChatModel): Initialized model instance with configured provider.

    Example:
        >>> factory = AgentFactory()
        >>> agent = factory.create_agent(system_prompt="You are a helpful assistant")
        >>> result = agent.run_sync(user_prompt="Hello!")
    """

    def __init__(self) -> None:
        """Initialize the factory with settings and prepare the model instance."""
        self.model_name = settings.MODEL_NAME
        self.ollama_base_url = settings.OLLAMA_BASE_URL
        self.model = self._model_init()

    def create_agent(self, system_prompt: Optional[str] = None) -> Agent:
        """
        Create a new Agent instance with optional system prompt.

        Agents created by this method share the same underlying model instance,
        making it efficient to create multiple agents with different behaviors.

        Args:
            system_prompt: Optional system prompt to define agent behavior and context.
                         If None, the agent will use default behavior without specific instructions.

        Returns:
            Agent: A configured pydantic-ai Agent instance ready for interaction.

        Example:
            >>> agent = factory.create_agent("You are a Python expert")
            >>> result = agent.run_sync(user_prompt="Explain decorators")
        """
        if system_prompt:
            agent = Agent(model=self.model, system_prompt=system_prompt)
        else:
            agent = Agent(model=self.model)

        return agent

    def _model_init(self) -> OpenAIChatModel:
        """
        Initialize the OpenAI-compatible chat model with Ollama provider.

        Creates a model instance using OpenAI's chat interface but backed by
        a local Ollama provider for running open-source models.

        Returns:
            OpenAIChatModel: Configured model instance ready for agent creation.
        """
        return OpenAIChatModel(
            self.model_name,
            provider=OllamaProvider(base_url=self.ollama_base_url),
        )

    def _identify_model_provider(self, model_name: str):
        """
        Placeholder for future model provider identification logic.

        This method is reserved for implementing automatic provider detection
        based on model name patterns (e.g., 'gpt-*' -> OpenAI, 'claude-*' -> Anthropic).

        Args:
            model_name: The name of the model to identify provider for.

        Note:
            Currently not implemented. Will be used when multi-provider support is added.
        """
        pass

    def test_agent(
        self, message: str, system_prompt: Optional[str] = None
    ) -> AgentRunResult[str]:
        """
        Test the agent with a synchronous message exchange.

        Convenience method for testing agent behavior during development.
        Creates a temporary agent instance and runs a single synchronous interaction.

        Args:
            message: The user message to send to the agent.
            system_prompt: Optional system prompt to configure agent behavior for this test.

        Returns:
            AgentRunResult[str]: The complete result object containing the agent's response
                                and metadata about the interaction.

        Example:
            >>> result = factory.test_agent("What is Python?", "You are concise")
            >>> print(result.data)
        """
        agent = self.create_agent(system_prompt)
        return agent.run_sync(user_prompt=message)


if __name__ == "__main__":
    # Interactive CLI for testing agent responses
    agent = AgentFactory()
    while True:
        msg = input("User: ")
        print(f"\n{agent.test_agent(msg)}")
