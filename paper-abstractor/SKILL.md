---
name: paper-abstractor
description: 给定一组DOI号，逐一访问原始文献，提取并翻译摘要内容，最终整理成格式化报告。支持批量处理，生成中文学术文献综述。
---

# Paper Abstractor / 论文摘要提取器

## Skill Overview

本Skill通过分层API策略自动化检索学术文献摘要，并生成结构化的中文报告。主要流程为：
1. **解析输入**: 接受单个或批量DOI列表
2. **分层检索**: 按优先级从多个API（Crossref → PubMed → Semantic Scholar）获取元数据和摘要
3. **多语言处理**: 自动将英文摘要翻译为中文
4. **报告生成**: 整合所有信息生成统一的Markdown格式报告

---

## 1. Core Architecture

### 1.1 API层次结构
系统采用三层API分层策略，确保信息覆盖率和检索成功率：

```
输入DOI → 第一层(Crossref API)
          ├─ 摘要存在? ✅ → 返回
          └─ 无摘要? ❌ → 第二层(PubMed E-utilities)
                     ├─ 查询成功? ✅ → 返回
                     └─ 失败? ❌ → 第三层(Semantic Scholar API)
                                ├─ API Key认证成功? ✅ → 返回
                                └─ 失败? ❌ → 返回空摘要标记
```

### 1.2 数据流转流程

```
DOI输入
  ↓
[验证阶段] - 格式检查(10.xxxx/xxxxx)
  ↓
[检索阶段] - 分层API调用 + 缓存管理
  ↓
[处理阶段] - 英→中翻译 + 数据格式化
  ↓
[汇总阶段] - 生成单一Markdown报告
  ↓
输出报告
```

---

## 2. Input Formats / 输入格式

系统支持多种DOI输入方式：

### 2.1 单个DOI查询
```
10.1038/nature12373
```

### 2.2 批量列表 (markdown列表)
```
- 10.1038/nature12373
- 10.1016/j.cell.2021.01.001
- 10.1038/nature11226
```

### 2.3 批量列表 (逗号分隔)
```
10.1038/nature12373, 10.1016/j.cell.2021.01.001, 10.1038/nature11226
```

### 2.4 引用格式 (带DOI)
```
Smith et al. (2021) doi:10.1038/nature12373; Johnson et al. (2020) http://doi.org/10.1016/j.cell.2020.01.001
```

---

## 3. API Reference / API参考

### 3.1 Crossref API (第一优先级)

**特性**:
- 覆盖率: ~1.8亿条记录
- 费用: 完全免费
- 认证: 可选（建议提供邮箱作为politeness参数）
- 速率限制: 无限制
- 摘要覆盖率: ~75%

**端点**:
```
https://api.crossref.org/works/{DOI}?mailto={email}
```

**请求示例**:
```python
import requests

def query_crossref(doi: str) -> dict:
    """
    从Crossref检索论文元数据
    
    Args:
        doi: DOI号，可带或不带"DOI:"前缀
        
    Returns:
        {
            'title': str,           # 论文标题
            'abstract': str,        # 摘要（可能为None）
            'authors': list,        # 作者列表
            'journal': str,         # 期刊名称
            'year': int,            # 发表年份
            'volume': str,          # 卷号
            'issue': str,           # 期号
            'pages': str,           # 页码
            'publisher': str,       # 出版社
            'url': str              # DOI网址
        }
    """
    doi_clean = doi.replace("DOI:", "").replace("doi:", "").strip()
    url = f"https://api.crossref.org/works/{doi_clean}"
    
    try:
        response = requests.get(url, params={'mailto': 'your@email.com'})
        if response.status_code == 200:
            msg = response.json().get('message', {})
            return {
                'title': (msg.get('title') or [None])[0],
                'abstract': msg.get('abstract'),
                'authors': [a.get('name') for a in msg.get('author', [])],
                'journal': (msg.get('container-title') or [None])[0],
                'year': msg.get('published-online', {}).get('date-parts', [[None]])[0][0],
                'volume': msg.get('volume'),
                'issue': msg.get('issue'),
                'pages': msg.get('page'),
                'publisher': msg.get('publisher'),
                'url': f"https://doi.org/{doi_clean}",
                'source': 'Crossref'
            }
    except Exception as e:
        return {'error': str(e)}
    return None
```

### 3.2 PubMed E-utilities API (第二优先级)

**特性**:
- 覆盖范围: 生物医学文献（~3400万篇）
- 费用: 免费
- 认证: API Key可选（建议申请以获得更高速率限制）
- 速率限制: 3 RPS（无Key）, 10 RPS（有Key）
- 专长: 生医领域，摘要通常完整

