---
name: academic-paper-interpreter
description: "Analyze academic papers at your chosen depth: get a quick archetype classification, a structured summary with figure analysis, an in-depth methodology and reference audit, or a full peer-review-grade assessment with quality-verified conclusions. Helps you understand what a paper says, whether its claims hold up, and whether it's worth adopting or replicating."
metadata:
  language: en
  requires:
    bins: []
    skills:
      - "superpowers:executing-plans"
      - "superpowers:dispatching-parallel-agents"
      - "pdf-figure-extractor"
    mcp:
      - mineru
---

# Academic Paper Interpreter — SSL Architecture

## Scheduling Layer

### Skill Identity
- **skill_id**: academic-paper-interpreter
- **skill_goal**: Transform academic papers into structured, peer-review-grade analysis reports
- **intent_signature**: User provides path to mineru-processed PDF markdown → skill produces structured analysis at chosen depth in configured language (default: en, supports: zh)

### Architecture Overview

This skill uses a **three-layer SSL representation** (Scheduling / Structural / Logical):

```
┌─────────────────────────────────────────────┐
│ Scheduling Layer (SKILL.md)                  │
│ - Entry routing & intent matching            │
│ - Archetype definitions                      │
│ - Execution guardrails                       │
├─────────────────────────────────────────────┤
│ Structural Layer (scenes/ + _scene-graph.md)  │
│ - Scene DAG with depth levels L0-L3          │
│ - Auto/manual transition gates               │
│ - Parallel execution at L2 and L3            │
├─────────────────────────────────────────────┤
│ Logical Layer (_logic/)                       │
│ - Closed vocabulary act types (9 types)      │
│ - Resource scope definitions (4 scopes)      │
└─────────────────────────────────────────────┘
```

### Language Configuration
All output files (SUMMARY_CARD.md, FIGURE_LOGS.md, SECTION_SUMMARIES.md, METHODOLOGY_CARD.md, REFERENCE_MAP.md, REVIEW_CARD.md, AUDIT_REPORT.md, CONCLUSION_CARD.md) MUST be written in the configured language.

| Field | Value |
|-------|-------|
| `language` | `en` (English, default) or `zh` (Chinese, 中文) |
| Propagation | Language setting is passed to EVERY scene agent and sub-agent |
| Scope | All output files — the analysis text, tables, headings, and summaries |
| Source material | The mineru markdown stays in its original language; only the analysis/report output is affected |
| Adding languages | Extend by adding new entries to this table; each scene's directive enforces the active language |

**Usage**: User specifies language when invoking (e.g., "interpret this paper in Chinese" or set `language: zh`). Default is English (`en`).

### Depth Levels

| Level | Name | Scenes | Outputs |
|-------|------|--------|---------|
| L0 | Surface Scan | PREPARE | archetype.json |
| L1 | Core Understanding | ACQUIRE → REASON (section) | SUMMARY_CARD.md, FIGURE_LOGS.md, SECTION_SUMMARIES.md |
| L2 | Deep Analysis | REASON (tech-stack, ref-lineage) + VERIFY (evidence-check) | METHODOLOGY_CARD.md, REFERENCE_MAP.md |
| L3 | Audit + Synthesis | VERIFY (consistency-audit, output-audit) + FINALIZE (conclusion) | REVIEW_CARD.md, AUDIT_REPORT.md, CONCLUSION_CARD.md |

### Scene Graph

```
L0: PREPARE ──auto──► L1: ACQUIRE ──auto──► REASON (section-analysis)
                                                    │
                                              manual gate ◄── user reviews L1 outputs
                                                    │
                              ┌─────────────────────┼─────────────────────┐
                              ▼                     ▼                     ▼
L2:                    REASON (tech-stack)   REASON (ref-lineage)   VERIFY (evidence-check)
                              │                     │                     │
                              └─────────────────────┼─────────────────────┘
                                                      ▼
                                                manual gate ◄── user reviews L2 findings
                                                      │
                              ┌─────────────────────────┴─────────────────────────┐
                              ▼                                                   ▼
L3:         Primary Track: VERIFY (consistency-audit) ──► FINALIZE (conclusion)
                              Meta Track: VERIFY (output-audit) ──────────────────┘
```

