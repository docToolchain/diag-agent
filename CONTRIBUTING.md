# Contributing to diag-agent

Thank you for your interest in contributing to diag-agent! This guide will help you get started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Contributing Diagram Examples](#contributing-diagram-examples)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Code Contributions](#code-contributions)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)

## Code of Conduct

This project adheres to a code of conduct that promotes a welcoming and inclusive environment. Be respectful, constructive, and collaborative in all interactions.

## How Can I Contribute?

### Contributing Diagram Examples

**Diagram examples are one of the most valuable contributions!** They help the LLM generate better diagrams by providing reference structures.

#### Example Directory Structure

```
src/diag_agent/examples/
├── bpmn/
│   ├── collaboration.bpmn
│   └── simple-process.bpmn
├── c4plantuml/
│   ├── context-diagram.puml
│   ├── container-diagram.puml
│   └── component-diagram.puml
└── <diagram-type>/
    └── <example-name>.<extension>
```

#### Adding a New Example

1. **Choose the right diagram type directory** (e.g., `bpmn`, `c4plantuml`, `mermaid`, `plantuml`)
2. **Name your example file descriptively** using kebab-case:
   - Good: `user-authentication-flow.puml`, `order-fulfillment.bpmn`
   - Bad: `example1.puml`, `test.bpmn`

3. **Ensure your example is valid**:
   - Test it with the appropriate renderer (Kroki, PlantUML, etc.)
   - Include all required elements for the diagram type
   - For BPMN: Include complete Diagram Interchange (BPMNShape, BPMNEdge) for visual layout

4. **Keep examples focused and clear**:
   - Examples should demonstrate one concept or pattern
   - Avoid overly complex examples (prefer multiple simple examples)
   - Include meaningful names for elements (not "Task1", "Task2")
   - Add comments if the structure needs explanation

5. **Consider example size**:
   - Small examples: 50-200 lines (preferred for simple concepts)
   - Medium examples: 200-500 lines (for more complex patterns)
   - Large examples: 500+ lines (only if necessary, e.g., complete BPMN processes)

#### Example Quality Checklist

- [ ] File is in the correct `src/diag_agent/examples/<type>/` directory
- [ ] Filename uses kebab-case and is descriptive
- [ ] Example renders correctly with Kroki/the target renderer
- [ ] Example demonstrates a clear use case or pattern
- [ ] Element names are meaningful and self-explanatory
- [ ] File size is appropriate (prefer smaller, focused examples)
- [ ] For BPMN: Includes complete Diagram Interchange
- [ ] For PlantUML/C4: Uses clear, standard syntax

#### Testing Your Example

```bash
# Install the project
uv sync

# List examples to verify your example appears
uv run diag-agent examples list --type <diagram-type>

# View your example source
uv run diag-agent examples show <diagram-type>/<example-name>

# Generate a diagram using your example as reference
uv run diag-agent create "Description similar to your example" \
  --type <diagram-type> \
  --output ./test-output
```

#### Example Contribution Workflow

```bash
# 1. Create feature branch
git checkout main
git pull
git checkout -b feature/add-<diagram-type>-example

# 2. Add your example file
# Place in src/diag_agent/examples/<type>/<name>.<ext>

# 3. Test the example
uv run diag-agent examples list --type <diagram-type>
uv run diag-agent examples show <diagram-type>/<name>

# 4. Run tests
uv run pytest

# 5. Commit and push
git add src/diag_agent/examples/<type>/<name>.<ext>
git commit -m "feat: add <name> example for <diagram-type>

Add example demonstrating <use case/pattern>.

- <Key feature 1>
- <Key feature 2>
"
git push origin feature/add-<diagram-type>-example

# 6. Create Pull Request on GitHub
```

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** (if available)
3. **Include**:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment details (OS, Python version, LLM provider)
   - Relevant logs (check `diagrams/generation.log`)

### Suggesting Features

1. **Check existing issues and discussions**
2. **Describe the use case** clearly
3. **Explain the benefit** to users
4. **Consider alternatives** you've explored

### Code Contributions

See [Development Setup](#development-setup) and [Code Standards](#code-standards) below.

## Development Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (optional, for local Kroki server)
- Git

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/docToolchain/diag-agent.git
cd diag-agent

# Install dependencies
uv sync

# Set up environment variables
export ANTHROPIC_API_KEY="your-api-key"  # or other LLM provider

# Run tests
uv run pytest

# Run the CLI
uv run diag-agent --help
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/diag_agent --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_orchestrator.py

# Run integration tests only
uv run pytest tests/integration/
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch** from `main`:
   ```bash
   git checkout main
   git pull
   git checkout -b feature/your-feature-name
   ```

2. **Make focused commits**:
   - One logical change per commit
   - Write clear commit messages (see [Commit Message Format](#commit-message-format))

3. **Ensure all tests pass**:
   ```bash
   uv run pytest
   ```

4. **Update documentation** if needed:
   - Update README.md for user-facing changes
   - Update docstrings for API changes
   - Add/update examples if relevant

### Commit Message Format

Follow conventional commits style:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `chore`: Maintenance tasks

**Examples:**
```
feat: add mermaid gantt chart example

Add example demonstrating project timeline visualization using
Mermaid gantt charts.
```

```
fix: improve BPMN collaboration generation

- Add missing collaboration.bpmn example
- Implement dual-example system for better guidance
- Update tests to verify example loading

Fixes #4
```

### PR Submission

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**:
   - Use a clear, descriptive title
   - Describe what the PR does and why
   - Reference related issues (e.g., "Fixes #123")
   - Include screenshots/examples for UI/output changes

3. **Wait for review**:
   - Respond to feedback constructively
   - Make requested changes in new commits
   - Re-request review when ready

4. **After approval**:
   - Maintainers will merge your PR
   - Delete your feature branch after merge

## Code Standards

### Python Style

- **PEP 8** compliance (with line length 100)
- **Type hints** for function signatures
- **Docstrings** for public functions/classes (Google style)
- **Black** for code formatting (configured in `pyproject.toml`)

### Code Organization

```python
# Good: Clear, typed, documented
def generate_diagram(
    description: str,
    diagram_type: str,
    max_iterations: int = 5
) -> dict:
    """Generate a diagram from a text description.
    
    Args:
        description: Natural language description of the diagram
        diagram_type: Type of diagram (e.g., 'plantuml', 'bpmn')
        max_iterations: Maximum refinement attempts
        
    Returns:
        dict: Result containing source, metadata, and file paths
        
    Raises:
        ValueError: If diagram_type is not supported
    """
    # Implementation...
```

### Testing Requirements

- **Unit tests** for new functions/classes
- **Integration tests** for workflows
- **Maintain or improve** code coverage (currently 85%)
- **Test edge cases** and error conditions

### File Organization

- Keep files under 500 lines
- One class per file (generally)
- Group related functionality in modules
- Use clear, descriptive names

## Questions?

- **Documentation**: Check [User Guide](src/docs/user-guide.md) and [Tutorial](src/docs/tutorial.md)
- **Issues**: [Open an issue](https://github.com/docToolchain/diag-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/docToolchain/diag-agent/discussions)

Thank you for contributing! 🎉
