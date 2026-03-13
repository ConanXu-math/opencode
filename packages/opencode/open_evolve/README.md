# OpenEvolve Python Agent

## 📚 文档

- [快速开始](docs/QUICK_START.md) - 立即开始使用
- [详细指南](docs/OPEN_EVOLVE_GUIDE.md) - 完整使用说明
- [模块化文档](docs/README_OPEN_EVOLVE.md) - 架构和模块说明

## 🚀 快速命令

```bash
# 统一接口优化
python -m open_evolve.main my_code.py --iteration 50 --outdir optimized

# 代码分析模式
python -m open_evolve.main "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)" --mode analyze

# 算法发现模式
python -m open_evolve.main sorting_algorithm.py --mode discover --iteration 100
```

## 📁 模块结构

```
open_evolve/
├── docs/                    # 文档
│   ├── QUICK_START.md       # 快速开始
│   ├── OPEN_EVOLVE_GUIDE.md # 使用指南
│   └── README_OPEN_EVOLVE.md # 详细文档
├── core/                    # 核心功能
│   ├── analyzer.py          # 代码分析器
│   ├── evaluator_builder.py # 评估器构建器
│   └── auto_evaluator.py    # 自动评估器系统
├── cli/                     # 命令行接口
│   ├── interactive.py       # 交互式界面
│   └── commands.py          # 命令行命令
├── config/                  # 配置管理
├── utils/                   # 工具函数
├── examples/                # 示例代码
├── __init__.py              # 包导出
└── main.py                  # 统一入口点
```

## 🎯 核心功能

1. **自动代码分析** - 识别函数结构和复杂度
2. **智能评估器生成** - 基于代码自动创建测试
3. **一键优化** - 自动运行OpenEvolve进化
4. **交互式界面** - 用户友好的命令行界面

## ⚙️ 配置

默认配置文件: `../openevolve_fixed_config.yaml`

- DeepSeek API密钥已配置
- 模型: deepseek-chat
- 温度: 0.7
- 种群大小: 50

## 📞 使用方式

### Python API

```python
from open_evolve import AutoEvaluatorSystem
system = AutoEvaluatorSystem()
result = system.auto_evolve(code, iterations=50)
```

### 命令行接口

```bash
# 统一接口优化
python -m open_evolve.main my_code.py --iteration 50 --outdir optimized

# 代码分析模式
python -m open_evolve.main "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)" --mode analyze

# 算法发现模式
python -m open_evolve.main sorting_algorithm.py --mode discover --iteration 100
```

### 在opencode中（推荐）

#### 使用 Unified Agent

```
@openevolve-unified fibonacci.py
@openevolve-unified slow_algorithm.py --iteration 100 --outdir optimized_results
@openevolve-unified complex_code.py --mode analyze
```

#### 查看帮助

```
@openevolve-unified
@openevolve-unified --help
```

#### 传统方式

```
@openevolve levenshtein_optimization.py
@openevolve slow_algorithm.py --iteration 100 --outdir optimized_results
@openevolve 请分析并优化这段斐波那契数列算法
```

## 🔗 相关文件

- `../openevolve_fixed_config.yaml` - 配置文件
- `docs/` - 完整文档
- `../.opencode/agents/openevolve-unified.md` - Unified Agent 配置文件
- `../.opencode/agents/openevolve-unified-README.md` - Unified Agent 详细使用指南

## 🆕 OpenEvolve Unified Agent

### 特性

- **统一接口**：简化参数传递
- **友好提示**：无参数时显示详细帮助
- **智能处理**：自动识别文件和代码片段
- **完整文档**：包含示例和故障排除

### 快速参考

```
@openevolve-unified <file.py> [--iteration <n>] [--outdir <path>] [--mode <mode>]

参数：
  <file.py>   要优化的Python文件（必需）
  -i, --iteration  迭代次数（默认：50）
  -o, --outdir     输出目录（默认：optimized_<timestamp>）
  -m, --mode       模式：optimize/analyze/discover（默认：optimize）

示例：
  @openevolve-unified fibonacci.py
  @openevolve-unified sorting.py -i 100 -o ./optimized -m discover
```

### 获取帮助

```
@openevolve-unified
@openevolve-unified --help
```
