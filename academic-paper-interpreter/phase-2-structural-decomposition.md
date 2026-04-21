### Phase 2: Structural Decomposition (Sub-agent Swarm)

#### Overview
**Goal**: High-granularity extraction without context window dilution. This phase uses parallel sub-agents to analyze each section of the paper through four distinct quadrants, ensuring comprehensive coverage while maintaining detail density.

#### Detailed Actions

##### 1. Section Identification
- Divide the paper into logical sections (Introduction, Methods, Results, Discussion, etc.).
- For each section, spawn a dedicated sub-agent using `superpowers:dispatching-parallel-agents`.

##### 2. Four Quadrant Analysis
Each sub-agent analyzes its assigned section through four lenses:

1. **Fact**: Extract core concepts, definitions, and narrative elements.
   - Focus: What is being described or explained?
   - Output: Key concepts, terminology, and foundational knowledge.

2. **Method**: Identify formulas, algorithms, procedures, and parametric setups.
   - Focus: How is it done?
   - Output: Step-by-step processes, equations, and implementation details.

3. **Data**: Capture specific quantitative outcomes, measurements, and results.
   - Focus: What are the numbers and measurements?
   - Output: Metrics, statistics, experimental results, and data points.

4. **Claim**: Extract author opinions, arguments, interpretations, and conclusions.
   - Focus: What does the author assert or conclude?
   - Output: Hypotheses, interpretations, and argumentative statements.

##### 3. Archetype-Adaptive Quadrant Boosting
Based on Phase 0 classification:
- **[ALGO/THEORY]**: Increase Method quadrant depth for algorithmic details and mathematical derivations.
- **[DATA/APP]**: Enhance Data quadrant extraction, including units, scales, benchmarks, and validation metrics.
- **[BENCH]**: Boost Claim quadrant for fairness nuances, metric interpretations, and comparative arguments.
- **[REVIEW]**: Expand Fact quadrant for lineage mapping, taxonomy details, and research context.

#### Outputs
- `SECTION_SUMMARIES.md`: Comprehensive summaries for each section, organized by the four quadrants.

#### Claude Code Implementation Notes
- Use `runSubagent` or equivalent to dispatch parallel analyses for each section.
- Ensure each sub-agent treats its section as an independent "micro-project" to maintain context density.
- Maintain cross-references between quadrants within each section.
- Preserve LaTeX formatting in Method quadrant extractions.
