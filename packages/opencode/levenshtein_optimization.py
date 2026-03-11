#!/usr/bin/env python3
"""
Levenshtein 距离算法优化示例
使用 OpenEvolve 进行流匹配优化
"""


def levenshtein_original(a: str, b: str) -> int:
    """原始 Levenshtein 算法实现"""
    if a == "" or b == "":
        return max(len(a), len(b))

    # 创建二维矩阵
    matrix = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

    # 初始化第一行和第一列
    for i in range(len(a) + 1):
        matrix[i][0] = i
    for j in range(len(b) + 1):
        matrix[0][j] = j

    # 填充矩阵
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,  # 删除
                matrix[i][j - 1] + 1,  # 插入
                matrix[i - 1][j - 1] + cost,  # 替换
            )

    return matrix[len(a)][len(b)]


def levenshtein_optimized_memory(a: str, b: str) -> int:
    """优化内存版本的 Levenshtein 算法"""
    if len(a) < len(b):
        return levenshtein_optimized_memory(b, a)

    if len(b) == 0:
        return len(a)

    # 使用两行滚动数组
    previous_row = list(range(len(b) + 1))
    current_row = [0] * (len(b) + 1)

    for i, char_a in enumerate(a, 1):
        current_row[0] = i
        for j, char_b in enumerate(b, 1):
            cost = 0 if char_a == char_b else 1
            current_row[j] = min(
                previous_row[j] + 1,  # 删除
                current_row[j - 1] + 1,  # 插入
                previous_row[j - 1] + cost,  # 替换
            )

        # 交换行
        previous_row, current_row = current_row, previous_row

    return previous_row[len(b)]


def levenshtein_stream_optimized(a: str, b: str, chunk_size: int = 100) -> int:
    """
    流优化版本的 Levenshtein 算法
    支持分块处理大字符串
    """
    if len(a) < len(b):
        return levenshtein_stream_optimized(b, a, chunk_size)

    if len(b) == 0:
        return len(a)

    # 初始化第一行
    previous_row = list(range(len(b) + 1))

    # 分块处理字符串 a
    for i in range(0, len(a), chunk_size):
        chunk = a[i : i + chunk_size]
        current_row = [0] * (len(b) + 1)

        for chunk_idx, char_a in enumerate(chunk, 1):
            global_i = i + chunk_idx
            current_row[0] = global_i

            for j, char_b in enumerate(b, 1):
                cost = 0 if char_a == char_b else 1
                current_row[j] = min(
                    previous_row[j] + 1,  # 删除
                    current_row[j - 1] + 1,  # 插入
                    previous_row[j - 1] + cost,  # 替换
                )

            # 更新 previous_row 为当前行（除了最后一个元素）
            if chunk_idx < len(chunk):
                previous_row = current_row.copy()
            else:
                previous_row = current_row

    return previous_row[len(b)]


def levenshtein_early_termination(a: str, b: str, max_distance: int = 10) -> int:
    """
    带早期终止的 Levenshtein 算法
    如果距离超过阈值，提前返回
    """
    if max_distance is None:
        max_distance = max(len(a), len(b))

    # 快速检查长度差异
    if abs(len(a) - len(b)) > max_distance:
        return abs(len(a) - len(b))

    if len(a) < len(b):
        return levenshtein_early_termination(b, a, max_distance)

    if len(b) == 0:
        return len(a)

    # 使用两行滚动数组
    previous_row = list(range(len(b) + 1))
    current_row = [0] * (len(b) + 1)

    for i, char_a in enumerate(a, 1):
        current_row[0] = i
        row_min = float("inf")

        for j, char_b in enumerate(b, 1):
            cost = 0 if char_a == char_b else 1
            current_row[j] = min(
                previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1] + cost
            )
            row_min = min(row_min, current_row[j])

        # 如果当前行最小值已经超过最大距离，提前终止
        if row_min > max_distance:
            return max_distance + 1

        previous_row, current_row = current_row, previous_row

    distance = previous_row[len(b)]
    return distance if distance <= max_distance else max_distance + 1


# 测试函数
def test_levenshtein_algorithms():
    """测试所有 Levenshtein 算法变体"""
    test_cases = [
        ("kitten", "sitting", 3),
        ("", "abc", 3),
        ("abc", "", 3),
        ("abc", "abc", 0),
        ("abc", "def", 3),
        ("a" * 100, "b" * 100, 100),  # 长字符串测试
        ("abcdef", "abcfed", 2),  # 部分匹配
    ]

    algorithms = [
        ("原始算法", levenshtein_original),
        ("内存优化", levenshtein_optimized_memory),
        ("流优化", lambda a, b: levenshtein_stream_optimized(a, b, 10)),
        ("早期终止", lambda a, b: levenshtein_early_termination(a, b, 10)),
    ]

    print("Levenshtein 算法测试结果:")
    print("=" * 60)

    for name, algorithm in algorithms:
        print(f"\n{name}:")
        all_correct = True

        for a, b, expected in test_cases:
            try:
                result = algorithm(a, b)
                correct = result == expected
                if not correct:
                    all_correct = False
                status = "✓" if correct else "✗"
                print(f"  {status} '{a}' -> '{b}': 期望={expected}, 实际={result}")
            except Exception as e:
                all_correct = False
                print(f"  ✗ '{a}' -> '{b}': 错误={e}")

        print(f"  所有测试: {'通过' if all_correct else '失败'}")


if __name__ == "__main__":
    test_levenshtein_algorithms()
