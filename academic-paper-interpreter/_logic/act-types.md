# Act Types — SSL Logical Layer Closed Vocabulary

## Definition
Act types are the closed vocabulary of atomic actions that logic steps within any scene can use. Every logic step in every scene MUST use exactly one act_type from this list.

## Vocabulary

| Act Type | Symbol | Description | Used In |
|----------|--------|-------------|---------|
| READ | R | Read data from a source (file, markdown, metadata) without modifying it | All scenes |
| SELECT | S | Choose among alternatives based on criteria (archetype, sections, strategy) | PREPARE, section-analysis, tech-stack, ref-lineage |
| COMPARE | C | Cross-reference two or more items for consistency, alignment, or contradiction | section-analysis, tech-stack, evidence-check, consistency-audit, conclusion |
| VALIDATE | V | Verify correctness, consistency, or integrity against a standard | evidence-check, consistency-audit, output-audit |
| INFER | I | Draw conclusions, reconstruct pipelines, synthesize insights from evidence | PREPARE, quick-scan, tech-stack, ref-lineage, consistency-audit, conclusion |
| WRITE | W | Create or overwrite an output file | All output-producing scenes |
| CALL_TOOL | T | Invoke an external tool (sub-agent, pdf-figure-extractor, semantic search) | quick-scan, section-analysis |
| UPDATE_STATE | U | Update execution context: precondition state, DAG traversal status, priority flags | _scene-graph orchestrator |
| TERMINATE | X | End scene execution and signal transition to next scene(s) | All scenes (implicit final step) |

## Usage Rules
1. Every logic step table MUST include an act_type column using these symbols
2. Do not invent new act types — if none fits, use INFER and document the gap
3. Multiple consecutive steps of the same act_type are allowed when they operate on different objects
