"""CLI commands for diag-agent.

Entry point for the command-line interface using Click framework.
"""

import click

from diag_agent.config.settings import Settings
from diag_agent.agent.orchestrator import Orchestrator


@click.group()
@click.version_option(version="0.1.0", prog_name="diag-agent")
def cli():
    """diag-agent - LLM-powered diagram generator.
    
    Generate architecture diagrams autonomously using AI with syntax validation
    and design feedback via Kroki integration.
    """
    pass


@cli.command()
@click.argument("description")
@click.option(
    "--type",
    "diagram_type",
    default="plantuml",
    help="Diagram type (plantuml, c4plantuml, mermaid, etc.)"
)
@click.option(
    "--output",
    default="./diagrams",
    help="Output directory for generated diagrams"
)
@click.option(
    "--format",
    "output_format",
    default="png,svg,source",
    help="Output formats (comma-separated: png, svg, pdf, source)"
)
def create(description: str, diagram_type: str, output: str, output_format: str):
    """Create a diagram from natural language description.
    
    DESCRIPTION is a natural language description of the diagram you want to create.
    
    Examples:
    
        diag-agent create "User authentication flow"
        
        diag-agent create "C4 context diagram for API gateway" --type c4plantuml
    """
    # Load settings
    settings = Settings()
    
    # Create orchestrator
    orchestrator = Orchestrator(settings)
    
    # Execute diagram generation
    result = orchestrator.execute(
        description=description,
        diagram_type=diagram_type,
        output_dir=output,
        output_formats=output_format
    )
    
    # Display result
    click.echo(f"✓ Diagram generated: {result['output_path']}")
    click.echo(f"  Source: {len(result['diagram_source'])} characters")
    click.echo(f"  Iterations: {result['iterations_used']}")
    click.echo(f"  Time: {result['elapsed_seconds']:.1f}s")
    click.echo(f"  Stopped: {result['stopped_reason']}")
