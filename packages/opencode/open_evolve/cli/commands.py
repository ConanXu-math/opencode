"""
命令行命令模块
"""

import sys
import os
from pathlib import Path
import argparse

from ..core.auto_evaluator import AutoEvaluatorSystem


def quick_optimize():
    """快速优化 - 命令行接口"""
    parser = argparse.ArgumentParser(description="OpenEvolve快速优化")
    parser.add_argument("file", help="要优化的代码文件")
    parser.add_argument("--iterations", "-i", type=int, default=50, help="迭代次数")
    parser.add_argument("--output", "-o", default="quick_optimize", help="输出目录")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        return

    code = Path(args.file).read_text()

    print(f"🚀 开始优化: {args.file}")
    print(f"   迭代次数: {args.iterations}")
    print(f"   输出目录: {args.output}")

    # 运行优化
    system = AutoEvaluatorSystem()
    result = system.auto_evolve(code, args.iterations, args.output)

    if result and result.get("success"):
        print("\n✅ 优化完成!")
        print(f"   输出目录: {result['output_dir']}")

        # 显示优化结果
        optimized_file = Path(result["output_dir"]) / "best" / "best_program.py"
        if optimized_file.exists():
            print(f"\n📄 优化后代码:")
            print(optimized_file.read_text())
    else:
        print(f"❌ 优化失败: {result.get('error') if result else '未知错误'}")


def generate_evaluator():
    """生成评估器 - 命令行接口"""
    parser = argparse.ArgumentParser(description="生成OpenEvolve评估器")
    parser.add_argument("file", help="要分析的代码文件")
    parser.add_argument("--output", "-o", default="evaluator_output", help="输出目录")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        return

    code = Path(args.file).read_text()

    print(f"🔧 生成评估器: {args.file}")

    system = AutoEvaluatorSystem()
    result = system.generate_for_code(code, args.output)

    if result.get("success"):
        print(f"✅ 评估器已生成到: {args.output}/auto_evaluator.py")
        print(f"   代码文件: {result['code_path']}")
        print(f"   评估器: {result['evaluator_path']}")
    else:
        print(f"❌ 生成失败: {result.get('error')}")


def main():
    """主命令行入口"""
    parser = argparse.ArgumentParser(description="OpenEvolve Python Agent")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 快速优化命令
    optimize_parser = subparsers.add_parser("optimize", help="快速优化代码")
    optimize_parser.add_argument("file", help="要优化的代码文件")
    optimize_parser.add_argument(
        "--iterations", "-i", type=int, default=50, help="迭代次数"
    )
    optimize_parser.add_argument("--output", "-o", default="optimized", help="输出目录")

    # 生成评估器命令
    eval_parser = subparsers.add_parser("generate", help="生成评估器")
    eval_parser.add_argument("file", help="要分析的代码文件")
    eval_parser.add_argument("--output", "-o", default="evaluator", help="输出目录")

    # 交互式界面
    subparsers.add_parser("interactive", help="启动交互式界面")

    args = parser.parse_args()

    if args.command == "optimize":
        # 临时修改sys.argv以使用quick_optimize
        sys.argv = [
            sys.argv[0],
            args.file,
            f"--iterations={args.iterations}",
            f"--output={args.output}",
        ]
        quick_optimize()

    elif args.command == "generate":
        sys.argv = [sys.argv[0], args.file, f"--output={args.output}"]
        generate_evaluator()

    elif args.command == "interactive":
        from .interactive import OpenEvolveInteractive

        app = OpenEvolveInteractive()
        app.run()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
