"""Orchestrator for diagram generation workflow.

Coordinates the feedback loop between LLM, Kroki validation, and design analysis.
"""

from typing import Dict, Any
import time
import logging
from pathlib import Path

from diag_agent.llm.client import LLMClient
from diag_agent.kroki.client import KrokiClient, KrokiRenderError
from diag_agent.kroki.manager import KrokiManager, KrokiManagerError


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
        
        # Initialize Kroki client with auto-mode support
        kroki_url = self._determine_kroki_url(settings)
        self.kroki_client = KrokiClient(kroki_url)
    
    def _determine_kroki_url(self, settings: Any) -> str:
        """Determine which Kroki URL to use based on mode and availability.
        
        Auto-mode logic:
        - Try to use local Kroki (Docker) if available
        - Start container if needed
        - Fallback to remote (kroki.io) if local unavailable
        
        Local-mode: Use local Kroki only (no fallback)
        Remote-mode: Use remote Kroki only
        
        Args:
            settings: Application settings
            
        Returns:
            Kroki URL to use (local or remote)
        """
        mode = settings.kroki_mode
        
        # Remote mode: Use kroki.io directly
        if mode == "remote":
            return settings.kroki_remote_url
        
        # Auto-mode or Local-mode: Try to use local Kroki
        if mode in ("auto", "local"):
            try:
                manager = KrokiManager()
                
                # Check if container is running
                if not manager.is_running():
                    # Try to start container
                    manager.start()
                
                # Verify container is healthy
                if manager.health_check():
                    return settings.kroki_local_url
                
                # Health check failed
                if mode == "auto":
                    # Auto-mode: Fallback to remote
                    return settings.kroki_remote_url
                else:
                    # Local-mode: Use local even if unhealthy (explicit choice)
                    return settings.kroki_local_url
                    
            except KrokiManagerError:
                # Docker not available or start failed
                if mode == "auto":
                    # Auto-mode: Graceful fallback to remote
                    return settings.kroki_remote_url
                else:
                    # Local-mode: Let error propagate (explicit local required)
                    raise
        
        # Default fallback (shouldn't reach here)
        return settings.kroki_local_url
    
    def _setup_file_logger(self, log_file: Path) -> logging.Logger:
        """Setup file logger for generation.log.
        
        Args:
            log_file: Path to log file
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        # Remove existing handlers to avoid duplicates
        logger.handlers = []
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(file_handler)
        return logger
    
    def _cleanup_logger(self, logger: logging.Logger) -> None:
        """Cleanup logger file handlers.
        
        Args:
            logger: Logger instance to cleanup
        """
        for handler in logger.handlers:
            handler.close()
        logger.handlers = []

    def _detect_subtype(self, description: str, diagram_type: str) -> str:
        """Detect diagram subtype from description using LLM.
        
        Args:
            description: Natural language description of diagram
            diagram_type: Type of diagram (plantuml, c4plantuml, mermaid, etc.)
            
        Returns:
            Detected subtype (e.g., "context", "container", "sequence", "simple-process")
        """
        # Build prompt for subtype detection
        prompt = f"""Analyze this diagram description and identify the specific subtype.

Diagram type: {diagram_type}
Description: {description}

For C4 diagrams, possible subtypes are: context, container, component
For BPMN diagrams, possible subtypes are: simple-process, collaboration
For PlantUML diagrams, possible subtypes are: sequence, activity, class, component

