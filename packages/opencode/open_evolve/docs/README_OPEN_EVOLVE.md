# OpenEvolve Python Agent - 模块化版本

## 📁 目录结构

```
open_evolve/
├── __init__.py              # 包导出
├── main.py                  # 统一入口点
├── core/                    # 核心模块
│   ├── __init__.py
│   ├── analyzer.py          # 代码分析器
│   ├── evaluator_builder.py # 评估器构建器
│   └── auto_evaluator.py    # 自动评估器系统
├── cli/                     # 命令行接口
│   ├── __init__.py
│   ├── interactive.py       # 交互式界面
│   └── commands.py          # 命令行命令
├── config/                  # 配置模块
│   ├── __init__.py
│   └── loader.py           # 配置加载器
├── utils/                   # 工具模块
│   └── __init__.py
└── examples/               # 示例代码
    └── __init__.py
```

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

### 2. 命令行参数

```bash
# 基本用法
python open_evolve/main.py <file_or_code>

# 带参数
python open_evolve/main.py my_code.py --iteration 100 --outdir results --mode optimize
```

### 3. 作为模块导入

```python
from open_evolve import AutoEvaluatorSystem, OpenEvolveInteractive

# 自动优化
system = AutoEvaluatorSystem()
result = system.auto_evolve(code, iterations=50)

# 交互式界面
app = OpenEvolveInteractive()
app.run()
```

## 📋 可用命令

### 交互式界面

```bash
python -m open_evolve.main interactive
```

### 快速优化

```bash
python -m open_evolve.main optimize <代码文件> [选项]
选项:
  --iterations, -i  迭代次数 (默认50)
  --output, -o      输出目录 (默认optimized)
```

### 生成评估器

```bash
python -m open_evolve.main generate <代码文件> [选项]
选项:
  --output, -o      输出目录 (默认evaluator)
```

## 🎯 使用示例

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

# 优化
python -m open_evolve.main optimize bubble_sort.py --iterations 30
```

### 示例2: 使用Python API

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

if result['success']:
    print(f"优化完成! 输出目录: {result['output_dir']}")
    print(f"优化后代码:\n{result['optimized_code']}")
```

## ⚙️ 配置管理

### 默认配置

配置文件: `openevolve_fixed_config.yaml`

- DeepSeek API密钥已配置
- 模型: deepseek-chat
- 温度: 0.7
- 种群大小: 50

### 自定义配置

```python
from open_evolve.config import load_config, get_default_config

# 加载配置文件
config = load_config("my_config.yaml")

# 获取默认配置
default_config = get_default_config()
```

## 🔧 核心模块

### 1. 代码分析器 (`core.analyzer`)

```python
from open_evolve.core.analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()
analysis = analyzer.analyze(code)
print(f"函数: {analysis['functions']}")
print(f"复杂度: {analysis['complexity']}")
```

### 2. 评估器构建器 (`core.evaluator_builder`)

```python
from open_evolve.core.evaluator_builder import EvaluatorBuilder, TestCaseGenerator

builder = EvaluatorBuilder()
evaluator_code = builder.build("my_code.py", analysis)
```

### 3. 自动评估器系统 (`core.auto_evaluator`)

```python
from open_evolve.core.auto_evaluator import AutoEvaluatorSystem

system = AutoEvaluatorSystem()
result = system.generate_for_code(code, "output_dir")
```

## 📊 输出结构

优化输出目录:

```
optimized_output/
├── best/
│   ├── best_program.py      # 优化后的代码
│   └── best_program_info.json # 优化指标
├── logs/                    # 运行日志
└── checkpoints/            # 检查点文件
```

## 💡 最佳实践

1. **从小开始**: 先用10-20次迭代测试
2. **明确目标**: 确定优化重点 (速度、内存、准确性)
3. **验证结果**: 检查优化后的代码正确性
4. **调整参数**: 根据结果调整迭代次数和种群大小

## 🆘 常见问题

### Q: 优化时间太长?

A: 减少 `--iterations` 参数，或使用更简单的评估器

### Q: 优化没有改进?

A: 检查评估器是否正确评分，或增加 `--iterations`

### Q: API错误?

A: 检查配置文件中的API密钥

## 🔗 相关文件

- `openevolve_fixed_config.yaml` - 默认配置文件
- `open_evolve/README.md` - 模块README
- `OPEN_EVOLVE_GUIDE.md` - 详细使用指南

## 🎪 工作流程

1. **识别优化机会**: 找到性能瓶颈或复杂代码
2. **生成评估器**: 自动或手动创建评估脚本
3. **运行优化**: 使用OpenEvolve进化代码
4. **验证结果**: 检查优化后的代码正确性
5. **集成应用**: 将优化代码应用到项目中

**提示**: 在opencode中，可以直接使用 `@openevolve` 调用优化功能。
