## Scene: tech-stack
- **scene_type**: REASON
- **depth_level**: 2
- **scene_goal**: Deconstruct the paper's technical pipeline and reconstruct replicable research workflow
- **preconditions**: `SECTION_SUMMARIES.md` exists; user confirmed L2 entry
- **outputs**: `METHODOLOGY_CARD.md`
- **next_scenes**:
  - scene_id: consistency-audit, condition: all L2 scenes complete + manual gate passed, transition: manual

### ⛔ Strict Execution Directive
You MUST execute ALL logic steps below (T0→T3) in sequential order. Do NOT skip, merge, or shortcut any step. The pipeline diagram MUST be a real ASCII diagram, not a text description. All LaTeX formulas MUST be preserved exactly. Write METHODOLOGY_CARD.md to disk with complete content. All output in the configured language ({language}). Self-check before completion.

### Logic Steps

| step_id | act_type | actor | object | instrument | preconditions | effects | output |
|---------|----------|-------|--------|------------|---------------|---------|--------|
| T0 | SELECT | orchestrator | Archetype-specific technical focus | archetype.json priority flags | scene ready | analysis direction set | — |
| T1 | COMPARE | orchestrator | Method vs. claimed contribution | SECTION_SUMMARIES.md | T0 complete | alignment assessment | — |
| T2 | INFER | orchestrator | Full technical pipeline | mineru markdown + T0 direction | T1 complete | pipeline reconstruction | — |
| T3 | WRITE | orchestrator | Methodology card | T2 output | T2 complete | — | `METHODOLOGY_CARD.md` |

### Execution Instructions

1. **Select focus** based on archetype:
   - ALGO/THEORY → "Secret Sauce": core innovation, software/hardware stack, LaTeX math definitions
   - DATA → "Data Pipeline": dataset origins, simulation protocols, preprocessing steps, evaluation metrics
   - APP → "Validation Protocol": industrial pain-points, experimental setups, ground truth
   - BENCH → "Benchmarking Protocol": metric validity, baselines, fairness
   - REVIEW → "Lineage Map": research evolution timeline, white spaces

2. **Verify method–claim alignment**: Does the technical approach actually support the claimed contribution? Flag any gap.

3. **Reconstruct pipeline** as input→process→output flow diagram in ASCII, with:
   - Each stage labeled
   - Key parameters noted
   - Data/control flow arrows

4. **METHODOLOGY_CARD.md** format:
   ```markdown
   ## Methodology Card
   ### Pipeline Overview
   [ASCII pipeline diagram]

   ### Technical Stack
   | Component | Technology | Purpose |
   |-----------|-----------|---------|

   ### Key Formulas
   $$...$$ (preserve exact LaTeX)

   ### Method–Claim Alignment
   [Assessment: aligned / partial gap / contradiction]
   ```
