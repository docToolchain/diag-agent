"""Unit tests for Orchestrator."""

import pytest
from unittest.mock import Mock, patch
import time


class TestOrchestrator:
    """Tests for Orchestrator feedback loop."""

    def test_orchestrator_respects_max_iterations(self):
        """Test orchestrator stops after reaching max_iterations limit.

        Validates that:
        - Orchestrator tracks iteration count
        - Stops when max_iterations reached (from Settings)
        - Returns result dict with diagram_source and metadata
        - Doesn't exceed iteration limit even if validation fails
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 2
        mock_settings.max_time_seconds = 60

        # Mock LLMClient
        mock_llm_client = Mock()
        mock_llm_client.generate.return_value = "@startuml\nTest\n@enduml"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client):
            orchestrator = Orchestrator(mock_settings)

            # Act
            result = orchestrator.execute(
                description="Test diagram",
                diagram_type="plantuml",
                output_dir="./test_output",
                output_formats="png"
            )

        # Assert
        assert "diagram_source" in result, "Missing diagram_source in result"
        assert "iterations_used" in result, "Missing iterations_used metadata"
        assert result["iterations_used"] <= mock_settings.max_iterations, \
            f"Exceeded max_iterations: {result['iterations_used']} > {mock_settings.max_iterations}"
        assert result["iterations_used"] > 0, "Should have at least 1 iteration"

    def test_orchestrator_respects_time_limit(self):
        """Test orchestrator stops when max_time_seconds exceeded.

        Validates that:
        - Orchestrator tracks elapsed time
        - Stops when max_time_seconds reached (from Settings)
        - Returns result even if time limit hit mid-iteration
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 100  # High number
        mock_settings.max_time_seconds = 1  # Very short timeout

        # Mock LLMClient
        mock_llm_client = Mock()
        mock_llm_client.generate.return_value = "@startuml\nTest\n@enduml"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client):
            orchestrator = Orchestrator(mock_settings)

            # Act
            start_time = time.time()
            result = orchestrator.execute(
                description="Test diagram",
                diagram_type="plantuml"
            )
            elapsed = time.time() - start_time

        # Assert
        assert "elapsed_seconds" in result, "Missing elapsed_seconds metadata"
        assert elapsed <= mock_settings.max_time_seconds + 1, \
            f"Took too long: {elapsed}s > {mock_settings.max_time_seconds + 1}s (allowing 1s grace)"
        assert "stopped_reason" in result, "Missing stopped_reason metadata"
        assert result["stopped_reason"] in ["max_iterations", "max_time", "success"], \
            f"Invalid stopped_reason: {result.get('stopped_reason')}"

    def test_orchestrator_uses_llm_client_for_generation(self):
        """Test orchestrator calls LLMClient.generate() for diagram generation.

        Validates that:
        - Orchestrator instantiates LLMClient with Settings
        - Calls llm_client.generate() with prompt containing description + type
        - Returns LLM-generated diagram source (not hardcoded value)
        - Prompt is properly constructed with diagram type and description
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60

        # Mock LLMClient
        mock_llm_client = Mock()
        mock_llm_client.generate.return_value = "@startuml\nAlice -> Bob: Auth Request\n@enduml"

        description = "User authentication flow"
        diagram_type = "plantuml"

        # Patch BEFORE creating Orchestrator (LLMClient is instantiated in __init__)
        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            result = orchestrator.execute(
                description=description,
                diagram_type=diagram_type
            )

        # Assert
        # Verify LLMClient.generate() was called
        mock_llm_client.generate.assert_called_once()
        
        # Verify prompt contains description and diagram type
        call_args = mock_llm_client.generate.call_args
        prompt = call_args[0][0]  # First positional argument
        assert description in prompt, f"Description not in prompt: {prompt}"
        assert diagram_type in prompt, f"Diagram type not in prompt: {prompt}"
        
        # Verify result contains LLM-generated source (not hardcoded)
        assert result["diagram_source"] == "@startuml\nAlice -> Bob: Auth Request\n@enduml"
        assert "' Generated diagram" not in result["diagram_source"], \
            "Should use LLM output, not hardcoded placeholder"

    def test_orchestrator_validates_with_kroki_success(self):
        """Test orchestrator validates diagram with KrokiClient (success path).

        Validates that:
        - Orchestrator calls KrokiClient.render_diagram() for syntax validation
        - On success (no exception), diagram is accepted
        - Result contains valid diagram_source and PNG output
        - Only 1 iteration needed for valid diagram
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_local_url = "http://localhost:8000"

        # Mock LLMClient - generates valid PlantUML
        mock_llm_client = Mock()
        mock_llm_client.generate.return_value = "@startuml\nAlice -> Bob: Hello\n@enduml"

        # Mock KrokiClient - validation succeeds
        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.return_value = b"\x89PNG\r\n\x1a\n"  # PNG bytes

        description = "Simple sequence diagram"
        diagram_type = "plantuml"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            result = orchestrator.execute(
                description=description,
                diagram_type=diagram_type
            )

        # Assert
        # Verify KrokiClient.render_diagram() was called for validation
        mock_kroki_client.render_diagram.assert_called_once()
        call_args = mock_kroki_client.render_diagram.call_args
        rendered_source = call_args[1]["diagram_source"]
        assert rendered_source == "@startuml\nAlice -> Bob: Hello\n@enduml"
        assert call_args[1]["diagram_type"] == diagram_type

        # Verify only 1 iteration (no retry needed)
        assert result["iterations_used"] == 1
        assert result["stopped_reason"] == "success"
        
        # Verify result contains validated source
        assert result["diagram_source"] == "@startuml\nAlice -> Bob: Hello\n@enduml"

    def test_orchestrator_retries_on_kroki_validation_error(self):
        """Test orchestrator retries when KrokiClient validation fails.

        Validates that:
        - Iteration 1: LLM generates invalid source → Kroki raises KrokiRenderError
        - Orchestrator catches error and builds refinement prompt with error details
        - Iteration 2: LLM generates fix based on error → Kroki succeeds
        - Result shows 2 iterations used
        - Refinement prompt contains error message from Kroki
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings
        from diag_agent.kroki.client import KrokiRenderError

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_local_url = "http://localhost:8000"

        # Mock LLMClient - first generates invalid, then valid source
        mock_llm_client = Mock()
        mock_llm_client.generate.side_effect = [
            "@startuml\nInvalid syntax here\n@enduml",  # Iteration 1: invalid
            "@startuml\nAlice -> Bob: Fixed\n@enduml"   # Iteration 2: valid
        ]

        # Mock KrokiClient - first raises error, then succeeds
        mock_kroki_client = Mock()
        error_message = "Kroki rendering failed for diagram type 'plantuml': HTTP 400 - Syntax error at line 2"
        mock_kroki_client.render_diagram.side_effect = [
            KrokiRenderError(error_message),  # Iteration 1: error
            b"\x89PNG\r\n\x1a\n"               # Iteration 2: success
        ]

        description = "Test diagram"
        diagram_type = "plantuml"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            result = orchestrator.execute(
                description=description,
                diagram_type=diagram_type
            )

        # Assert
        # Verify 2 LLM calls (initial + retry)
        assert mock_llm_client.generate.call_count == 2
        
        # Verify 2nd LLM call contains error message in prompt
        second_call_args = mock_llm_client.generate.call_args_list[1]
        refinement_prompt = second_call_args[0][0]
        assert "error" in refinement_prompt.lower() or "fix" in refinement_prompt.lower(), \
            f"Refinement prompt should mention error/fix: {refinement_prompt}"
        assert "Syntax error" in refinement_prompt or error_message in refinement_prompt, \
            f"Refinement prompt should contain Kroki error details: {refinement_prompt}"

        # Verify 2 Kroki validation calls
        assert mock_kroki_client.render_diagram.call_count == 2

        # Verify result shows 2 iterations and success
        assert result["iterations_used"] == 2
        assert result["stopped_reason"] == "success"
        assert result["diagram_source"] == "@startuml\nAlice -> Bob: Fixed\n@enduml"
