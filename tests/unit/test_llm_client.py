"""Unit tests for LLM Client."""

import pytest
from unittest.mock import Mock, patch


class TestLLMClient:
    """Tests for LLM Client text generation."""

    def test_generate_diagram_source_success(self):
        """Test LLMClient.generate() returns diagram source from LLM.

        Validates that:
        - LLMClient uses Settings (llm_provider, llm_model)
        - generate() calls litellm.completion() with correct parameters
        - Response content is extracted and returned
        - Prompt is passed correctly to LLM
        """
        from diag_agent.llm.client import LLMClient
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-sonnet-4"

        # Mock LiteLLM response structure
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "@startuml\nAlice -> Bob: Hello\n@enduml"

        client = LLMClient(mock_settings)
        prompt = "Generate a PlantUML sequence diagram showing Alice greeting Bob"

        with patch("diag_agent.llm.client.litellm.completion", return_value=mock_response) as mock_completion:
            # Act
            result = client.generate(prompt)

            # Assert
            assert result == "@startuml\nAlice -> Bob: Hello\n@enduml"
            
            # Verify litellm.completion was called with correct parameters
            mock_completion.assert_called_once()
            call_kwargs = mock_completion.call_args.kwargs
            
            assert call_kwargs["model"] == "anthropic/claude-sonnet-4"
            assert call_kwargs["messages"][0]["role"] == "user"
            assert call_kwargs["messages"][0]["content"] == prompt
