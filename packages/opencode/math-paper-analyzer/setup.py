#!/usr/bin/env python3
"""Setup script for math paper analyzer."""

import subprocess
import sys


def install_dependencies():
    """Install required dependencies."""
    print("正在安装依赖...")

    dependencies = [
        "pymupdf>=1.24.0",
        "openai>=1.0.0",
        "httpx>=0.27.0",
        "python-dotenv>=1.0.0",
    ]

    for dep in dependencies:
        print(f"安装 {dep}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ {dep} 安装成功")
        except subprocess.CalledProcessError:
            print(f"✗ {dep} 安装失败")
            return False

    return True


def test_imports():
    """Test if all imports work."""
    print("\n测试导入...")

    imports_to_test = [
        ("fitz", "pymupdf"),
        ("openai", "openai"),
        ("httpx", "httpx"),
    ]

    all_imports_ok = True
    for import_name, package_name in imports_to_test:
        try:
            __import__(import_name)
            print(f"✓ {package_name} 导入成功")
        except ImportError:
            print(f"✗ {package_name} 导入失败")
            all_imports_ok = False

    return all_imports_ok


def test_basic_functionality():
    """Test basic functionality without OCR."""
    print("\n测试基本功能...")

    try:
        # 测试结构分析器
        from scripts.structure_analyzer import (
            extract_paper_structure,
            format_structure_for_display,
        )

        # 创建测试页面
        test_pages = [
            "1. Introduction\nTest paper.",
            "Definition 2.1: A test definition.",
            "Theorem 3.1: Test theorem statement.",
            "Proof. Test proof.",
            "Formula: $$E = mc^2$$",
        ]

        # 测试结构提取
        structure = extract_paper_structure(test_pages, use_llm=False)

        print(f"✓ 结构提取测试通过")
        print(f"  提取到 {len(structure.get('sections', []))} 个章节")
        print(f"  提取到 {len(structure.get('definitions', []))} 个定义")
        print(f"  提取到 {len(structure.get('theorems', []))} 个定理")
        print(f"  提取到 {len(structure.get('proofs', []))} 个证明")
        print(f"  提取到 {len(structure.get('key_equations', []))} 个公式")

        # 测试格式化
        formatted = format_structure_for_display(structure)
        print(f"✓ 格式化测试通过，输出长度: {len(formatted)} 字符")

        return True

    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False


def main():
    """Main setup function."""
    print("数学论文分析技能设置")
    print("=" * 50)

    # 安装依赖
    if not install_dependencies():
        print("\n依赖安装失败，请手动安装。")
        return 1

    # 测试导入
    if not test_imports():
        print("\n导入测试失败，请检查依赖。")
        return 1

    # 测试基本功能
    if not test_basic_functionality():
        print("\n基本功能测试失败。")
        return 1

    print("\n" + "=" * 50)
    print("设置完成！")
    print("\n使用方法:")
    print("  快速模式: python scripts/cli.py paper.pdf --mode fast")
    print(
        "  标准模式: python scripts/cli.py paper.pdf --mode standard --llm-api-key KEY --llm-base-url URL"
    )
    print(
        "  深度模式: python scripts/cli.py paper.pdf --mode deep --llm-api-key KEY --llm-base-url URL"
    )
    print("\n更多信息请查看 README.md 和 SKILL.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
