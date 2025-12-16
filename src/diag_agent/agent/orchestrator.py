"""Orchestrator for diagram generation workflow.

Coordinates the feedback loop between LLM, Kroki validation, and design analysis.
"""

from typing import Dict, Any
import time
from pathlib import Path

from diag_agent.llm.client import LLMClient
from diag_agent.kroki.client import KrokiClient, KrokiRenderError


class Orchestrator:
    """Orchestrates the diagram generation process with autonomous feedback loop.
    
    The orchestrator manages:
    - LLM prompting for diagram generation
    - Syntax validation via Kroki
    - Design feedback via vision analysis
    - Iteration limits and timeouts
    """
    
    def __init__(self, settings: Any) -> None:
        """Initialize orchestrator with settings.
        
        Args:
            settings: Application settings (Settings instance)
        """
        self.settings = settings
        # Initialize LLM client for diagram generation
        self.llm_client = LLMClient(settings)
        # Initialize Kroki client for syntax validation
        self.kroki_client = KrokiClient(settings.kroki_local_url)
    
    def execute(
        self,
        description: str,
        diagram_type: str = "plantuml",
        output_dir: str = "./diagrams",
        output_formats: str = "png,svg,source"
    ) -> Dict[str, Any]:
        """Execute diagram generation workflow with iteration limits.
        
        Args:
            description: Natural language description of diagram
            diagram_type: Type of diagram (plantuml, c4plantuml, mermaid, etc.)
            output_dir: Output directory for generated files
            output_formats: Comma-separated output formats
            
        Returns:
            Dict with diagram_source, output_path, and metadata:
            - iterations_used: Number of iterations performed
            - elapsed_seconds: Total time elapsed
            - stopped_reason: Why iteration stopped (max_iterations | max_time | success)
        """
        # Track iteration state
        iterations_used = 0
        start_time = time.time()
        stopped_reason = "success"
        diagram_source = ""  # Will be set by LLM
        validation_error = None  # Track validation errors for refinement
        
        # Get limits from settings
        max_iterations = self.settings.max_iterations
        max_time_seconds = self.settings.max_time_seconds
        
        # Iteration loop
        while iterations_used < max_iterations:
            iterations_used += 1
            
            # Check time limit
            elapsed = time.time() - start_time
            if elapsed >= max_time_seconds:
                stopped_reason = "max_time"
                break
            
            # Build prompt for diagram generation
            if validation_error:
                # Refinement prompt with error details
                prompt = f"Fix the following {diagram_type} diagram. Previous attempt had this error: {validation_error}\n\nOriginal request: {description}\n\nPrevious source:\n{diagram_source}"
            else:
                # Initial prompt
                prompt = f"Generate a {diagram_type} diagram: {description}"
            
            # Call LLM to generate diagram source
            diagram_source = self.llm_client.generate(prompt)
            
            # Validate syntax with Kroki
            try:
                self.kroki_client.render_diagram(
                    diagram_source=diagram_source,
                    diagram_type=diagram_type,
                    output_format="png"
                )
                # Validation successful - diagram is syntactically valid
                validation_error = None
                break  # Success!
            except KrokiRenderError as e:
                # Validation failed - save error for refinement prompt
                validation_error = str(e)
                # Continue to next iteration for retry
        
        # Check if we hit iteration limit
        if iterations_used >= max_iterations and stopped_reason == "success":
            stopped_reason = "max_iterations"
        
        # Calculate final elapsed time
        elapsed_seconds = time.time() - start_time
        
        # Write output files
        output_path_obj = Path(output_dir)
        output_path_obj.mkdir(parents=True, exist_ok=True)
        
        # Parse output formats (comma-separated)
        formats = [fmt.strip() for fmt in output_formats.split(",")]
        primary_output_path = None
        
        for fmt in formats:
            if fmt == "source":
                # Write source file with appropriate extension
                extension = self._get_source_extension(diagram_type)
                file_path = output_path_obj / f"diagram{extension}"
                file_path.write_text(diagram_source)
            else:
                # Render diagram via Kroki
                rendered_bytes = self.kroki_client.render_diagram(
                    diagram_source=diagram_source,
                    diagram_type=diagram_type,
                    output_format=fmt
                )
                file_path = output_path_obj / f"diagram.{fmt}"
                file_path.write_bytes(rendered_bytes)
            
            # Track first file as primary output
            if primary_output_path is None:
                primary_output_path = str(file_path)
        
        return {
            "diagram_source": diagram_source,
            "output_path": primary_output_path,
            "iterations_used": iterations_used,
            "elapsed_seconds": elapsed_seconds,
            "stopped_reason": stopped_reason
        }
    
    def _get_source_extension(self, diagram_type: str) -> str:
        """Get file extension for source format based on diagram type.
        
        Args:
            diagram_type: Type of diagram (plantuml, mermaid, etc.)
            
        Returns:
            File extension including dot (e.g., ".puml", ".mmd")
        """
        # Extension mapping for common diagram types
        extension_map = {
            "plantuml": ".puml",
            "c4plantuml": ".puml",
            "mermaid": ".mmd",
        }
        return extension_map.get(diagram_type, f".{diagram_type}")
