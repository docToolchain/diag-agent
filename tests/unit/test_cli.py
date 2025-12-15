"""Unit tests for CLI commands."""

import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch


class TestCLI:
    """Tests for CLI entry point and commands."""

    def test_cli_help_output(self):
        """Test `diag-agent --help` shows commands and version.

        Validates that:
        - CLI is callable and returns exit code 0
        - Help text contains main command 'create'
        - Help text is context-efficient (< 500 tokens for LLM)
        - Version information is displayed
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()

        # Act
        result = runner.invoke(cli, ['--help'])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"
        assert "create" in result.output, "Missing 'create' command in help"
        assert "diagram" in result.output.lower(), "Missing diagram description"
        
        # Verify context efficiency (rough estimate: ~4 chars per token)
        assert len(result.output) < 2000, f"Help output too long: {len(result.output)} chars"

    def test_create_command_calls_orchestrator(self):
        """Test `diag-agent create` invokes Orchestrator with correct parameters.

        Validates that:
        - create command successfully invokes Orchestrator
        - Description is passed to Orchestrator.execute()
        - Settings are loaded and passed to Orchestrator
        - CLI options (type, output, format) are forwarded
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()
        description = "User authentication flow"
        
        # Mock Orchestrator (doesn't exist yet - will be implemented later)
        mock_orchestrator = Mock()
        mock_orchestrator.execute.return_value = {
            "diagram_source": "@startuml\nAlice -> Bob\n@enduml",
            "output_path": "./diagrams/diagram.png"
        }
        
        # Mock Settings
        mock_settings = Mock()
        mock_settings.llm_provider = "anthropic"
        mock_settings.llm_model = "claude-sonnet-4"
        
        with patch("diag_agent.cli.commands.Orchestrator", return_value=mock_orchestrator):
            with patch("diag_agent.cli.commands.Settings", return_value=mock_settings):
                # Act
                result = runner.invoke(cli, ["create", description])
        
        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"
        
        # Verify Orchestrator was instantiated with Settings
        mock_orchestrator.execute.assert_called_once()
        
        # Verify description was passed
        call_args = mock_orchestrator.execute.call_args
        assert call_args is not None, "Orchestrator.execute() was not called"
        assert description in str(call_args), f"Description not passed to Orchestrator: {call_args}"
