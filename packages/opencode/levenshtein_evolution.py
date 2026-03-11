#!/usr/bin/env python3
"""
Levenshtein 算法进化优化
使用 OpenEvolve 进行自动优化
"""

import sys
import os

# 添加 OpenEvolve 到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from open_evolve.core.auto_evaluator import AutoEvaluatorSystem

# 初始 Levenshtein 算法实现
INITIAL_CODE = '''
def levenshtein(a: str, b: str) -> int:
    """计算两个字符串之间的 Levenshtein 编辑距离"""
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
            cost = 0 if a[i-1] == b[j-1] else 1
            matrix[i][j] = min(
                matrix[i-1][j] + 1,      # 删除
                matrix[i][j-1] + 1,      # 插入
                matrix[i-1][j-1] + cost  # 替换
            )
    
    return matrix[len(a)][len(b)]
'''

# 优化目标描述
OPTIMIZATION_TARGET = """
优化 Levenshtein 编辑距离算法，使其：

1. **提高性能**：减少计算时间，特别是对于长字符串
2. **降低内存使用**：避免创建完整的二维矩阵
3. **保持准确性**：确保计算结果完全正确
4. **添加优化特性**：
   - 早期终止（当距离超过阈值时）
   - 流式处理（支持分块计算）
   - 内存优化（使用滚动数组）

优化方向：
- 使用两行滚动数组代替完整矩阵
- 实现早期终止检测
- 添加长度差异快速检查
- 考虑 SIMD 或并行化机会
- 实现分块处理支持大字符串

评估标准：
1. 准确性（必须100%正确）
2. 性能（运行时间越短越好）
3. 内存效率（使用内存越少越好）
4. 代码复杂度（代码越简洁越好）
"""


def main():
    """主函数：运行 Levenshtein 算法进化优化"""
    print("=" * 70)
    print("Levenshtein 算法进化优化")
    print("=" * 70)

    print("\n初始算法:")
    print("-" * 40)
    print(INITIAL_CODE)

    print("\n优化目标:")
    print("-" * 40)
    print(OPTIMIZATION_TARGET)

    # 创建自动评估系统
    print("\n创建 OpenEvolve 自动评估系统...")
    system = AutoEvaluatorSystem()

    # 运行进化优化
    print("\n开始进化优化...")
    print("这可能需要几分钟时间，请耐心等待...")

    try:
        result = system.auto_evolve(
            code=INITIAL_CODE,
            iterations=30,  # 进化迭代次数
        )

        print("\n" + "=" * 70)
        print("优化完成!")
        print("=" * 70)

        if result.get("success"):
            print(f"\n最佳算法得分: {result.get('best_score', 0):.4f}")
            print(f"\n优化后的代码:")
            print("-" * 40)
            print(result.get("best_code", ""))

            # 保存优化结果
            output_dir = "levenshtein_optimized"
            os.makedirs(output_dir, exist_ok=True)

            best_code_file = os.path.join(output_dir, "best_levenshtein.py")
            with open(best_code_file, "w") as f:
                f.write(result.get("best_code", ""))

            print(f"\n优化结果已保存到: {best_code_file}")

            # 显示优化指标
            if "metrics" in result:
                print("\n优化指标:")
                print("-" * 40)
                for key, value in result["metrics"].items():
                    print(f"  {key}: {value}")

        else:
            print(f"\n优化失败: {result.get('error', '未知错误')}")

    except Exception as e:
        print(f"\n优化过程中出现错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
