# diag-agent

An LLM Agent for creating software architecture diagrams with autonomous syntax validation and design feedback.

## Features

- 🤖 **Autonomous diagram generation** with syntax validation and design feedback loop
- 🎨 **Multi-format support** via Kroki integration (PlantUML, C4, BPMN, Mermaid, etc.)
- 🚀 **Flexible deployment**: CLI tool, MCP server, or Python library
- 🔒 **Privacy-first**: Local-first approach with optional remote rendering
- 🔌 **LLM-agnostic**: Works with any LLM via LiteLLM (Anthropic, OpenAI, etc.)
- ⚡ **Context-efficient**: Minimal token consumption through optimized prompts

## Quick Start

### CLI Usage

```bash
# Configure API key
export ANTHROPIC_API_KEY=your_key_here

# Generate a diagram (using uvx - no installation needed)
uvx diag-agent create "C4 context diagram for API gateway"

# Or install and use directly
uv pip install diag-agent
diag-agent create "User authentication flow"
```

### MCP Server (for Claude Desktop)

```bash
# Install with MCP support
uv pip install diag-agent[mcp]

# Add to Claude Desktop config (~/.config/Claude/claude_desktop_config.json)
{
  "mcpServers": {
    "diag-agent": {
      "command": "python",
      "args": ["-m", "diag_agent.mcp.server"],
      "env": {
        "ANTHROPIC_API_KEY": "your_key_here",
        "KROKI_URL": "http://localhost:8000"
      }
    }
  }
}
```

Then in Claude Desktop:
> "Create a C4 context diagram for an e-commerce platform"

## Documentation

- **[User Guide](src/docs/user-guide.md)** - Comprehensive reference with all CLI commands, configuration, and MCP setup
- **[Tutorial](src/docs/tutorial.md)** - Hands-on examples for different diagram types and use cases
- **[Architecture](src/docs/arc42/arc42.adoc)** - Technical architecture documentation (arc42)

## CLI Commands

```bash
# Generate diagrams
diag-agent create "diagram description" [--type TYPE] [--output DIR] [--format FORMATS]

# Browse examples
diag-agent examples list [--type TYPE]
diag-agent examples show TYPE/NAME

# Manage local Kroki server
diag-agent kroki start|stop|status|logs
```

See [User Guide - CLI Commands](src/docs/user-guide.md#cli-commands) for detailed documentation.

## Supported Diagram Types

- **C4 Architecture**: `c4plantuml` - Context, Container, Component diagrams
- **UML**: `plantuml` - Sequence, Class, Component, Deployment, etc.
- **BPMN**: `bpmn` - Business processes and workflows
- **Mermaid**: `mermaid` - Flowcharts, Sequence, Gantt, etc.
- **Database**: `erd` - Entity Relationship Diagrams
- **And 20+ more** via [Kroki](https://kroki.io/#support)

See [Tutorial - Diagram Types](src/docs/tutorial.md) for practical examples.

## Installation

### Requirements

- Python 3.10+
- Docker (optional, for local Kroki server)
- LLM API key (Anthropic, OpenAI, or other)

### Install via uv (Recommended)

```bash
# Install uv package manager
pip install uv

# Install diag-agent
uv pip install diag-agent

# Install with MCP server support
uv pip install diag-agent[mcp]

# Development installation
uv pip install -e ".[dev,mcp]"
```

### No-Install Usage with uvx

```bash
# Run directly without installing
uvx diag-agent create "architecture diagram"
```

## Configuration

Configure via environment variables or `.env` file:

```bash
# LLM Configuration
export LLM_PROVIDER=anthropic        # anthropic, openai, azure, etc.
export LLM_MODEL=claude-sonnet-4     # Model name
export ANTHROPIC_API_KEY=your_key    # API key

# Kroki Configuration
export KROKI_URL=http://localhost:8000  # Local or remote Kroki server

# Agent Configuration
export MAX_ITERATIONS=10             # Max LLM iterations
export ENABLE_DESIGN_FEEDBACK=true   # Enable design feedback loop
```

See [User Guide - Configuration](src/docs/user-guide.md#configuration) for all options.

## Examples

### Generate Different Diagram Types

```bash
# C4 Context Diagram
diag-agent create "C4 context diagram for e-commerce platform" --type c4plantuml

# BPMN Process
diag-agent create "Order fulfillment process" --type bpmn

# Mermaid Flowchart
diag-agent create "CI/CD pipeline stages" --type mermaid

# Database Schema
diag-agent create "User management database schema" --type erd
```

### Use Local Kroki Server

```bash
# Start local Kroki (requires Docker)
diag-agent kroki start

# Generate diagram using local server
diag-agent create "architecture diagram"

# Stop Kroki when done
diag-agent kroki stop
```

### Custom Output

```bash
# Custom output directory and formats
diag-agent create "System architecture" \
  --type c4plantuml \
  --output ./docs/architecture \
  --format svg,pdf,source
```

See [Tutorial](src/docs/tutorial.md) for step-by-step examples.

## Development

```bash
# Install development dependencies
uv pip install -e ".[dev,mcp]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=diag_agent --cov-report=html

# Format code
black src tests
ruff check src tests

# Type checking
mypy src
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
