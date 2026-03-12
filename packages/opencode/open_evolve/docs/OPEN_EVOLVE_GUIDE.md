# OpenEvolve Python Agent 使用指南

## 🚀 快速开始

### 方式1: 统一接口优化

```bash
python -m open_evolve.main <文件.py> --iteration 50 --outdir optimized
```

### 方式2: 代码分析

```bash
python -m open_evolve.main "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)" --mode analyze
```

### 方式3: 在opencode中直接调用

```
@openevolve levenshtein_optimization.py

@openevolve slow_algorithm.py --iteration 100 --outdir optimized_results

@openevolve 请分析并优化这段斐波那契数列算法
```

## 📋 可用命令

### 1. 分析代码并生成评估器

```bash
python -m open_evolve.main generate <文件.py> --output <目录>
```

### 2. 自动优化

```bash
python -m open_evolve.main optimize <文件.py> --iterations 50
```

### 3. 测试评估器

```bash
cd <输出目录>
python -m openevolve.cli target_code.py auto_evaluator.py --config ../openevolve_fixed_config.yaml
```

## 🎯 优化示例

### 示例1: 排序算法

```python
# 保存为 sort.py
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

运行优化:

```bash
python -m open_evolve.main optimize sort.py
```

### 示例2: 数值计算

```python
# 保存为 math.py
def slow_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
```

## ⚙️ 配置说明

配置文件: `openevolve_fixed_config.yaml`

- 已配置DeepSeek API密钥
- 模型: deepseek-chat
- 温度: 0.7
- 种群大小: 50

## 📊 优化结果

优化输出目录包含:

```
optimized_output/
├── best/
│   ├── best_program.py      # 优化后的代码
│   └── best_program_info.json # 优化指标
├── logs/                    # 运行日志
└── checkpoints/            # 检查点文件
```

## 💡 使用技巧

1. **从小开始**: 先用10-20次迭代测试
2. **明确目标**: 代码要优化什么? (速度、内存、准确性)
3. **检查结果**: 验证优化后的代码是否正确
4. **调整参数**: 根据结果调整迭代次数和种群大小

## 🆘 常见问题

### Q: 优化时间太长?

A: 减少 `--iterations` 参数，或使用更简单的评估器

### Q: 优化没有改进?

A: 检查评估器是否正确评分，或增加 `--iterations`

### Q: API错误?

A: 检查 `openevolve_fixed_config.yaml` 中的API密钥

## 🔗 相关文件

- `open_evolve/` - 模块化OpenEvolve
- `openevolve_fixed_config.yaml` - 配置文件
- `README_OPEN_EVOLVE.md` - 模块化文档

## 🎪 实际工作流程

1. **识别优化机会**: 找到性能瓶颈或复杂代码
2. **生成评估器**: 自动或手动创建评估脚本
3. **运行优化**: 使用OpenEvolve进化代码
4. **验证结果**: 检查优化后的代码正确性
5. **集成应用**: 将优化代码应用到项目中

**提示**: 在opencode中，可以直接使用 `@openevolve` 调用优化功能。
