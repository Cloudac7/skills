# Resource Scopes — SSL Logical Layer Closed Vocabulary

## Definition
Resource scopes classify the type of resource a logic step accesses, reads, or writes. Every CALL_TOOL and READ/WRITE step SHOULD declare a resource_scope.

## Vocabulary

| Scope | Symbol | Description | Examples |
|-------|--------|-------------|----------|
| MEMORY | MEM | In-context data, agent working memory, sub-agent context | Analysis state, quadrant results, priority flags |
| LOCAL_FS | FS | Local file system — output files, cached artifacts | SUMMARY_CARD.md, figure images, mineru markdown |
| CODEBASE | CODE | Skill definition files, scene files, logic vocabularies | SKILL.md, scene-*.md, act-types.md |
| NETWORK | NET | External API calls, MCP tools, network services | mineru MCP, pdf-figure-extractor |

## Usage Rules
1. Declare resource_scope in the `instrument` column of logic step tables
2. Each scene's preconditions define what resources must already be available
3. CALL_TOOL steps MUST specify the target tool's resource scope
