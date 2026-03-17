#!/usr/bin/env python3
"""Test script for math paper analyzer."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.paper_analyzer import MathPaperAnalyzer


def test_ocr_only():
    """Test OCR processing without LLM."""
    print("=== 测试1: OCR处理测试 ===")

    # 创建测试PDF（简单文本）
    test_pdf = create_test_pdf()

    analyzer = MathPaperAnalyzer(
        ocr_url="https://edusys5.sii.edu.cn/ocr",
        llm_api_key=None,  # 无LLM，测试快速模式
        llm_base_url=None,
        llm_model=None,
    )

    try:
        # 测试PDF字节处理
        with open(test_pdf, "rb") as f:
            pdf_bytes = f.read()

        results = analyzer.analyze_pdf_bytes(
            pdf_bytes=pdf_bytes,
            paper_name="test_paper",
            mode="fast",
        )

        print(f"✓ OCR处理测试通过")
        print(f"  页数: {results['page_count']}")
        print(f"  章节数: {len(results['structure'].get('sections', []))}")
        print(f"  定理数: {len(results['structure'].get('theorems', []))}")

        # 清理测试文件
        os.remove(test_pdf)

        return True

    except Exception as e:
        print(f"✗ OCR处理测试失败: {e}")
        if os.path.exists(test_pdf):
            os.remove(test_pdf)
        return False


def test_structure_extraction():
    """Test structure extraction with mock pages."""
    print("\n=== 测试2: 结构提取测试 ===")

    from scripts.structure_analyzer import (
        extract_paper_structure,
        format_structure_for_display,
    )

    # 模拟OCR页面文本
    mock_pages = [
        "1. Introduction\nThis paper studies graph theory.",
        "2. Preliminaries\nDefinition 2.1: A graph G = (V, E)...",
        "Theorem 3.1: Every connected graph contains a spanning tree.",
        "Proof. We prove by induction...",
        "Key formula: $$|E| = n - 1$$ for trees.",
    ]

    try:
        # 快速模式（无LLM）
        structure = extract_paper_structure(
            pages=mock_pages,
            use_llm=False,
        )

        print(f"✓ 结构提取测试通过")
        print(f"  章节: {len(structure.get('sections', []))}")
        print(f"  定义: {len(structure.get('definitions', []))}")
        print(f"  定理: {len(structure.get('theorems', []))}")
        print(f"  证明: {len(structure.get('proofs', []))}")
        print(f"  公式: {len(structure.get('key_equations', []))}")

        # 测试格式化
        formatted = format_structure_for_display(structure)
        print(f"  格式化输出长度: {len(formatted)} 字符")

        return True

    except Exception as e:
        print(f"✗ 结构提取测试失败: {e}")
        return False


def test_analyzer_integration():
    """Test full analyzer integration."""
    print("\n=== 测试3: 完整集成测试 ===")

    # 创建更复杂的测试PDF内容
    test_content = """1. Introduction

This is a test mathematical paper about graph theory.

2. Definitions

Definition 2.1: A graph G = (V, E) consists of a vertex set V and an edge set E.

Definition 2.2: The degree of a vertex v is deg(v).

3. Theorems

Theorem 3.1: Every tree with n vertices has n-1 edges.

Proof. We prove by induction on n.

Lemma 3.2: In any graph, sum of degrees equals 2|E|.

Important formula: $$\sum_{v \in V} \deg(v) = 2|E|$$

4. Conclusion

This concludes our test paper."""

    # 保存为文本文件（模拟OCR结果）
    test_file = "test_paper_content.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test_content)

    try:
        # 模拟OCR页面
        mock_pages = [test_content]

        from scripts.structure_analyzer import extract_paper_structure

        structure = extract_paper_structure(
            pages=mock_pages,
            use_llm=False,
        )

        print(f"✓ 集成测试通过")
        print(f"  提取到的结构元素:")

        stats = [
            ("章节", "sections"),
            ("定义", "definitions"),
            ("定理", "theorems"),
            ("证明", "proofs"),
            ("公式", "key_equations"),
        ]

        for name, key in stats:
            count = len(structure.get(key, []))
            if count > 0:
                print(f"    - {name}: {count}")

        # 清理测试文件
        os.remove(test_file)

        return True

    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        if os.path.exists(test_file):
            os.remove(test_file)
        return False


def create_test_pdf():
    """Create a simple test PDF file."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        test_pdf = "test_math_paper.pdf"

        c = canvas.Canvas(test_pdf, pagesize=letter)
        width, height = letter

        # 第一页：标题和摘要
        c.setFont("Helvetica", 16)
        c.drawString(100, height - 100, "Test Mathematical Paper")

        c.setFont("Helvetica", 12)
        c.drawString(
            100,
            height - 150,
            "Abstract: This is a test paper for the math paper analyzer.",
        )

        # 第二页：定义和定理
        c.showPage()
        c.setFont("Helvetica", 14)
        c.drawString(100, height - 100, "2. Definitions")

        c.setFont("Helvetica", 12)
        c.drawString(100, height - 150, "Definition 2.1: A test definition.")
        c.drawString(100, height - 180, "Definition 2.2: Another test definition.")

        # 第三页：定理和证明
        c.showPage()
        c.setFont("Helvetica", 14)
        c.drawString(100, height - 100, "3. Theorems")

        c.setFont("Helvetica", 12)
        c.drawString(100, height - 150, "Theorem 3.1: Test theorem statement.")
        c.drawString(100, height - 180, "Proof. Test proof by contradiction.")

        c.save()

        return test_pdf

    except ImportError:
        # 如果没有reportlab，创建文本文件
        test_pdf = "test_math_paper.txt"
        with open(test_pdf, "w", encoding="utf-8") as f:
            f.write("Test Mathematical Paper\n\n")
            f.write("1. Introduction\n")
            f.write("This is a test paper.\n\n")
            f.write("Definition 2.1: Test definition.\n")
            f.write("Theorem 3.1: Test theorem.\n")
            f.write("Proof. Test proof.\n")

        return test_pdf


def main():
    """Run all tests."""
    print("数学论文分析器测试套件")
    print("=" * 50)

    tests = [
        ("OCR处理测试", test_ocr_only),
        ("结构提取测试", test_structure_extraction),
        ("完整集成测试", test_analyzer_integration),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"{test_name} 异常: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("测试结果汇总:")

    all_passed = True
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name:20} {status}")
        if not success:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("所有测试通过！")
        return 0
    else:
        print("部分测试失败，请检查配置和依赖。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
