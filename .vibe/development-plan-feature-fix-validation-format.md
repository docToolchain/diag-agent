# Development Plan: diag-agent (feature/fix-validation-format branch)

*Generated on 2025-12-16 by Vibe Feature MCP*
*Workflow: [bugfix](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/bugfix)*

## Goal
Fix validation format issue that causes BPMN diagram generation to fail. The orchestrator uses hardcoded PNG format for validation, but BPMN only supports SVG output.

## Reproduce
### Bug Report
- **Symptom**: BPMN diagram generation fails with error "Unsupported output format: png for bpmn. Must be one of svg"
- **Command**: `uv run diag-agent create "Simple order processing workflow" --type bpmn --output ./test-bpmn`
- **Error Location**: orchestrator.py line 295-299
- **Root Cause**: Hardcoded `output_format="png"` in validation step
- **Impact**: All diagram types that don't support PNG fail (e.g., BPMN)

### Reproduction Steps
1. Run: `uv run diag-agent create "workflow" --type bpmn`
2. Observe: Validation fails with HTTP 400 error
3. Check log: Shows "Unsupported output format: png for bpmn"
4. Result: LLM wastes all iterations trying to "fix" the diagram (but diagram is correct)

### Environment
- OS: Linux
- Python: 3.12
- Kroki: Remote (kroki.io)
- Diagram Type: BPMN (only supports SVG)

### Tasks
- [x] Reproduce the bug with BPMN diagram
- [x] Verify error message and location
- [x] Confirm diagram source is actually valid
- [x] Document reproduction steps

### Completed
- [x] Created development plan file
- [x] Bug successfully reproduced

## Analyze
### Root Cause Analysis

**Problem Code** (orchestrator.py:303-307):
```python
png_bytes = self.kroki_client.render_diagram(
    diagram_source=diagram_source,
    diagram_type=diagram_type,
    output_format="png"  # <-- HARDCODED!
)
```

**Why This Fails**:
1. Validation step uses PNG format for all diagram types
2. Not all diagram types support PNG (e.g., BPMN only supports SVG)
3. Kroki returns HTTP 400 error for unsupported format combinations
4. Orchestrator interprets this as a syntax error in the diagram
5. LLM wastes all iterations trying to "fix" valid diagrams

**Supported Formats by Diagram Type**:
- PlantUML: png, svg, pdf
- C4-PlantUML: png, svg, pdf
- Mermaid: png, svg
- **BPMN: svg only** ❌ (causes bug)
- Most others: svg (universal format)

**Solution**:
Use SVG for validation instead of PNG, as SVG is supported by ALL diagram types.

### Tasks
- [x] Locate problematic code (orchestrator.py:303-307)
- [x] Verify Kroki format support for different diagram types
- [x] Identify root cause: hardcoded PNG format
- [x] Confirm SVG works for all diagram types
- [x] Document analysis findings

### Completed
- [x] Root cause identified: hardcoded PNG in validation
- [x] Solution confirmed: use SVG (universal format)

## Fix
### Implementation Plan

**Change Required**:
Replace hardcoded PNG format with SVG in validation step.

**Files to Modify**:
- `src/diag_agent/agent/orchestrator.py` (line 303-307)

**Change Details**:
```python
# BEFORE:
png_bytes = self.kroki_client.render_diagram(
    diagram_source=diagram_source,
    diagram_type=diagram_type,
    output_format="png"
)

# AFTER:
validation_bytes = self.kroki_client.render_diagram(
    diagram_source=diagram_source,
    diagram_type=diagram_type,
    output_format="svg"  # SVG is universally supported
)
```

**Impact Assessment**:
- ✅ Minimal change (single line)
- ✅ No API changes
- ✅ Backwards compatible (validation still works for all existing types)
- ✅ Fixes BPMN and other SVG-only diagram types
- ⚠️ Validation uses SVG instead of PNG (design feedback still uses PNG if enabled)

### Tasks
- [ ] Change output_format from "png" to "svg"
- [ ] Rename variable from png_bytes to validation_bytes for clarity
- [ ] Update design feedback to also use validation_bytes
- [ ] Run all tests to verify no regressions

### Completed
*None yet*

## Verify
### Tasks
- [ ] *To be added when this phase becomes active*

### Completed
*None yet*

## Finalize
### Tasks
- [ ] *To be added when this phase becomes active*

### Completed
*None yet*

## Key Decisions
*Important decisions will be documented here as they are made*

## Notes
*Additional context and observations*

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
