### Phase 4: Consistency Audit (Peer Review)

#### Overview
**Goal**: Validate robustness and detect "Logical Leaps." This phase performs a critical review by cross-referencing claims against evidence, auditing assumptions, and identifying potential weaknesses in the research.

#### Detailed Actions

##### 1. Cross-Reference Analysis
- Compare summary claims from Phase 1 with quantitative data from Phase 2.
- Verify figure data alignments with textual assertions.
- Check for consistency between abstract promises and conclusion deliveries.

##### 2. Assumption Auditing
- Identify implicit assumptions (e.g., "ideal gas behavior", "normal distribution", "linear relationships").
- Evaluate generalizability risks under non-ideal conditions.
- Assess boundary conditions and edge cases.

##### 3. Archetype-Specific Audits
- **[DATA]**: Audit for data leakage, selection bias, and preprocessing artifacts.
- **[ALGO]**: Verify ablation studies justify claimed innovations; check for overfitting.
- **[THEORY]**: Validate proofs under non-ideal conditions; assess mathematical rigor.
- **[APP]**: Evaluate real-world validation comprehensiveness and industrial relevance.
- **[BENCH]**: Scrutinize fairness metrics across subgroups and demographic variations.
- **[REVIEW]**: Confirm lineage claims are supported by cited evidence.

##### 4. Challenge Identification
Generate 3-5 high-level technical challenges or limitations:
- Methodological weaknesses
- Data constraints
- Generalization issues
- Implementation hurdles
- Future research directions

#### Outputs
- `REVIEW_CARD.md`: Critical audit report including novelty assessment, data integrity evaluation, and peer-review style questions.

#### Claude Code Implementation Notes
- Cross-reference outputs from previous phases for consistency checks.
- Use logical reasoning to identify potential flaws or unsupported claims.
- Focus on evidence-based critiques rather than speculative concerns.
- Structure challenges as actionable insights for improvement.
