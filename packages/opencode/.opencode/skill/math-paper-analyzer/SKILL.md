---
name: math-paper-analyzer
description: 数学论文结构化分析技能，为数学学习者和研究人员提供深度论文分析。自动提取论文的基本信息、定理定义、主要内容、证明思路、证明方法和技巧，生成结构化Markdown报告。使用此技能当用户需要分析数学论文、提取结构化信息、理解证明思路或生成学习材料时。
compatibility:
  tools: [bash, read, write, glob, grep]
  dependencies: [python, pymupdf, httpx, openai]
---

# 数学论文分析技能

## 概述

本技能基于 arXiv-Paper-Assistant 项目的核心功能，为数学学习者和研究人员提供专业的数学论文结构化分析。通过OCR提取数学公式，两阶段（正则+LLM）结构分析，生成包含多维标签的深度分析报告。

## 核心功能

### 1. 三级分析模式

- **快速模式**：仅OCR+正则提取（<30秒，无LLM依赖）
- **标准模式**：OCR+正则+LLM结构精炼（1-3分钟）
- **深度模式**：完整分析+LLM摘要生成（3-5分钟）

### 2. 结构化提取

- **章节结构**：自动识别多级章节标题
- **数学元素**：定理、引理、命题、推论、定义
- **证明分析**：证明段落、证明思路、核心方法
- **关键公式**：LaTeX显示数学公式提取

### 3. 多维标签系统

- **领域标签**：数学分支领域（图论、组合优化等）
- **内容标签**：研究的具体问题
- **方法标签**：使用的证明技巧和方法

### 4. 输出格式

- **Markdown报告**：结构化分析报告
- **JSON数据**：原始分析数据
- **学习材料**：适合教学和自学的格式

## 使用场景

### 应该触发此技能的场景

- "帮我分析这篇数学论文的主要定理和证明思路"
- "提取论文中的定义和关键公式"
- "生成这篇论文的结构化摘要"
- "这篇论文用了哪些证明技巧？"
- "为这篇论文生成学习笔记"
- "分析论文的创新点和贡献"
- "提取论文的章节结构和主要内容"

### 不应该触发此技能的场景

- 非数学论文的分析
- 简单的文本摘要（不需要结构化分析）
- 代码分析或编程问题
- 图像或视频内容分析

## 快速开始

### 1. 基本使用

```python
from scripts.paper_analyzer import PaperAnalyzer

# 创建分析器
analyzer = PaperAnalyzer()

# 快速分析（仅正则）
result = analyzer.analyze("paper.pdf", mode="fast")

# 标准分析（需要LLM配置）
result = analyzer.analyze("paper.pdf", mode="standard")

# 深度分析
result = analyzer.analyze("paper.pdf", mode="deep")

# 输出Markdown
print(result["markdown"])
```

### 2. 环境配置

```bash
# 复制环境配置
cp .env.example .env

# 编辑 .env 文件
# 配置OCR和LLM服务
```

### 3. 命令行使用

```bash
# 安装依赖
pip install -r requirements.txt

# 快速分析
python -m scripts.paper_analyzer paper.pdf --mode fast

# 标准分析（需要配置LLM）
python -m scripts.paper_analyzer paper.pdf --mode standard \
  --llm-api-key sk-xxx --llm-base-url https://api.openai.com/v1 --llm-model gpt-4o

# 保存输出到指定目录
python -m scripts.paper_analyzer paper.pdf --mode deep --output-dir ./analysis
```

## 配置说明

### 必需配置

1. **OCR服务**：默认使用 `https://edusys5.sii.edu.cn/ocr`
2. **PyMuPDF**：PDF渲染库，用于OCR预处理

### 可选配置（标准/深度模式）

1. **LLM服务**：OpenAI兼容API
2. **环境变量**：支持 `.env` 文件配置

### 环境变量

```bash
# OCR配置
MATH_PAPER_OCR_URL=https://edusys5.sii.edu.cn/ocr

# LLM配置（OpenAI）
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# 或自定义LLM
MATH_PAPER_LLM_API_KEY=your_key
MATH_PAPER_LLM_BASE_URL=https://your-api.com/v1
MATH_PAPER_LLM_MODEL=your-model
```

## 输出示例

### Markdown报告结构

