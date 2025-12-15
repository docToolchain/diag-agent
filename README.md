# diag-agent

An LLM Agent for creating software architecture diagrams with autonomous syntax validation and design feedback.

## Features

- 🤖 **Autonomous diagram generation** with syntax validation and design feedback loop
- 🎨 **Multi-format support** via Kroki integration (PlantUML, C4, BPMN, Mermaid, etc.)
- 🚀 **Flexible deployment**: CLI tool, MCP server (local/remote), or Docker container
- 🔒 **Privacy-first**: Local-first approach with optional remote rendering
- 🔌 **LLM-agnostic**: Works with any LLM via LiteLLM abstraction
- ⚡ **Context-efficient**: Minimal token consumption through help system and URL references

## Installation

```bash
pip install diag-agent
```

## Quick Start

```bash
# Configure API key
export ANTHROPIC_API_KEY=your_key_here

# Generate a diagram
diag-agent create "C4 context diagram for API gateway"
```

## Project Structure

See [Architecture Documentation](src/docs/arc42/arc42.adoc) for detailed information.

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests
ruff check src tests
```

## License

MIT
