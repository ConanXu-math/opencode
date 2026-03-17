---
name: math-paper-analyzer
description: 数学论文结构化分析技能，为数学学习者和研究人员提供深度论文分析，提取定理、定义、证明思路、核心方法等多维信息，输出结构化Markdown报告。使用此技能当用户需要分析数学论文、提取结构化信息、理解证明思路或生成学习材料时。
compatibility:
  tools: [bash, read, write, glob, grep]
  dependencies: [python, pymupdf, openai, httpx]
---

# 数学论文分析技能

## 概述

本技能基于 arXiv-Paper-Assistant 项目的核心功能，专为数学学习者和研究人员设计，提供深度数学论文结构化分析。通过 OCR 提取数学公式，两阶段（正则+LLM）结构分析，生成包含定理、定义、证明思路、核心方法等多维信息的结构化报告。

## 核心功能

### 三级分析模式

1. **快速模式**：仅正则提取（无 LLM，<30秒）
   - 提取章节、定理、定义、证明、关键公式
   - 适合快速浏览和基本结构了解

2. **标准模式**：正则+LLM 结构精炼（1-3分钟）
   - 修正正则结果，建立定理-证明关联
   - 补充论文标题和概要
   - 标注章节归属关系

3. **深度模式**：完整七维分析（3-5分钟）
   - 生成高层摘要和三维标签
   - 分析证明思路和核心技巧
   - 输出完整学习报告

### 输出内容

- **基本信息**：标题、页数、分析模式
- **章节结构**：层级化章节标题和页码
- **定理/引理**：定理陈述、类型、所属章节
- **定义**：数学定义内容
- **证明**：证明范围、关联定理
- **关键公式**：LaTeX 公式提取
- **七维摘要**（深度模式）：
  - 论文摘要（1-2段）
  - 证明思路分析
  - 核心方法列表
  - 领域/内容/方法三维标签

## 使用场景

### 应该触发此技能的场景

- 用户说"帮我分析这篇数学论文"
- 用户询问"这篇论文的主要定理是什么"
- 用户需要"提取论文中的定义和公式"
- 用户想要"理解证明思路和方法"
- 用户需要"生成论文的结构化摘要"
- 用户说"这篇论文用了哪些数学技巧"
- 用户需要"为学习准备材料"

### 不应该触发此技能的场景

- 非数学论文的分析
- 简单的文本摘要（不需要结构化分析）
- 代码分析或编程问题
- 图像或图表分析（仅文本和公式）

## 自动配置

### 零配置启动

技能会自动检测和配置所需环境：

1. **自动依赖安装**：首次使用时自动安装 Python 依赖
2. **环境变量检测**：自动检测 `OPENAI_API_KEY` 等环境变量
3. **交互式设置**：缺少配置时提供友好的交互式设置向导
4. **智能降级**：根据可用资源自动选择最佳分析模式

### 配置检测顺序

1. 检查 Python 依赖，自动安装缺失包
2. 检测环境变量中的 LLM 配置
3. 如果 LLM 不可用，自动降级到快速模式
4. 提供交互式配置选项

### 手动配置（可选）

如需手动配置，可运行：

```bash
python scripts/interactive_setup.py
```

## 使用方法

### 作为技能使用（推荐）

当技能触发时，完全自动化工作：

1. **自动检测**：检查系统配置和依赖
2. **交互引导**：如果需要配置，提供友好的交互式设置
3. **智能分析**：根据可用资源选择最佳分析模式
4. **自动处理**：执行 OCR → 结构提取 → 摘要生成
5. **结果展示**：生成并显示分析报告，保存到默认位置

### 一键式命令行使用

```bash
# 完全自动（推荐）
python scripts/auto_analyzer.py paper.pdf

# 指定模式
python scripts/auto_analyzer.py paper.pdf deep

# 交互式设置
python scripts/interactive_setup.py
```

### 传统命令行（手动配置）

```bash
# 快速模式
python scripts/cli.py paper.pdf --mode fast

# 标准/深度模式（需要预先配置）
python scripts/cli.py paper.pdf --mode standard
```

### Python API 使用（自动配置）

```python
from scripts.auto_analyzer import AutoMathPaperAnalyzer

# 创建自动分析器（零配置）
analyzer = AutoMathPaperAnalyzer()

# 分析论文（自动检测和配置）
results = analyzer.analyze("paper.pdf", mode="deep")

if "error" in results:
    print(f"Error: {results['error']}")
else:
    report = results["output"]["full_report"]
    print(report)
```

### 传统 Python API（手动配置）

```python
from scripts.paper_analyzer import MathPaperAnalyzer

# 手动配置分析器
analyzer = MathPaperAnalyzer(
    llm_api_key="your-key",
    llm_base_url="https://api.openai.com/v1",
    llm_model="gpt-4o",
)

# 分析论文
results = analyzer.analyze_paper(
    pdf_path="paper.pdf",
    mode="deep",
    save_output=True,
)
```

