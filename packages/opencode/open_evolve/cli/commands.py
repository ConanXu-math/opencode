"""
命令行命令模块
"""

import sys
import os
import time
from pathlib import Path
import argparse

from ..core.auto_evaluator import AutoEvaluatorSystem


def main():
    """主命令行入口 - 统一接口"""
    parser = argparse.ArgumentParser(description="OpenEvolve Unified Agent")
    parser.add_argument("file", help="要优化的Python文件或代码片段")
    parser.add_argument("--iteration", "-i", type=int, default=50, help="迭代次数")
    parser.add_argument("--outdir", "-o", help="输出目录")
    parser.add_argument(
        "--mode",
        "-m",
        choices=["optimize", "analyze", "discover"],
        default="optimize",
        help="运行模式",
    )

    args = parser.parse_args()

    # 检查是否是文件路径
    if os.path.exists(args.file):
        # 文件模式 - 运行优化
        if not args.outdir:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(os.path.basename(args.file))[0]
            args.outdir = f"optimized_{base_name}_{timestamp}"

        code = Path(args.file).read_text()

        print(f"🔧 OpenEvolve 统一优化接口")
        print(f"   输入文件: {args.file}")
        print(f"   迭代次数: {args.iteration}")
        print(f"   输出目录: {args.outdir}")
        print(f"   运行模式: {args.mode}")

        # 运行优化
        system = AutoEvaluatorSystem()
        result = system.auto_evolve(code, args.iteration, args.outdir)

        if result and result.get("success"):
            print("\n✅ 优化完成!")

            # 创建标准输出结构
            output_dir = Path(result["output_dir"])
            best_dir = output_dir / "best"
            logs_dir = output_dir / "logs"

            best_dir.mkdir(exist_ok=True)
            logs_dir.mkdir(exist_ok=True)

            # 移动最佳程序
            best_program = output_dir / "best_program.py"
            if best_program.exists():
                target = best_dir / "best_program.py"
                best_program.rename(target)

                # 创建 metrics.json
                metrics = {
                    "file": args.file,
                    "iterations": args.iteration,
                    "output_dir": str(output_dir),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "optimization_success": True,
                    "mode": args.mode,
                }

                metrics_file = best_dir / "metrics.json"
                import json

                metrics_file.write_text(json.dumps(metrics, indent=2))

            # 创建总结文件
            summary = output_dir / "summary.md"
            summary_content = f"""# OpenEvolve 优化总结

## 优化详情
- **输入文件**: {args.file}
- **迭代次数**: {args.iteration}
- **输出目录**: {output_dir}
- **运行模式**: {args.mode}
- **完成时间**: {time.strftime("%Y-%m-%d %H:%M:%S")}

## 输出结构
```
{output_dir}/
├── best/
│   ├── best_program.py      # 优化后的程序
│   └── metrics.json         # 性能指标
├── logs/
│   └── evolution.log        # 进化过程日志
└── summary.md              # 本总结文件
```

## 使用优化结果
1. 查看优化后的代码: `{best_dir}/best_program.py`
2. 检查性能指标: `{best_dir}/metrics.json`
3. 查看进化过程: `{logs_dir}/evolution.log`

## 下一步
- 测试优化后的代码功能
- 对比优化前后的性能
- 考虑进一步优化机会
"""
            summary.write_text(summary_content)

            # 创建配置文件
            config = output_dir / "config.yaml"
            config_content = f"""# OpenEvolve 配置
llm:
  model: "deepseek-chat"
  temperature: 0.7
  max_tokens: 4000

evolution:
  population_size: 50
  num_islands: 3
  crossover_rate: 0.8
  mutation_rate: 0.2
  elitism_count: 5

evaluation:
  timeout_seconds: 30
  max_memory_mb: 1024

# 运行参数
run:
  file: {args.file}
  iterations: {args.iteration}
  output_dir: {output_dir}
  mode: {args.mode}
"""
            config.write_text(config_content)

            print(f"   输出目录: {output_dir}")
            print(f"   最佳程序: {best_dir}/best_program.py")
            print(f"   优化总结: {summary}")

            # 显示优化结果
            best_file = best_dir / "best_program.py"
            if best_file.exists():
                print(f"\n📄 优化后代码预览:")
                print("-" * 50)
                print(
                    best_file.read_text()[:500] + "..."
                    if len(best_file.read_text()) > 500
                    else best_file.read_text()
                )
                print("-" * 50)
        else:
            print(f"❌ 优化失败: {result.get('error') if result else '未知错误'}")
    else:
        # 代码分析模式
        print(f"🔍 OpenEvolve 代码分析模式")
        print(
            f"   输入代码: {args.file[:100]}..."
            if len(args.file) > 100
            else f"   输入代码: {args.file}"
        )
        print(f"   运行模式: {args.mode}")

        # 代码分析逻辑
        system = AutoEvaluatorSystem()

        # 尝试分析代码
        try:
            analysis = system.analyzer.analyze(args.file)

            if analysis and "functions" in analysis:
                print("\n📊 分析结果:")
                print(f"   函数数量: {len(analysis['functions'])}")

                if analysis.get("complexity"):
                    print(f"   代码复杂度: {analysis['complexity']}")

                if analysis.get("suggestions"):
                    print(f"   优化建议: {analysis['suggestions']}")

                # 显示函数信息
                for i, func in enumerate(analysis["functions"][:3]):  # 只显示前3个函数
                    print(f"   函数 {i + 1}: {func.get('name', '匿名函数')}")
            else:
                print("📝 代码分析完成，但未发现具体优化建议")
        except Exception as e:
            print(f"❌ 代码分析失败: {e}")


if __name__ == "__main__":
    main()
