# diag-agent Tutorial

This hands-on tutorial walks you through using diag-agent to generate various types of diagrams, from simple flowcharts to complex architecture diagrams.

## Prerequisites

- diag-agent installed (see [User Guide - Installation](user-guide.md#installation))
- LLM API key configured (Anthropic, OpenAI, etc.)
- Optional: Docker installed for local Kroki server

---

## Tutorial 1: Your First Diagram

Let's start with a simple PlantUML sequence diagram.

### Step 1: Set Up Environment

```bash
# Set your API key
export ANTHROPIC_API_KEY=your_api_key_here

# Optional: Start local Kroki server
diag-agent kroki start
```

### Step 2: Generate Your First Diagram

```bash
diag-agent create "User authentication flow with login, verify password, and return JWT token"
```

### Step 3: View the Output

```bash
# Check the generated files
ls ./diagrams/

# Files created:
# - diagram.png       (PNG image)
# - diagram.svg       (SVG vector image)
# - diagram.puml      (PlantUML source code)
```

### Step 4: Understand the Output

The command prints metadata about the generation process:

```
✓ Diagram generated: ./diagrams/diagram.png
  Source: 234 characters
  Iterations: 2
  Time: 8.3s
  Stopped: success
```

**What happened:**
1. diag-agent sent your description to the LLM
2. LLM generated PlantUML source code
3. Code was validated via Kroki
4. Design feedback loop improved the diagram (if validation failed)
5. Final diagram rendered in PNG, SVG, and source formats

---

## Tutorial 2: C4 Architecture Diagram

C4 diagrams are ideal for documenting software architecture at different zoom levels.

### Step 1: Learn from Examples

```bash
# View available C4 examples
diag-agent examples list --type c4plantuml

# Study a context diagram example
diag-agent examples show c4plantuml/context-diagram
```

### Step 2: Generate a Context Diagram

```bash
diag-agent create \
  "C4 context diagram for an e-commerce platform with customer, admin, payment gateway, and inventory system" \
  --type c4plantuml \
  --output ./architecture-diagrams
```

### Step 3: Generate a Container Diagram

```bash
diag-agent create \
  "C4 container diagram for e-commerce platform showing web app, mobile app, API gateway, database, and message queue" \
  --type c4plantuml \
  --output ./architecture-diagrams
```

### Step 4: Generate a Component Diagram

```bash
diag-agent create \
  "C4 component diagram for the API gateway showing authentication, routing, rate limiting, and logging components" \
  --type c4plantuml \
  --output ./architecture-diagrams
```

### Result

You now have three diagrams documenting your architecture at different abstraction levels:
- **Context**: System and external actors
- **Container**: Major technical building blocks
- **Component**: Internal structure of containers

---

## Tutorial 3: BPMN Business Process

Let's model a business process using BPMN.

### Step 1: Explore BPMN Examples

```bash
diag-agent examples list --type bpmn
diag-agent examples show bpmn/simple-process
```

### Step 2: Generate an Order Fulfillment Process

```bash
diag-agent create \
  "BPMN process for order fulfillment: receive order, check inventory, if available ship order and notify customer, if not available backorder and notify supplier" \
  --type bpmn \
  --output ./processes \
  --format svg,pdf
```

### Step 3: Generate a Multi-Pool Collaboration

```bash
diag-agent create \
  "BPMN collaboration diagram with customer pool submitting request, support team pool processing ticket, and IT team pool resolving issue" \
  --type bpmn \
  --output ./processes
```

### Use Cases for BPMN

- **Business Processes**: Order fulfillment, customer onboarding
- **Workflows**: Approval workflows, escalation processes
- **Collaborations**: Cross-team processes with message flows

---

## Tutorial 4: Mermaid Flowcharts

Mermaid is great for quick, simple diagrams with clean syntax.

### Step 1: Generate a Deployment Pipeline

```bash
diag-agent create \
  "Flowchart for CI/CD pipeline: code commit, run tests, build Docker image, deploy to staging, run smoke tests, deploy to production" \
  --type mermaid \
  --output ./diagrams
```

### Step 2: Generate a Decision Tree

```bash
diag-agent create \
  "Decision flowchart for user access: check if logged in, if yes check permissions, if admin grant full access, if user grant read access, if guest show login page" \
  --type mermaid
```

### Step 3: Generate a Sequence Diagram

```bash
diag-agent create \
  "Mermaid sequence diagram for payment processing: user submits payment, frontend calls backend API, backend validates with payment gateway, gateway returns success, backend updates database, frontend shows confirmation" \
  --type mermaid
```

### Mermaid Advantages

- **Fast**: Quick syntax, fast rendering
- **Clean**: Modern, clean visual style
- **Versatile**: Flowcharts, sequence, Gantt, class diagrams

---

## Tutorial 5: Custom Output Formats

Control exactly what formats are generated.

### Generate Only SVG

```bash
diag-agent create \
  "System architecture diagram" \
  --format svg
```

### Generate All Formats

```bash
diag-agent create \
  "Database schema diagram" \
  --type erd \
  --format png,svg,pdf,source
```

### Custom Output Directory

```bash
# Organize by project
diag-agent create \
  "Microservices architecture" \
  --type c4plantuml \
  --output ./docs/architecture/microservices
```

---

## Tutorial 6: Using the MCP Server

Use diag-agent as an MCP server with Claude Desktop or other MCP clients.

### Step 1: Install MCP Support

```bash
uv pip install diag-agent[mcp]
```

### Step 2: Configure Claude Desktop

Edit your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
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

### Step 3: Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

### Step 4: Use in Claude Desktop

In a Claude conversation, ask:

> **You:** Create a C4 context diagram for a ride-sharing platform with riders, drivers, payment system, and mapping service.

Claude will automatically use the `create_diagram` MCP tool to generate the diagram.

### Step 5: Verify Output

```bash
# Check generated diagrams
ls ./diagrams/
```

### MCP Server Benefits

- **Seamless Integration**: Use diag-agent directly in Claude conversations
- **No CLI Switching**: Stay in Claude Desktop, no terminal needed
- **Conversational**: Refine diagrams through natural conversation

---

## Tutorial 7: Local vs. Remote Kroki

Choose between local privacy and remote convenience.

### Local Kroki (Recommended for Sensitive Data)

```bash
# Start local Kroki
diag-agent kroki start

# Verify status
diag-agent kroki status

# Generate diagram (uses local Kroki)
diag-agent create "Database schema"

# Stop when done
diag-agent kroki stop
```

**Advantages:**
- **Privacy**: Diagrams never leave your machine
- **Speed**: No internet latency
- **Offline**: Works without internet connection

**Disadvantages:**
- Requires Docker
- Uses local resources (CPU, RAM)

### Remote Kroki (Quick Start)

```bash
# Use public Kroki server
export KROKI_URL=https://kroki.io

# Generate diagram (uses remote Kroki)
diag-agent create "Architecture diagram"
```

**Advantages:**
- **No Docker**: No local installation needed
- **Zero Setup**: Works immediately

**Disadvantages:**
- **Privacy**: Diagram source sent to public server
- **Internet Required**: Needs active connection
- **Rate Limits**: Public server may have limits

---

## Tutorial 8: Troubleshooting Common Issues

### Issue: "Docker is not installed"

**Solution 1: Install Docker**
```bash
# macOS
brew install --cask docker

# Linux
sudo apt-get install docker.io
```

**Solution 2: Use Remote Kroki**
```bash
export KROKI_URL=https://kroki.io
diag-agent create "diagram"
```

---

### Issue: "Max iterations reached"

**Cause**: Description was too complex or ambiguous

**Solution 1: Simplify Description**
```bash
# Too complex
diag-agent create "detailed microservices architecture with 15 services, API gateway, service mesh, multiple databases, caching layer, message queue, monitoring, logging, and tracing"

# Better
diag-agent create "microservices architecture with API gateway, 3 core services, database, and message queue"
```

**Solution 2: Increase Max Iterations**
```bash
export MAX_ITERATIONS=20
diag-agent create "complex diagram"
```

---

### Issue: "Diagram quality is poor"

**Solution: Provide More Context**

```bash
# Vague
diag-agent create "user flow"

# Better
diag-agent create "user authentication flow: user enters credentials, system validates against database, generates JWT token, returns token to client"

# Best
diag-agent create "sequence diagram for user authentication: user submits login form with email and password, frontend sends POST to /auth/login, backend validates credentials against PostgreSQL, if valid generates JWT token with 1 hour expiry, returns token in JSON response, frontend stores token in localStorage"
```

---

### Issue: "LLM API errors"

**Check API Key:**
```bash
# Verify key is set
echo $ANTHROPIC_API_KEY

# Test with simple diagram
diag-agent create "simple flowchart with start and end"
```

**Check LLM Provider:**
```bash
# Switch providers if needed
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_openai_key
diag-agent create "diagram"
```

---

## Next Steps

### Explore More Diagram Types

```bash
# Try different types
diag-agent create "class diagram for user management" --type plantuml
diag-agent create "entity relationship diagram for blog database" --type erd
diag-agent create "state machine for order lifecycle" --type plantuml
```

### Automate Diagram Generation

Create a script to generate multiple diagrams:

```bash
#!/bin/bash
# generate-docs.sh

diag-agent create "C4 context diagram" --type c4plantuml --output ./docs/architecture
diag-agent create "C4 container diagram" --type c4plantuml --output ./docs/architecture
diag-agent create "deployment view" --type plantuml --output ./docs/architecture
diag-agent create "database schema" --type erd --output ./docs/architecture
```

### Integrate into CI/CD

```yaml
# .github/workflows/docs.yml
name: Generate Architecture Diagrams

on:
  push:
    branches: [main]

jobs:
  generate-diagrams:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install diag-agent
        run: pip install diag-agent
      - name: Generate diagrams
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          KROKI_URL: https://kroki.io
        run: |
          diag-agent create "C4 context" --type c4plantuml --output ./docs/diagrams
          diag-agent create "deployment view" --type plantuml --output ./docs/diagrams
      - name: Commit diagrams
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add docs/diagrams/
          git commit -m "docs: update architecture diagrams"
          git push
```

---

## Advanced Topics

### Custom Settings

Create a `.env` file for project-specific settings:

```bash
# .env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4
ANTHROPIC_API_KEY=sk-ant-xxxxx
KROKI_URL=http://localhost:8000
MAX_ITERATIONS=15
MAX_EXECUTION_TIME=600
ENABLE_DESIGN_FEEDBACK=true
```

### Multiple LLM Providers

Switch between providers easily:

```bash
# Use Claude for C4 diagrams (better at architecture)
export LLM_PROVIDER=anthropic
export LLM_MODEL=claude-sonnet-4
diag-agent create "C4 context diagram" --type c4plantuml

# Use GPT-4 for BPMN (better at business processes)
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4
diag-agent create "order fulfillment process" --type bpmn
```

### Batch Processing

Generate multiple diagrams from a file:

```bash
# diagrams.txt
C4 context diagram for API gateway|c4plantuml
User authentication flow|plantuml
Order fulfillment process|bpmn
Database schema for users|erd

# Process file
while IFS='|' read -r description type; do
  diag-agent create "$description" --type "$type" --output ./batch-diagrams
done < diagrams.txt
```

---

## Resources

- **[User Guide](user-guide.md)** - Comprehensive reference documentation
- **[Architecture Documentation](arc42/arc42.adoc)** - Technical architecture details
- **[Examples](../diag_agent/examples/)** - Example diagram templates
- **[Kroki Documentation](https://kroki.io/)** - Supported diagram types and syntax
- **[LiteLLM Documentation](https://docs.litellm.ai/)** - LLM provider configuration

---

## Feedback & Support

- Found a bug? [Open an issue](https://github.com/yourusername/diag-agent/issues)
- Have a question? Check the [User Guide](user-guide.md) or [open a discussion](https://github.com/yourusername/diag-agent/discussions)
- Want to contribute? See [CONTRIBUTING.md](../../CONTRIBUTING.md)

Happy diagramming! 🎨📊