**两步查询流程**:
```python
def query_pubmed(doi: str) -> dict:
    """
    通过DOI在PubMed查询，获取生医论文信息
    """
    import requests
    import xml.etree.ElementTree as ET
    
    doi_clean = doi.replace("DOI:", "").strip()
    
    # 步骤1: 通过DOI查找PubMed ID
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        'db': 'pubmed',
        'term': f'{doi_clean}[DOI]',
        'rettype': 'json'
    }
    
    search_resp = requests.get(search_url, params=search_params)
    pmids = search_resp.json()['esearchresult'].get('idlist', [])
    
    if not pmids:
        return None
    
    pmid = pmids[0]
    
    # 步骤2: 通过PMID获取详细信息
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        'db': 'pubmed',
        'id': pmid,
        'rettype': 'xml'
    }
    
    fetch_resp = requests.get(fetch_url, params=fetch_params)
    root = ET.fromstring(fetch_resp.content)
    
    # 解析XML
    article = root.find('.//Article')
    if article:
        return {
            'title': article.findtext('ArticleTitle'),
            'abstract': article.findtext('.//AbstractText'),
            'journal': article.findtext('.//Journal/Title'),
            'year': int(article.findtext('.//PubDate/Year') or 0),
            'pmid': pmid,
            'source': 'PubMed'
        }
    
    return None
```

### 3.3 Semantic Scholar API (第三优先级与补充)

**特性**:
- 覆盖率: 2.14亿篇论文
- 费用: 免费（需API Key）
- 认证: 必需（免费申请: https://www.semanticscholar.org/product/api）
- 速率限制: 1 RPS (需升级获得更高限制)
- 特色: AI生成的论文摘要、引用计数、开放获取检测

**端点**:
```
https://api.semanticscholar.org/graph/v1/paper/DOI:{DOI}
```

**请求示例**:
```python
def query_semantic_scholar(doi: str, api_key: str = None) -> dict:
    """
    从Semantic Scholar检索高质量的论文信息和AI生成摘要
    """
    import requests
    
    doi_clean = doi.replace("DOI:", "").strip()
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi_clean}"
    
    headers = {}
    if api_key:
        headers['x-api-key'] = api_key
    
    params = {
        'fields': 'title,abstract,authors,citationCount,venue,'
                  'publicationDate,openAccessPdf,tldr,isOpenAccess'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'title': data.get('title'),
                'abstract': data.get('abstract'),
                'ai_summary': data.get('tldr', {}).get('text'),  # AI生成的简要摘要
                'authors': [a.get('name') for a in data.get('authors', [])],
                'citations': data.get('citationCount'),
                'venue': data.get('venue'),
                'year': int(data.get('publicationDate', '0')[:4]) if data.get('publicationDate') else None,
                'is_open_access': data.get('isOpenAccess'),
                'pdf_url': data.get('openAccessPdf', {}).get('url'),
                'source': 'Semantic Scholar'
            }
    except Exception as e:
        return {'error': str(e)}
    
    return None
```

---

## 4. Processing Pipeline / 处理流程

### 4.1 DOI验证与正规化

```python
import re

def validate_and_normalize_doi(doi_input: str) -> str | None:
    """
    验证和正规化DOI格式
    
    Valid formats:
    - 10.1038/nature12373
    - DOI: 10.1038/nature12373
    - doi:10.1038/nature12373
    - http://doi.org/10.1038/nature12373
    - https://doi.org/10.1038/nature12373
    """
    # 移除常见前缀
    cleaned = re.sub(r'^(DOI:|doi:|http[s]?://)?(?:dx\.)?doi\.org/', '', doi_input.strip())
    
    # 验证DOI格式：必须以10.开头，后跟注册号和后缀
    if re.match(r'^10\.\S+/\S+$', cleaned):
        return cleaned
    
    return None
```

### 4.2 分层检索策略

```python
def retrieve_paper_metadata(doi: str, semantic_scholar_key: str = None) -> dict:
    """
    按优先顺序尝试从多个API检索论文信息
    
    Strategy:
    1. Try Crossref first (fastest, no auth needed)
    2. If no abstract, try PubMed (good for biomedical)
    3. If still missing, try Semantic Scholar (most comprehensive)
    4. Fallback: Return minimal info with note
    """
    
    # 第一层：Crossref
    result = query_crossref(doi)
    if result and result.get('abstract'):
        return {**result, 'retrieval_stage': 'Stage 1 (Crossref)'}
    
    # 第二层：PubMed
    pubmed_result = query_pubmed(doi)
    if pubmed_result and pubmed_result.get('abstract'):
        return {**pubmed_result, 'retrieval_stage': 'Stage 2 (PubMed)'}
    
    # 合并Crossref和PubMed的结果（优先Crossref的元数据）
    if result:
        merged = {**result, 'retrieval_stage': 'Stage 1+2 (Crossref+PubMed)'}
        if pubmed_result and pubmed_result.get('abstract') and not result.get('abstract'):
            merged['abstract'] = pubmed_result.get('abstract')
        return merged
    
    # 第三层：Semantic Scholar
    ss_result = query_semantic_scholar(doi, semantic_scholar_key)
    if ss_result and ss_result.get('abstract'):
        return {**ss_result, 'retrieval_stage': 'Stage 3 (Semantic Scholar)'}
    
    # 后备方案
    return {
        'doi': doi,
        'abstract': '【摘要获取失败】',
        'retrieval_stage': 'Failed - No source available',
        'error': True
    }
```

