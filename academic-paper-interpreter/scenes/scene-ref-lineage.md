## Scene: ref-lineage
- **scene_type**: REASON
- **depth_level**: 2
- **scene_goal**: Map the paper's reference ecosystem — categorize each citation by its role in supporting the paper's contribution
- **preconditions**: `SECTION_SUMMARIES.md` exists; user confirmed L2 entry
- **outputs**: `REFERENCE_MAP.md`
- **next_scenes**:
  - scene_id: consistency-audit, condition: all L2 scenes complete + manual gate passed, transition: manual

### ⛔ Strict Execution Directive
You MUST execute ALL logic steps below (R0→R3) in sequential order. Do NOT skip, merge, or shortcut any step. Extract EVERY citation from the paper — do not sample or summarize. Annotate EACH reference with its role and relevance. Write REFERENCE_MAP.md to disk with the full reference table. All output in the configured language ({language}). Self-check before completion.

### Logic Steps

| step_id | act_type | actor | object | instrument | preconditions | effects | output |
|---------|----------|-------|--------|------------|---------------|---------|--------|
| R0 | READ | orchestrator | Citation patterns in text | mineru markdown | scene ready | list of [ref_id, context_snippet] | — |
| R1 | SELECT | orchestrator | Circling strategy | archetype.json circling rules | R0 complete | categorization schema set | — |
| R2 | INFER | orchestrator | Role per reference | R0 + R1 + archetype-logic-vault.md | R1 complete | reference role annotations | — |
| R3 | WRITE | orchestrator | Reference map | R2 output | R2 complete | — | `REFERENCE_MAP.md` |

### Execution Instructions

1. **Extract all citations** from mineru markdown — match patterns like `[1]`, `[2,3]`, `[4-6]`, `@author`

2. **Select circling strategy** from archetype-logic-vault.md:
   - THEORY → Circle "Foundational Theory"
   - ALGO → Circle "Ancestor Model" and "Direct Competitors"
   - DATA → Circle "Dataset Origin" and "Simulation Protocol"
   - APP → Circle "Pain-point Reference" and "Experimental Ground Truth"
   - BENCH → Circle "Baseline Methods" and "Evaluation Standards"
   - REVIEW → Circle "Turning Point" papers (Milestones)

3. **Annotate each reference** with:
   - In-text citation ID
   - Context of usage (1-sentence from surrounding text)
   - Role classification (foundation / competitor / validation / background / milestone)
   - Relevance to current paper's contribution (high / medium / low)

4. **REFERENCE_MAP.md** format:
   ```markdown
   ## Reference Map
   ### Circling Strategy: [archetype-specific rule]

   | Citation ID | First Author | Role | Context | Relevance |
   |-------------|-------------|------|---------|-----------|
   | [12] | Smith et al. | Foundation | "Our work builds on..." | High |

   ### Key Lineage Insights
   [2-3 sentence synthesis of the reference ecosystem]
   ```
