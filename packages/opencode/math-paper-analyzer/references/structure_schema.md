# 数据结构参考

## 结构提取输出格式

### 基础结构

```json
{
  "title": "论文标题（LLM精炼后）",
  "summary": "1-2句概要（LLM精炼后）",
  "sections": [...],
  "theorems": [...],
  "proofs": [...],
  "definitions": [...],
  "key_equations": [...]
}
```

### 章节 (Section)

```json
{
  "id": "sec1", // 章节ID，如 sec1, sec2.1
  "title": "Introduction", // 章节标题
  "level": 1, // 层级，1=一级标题，2=二级标题
  "page": 1 // 起始页码
}
```

### 定理/引理 (Theorem/Lemma)

```json
{
  "id": "thm3.1", // 定理ID
  "label": "Theorem 3.1", // 显示标签
  "type": "theorem", // 类型：theorem/lemma/proposition/corollary
  "statement": "Every connected graph...", // 定理陈述
  "section_id": "sec3", // 所属章节ID
  "page": 5 // 所在页码
}
```

### 证明 (Proof)

```json
{
  "id": "prf_p5_120", // 证明ID
  "proves": "thm3.1", // 证明的定理ID
  "page_start": 5, // 起始页码
  "page_end": 6 // 结束页码
}
```

### 定义 (Definition)

```json
{
  "id": "def2.1", // 定义ID
  "label": "Definition 2.1", // 显示标签
  "content": "A graph G = (V, E)...", // 定义内容
  "section_id": "sec2", // 所属章节ID
  "page": 3 // 所在页码
}
```

### 关键公式 (Key Equation)

```json
{
  "id": "eq_p8_50", // 公式ID
  "latex": "|E| = \\frac{1}{2}\\sum_{v\\in V} \\deg(v)", // LaTeX公式
  "page": 8 // 所在页码
}
```

## 摘要输出格式

### 七维摘要

```json
{
  "title": "论文标题",
  "abstract": "1-2段中文概述论文的主要研究内容和贡献...",
  "proof_approaches": {
    "Theorem 3.1": "通过构造性证明，首先假设...",
    "Lemma 3.2": "利用归纳法，对顶点数进行归纳..."
  },
  "core_techniques": ["数学归纳法", "反证法", "构造性证明"],
  "field_tags": ["图论", "组合数学"],
  "content_tags": ["生成树存在性", "树的性质"],
  "technique_tags": ["归纳法", "极值原理"]
}
```

### 标签说明

1. **field_tags** (领域标签): 论文所属数学分支
   - 如: ["图论", "组合数学", "数论", "代数几何"]

2. **content_tags** (内容标签): 研究的具体问题
   - 如: ["生成树存在性", "匹配问题", "素数分布"]

3. **technique_tags** (方法标签): 使用的数学方法
   - 如: ["归纳法", "反证法", "概率方法", "代数方法"]

## 正则表达式模式

### 章节匹配

```regex
^(?:#{1,3}\s+)?(\d+(?:\.\d+)*)\.?\s+(.+)
```

匹配: `1. Introduction`, `2.1 Preliminaries`

### 定理匹配

```regex
(?P<type>Theorem|Lemma|Proposition|Corollary|定理|引理|命题|推论)\s+(?P<label>[\d.]+)[.:\s]*(?P<statement>[^\n]*)
```

匹配: `Theorem 3.1: Every connected graph...`

### 证明匹配

```regex
(?P<keyword>Proof|证明)[.\s:]*
```

匹配: `Proof.` 或 `证明：`

### 定义匹配

```regex
(?P<type>Definition|定义)\s+(?P<label>[\d.]+)[.:\s]*(?P<content>[^\n]*)
```

匹配: `Definition 2.1: A graph G = (V, E)...`

### 公式匹配

```regex
\$\$(.+?)\$\$|\\\[(.+?)\\]
```

匹配: `$$E = mc^2$$` 或 `\[ \sum_{i=1}^n i = \frac{n(n+1)}{2} \]`

## 处理流程

### 快速模式流程

```
PDF文件
    ↓
OCR处理（提取文本+公式）
    ↓
正则结构提取
    ↓
生成基础Markdown报告
```

### 标准模式流程

```
PDF文件
    ↓
OCR处理
    ↓
正则结构提取
    ↓
LLM结构精炼（修正、关联、补充）
    ↓
生成详细Markdown报告
```

### 深度模式流程

```
PDF文件
    ↓
OCR处理
    ↓
正则结构提取
    ↓
LLM结构精炼
    ↓
LLM摘要生成（七维信息）
    ↓
生成完整学习报告
```

## 错误代码

### OCR错误

- `OCR_API_UNAVAILABLE`: OCR服务不可用
- `OCR_TIMEOUT`: OCR请求超时
- `OCR_EMPTY_RESULT`: OCR返回空结果

### 结构提取错误

- `REGEX_NO_MATCH`: 正则未匹配到结构
- `LLM_REFINEMENT_FAILED`: LLM精炼失败
- `JSON_PARSE_ERROR`: JSON解析错误

### 摘要生成错误

- `LLM_SUMMARY_FAILED`: LLM摘要生成失败
- `INSUFFICIENT_CONTENT`: 内容不足生成摘要

### 文件处理错误

- `PDF_CORRUPTED`: PDF文件损坏
- `FILE_NOT_FOUND`: 文件不存在
- `PERMISSION_DENIED`: 权限不足

## 性能指标

### 处理时间（10页论文）

| 模式 | OCR时间 | 结构提取 | 摘要生成 | 总时间   |
| ---- | ------- | -------- | -------- | -------- |
| 快速 | 20-30s  | 5-10s    | -        | 25-40s   |
| 标准 | 20-30s  | 30-60s   | -        | 50-90s   |
| 深度 | 20-30s  | 30-60s   | 60-120s  | 110-210s |

### 内存使用

- OCR处理: 100-200MB（取决于PDF大小）
- 结构提取: 50-100MB
- LLM调用: 依赖模型大小
- 峰值内存: 200-300MB

### 输出文件大小

- Markdown报告: 10-50KB
- JSON原始数据: 20-100KB
- 临时文件: 50-200MB（自动清理）
