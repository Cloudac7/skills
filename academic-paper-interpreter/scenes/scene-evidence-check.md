## Scene: evidence-check
- **scene_type**: VERIFY
- **depth_level**: 2
- **scene_goal**: Lightweight cross-validation — verify that figure data supports text claims and abstract promises match conclusion deliveries
- **preconditions**: `FIGURE_LOGS.md` and `SECTION_SUMMARIES.md` exist
- **outputs**: Validation marks appended to `SECTION_SUMMARIES.md`
- **transition**: Auto (runs in parallel with other L2 scenes; does NOT require manual gate)

### ⛔ Strict Execution Directive
You MUST execute ALL logic steps below (E0→E2) in sequential order. Do NOT skip, merge, or shortcut any step. Check EVERY figure against its text claim. Check EVERY abstract promise against the conclusion. Do NOT cherry-pick only the easy verifications. Append the full validation table to SECTION_SUMMARIES.md. All output in the configured language ({language}). Self-check before completion.

### Logic Steps

| step_id | act_type | actor | object | instrument | preconditions | effects | output |
|---------|----------|-------|--------|------------|---------------|---------|--------|
| E0 | COMPARE | orchestrator | Figure data vs. text claims | FIGURE_LOGS.md + SECTION_SUMMARIES.md | scene ready | per-figure alignment status | — |
| E1 | COMPARE | orchestrator | Abstract promises vs. conclusion deliveries | SUMMARY_CARD.md + mineru markdown conclusion | E0 complete | delivery status per claim | — |
| E2 | WRITE | orchestrator | Validation marks | E0-E1 output | E0-E1 complete | — | Appended to SECTION_SUMMARIES.md |

### Execution Instructions

1. **Figure–text alignment**: For each figure in FIGURE_LOGS.md:
   - Find the text claim it references (via figure cross-reference in mineru markdown)
   - Does the figure data actually support the claim? (verified / questionable / contradiction)
   - Log specific discrepancies when found

2. **Abstract–conclusion alignment**: For each claim in the abstract:
   - Find if it's addressed in the conclusion
   - Is the conclusion consistent with the abstract claim? (delivered / partially / undelivered)

3. **Write validation marks** as a section appended to SECTION_SUMMARIES.md:
   ```markdown
   ## Evidence Check Results

   ### Figure–Text Alignment
   | Figure ID | Claim Reference | Status | Note |
   |-----------|----------------|--------|------|
   | Figure 2 | "15% improvement" | Verified | Matches bar chart data |
   | Figure 4 | "linear scaling" | Contradiction | Log-scale shows exponential |

   ### Abstract–Conclusion Alignment
   | Abstract Claim | Conclusion Status | Note |
   |---------------|-------------------|------|
   | "novel architecture" | Delivered | Detailed in Section 3 |
   | "state-of-the-art results" | Partial | Only compared against 2 baselines |
   ```
