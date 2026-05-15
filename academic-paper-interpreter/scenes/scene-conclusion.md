## Scene: conclusion
- **scene_type**: FINALIZE
- **depth_level**: 3
- **scene_goal**: Synthesize primary analysis + meta-track audit into a final verdict with confidence indicators
- **preconditions**: `REVIEW_CARD.md` exists AND `AUDIT_REPORT.md` exists (waits for both tracks to complete)
- **outputs**: `CONCLUSION_CARD.md`
- **transition**: Terminal

### ⛔ Strict Execution Directive
You MUST execute ALL logic steps below (C0→C4) in sequential order. Do NOT skip, merge, or shortcut any step. You MUST read BOTH REVIEW_CARD.md AND AUDIT_REPORT.md — if AUDIT_REPORT.md found hallucinations, you MUST downgrade affected claims. Do not produce a final verdict without considering both tracks. Write CONCLUSION_CARD.md to disk with ALL sections populated. All output in the configured language ({language}). Self-check before completion.

### Logic Steps

| step_id | act_type | actor | object | instrument | preconditions | effects | output |
|---------|----------|-------|--------|------------|---------------|---------|--------|
| C0 | READ | orchestrator | Primary track findings | REVIEW_CARD.md | scene ready | primary findings in context | — |
| C1 | READ | orchestrator | Meta track findings | AUDIT_REPORT.md | scene ready | audit findings in context | — |
| C2 | COMPARE | orchestrator | Conflicts between tracks | C0 + C1 output | C0-C1 complete | conflict resolution map | — |
| C3 | INFER | orchestrator | Final recommendation | C2 output + all L0-L2 outputs | C2 complete | Adopt/Replicate/Pivot/Monitor | — |
| C4 | WRITE | orchestrator | Conclusion card | C3 output | C3 complete | — | `CONCLUSION_CARD.md` |

### Execution Instructions

1. **Read both tracks** — REVIEW_CARD.md (primary) and AUDIT_REPORT.md (meta)

2. **Resolve conflicts**: If AUDIT_REPORT.md flags hallucinations or inconsistencies in L0-L2 outputs:
   - Downgrade confidence for affected conclusions
   - Mark specific claims as "unverified by source audit"
   - If audit found major hallucination, set recommendation to Pivot (audit failure)

3. **Apply trust-level indicators**:
   - ✅ **High confidence**: All claims grounded, no cross-scene conflicts
   - ⚠️ **Medium confidence**: Minor grounding gaps or non-critical inconsistencies
   - ❌ **Low confidence**: Major hallucination or unresolved contradictions

4. **Generate recommendation**:
   - **Adopt**: Method clearly superior, well-grounded, applicable to user's context
   - **Replicate**: Results promising but need verification (provide replication focus areas)
   - **Pivot**: Fundamental flaws or better alternatives identified
   - **Monitor**: Area shows potential but needs maturation

5. **CONCLUSION_CARD.md** format:
   ```markdown
   ## Conclusion Card

   ### Final Verdict
   **Recommendation**: [Adopt / Replicate / Pivot / Monitor]
   **Confidence**: [High / Medium / Low] (per meta-track audit)

   ### Key Findings
   [3-5 bullet points synthesizing all phases]

   ### Confidence Annotations
   | Claim | Confidence | Audit Note |
   |-------|-----------|------------|

   ### Actionable Next Steps
   [Specific recommendations based on verdict]

   ### Key Quotes
   > [Verbatim quotes from paper supporting the verdict]
   ```
