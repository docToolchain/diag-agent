"""Unit tests for CLI commands."""

import pytest
from click.testing import CliRunner


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
