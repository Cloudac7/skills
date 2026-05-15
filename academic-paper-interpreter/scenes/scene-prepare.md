## Scene: prepare
- **scene_type**: PREPARE
- **depth_level**: 0
- **scene_goal**: Classify paper archetype and generate analysis strategy flags
- **preconditions**: mineru PDF markdown available at known path
- **outputs**: `archetype.json`
- **next_scenes**:
  - scene_id: quick-scan, condition: archetype.json written, transition: auto

### ⛔ Strict Execution Directive
You MUST execute ALL logic steps below (P0→P4) in sequential order. Do NOT skip, merge, or shortcut any step. Each WRITE step must produce a real file on disk with complete content. Do NOT produce placeholders, TODOs, or abbreviated output. All output in the configured language ({language}). Self-check before completion: every step ran, every output file exists.

### Logic Steps

| step_id | act_type | actor | object | instrument | preconditions | effects | output |
|---------|----------|-------|--------|------------|---------------|---------|--------|
| P0 | READ | orchestrator | PDF metadata (title, abstract, keywords) | mineru markdown | mineru markdown available | metadata in context | — |
| P1 | READ | orchestrator | Section headings and structure | mineru markdown | P0 complete | section map in context | — |
| P2 | SELECT | orchestrator | Archetype classification | Archetype Logic Vault | P0-P1 complete | archetype assigned | archetype.json |
| P3 | INFER | orchestrator | Priority flags per archetype | Archetype->priority mapping | P2 complete | flags in context | (embedded in archetype.json) |
| P4 | WRITE | orchestrator | Structured classification | — | P2-P3 complete | archetype.json on disk | `archetype.json` |

### Execution Instructions

1. **Extract metadata** from the first 20% of mineru markdown: title, abstract, keywords, section headings
2. **Classify archetype** by analyzing keyword density against the six archetype definitions in `archetype-logic-vault.md`:
   - THEORY: mathematical derivations, proofs, lemmas, theorems
   - ALGO: novel architectures, pseudocode, innovation claims
   - DATA: dataset pipelines, fidelity metrics, preprocessing
   - APP: industrial validation, case studies, real-world
   - BENCH: comparative evaluation, fairness, metrics
   - REVIEW: survey, taxonomy, research landscape
3. **Generate priority flags** as JSON:
   ```json
   {
     "archetype": "ALGO",
     "confidence": 0.87,
     "evidence": ["keyword 'architecture' 12x", "keyword 'novel method' 8x", "pseudocode in section 3"],
     "priority_sections": [3, 4],
     "boosted_quadrants": ["method", "claim"],
     "recommended_scenes": ["tech-stack", "evidence-check"]
   }
   ```
4. If uncertain between archetypes, assign the highest-confidence match AND list the runner-up in `archetype.json` with `ambiguous: true`
