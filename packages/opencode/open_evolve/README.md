# OpenEvolve Python Agent

## 📚 文档

- [快速开始](docs/QUICK_START.md) - 立即开始使用
- [详细指南](docs/OPEN_EVOLVE_GUIDE.md) - 完整使用说明
- [模块化文档](docs/README_OPEN_EVOLVE.md) - 架构和模块说明

## 🚀 快速命令

```bash
# 交互式界面
python -m open_evolve.main interactive

# 快速优化代码
python -m open_evolve.main optimize my_code.py

# 生成评估器
python -m open_evolve.main generate my_code.py
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

### 在opencode中

```
@open-evolve-python 优化以下代码...
```

## 🔗 相关文件

- `../openevolve_fixed_config.yaml` - 配置文件
- `docs/` - 完整文档
