"""
示例代码模块
"""

from pathlib import Path


def get_example_code(example_name: str) -> str:
    """获取示例代码"""
    examples_dir = Path(__file__).parent

    if example_name == "bubble_sort":
        return '''
def bubble_sort(arr):
    """冒泡排序 - 简单实现"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
'''

    elif example_name == "slow_sum":
        return '''
def slow_sum(numbers):
    """计算列表和 - 朴素实现"""
    total = 0
    for num in numbers:
        total += num
    return total
'''

    elif example_name == "fibonacci":
        return '''
def fibonacci(n):
    """斐波那契数列 - 递归实现"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
'''

    elif example_name == "find_max":
        return '''
def find_max(numbers):
    """查找最大值 - 朴素实现"""
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    return max_val
'''

    else:
        raise ValueError(f"未知示例: {example_name}")


def list_examples() -> list:
    """列出所有示例"""
    return ["bubble_sort", "slow_sum", "fibonacci", "find_max"]


__all__ = ["get_example_code", "list_examples"]
