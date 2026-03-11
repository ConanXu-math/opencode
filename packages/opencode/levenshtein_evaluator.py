#!/usr/bin/env python3
"""
Levenshtein 算法评估器
用于 OpenEvolve 进化优化
"""

import time
import random
import string
from typing import Dict, Any


def generate_random_string(length: int) -> str:
    """生成随机字符串"""
    return "".join(random.choices(string.ascii_lowercase, k=length))


# 测试用例
TEST_CASES = [
    # (字符串1, 字符串2, 期望距离)
    ("kitten", "sitting", 3),
    ("", "abc", 3),
    ("abc", "", 3),
    ("abc", "abc", 0),
    ("abc", "def", 3),
    ("abcdef", "abcfed", 2),
    ("book", "back", 2),
    ("intention", "execution", 5),
]

# 性能测试用例
PERFORMANCE_CASES = (
    [(generate_random_string(100), generate_random_string(100)) for _ in range(5)]
    + [(generate_random_string(500), generate_random_string(500)) for _ in range(3)]
    + [(generate_random_string(1000), generate_random_string(1000)) for _ in range(2)]
)


def evaluate_levenshtein(code: str) -> Dict[str, Any]:
    """
    评估 Levenshtein 算法实现
    返回包含多个指标的字典
    """
    try:
        # 执行代码以定义函数
        exec_globals = {}
        exec(code, exec_globals)

        # 获取 levenshtein 函数
        if "levenshtein" not in exec_globals:
            return {
                "valid": False,
                "error": "代码必须定义 'levenshtein' 函数",
                "accuracy": 0.0,
                "performance": float("inf"),
                "memory_score": 0.0,
                "complexity_score": 0.0,
            }

        levenshtein_func = exec_globals["levenshtein"]

        # 1. 准确性测试
        correct_count = 0
        total_tests = len(TEST_CASES)

        for a, b, expected in TEST_CASES:
            try:
                result = levenshtein_func(a, b)
                if result == expected:
                    correct_count += 1
            except:
                pass

        accuracy = correct_count / total_tests if total_tests > 0 else 0.0

        # 2. 性能测试
        performance_times = []
        for a, b in PERFORMANCE_CASES:
            try:
                start_time = time.perf_counter()
                for _ in range(10):  # 多次运行取平均
                    levenshtein_func(a, b)
                end_time = time.perf_counter()
                avg_time = (end_time - start_time) / 10
                performance_times.append(avg_time)
            except:
                performance_times.append(float("inf"))

        avg_performance = (
            sum(performance_times) / len(performance_times)
            if performance_times
            else float("inf")
        )

        # 3. 代码复杂度评估
        complexity_score = evaluate_complexity(code)

        # 4. 内存使用评估（基于代码分析）
        memory_score = evaluate_memory_usage(code)

        # 综合评分
        if accuracy < 1.0:
            # 准确性不足，惩罚性评分
            overall_score = accuracy * 0.1  # 最大0.1分
        else:
            # 准确性100%，基于性能评分
            performance_score = 1.0 / (1.0 + avg_performance * 1000)  # 转换为0-1范围
            overall_score = (
                0.3 * accuracy
                + 0.4 * performance_score
                + 0.2 * memory_score
                + 0.1 * complexity_score
            )

        return {
            "valid": True,
            "accuracy": accuracy,
            "performance": avg_performance,
            "memory_score": memory_score,
            "complexity_score": complexity_score,
            "overall_score": overall_score,
            "details": {
                "correct_tests": correct_count,
                "total_tests": total_tests,
                "performance_cases": len(PERFORMANCE_CASES),
                "code_length": len(code),
            },
        }

    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
            "accuracy": 0.0,
            "performance": float("inf"),
            "memory_score": 0.0,
            "complexity_score": 0.0,
            "overall_score": 0.0,
        }


def evaluate_complexity(code: str) -> float:
    """评估代码复杂度"""
    score = 1.0  # 基础分

    # 检查嵌套循环
    lines = code.split("\n")
    max_nesting = 0
    current_nesting = 0

    for line in lines:
        line = line.strip()
        if (
            line.startswith("for ")
            or line.startswith("while ")
            or line.startswith("if ")
        ):
            current_nesting += 1
            max_nesting = max(max_nesting, current_nesting)
        elif line == "pass" or line.startswith("return") or line.startswith("#"):
            # 这些行不结束嵌套
            pass
        else:
            # 其他行可能结束嵌套
            if current_nesting > 0 and not line.endswith(":"):
                current_nesting -= 1

    # 嵌套越深，分数越低
    if max_nesting > 3:
        score *= 0.5
    elif max_nesting > 2:
        score *= 0.7
    elif max_nesting > 1:
        score *= 0.9

    # 检查代码长度
    if len(code) > 1000:
        score *= 0.7
    elif len(code) > 500:
        score *= 0.8
    elif len(code) > 200:
        score *= 0.9

    return score


def evaluate_memory_usage(code: str) -> float:
    """评估内存使用（基于代码模式）"""
    score = 1.0

    # 检查是否使用二维矩阵
    if (
        "[[0]" in code
        or "list(range(" in code
        or "range(" in code
        and "for _ in range(" in code
    ):
        # 可能是二维矩阵实现
        score *= 0.5

    # 检查是否使用滚动数组
    if "previous_row" in code and "current_row" in code:
        # 可能是内存优化版本
        score *= 1.2

    # 检查是否使用早期终止
    if "max_distance" in code or "early" in code or "terminat" in code:
        # 可能有优化
        score *= 1.1

    # 检查是否使用分块
    if "chunk" in code or "block" in code:
        # 流处理优化
        score *= 1.15

    return min(score, 2.0)  # 上限2.0


# 示例评估
if __name__ == "__main__":
    # 测试原始算法
    original_code = """
def levenshtein(a: str, b: str) -> int:
    if a == "" or b == "":
        return max(len(a), len(b))
    
    matrix = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    
    for i in range(len(a) + 1):
        matrix[i][0] = i
    for j in range(len(b) + 1):
        matrix[0][j] = j
    
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            matrix[i][j] = min(
                matrix[i-1][j] + 1,
                matrix[i][j-1] + 1,
                matrix[i-1][j-1] + cost
            )
    
    return matrix[len(a)][len(b)]
"""

    result = evaluate_levenshtein(original_code)
    print("原始算法评估结果:")
    for key, value in result.items():
        if key != "details":
            print(f"  {key}: {value}")

    print("\n详细信息:")
    for key, value in result.get("details", {}).items():
        print(f"  {key}: {value}")
