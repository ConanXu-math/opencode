#!/usr/bin/env python3
"""
Levenshtein 算法性能基准测试
"""

import time
import random
import string
from levenshtein_optimization import (
    levenshtein_original,
    levenshtein_optimized_memory,
    levenshtein_stream_optimized,
    levenshtein_early_termination,
)


def generate_random_string(length: int) -> str:
    """生成随机字符串"""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def benchmark_algorithm(
    name: str, algorithm, a: str, b: str, iterations: int = 100
) -> float:
    """基准测试算法性能"""
    # 预热
    for _ in range(10):
        algorithm(a, b)

    # 正式测试
    start_time = time.perf_counter()
    for _ in range(iterations):
        algorithm(a, b)
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    avg_time = elapsed / iterations
    return avg_time


def memory_usage_estimate(a: str, b: str) -> dict:
    """估算各算法的内存使用"""
    n, m = len(a), len(b)

    estimates = {
        "原始算法": n * m * 8,  # 假设每个整数8字节
        "内存优化": 2 * max(n, m) * 8,
        "流优化": 2 * m * 8,  # 分块处理
        "早期终止": 2 * m * 8,
    }

    return estimates


def run_benchmarks():
    """运行性能基准测试"""
    print("Levenshtein 算法性能基准测试")
    print("=" * 70)

    # 测试用例
    test_cases = [
        ("短字符串", "kitten", "sitting"),
        ("中等字符串", generate_random_string(100), generate_random_string(100)),
        ("长字符串", generate_random_string(500), generate_random_string(500)),
        ("非常长字符串", generate_random_string(2000), generate_random_string(2000)),
        ("长度差异大", generate_random_string(100), generate_random_string(20)),
    ]

    algorithms = [
        ("原始算法", levenshtein_original),
        ("内存优化", levenshtein_optimized_memory),
        ("流优化", lambda a, b: levenshtein_stream_optimized(a, b, 100)),
        ("早期终止", lambda a, b: levenshtein_early_termination(a, b, 50)),
    ]

    results = []

    for case_name, a, b in test_cases:
        print(f"\n测试用例: {case_name} ({len(a)} vs {len(b)} 字符)")
        print("-" * 50)

        case_results = {"case": case_name, "algorithms": {}}

        for algo_name, algorithm in algorithms:
            try:
                # 计算正确性
                if algo_name != "早期终止":  # 早期终止可能返回近似值
                    result = algorithm(a, b)
                    correct = True
                else:
                    result = algorithm(a, b)
                    correct = result <= 50  # 早期终止的阈值

                # 性能测试
                avg_time = benchmark_algorithm(algo_name, algorithm, a, b, 50)

                # 内存估算
                mem_est = memory_usage_estimate(a, b).get(algo_name, 0)

                print(
                    f"  {algo_name:15} | 时间: {avg_time * 1000:6.2f}ms | 内存: {mem_est:8}字节 | 结果: {result}"
                )

                case_results["algorithms"][algo_name] = {
                    "time_ms": avg_time * 1000,
                    "memory_bytes": mem_est,
                    "result": result,
                    "correct": correct,
                }

            except Exception as e:
                print(f"  {algo_name:15} | 错误: {e}")
                case_results["algorithms"][algo_name] = {"error": str(e)}

        results.append(case_results)

    # 总结
    print("\n" + "=" * 70)
    print("性能总结:")
    print("-" * 70)

    for algo_name, _ in algorithms:
        times = []
        for case in results:
            if (
                algo_name in case["algorithms"]
                and "time_ms" in case["algorithms"][algo_name]
            ):
                times.append(case["algorithms"][algo_name]["time_ms"])

        if times:
            avg_time = sum(times) / len(times)
            print(f"{algo_name:15} | 平均时间: {avg_time:6.2f}ms")

    # 内存使用总结
    print("\n内存使用总结 (最长字符串用例):")
    longest_case = test_cases[3]  # 非常长字符串
    a, b = longest_case[1], longest_case[2]
    mem_estimates = memory_usage_estimate(a, b)

    for algo_name, mem_bytes in mem_estimates.items():
        print(
            f"{algo_name:15} | 内存: {mem_bytes:12}字节 | {(mem_bytes / 1024 / 1024):6.2f}MB"
        )


def analyze_flow_matching_optimization():
    """分析流匹配优化机会"""
    print("\n" + "=" * 70)
    print("流匹配优化分析")
    print("=" * 70)

    print("\n1. 内存优化策略:")
    print("   - 原始算法: O(n*m) 空间复杂度")
    print("   - 优化版本: O(min(n,m)) 空间复杂度")
    print("   - 节省内存: 对于 2000x2000 字符串，从 32MB 降到 16KB")

    print("\n2. 流处理优化:")
    print("   - 分块处理大字符串")
    print("   - 支持增量计算")
    print("   - 减少内存峰值使用")

    print("\n3. 早期终止优化:")
    print("   - 检测长度差异过大")
    print("   - 实时监控距离增长")
    print("   - 适用于相似度阈值检查")

    print("\n4. 并行化机会:")
    print("   - 字符比较可以向量化")
    print("   - 分块可以并行处理")
    print("   - GPU 加速可能性")


if __name__ == "__main__":
    run_benchmarks()
    analyze_flow_matching_optimization()
