# OpenEvolve Unified Agent 使用指南

## 🎯 概述

OpenEvolve Unified Agent 是一个基于进化算法的代码优化助手，能够自动分析和优化Python代码的性能、内存使用和算法效率。

## 🚀 快速开始

### 基本调用

```
@openevolve-unified <file.py>
```

### 查看帮助

```
@openevolve-unified
@openevolve-unified --help
@openevolve-unified -h
```

## 📋 命令语法

```
@openevolve-unified <file.py> [--iteration <n>] [--outdir <path>] [--mode <mode>]
```

### 参数说明

| 参数          | 缩写 | 说明                                                                | 默认值                  |
| ------------- | ---- | ------------------------------------------------------------------- | ----------------------- |
| `<file.py>`   | -    | 要优化的Python文件路径（必需）                                      | -                       |
| `--iteration` | `-i` | 进化迭代次数                                                        | 50                      |
| `--outdir`    | `-o` | 输出目录路径                                                        | `optimized_<timestamp>` |
| `--mode`      | `-m` | 运行模式：`optimize`（优化）、`analyze`（分析）、`discover`（发现） | `optimize`              |

## 📝 使用示例

### 示例1：基本优化

```bash
@openevolve-unified fibonacci.py
```

- 优化 `fibonacci.py` 文件
- 使用50次迭代
- 输出到自动生成的目录（如 `optimized_fibonacci_20250312_143022`）

### 示例2：自定义参数

```bash
@openevolve-unified sorting_algorithm.py --iteration 100 --outdir ./my_optimized
```

- 优化 `sorting_algorithm.py` 文件
- 使用100次迭代
- 输出到 `./my_optimized` 目录

### 示例3：分析模式

```bash
@openevolve-unified complex_code.py --mode analyze
```

- 分析代码结构和复杂度
- 提供优化建议
- 不执行进化优化

### 示例4：算法发现

```bash
@openevolve-unified search_problem.py --mode discover --iteration 200
```

- 尝试发现新的算法解决方案
- 使用200次迭代
- 探索不同的算法实现

### 示例5：直接优化代码片段

```
@openevolve-unified "def slow_function(n):
    result = 0
    for i in range(n):
        for j in range(n):
            result += i * j
    return result"
```

- 直接优化提供的代码片段
- 自动创建临时文件处理

## 📁 输出结构

优化完成后，系统会创建以下目录结构：

```
optimized_<timestamp>/
├── best/                    # 最佳优化结果
│   ├── best_program.py     # 优化后的程序
│   ├── metrics.json        # 性能指标
│   └── analysis_report.md  # 分析报告
├── logs/                   # 运行日志
│   ├── evolution.log       # 进化过程日志
│   └── error.log          # 错误日志
├── intermediate/           # 中间结果
│   ├── generation_*.py    # 各代程序
│   └── fitness_scores.csv # 适应度分数
├── summary.md             # 优化总结报告
├── config.yaml            # 使用的配置
└── README.md              # 结果说明文档
```

### 输出文件说明

1. **best_program.py** - 优化后的最佳程序
2. **metrics.json** - 包含性能改进数据：
   ```json
   {
     "speed_improvement": 2.3,
     "memory_reduction": 0.15,
     "original_time": 0.45,
     "optimized_time": 0.19,
     "code_complexity_change": -0.3
   }
   ```
3. **summary.md** - 优化过程总结
4. **evolution.log** - 详细的进化过程日志

## 🔧 技术要求

### 支持的Python版本

- Python 3.8+
- 建议使用Python 3.10或更高版本

### 依赖项

- 确保要优化的代码的所有依赖项已安装
- 系统不会自动安装Python包

### 代码要求

- 必须是有效的Python语法
- 包含至少一个函数定义
- 避免使用全局变量（如必须使用，请确保可测试性）

## 🎯 优化类型

### 1. 性能优化

- 算法复杂度优化（O(n²) → O(n log n)）
- 循环优化
- 缓存和记忆化
- 向量化操作

### 2. 内存优化

- 减少不必要的对象创建
- 使用生成器代替列表
- 内存复用

### 3. 代码简化

- 减少冗余代码
- 提取公共函数
- 改进可读性

### 4. 算法改进

- 发现更优的算法
- 改进边界条件处理
- 优化递归实现

## 🔍 工作流程

1. **代码分析** - 分析代码结构、复杂度和性能瓶颈
2. **评估器生成** - 自动创建测试评估器
3. **进化优化** - 运行遗传算法进行优化
4. **结果验证** - 验证优化后代码的正确性
5. **报告生成** - 生成优化报告和结果文件

## 📊 性能指标

优化过程会跟踪以下指标：

| 指标       | 说明                 |
| ---------- | -------------------- |
| 执行时间   | 代码运行时间（秒）   |
| 内存使用   | 峰值内存使用量（MB） |
| 代码复杂度 | 圈复杂度指标         |
| 代码行数   | 源代码行数变化       |
| 适应度分数 | 进化算法中的适应度值 |

