# 数学论文分析示例

## 示例1：快速模式分析

### 用户输入

```
请帮我快速分析这篇图论论文的基本结构
```

### 技能响应

```
我将为您分析这篇图论论文。请提供PDF文件路径，我将使用快速模式提取基本结构。
```

### 分析过程

```
=== 开始分析: graph_theory.pdf ===
模式: fast

[1/3] OCR 处理中...
[OCR] Processing 12 pages...
[OCR] Processed 5/12 pages
[OCR] Processed 10/12 pages
[OCR] Processed 12/12 pages
✓ OCR 完成: 12 页, 耗时 25.3秒

[2/3] 结构提取中...
✓ 结构提取完成:
  - 章节: 5
  - 定理/引理: 8
  - 定义: 6
  - 证明: 7
  - 关键公式: 4
  耗时 8.2秒

[3/3] 生成输出...
✓ 输出已保存到: /path/to/analysis
  - 完整报告: graph_theory_fast_analysis.md
  - 结构分析: graph_theory_structure.md
  - 原始数据: graph_theory_analysis.json

✓ 分析完成! 总耗时: 35.1秒
```

### 输出报告（摘要）

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
  - **sec2.1** Basic Definitions (p.3)
  - **sec2.2** Graph Properties (p.4)
- **sec3** Main Results (p.5)
- **sec4** Applications (p.9)
- **sec5** Conclusion (p.11)

### 定理/引理

- **Theorem 3.1** (p.5): Every connected graph contains a spanning tree...
- **Lemma 3.2** (p.6): If G is a tree with n vertices, then it has n-1 edges...
- **Corollary 3.3** (p.7): A graph with n vertices and more than n-1 edges must contain a cycle...
- **Proposition 3.4** (p.8): In any graph, the number of vertices with odd degree is even...

### 定义

- **Definition 2.1** (p.3): A graph G = (V, E) consists of a set V of vertices and a set E of edges...
- **Definition 2.2** (p.4): The degree of a vertex v is the number of edges incident to v...
- **Definition 2.3** (p.4): A path in a graph is a sequence of vertices where consecutive vertices are adjacent...
- **Definition 2.4** (p.4): A cycle is a path that starts and ends at the same vertex...

### 证明

- prf_p5_120 (p.5-6) → thm3.1
- prf_p6_80 (p.6-7) → lem3.2
- prf_p7_50 (p.7-8) → cor3.3
- prf_p8_30 (p.8-9) → prop3.4

### 关键公式

- (p.4) $\deg(v) = |\{e \in E : v \in e\}|$
- (p.6) $|E| = n - 1$ (for trees)
- (p.7) $\sum_{v \in V} \deg(v) = 2|E|$
- (p.8) $|\{v \in V : \deg(v) \text{ is odd}\}|$ is even

---

_分析完成时间: 2024-01-15 14:30:25_
_注: fast 模式仅提取基本结构，如需深度分析请使用 deep 模式_
```

## 示例2：深度模式分析

### 用户输入

```
我需要深度分析这篇代数几何论文，包括证明思路和核心方法
```

### 技能响应

```
我将为您进行深度分析。深度模式需要LLM服务，请确认已配置API密钥。
分析将包括：论文摘要、证明思路、核心方法、多维标签等。
```

### 分析过程

```
=== 开始分析: algebraic_geometry.pdf ===
模式: deep

[1/3] OCR 处理中...
[OCR] Processing 18 pages...
✓ OCR 完成: 18 页, 耗时 42.5秒

[2/3] 结构提取中...
✓ 结构提取完成:
  - 章节: 6
  - 定理/引理: 12
  - 定义: 9
  - 证明: 10
  - 关键公式: 7
  耗时 52.8秒

[3/3] 深度摘要生成中...
✓ 深度摘要完成:
  - 标题: On the Classification of Algebraic Varieties
  - 领域标签: 代数几何, 复几何
  - 核心方法: 5 个
  耗时 98.3秒

[4/4] 生成输出...
✓ 输出已保存到: /path/to/analysis
  - 完整报告: algebraic_geometry_deep_analysis.md
  - 结构分析: algebraic_geometry_structure.md
  - 深度摘要: algebraic_geometry_summary.md
  - 原始数据: algebraic_geometry_analysis.json

