"""MCP Server for diag-agent diagram generation.

Exposes diagram generation capabilities via Model Context Protocol (MCP)
using FastMCP framework.
"""

from typing import Dict, Any
from fastmcp import FastMCP

from diag_agent.config.settings import Settings
from diag_agent.agent.orchestrator import Orchestrator


# Initialize FastMCP server
mcp = FastMCP("diag-agent")


def create_diagram(
    description: str,
    diagram_type: str = "plantuml",
    output_dir: str = "./diagrams",
    output_formats: str = "png,svg,source"
) -> Dict[str, Any]:
    """Create a diagram from natural language description.

    Generates architecture diagrams autonomously using AI with syntax validation
    and design feedback via Kroki integration.

    Args:
        description: Natural language description of the diagram to create
        diagram_type: Type of diagram (plantuml, c4plantuml, mermaid, etc.)
        output_dir: Output directory for generated diagrams
        output_formats: Comma-separated output formats (png, svg, pdf, source)

    Returns:
        Dictionary with:
        - diagram_source: Generated diagram source code
        - output_path: Path to primary output file
        - iterations_used: Number of LLM iterations performed
        - elapsed_seconds: Total time elapsed
        - stopped_reason: Why iteration stopped (success, max_iterations, max_time)

    Raises:
        Exception: If diagram generation fails
    """
    # Load settings
    settings = Settings()

    # Create orchestrator
    orchestrator = Orchestrator(settings)

    # Execute diagram generation
    result = orchestrator.execute(
        description=description,
        diagram_type=diagram_type,
        output_dir=output_dir,
        output_formats=output_formats
    )

    return result


# Register tool with MCP server
mcp.tool()(create_diagram)


if __name__ == "__main__":
    # Run MCP server
    mcp.run()
