"""Orchestrator for diagram generation workflow.

Coordinates the feedback loop between LLM, Kroki validation, and design analysis.
"""

from typing import Dict, Any
import time


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
        diagram_source = "@startuml\n' Generated diagram\n@enduml"  # Default value
        
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
            
            # TODO: In later TDD cycles:
            # - Call LLMClient to generate diagram source
            # - Validate with KrokiClient
            # - Analyze design with Analyzer
            # - Build refinement prompt if needed
            # For now, just break after 1 iteration (MVP)
            break  # Success after first iteration (MVP)
        
        # Check if we hit iteration limit
        if iterations_used >= max_iterations and stopped_reason == "success":
            stopped_reason = "max_iterations"
        
        # Calculate final elapsed time
        elapsed_seconds = time.time() - start_time
        
        return {
            "diagram_source": diagram_source,
            "output_path": f"{output_dir}/diagram.png",
            "iterations_used": iterations_used,
            "elapsed_seconds": elapsed_seconds,
            "stopped_reason": stopped_reason
        }
