# OpenEvolve Unified Agent

## 🚀 快速开始

### 1. 使用统一接口

```bash
# 优化Python文件
python -m open_evolve.main my_code.py --iteration 50 --outdir optimized

# 分析代码片段
python -m open_evolve.main "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)" --mode analyze

# 算法发现模式
python -m open_evolve.main sorting_algorithm.py --mode discover --iteration 100
```

### 2. 作为Python模块导入

```python
from open_evolve import AutoEvaluatorSystem

# 自动优化代码
system = AutoEvaluatorSystem()
result = system.auto_evolve(code, iterations=50)

if result['success']:
    print(f"优化完成! 输出目录: {result['output_dir']}")
    print(f"优化后代码:\n{result['optimized_code']}")
```

### 3. 在opencode中调用

```
@openevolve levenshtein_optimization.py

@openevolve slow_algorithm.py --iteration 100 --outdir optimized_results

@openevolve 请分析并优化这段斐波那契数列算法
```

## 📁 模块结构

```
open_evolve/
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

## 🎯 功能特性

### 1. 自动代码分析

- 识别函数结构和参数
- 分析代码复杂度
- 生成测试用例

### 2. 智能评估器生成

- 基于代码功能自动创建评估器
- 生成测试用例和性能测试
- 支持多目标优化评估

### 3. 一键优化

- 自动生成评估器并运行OpenEvolve
- 支持自定义迭代次数和输出目录
- 返回优化后的代码和性能指标

## ⚙️ 配置说明

### 默认配置

配置文件: `../openevolve_fixed_config.yaml`

- DeepSeek API密钥已配置
- 模型: deepseek-chat
- 温度: 0.7
- 种群大小: 50

### 自定义配置

```python
from open_evolve.config import load_config, get_default_config

# 加载自定义配置
config = load_config("my_config.yaml")

# 获取默认配置
default_config = get_default_config()
```

## 📊 输出结构

优化完成后会生成:

```
optimized_output/
├── best/
│   ├── best_program.py      # 优化后的代码
│   └── best_program_info.json # 优化指标
├── logs/                    # 运行日志
└── checkpoints/            # 检查点文件
```

## 🎪 使用示例

### 示例1: 优化排序算法

```bash
# 创建示例文件
cat > bubble_sort.py << 'EOF'
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
EOF

# 运行优化
python -m open_evolve.main optimize bubble_sort.py --iterations 30
```

### 示例2: 优化数值计算

```python
from open_evolve import AutoEvaluatorSystem

code = '''
def slow_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
'''

system = AutoEvaluatorSystem()
result = system.auto_evolve(code, iterations=20)
```

## 💡 最佳实践

1. **从小开始**: 先用10-20次迭代测试
2. **明确目标**: 确定优化重点 (速度、内存、准确性)
3. **验证结果**: 检查优化后的代码正确性
4. **调整参数**: 根据结果调整迭代次数

## 🆘 常见问题

### Q: 优化时间太长?

A: 减少 `--iterations` 参数，或使用更简单的评估器

### Q: 优化没有改进?

A: 检查评估器是否正确评分，或增加 `--iterations`

### Q: API错误?

A: 检查配置文件中的API密钥

## 🔗 相关文档

- `../README_OPEN_EVOLVE.md` - 详细模块化文档
- `../OPEN_EVOLVE_GUIDE.md` - 使用指南
- `../openevolve_fixed_config.yaml` - 配置文件

## 📝 工作流程

1. **识别优化机会**: 找到性能瓶颈或复杂代码
2. **生成评估器**: 自动创建评估脚本
3. **运行优化**: 使用OpenEvolve进化代码
4. **验证结果**: 检查优化后的代码正确性
5. **集成应用**: 将优化代码应用到项目中

**提示**: 在opencode中，可以直接使用 `@openevolve` 调用优化功能。