Respond with ONLY the subtype name (one word, lowercase). If unsure, respond with the diagram type."""
        
        # Use LLM to detect subtype
        subtype = self.llm_client.generate(prompt).strip().lower()
        
        # Clean up response (remove any extra text, just get the first word)
        subtype = subtype.split()[0] if subtype else diagram_type
        
        return subtype
    
    def _load_example(self, diagram_type: str, subtype: str) -> str:
        """Load example diagram from examples directory.
        
        Tries to find an exact match for the subtype, otherwise returns
        the first available example for the diagram type.
        
        Args:
            diagram_type: Type of diagram (c4plantuml, bpmn, etc.)
            subtype: Specific subtype (context, simple-process, etc.)
            
        Returns:
            Example content as string, or None if no examples available
        """
        from pathlib import Path
        
        # Get examples directory (relative to this file)
        # orchestrator.py is in src/diag_agent/agent/
        # examples are in src/diag_agent/examples/
        current_file = Path(__file__)
        examples_dir = current_file.parent.parent / "examples" / diagram_type
        
        # Check if examples directory exists
        if not examples_dir.exists():
            return None
        
        # Try to find exact match for subtype
        # Example files can be named: {subtype}.ext or {subtype}-diagram.ext
        for pattern in [f"{subtype}.*", f"{subtype}-diagram.*"]:
            matches = list(examples_dir.glob(pattern))
            if matches:
                # Return first match
                return matches[0].read_text()
        
        # Fallback: Return first available example
        all_examples = [f for f in examples_dir.iterdir() if f.is_file() and not f.name.startswith("_")]
        if all_examples:
            return all_examples[0].read_text()
        
        # No examples available
        return None

    def execute(
        self,
        description: str,
        diagram_type: str = "plantuml",
        output_dir: str = "./diagrams",
        output_formats: str = "png,svg,source",
        progress_callback: Any = None
    ) -> Dict[str, Any]:
        """Execute diagram generation workflow with iteration limits.
        
        Args:
            description: Natural language description of diagram
            diagram_type: Type of diagram (plantuml, c4plantuml, mermaid, etc.)
            output_dir: Output directory for generated files
            output_formats: Comma-separated output formats
            progress_callback: Optional callback(message: str) for progress updates
            
        Returns:
            Dict with diagram_source, output_path, and metadata:
            - iterations_used: Number of iterations performed
            - elapsed_seconds: Total time elapsed
            - stopped_reason: Why iteration stopped (max_iterations | max_time | success)
        """
        # Setup logging to file
        output_path_obj = Path(output_dir)
        output_path_obj.mkdir(parents=True, exist_ok=True)
        log_file = output_path_obj / "generation.log"
        
        # Configure logger
        logger = self._setup_file_logger(log_file)
        
        # Detect subtype and load example (before iteration loop)
        subtype = self._detect_subtype(description, diagram_type)
        example_content = self._load_example(diagram_type, subtype)
        
        # Track iteration state
        iterations_used = 0
        start_time = time.time()
        stopped_reason = "success"
        diagram_source = ""  # Will be set by LLM
        validation_error = None  # Track validation errors for refinement
        design_feedback = None  # Track design feedback for refinement
        
        # Get limits from settings
        max_iterations = self.settings.max_iterations
        max_time_seconds = self.settings.max_time_seconds
        
        # Iteration loop
        while iterations_used < max_iterations:
            iterations_used += 1
            
            # Progress callback for CLI
            if progress_callback:
                progress_callback(f"Generating diagram... [Iteration {iterations_used}/{max_iterations}]")
            
            # Log iteration start
            logger.info(f"Iteration {iterations_used}/{max_iterations} - START")
            
            # Check time limit
            elapsed = time.time() - start_time
            if elapsed >= max_time_seconds:
                stopped_reason = "max_time"
                logger.info(f"Stopping: max_time ({max_time_seconds}s) reached")
                break
            
            # Build prompt for diagram generation
            if validation_error:
                # Refinement prompt with syntax error details
                prompt = f"Fix the following {diagram_type} diagram. Previous attempt had this error: {validation_error}\\n\\nOriginal request: {description}\\n\\nPrevious source:\\n{diagram_source}"
                # Add example if available
                if example_content:
                    prompt += f"\\n\\nReference example:\\n{example_content}"
                logger.info(f"LLM Prompt (syntax fix):")
                logger.info(f"  {prompt}")
            elif design_feedback:
                # Refinement prompt with design feedback
                prompt = f"Improve the following {diagram_type} diagram based on this design feedback: {design_feedback}\\n\\nOriginal request: {description}\\n\\nPrevious source:\\n{diagram_source}"
                # Add example if available
                if example_content:
                    prompt += f"\\n\\nReference example:\\n{example_content}"
                logger.info(f"LLM Prompt (design refinement):")
                logger.info(f"  {prompt}")
            else:
                # Initial prompt
                prompt = f"Generate a {diagram_type} diagram: {description}"
                # Add example if available
                if example_content:
                    prompt += f"\\n\\nReference example:\\n{example_content}"
                logger.info(f"LLM Prompt (initial):")
                logger.info(f"  {prompt}")
            
            # Call LLM to generate diagram source
            diagram_source = self.llm_client.generate(prompt)
            logger.info(f"LLM Response: {len(diagram_source)} characters")
            
            # Validate syntax with Kroki
            try:
                png_bytes = self.kroki_client.render_diagram(
                    diagram_source=diagram_source,
                    diagram_type=diagram_type,
                    output_format="png"
                )
                # Validation successful - diagram is syntactically valid
                validation_error = None
                logger.info("Kroki Validation: SUCCESS")
                
                # Design validation (if enabled)
                if self.settings.validate_design:
                    logger.info("Design Analysis: ANALYZING")
                    # Analyze design with vision-capable LLM
                    design_criteria_prompt = "Analyze this diagram for layout quality, readability, and spacing. If the design is good, respond with 'approved'. Otherwise, provide specific improvement suggestions."
                    feedback = self.llm_client.vision_analyze(png_bytes, design_criteria_prompt)
                    
                    # Check if design is approved
                    if "approved" in feedback.lower():
                        # Design approved - done!
                        design_feedback = None
                        logger.info("Design Feedback: APPROVED")
                        logger.info(f"Iteration {iterations_used}/{max_iterations} - COMPLETE (design approved)")
                        break
                    else:
                        # Design needs improvement - save feedback for refinement
                        design_feedback = feedback
                        logger.info("Design Feedback:")
                        logger.info(f"  {feedback}")
                        logger.info(f"Iteration {iterations_used}/{max_iterations} - COMPLETE (design improvement needed)")
                        # Continue to next iteration
                else:
                    # Design validation disabled - done after syntax check
                    logger.info(f"Iteration {iterations_used}/{max_iterations} - COMPLETE (syntax valid)")
                    break
                    
            except KrokiRenderError as e:
                # Validation failed - save error for refinement prompt
                validation_error = str(e)
                logger.info("Kroki Validation: ERROR")
                logger.info(f"  {validation_error}")
                logger.info(f"Iteration {iterations_used}/{max_iterations} - COMPLETE (validation error)")
                # Continue to next iteration for retry
        
        # Check if we hit iteration limit
        if iterations_used >= max_iterations and stopped_reason == "success":
            stopped_reason = "max_iterations"
            logger.info(f"Stopping: max_iterations ({max_iterations}) reached")
        
        # Calculate final elapsed time
        elapsed_seconds = time.time() - start_time
        logger.info(f"Final result: {iterations_used} iterations, {elapsed_seconds:.1f}s, stopped_reason={stopped_reason}")
        
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
        
        # Cleanup logger
        self._cleanup_logger(logger)
        
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
