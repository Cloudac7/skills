## 0. Phase 0: Archetype Detection (Pre-flight)

### Overview
Referring to the **Focus Priority Matrix** in `archetype-logic-vault.md`, the Orchestrator will adapt the subsequent phases to prioritize the relevant aspects of the paper based on its archetype classification. This pre-flight phase ensures that the analysis is tailored to the paper\'s primary focus, maximizing efficiency and relevance.

### Detailed Actions

#### 1. Surface Scan Execution
- **Input**: Raw PDF content extracted via `mineru-document-extractor`.
- **Process**:
  - Extract and analyze the Title for key terms indicating domain (e.g., "neural network", "thermodynamics", "benchmark").
  - Parse the Abstract for core contributions, methodology hints, and outcome statements.
  - Scan for keyword density across the document, focusing on technical terms, acronyms, and domain-specific vocabulary.
- **Tools**: Use semantic search or regex patterns to identify high-frequency terms.

#### 2. Archetype Classification
Assign the paper to one of the 6 archetypes based on the dominant theme and evidence from the surface scan:

1. **[THEORY]**: Papers focused on mathematical derivations, physical proofs, or theoretical frameworks.
   - Indicators: Heavy use of equations, proofs, lemmas, theorems; keywords like "proof", "derivation", "theorem", "mathematical model".
   - Priority: Emphasize Method quadrant in later phases.

2. **[ALGO]**: Papers introducing novel algorithms, architectures, or computational methods.
   - Indicators: Algorithm descriptions, pseudocode, innovation claims; keywords like "algorithm", "architecture", "novel method", "optimization".
   - Priority: Deep dive into technical implementation and innovation delta.

3. **[DATA]**: Papers centered on data processing pipelines, fidelity improvements, or data-centric techniques.
   - Indicators: Dataset descriptions, preprocessing steps, fidelity metrics; keywords like "dataset", "pipeline", "fidelity", "preprocessing".
   - Priority: Focus on data lineage and evaluation protocols.

4. **[APP]**: Applied papers addressing industrial problems, real-world validation, or practical implementations.
   - Indicators: Case studies, industrial applications, validation against real data; keywords like "industrial", "application", "validation", "real-world".
   - Priority: Emphasize experimental ground truth and pain-point resolution.

5. **[BENCH]**: Benchmarking or evaluation-focused papers comparing methods across metrics.
   - Indicators: Comparative studies, fairness analysis, metric evaluations; keywords like "benchmark", "fairness", "metrics", "comparison".
   - Priority: Audit for robustness and subgroup fairness.

6. **[REVIEW]**: Survey or review papers synthesizing existing work, taxonomies, or research landscapes.
   - Indicators: Citations to many sources, taxonomy sections, gap analysis; keywords like "survey", "review", "taxonomy", "landscape".
   - Priority: Map research lineage and identify white spaces.

#### 3. Adaptation Logic
- Based on the assigned archetype, set flags or priorities for subsequent phases:
  - If [THEORY]: Boost Phase 3 Method extraction and LaTeX preservation.
  - If [ALGO]: Enhance Phase 2 Claim quadrant for innovation justification.
  - If [DATA]: Prioritize Phase 4 data integrity audits.
  - If [APP]: Focus Phase 1 on experimental vs. predicted visuals.
  - If [BENCH]: Increase Phase 4 fairness and metric scrutiny.
  - If [REVIEW]: Expand Phase 3 reference mapping and lineage analysis.

#### 4. Output Preparation
- Record the archetype classification in a metadata file or pass as context to Phase 1.
- Ensure classification is grounded in explicit paper content; avoid assumptions.

### Claude Code Implementation Notes
- When executing this phase, use the `semantic_search` tool to analyze the PDF content for keywords.
- Cross-reference with `archetype-logic-vault.md` for additional classification rules.
- If uncertain between archetypes, default to the one with the highest keyword match density.
- Log the classification reasoning for transparency in the final report.
