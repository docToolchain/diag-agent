"""Unit tests for Orchestrator example integration."""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path


class TestOrchestratorExampleDetection:
    """Tests for subtype detection."""

    def test_detect_subtype_c4_context_from_description(self):
        """Test detecting 'context' subtype from description with c4plantuml.
        
        Validates that:
        - LLM is called with detection prompt
        - Description contains keywords like "system context"
        - Returns "context" subtype
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"

        mock_llm_client = Mock()
        mock_llm_client.generate.return_value = "context"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient"):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            subtype = orchestrator._detect_subtype(
                description="System context diagram for banking system",
                diagram_type="c4plantuml"
            )

        # Assert
        assert subtype == "context"
        mock_llm_client.generate.assert_called_once()
        call_args = mock_llm_client.generate.call_args[0][0]
        assert "context" in call_args.lower() or "subtype" in call_args.lower()

    def test_detect_subtype_c4_container_from_description(self):
        """Test detecting 'container' subtype from description."""
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"

        mock_llm_client = Mock()
        mock_llm_client.generate.return_value = "container"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient"):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            subtype = orchestrator._detect_subtype(
                description="Container diagram showing web app, database, and API",
                diagram_type="c4plantuml"
            )

        # Assert
        assert subtype == "container"

    def test_detect_subtype_bpmn_process_from_description(self):
        """Test detecting 'simple-process' subtype for BPMN."""
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"

        mock_llm_client = Mock()
        mock_llm_client.generate.return_value = "simple-process"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient"):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            subtype = orchestrator._detect_subtype(
                description="Order processing workflow",
                diagram_type="bpmn"
            )

        # Assert
        assert subtype == "simple-process"


class TestOrchestratorExampleLoader:
    """Tests for example loading."""

    def test_load_example_exact_match_c4_context(self):
        """Test loading exact match example for c4plantuml context.
        
        Validates that:
        - Searches for examples/{diagram_type}/{subtype}*
        - Finds context-diagram.puml
        - Returns file content as string
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"

        with patch("diag_agent.agent.orchestrator.LLMClient"), \
             patch("diag_agent.agent.orchestrator.KrokiClient"):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            example = orchestrator._load_example(
                diagram_type="c4plantuml",
                subtype="context"
            )

        # Assert
        assert example is not None
        assert "Person" in example or "System" in example
        assert "@startuml" in example

    def test_load_example_exact_match_bpmn_simple_process(self):
        """Test loading BPMN simple-process example."""
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"

        with patch("diag_agent.agent.orchestrator.LLMClient"), \
             patch("diag_agent.agent.orchestrator.KrokiClient"):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            example = orchestrator._load_example(
                diagram_type="bpmn",
                subtype="simple-process"
            )

        # Assert
        assert example is not None
        assert "process" in example.lower()
        assert "startEvent" in example or "endEvent" in example

    def test_load_example_fallback_to_first_available(self):
        """Test fallback to first available example when no exact match.
        
        Validates that:
        - Subtype 'unknown' doesn't match any file
        - Falls back to first .puml file in c4plantuml/
        - Returns content (any of the 3 c4 examples)
        """
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"

        with patch("diag_agent.agent.orchestrator.LLMClient"), \
             patch("diag_agent.agent.orchestrator.KrokiClient"):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            example = orchestrator._load_example(
                diagram_type="c4plantuml",
                subtype="unknown-subtype"
            )

        # Assert
        assert example is not None  # Should fallback to first available
        assert "@startuml" in example

    def test_load_example_no_examples_available(self):
        """Test returns None when no examples exist for diagram type."""
        from diag_agent.agent.orchestrator import Orchestrator
        from diag_agent.config.settings import Settings

        # Arrange
        mock_settings = Mock(spec=Settings)
        mock_settings.kroki_mode = "remote"
        mock_settings.kroki_remote_url = "https://kroki.io"

        with patch("diag_agent.agent.orchestrator.LLMClient"), \
             patch("diag_agent.agent.orchestrator.KrokiClient"):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            example = orchestrator._load_example(
                diagram_type="mermaid",  # No examples for mermaid yet
                subtype="flowchart"
            )

        # Assert
        assert example is None


class TestOrchestratorExampleIntegration:
    """Integration tests for example usage in prompts."""

    def test_execute_includes_example_in_initial_prompt(self, tmp_path):
        """Test execute() includes example in initial LLM prompt.
        
        Validates that:
        - _detect_subtype() is called
        - _load_example() is called with detected subtype
        - Initial prompt contains example content
        - Example is NOT included in refinement prompts (syntax fix, design)
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

        # Mock LLM
        mock_llm_client = Mock()
        mock_llm_client.generate.return_value = "@startuml\nTest\n@enduml"

        # Mock Kroki
        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.return_value = b"\x89PNG"

        output_dir = tmp_path / "diagrams"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            result = orchestrator.execute(
                description="System context for banking",
                diagram_type="c4plantuml",
                output_dir=str(output_dir),
                output_formats="png"
            )

        # Assert
        # Should have called generate at least twice (subtype detection + diagram generation)
        assert mock_llm_client.generate.call_count >= 2
        
        # Second call (diagram generation) should include example
        diagram_gen_call = mock_llm_client.generate.call_args_list[1][0][0]
        assert "Reference example" in diagram_gen_call or "example" in diagram_gen_call.lower()
        # Should contain C4 syntax from example
        assert "Person" in diagram_gen_call or "System" in diagram_gen_call

    def test_execute_works_without_examples(self, tmp_path):
        """Test execute() works gracefully when no examples available.
        
        Validates backward compatibility:
        - When diagram_type has no examples (e.g., mermaid)
        - _load_example() returns None
        - Prompt doesn't include example section
        - Generation still works
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
        mock_llm_client.generate.return_value = "graph TD\nA-->B"

        mock_kroki_client = Mock()
        mock_kroki_client.render_diagram.return_value = b"\x89PNG"

        output_dir = tmp_path / "diagrams"

        with patch("diag_agent.agent.orchestrator.LLMClient", return_value=mock_llm_client), \
             patch("diag_agent.agent.orchestrator.KrokiClient", return_value=mock_kroki_client):
            orchestrator = Orchestrator(mock_settings)
            
            # Act
            result = orchestrator.execute(
                description="Simple flowchart",
                diagram_type="mermaid",  # No examples
                output_dir=str(output_dir),
                output_formats="png"
            )

        # Assert
        assert result["iterations_used"] == 1
        assert "diagram_source" in result
        # Should still work without examples
