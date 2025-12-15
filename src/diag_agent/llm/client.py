"""LLM client for diagram generation via LiteLLM."""

from typing import Any
import litellm


class LLMGenerationError(Exception):
    """Exception raised when LLM diagram generation fails.
    
    This wraps LLM API errors with additional context about
    the provider, model, and error details.
    """
    pass


class LLMClient:
    """Client for interacting with LLM providers via LiteLLM.

    Supports multiple providers (Anthropic, OpenAI, local models)
    through unified LiteLLM interface.
    """

    def __init__(self, settings: Any) -> None:
        """Initialize LLM client with settings.

        Args:
            settings: Application settings (Settings instance)
        """
        self.settings = settings

    def generate(self, prompt: str) -> str:
        """Generate diagram source code from prompt.

        Args:
            prompt: Natural language description and instructions for diagram

        Returns:
            Generated diagram source code

        Raises:
            LLMGenerationError: If LLM API call fails
        """
        # Build model string: provider/model (e.g., "anthropic/claude-sonnet-4")
        model = f"{self.settings.llm_provider}/{self.settings.llm_model}"

        try:
            # Call LiteLLM completion API
            response = litellm.completion(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract generated content from response
            return response.choices[0].message.content

        except Exception as e:
            # Convert any LLM errors to custom exception with context
            raise LLMGenerationError(
                f"LLM generation failed for model '{model}': {str(e)}"
            ) from e
