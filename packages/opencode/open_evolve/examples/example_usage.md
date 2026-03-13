# OpenEvolve Unified Agent 使用示例

## 示例1：优化斐波那契数列

### 创建示例文件 `fibonacci.py`

```python
def fibonacci(n):
    """计算斐波那契数列（低效递归版本）"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    # 测试代码
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"fibonacci(20) = {fibonacci(20)}")
```

### 运行优化

```
@openevolve-unified fibonacci.py --iteration 30 --outdir fib_optimized
```

### 预期输出

```
🔧 OpenEvolve 统一优化接口
   输入文件: fibonacci.py
   迭代次数: 30
   输出目录: fib_optimized
   运行模式: optimize

✅ 优化完成！

**总结:**
- 文件: fibonacci.py
- 迭代次数: 30
- 输出目录: fib_optimized/

**结果:**
- 速度提升: 1000倍
- 内存使用: 无显著变化
- 最佳程序: fib_optimized/best/best_program.py

**关键优化:**
1. 添加了缓存（记忆化）
2. 实现了迭代版本
3. 优化了边界条件处理

**下一步:**
- 测试优化后代码
- 考虑进一步优化大数计算
```

## 示例2：分析排序算法

### 创建示例文件 `bubble_sort.py`

```python
def bubble_sort(arr):
    """冒泡排序算法"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

if __name__ == "__main__":
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"原始数组: {test_arr}")
    print(f"排序后: {bubble_sort(test_arr.copy())}")
```

### 运行分析

```
@openevolve-unified bubble_sort.py --mode analyze
```

### 预期输出

```
🔍 代码分析模式
   输入文件: bubble_sort.py
   运行模式: analyze

📊 分析结果:

**代码结构:**
- 函数数量: 1
- 代码行数: 15
- 圈复杂度: 3

**性能分析:**
- 时间复杂度: O(n²)
- 空间复杂度: O(1)
- 算法类型: 比较排序

**优化建议:**
1. 考虑使用快速排序（O(n log n)）
2. 对于小数组，插入排序可能更高效
3. 可以添加提前终止优化

**下一步:**
- 使用 @openevolve-unified bubble_sort.py --mode optimize 进行优化
- 考虑实现更高效的排序算法
```

## 示例3：直接优化代码片段

### 运行优化

```
@openevolve-unified "def sum_of_squares(n):
    result = 0
    for i in range(n):
        result += i * i
    return result"
```

### 预期输出

````
🔧 代码片段优化模式
   输入类型: 代码片段
   迭代次数: 50
   输出目录: optimized_20250312_143022

✅ 优化完成！

**结果:**
- 速度提升: 2.5倍
- 最佳实现: 使用公式 n*(n+1)*(2n+1)//6

**优化后代码:**
```python
def sum_of_squares(n):
    """计算1² + 2² + ... + n²"""
    return n * (n + 1) * (2 * n + 1) // 6
````

**验证:**

- 原始结果: sum_of_squares(100) = 338350
- 优化结果: sum_of_squares(100) = 338350 ✓

````

## 示例4：算法发现模式

### 创建示例文件 `max_subarray.py`
```python
def max_subarray_sum(arr):
    """寻找最大子数组和（暴力解法）"""
    n = len(arr)
    max_sum = float('-inf')

    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum > max_sum:
                max_sum = current_sum

    return max_sum

if __name__ == "__main__":
    test_arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print(f"最大子数组和: {max_subarray_sum(test_arr)}")  # 应输出 6
````

### 运行算法发现

```
@openevolve-unified max_subarray.py --mode discover --iteration 100 --outdir max_subarray_discovered
```

### 预期输出

````
🔬 算法发现模式
   输入文件: max_subarray.py
   迭代次数: 100
   输出目录: max_subarray_discovered
   运行模式: discover

🎯 发现结果:

**发现的算法:**
1. Kadane算法（O(n)时间复杂度）
2. 分治法实现
3. 动态规划变体

**最佳算法 (Kadane算法):**
```python
def max_subarray_sum(arr):
    """Kadane算法 - O(n)时间复杂度"""
    max_ending_here = max_so_far = arr[0]

    for x in arr[1:]:
        max_ending_here = max(x, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far
````

**性能对比:**

- 原始算法: O(n²) 时间
- 发现算法: O(n) 时间
- 加速比: 100倍（对于n=1000）

**验证:**

- 测试数组: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
- 原始结果: 6
- 发现结果: 6 ✓

````

## 示例5：完整工作流程

### 步骤1：创建测试文件
```python
# inefficient_search.py
def linear_search(arr, target):
    """线性搜索"""
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1

if __name__ == "__main__":
    arr = list(range(1000))
    print(f"搜索 999: {linear_search(arr, 999)}")
    print(f"搜索 2000: {linear_search(arr, 2000)}")
````

### 步骤2：分析代码

```
@openevolve-unified inefficient_search.py --mode analyze
```

### 步骤3：优化代码

```
@openevolve-unified inefficient_search.py --iteration 50 --outdir search_optimized
```

### 步骤4：验证结果

```bash
# 查看优化结果
cat search_optimized/best/best_program.py

# 查看性能指标
cat search_optimized/best/metrics.json

# 查看总结报告
cat search_optimized/summary.md
```

## 故障排除示例

### 问题：文件不存在

```
错误：找不到文件 'nonexistent.py'
```

**解决：**

```
@openevolve-unified ./path/to/existing_file.py
```

### 问题：语法错误

```
错误：代码包含语法错误
```

**解决：** 先修复语法错误

```python
# 修复前
def bad_function(
    return 42

# 修复后
def good_function():
    return 42
```

### 问题：依赖缺失

```
错误：导入模块 'numpy' 失败
```

**解决：** 安装依赖

```bash
pip install numpy
```

## 最佳实践

1. **从小开始**：先用小迭代次数测试

   ```
   @openevolve-unified my_code.py --iteration 20
   ```

2. **逐步优化**：先分析，再优化

   ```
   @openevolve-unified my_code.py --mode analyze
   @openevolve-unified my_code.py --iteration 50
   ```

3. **保存结果**：指定输出目录

   ```
   @openevolve-unified my_code.py --outdir ./optimized_results
   ```

4. **验证正确性**：检查优化后代码

   ```bash
   python optimized_results/best/best_program.py
   ```

5. **查看日志**：了解优化过程
   ```bash
   tail -f optimized_results/logs/evolution.log
   ```

## 更多资源

- 完整文档：`../.opencode/agents/openevolve-unified-README.md`
- 配置说明：`../openevolve_fixed_config.yaml`
- 示例代码：`./examples/` 目录
- 问题反馈：查看日志文件中的错误信息