```markdown
# 论文标题

## 论文摘要

1-2段中文概述...

## 多维标签

- **领域**: 图论, 组合优化
- **内容**: 匹配存在性条件, Hall定理推广
- **方法**: 构造性证明, 鸽巢原理

## 章节结构

1. Introduction (p.1)
2. Preliminaries (p.2)
   2.1 Basic Definitions (p.3)

## 定理与定义

### 定理

- **Theorem 3.1** (p.5): 主要定理陈述...
  - **证明思路**: 通过构造...证明

### 定义

- **Definition 2.1** (p.3): 基本概念定义...

## 证明分析

### 核心方法

1. 归纳法
2. 反证法
3. 概率方法

## 关键公式

- (p.4) $f(x) = \sum_{i=1}^n a_i x_i$
```

## 技能内部工作流程

### 处理流程

```
用户输入PDF文件
    ↓
OCR处理（保留LaTeX公式）
    ↓
正则结构提取（快速）
    ↓
LLM结构精炼（可选）
    ↓
LLM摘要生成（可选）
    ↓
Markdown格式化输出
    ↓
返回结构化分析报告
```

### 错误处理

1. **OCR失败**：尝试备用处理或返回错误
2. **LLM不可用**：自动降级到快速模式
3. **PDF格式问题**：提供详细错误信息
4. **网络超时**：重试机制和超时控制

## 性能优化

### 处理时间预估

- **快速模式**：10-30秒（10页论文）
- **标准模式**：1-3分钟（10页论文）
- **深度模式**：3-5分钟（10页论文）

### 内存使用

- 分页处理大型PDF
- 流式OCR处理
- 自动清理临时文件

## 扩展功能

### 计划中的功能

1. **定理关系图谱**：建立定理之间的依赖关系
2. **证明策略分类**：自动识别证明方法
3. **难度分级**：基于数学复杂度分级
4. **学习路线图**：基于分析推荐学习路径

### 用户定制

1. **输出模板**：可定制的Markdown模板
2. **分析深度**：用户可配置的分析参数
3. **批量处理**：多篇论文批量分析
4. **结果缓存**：避免重复分析相同论文

## 故障排除

### 常见问题

1. **OCR服务不可用**
   - 检查网络连接
   - 尝试备用OCR服务
   - 使用快速模式（无OCR依赖）

2. **LLM配置错误**
   - 检查API密钥和端点
   - 验证模型可用性
   - 使用快速模式绕过LLM

3. **PDF处理失败**
   - 检查PDF文件完整性
   - 尝试其他PDF阅读器
   - 转换为标准PDF格式

4. **内存不足**
   - 减少并行工作线程
   - 使用分页处理模式
   - 增加系统内存

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

analyzer = PaperAnalyzer()
result = analyzer.analyze("paper.pdf", mode="standard")
```

## 技能集成

### 在Claude Code中使用

```python
# 加载技能后，Claude会自动识别数学论文分析需求
# 用户只需提供PDF文件或路径

# 示例对话：
# 用户: "请分析这篇数学论文：/path/to/paper.pdf"
# Claude: "我将使用数学论文分析技能为您分析这篇论文..."
```

### 与其他技能配合

1. **文献管理技能**：分析结果存入文献数据库
2. **笔记生成技能**：基于分析生成学习笔记
3. **教学材料技能**：创建教学幻灯片和练习题

## 技术架构

### 核心模块

1. **ocr_pdf_reader.py**：OCR PDF处理，保留数学公式
2. **structure_extractor.py**：两阶段结构提取
3. **paper_analyzer.py**：统一处理管道

### 依赖关系

- **PyMuPDF**：PDF渲染
- **httpx**：HTTP客户端（OCR API调用）
- **openai**：LLM API调用（可选）

### 设计原则

1. **渐进增强**：快速模式为基础，LLM为增强
2. **错误恢复**：各阶段独立，失败不影响整体
3. **用户友好**：清晰的进度反馈和错误信息
4. **性能优化**：并行处理和内存管理

## 贡献指南

### 开发环境

```bash
# 克隆仓库
git clone ...

# 安装开发依赖
pip install -r requirements.txt
pip install black ruff pytest

# 运行测试
pytest tests/
```

### 代码规范

- 使用Black代码格式化
- 使用Ruff代码检查
- 添加类型注解
- 编写文档字符串

### 提交贡献

1. Fork仓库
2. 创建功能分支
3. 编写测试用例
4. 提交Pull Request

## 许可证

本技能基于MIT许可证开源。

## 支持与反馈

如有问题或建议，请：

1. 查看故障排除部分
2. 提交Issue报告问题
3. 参与社区讨论
4. 贡献代码改进

---

_本技能专为数学学习者和研究人员设计，旨在提高数学论文阅读和研究效率。_
