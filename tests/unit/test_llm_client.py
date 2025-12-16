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

    def test_vision_analyze_design_feedback_success(self):
        """Test LLMClient.vision_analyze() returns design feedback from vision analysis.

        Validates that:
        - vision_analyze() converts PNG bytes to base64 data URL
        - Calls litellm.completion() with vision message structure
        - Message contains text prompt + image_url with base64 data
        - Returns design feedback string from LLM response
        """
        from diag_agent.llm.client import LLMClient
        from diag_agent.config.settings import Settings
        import base64

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-3-7-sonnet-latest"

        # Mock PNG image bytes (minimal valid PNG header)
        png_bytes = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        
        # Mock LiteLLM response with design feedback
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Layout is cramped. Suggest using vertical layout for better readability."

        client = LLMClient(mock_settings)
        analysis_prompt = "Analyze this diagram for layout quality, readability, and spacing."

        with patch("diag_agent.llm.client.litellm.completion", return_value=mock_response) as mock_completion:
            # Act
            result = client.vision_analyze(png_bytes, analysis_prompt)

            # Assert
            assert result == "Layout is cramped. Suggest using vertical layout for better readability."
            
            # Verify litellm.completion was called with vision message structure
            mock_completion.assert_called_once()
            call_kwargs = mock_completion.call_args.kwargs
            
            assert call_kwargs["model"] == "anthropic/claude-3-7-sonnet-latest"
            assert call_kwargs["messages"][0]["role"] == "user"
            
            # Verify message content is array with text + image
            content = call_kwargs["messages"][0]["content"]
            assert isinstance(content, list)
            assert len(content) == 2
            
            # Verify text component
            assert content[0]["type"] == "text"
            assert content[0]["text"] == analysis_prompt
            
            # Verify image component with base64 data URL
            assert content[1]["type"] == "image_url"
            assert "image_url" in content[1]
            assert content[1]["image_url"]["url"].startswith("data:image/png;base64,")
            
            # Verify base64 encoding is correct
            expected_base64 = base64.b64encode(png_bytes).decode('utf-8')
            assert content[1]["image_url"]["url"] == f"data:image/png;base64,{expected_base64}"

    def test_vision_analyze_api_error(self):
        """Test LLMClient.vision_analyze() raises LLMGenerationError on API failure.

        Validates that:
        - LiteLLM exceptions are caught and wrapped
        - LLMGenerationError includes model and error context
        - Original exception is preserved in chain
        """
        from diag_agent.llm.client import LLMClient, LLMGenerationError
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-3-7-sonnet-latest"

        png_bytes = b'\x89PNG\r\n\x1a\n'
        client = LLMClient(mock_settings)
        analysis_prompt = "Analyze this diagram."

        with patch("diag_agent.llm.client.litellm.completion") as mock_completion:
            # Mock API error
            mock_completion.side_effect = Exception("API rate limit exceeded")

            # Act & Assert
            with pytest.raises(LLMGenerationError) as exc_info:
                client.vision_analyze(png_bytes, analysis_prompt)
            
            # Verify error message contains context
            error_message = str(exc_info.value)
            assert "anthropic/claude-3-7-sonnet-latest" in error_message
            assert "API rate limit exceeded" in error_message
