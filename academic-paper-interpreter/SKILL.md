---
name: academic-paper-interpreter
description: A high-fidelity, process-driven academic analysis tool. It utilizes a Multi-Agent Swarm and Visual-First strategy to deconstruct PDFs into structured, peer-review-grade Markdown reports.
metadata:
  requires:
    bins: []
    skills: ["superpowers:executing-plans", "superpowers:dispatching-parallel-agents", "pdf-figure-extractor"]
    mcp:
      - mineru
---

# Academic Paper Interpreter

## Skill Overview
This skill transforms raw PDFs into a structured "Logic Map" by leveraging the **mineru MCP** for layout fidelity and a phased **Sub-agent Swarm** for cognitive analysis. It prioritizes "Semantic DNA"—preserving complex equations, quantitative tables, and visual evidence chains.

## Execution Overview
The skill operates through a 6-phase pipeline, adapting analysis based on paper archetype. Each phase builds on the previous, culminating in comprehensive deliverables.

## Prerequisites
- **Input**: PDF file path for processing via mineru MCP
- **Tools**: Access to mineru MCP, semantic search, file reading, sub-agent dispatching
- **Dependencies**: Ensure mineru MCP is configured and available

## Core Dependencies
* **Parser**: `mineru MCP` (Native Markdown output via Model Context Protocol).
* **Fidelity**: Strict preservation of **LaTeX** ($inline$ and $$block$$) and **Markdown Tables**.
* **Agent Logic**: Orchestrator-Worker model for section-specific deep dives.

## The Deep Reading Pipeline

### Phase 0: Archetype Detection (Pre-flight)
Performs surface scan and archetype classification to adapt subsequent phases. [Details](phase-0-archetype-detection.md)

### Phase 1: Reconnaissance (Visual-First)
Establishes "What" and "Where" using a visual-first strategy. [Details](phase-1-reconnaissance.md)

### Phase 2: Structural Decomposition (Sub-agent Swarm)
High-granularity extraction using four quadrants for section analysis. [Details](phase-2-structural-decomposition.md)

### Phase 3: Technical Archeology (Deep Dive)
Deconstructs the technical stack and reference lineage. [Details](phase-3-technical-archeology.md)

### Phase 4: Consistency Audit (Peer Review)
Validates robustness and detects logical leaps. [Details](phase-4-consistency-audit.md)

### Phase 5: Conclusion Synthesis (The Verdict)
Distills final findings into actionable insights. [Details](phase-5-conclusion-synthesis.md)

## Tool Integration for Claude Code
- **PDF Processing**: Use **mineru MCP** for initial PDF parsing and extraction
- **Figure Extraction**: Use `pdf-figure-extractor` skill in Phase 1 to extract figures and embed them in FIGURE_LOGS.md
- **Content Analysis**: Employ `semantic_search` and `grep_search` for keyword and pattern detection
- **Parallel Processing**: Leverage `runSubagent` for phase 2 section analysis
- **File Operations**: Use `read_file` and `create_file` for input/output handling
- **Image Analysis**: Apply `view_image` for figure interpretation when available

## Step-by-Step Execution
1. **Initialize**: Load PDF content via mineru MCP
2. **Phase 0**: Classify archetype using surface scan
3. **Phase 1**: Extract visual insights and create summary cards
4. **Phase 2**: Dispatch sub-agents for quadrant-based section analysis
5. **Phase 3**: Map technical implementation and references
6. **Phase 4**: Perform cross-validation and identify challenges
7. **Phase 5**: Synthesize final recommendations

## Deliverables Summary
Generate a comprehensive Markdown report with the following structure:

| File | Primary Focus | Content Highlights |
| :--- | :--- | :--- |
| `SUMMARY_CARD.md` | Executive View | Core contribution, Quantitative data, Boundaries. |
| `FIGURE_LOGS.md` | Visual Logic | Caption analysis, Takeaways, Evidence linkage. |
| `SECTION_SUMMARIES.md` | Granular Detail | Four Quadrant summaries for every chapter. |
| `METHODOLOGY_CARD.md` | Replicability | Workflow mapping, Technical stack, LaTeX formulas. |
| `REFERENCE_MAP.md` | Lineage Mapping | "Circled" references based on archetype logic. |
| `REVIEW_CARD.md` | Critical Audit | Novelty vs. SOTA, Data integrity, Peer-review questions. |
| `CONCLUSION_CARD.md` | Final Verdict | Actionable insights, Final findings, Key quotes. |

## Execution Guardrails
1. **Symbolic Precision**: Never corrupt LaTeX syntax during summarization.
2. **Zero Hallucination**: If a parameter isn\'t in the MinerU data, mark it as **"Not Disclosed"**.
3. **Sub-agent Independence**: Each section agent must treat its section as a standalone "micro-project".
4. **Structure**: Maintain cross-reference anchoring between text claims and Figure IDs.
5. **Final Synthesis**: The Conclusion Card must be a distillation of all previous cards.