### Transition Rules
- **Auto**: L0→L1, L1 internal, L2 internal, L3 internal
- **Manual gates**: L1→L2 entry, L2→L3 entry
  - At each gate: show user a summary of current level's findings
  - Offer: proceed all / select specific scenes / stop

### ⛔ Strict Execution Mandate (Anti-Corner-Cutting)
These rules are ABSOLUTE. Every scene at every depth level MUST obey:

1. **Execute ALL logic steps, in order** — every step in a scene's logic step table. Do NOT skip, merge, reorder, or shortcut any step. "Reading and summarizing" is NOT the same as "executing."

2. **Each WRITE step produces a real file on disk** — complete, no placeholders, no "TODOs", no abbreviated content.

3. **No step fusion** — if the table says READ → INFER → WRITE, you must do three separate actions. Do not combine multiple steps into one.

4. **Scene completion is binary** — a scene is only done when ALL its logic steps have finished AND ALL output files exist with full content. Do not proceed to the next scene until current one is fully complete.

5. **No output truncation** — every output file must contain the full analysis. Never write "TODO", "in progress", "see above", or any placeholder.

6. **Self-check before completion** — before marking any scene done, verify: (a) every logic step ran, (b) every output file exists with substantive content, (c) every claim references a source line in mineru markdown.

7. **Language compliance** — ALL output files MUST be written in the configured language. The configured language is propagated to every scene and sub-agent. Do NOT mix languages in output files.

### Execution Guardrails
1. **Scene isolation**: Each scene independently executable given its preconditions
2. **No hallucination propagation**: AUDIT_REPORT.md must flag unsupported claims; CONCLUSION_CARD.md must downgrade confidence accordingly
3. **Source grounding**: Every output claim references specific mineru markdown location
4. **LaTeX preservation**: Never corrupt inline (`$...$`) or block (`$$...$$`) LaTeX
5. **Meta-track independence**: output-audit agent shares NO context with primary analysis agents
6. **Language compliance**: ALL output files MUST be written in the configured language (`en` or `zh`). Source material (mineru markdown) stays in original language.

### Prerequisites
- **Input**: Path to mineru-processed PDF markdown (or equivalent structured markdown with LaTeX and tables preserved)
- **Skills**: pdf-figure-extractor, superpowers:dispatching-parallel-agents
- **Tools**: mineru MCP (for initial PDF→markdown, external to this skill)

### Archetype Definitions
Six archetypes from `archetype-logic-vault.md`:
| Archetype | Primary Focus | Secondary Focus |
|-----------|--------------|-----------------|
| THEORY | Mathematical Axioms | Logical Consistency |
| ALGO | Architecture Delta (Δ) | Complexity O(N) |
| DATA | Sampling Diversity | Label Reliability |
| APP | Industrial Bottleneck | Practical Speedup |
| BENCH | Metric Validity | Baseline Fairness |
| REVIEW | Research White-space | Milestone Timeline |

### Execution Pattern
1. **L0**: PREPARE → classify archetype → emit archetype.json (auto)
2. **L1**: ACQUIRE → quick scan + section analysis → emit summaries (auto)
3. **Gate**: Present L1 findings to user; ask to proceed to L2
4. **L2**: Parallel tech-stack + ref-lineage + evidence-check → emit deep analyses (manual)
5. **Gate**: Present L2 findings to user; ask to proceed to L3
6. **L3**: Parallel primary + meta tracks → consistency-audit + output-audit → conclusion (auto within L3)

### Deliverables
| File | Scene | Description |
|------|-------|-------------|
| archetype.json | PREPARE | Machine-readable classification |
| SUMMARY_CARD.md | ACQUIRE | Executive summary |
| FIGURE_LOGS.md | ACQUIRE | Figure-by-figure analysis |
| SECTION_SUMMARIES.md | REASON (section) | 4-quadrant chapter analysis |
| METHODOLOGY_CARD.md | REASON (tech-stack) | Technical pipeline |
| REFERENCE_MAP.md | REASON (ref-lineage) | Citation lineage |
| REVIEW_CARD.md | VERIFY (consistency) | Academic audit |
| AUDIT_REPORT.md | VERIFY (output-audit) | Quality assessment |
| CONCLUSION_CARD.md | FINALIZE | Final verdict |

