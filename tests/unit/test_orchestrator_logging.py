"""Unit tests for Orchestrator logging functionality."""

import pytest
from unittest.mock import Mock, patch, call
import logging
from pathlib import Path


class TestOrchestratorLogging:
    """Tests for Orchestrator logging and progress output."""

    def test_orchestrator_creates_log_file_in_output_dir(self, tmp_path):
        """Test orchestrator creates generation.log in output directory.
        
        Validates that:
        - Log file is created at {output_dir}/generation.log
        - Log file exists after execution
        - Log file contains structured log entries
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"
        mock_settings.validate_design = False

        mock_llm_client = Mock()
        mock_llm_client.validate_description.return_value = (True, None)  # Validation passes
        mock_llm_client.generate.return_value = "@startuml\\nTest\\n@enduml"

        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.return_value = b"\\x89PNG"

        output_dir = tmp_path / "diagrams"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            orchestrator.execute(
                description="Test diagram",
                diagram_type="plantuml",
                output_dir=str(output_dir),
                output_formats="png"
            )

        # Assert
        log_file = output_dir / "generation.log"
        assert log_file.exists(), f"Log file not created: {log_file}"
        
        log_content = log_file.read_text()
        assert len(log_content) > 0, "Log file is empty"

    def test_orchestrator_logs_iteration_start(self, tmp_path):
        """Test orchestrator logs iteration start with number.
        
        Validates that:
        - Each iteration logs "Iteration X/Y - START"
        - Timestamp is included
        - Correct iteration numbers (1-based)
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 3
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"
        mock_settings.validate_design = False

        mock_llm_client = Mock()
        mock_llm_client.validate_description.return_value = (True, None)  # Validation passes
        mock_llm_client.generate.return_value = "@startuml\\nTest\\n@enduml"

        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.return_value = b"\\x89PNG"

        output_dir = tmp_path / "diagrams"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            orchestrator.execute(
                description="Test diagram",
                diagram_type="plantuml",
                output_dir=str(output_dir)
            )

        # Assert
        log_content = (output_dir / "generation.log").read_text()
        assert "Iteration 1/3 - START" in log_content
        assert "- " in log_content, "Should have timestamp separator"

    def test_orchestrator_logs_llm_prompt_initial(self, tmp_path):
        """Test orchestrator logs initial LLM prompt.
        
        Validates that:
        - Initial prompt is logged
        - Contains "LLM Prompt (initial):"
        - Includes diagram description and type
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"
        mock_settings.validate_design = False

        mock_llm_client = Mock()
        mock_llm_client.validate_description.return_value = (True, None)  # Validation passes
        mock_llm_client.generate.return_value = "@startuml\\nTest\\n@enduml"

        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.return_value = b"\\x89PNG"

        output_dir = tmp_path / "diagrams"
        description = "User authentication flow"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            orchestrator.execute(
                description=description,
                diagram_type="plantuml",
                output_dir=str(output_dir)
            )

        # Assert
        log_content = (output_dir / "generation.log").read_text()
        assert "LLM Prompt (initial):" in log_content
        assert description in log_content

    def test_orchestrator_logs_validation_error(self, tmp_path):
        """Test orchestrator logs Kroki validation errors.
        
        Validates that:
        - Validation errors are logged
        - Contains "Kroki Validation: ERROR"
        - Includes error message details
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings
        from diag_agent.kroki.client import KrokiRenderError

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"
        mock_settings.validate_design = False

        mock_llm_client = Mock()
        mock_llm_client.validate_description.return_value = (True, None)  # Validation passes
        mock_llm_client.generate.side_effect = [
            "plantuml",  # Subtype detection
            "@startuml\\nInvalid\\n@enduml",  # Iteration 1: invalid
            "@startuml\\nFixed\\n@enduml"     # Iteration 2: valid
        ]

        mock_kroki_client = Mock()
        error_message = "Syntax error at line 2"
        mock_kroki_client.render_diagram.side_effect = [
            KrokiRenderError(f"Kroki rendering failed: {error_message}"),  # Iter 1
            b"\\x89PNG",  # Iter 2 validation
            b"\\x89PNG"   # File write
        ]

        output_dir = tmp_path / "diagrams"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            orchestrator.execute(
                description="Test",
                diagram_type="plantuml",
                output_dir=str(output_dir),
                output_formats="png"
            )

        # Assert
        log_content = (output_dir / "generation.log").read_text()
        assert "Kroki Validation: ERROR" in log_content
        assert error_message in log_content

    def test_orchestrator_logs_design_feedback(self, tmp_path):
        """Test orchestrator logs design feedback from vision analysis.
        
        Validates that:
        - Design feedback is logged
        - Contains "Design Feedback:"
        - Includes feedback text
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"
        mock_settings.validate_design = True  # Enable design validation

        mock_llm_client = Mock()
        mock_llm_client.validate_description.return_value = (True, None)  # Validation passes
        mock_llm_client.generate.side_effect = [
            "plantuml",  # Subtype detection
            "@startuml\\nV1\\n@enduml",
            "@startuml\\nV2 improved\\n@enduml"
        ]
        
        feedback_text = "Layout is too cramped. Increase spacing."
        mock_llm_client.vision_analyze.side_effect = [
            feedback_text,
            "The design is approved."
        ]

        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.return_value = b"\\x89PNG"

        output_dir = tmp_path / "diagrams"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            orchestrator.execute(
                description="Test",
                diagram_type="plantuml",
                output_dir=str(output_dir),
                output_formats="png"
            )

        # Assert
        log_content = (output_dir / "generation.log").read_text()
        assert "Design Feedback:" in log_content
        assert feedback_text in log_content

    def test_orchestrator_logs_refinement_prompt(self, tmp_path):
        """Test orchestrator logs refinement prompts with error/feedback.
        
        Validates that:
        - Refinement prompts are logged
        - Contains "LLM Prompt (syntax fix):" or "LLM Prompt (design refinement):"
        - Includes previous error/feedback
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings
        from diag_agent.kroki.client import KrokiRenderError

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 5
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"
        mock_settings.validate_design = False

        mock_llm_client = Mock()
        mock_llm_client.validate_description.return_value = (True, None)  # Validation passes
        mock_llm_client.generate.side_effect = [
            "plantuml",  # Subtype detection
            "@startuml\\nInvalid\\n@enduml",
            "@startuml\\nFixed\\n@enduml"
        ]

        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.side_effect = [
            KrokiRenderError("Syntax error"),
            b"\\x89PNG",
            b"\\x89PNG"
        ]

        output_dir = tmp_path / "diagrams"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            orchestrator.execute(
                description="Test",
                diagram_type="plantuml",
                output_dir=str(output_dir),
                output_formats="png"
            )

        # Assert
        log_content = (output_dir / "generation.log").read_text()
        assert "LLM Prompt (syntax fix):" in log_content

    def test_cli_shows_minimal_progress_updates(self, tmp_path, capsys):
        """Test CLI shows minimal progress updates to stdout.
        
        Validates that:
        - "Generating diagram... [Iteration X/Y]" shown during execution
        - Final "✓ Diagram generated" message shown
        - "See generation.log for details" shown
        - Minimal output (no detailed errors on stdout)
        """
        from diag_agent.cli.commands import create
        from diag_agent.config.settings import Settings
        from click.testing import CliRunner

        # This test will fail initially because CLI doesn't show progress yet
        # We'll implement this in GREEN phase
        
        runner = CliRunner()
        
        # Mock the dependencies
        mock_settings = Mock(spec=Settings)
        mock_settings.max_iterations = 3
        mock_settings.max_time_seconds = 60
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"
        mock_settings.validate_design = False

        mock_llm_client = Mock()
        mock_llm_client.validate_description.return_value = (True, None)  # Validation passes
        mock_llm_client.generate.return_value = "@startuml\\nTest\\n@enduml"

        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.return_value = b"\\x89PNG"

        output_dir = str(tmp_path / "diagrams")

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client), \
             patch("diag_agent.cli.commands.Settings", return_value=mock_settings):
            
            # Act
            result = runner.invoke(create, [
                "Test diagram",
                "--type", "plantuml",
                "--output", output_dir,
                "--format", "png"
            ])

        # Assert
        assert result.exit_code == 0
        output = result.output
        
        # Should show progress updates
        assert "Generating diagram..." in output
        assert "[Iteration" in output
        
        # Should show final success message
        assert "✓ Diagram generated" in output
        
        # Should point to log file
        assert "generation.log" in output
        
        # Should NOT contain detailed errors (those go to log file)
        assert "Syntax error" not in output
        assert "Kroki" not in output or "Kroki" in output.split("generation.log")[0]  # Only before log reference
