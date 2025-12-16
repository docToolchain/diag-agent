"""Integration tests for Orchestrator with real component interactions.

These tests verify the integration between multiple components:
- Orchestrator coordinating the workflow
- LLMClient (mocked) generating diagram code
- KrokiClient (real or mocked) validating syntax
- Settings configuration
- File I/O

Unlike unit tests, these tests exercise the full workflow with minimal mocking.
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import time


class TestOrchestratorIntegration:
    """Integration tests for Orchestrator workflows."""

    def test_orchestrator_happy_path_integration(self, tmp_path):
        """Test complete workflow: Settings → Orchestrator → File Output.

        Validates:
        - Settings loaded correctly
        - LLM generates valid diagram code
        - Kroki validates syntax successfully
        - Files written to disk
        - Metadata returned correctly
        """
        from diag_agent.config.settings import Settings
        from diag_agent.agent.orchestrator import Orchestrator

        # Arrange - Mock settings
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_url = "https://kroki.io"
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.validate_design = False
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-sonnet-4"

        # Valid PlantUML code (no syntax errors)
        valid_plantuml = "@startuml\nAlice -> Bob: Hello\n@enduml"

        orchestrator = Orchestrator(mock_settings)

        # Mock LLMClient to return valid code immediately
        with patch.object(orchestrator.llm_client, 'generate', return_value=valid_plantuml):
            # Act - Execute with real Kroki validation
            result = orchestrator.execute(
                description="Simple sequence diagram",
                diagram_type="plantuml",
                output_dir=str(tmp_path),
                output_formats="source,png"
            )

        # Assert - Verify result
        assert result["diagram_source"] == valid_plantuml
        assert result["iterations_used"] == 1  # Success on first try
        assert result["stopped_reason"] == "success"
        assert result["elapsed_seconds"] < 10  # Should be fast

        # Verify files written
        source_file = tmp_path / "diagram.puml"
        png_file = tmp_path / "diagram.png"
        assert source_file.exists()
        assert png_file.exists()
        assert source_file.read_text() == valid_plantuml
        assert png_file.stat().st_size > 0  # PNG has content

    def test_orchestrator_syntax_error_recovery_integration(self, tmp_path):
        """Test error recovery: Syntax Error → Refinement → Success.

        Validates:
        - LLM generates invalid code first
        - Kroki returns validation error (mocked)
        - Orchestrator refines with error feedback
        - LLM generates valid code on retry
        - Success after 2 iterations
        """
        from diag_agent.config.settings import Settings
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.kroki.client import KrokiRenderError

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_url = "https://kroki.io"
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.validate_design = False
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-sonnet-4"

        # Invalid and valid PlantUML
        invalid_plantuml = "@startuml\nAlice -> Bob: Hello"
        valid_plantuml = "@startuml\nAlice -> Bob: Hello\n@enduml"

        orchestrator = Orchestrator(mock_settings)

        # Mock LLMClient: first invalid, then valid
        # Mock KrokiClient: first error, then success (twice for validation + file output)
        with patch.object(orchestrator.llm_client, 'generate', side_effect=[invalid_plantuml, valid_plantuml]), \
             patch.object(orchestrator.kroki_client, 'render_diagram') as mock_kroki:
            # First call fails, second call succeeds (validation), third call succeeds (file output)
            mock_kroki.side_effect = [
                KrokiRenderError("Syntax error: missing @enduml"),
                b'\x89PNG',  # Valid PNG bytes (validation)
                b'\x89PNG'   # Valid PNG bytes (file output)
            ]

            # Act
            result = orchestrator.execute(
                description="Simple sequence diagram",
                diagram_type="plantuml",
                output_dir=str(tmp_path),
                output_formats="source,png"
            )

        # Assert
        assert result["diagram_source"] == valid_plantuml  # Final code is valid
        assert result["iterations_used"] == 2  # Error + Retry
        assert result["stopped_reason"] == "success"

        # Verify files written with valid code
        source_file = tmp_path / "diagram.puml"
        assert source_file.exists()
        assert source_file.read_text() == valid_plantuml

    def test_orchestrator_iteration_limit_integration(self, tmp_path):
        """Test iteration limit enforcement.

        Validates:
        - LLM generates invalid code repeatedly
        - Kroki rejects all attempts (mocked)
        - Orchestrator stops at max_iterations
        - stopped_reason = "max_iterations"
        - Files still written with last attempt
        """
        from diag_agent.config.settings import Settings
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.kroki.client import KrokiRenderError

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_url = "https://kroki.io"
        mock_settings.max_iterations = 3  # Low limit
        mock_settings.max_time_seconds = 60
        mock_settings.validate_design = False
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-sonnet-4"

        # Always return invalid code
        invalid_plantuml = "@startuml\nAlice -> Bob: Hello"

        orchestrator = Orchestrator(mock_settings)

        # Mock LLMClient to always return invalid code
        # Mock KrokiClient to always fail
        with patch.object(orchestrator.llm_client, 'generate', return_value=invalid_plantuml), \
             patch.object(orchestrator.kroki_client, 'render_diagram') as mock_kroki:
            # Always raise error
            mock_kroki.side_effect = KrokiRenderError("Syntax error: invalid PlantUML")

            # Act
            result = orchestrator.execute(
                description="Simple sequence diagram",
                diagram_type="plantuml",
                output_dir=str(tmp_path),
                output_formats="source"
            )

        # Assert
        assert result["iterations_used"] == 3  # Stopped at limit
        assert result["stopped_reason"] == "max_iterations"
        assert result["diagram_source"] == invalid_plantuml  # Last attempt

        # Verify source file written (even though invalid)
        source_file = tmp_path / "diagram.puml"
        assert source_file.exists()

    def test_orchestrator_time_limit_integration(self, tmp_path):
        """Test time limit enforcement.

        Validates:
        - Orchestrator stops when time limit exceeded
        - stopped_reason = "max_time"
        - Files written with last attempt
        """
        from diag_agent.config.settings import Settings
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.kroki.client import KrokiRenderError

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_url = "https://kroki.io"
        mock_settings.max_iterations = 10  # High iteration limit
        mock_settings.max_time_seconds = 1  # Very low time limit (1 second)
        mock_settings.validate_design = False
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-sonnet-4"

        # Valid code
        valid_plantuml = "@startuml\nAlice -> Bob: Hello\n@enduml"

        orchestrator = Orchestrator(mock_settings)

        # Mock LLMClient with delay to trigger time limit
        # Mock KrokiClient to always fail (forcing retries until time limit)
        def slow_generate(prompt):
            time.sleep(0.6)  # Each call takes 0.6s
            return valid_plantuml

        with patch.object(orchestrator.llm_client, 'generate', side_effect=slow_generate), \
             patch.object(orchestrator.kroki_client, 'render_diagram') as mock_kroki:
            # Always fail to force retries
            mock_kroki.side_effect = KrokiRenderError("Syntax error")

            # Act
            result = orchestrator.execute(
                description="Simple sequence diagram",
                diagram_type="plantuml",
                output_dir=str(tmp_path),
                output_formats="source"
            )

        # Assert
        assert result["stopped_reason"] == "max_time"
        assert result["elapsed_seconds"] >= 1  # At least 1 second elapsed
        assert result["iterations_used"] >= 1  # At least one iteration

    def test_orchestrator_design_feedback_integration(self, tmp_path):
        """Test design feedback loop integration.

        Validates:
        - validate_design=true triggers vision analysis
        - Vision LLM provides design feedback
        - Orchestrator refines based on feedback
        - Loop continues until approved or limit
        """
        from diag_agent.config.settings import Settings
        from diag_agent.agent.orchestrator import Orchestrator

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_url = "https://kroki.io"
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.validate_design = True  # Enable design feedback
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-sonnet-4"

        # Valid PlantUML codes (initial and refined)
        initial_code = "@startuml\nAlice -> Bob: Hello\n@enduml"
        refined_code = "@startuml\nskinparam sequenceMessageAlign center\nAlice -> Bob: Hello\n@enduml"

        orchestrator = Orchestrator(mock_settings)

        # Mock LLMClient: generate returns initial, then refined
        # Mock vision_analyze: first gives feedback, then approves
        with patch.object(orchestrator.llm_client, 'generate', side_effect=[initial_code, refined_code]), \
             patch.object(orchestrator.llm_client, 'vision_analyze', side_effect=[
                 "Layout could be improved. Center-align messages for better readability.",
                 "The design looks good and is approved."
             ]):
            # Act
            result = orchestrator.execute(
                description="Simple sequence diagram",
                diagram_type="plantuml",
                output_dir=str(tmp_path),
                output_formats="source,png"
            )

        # Assert
        assert result["diagram_source"] == refined_code  # Refined version
        assert result["iterations_used"] == 2  # Initial + Refinement
        assert result["stopped_reason"] == "success"  # Approved

        # Verify files written
        source_file = tmp_path / "diagram.puml"
        assert source_file.exists()
        assert source_file.read_text() == refined_code