### Task/Agent Configuration
Each scene is executed as an independent task or sub-agent, with clear inputs and outputs. Use `runSubagent` to invoke specialized agents per scene.

**L0 Dispatch — PREPARE (mandatory, no skip):**
```
runSubagent({
  agentName: "academic-paper-interpreter-l0-prepare",
  description: "Classify paper archetype",
  prompt: "⛔ EXECUTE FULLY — NO SHORTCUTS. Read the full scene-prepare.md instructions, then execute EVERY logic step (P0→P4) in order. Write the complete archetype.json to disk. All output in {language}. Do NOT skip any step."
})
```

**L1 Dispatch (sequential, both mandatory):**
```
runSubagent({
  agentName: "academic-paper-interpreter-l1-quick-scan",
  description: "Extract summary and figures",
  prompt: "⛔ EXECUTE FULLY — NO SHORTCUTS. Read scenes/scene-quick-scan.md, execute EVERY logic step (Q0→Q5) in order. Write both SUMMARY_CARD.md and FIGURE_LOGS.md to disk with full content. All output in {language}. Do NOT skip any step, do NOT produce placeholders."
})

runSubagent({
  agentName: "academic-paper-interpreter-l1-section-analysis",
  description: "Analyze paper sections",
  prompt: "⛔ EXECUTE FULLY — NO SHORTCUTS. Read scenes/scene-section-analysis.md, execute EVERY logic step (S0→S4) in order. Dispatch sub-agents for each selected section, consolidate results, write complete SECTION_SUMMARIES.md. All output in {language}. Do NOT skip any step."
})
```

**L2 Dispatch (parallel, after manual gate — ALL THREE mandatory):**
```
runSubagent({
  agentName: "academic-paper-interpreter-l2-tech-stack",
  description: "Deconstruct technical pipeline",
  prompt: "⛔ EXECUTE FULLY. Read scenes/scene-tech-stack.md, execute EVERY logic step (T0→T3) in order. Write METHODOLOGY_CARD.md to disk. All output in {language}. No shortcuts."
})

runSubagent({
  agentName: "academic-paper-interpreter-l2-ref-lineage",
  description: "Map reference ecosystem",
  prompt: "⛔ EXECUTE FULLY. Read scenes/scene-ref-lineage.md, execute EVERY logic step (R0→R3) in order. Write REFERENCE_MAP.md to disk. All output in {language}. No shortcuts."
})

runSubagent({
  agentName: "academic-paper-interpreter-l2-evidence-check",
  description: "Cross-validate figures and claims",
  prompt: "⛔ EXECUTE FULLY. Read scenes/scene-evidence-check.md, execute EVERY logic step (E0→E2) in order. Append validation marks to SECTION_SUMMARIES.md. All output in {language}. No shortcuts."
})
```

**L3 Dispatch (parallel, after manual gate — BOTH tracks + conclusion):**
```
runSubagent({
  agentName: "academic-paper-interpreter-l3-consistency-audit",
  description: "Full peer-review audit",
  prompt: "⛔ EXECUTE FULLY. Read scenes/scene-consistency-audit.md, execute EVERY logic step (A0→A3) in order. Write REVIEW_CARD.md to disk. All output in {language}. No shortcuts."
})

runSubagent({
  agentName: "academic-paper-interpreter-l3-output-audit",
  description: "Meta-track quality audit (fully independent agent)",
  prompt: "⛔ EXECUTE FULLY as INDEPENDENT meta-track agent. Read scenes/scene-output-audit.md, execute EVERY logic step (O0→O4) in order. Do NOT share context with primary track. Write AUDIT_REPORT.md to disk. All output in {language}. No shortcuts."
})

// After BOTH primary and meta tracks complete:
runSubagent({
  agentName: "academic-paper-interpreter-l3-conclusion",
  description: "Synthesize final verdict",
  prompt: "⛔ EXECUTE FULLY. Read scenes/scene-conclusion.md, execute EVERY logic step (C0→C4) in order. Read both REVIEW_CARD.md and AUDIT_REPORT.md, resolve conflicts, write CONCLUSION_CARD.md to disk. All output in {language}. No shortcuts."
})
```