✓ 分析完成! 总耗时: 195.6秒

=== 时间统计 ===
ocr         : 42.5秒
structure   : 52.8秒
summary     : 98.3秒
output      : 2.0秒
total       : 195.6秒
```

### 输出报告（深度摘要部分）

```markdown
# 数学论文分析报告

## 基本信息

- **论文**: algebraic_geometry.pdf
- **分析模式**: deep
- **总页数**: 18 页
- **分析耗时**: 195.6 秒

## 论文摘要

本文研究了代数簇的分类问题，主要贡献在于提出了基于上同调群的新分类方法。通过引入广义的Hodge结构，作者证明了在特定条件下，代数簇的同构类完全由上同调环决定。这一结果推广了经典的Kodaira分类定理，为高维代数几何提供了新的工具。

## 分类标签

- **领域**: 代数几何, 复几何
- **内容**: 代数簇分类, Hodge结构, 上同调理论
- **方法**: 层上同调, 谱序列, 形变理论

## 核心方法

1. 层上同调理论
2. Hodge分解定理
3. 形变理论与障碍理论
4. 谱序列技术
5. 极小模型纲领

## 证明思路

### Theorem 4.1 (主要分类定理)

通过构造适当的Hodge滤过，证明代数簇的上同调环决定了其同构类。关键步骤包括：首先建立上同调群的Hodge结构，然后利用形变理论证明刚性，最后通过比较引理完成分类。

### Lemma 3.2 (上同调有限性)

利用层上同调的有限性定理，证明在紧致复流形上，上同调群是有限维的。证明基于Čech上同调和Leray谱序列。

### Proposition 5.3 (稳定性结果)

证明在小的形变下，代数簇的分类保持不变。使用Kuranishi理论构造万有形变空间，然后分析切空间上的障碍类。

## 详细结构

（结构分析部分与快速模式类似，但更详细）
```

## 示例3：标准模式分析

### 用户输入

```
分析这篇概率论论文，我需要知道定理和证明的关联关系
```

### 技能响应

```
我将使用标准模式分析，这会通过LLM精炼结构，建立定理-证明关联。
```

### 输出特点

- **定理-证明关联**: 明确标注每个证明对应的定理
- **章节归属**: 每个定理/定义标注所属章节
- **标题概要**: 自动提取论文标题和概要
- **修正错误**: 修正正则提取中的误识别

## 使用建议

### 选择分析模式

1. **快速模式** (fast)
   - 仅需基本结构了解
   - 没有LLM配置
   - 需要快速结果
   - 适合: 论文浏览、初步筛选

2. **标准模式** (standard)
   - 需要准确的结构信息
   - 需要定理-证明关联
   - 有LLM配置
   - 适合: 文献调研、笔记整理

3. **深度模式** (deep)
   - 需要全面理解论文
   - 需要摘要和标签
   - 有LLM配置且时间充足
   - 适合: 深入学习、研究分析

### 输出文件说明

1. `{paper}_{mode}_analysis.md` - 完整报告
2. `{paper}_structure.md` - 纯结构分析
3. `{paper}_summary.md` - 深度摘要（仅深度模式）
4. `{paper}_analysis.json` - 原始数据（用于程序处理）

### 性能提示

1. **大型论文**: 超过50页建议使用快速模式
2. **网络环境**: OCR需要稳定网络连接
3. **LLM配置**: 标准/深度模式需要正确配置
4. **内存使用**: 处理大型PDF时注意内存

## 常见问题

### Q: 快速模式和标准模式有什么区别？

A: 快速模式仅用正则提取，速度快但可能不准确；标准模式用LLM精炼，建立关联关系，更准确但需要LLM。

### Q: 深度模式比标准模式多了什么？

A: 深度模式额外生成：论文摘要、证明思路分析、核心方法列表、三维标签分类。

### Q: 需要什么配置？

A: 快速模式只需Python和PyMuPDF；标准/深度模式还需要LLM API配置。

### Q: 支持中文论文吗？

A: 支持，但数学公式提取效果可能因OCR服务而异。

### Q: 分析失败怎么办？

A: 尝试：1) 检查PDF文件完整性 2) 降低DPI设置 3) 使用快速模式 4) 分页处理
