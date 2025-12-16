# diag-agent User Guide

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [CLI Commands](#cli-commands)
4. [MCP Server](#mcp-server)
5. [Docker Deployment](#docker-deployment)
6. [Diagram Types](#diagram-types)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Requirements

- **Python**: 3.10 or higher
- **Docker**: Optional, required only for local Kroki server
- **LLM API Key**: Anthropic (Claude), OpenAI, or other LiteLLM-supported provider

### Installation Methods

#### Using uv (Recommended)

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

#### Using uvx (No Installation)

For one-off usage without installation:

```bash
# Run directly without installing
uvx diag-agent create "User authentication flow"

# Check version
uvx diag-agent --version
```

### Verify Installation

```bash
diag-agent --version
diag-agent --help
```

---

## Configuration

### Environment Variables

diag-agent uses environment variables for configuration. Create a `.env` file or export them in your shell.

#### LLM Configuration

```bash
# LLM Provider (default: anthropic)
export LLM_PROVIDER=anthropic

# LLM Model (default: claude-sonnet-4)
export LLM_MODEL=claude-sonnet-4

# Anthropic API Key
export ANTHROPIC_API_KEY=your_api_key_here

# Alternative: OpenAI
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4
export OPENAI_API_KEY=your_openai_key_here
```

**Supported LLM Providers** (via LiteLLM):
- `anthropic` - Claude models
- `openai` - GPT models
- `azure` - Azure OpenAI
- `vertex_ai` - Google Vertex AI
- `bedrock` - AWS Bedrock
- And 100+ more via [LiteLLM](https://docs.litellm.ai/docs/providers)

#### Kroki Configuration

```bash
# Kroki Server URL (default: http://localhost:8000)
export KROKI_URL=http://localhost:8000

# Alternative: Use public Kroki server (not recommended for sensitive data)
export KROKI_URL=https://kroki.io
```

#### Agent Configuration

```bash
# Maximum LLM iterations for diagram generation (default: 10)
export MAX_ITERATIONS=10

# Maximum execution time in seconds (default: 300)
export MAX_EXECUTION_TIME=300

# Enable design feedback loop (default: true)
export ENABLE_DESIGN_FEEDBACK=true
```

### Configuration File

Create a `.env` file in your project root:

```bash
# .env example
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4
ANTHROPIC_API_KEY=sk-ant-xxxxx
KROKI_URL=http://localhost:8000
MAX_ITERATIONS=10
ENABLE_DESIGN_FEEDBACK=true
```

---

## CLI Commands

### `diag-agent create`

Generate a diagram from natural language description.

#### Syntax

```bash
diag-agent create DESCRIPTION [OPTIONS]
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--type DIAGRAM_TYPE` | Diagram type (plantuml, c4plantuml, mermaid, etc.) | `plantuml` |
| `--output OUTPUT_DIR` | Output directory for generated diagrams | `./diagrams` |
| `--format OUTPUT_FORMATS` | Comma-separated output formats (png, svg, pdf, source) | `png,svg,source` |

#### Examples

```bash
# Basic diagram generation
diag-agent create "User authentication flow"

# C4 Context Diagram
diag-agent create "C4 context diagram for API gateway" --type c4plantuml

# BPMN Process with custom output
diag-agent create "Order fulfillment process" \
  --type bpmn \
  --output ./bpmn-diagrams \
  --format svg,pdf

# Mermaid flowchart
diag-agent create "Deployment pipeline stages" --type mermaid
```

#### Output

The command generates:
- **Diagram files** in specified formats (PNG, SVG, PDF)
- **Source code** file (.puml, .bpmn, .mmd, etc.)
- **Console output** with metadata:
  - Output path
  - Source code length
  - Iterations used
  - Execution time
  - Stop reason (success, max_iterations, max_time)

---

### `diag-agent examples`

Manage and view example diagrams for different diagram types.

#### List Examples

```bash
# List all examples
diag-agent examples list

# Filter by diagram type
diag-agent examples list --type c4plantuml
```

#### Show Example Source

```bash
# Show example source code
diag-agent examples show c4plantuml/context-diagram

# Show BPMN example
diag-agent examples show bpmn/simple-process
```

#### Available Examples

**C4-PlantUML:**
- `c4plantuml/context-diagram` - System context diagram
- `c4plantuml/container-diagram` - Container diagram
- `c4plantuml/component-diagram` - Component diagram

**BPMN:**
- `bpmn/simple-process` - Basic BPMN process
- `bpmn/collaboration` - Multi-pool collaboration diagram

---

### `diag-agent kroki`

Manage local Kroki Docker container for diagram rendering.

#### Start Kroki Server

```bash
diag-agent kroki start
```

Launches a Docker container with Kroki server at `http://localhost:8000`.

#### Stop Kroki Server

```bash
diag-agent kroki stop
```

Stops and removes the Kroki container.

#### Check Status

```bash
diag-agent kroki status
```

Shows container running state and health status.

#### View Logs

```bash
# Show logs
diag-agent kroki logs

# Follow logs (live streaming)
diag-agent kroki logs --follow
```

---

## MCP Server

diag-agent can run as a **Model Context Protocol (MCP) server**, exposing diagram generation capabilities to LLM applications like Claude Desktop.

### What is MCP?

The Model Context Protocol enables LLM applications to connect to external tools and data sources. diag-agent's MCP server exposes a `create_diagram` tool that other LLMs can use.

### Setup for Claude Desktop

1. **Install diag-agent with MCP support:**

```bash
uv pip install diag-agent[mcp]
```

2. **Configure Claude Desktop:**

Edit your Claude Desktop configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the MCP server configuration:

```json
{
  "mcpServers": {
    "diag-agent": {
      "command": "python",
      "args": [
        "-m",
        "diag_agent.mcp.server"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "your_api_key_here",
        "KROKI_URL": "http://localhost:8000"
      }
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Use the tool:**

In Claude Desktop, you can now ask:
> "Create a C4 context diagram for an e-commerce system"

Claude will use the `create_diagram` MCP tool to generate the diagram.

### MCP Tool: `create_diagram`

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `description` | string | Natural language description of the diagram | (required) |
| `diagram_type` | string | Type of diagram (plantuml, c4plantuml, mermaid, etc.) | `plantuml` |
| `output_dir` | string | Output directory for generated diagrams | `./diagrams` |
| `output_formats` | string | Comma-separated output formats (png, svg, pdf, source) | `png,svg,source` |

#### Return Value

The tool returns a JSON object with:
- `diagram_source` - Generated diagram source code
- `output_path` - Path to primary output file
- `iterations_used` - Number of LLM iterations performed
- `elapsed_seconds` - Total execution time
- `stopped_reason` - Why iteration stopped (success, max_iterations, max_time)

#### Example Usage in MCP Client

```python
# Using FastMCP client
from fastmcp import Client

async with Client("diag-agent") as client:
    result = await client.call_tool(
        "create_diagram",
        description="User login flow",
        diagram_type="plantuml",
        output_formats="svg,png"
    )
    print(f"Diagram created: {result['output_path']}")
```

---

## Docker Deployment

diag-agent provides Docker images for containerized deployment with support for both CLI and MCP Server modes.

### Docker Image

#### Pull Pre-built Image

```bash
# Pull from Docker Hub (when published)
docker pull yourusername/diag-agent:latest
```

#### Build Locally

```bash
# Build from source
docker build -t diag-agent .

# Build with specific tag
docker build -t diag-agent:0.1.0 .
```

### Docker CLI Usage

#### Basic Usage

```bash
# Run CLI command
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key \
  -e KROKI_URL=https://kroki.io \
  -v $(pwd)/diagrams:/diagrams \
  diag-agent create "User authentication flow"
```

#### With Options

```bash
# Generate C4 diagram with custom output
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key \
  -e KROKI_URL=https://kroki.io \
  -v $(pwd)/diagrams:/diagrams \
  diag-agent create "C4 context diagram for API gateway" \
    --type c4plantuml \
    --format svg,pdf
```

#### Using Local Kroki

```bash
# Start local Kroki first
docker run -d --name kroki -p 8000:8000 yuzutech/kroki

# Run diag-agent using local Kroki (use host.docker.internal on Mac/Windows)
docker run --rm \
  -e ANTHROPIC_API_KEY=your_key \
  -e KROKI_URL=http://host.docker.internal:8000 \
  -v $(pwd)/diagrams:/diagrams \
  diag-agent create "architecture diagram"

# On Linux, use host network mode
docker run --rm --network host \
  -e ANTHROPIC_API_KEY=your_key \
  -e KROKI_URL=http://localhost:8000 \
  -v $(pwd)/diagrams:/diagrams \
  diag-agent create "architecture diagram"
```

#### Interactive Shell

```bash
# Open interactive shell in container
docker run --rm -it \
  -e ANTHROPIC_API_KEY=your_key \
  -v $(pwd)/diagrams:/diagrams \
  diag-agent bash

# Inside container, run commands
diag-agent create "diagram"
diag-agent examples list
```

---

### Docker Compose

Docker Compose provides the easiest way to run diag-agent with Kroki.

#### Setup

1. **Create `.env` file:**

```bash
# Copy example configuration
cp .env.example .env

# Edit with your values
nano .env
```

Example `.env`:
```bash
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4
ANTHROPIC_API_KEY=sk-ant-xxxxx
MAX_ITERATIONS=10
ENABLE_DESIGN_FEEDBACK=true
```

2. **Choose deployment mode:**

#### Mode 1: Kroki Only (for local CLI)

Start only the Kroki server for use with local CLI:

```bash
# Start Kroki server
docker-compose up -d kroki

# Check status
docker-compose ps

# Use local CLI with Docker Kroki
export KROKI_URL=http://localhost:8000
diag-agent create "architecture diagram"

# Stop
docker-compose down
```

#### Mode 2: CLI via Docker Compose

Run CLI commands through Docker Compose:

```bash
# Run one-off CLI command
docker-compose run --rm diag-agent-cli create "User authentication flow"

# With options
docker-compose run --rm diag-agent-cli create \
  "C4 context diagram" \
  --type c4plantuml \
  --output /diagrams

# Stop Kroki after use
docker-compose down
```

#### Mode 3: MCP Server

Run diag-agent as an MCP server:

```bash
# Start MCP server with Kroki
docker-compose --profile mcp up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f diag-agent-mcp

# MCP server is now available at localhost:8080
# Configure your MCP client to connect to this endpoint

# Stop all services
docker-compose down
```

#### Common Commands

```bash
# View all logs
docker-compose logs -f

# View Kroki logs only
docker-compose logs -f kroki

# Restart service
docker-compose restart diag-agent-mcp

# Remove all containers and volumes
docker-compose down -v

# Rebuild after code changes
docker-compose build
docker-compose up -d
```

---

### Docker Environment Variables

All environment variables from [Configuration](#configuration) are supported:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (anthropic, openai, etc.) | `anthropic` |
| `LLM_MODEL` | Model name | `claude-sonnet-4` |
| `ANTHROPIC_API_KEY` | Anthropic API key | (required) |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `KROKI_URL` | Kroki server URL | `http://localhost:8000` |
| `MAX_ITERATIONS` | Max LLM iterations | `10` |
| `MAX_EXECUTION_TIME` | Max execution time (seconds) | `300` |
| `ENABLE_DESIGN_FEEDBACK` | Enable design feedback | `true` |
| `OUTPUT_DIR` | Output directory | `/diagrams` |

---

### Docker Volumes

Mount volumes to persist generated diagrams:

```bash
# Mount current directory
-v $(pwd)/diagrams:/diagrams

# Mount absolute path
-v /home/user/my-diagrams:/diagrams

# Named volume (persists across containers)
docker volume create diag-diagrams
-v diag-diagrams:/diagrams
```

---

### Docker Security

The Docker image follows security best practices:

- **Non-root user**: Runs as `diaguser` (UID 1000)
- **Minimal base**: Uses `python:3.12-slim` (< 200MB)
- **Multi-stage build**: Separates build and runtime dependencies
- **No secrets in image**: All credentials via environment variables
- **Read-only filesystem**: Application files are read-only

#### Security Recommendations

1. **Never commit `.env` file** with API keys
2. **Use secrets management** in production:
   ```bash
   # Docker Swarm secrets
   docker secret create anthropic_key your_key.txt
   
   # Kubernetes secrets
   kubectl create secret generic diag-agent-secrets \
     --from-literal=anthropic-api-key=your_key
   ```

3. **Scan for vulnerabilities**:
   ```bash
   docker scan diag-agent
   ```

4. **Use specific tags** instead of `latest` in production

---

### Production Deployment

#### Docker Swarm

```yaml
# stack.yml
version: '3.8'

services:
  diag-agent-mcp:
    image: diag-agent:0.1.0
    command: ["python", "-m", "diag_agent.mcp.server"]
    secrets:
      - anthropic_api_key
    environment:
      ANTHROPIC_API_KEY_FILE: /run/secrets/anthropic_api_key
      KROKI_URL: http://kroki:8000
    ports:
      - "8080:8080"
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure

secrets:
  anthropic_api_key:
    external: true
```

Deploy:
```bash
docker stack deploy -c stack.yml diag-agent
```

#### Kubernetes

```yaml
# deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: diag-agent-mcp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: diag-agent-mcp
  template:
    metadata:
      labels:
        app: diag-agent-mcp
    spec:
      containers:
      - name: diag-agent
        image: diag-agent:0.1.0
        command: ["python", "-m", "diag_agent.mcp.server"]
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: diag-agent-secrets
              key: anthropic-api-key
        - name: KROKI_URL
          value: "http://kroki-service:8000"
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: diagrams
          mountPath: /diagrams
      volumes:
      - name: diagrams
        persistentVolumeClaim:
          claimName: diag-agent-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: diag-agent-mcp-service
spec:
  selector:
    app: diag-agent-mcp
  ports:
  - port: 8080
    targetPort: 8080
  type: LoadBalancer
```

Deploy:
```bash
kubectl apply -f deployment.yml
```

---

## Diagram Types

### Supported Diagram Types

diag-agent supports all diagram types that Kroki supports:

| Type | Description | Example Use Cases |
|------|-------------|-------------------|
| `plantuml` | General-purpose UML diagrams | Sequence, class, component diagrams |
| `c4plantuml` | C4 architecture diagrams | System context, containers, components |
| `bpmn` | Business Process Model and Notation | Business processes, workflows |
| `mermaid` | Lightweight text-based diagrams | Flowcharts, sequence, Gantt charts |
| `structurizr` | Structurizr DSL diagrams | Software architecture |
| `graphviz` | DOT language graphs | Directed graphs, hierarchies |
| `ditaa` | ASCII art to diagrams | Quick sketches |
| `erd` | Entity Relationship Diagrams | Database schemas |
| `excalidraw` | Hand-drawn style diagrams | Sketchy, informal diagrams |

For the full list, see [Kroki Documentation](https://kroki.io/#support).

### Choosing a Diagram Type

**For Software Architecture:**
- Use `c4plantuml` for layered architecture diagrams
- Use `plantuml` for detailed UML diagrams

**For Business Processes:**
- Use `bpmn` for formal business processes

**For Quick Visualizations:**
- Use `mermaid` for simple flowcharts and sequences
- Use `ditaa` for ASCII-art style diagrams

**For Databases:**
- Use `erd` for entity relationship diagrams

---

## Troubleshooting

### Common Issues

#### 1. `ModuleNotFoundError: No module named 'diag_agent'`

**Cause**: diag-agent not installed or not in PATH

**Solution**:
```bash
# Install diag-agent
uv pip install diag-agent

# Or use uvx for one-off execution
uvx diag-agent create "diagram description"
```

---

#### 2. `Error: Docker is not installed`

**Cause**: Docker not available when running `diag-agent kroki start`

**Solution**:
```bash
# Install Docker (macOS/Linux)
# Visit: https://docs.docker.com/get-docker/

# Alternative: Use public Kroki server
export KROKI_URL=https://kroki.io
diag-agent create "diagram"
```

---

#### 3. `Error: Kroki server unavailable`

**Cause**: Kroki server not running or wrong URL

**Solution**:
```bash
# Check if local Kroki is running
diag-agent kroki status

# Start local Kroki
diag-agent kroki start

# Or use public server
export KROKI_URL=https://kroki.io
```

---

#### 4. `AuthenticationError: Invalid API key`

**Cause**: Missing or invalid LLM API key

**Solution**:
```bash
# Set API key
export ANTHROPIC_API_KEY=your_key_here

# Or create .env file
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

---

#### 5. `Error: Max iterations reached`

**Cause**: Diagram generation exceeded maximum iterations

**Solution**:
```bash
# Increase max iterations
export MAX_ITERATIONS=20
diag-agent create "complex diagram"

# Or simplify the description
diag-agent create "simple user login flow"
```

---

#### 6. MCP Server: `fastmcp not found`

**Cause**: FastMCP not installed

**Solution**:
```bash
# Install diag-agent with MCP support
uv pip install diag-agent[mcp]
```

---

### Enable Debug Logging

For detailed troubleshooting, enable debug logging:

```bash
export LOG_LEVEL=DEBUG
diag-agent create "diagram"
```

---

### Getting Help

- **Documentation**: [User Guide](user-guide.md) | [Tutorial](tutorial.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/diag-agent/issues)
- **Examples**: Run `diag-agent examples list` to see available examples

---

## Next Steps

- Follow the [Tutorial](tutorial.md) for hands-on examples
- Explore [Examples](../diag_agent/examples/) for diagram templates
- Read [Architecture Documentation](arc42/arc42.adoc) for technical details
