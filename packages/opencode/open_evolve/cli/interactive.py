"""
交互式界面模块
"""

import sys
import os
from pathlib import Path
import json
from typing import Dict, List, Optional

from ..core.auto_evaluator import AutoEvaluatorSystem


class OpenEvolveInteractive:
    """OpenEvolve交互式界面"""

    def __init__(self):
        self.config_path = "/Users/conanxu/Desktop/ai_math_agent/opencode/packages/opencode/openevolve_fixed_config.yaml"

    def show_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 60)
        print("🚀 OpenEvolve Python Agent - 交互式界面")
        print("=" * 60)
        print("\n请选择操作:")
        print("1. 🔍 分析代码并生成评估器")
        print("2. ⚡ 一键优化代码")
        print("3. 📊 查看优化历史")
        print("4. 🛠️  手动配置优化")
        print("5. 📚 查看使用示例")
        print("6. 🚪 退出")
        print("\n" + "-" * 60)

    def analyze_code(self):
        """分析代码"""
        print("\n📝 分析代码功能")
        print("请提供要分析的代码:")
        print("1. 输入文件路径")
        print("2. 直接粘贴代码")
        print("3. 返回")

        choice = input("\n选择: ").strip()

        if choice == "1":
            path = input("文件路径: ").strip()
            if os.path.exists(path):
                code = Path(path).read_text()
                self._analyze_and_generate(code, path)
            else:
                print("❌ 文件不存在")

        elif choice == "2":
            print("\n请粘贴代码 (输入空行结束):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            code = "\n".join(lines)
            self._analyze_and_generate(code, "pasted_code.py")

    def _analyze_and_generate(self, code: str, source_name: str):
        """分析并生成评估器"""
        print(f"\n🔧 分析代码: {source_name}")

        system = AutoEvaluatorSystem()
        result = system.generate_for_code(code, "interactive_output")

        if result.get("success"):
            print("✅ 评估器生成成功!")
            print(f"   代码文件: {result['code_path']}")
            print(f"   评估器: {result['evaluator_path']}")

            # 显示分析结果
            analysis = result["analysis"]
            print(f"\n📊 代码分析:")
            print(f"   函数: {[f['name'] for f in analysis['functions']]}")
            print(f"   复杂度: {analysis['complexity']}")

            # 询问是否立即优化
            optimize = input("\n⚡ 是否立即运行优化? (y/n): ").lower()
            if optimize == "y":
                self._run_optimization(result["code_path"], result["evaluator_path"])
        else:
            print(f"❌ 生成失败: {result.get('error')}")

    def one_click_optimize(self):
        """一键优化"""
        print("\n⚡ 一键优化代码")
        print("请提供要优化的代码:")

        path = input("代码文件路径: ").strip()
        if not os.path.exists(path):
            print("❌ 文件不存在")
            return

        code = Path(path).read_text()

        # 询问优化参数
        print("\n🔧 优化参数:")
        iterations = input("迭代次数 (默认50): ").strip()
        iterations = int(iterations) if iterations else 50

        output_dir = input("输出目录 (默认optimized_output): ").strip()
        output_dir = output_dir if output_dir else "optimized_output"

        print(f"\n🚀 开始优化...")
        print(f"   迭代次数: {iterations}")
        print(f"   输出目录: {output_dir}")

        # 运行优化
        system = AutoEvaluatorSystem()
        result = system.auto_evolve(code, iterations, output_dir)

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

    def view_history(self):
        """查看优化历史"""
        print("\n📊 优化历史")

        # 查找输出目录
        output_dirs = []
        for item in Path(".").iterdir():
            if item.is_dir() and any(
                x in item.name.lower() for x in ["output", "results", "optimized"]
            ):
                output_dirs.append(item)

        if not output_dirs:
            print("暂无优化历史")
            return

        print("找到的优化结果:")
        for i, dir_path in enumerate(output_dirs[:10], 1):
            print(f"{i}. {dir_path.name}")

        choice = input("\n选择查看的目录编号 (0返回): ").strip()
        if choice == "0":
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(output_dirs):
                self._show_optimization_details(output_dirs[idx])
        except ValueError:
            print("❌ 无效选择")

    def _show_optimization_details(self, dir_path: Path):
        """显示优化详情"""
        best_file = dir_path / "best" / "best_program.py"
        info_file = dir_path / "best" / "best_program_info.json"

        if best_file.exists():
            print(f"\n📄 优化后代码 ({best_file}):")
            print(best_file.read_text())

        if info_file.exists():
            print(f"\n📊 优化指标:")
            info = json.loads(info_file.read_text())
            metrics = info.get("metrics", {})
            for key, value in metrics.items():
                print(f"   {key}: {value}")

    def manual_config(self):
        """手动配置"""
        print("\n🛠️  手动配置优化")
        print("1. 编辑配置文件")
        print("2. 创建新配置")
        print("3. 测试配置")
        print("4. 返回")

        choice = input("\n选择: ").strip()

        if choice == "1":
            self._edit_config()
        elif choice == "2":
            self._create_config()
        elif choice == "3":
            self._test_config()

    def _edit_config(self):
        """编辑配置文件"""
        config_path = self.config_path
        if os.path.exists(config_path):
            print(f"\n编辑配置文件: {config_path}")
            print("当前内容:")
            print(Path(config_path).read_text())

            edit = input("\n是否编辑? (y/n): ").lower()
            if edit == "y":
                print(f"请手动编辑: {config_path}")
        else:
            print("❌ 配置文件不存在")

    def _create_config(self):
        """创建新配置"""
        print("\n创建新配置文件")
        model = input("LLM模型 (默认deepseek-chat): ").strip() or "deepseek-chat"
        api_key = input("API密钥: ").strip()
        api_base = (
            input("API地址 (默认https://api.deepseek.com/v1): ").strip()
            or "https://api.deepseek.com/v1"
        )

        config = f"""# OpenEvolve 配置文件
llm:
  models:
    - name: "{model}"
      api_key: "{api_key}"
      api_base: "{api_base}"
      temperature: 0.7
      max_tokens: 4000
  api_base: "{api_base}"
  temperature: 0.7
  max_tokens: 4000

evolution:
  population_size: 50
  num_islands: 3
  crossover_rate: 0.8
  mutation_rate: 0.2
  elitism_count: 5
  max_program_length: 1000

evaluation:
  timeout_seconds: 30
  max_memory_mb: 1024
  cascade_evaluation: false

logging:
  level: "INFO"
  file: "evolution.log"

prompt:
  system_template: "evaluator_system_message"
  user_template: null
"""

        save_path = (
            input("保存路径 (默认new_config.yaml): ").strip() or "new_config.yaml"
        )
        Path(save_path).write_text(config)
        print(f"✅ 配置文件已保存: {save_path}")

    def _test_config(self):
        """测试配置"""
        print("\n测试配置文件")
        config_path = input("配置文件路径: ").strip()

        if not os.path.exists(config_path):
            print("❌ 文件不存在")
            return

        print(f"测试配置文件: {config_path}")
        print(Path(config_path).read_text())

    def show_examples(self):
        """显示示例"""
        print("\n📚 使用示例")
        print("\n1. 优化排序算法:")
        print("""
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
""")

        print("\n2. 优化数值计算:")
        print("""
def slow_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
""")

        print("\n3. 优化图像处理:")
        print("""
def process_image(pixels):
    result = []
    for row in pixels:
        new_row = []
        for pixel in row:
            # 复杂处理
            processed = pixel * 0.5 + 128
            new_row.append(processed)
        result.append(new_row)
    return result
""")

        input("\n按Enter继续...")

    def _run_optimization(self, code_path: str, evaluator_path: str):
        """运行优化"""
        import subprocess

        print(f"\n🚀 运行OpenEvolve优化...")

        iterations = input("迭代次数 (默认30): ").strip()
        iterations = int(iterations) if iterations else 30

        output_dir = input("输出目录 (默认optimization_run): ").strip()
        output_dir = output_dir if output_dir else "optimization_run"

        cmd = [
            sys.executable,
            "-m",
            "openevolve.cli",
            code_path,
            evaluator_path,
            "--config",
            self.config_path,
            "--iterations",
            str(iterations),
            "--output",
            output_dir,
        ]

        print(f"\n执行命令:")
        print(" ".join(cmd))

        try:
            process = subprocess.run(
                cmd, capture_output=True, text=True, cwd=Path(code_path).parent
            )

            if process.returncode == 0:
                print("✅ 优化完成!")

                # 显示结果
                result_file = Path(output_dir) / "best" / "best_program.py"
                if result_file.exists():
                    print(f"\n📄 优化后代码:")
                    print(result_file.read_text())
            else:
                print(f"❌ 优化失败:")
                print(process.stderr)

        except Exception as e:
            print(f"❌ 运行失败: {e}")

    def run(self):
        """运行交互界面"""
        while True:
            self.show_menu()
            choice = input("\n请选择 (1-6): ").strip()

            if choice == "1":
                self.analyze_code()
            elif choice == "2":
                self.one_click_optimize()
            elif choice == "3":
                self.view_history()
            elif choice == "4":
                self.manual_config()
            elif choice == "5":
                self.show_examples()
            elif choice == "6":
                print("\n👋 再见!")
                break
            else:
                print("❌ 无效选择")

            input("\n按Enter继续...")
