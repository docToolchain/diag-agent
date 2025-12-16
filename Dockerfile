# Multi-stage Dockerfile for diag-agent
# Supports both CLI and MCP Server modes

# ==============================================================================
# Stage 1: Builder
# ==============================================================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Copy source code
COPY src/ ./src/

# Install diag-agent with MCP support
RUN uv pip install --system --no-cache-dir .

# ==============================================================================
# Stage 2: Runtime
# ==============================================================================
FROM python:3.12-slim

# Metadata
LABEL org.opencontainers.image.title="diag-agent" \
      org.opencontainers.image.description="LLM Agent for creating software architecture diagrams" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.authors="diag-agent contributors" \
      org.opencontainers.image.source="https://github.com/yourusername/diag-agent"

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash diaguser

WORKDIR /app

# Copy application from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/diag-agent /usr/local/bin/diag-agent
COPY --from=builder /build/src /app/src

# Create output directory with correct permissions
RUN mkdir -p /diagrams && chown -R diaguser:diaguser /diagrams /app

# Switch to non-root user
USER diaguser

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OUTPUT_DIR=/diagrams

# Volume for generated diagrams
VOLUME ["/diagrams"]

# Default: Run CLI with help
# Override with docker run arguments or use MCP mode
ENTRYPOINT ["diag-agent"]
CMD ["--help"]

# ==============================================================================
# Usage Examples
# ==============================================================================
# 
# CLI Mode:
#   docker run --rm \
#     -e ANTHROPIC_API_KEY=your_key \
#     -e KROKI_URL=https://kroki.io \
#     -v $(pwd)/diagrams:/diagrams \
#     diag-agent create "architecture diagram"
#
# MCP Server Mode:
#   docker run --rm \
#     -e ANTHROPIC_API_KEY=your_key \
#     -e KROKI_URL=http://host.docker.internal:8000 \
#     -p 8080:8080 \
#     diag-agent python -m diag_agent.mcp.server
#
# Interactive Mode:
#   docker run --rm -it \
#     -e ANTHROPIC_API_KEY=your_key \
#     -v $(pwd)/diagrams:/diagrams \
#     diag-agent bash
