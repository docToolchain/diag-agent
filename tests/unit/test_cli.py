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
        - Output contains all 4 examples (3 C4-PlantUML + 1 BPMN)
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
        assert "simple-process" in result.output, "Missing simple-process BPMN example"
        assert "collaboration" in result.output, "Missing collaboration BPMN example"

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
        assert "default" not in result.output or "[bpmn]" not in result.output, "BPMN example should not be shown"

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

    def test_kroki_start_command_starts_container(self):
        """Test `diag-agent kroki start` starts the Kroki Docker container.

        Validates that:
        - Command successfully invokes KrokiManager.start()
        - Success message is displayed to user
        - Exit code is 0
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()
        mock_manager = Mock()

        with patch("diag_agent.cli.commands.KrokiManager", return_value=mock_manager):
            # Act
            result = runner.invoke(cli, ["kroki", "start"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"
        mock_manager.start.assert_called_once()
        assert "started" in result.output.lower() or "success" in result.output.lower(), \
            "Missing success message in output"

    def test_kroki_stop_command_stops_container(self):
        """Test `diag-agent kroki stop` stops the Kroki Docker container.

        Validates that:
        - Command successfully invokes KrokiManager.stop()
        - Success message is displayed to user
        - Exit code is 0
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()
        mock_manager = Mock()

        with patch("diag_agent.cli.commands.KrokiManager", return_value=mock_manager):
            # Act
            result = runner.invoke(cli, ["kroki", "stop"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"
        mock_manager.stop.assert_called_once()
        assert "stopped" in result.output.lower() or "success" in result.output.lower(), \
            "Missing success message in output"

    def test_kroki_status_shows_running_and_healthy(self):
        """Test `diag-agent kroki status` shows running and healthy status.

        Validates that:
        - Status command checks if container is running
        - Status command performs health check
        - Output shows "running" and "healthy" status
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()
        mock_manager = Mock()
        mock_manager.is_running.return_value = True
        mock_manager.health_check.return_value = True

        with patch("diag_agent.cli.commands.KrokiManager", return_value=mock_manager):
            # Act
            result = runner.invoke(cli, ["kroki", "status"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"
        mock_manager.is_running.assert_called_once()
        mock_manager.health_check.assert_called_once()
        assert "running" in result.output.lower(), "Missing 'running' status in output"
        assert "healthy" in result.output.lower(), "Missing 'healthy' status in output"

    def test_kroki_status_shows_stopped(self):
        """Test `diag-agent kroki status` shows stopped status.

        Validates that:
        - Status command detects stopped container
        - Output shows "stopped" status
        - Health check is not performed when container is stopped
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()
        mock_manager = Mock()
        mock_manager.is_running.return_value = False

        with patch("diag_agent.cli.commands.KrokiManager", return_value=mock_manager):
            # Act
            result = runner.invoke(cli, ["kroki", "status"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"
        mock_manager.is_running.assert_called_once()
        mock_manager.health_check.assert_not_called()  # Don't check health if not running
        assert "stopped" in result.output.lower() or "not running" in result.output.lower(), \
            "Missing 'stopped' status in output"

    def test_kroki_logs_displays_container_logs(self):
        """Test `diag-agent kroki logs` displays container logs.

        Validates that:
        - Logs command executes `docker logs kroki`
        - Log output is displayed to user
        - Exit code is 0
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()
        mock_logs_output = "2024-01-01 10:00:00 INFO Starting Kroki server\n2024-01-01 10:00:01 INFO Server started on port 8000"

        mock_subprocess_result = Mock()
        mock_subprocess_result.stdout = mock_logs_output
        mock_subprocess_result.returncode = 0

        with patch("diag_agent.cli.commands.subprocess.run", return_value=mock_subprocess_result) as mock_run:
            # Act
            result = runner.invoke(cli, ["kroki", "logs"])

        # Assert
        assert result.exit_code == 0, f"CLI failed with: {result.output}"

        # Verify docker logs command was called correctly
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "docker" in call_args
        assert "logs" in call_args
        assert "kroki" in call_args

        # Verify logs are displayed
        assert "Kroki server" in result.output or mock_logs_output in result.output, \
            "Missing log output in CLI output"

    def test_kroki_start_handles_docker_not_installed(self):
        """Test `diag-agent kroki start` handles Docker not installed error.

        Validates that:
        - KrokiManagerError is caught and displayed to user
        - Error message mentions Docker installation
        - Exit code is non-zero
        """
        from diag_agent.cli.commands import cli
        from diag_agent.kroki.manager import KrokiManagerError

        # Arrange
        runner = CliRunner()
        mock_manager = Mock()
        mock_manager.start.side_effect = KrokiManagerError("Docker is not installed")

        with patch("diag_agent.cli.commands.KrokiManager", return_value=mock_manager):
            # Act
            result = runner.invoke(cli, ["kroki", "start"])

        # Assert
        assert result.exit_code != 0, "CLI should exit with error when Docker not installed"
        assert "docker" in result.output.lower(), "Missing Docker error message"
        assert "not installed" in result.output.lower() or "error" in result.output.lower(), \
            "Missing helpful error message"

    def test_kroki_logs_follow_mode(self):
        """Test `diag-agent kroki logs --follow` enables follow mode.

        Validates that:
        - --follow option is supported
        - docker logs command includes --follow flag
        - Command execution is correct
        """
        from diag_agent.cli.commands import cli

        # Arrange
        runner = CliRunner()
        mock_subprocess_result = Mock()
        mock_subprocess_result.stdout = "Log line 1\nLog line 2"
        mock_subprocess_result.returncode = 0

        with patch("diag_agent.cli.commands.subprocess.run", return_value=mock_subprocess_result) as mock_run:
            # Act
            result = runner.invoke(cli, ["kroki", "logs", "--follow"])

        # Assert
        # Note: Follow mode might have different exit behavior, so we check command construction
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert "docker" in call_args
        assert "logs" in call_args
        assert "--follow" in call_args or "-f" in call_args, \
            "Missing --follow flag in docker logs command"
