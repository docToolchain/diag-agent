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
# Install uv (if not already installed)
pip install uv

# Install diag-agent
uv pip install diag-agent

# Or use uvx for one-off executions (no installation needed)
uvx diag-agent --help
```

## Quick Start

```bash
# Configure API key
export ANTHROPIC_API_KEY=your_key_here

# Generate a diagram (using uvx - no installation needed)
uvx diag-agent create "C4 context diagram for API gateway"

# Or if you installed with 'uv pip install'
diag-agent create "C4 context diagram for API gateway"
```

## Usage Examples

| Use Case | Command |
|----------|---------|
| Quick test (no install) | `uvx diag-agent --help` |
| One-off diagram generation | `uvx diag-agent create "architecture diagram"` |
| Batch processing | `uvx diag-agent create-batch --input requirements.txt` |
| Development install | `uv pip install -e ".[dev]"` |
| Production install | `uv pip install diag-agent` |

## Project Structure

See [Architecture Documentation](src/docs/arc42/arc42.adoc) for detailed information.

## Development

```bash
# Install dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests
ruff check src tests
```

## License

MIT
