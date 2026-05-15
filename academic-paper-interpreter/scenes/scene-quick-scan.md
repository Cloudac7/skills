## Scene: quick-scan
- **scene_type**: ACQUIRE
- **depth_level**: 1
- **scene_goal**: Establish "what" and "where" — extract core contribution, quantitative highlights, and visual evidence map
- **preconditions**: `archetype.json` exists and is readable
- **outputs**: `SUMMARY_CARD.md`, `FIGURE_LOGS.md`
- **next_scenes**:
  - scene_id: section-analysis, condition: SUMMARY_CARD.md written, transition: auto

### ⛔ Strict Execution Directive
You MUST execute ALL logic steps below (Q0→Q5) in sequential order. Do NOT skip, merge, or shortcut any step. You MUST produce BOTH SUMMARY_CARD.md and FIGURE_LOGS.md on disk with full content — not placeholders, not TODOs, not "see above". All output in the configured language ({language}). Self-check before completion: every step ran, both output files exist and are substantive.

### Logic Steps

| step_id | act_type | actor | object | instrument | preconditions | effects | output |
|---------|----------|-------|--------|------------|---------------|---------|--------|
| Q0 | READ | orchestrator | Abstract + conclusion sections | mineru markdown | archetype.json ready | core claims extracted | — |
| Q1 | READ | orchestrator | All figure/table captions | mineru markdown | Q0 complete | caption list with line refs | — |
| Q2 | INFER | orchestrator | Evidence chain map | figure references + text claims | Q0-Q1 complete | figure↔claim mapping in context | — |
| Q3 | CALL_TOOL | orchestrator | pdf-figure-extractor | pdf-figure-extractor skill | Q1 complete; archetype priority flags | figure images on disk | figures/*.png |
| Q4 | WRITE | orchestrator | Executive summary | archetype.json + Q2 output | Q2-Q3 complete | — | `SUMMARY_CARD.md` |
| Q5 | WRITE | orchestrator | Figure log | Q2-Q3 output | Q2-Q3 complete | — | `FIGURE_LOGS.md` |

### Execution Instructions

1. **Extract abstract and conclusion** paragraphs verbatim from mineru markdown
2. **Scan all figure/table captions** — grep for `Figure`, `Fig.`, `Table`, `Tab.` patterns
3. **Map evidence chains**: For each figure/table, identify which text claim it supports (look for cross-references like "as shown in Figure 3")
4. **Extract key figures** via pdf-figure-extractor skill for all figures marked as high-priority by archetype flags
5. **Write SUMMARY_CARD.md** with sections:
   - Core Contribution (1-2 sentences from abstract)
   - Quantitative Highlights (key numbers with figure references)
   - Key Boundaries (limitations explicitly stated in conclusion)
6. **Write FIGURE_LOGS.md** as a table:
   | Figure ID | Caption | Subject | Key Takeaway | Linked Claim | File |
   |-----------|---------|---------|--------------|--------------|------|
   | Figure 1 | ... | ... | ... | See Section X | figures/figure-1.png |
