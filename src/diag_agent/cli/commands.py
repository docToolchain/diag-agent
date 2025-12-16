"""CLI commands for diag-agent.

Entry point for the command-line interface using Click framework.
"""

import click
from pathlib import Path
from typing import List, Tuple

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


# ============================================================================
# Examples Commands
# ============================================================================

def _get_examples_dir() -> Path:
    """Get the path to the examples directory.

    Returns:
        Path to src/diag_agent/examples/
    """
    # Get the directory where this commands.py file is located
    cli_dir = Path(__file__).parent
    # Navigate to examples: cli/ -> diag_agent/ -> examples/
    examples_dir = cli_dir.parent / "examples"
    return examples_dir


def _list_examples(diagram_type: str = None) -> List[Tuple[str, str]]:
    """List all available examples, optionally filtered by type.

    Args:
        diagram_type: Optional diagram type to filter by (e.g., "c4plantuml", "bpmn")

    Returns:
        List of (diagram_type, example_name) tuples
    """
    examples_dir = _get_examples_dir()
    examples = []

    # Iterate through type directories (c4plantuml, bpmn, etc.)
    for type_dir in examples_dir.iterdir():
        if not type_dir.is_dir() or type_dir.name.startswith("_"):
            continue

        # Filter by type if specified
        if diagram_type and type_dir.name != diagram_type:
            continue

        # Iterate through example files
        for example_file in type_dir.iterdir():
            if example_file.is_file() and not example_file.name.startswith("_"):
                # Extract example name (without extension)
                example_name = example_file.stem
                examples.append((type_dir.name, example_name))

    return sorted(examples)


def _load_example(example_path: str) -> str:
    """Load an example diagram source code.

    Args:
        example_path: Path to example in format "type/name" (e.g., "c4plantuml/context-diagram")

    Returns:
        Example source code

    Raises:
        FileNotFoundError: If example does not exist
    """
    examples_dir = _get_examples_dir()

    # Parse example path
    parts = example_path.split("/")
    if len(parts) != 2:
        raise ValueError(f"Invalid example path format: {example_path}. Expected: type/name")

    diagram_type, example_name = parts

    # Find the example file (try common extensions)
    type_dir = examples_dir / diagram_type
    if not type_dir.exists():
        raise FileNotFoundError(f"Diagram type not found: {diagram_type}")

    # Try common extensions based on diagram type
    extensions = {
        "c4plantuml": [".puml", ".plantuml"],
        "plantuml": [".puml", ".plantuml"],
        "bpmn": [".bpmn"],
        "mermaid": [".mmd", ".mermaid"],
    }

    possible_extensions = extensions.get(diagram_type, [".txt"])

    for ext in possible_extensions:
        example_file = type_dir / f"{example_name}{ext}"
        if example_file.exists():
            return example_file.read_text()

    raise FileNotFoundError(f"Example not found: {example_path}")


@cli.group()
def examples():
    """Manage and view example diagrams.

    Browse available diagram examples for different diagram types
    (C4-PlantUML, BPMN, etc.) to learn syntax and use as templates.
    """
    pass


@examples.command(name="list")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Filter examples by diagram type (c4plantuml, bpmn, etc.)"
)
def list_examples(diagram_type: str):
    """List all available example diagrams.

    Examples:

        diag-agent examples list

        diag-agent examples list --type c4plantuml
    """
    try:
        examples_list = _list_examples(diagram_type)

        if not examples_list:
            if diagram_type:
                click.echo(f"No examples found for type: {diagram_type}")
            else:
                click.echo("No examples available.")
            return

        # Display examples grouped by type
        click.echo("Available examples:\n")

        current_type = None
        for ex_type, ex_name in examples_list:
            # Print type header when it changes
            if ex_type != current_type:
                click.echo(f"[{ex_type}]")
                current_type = ex_type

            # Print example name
            click.echo(f"  {ex_name}")

        click.echo(f"\nTotal: {len(examples_list)} examples")
        click.echo("\nUse 'diag-agent examples show <type>/<name>' to view source code.")

    except Exception as e:
        click.echo(f"Error listing examples: {e}", err=True)
        raise click.Abort()


@examples.command(name="show")
@click.argument("example_name")
def show_example(example_name: str):
    """Show the source code of an example diagram.

    EXAMPLE_NAME should be in format: type/name

    Examples:

        diag-agent examples show c4plantuml/context-diagram

        diag-agent examples show bpmn/simple-process
    """
    try:
        source_code = _load_example(example_name)
        click.echo(source_code)

    except FileNotFoundError as e:
        click.echo(f"Error: Example not found: {example_name}", err=True)
        click.echo(f"Details: {e}", err=True)
        click.echo("\nUse 'diag-agent examples list' to see available examples.", err=True)
        raise click.Abort()
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("\nExample name should be in format: type/name", err=True)
        click.echo("Example: diag-agent examples show c4plantuml/context-diagram", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error loading example: {e}", err=True)
        raise click.Abort()