## 输出示例

### 快速/标准模式输出

```markdown
# 数学论文结构分析

## 基本信息

- **论文**: graph_theory_paper.pdf
- **分析模式**: standard
- **总页数**: 15 页
- **分析耗时**: 45.2 秒

## 论文结构

### 章节结构

- **sec1** Introduction (p.1)
- **sec2** Preliminaries (p.3)
  - **sec2.1** Basic Definitions (p.3)
  - **sec2.2** Graph Properties (p.4)

### 定理/引理

- **Theorem 3.1** (p.5): Every connected graph contains a spanning tree...
- **Lemma 3.2** (p.6): If G is a tree with n vertices, then it has n-1 edges...

### 定义

- **Definition 2.1** (p.3): A graph G = (V, E) consists of...
- **Definition 2.2** (p.4): The degree of a vertex v is...

### 证明

- prf_p5_120 (p.5-6) → thm3.1
- prf_p6_80 (p.6-7) → lem3.2

### 关键公式

- (p.8) $|E| = \frac{1}{2}\sum_{v\in V} \deg(v)$
```

### 深度模式输出（额外内容）

```markdown
## 论文摘要

本文研究了连通图中生成树的存在性问题，提出了基于归纳法的新证明...

## 分类标签

- **领域**: 图论, 组合数学
- **内容**: 生成树存在性, 树的性质
- **方法**: 归纳法, 构造性证明

## 核心方法

1. 数学归纳法
2. 反证法
3. 极值原理

## 证明思路

- **Theorem 3.1**: 通过对顶点数进行归纳，构造生成树...
- **Lemma 3.2**: 利用树的性质和握手引理推导边数公式...
```

## 文件结构

```
math-paper-analyzer/
├── SKILL.md (本文件)
├── scripts/
│   ├── ocr_pdf_processor.py    # OCR PDF 处理
│   ├── structure_analyzer.py   # 结构分析器
│   ├── paper_analyzer.py       # 统一处理管道
│   └── cli.py                  # 命令行接口
├── references/
│   ├── structure_schema.md     # 数据结构参考
│   └── usage_examples.md       # 使用示例
├── templates/
│   ├── summary_template.md     # 摘要模板
│   └── analysis_template.md    # 分析模板
└── examples/
    └── sample_analysis.md      # 示例分析报告
```

## 错误处理

### 常见错误及解决

1. **OCR API 不可用**
   - 检查网络连接
   - 尝试备用 OCR 服务
   - 降级到文本提取模式

2. **LLM 服务错误**
   - 检查 API 密钥和 URL
   - 降级到快速模式
   - 提示用户配置 LLM

3. **PDF 处理失败**
   - 检查 PDF 文件完整性
   - 尝试降低 DPI 设置
   - 分页处理大型文件

4. **内存不足**
   - 自动分块处理
   - 清理临时文件
   - 提示用户使用更小文件

### 降级策略

- LLM 不可用 → 降级到快速模式
- OCR 失败 → 尝试文本提取
- 内存不足 → 分页处理
- 超时 → 返回部分结果

## 性能优化

### 处理速度

- **快速模式**: <30秒（10页论文）
- **标准模式**: 1-3分钟（10页论文）
- **深度模式**: 3-5分钟（10页论文）

### 内存使用

- 分页处理避免内存溢出
- 自动清理临时文件
- 流式处理大型 PDF

### 并行处理

- 多页 OCR 并行
- 结构提取与摘要生成并行
- 可配置工作线程数

## 扩展功能

### 已实现

- [x] 三级分析模式
- [x] 数学公式 OCR
- [x] 结构化提取
- [x] 七维摘要
- [x] Markdown 输出
- [x] 错误恢复

### 计划中

- [ ] 定理关系图谱
- [ ] 证明策略分类
- [ ] 符号表生成
- [ ] 多篇论文对比
- [ ] 学习路线图
- [ ] 练习问题生成

## 注意事项

### 数学公式处理

- 使用 OCR 保留 LaTeX 公式
- 支持行间公式 `$$...$$` 和 `\[...\]`
- 可能无法识别手写公式

### 论文类型限制

- 最适合数学、理论计算机科学论文
- 适用于包含定理、证明、定义的论文
- 对实验性论文效果有限

### 语言支持

- 主要支持英文数学论文
- 支持中英文混合内容
- 对非拉丁字符可能有限制

## 更新日志

### v1.0.0 (初始版本)

- 基于 arXiv-Paper-Assistant 核心功能
- 三级分析模式实现
- 完整的处理管道
- Markdown 报告生成
- 命令行接口

## 贡献指南

欢迎改进此技能：

1. 添加新的分析维度
2. 优化 OCR 准确率
3. 扩展数学领域支持
4. 改进错误处理
5. 添加测试用例

## 许可证

基于原 arXiv-Paper-Assistant 项目，遵循相应许可证。
