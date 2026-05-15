## Scene: section-analysis
- **scene_type**: REASON
- **depth_level**: 1
- **scene_goal**: Deep-dive into paper sections using four-quadrant analysis (Fact/Method/Data/Claim), driven by archetype priorities
- **preconditions**: `SUMMARY_CARD.md` exists; `archetype.json` exists
- **outputs**: `SECTION_SUMMARIES.md`
- **next_scenes**:
  - scene_id: tech-stack, condition: manual gate, transition: manual
  - scene_id: ref-lineage, condition: manual gate, transition: manual
  - scene_id: evidence-check, condition: manual gate, transition: manual

### ⛔ Strict Execution Directive
You MUST execute ALL logic steps below (S0→S4) in sequential order. Do NOT skip, merge, or shortcut any step. You MUST dispatch sub-agents for EACH selected section — do not analyze sections yourself in a single pass. Consolidate all sub-agent outputs into SECTION_SUMMARIES.md with full content. All output in the configured language ({language}). Self-check before completion: every step ran, output file exists with all sections covered.

### Logic Steps

| step_id | act_type | actor | object | instrument | preconditions | effects | output |
|---------|----------|-------|--------|------------|---------------|---------|--------|
| S0 | READ | orchestrator | Archetype priority flags | archetype.json | scene ready | section selection criteria set | — |
| S1 | SELECT | orchestrator | Sections to analyze | priority flags + section map | S0 complete | section list in context | — |
| S2 | CALL_TOOL | orchestrator | Sub-agents per section | superpowers:dispatching-parallel-agents | S1 complete | section analyses in context | — |
| S3 | COMPARE | orchestrator | Cross-section quadrant results | all sub-agent outputs | S2 complete | merged analysis | — |
| S4 | WRITE | orchestrator | Consolidated section analysis | S3 output | S3 complete | — | `SECTION_SUMMARIES.md` |

### Execution Instructions

1. **Read priority flags** from archetype.json — these determine:
   - Which sections to analyze (not all sections are mandatory)
   - Which quadrants to boost (e.g., ALGO → boost Method quadrant)
2. **Select sections** by scanning the mineru markdown's heading hierarchy (##, ###)
3. **Dispatch sub-agents**: One agent per selected section. Each sub-agent receives the section text and analyzes through four quadrants:
   - **Fact**: Core concepts, definitions, narrative — "What is being described?"
   - **Method**: Formulas, algorithms, procedures — "How is it done?"
   - **Data**: Quantitative outcomes, measurements — "What are the numbers?"
   - **Claim**: Author arguments, interpretations — "What does the author assert?"
4. **Quadrant boost priority** by archetype:
   - ALGO/THEORY → Method depth increased
   - DATA/APP → Data quadrant extraction enhanced
   - BENCH → Claim quadrant scrutiny deepened
   - REVIEW → Fact quadrant expanded
5. **Merge results**: After all sub-agents complete, resolve cross-section conflicts and consolidate into SECTION_SUMMARIES.md with each section as a separate heading

### Manual Gate Instruction
After this scene completes, the orchestrator MUST pause and present to the user:
- Summary of archetype classification + quick-scan findings
- List of available L2 scenes (tech-stack, ref-lineage, evidence-check)
- Recommendation of which L2 scenes are relevant based on archetype
- Prompt: "Proceed to L2 deep analysis? (yes / select scenes / stop)"
