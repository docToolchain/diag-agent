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
