### Phase 3: Technical Archeology (Deep Dive)

#### Overview
**Goal**: Isolate the replicable "Research Pipeline." This phase deconstructs the technical implementation and reference ecosystem to understand the complete research workflow and its foundations.

#### Detailed Actions

##### 1. Technical Stack Deconstruction
Based on archetype:
- **[ALGO/THEORY]**: Map the "Secret Sauce" - identify core innovations, technical stack (software frameworks, hardware), and extract mathematical definitions in LaTeX.
- **[DATA]**: Deconstruct the "Data Pipeline" - trace dataset origins, simulation protocols, preprocessing steps, and evaluation metrics.
- **[APP]**: Deconstruct the "Validation Protocol" - identify industrial pain-points, experimental setups, and ground truth measurements.
- **[BENCH]**: Deconstruct the "Benchmarking Protocol" - analyze metric validity, baseline comparisons, and fairness considerations.
- **[REVIEW]**: Deconstruct the "Lineage Map" - trace research evolution, identify white spaces, and timeline milestones.

##### 2. Reference Lineage Mapping
- **Ref-Mapping Logic**: Categorize references based on archetype context:
  - [ALGO]: Identify "Ancestor" models or baseline algorithms.
  - [APP]: Identify "Ground Truth" datasets or real-world validation sources.
  - [DATA]: Circle preprocessing or data augmentation references.
  - [THEORY]: Highlight foundational mathematical or physical principles.
  - [BENCH]: Mark fairness frameworks or evaluation standards.
  - [REVIEW]: Map the research trajectory and key milestones.

##### 3. Strict Grounding Constraints
- All "circled" references must be explicitly cited in the paper (e.g., [12], Smith et al.).
- Prohibit introducing external knowledge or unmentioned papers.
- For each key reference, include:
  - In-text citation ID
  - Specific context of usage
  - Relevance to the current paper\'s contribution

#### Outputs
- `METHODOLOGY_CARD.md`: Detailed workflow mapping, technical stack, and LaTeX formulas.
- `REFERENCE_MAP.md`: Structured reference lineage with archetype-based categorization.

#### Claude Code Implementation Notes
- Use `grep_search` to locate citation patterns and reference usage.
- Cross-reference with Phase 2 outputs for technical details.
- Validate all reference mappings against explicit paper content.
- Preserve mathematical notation integrity during extraction.
