# 数学论文分析技能

基于 arXiv-Paper-Assistant 项目的核心功能，专为数学学习者和研究人员设计的数学论文结构化分析技能。

## 功能特性

### 三级分析模式

- **快速模式**: 仅正则提取，无需LLM，<30秒完成
- **标准模式**: 正则+LLM精炼，建立定理-证明关联
- **深度模式**: 完整七维分析，生成学习报告

### 核心能力

- 数学公式OCR提取（保留LaTeX）
- 章节、定理、定义、证明结构化提取
- 定理-证明关联关系建立
- 七维摘要生成（标题、摘要、证明思路、核心方法、三维标签）
- Markdown格式结构化输出

## 快速开始

### 安装依赖

```bash
pip install pymupdf openai httpx
```

### 命令行使用

```bash
# 快速模式（无需LLM）
python scripts/cli.py your_paper.pdf --mode fast

# 标准模式（需要LLM）
python scripts/cli.py your_paper.pdf --mode standard \
  --llm-api-key YOUR_KEY \
  --llm-base-url https://api.openai.com/v1

# 深度模式
python scripts/cli.py your_paper.pdf --mode deep \
  --llm-api-key YOUR_KEY \
  --llm-base-url https://api.openai.com/v1
```

### Python API使用

```python
from scripts.paper_analyzer import MathPaperAnalyzer

analyzer = MathPaperAnalyzer(
    llm_api_key="your-key",
    llm_base_url="https://api.openai.com/v1",
    llm_model="gpt-4o",
)

results = analyzer.analyze_paper(
    pdf_path="paper.pdf",
    mode="deep",
    save_output=True,
)

print(results["output"]["full_report"])
```

## 输出示例

### 快速模式输出

```markdown
# 数学论文结构分析

## 基本信息

- **论文**: graph_theory.pdf
- **分析模式**: fast
- **总页数**: 12 页
- **分析耗时**: 35.1 秒

## 论文结构

### 章节结构

- **sec1** Introduction (p.1)
- **sec2** Preliminaries (p.3)

### 定理/引理

- **Theorem 3.1** (p.5): Every connected graph contains a spanning tree...

### 定义

- **Definition 2.1** (p.3): A graph G = (V, E) consists of...

### 证明

- prf_p5_120 (p.5-6) → thm3.1

### 关键公式

- (p.6) $|E| = n - 1$ (for trees)
```

### 深度模式额外输出

```markdown
## 论文摘要

本文研究了连通图中生成树的存在性问题...

## 分类标签

- **领域**: 图论, 组合数学
- **内容**: 生成树存在性, 树的性质
- **方法**: 归纳法, 构造性证明

## 核心方法

1. 数学归纳法
2. 反证法

## 证明思路

- **Theorem 3.1**: 通过对顶点数进行归纳，构造生成树...
```

## 文件结构

```
math-paper-analyzer/
├── SKILL.md                    # 技能核心说明
├── README.md                   # 本文件
├── requirements.txt            # 依赖列表
├── scripts/
│   ├── ocr_pdf_processor.py    # OCR PDF处理
│   ├── structure_analyzer.py   # 结构分析器
│   ├── paper_analyzer.py       # 统一处理管道
│   ├── cli.py                  # 命令行接口
│   └── test_analyzer.py        # 测试脚本
├── references/
│   └── structure_schema.md     # 数据结构参考
├── templates/                  # 输出模板
└── examples/
    └── sample_analysis.md      # 示例分析报告
```

## 配置说明

### 必需配置

1. **OCR API**: 默认使用 `https://edusys5.sii.edu.cn/ocr`
   - 可通过环境变量 `MATH_PAPER_OCR_URL` 修改

2. **Python依赖**: `pymupdf`, `openai`, `httpx`

### 可选配置（标准/深度模式）

1. **LLM服务**: OpenAI兼容接口
   - 环境变量: `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL`
   - 或通过参数传递

## 测试

运行测试套件：

```bash
python scripts/test_analyzer.py
```

## 作为技能使用

本技能设计为 Claude Code 技能，当用户需要：

- 分析数学论文结构
- 提取定理、定义、证明
- 理解证明思路和方法
- 生成学习材料

时自动触发。

## 许可证

基于原 arXiv-Paper-Assistant 项目，遵循相应许可证。
