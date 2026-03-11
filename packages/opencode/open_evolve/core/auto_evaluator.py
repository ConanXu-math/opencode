"""
自动评估器系统模块
主协调器
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import subprocess
import sys

from .analyzer import CodeAnalyzer
from .evaluator_builder import EvaluatorBuilder


class AutoEvaluatorSystem:
    """自动评估器系统 - 主协调器"""

    def __init__(self, config_path: Optional[str] = None):
        self.analyzer = CodeAnalyzer()
        self.builder = EvaluatorBuilder(config_path)

    def generate_for_code(
        self, code: str, output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """为给定代码生成评估器"""

        # 分析代码
        analysis = self.analyzer.analyze(code)

        if "error" in analysis:
            return {"error": analysis["error"]}

        if not analysis["functions"]:
            return {"error": "代码中没有找到函数定义"}

        # 创建临时文件保存代码
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            code_path = f.name

        try:
            # 生成评估器
            evaluator_code = self.builder.build(code_path, analysis)

            # 保存评估器
            if output_dir:
                output_path = Path(output_dir) / "auto_evaluator.py"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(evaluator_code)

                # 也保存代码文件
                code_output = Path(output_dir) / "target_code.py"
                code_output.write_text(code)

                return {
                    "success": True,
                    "code_path": str(code_output),
                    "evaluator_path": str(output_path),
                    "analysis": analysis,
                    "evaluator_code": evaluator_code,
                }
            else:
                return {
                    "success": True,
                    "code_path": code_path,
                    "evaluator_code": evaluator_code,
                    "analysis": analysis,
                }

        finally:
            # 清理临时文件
            try:
                os.unlink(code_path)
            except:
                pass

    def auto_evolve(
        self, code: str, iterations: int = 50, output_dir: str = "auto_evolution"
    ) -> Dict[str, Any]:
        """一键自动进化 - 自动生成评估器并运行OpenEvolve"""

        print("🚀 开始自动进化流程...")

        # 1. 生成评估器
        result = self.generate_for_code(code, output_dir)

        if not result.get("success"):
            print(f"❌ 评估器生成失败: {result.get('error')}")
            return None

        code_path = result["code_path"]
        evaluator_path = result["evaluator_path"]

        print(f"✅ 评估器生成完成")
        print(f"   目标代码: {code_path}")
        print(f"   评估器: {evaluator_path}")

        # 2. 运行OpenEvolve
        print(f"🔧 运行OpenEvolve进化 ({iterations}次迭代)...")

        try:
            # 使用配置好的环境
            config_path = "/Users/conanxu/Desktop/ai_math_agent/opencode/packages/opencode/openevolve_fixed_config.yaml"

            cmd = [
                sys.executable,
                "-m",
                "openevolve.cli",
                code_path,
                evaluator_path,
                "--config",
                config_path,
                "--iterations",
                str(iterations),
                "--output",
                str(Path(output_dir) / "results"),
            ]

            # 运行命令
            process = subprocess.run(
                cmd, capture_output=True, text=True, cwd=Path(output_dir).parent
            )

            if process.returncode == 0:
                print("✅ 进化完成!")

                # 读取结果
                result_file = Path(output_dir) / "results" / "best" / "best_program.py"
                if result_file.exists():
                    optimized_code = result_file.read_text()
                    print(f"\n📄 优化后代码:")
                    print(optimized_code)

                    return {
                        "success": True,
                        "original_code": code,
                        "optimized_code": optimized_code,
                        "output_dir": str(Path(output_dir) / "results"),
                    }
                else:
                    print("⚠️  未找到优化结果文件")
                    return {"success": False, "error": "结果文件未生成"}
            else:
                print(f"❌ OpenEvolve运行失败:")
                print(f"   错误: {process.stderr}")
                return {"success": False, "error": process.stderr}

        except Exception as e:
            print(f"❌ 运行失败: {e}")
            return {"success": False, "error": str(e)}
