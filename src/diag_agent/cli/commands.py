"""CLI commands for diag-agent.

Entry point for the command-line interface using Click framework.
"""

import click


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
def create(description: str, type: str, output: str, output_format: str):
    """Create a diagram from natural language description.
    
    DESCRIPTION is a natural language description of the diagram you want to create.
    
    Examples:
    
        diag-agent create "User authentication flow"
        
        diag-agent create "C4 context diagram for API gateway" --type c4plantuml
    """
    # TODO: Implementation in next TDD cycle (with Orchestrator integration)
    click.echo(f"Creating {type} diagram: {description}")
    click.echo(f"Output: {output}")
    click.echo(f"Formats: {output_format}")