### 4.3 英文到中文的翻译

```python
def translate_to_chinese(text: str) -> str:
    """
    使用Claude完整的中文翻译功能
    
    Requirements:
    - 保留所有科学术语的准确性
    - 保留方程式、专业名词的英文形式（如需要）
    - 维持原始表达式的学术严谨性
    """
    # 本函数在Skill执行时由Claude直接处理
    # 不需要额外API调用，利用Claude自身的翻译能力
    pass
```

### 4.4 数据去重与合并

```python
def deduplicate_dois(doi_list: list) -> list:
    """
    去除重复的DOI并准确化格式
    """
    seen = set()
    normalized = []
    
    for doi in doi_list:
        normalized_doi = validate_and_normalize_doi(doi)
        if normalized_doi and normalized_doi not in seen:
            seen.add(normalized_doi)
            normalized.append(normalized_doi)
    
    return normalized
```

---

## 5. Output Format / 输出格式

生成的报告为单一Markdown文件，包含所有论文的汇总信息。

### 5.1 报告结构

```markdown
# 文献列表总结报告
生成时间: 2026-03-23
处理论文数: 15
成功检索: 14
失败/部分检索: 1

---

## 📊 数据统计
- 总论文数: 15
- 完整元数据: 14 (93%)
- 仅有摘要: 12 (80%)
- 完全失败: 1 (7%)

---

## 📑 论文摘要总览

### 1. 论文标题
**期刊**: Nature Genetics | **年份**: 2021 | **DOI**: 10.1038/nature12373
**作者**: John Smith, Jane Doe
**来源**: Crossref
**检索状态**: ✅ 完整

**【原文摘要】**
Title abstract in English...

**【中文摘要】**
英文摘要的中文翻译...

**【简要总结】**
- 主要贡献：...
- 关键发现：...
- 研究方法：...

---

### 2. 论文标题
...

---

## 📌 汇总与分析

### 按学科分类
- 分子生物学：8篇
- 计算机科学：5篇
- 物理学：2篇

### 高引用论文 (引用次数 > 1000)
- 论文1: 2354次引用
- 论文2: 1876次引用

### 开放获取论文
- 开放获取论文数: 7篇 (47%)
- 仅限订阅: 8篇 (53%)

---

## ⚠️  检索失败清单
1. DOI: 10.xxxx/xxxxx - 原因：该DOI无法在任何数据库中找到
```

### 5.2 单篇论文的详细格式

每篇论文遵循以下格式：

```markdown
### {序号}. {论文标题}

**基本信息**
- 期刊/会议：{journal_name}
- 年份：{year}
- DOI：{doi_link}
- 作者：{author1}, {author2}, ...
- 卷号：{volume} | 期号：{issue} | 页码：{pages}

**检索信息**
- 数据来源：{Crossref/PubMed/Semantic Scholar}
- 检索成功率：{retrieval_stage}

**原文摘要** (English)
{original_abstract}

**中文摘要**
{chinese_translation}

**补充信息** (若有)
- 引用次数：{citation_count}（Semantic Scholar）
- 开放获取：{是/否}
- PDF链接：{pdf_url}
```

---

## 6. Execution Workflow / 执行工作流

### 6.1 用户使用流程

1. **输入**: 提供DOI列表（单个或批量）
2. **配置**: （可选）提供Semantic Scholar API Key以获得更好的覆盖率
3. **执行**: 系统自动调用本Skill
4. **处理**: 分层检索 → 数据验证 → 中文翻译 → 报告生成
5. **输出**: 生成完整的Markdown报告文件

### 6.2 处理流程（详细步骤）

```
Step 1: 解析输入
  └─ 识别输入类型（单个DOI/列表/引用格式）
  └─ DOI格式验证与正规化
  └─ 去重处理

Step 2: 分批检索
  └─ Batch Size: 5-10 (避免API限制)
  └─ 并发调用: Crossref (无限制) + PubMed (3 RPS) + SS (1 RPS)
  └─ 缓存管理: 缓存已检索的结果
  └─ 错误重试: 指数退避策略

Step 3: 数据处理
  └─ 统一元数据格式
  └─ 摘要完整性检查
  └─ 英文内容识别

Step 4: 批量翻译
  └─ 按照科学术语保留规则翻译
  └─ 注意保留化学式、数学公式等

Step 5: 报告生成
  └─ 汇总统计数据
  └─ 按照指定格式生成Markdown
  └─ 生成检索失败清单

Step 6: 输出
  └─ 生成单一Markdown文件
  └─ 文件名: `文献列表总结_{timestamp}.md`
```

