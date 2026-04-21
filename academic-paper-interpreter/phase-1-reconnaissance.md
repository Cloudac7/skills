### Phase 1: Reconnaissance (Visual-First)

#### Overview
**Goal**: Establish "What" and "Where" using a **Visual-First Strategy**. This phase builds on the archetype classification from Phase 0 to create an initial understanding of the paper\'s structure and key insights through visual elements.

#### Detailed Actions

##### 1. Content Analysis
- **Abstract**: Extract core problem statement, methodology overview, and main results.
- **Conclusion**: Identify final outcomes, limitations, and future work.
- **Figure/Table Captions**: Analyze all captions for data trends, experimental setups, and key findings.

##### 2. Evidence Chain Mapping
For each visual element (figures, tables, diagrams):
- **Subject Identification**: Determine what the visual represents (e.g., algorithm flowchart, performance comparison, data distribution).
- **Strategic Takeaway Extraction**: Identify the specific insight or conclusion drawn from the visual (e.g., "Method A outperforms baselines by 15%", "Data shows linear correlation").

##### 3. Archetype-Specific Focus
- **If [APP]**: Prioritize "Experimental vs. Predicted" charts to understand real-world applicability.
- **If [THEORY]**: Focus on "Structural Diagrams" for conceptual frameworks and proofs.
- **If [ALGO]**: Examine architecture diagrams and flowcharts for innovation points.
- **If [DATA]**: Look for pipeline visualizations and data flow diagrams.
- **If [BENCH]**: Analyze comparative charts and fairness plots.
- **If [REVIEW]**: Map taxonomy diagrams and research landscape visualizations.

#### Outputs
- `SUMMARY_CARD.md`: Executive summary with core contribution, quantitative highlights, and key boundaries.
- `FIGURE_LOGS.md`: Detailed log of each figure/table with subject, takeaway, linkage to text claims, and extracted figure images.

#### Claude Code Implementation Notes
- Use `pdf-figure-extractor` skill to extract and embed figures from the PDF into FIGURE_LOGS.md with proper Markdown image references.
- For each figure/table:
  - Extract image using `pdf-figure-extractor`
  - Store image in appropriate directory (e.g., `figures/`)
  - Link image in markdown as `![Figure caption](figures/figure-N.png)`
- Use `view_image` tool if images are available for caption analysis and verification.
- Employ `grep_search` to locate figure references in the text (e.g., "Figure 1", "Table 2").
- Cross-reference visual takeaways with abstract and conclusion statements.
- Ensure all visual analyses are grounded in explicit captions and surrounding text.
- Maintain consistent figure numbering and directory structure across all outputs.
