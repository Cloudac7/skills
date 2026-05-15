## Scene: consistency-audit
- **scene_type**: VERIFY
- **depth_level**: 3
- **scene_goal**: Full academic peer-review-style audit — assess novelty, assumption validity, data integrity, and methodological soundness
- **preconditions**: All L0-L2 output files exist (archetype.json, SUMMARY_CARD.md, FIGURE_LOGS.md, SECTION_SUMMARIES.md, METHODOLOGY_CARD.md, REFERENCE_MAP.md)
- **outputs**: `REVIEW_CARD.md`
- **next_scenes**:
  - scene_id: conclusion, condition: REVIEW_CARD.md written AND AUDIT_REPORT.md ready (wait for Meta Track), transition: auto

### ⛔ Strict Execution Directive
You MUST execute ALL logic steps below (A0→A3) in sequential order. Do NOT skip, merge, or shortcut any step. The novelty assessment must include a substantive comparison to SOTA (not just "novel" or "incremental" without evidence). Generate ALL 3-5 challenges, each with title, description, affected component, and severity. Write REVIEW_CARD.md to disk with complete sections. All output in the configured language ({language}). Self-check before completion.

### Logic Steps

| step_id | act_type | actor | object | instrument | preconditions | effects | output |
|---------|----------|-------|--------|------------|---------------|---------|--------|
| A0 | COMPARE | orchestrator | Methodology vs. SOTA | METHODOLOGY_CARD.md + prior knowledge | scene ready | novelty assessment | — |
| A1 | VALIDATE | orchestrator | Implicit assumptions | All L0-L2 outputs | A0 complete | assumption risk inventory | — |
| A2 | INFER | orchestrator | Limitations and challenges | A0-A1 output | A1 complete | 3-5 structured challenges | — |
| A3 | WRITE | orchestrator | Review card | A0-A2 output | A2 complete | — | `REVIEW_CARD.md` |

### Execution Instructions

1. **Novelty assessment**: Compare methodological contribution against known SOTA (use the paper's own SOTA discussion + external knowledge). Rate as: novel increment / incremental / incremental with insights / re-packaging.

2. **Assumption auditing**: Identify implicit assumptions in the methodology:
   - Statistical assumptions (distribution, independence)
   - Environmental assumptions (ideal conditions, controlled settings)
   - Generalization assumptions (domain transfer, scaling)
   - For each: assess risk if assumption is violated

3. **Challenge identification**: Generate 3-5 structured challenges:
   - Each challenge has: title, description, affected component, severity (high/med/low)
   - Cover these dimensions: methodology, data, generalization, implementation, reproducibility

4. **REVIEW_CARD.md** format:
   ```markdown
   ## Review Card

   ### Novelty Assessment
   [rating + 2-3 sentence justification]

   ### Assumption Audit
   | Assumption | Risk if Violated | Severity |
   |-----------|-----------------|----------|

   ### Challenges
   1. **[Title]** — Description. *Severity: High*
   2. **[Title]** — Description. *Severity: Medium*

   ### Peer-Review Questions
   - [Question about methodology gap]
   - [Question about data integrity]
   ```