---

## 7. Error Handling / 错误处理

### 7.1 常见错误场景

| 错误类型 | 原因 | 处理方案 |
|--------|------|--------|
| Invalid DOI | 格式不符 | 返回验证错误，列出正确格式 |
| API Timeout | 网络问题 | 重试最多3次，间隔指数增长 |
| Rate Limit | API速率限制 | 队列等待，优先级调整 |
| No Result | DOI不存在 | 标记为失败，继续处理其他 |
| Partial Data | 仅找到元数据 | 标记为"部分成功"，继续下一层 |
| Translation Error | 翻译失败 | 保留英文，标注翻译缺失 |

### 7.2 重试策略

```python
def retry_with_exponential_backoff(func, doi, max_retries=3):
    """
    带指数退避的重试机制
    """
    import time
    
    for attempt in range(max_retries):
        try:
            return func(doi)
        except Exception as e:
            if attempt == max_retries - 1:
                return None
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
    
    return None
```

---

## 8. Configuration / 配置参数

用户可选配置：

```yaml
# API配置
api:
  crossref:
    email: "your@email.com"  # 可选，但建议提供
    enabled: true
  
  pubmed:
    api_key: null            # 可选，无Key时速率低
    enabled: true
  
  semantic_scholar:
    api_key: null            # 可选，无Key时无法使用
    enabled: true

# 处理配置
processing:
  batch_size: 5              # 每批检索数量
  max_retries: 3             # 失败重试次数
  timeout_per_doi: 10        # 每个DOI的超时（秒）
  
# 输出配置
output:
  language: "chinese"        # chinese / english / bilingual
  include_pdf_links: true    # 包含开放获取PDF链接
  include_citations: true    # 包含引用计数
  output_format: "single_file"  # single_file（默认）
```

---

## 9. Performance Considerations / 性能考虑

### 9.1 缓存策略

```python
# 本地缓存机制
cache = {
    'doi': {
        'metadata': {...},
        'timestamp': 1711182000,
        'ttl': 2592000  # 30天过期
    }
}

# 缓存检查：在API调用前检查，避免重复查询
```

### 9.2 并发控制

- **Crossref**: 无限制，可平行调用所有请求
- **PubMed**: 3 RPS限制，使用队列顺序处理
- **Semantic Scholar**: 1 RPS限制，严格序列化

建议总处理流程：
- 小规模（1-10个DOI）: 直接串行处理，< 30秒
- 中等规模（11-50个DOI）: 混合并发，< 2分钟
- 大规模（50+个DOI）: 完全并发+队列，< 5分钟

### 9.3 翻译优化

适用于大量文本的批量翻译策略：
- 分段翻译（每个摘要独立）
- 保留术语词表（减少重复翻译）
- 缓存单个句子的翻译结果

---

## 10. Success Criteria / 成功标准

一份高质量的文献列表总结报告应满足：

✅ **完整性**
- [ ] 所有DOI都经过解析和验证
- [ ] 所有未检索的DOI都被标记并说明原因
- [ ] 覆盖度 ≥ 90%（至少90%的DOI成功检索）

✅ **准确性**
- [ ] 元数据完全来自可信API，无任何hallucination
- [ ] 所有摘要都是原始内容，无篡改
- [ ] 中文翻译准确，科学术语符合学科规范

✅ **可用性**
- [ ] 报告结构清晰，易于浏览和检索
- [ ] 每篇论文附带完整出处（DOI链接）
- [ ] 汇总统计数据正确且有价值

✅ **可维护性**
- [ ] 代码注释完整
- [ ] 错误日志详细
- [ ] 支持增量更新（添加新DOI到现有报告）

---

## 附录：快速参考

### API选择决策树

```
有Semantic Scholar API Key?
├─ YES → 优先使用SS (最全面)，再用Crossref充填
└─ NO  → Crossref优先 → PubMed补充 → 手动SS查询
```

### DOI提取正则表达式

```regex
\b(10\.\S+/\S+)\b
```

### 摘要长度建议

- 最小长度: 50字符（标记为"摘要过短"）
- 典型长度: 150-300字符
- 最大长度: 2000字符（某些综述）
- 中文翻译通常比英文长20-30%

---

## 参考资源

- **Crossref API文档**: https://github.com/CrossRef/rest-api-doc
- **PubMed E-utilities**: https://www.ncbi.nlm.nih.gov/books/NBK25497/
- **Semantic Scholar API**: https://www.semanticscholar.org/product/api
- **DOI**: https://www.doi.org/
