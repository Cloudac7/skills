---
name: lark-paper-interpreter
description: 从Zotero检索论文、解析PDF、生成学术论文解读报告并创建飞书文档。当用户需要检索论文、解析PDF并生成解读报告时使用。
metadata:
  requires:
    bins: ["lark-cli", "mineru-open-api"]
    skills: ["zotero-mcp-code", "mineru-document-extractor", "academic-paper-interpreter", "superpowers:executing-plans", "superpowers:dispatching-parallel-agents", "lark-doc", "lark-shared"]
---

# 学术论文解读工作流

## 概述

本技能整合多个工具完成学术论文的检索、解析、解读和飞书文档创建全流程。

## 工作流步骤

### Step 1: Zotero文献检索

使用 `zotero-mcp-code` skill 搜索文献：

```python
import os
import sys
ZOTERO_CODE_PATH = os.environ.get("ZOTERO_CODE_EXECUTION_PATH")
if not ZOTERO_CODE_PATH:
    raise ValueError("必须设置 ZOTERO_CODE_EXECUTION_PATH 环境变量")
sys.path.append(ZOTERO_CODE_PATH)
import setup_paths
from zotero_lib import SearchOrchestrator, format_results

orchestrator = SearchOrchestrator()
results = orchestrator.comprehensive_search("论文标题或关键词", max_results=10)
print(format_results(results))
```

记录返回的文献 **Key**（用于定位PDF）。

### Step 2: 定位PDF文件

**配置 Zotero 存储路径**

设置环境变量 `ZOTERO_STORAGE_PATH` 指向你的 Zotero 存储位置：

```bash
# Windows (WSL下)
export ZOTERO_STORAGE_PATH="/mnt/c/Users/YourUsername/Zotero/storage/"

# macOS/Linux
export ZOTERO_STORAGE_PATH="$HOME/Zotero/storage/"

# 或在命令中直接使用（如未设置环境变量）
ZOTERO_STORAGE_PATH="/path/to/your/zotero/storage"
```

**查找PDF文件**

```bash
# 查找目标文献的storage文件夹
ls -la "$ZOTERO_STORAGE_PATH<KEY>/"

# 查找PDF文件
find "$ZOTERO_STORAGE_PATH" -o -name "*.pdf" | grep -i <KEY>
```

### Step 3: PDF解析

使用 MinerU 解析PDF。

参考 `mineru-document-extractor` 或 `mineru` skill 进行PDF解析，生成Markdown格式的文本输出。

```bash
# 文件小于10MB用flash-extract
mineru-open-api flash-extract "/path/to/paper.pdf" --language en -o /tmp/output/

# 文件大于10MB用extract（需token）
mineru-open-api extract "/path/to/paper.pdf" --language en -o /tmp/output/
```

**提示**：
- flash-extract 限制：10MB/20页，无表格识别
- extract 需要token（创建于 https://mineru.net/apiManage/token）

### Step 4: 生成学术论文解读

根据 [academic-paper-interpreter skill](../academic-paper-interpreter/SKILL.md) ，生成以下5个markdown文件：

1. **SUMMARY_CARD.md** - 论文摘要
   - 标题、核心贡献、关键数据、局限性

2. **SECTION_SUMMARIES.md** - 分章节摘要
   - 各章节详细总结

3. **METHODOLOGY_CARD.md** - 论文方法
   - 流程映射、技术栈、数学定义

4. **REVIEW_CARD.md** - 论文评述
   - 创新性、数据完整性、领域影响

5. **CONCLUSION_CARD.md** - 结论与建议
   - 最终发现、行动建议、关键引述

### Step 5: 创建飞书文档

使用 `lark-doc` skill 创建文档：

```bash
# 先阅读lark-shared了解认证
# 读取: ../lark-shared/SKILL.md

# 合并5个markdown文件
cat SUMMARY_CARD.md SECTION_SUMMARIES.md METHODOLOGY_CARD.md REVIEW_CARD.md CONCLUSION_CARD.md > combined.md

# 创建飞书文档
lark-cli docs +create --title "【论文解读】论文标题" --markdown "$(cat combined.md)"
```

## 目录结构

```
/tmp/
├── <paper_name>/              # MinerU解析输出
│   └── <paper_name>.md
├── <paper_name>_papers/      # 解读报告输出
│   ├── SUMMARY_CARD.md
│   ├── SECTION_SUMMARIES.md
│   ├── METHODOLOGY_CARD.md
│   ├── REVIEW_CARD.md
│   └── CONCLUSION_CARD.md
└── combined.md                # 合并后的完整报告
```

## 关键路径

| 资源 | 路径 |
|------|------|
| Zotero存储 | `$ZOTERO_STORAGE_PATH`（环境变量，见 Step 2） |
| MinerU Skill | `$CLAUDE_SKILLS_PATH/mineru/` |
| Zotero Skill | `$ZOTERO_CODE_EXECUTION_PATH` |
| Lark-doc Skill | `$CLAUDE_SKILLS_PATH/lark-doc/` |
| Lark-shared Skill | `$CLAUDE_SKILLS_PATH/lark-shared/` |

## 注意事项

1. **Zotero路径配置**：必须设置 `ZOTERO_STORAGE_PATH` 环境变量指向你的Zotero存储位置（见 Step 2）
   - 查找方法：在Zotero首选项 → 高级 → 文件中找到数据目录路径
   - 完整路径应包含 `/storage/` 子目录
2. **PDF大小**：超过10MB需使用 `extract` 而非 `flash-extract`
3. **Token配置**：MinerU extract需要配置token（`mineru-open-api auth`）
4. **文件编码**：中文内容确保UTF-8编码
5. **飞书文档**：创建后文档自动添加到当前用户空间
