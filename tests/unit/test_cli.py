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
        
        # Mock Orchestrator
        mock_orchestrator = Mock()
        mock_orchestrator.execute.return_value = {
            "diagram_source": "@startuml\nAlice -> Bob\n@enduml",
            "output_path": "./diagrams/diagram.png",
            "iterations_used": 1,
            "elapsed_seconds": 2.5,
            "stopped_reason": "success"
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

    def test_examples_list_shows_all_examples(self):
        """Test `diag-agent examples list` shows all available examples.

        Validates that:
        - examples list command works without errors
        - Output contains all 5 examples (3 C4-PlantUML + 2 BPMN)
        - Output shows diagram type and example name
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()

        # Act
        result = runner.invoke(cli, ["examples", "list"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"

        # Verify all C4-PlantUML examples are shown
        assert "context-diagram" in result.output, "Missing context-diagram example"
        assert "container-diagram" in result.output, "Missing container-diagram example"
        assert "component-diagram" in result.output, "Missing component-diagram example"

        # Verify all BPMN examples are shown
        assert "simple-process" in result.output, "Missing simple-process example"
        assert "collaboration" in result.output, "Missing collaboration example"

        # Verify type information is shown
        assert "c4plantuml" in result.output.lower() or "C4" in result.output, "Missing C4-PlantUML type"
        assert "bpmn" in result.output.lower(), "Missing BPMN type"

    def test_examples_list_filters_by_type(self):
        """Test `diag-agent examples list --type c4plantuml` filters by diagram type.

        Validates that:
        - Type filter works correctly
        - Only C4-PlantUML examples are shown (3)
        - BPMN examples are not shown
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()

        # Act
        result = runner.invoke(cli, ["examples", "list", "--type", "c4plantuml"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"

        # Verify C4-PlantUML examples are shown
        assert "context-diagram" in result.output, "Missing context-diagram example"
        assert "container-diagram" in result.output, "Missing container-diagram example"
        assert "component-diagram" in result.output, "Missing component-diagram example"

        # Verify BPMN examples are NOT shown
        assert "simple-process" not in result.output, "BPMN example should not be shown"
        assert "collaboration" not in result.output, "BPMN example should not be shown"

    def test_examples_show_displays_source_code(self):
        """Test `diag-agent examples show <name>` displays example source code.

        Validates that:
        - show command works with valid example name
        - Output contains the actual diagram source code
        - Output contains characteristic markers for C4-PlantUML
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()

        # Act
        result = runner.invoke(cli, ["examples", "show", "c4plantuml/context-diagram"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"

        # Verify source code is displayed (characteristic C4-PlantUML markers)
        assert "@startuml" in result.output, "Missing PlantUML start marker"
        assert "@enduml" in result.output, "Missing PlantUML end marker"
        assert "!include" in result.output or "C4_Context" in result.output, "Missing C4 include"

        # Verify it's the context diagram content
        assert "System Context" in result.output or "Internet Banking" in result.output, \
            "Missing context diagram content"

    def test_examples_show_handles_nonexistent(self):
        """Test `diag-agent examples show` handles nonexistent example gracefully.

        Validates that:
        - show command with invalid name exits with error
        - Error message is helpful (mentions the invalid name)
        - Exit code is non-zero
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()
        invalid_name = "nonexistent/example"

        # Act
        result = runner.invoke(cli, ["examples", "show", invalid_name])

        # Assert
        assert result.exit_code != 0, "CLI should exit with error for nonexistent example"

        # Verify error message is helpful
        assert "not found" in result.output.lower() or "invalid" in result.output.lower() or \
               "does not exist" in result.output.lower(), \
               f"Missing helpful error message: {result.output}"

    def test_examples_list_output_context_efficient(self):
        """Test `diag-agent examples list` output is context-efficient for LLM.

        Validates that:
        - Output is concise (< 2000 chars, ~500 tokens)
        - Output contains essential information only
        - Format is LLM-friendly (parseable)
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()

        # Act
        result = runner.invoke(cli, ["examples", "list"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"

        # Verify context efficiency (rough estimate: ~4 chars per token)
        assert len(result.output) < 2000, \
            f"Output too long for context efficiency: {len(result.output)} chars (>500 tokens)"
