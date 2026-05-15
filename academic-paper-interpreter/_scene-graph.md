# Scene Graph — SSL Structural Layer

## Scene Topology (DAG)

```
L0    PREPARE (archetype-detect)
        │
        ▼ (auto)
L1    ACQUIRE (quick-scan) ──► REASON (section-analysis)
        │                           │
        ▼ (manual gate)
        │
L2    ┌── REASON (tech-stack) ──► METHODOLOGY_CARD.md
      │── REASON (ref-lineage) ──► REFERENCE_MAP.md
      │── VERIFY (evidence-check) ──► marks in SECTION_SUMMARIES.md
        │                           │
        ▼ (manual gate)
        │
L3    ┌── Primary Track:
      │   ├── VERIFY (consistency-audit) ──► REVIEW_CARD.md
      │   └── FINALIZE (conclusion) ──────► CONCLUSION_CARD.md
      │
      └── Meta Track (independent agent):
          └── VERIFY (output-audit) ──────► AUDIT_REPORT.md
```

## Depth Level Rules

| Level | Scenes | Entry | Exit Transition |
|-------|--------|-------|-----------------|
| L0 | PREPARE | External (mineru markdown ready) | Auto → L1 |
| L1 | ACQUIRE → REASON (section-analysis) | Auto from L0 | Manual gate to L2 |
| L2 | REASON (tech-stack, ref-lineage) + VERIFY (evidence-check) | Manual gate from L1 | Manual gate to L3 |
| L3 | VERIFY (consistency-audit, output-audit) + FINALIZE | Manual gate from L2 | Terminal |

## Transition Conditions

### Auto Transitions
| From | To | Condition |
|------|----|-----------|
| PREPARE | ACQUIRE | archetype.json written successfully |
| ACQUIRE | section-analysis | SUMMARY_CARD.md written successfully |
| All L2 scenes | (wait for L2 gate) | All dispatched L2 parallel scenes complete |
| L3 Primary scenes | FINALIZE | Both REVIEW_CARD.md and AUDIT_REPORT.md ready |
| L3 Meta Track | (join with Primary) | AUDIT_REPORT.md written |

### Manual Gates
| Gate | Trigger | Display to User |
|------|---------|-----------------|
| L1→L2 | After SECTION_SUMMARIES.md complete | Summary of L1 findings + recommended L2 scenes based on archetype |
| L2→L3 | After all L2 outputs complete | Consolidated L2 findings + prompt: "Proceed to full audit and conclusion?" |

## Manual Gate Protocol
At each manual gate, the orchestrator MUST:
1. Present a bullet-point summary of the just-completed level's key findings
2. List which next-level scenes are recommended (based on archetype priority flags)
3. Offer the user options: (a) proceed to all recommended scenes, (b) select specific scenes, (c) stop

## Dependency Resolution
| Scene | Depends On | Produces |
|-------|-----------|----------|
| PREPARE | mineru markdown | archetype.json |
| ACQUIRE | archetype.json | SUMMARY_CARD.md, FIGURE_LOGS.md |
| section-analysis | SUMMARY_CARD.md, archetype.json | SECTION_SUMMARIES.md |
| tech-stack | SECTION_SUMMARIES.md | METHODOLOGY_CARD.md |
| ref-lineage | SECTION_SUMMARIES.md | REFERENCE_MAP.md |
| evidence-check | FIGURE_LOGS.md, SECTION_SUMMARIES.md | Validation marks |
| consistency-audit | All L0-L2 outputs | REVIEW_CARD.md |
| output-audit | All L0-L2 outputs + mineru markdown | AUDIT_REPORT.md |
| conclusion | REVIEW_CARD.md, AUDIT_REPORT.md, L0-L2 outputs | CONCLUSION_CARD.md |
