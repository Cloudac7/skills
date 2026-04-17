---
name: academic-paper-interpreter
description: A high-fidelity, process-driven academic analysis tool. It utilizes a Multi-Agent Swarm and Visual-First strategy to deconstruct PDFs into structured, peer-review-grade Markdown reports.
metadata:
  requires:
    bins: ["mineru-open-api"]
    skills: ["mineru-document-extractor", "superpowers:executing-plans", "superpowers:dispatching-parallel-agents"]
---

# Academic Paper Interpreter

## Skill Overview
This skill transforms raw PDFs into a structured "Logic Map" by leveraging **mineru-document-extractor** for layout fidelity and a phased **Sub-agent Swarm** for cognitive analysis. It prioritizes "Semantic DNA"—preserving complex equations, quantitative tables, and visual evidence chains.

---

## Core Dependencies
* **Parser**: `mineru-document-extractor` (Native Markdown output).
* **Fidelity**: Strict preservation of **LaTeX** ($inline$ and $$block$$) and **Markdown Tables**.
* **Agent Logic**: Orchestrator-Worker model for section-specific deep dives.

---

## The 5-Phase Deep Reading Pipeline

### Phase 1: Global Reconnaissance (Recon)
**Goal**: Establish "What" and "Where" using a **Visual-First Strategy**.
* **Analyze**: Abstract, Conclusion, and all Figure/Table Captions.
* **Action**: Map the evidence chain. For each visual, identify the **Subject** and the **Strategic Takeaway** (the specific insight it provides).
* **Outputs**: `SUMMARY_CARD.md` & `FIGURE_LOGS.md`

### Phase 2: Structural Decomposition (Sub-agent Swarm)
**Goal**: High-granularity extraction without context window dilution.
* **Action**: Orchestrator partitions the paper by headers. Create **Section-Sub-Agents** to analyze each part using the **Four Quadrants**:
    1.  **Fact**: Core concepts and narrative.
    2.  **Method**: Formulas, algorithms, and parametric setups.
    3.  **Data**: Specific quantitative outcomes.
    4.  **Claim**: Author's specific opinions and arguments.
  Use `superpowers:dispatching-parallel-agents` to run these analyses concurrently.
* **Output**: `SECTION_SUMMARIES.md`

### Phase 3: Technical Archeology (Deep Dive)
**Goal**: Isolate the replicable "Research Pipeline."
* **Action**: Deconstruct the "Secret Sauce." Map the **Technical Stack** (Software, Force Fields, GNN architectures) and extract core **Mathematical Definitions** in LaTeX.
* **Output**: `METHODOLOGY_CARD.md`

### Phase 4: Consistency Audit (Peer Review)
**Goal**: Validate robustness and detect "Logical Leaps."
* **Action**: Cross-reference Summary Claims vs. Figure Data. Audit implicit assumptions (e.g., ideal gas behavior) and detect potential risks in generalizability.
* **Output**: `REVIEW_CARD.md` (Includes 3–5 high-level technical challenges).

### Phase 5: Conclusion Synthesis (The Verdict)
**Goal**: Determine practical utility for the user's current roadmap.
* **Action**: Distill final findings into **Actionable Insights**. Recommend whether to adopt, replicate, or pivot based on the study.
* **Output**: `CONCLUSION_CARD.md`

---

## Deliverables Summary

Generate a comprehensive Markdown report with the following structure, following the execution of all phases:

| File | Primary Focus | Content Highlights |
| :--- | :--- | :--- |
| `SUMMARY_CARD.md` | Executive View | Core contribution, Quantitative data, Boundaries. |
| `FIGURE_LOGS.md` | Visual Logic | Caption analysis, Takeaways, Evidence linkage. |
| `SECTION_SUMMARIES.md` | Granular Detail | Four Quadrant summaries for every chapter. Please create sub-agents for each section with `superpowers:dispatching-parallel-agents` skill. |
| `METHODOLOGY_CARD.md` | Replicability | Workflow mapping, Technical stack, LaTeX formulas. |
| `REVIEW_CARD.md` | Critical Audit | Novelty vs. SOTA, Data integrity, Peer-review questions. |
| `CONCLUSION_CARD.md` | Final Verdict | Actionable insights, Final findings, Key quotes. |

---

## Execution Guardrails
1.  **Symbolic Precision**: Never corrupt LaTeX syntax during summarization.
2.  **Zero Hallucination**: If a parameter (e.g., temperature, concentration) isn't in the MinerU data, mark it as **"Not Disclosed"**.
3. **Sub-agent Independence**: Each section agent must treat its assigned section as a standalone "micro-project" to maintain detail density.
4.  **Structure**: Maintain cross-reference anchoring between text claims and Figure IDs.
5.  **Final Synthesis**: The Conclusion Card must be a distillation of all previous cards, not an independent summary.
