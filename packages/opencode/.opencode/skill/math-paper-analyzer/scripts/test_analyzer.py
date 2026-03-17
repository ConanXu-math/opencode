"""Test script for Math Paper Analyzer."""

import os
import sys
import tempfile
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from paper_analyzer import PaperAnalyzer


def test_ocr_pdf_reader():
    """Test OCR PDF Reader functionality."""
    print("Testing OCR PDF Reader...")

    from ocr_pdf_reader import OcrPDFReader

    # Create a simple PDF for testing (if available)
    test_pdf = None
    for ext in [".pdf", ".PDF"]:
        pdf_files = list(Path(".").glob(f"*{ext}"))
        if pdf_files:
            test_pdf = pdf_files[0]
            break

    if not test_pdf:
        print("  ⚠ No PDF files found for testing")
        return False

    print(f"  Using test PDF: {test_pdf.name}")

    try:
        reader = OcrPDFReader(max_workers=1)
        pages = reader.read(test_pdf)

        print(f"  ✓ OCR completed: {len(pages)} pages")
        print(f"  First page preview: {pages[0][:100]}..." if pages else "  No content")

        return True
    except Exception as e:
        print(f"  ✗ OCR failed: {type(e).__name__}: {e}")
        return False


def test_structure_extractor():
    """Test structure extractor functionality."""
    print("\nTesting Structure Extractor...")

    from structure_extractor import (
        extract_paper_structure,
        format_structure_for_display,
    )

    # Create sample OCR text
    sample_pages = [
        "1. Introduction\nThis paper studies graph theory.",
        "2. Preliminaries\nDefinition 2.1 A graph G = (V, E).",
        "Theorem 3.1 Every graph has a spanning tree.\nProof. By induction.",
    ]

    try:
        # Test regex extraction (fast mode)
        structure = extract_paper_structure(sample_pages)

        print(f"  ✓ Structure extraction completed")
        print(f"  Sections: {len(structure.get('sections', []))}")
        print(f"  Theorems: {len(structure.get('theorems', []))}")
        print(f"  Definitions: {len(structure.get('definitions', []))}")

        # Test formatting
        formatted = format_structure_for_display(structure)
        print(f"  ✓ Formatting completed ({len(formatted)} chars)")

        return True
    except Exception as e:
        print(f"  ✗ Structure extraction failed: {type(e).__name__}: {e}")
        return False


def test_paper_analyzer_fast_mode():
    """Test PaperAnalyzer in fast mode."""
    print("\nTesting PaperAnalyzer (Fast Mode)...")

    # Create analyzer
    analyzer = PaperAnalyzer()

    # Find a test PDF
    test_pdf = None
    for ext in [".pdf", ".PDF"]:
        pdf_files = list(Path(".").glob(f"*{ext}"))
        if pdf_files:
            test_pdf = pdf_files[0]
            break

    if not test_pdf:
        print("  ⚠ No PDF files found for testing")
        return False

    print(f"  Using test PDF: {test_pdf.name}")

    try:
        # Test fast mode
        result = analyzer.analyze(
            test_pdf,
            mode="fast",
            save_output=False,
        )

        if result["success"]:
            print(f"  ✓ Fast mode analysis successful")
            print(f"    Pages: {result['pages']}")
            print(f"    Duration: {result['duration_seconds']:.1f}s")
            print(f"    Has structure: {bool(result.get('structure'))}")
            return True
        else:
            print(f"  ✗ Analysis failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"  ✗ Analysis failed: {type(e).__name__}: {e}")
        return False


def test_configuration():
    """Test configuration options."""
    print("\nTesting Configuration...")

    try:
        # Test with custom temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            analyzer = PaperAnalyzer(
                ocr_url="https://edusys5.sii.edu.cn/ocr",
                temp_dir=temp_dir,
            )

            print(f"  ✓ Analyzer created with custom temp dir: {temp_dir}")
            print(f"    OCR URL: {analyzer.ocr_url}")
            print(f"    Has LLM: {analyzer.has_llm}")

            return True
    except Exception as e:
        print(f"  ✗ Configuration test failed: {type(e).__name__}: {e}")
        return False


def test_error_handling():
    """Test error handling."""
    print("\nTesting Error Handling...")

    analyzer = PaperAnalyzer()

    # Test with non-existent file
    try:
        result = analyzer.analyze(
            "non_existent_file.pdf", mode="fast", save_output=False
        )
        if not result["success"]:
            print(f"  ✓ Properly handled non-existent file: {result.get('error')}")
        else:
            print(f"  ✗ Should have failed for non-existent file")
            return False
    except Exception as e:
        print(f"  ✓ Exception raised for non-existent file: {type(e).__name__}")

    # Test with invalid input
    try:
        result = analyzer.analyze(b"not a pdf", mode="fast", save_output=False)
        if not result["success"]:
            print(f"  ✓ Properly handled invalid PDF bytes")
        else:
            print(f"  ✗ Should have failed for invalid PDF bytes")
            return False
    except Exception as e:
        print(f"  ✓ Exception raised for invalid PDF bytes: {type(e).__name__}")

    return True


def run_all_tests():
    """Run all tests."""
    print("Math Paper Analyzer - Test Suite")
    print("=" * 50)

    tests = [
        ("OCR PDF Reader", test_ocr_pdf_reader),
        ("Structure Extractor", test_structure_extractor),
        ("PaperAnalyzer Fast Mode", test_paper_analyzer_fast_mode),
        ("Configuration", test_configuration),
        ("Error Handling", test_error_handling),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"  ✗ Test crashed: {type(e).__name__}: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("Test Summary:")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {test_name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    # Check dependencies
    print("Checking dependencies...")

    missing_deps = []
    try:
        import fitz

        print("✓ PyMuPDF (fitz)")
    except ImportError:
        print("✗ PyMuPDF (fitz) - required for OCR")
        missing_deps.append("pymupdf")

    try:
        import httpx

        print("✓ httpx")
    except ImportError:
        print("✗ httpx - required for HTTP requests")
        missing_deps.append("httpx")

    try:
        import openai

        print("✓ openai (optional)")
    except ImportError:
        print("⚠ openai - optional for LLM features")

    if missing_deps:
        print(f"\nMissing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install " + " ".join(missing_deps))
        sys.exit(1)

    # Run tests
    sys.exit(run_all_tests())
