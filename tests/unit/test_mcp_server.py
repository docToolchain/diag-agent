"""Unit tests for MCP Server."""

import pytest
from unittest.mock import Mock, patch


class TestMCPServer:
    """Tests for MCP Server and create_diagram tool."""

    def test_mcp_server_initialization(self):
        """Test MCP server initializes correctly with FastMCP.

        Validates that:
        - Server can be imported and created
        - Server has correct name
        - create_diagram tool is registered
        """
        from diag_agent.mcp.server import mcp, create_diagram

        # Assert server exists and has expected name
        assert mcp is not None
        assert "diag-agent" in mcp.name.lower() or "diagram" in mcp.name.lower()

        # Assert create_diagram function is importable and callable
        assert create_diagram is not None
        assert callable(create_diagram), "create_diagram should be callable"

    def test_create_diagram_tool_success(self):
        """Test create_diagram tool executes Orchestrator successfully.

        Validates that:
        - Tool calls Orchestrator.execute() with correct parameters
        - Tool returns diagram source and metadata
        - Success case produces expected output structure
        """
        from diag_agent.mcp.server import create_diagram

        # Arrange
        description = "User authentication flow"
        expected_result = {
            "diagram_source": "@startuml\nAlice -> Bob\n@enduml",
            "output_path": "./diagrams/diagram.png",
            "iterations_used": 1,
            "elapsed_seconds": 2.5,
            "stopped_reason": "success"
        }

        mock_orchestrator = Mock()
        mock_orchestrator.execute.return_value = expected_result

        with patch("diag_agent.mcp.server.Orchestrator", return_value=mock_orchestrator):
            with patch("diag_agent.mcp.server.Settings"):
                # Act
                result = create_diagram(description)

        # Assert
        assert result is not None
        assert "diagram_source" in result
        assert "output_path" in result
        assert result["diagram_source"] == expected_result["diagram_source"]
        assert result["iterations_used"] == 1
        assert result["stopped_reason"] == "success"

        # Verify Orchestrator.execute was called
        mock_orchestrator.execute.assert_called_once()

    def test_create_diagram_with_custom_parameters(self):
        """Test create_diagram accepts and forwards custom parameters.

        Validates that:
        - Tool accepts diagram_type parameter
        - Tool accepts output_dir parameter
        - Tool accepts output_formats parameter
        - All parameters are forwarded to Orchestrator.execute()
        """
        from diag_agent.mcp.server import create_diagram

        # Arrange
        description = "API architecture"
        diagram_type = "c4plantuml"
        output_dir = "./custom/output"
        output_formats = "svg,pdf"

        mock_orchestrator = Mock()
        mock_orchestrator.execute.return_value = {
            "diagram_source": "test source",
            "output_path": "./custom/output/diagram.svg",
            "iterations_used": 1,
            "elapsed_seconds": 1.0,
            "stopped_reason": "success"
        }

        with patch("diag_agent.mcp.server.Orchestrator", return_value=mock_orchestrator):
            with patch("diag_agent.mcp.server.Settings"):
                # Act
                result = create_diagram(
                    description=description,
                    diagram_type=diagram_type,
                    output_dir=output_dir,
                    output_formats=output_formats
                )

        # Assert - Verify parameters were forwarded
        mock_orchestrator.execute.assert_called_once_with(
            description=description,
            diagram_type=diagram_type,
            output_dir=output_dir,
            output_formats=output_formats
        )
        assert result["output_path"] == "./custom/output/diagram.svg"

    def test_create_diagram_returns_correct_structure(self):
        """Test create_diagram returns expected JSON structure.

        Validates that:
        - Return value is a dictionary
        - Contains all required fields (diagram_source, output_path, metadata)
        - Field types are correct (strings, integers, etc.)
        """
        from diag_agent.mcp.server import create_diagram

        # Arrange
        mock_result = {
            "diagram_source": "@startuml\nA -> B\n@enduml",
            "output_path": "./diagrams/diagram.png",
            "iterations_used": 3,
            "elapsed_seconds": 5.2,
            "stopped_reason": "max_iterations"
        }

        mock_orchestrator = Mock()
        mock_orchestrator.execute.return_value = mock_result

        with patch("diag_agent.mcp.server.Orchestrator", return_value=mock_orchestrator):
            with patch("diag_agent.mcp.server.Settings"):
                # Act
                result = create_diagram("test description")

        # Assert - Verify structure
        assert isinstance(result, dict), "Result should be a dictionary"

        # Required fields
        assert "diagram_source" in result
        assert "output_path" in result
        assert "iterations_used" in result
        assert "elapsed_seconds" in result
        assert "stopped_reason" in result

        # Field types
        assert isinstance(result["diagram_source"], str)
        assert isinstance(result["output_path"], str)
        assert isinstance(result["iterations_used"], int)
        assert isinstance(result["elapsed_seconds"], (int, float))
        assert isinstance(result["stopped_reason"], str)

    def test_create_diagram_error_handling(self):
        """Test create_diagram handles Orchestrator errors gracefully.

        Validates that:
        - Exceptions from Orchestrator are caught
        - Error message is included in response or re-raised appropriately
        - Tool doesn't crash on errors
        """
        from diag_agent.mcp.server import create_diagram

        # Arrange
        mock_orchestrator = Mock()
        mock_orchestrator.execute.side_effect = Exception("Kroki server unavailable")

        with patch("diag_agent.mcp.server.Orchestrator", return_value=mock_orchestrator):
            with patch("diag_agent.mcp.server.Settings"):
                # Act & Assert - Exception should be raised or handled
                with pytest.raises(Exception) as exc_info:
                    create_diagram("test description")

                assert "Kroki" in str(exc_info.value) or "unavailable" in str(exc_info.value)