## 🚨 常见问题

### Q1: 优化过程太慢怎么办？

**A:** 尝试减少迭代次数：`--iteration 20`，或简化代码逻辑。

### Q2: 如何查看实时进度？

**A:** 查看输出目录中的 `logs/evolution.log` 文件。

### Q3: 优化后的代码不工作怎么办？

**A:** 系统会验证优化后代码的正确性，如果仍有问题，请检查：

1. 原始代码是否有隐藏的依赖
2. 边界条件是否被正确处理
3. 联系开发者查看详细日志

### Q4: 支持多文件项目吗？

**A:** 目前主要支持单文件优化。对于多文件项目，建议：

1. 将主要逻辑提取到单个文件
2. 使用 `--mode analyze` 先进行分析
3. 分模块优化

### Q5: 如何自定义优化目标？

**A:** 可以通过修改配置文件自定义评估标准：

1. 查看 `openevolve_fixed_config.yaml`
2. 调整评估权重
3. 添加自定义评估函数

### Q6: 优化会改变代码功能吗？

**A:** 不会。系统会确保优化后的代码与原始代码功能等价。

## 📚 进阶用法

### 1. 批量优化

```bash
# 优化多个文件
for file in *.py; do
  @openevolve-unified "$file" --iteration 30 --outdir "optimized_${file%.py}"
done
```

### 2. 对比优化

```bash
# 优化并对比不同参数
@openevolve-unived algorithm.py --iteration 50 --outdir opt_50
@openevolve-unived algorithm.py --iteration 100 --outdir opt_100
# 对比两个结果目录
```

### 3. 集成到开发流程

```bash
# 在CI/CD中集成
@openevolve-unified src/main_algorithm.py --iteration 20 --outdir ./optimized
# 使用优化后的代码
cp ./optimized/best/best_program.py src/optimized_algorithm.py
```

## 🛠️ 故障排除

### 错误：文件不存在

```
错误：找不到文件 'my_code.py'
```

**解决方法：**

- 检查文件路径是否正确
- 使用绝对路径：`@openevolve-unified /full/path/to/my_code.py`

### 错误：语法错误

```
错误：代码包含语法错误
```

**解决方法：**

- 先修复代码语法错误
- 使用Python解释器验证：`python -m py_compile my_code.py`

### 错误：导入错误

```
错误：导入模块失败
```

**解决方法：**

- 确保所有依赖项已安装：`pip install missing_module`
- 检查Python路径设置

### 错误：超时

```
错误：优化过程超时
```

**解决方法：**

- 减少迭代次数：`--iteration 20`
- 简化代码逻辑
- 增加超时时间（需要修改配置）

### 错误：内存不足

```
错误：内存使用超过限制
```

**解决方法：**

- 减少种群大小（需要修改配置）
- 优化代码减少内存使用
- 使用更高效的算法

## 📞 获取帮助

### 1. 查看内置帮助

```
@openevolve-unified
@openevolve-unified --help
```

### 2. 查看示例

查看 `open_evolve/examples/` 目录中的示例代码。

### 3. 查看详细文档

阅读 `open_evolve/README.md` 和 `open_evolve/docs/` 中的文档。

### 4. 查看日志

优化过程中生成的日志文件包含详细信息：

- `logs/evolution.log` - 进化过程日志
- `logs/error.log` - 错误日志

### 5. 报告问题

如果遇到问题，请提供：

1. 原始代码
2. 使用的命令
3. 错误信息
4. 日志文件内容

## 🎉 成功案例

### 案例1：斐波那契数列优化

**原始代码：** O(2ⁿ) 的递归实现
**优化后：** O(n) 的迭代实现，带缓存
**性能提升：** 1000倍加速

### 案例2：矩阵乘法优化

**原始代码：** 三重嵌套循环
**优化后：** 使用NumPy向量化
**性能提升：** 50倍加速

### 案例3：数据过滤优化

**原始代码：** 多次遍历列表
**优化后：** 单次遍历，使用生成器
**内存减少：** 70%内存使用

## 🔮 未来计划

### 即将支持的功能：

1. **多语言支持** - 支持JavaScript、Go等其他语言
2. **云端优化** - 利用云端计算资源加速优化
3. **智能推荐** - 基于代码类型推荐优化策略
4. **团队协作** - 共享优化结果和最佳实践
5. **可视化界面** - 图形化展示优化过程

### 路线图：

- 2024 Q2: 增强分析功能
- 2024 Q3: 支持更多优化类型
- 2024 Q4: 集成到主流IDE

## 📄 许可证

OpenEvolve Unified Agent 基于MIT许可证开源。

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 🙏 致谢

感谢所有贡献者和用户的支持！

---

**最后更新：** 2024年3月12日  
**版本：** 1.0.0  
**作者：** OpenEvolve团队