## Claude Code Best Practices
- Execute phases sequentially, passing context between them
- Use archetype classification to prioritize analysis focus
- Maintain evidence-based reasoning throughout
- Preserve all mathematical notation and technical details
- Generate outputs in specified Markdown format
- Cross-validate findings across phases for consistency

## Phase Execution as Tasks/Sub-agents

Each phase should be executed as an independent task or sub-agent, with clear inputs and outputs. Use `runSubagent` to invoke specialized agents for each phase.

### Phase 0 Task: Archetype Detection
**Input**: Raw PDF markdown content
**Reference**: [phase-0-archetype-detection.md](phase-0-archetype-detection.md)
**Agent Configuration**:
```
runSubagent({
  agentName: "academic-paper-interpreter-phase-0",
  description: "Classify paper archetype",
  prompt: "Classify the paper into one of 6 archetypes. See phase-0-archetype-detection.md for detailed instructions."
})
```
**Output**: `archetype.json` with classification and priority flags

### Phase 1 Task: Reconnaissance (Visual-First)
**Input**: PDF content + archetype classification from Phase 0
**Reference**: [phase-1-reconnaissance.md](phase-1-reconnaissance.md)
**Skills**: Uses `pdf-figure-extractor` for image extraction
**Agent Configuration**:
```
runSubagent({
  agentName: "academic-paper-interpreter-phase-1",
  description: "Extract visual insights and create summary with embedded figures",
  prompt: "Execute Phase 1 reconnaissance. See phase-1-reconnaissance.md for execution details."
})
```
**Output**: `SUMMARY_CARD.md`, `FIGURE_LOGS.md` (with extracted figure images), `figures/` directory

### Phase 2 Task: Structural Decomposition (Sub-agent Swarm)
**Input**: PDF content + archetype + Phase 1 outputs
**Reference**: [phase-2-structural-decomposition.md](phase-2-structural-decomposition.md)
**Agent Configuration**:
```
runSubagent({
  agentName: "academic-paper-interpreter-phase-2",
  description: "Decompose sections into four quadrants",
  prompt: "Execute Phase 2 structural decomposition with parallel sub-agents. See phase-2-structural-decomposition.md for execution details."
})
```
**Output**: `SECTION_SUMMARIES.md` with quadrant-based analysis

### Phase 3 Task: Technical Archeology
**Input**: PDF content + archetype + Phase 2 outputs
**Reference**: [phase-3-technical-archeology.md](phase-3-technical-archeology.md)
**Agent Configuration**:
```
runSubagent({
  agentName: "academic-paper-interpreter-phase-3",
  description: "Map technical stack and references",
  prompt: "Execute Phase 3 technical archeology. See phase-3-technical-archeology.md for execution details."
})
```
**Output**: `METHODOLOGY_CARD.md`, `REFERENCE_MAP.md`

### Phase 4 Task: Consistency Audit
**Input**: All previous outputs + PDF content
**Reference**: [phase-4-consistency-audit.md](phase-4-consistency-audit.md)
**Agent Configuration**:
```
runSubagent({
  agentName: "academic-paper-interpreter-phase-4",
  description: "Validate robustness and detect logical leaps",
  prompt: "Execute Phase 4 consistency audit. See phase-4-consistency-audit.md for execution details."
})
```
**Output**: `REVIEW_CARD.md`

### Phase 5 Task: Conclusion Synthesis
**Input**: All previous phase outputs
**Reference**: [phase-5-conclusion-synthesis.md](phase-5-conclusion-synthesis.md)
**Agent Configuration**:
```
runSubagent({
  agentName: "academic-paper-interpreter-phase-5",
  description: "Synthesize final recommendations",
  prompt: "Execute Phase 5 conclusion synthesis. See phase-5-conclusion-synthesis.md for execution details."
})
```
**Output**: `CONCLUSION_CARD.md`

## Sequential Task Orchestration
Execute phases in order with context passing:
1. Run Phase 0, capture archetype output
2. Pass archetype to Phase 1, capture summary outputs
3. Pass Phase 1 + archetype to Phase 2, capture section summaries
4. Pass Phase 2 + archetype to Phase 3, capture methodology/references
5. Pass all outputs to Phase 4, capture review findings
6. Pass all outputs to Phase 5, generate final verdict

## Parallel Sub-agent Execution (Phase 2)
For Phase 2, dispatch multiple sub-agents in parallel:
- One sub-agent per major section (Introduction, Methods, Results, Discussion, etc.)
- Each sub-agent analyzes its section through Fact-Method-Data-Claim quadrants
- Quadrant boost priorities set by archetype classification
- Collect and consolidate results into unified SECTION_SUMMARIES.md
