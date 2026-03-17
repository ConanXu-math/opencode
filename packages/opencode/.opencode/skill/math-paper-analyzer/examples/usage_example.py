"""Math Paper Analyzer - Usage Examples

This file demonstrates how to use the math paper analyzer skill.
"""

import os
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from paper_pipeline import PaperPipeline, create_pipeline_from_env


def example_basic_usage():
    """Example 1: Basic usage with fast mode."""
    print("=== Example 1: Basic Usage (Fast Mode) ===")

    # Create analyzer with default settings
    analyzer = PaperAnalyzer()

    # Analyze a paper (fast mode - no LLM required)
    # Note: Replace with actual PDF path
    pdf_path = "path/to/your/math_paper.pdf"

    if Path(pdf_path).exists():
        result = analyzer.analyze(pdf_path, mode="fast", save_output=True)

        if result["success"]:
            print(f"✓ Analysis successful!")
            print(f"  Mode: {result['mode']}")
            print(f"  Pages: {result['pages']}")
            print(f"  Duration: {result['duration_seconds']:.1f}s")

            # Print first 500 chars of markdown
            preview = (
                result["markdown"][:500] + "..."
                if len(result["markdown"]) > 500
                else result["markdown"]
            )
            print(f"\nPreview:\n{preview}")
        else:
            print(f"✗ Analysis failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"⚠ PDF file not found: {pdf_path}")
        print("Please update the path to a real PDF file.")

    print()


def example_with_llm():
    """Example 2: Using LLM for deeper analysis."""
    print("=== Example 2: Standard Mode with LLM ===")

    # Check if LLM is configured
    llm_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("MATH_PAPER_LLM_API_KEY")

    if not llm_api_key:
        print(
            "⚠ LLM not configured. Set OPENAI_API_KEY or MATH_PAPER_LLM_API_KEY environment variable."
        )
        print("   Using fast mode instead...")
        analyzer = PaperAnalyzer()
        mode = "fast"
    else:
        # Create analyzer with LLM configuration
        analyzer = create_analyzer_from_env()
        mode = "standard"

    pdf_path = "path/to/your/math_paper.pdf"

    if Path(pdf_path).exists():
        result = analyzer.analyze(pdf_path, mode=mode, save_output=True)

        if result["success"]:
            print(f"✓ Analysis successful!")
            print(f"  Mode: {result['mode']}")
            print(f"  Has LLM: {result['has_llm']}")
            print(f"  Pages: {result['pages']}")
            print(f"  Duration: {result['duration_seconds']:.1f}s")

            if result.get("summary"):
                print(f"\nSummary generated:")
                print(f"  Title: {result['summary'].get('title', 'N/A')}")
                print(
                    f"  Field tags: {', '.join(result['summary'].get('field_tags', []))}"
                )
        else:
            print(f"✗ Analysis failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"⚠ PDF file not found: {pdf_path}")

    print()


def example_batch_processing():
    """Example 3: Batch processing multiple papers."""
    print("=== Example 3: Batch Processing ===")

    analyzer = PaperAnalyzer()

    # List of PDF files to analyze
    pdf_files = [
        "path/to/paper1.pdf",
        "path/to/paper2.pdf",
        "path/to/paper3.pdf",
    ]

    # Filter to existing files
    existing_files = [f for f in pdf_files if Path(f).exists()]

    if not existing_files:
        print("⚠ No PDF files found. Please update the file paths.")
        return

    print(f"Analyzing {len(existing_files)} papers...")

    # Analyze in sequence (set parallel=True for parallel processing)
    results = analyzer.analyze_multiple(
        existing_files,
        mode="fast",
        parallel=False,
        max_workers=2,
    )

    # Print summary
    successful = sum(1 for r in results if r.get("success", False))
    print(f"\nBatch processing complete:")
    print(f"  Total papers: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(results) - successful}")

    for i, result in enumerate(results):
        status = "✓" if result.get("success", False) else "✗"
        source = result.get("paper_source", f"Paper {i + 1}")
        print(f"  {status} {source}")

    print()


def example_custom_configuration():
    """Example 4: Custom configuration."""
    print("=== Example 4: Custom Configuration ===")

    # Create analyzer with custom settings
    analyzer = PaperAnalyzer(
        ocr_url="https://edusys5.sii.edu.cn/ocr",  # Default OCR service
        llm_api_key=os.getenv("OPENAI_API_KEY"),  # Optional
        llm_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        llm_model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        temp_dir="/tmp/my_paper_analysis",  # Custom temp directory
    )

    print(f"Analyzer configured:")
    print(f"  OCR URL: {analyzer.ocr_url}")
    print(f"  Has LLM: {analyzer.has_llm}")
    print(f"  Temp dir: {analyzer.temp_dir}")

    # Test with a sample PDF if available
    sample_pdfs = list(Path(".").glob("*.pdf"))
    if sample_pdfs:
        pdf_path = sample_pdfs[0]
        print(f"\nTesting with: {pdf_path.name}")

        result = analyzer.analyze(
            pdf_path,
            mode="fast",
            save_output=True,
            output_dir="./analysis_output",  # Custom output directory
        )

        if result["success"] and "output_files" in result:
            print(f"✓ Output saved to:")
            for file_type, file_path in result["output_files"].items():
                print(f"  {file_type}: {file_path}")
    else:
        print("\n⚠ No PDF files found in current directory.")

    print()


def example_error_handling():
    """Example 5: Error handling and recovery."""
    print("=== Example 5: Error Handling ===")

    analyzer = PaperAnalyzer()

    # Test cases
    test_cases = [
        ("Non-existent file", "non_existent.pdf"),
        ("Invalid PDF", __file__),  # This Python file, not a PDF
        ("Empty PDF", ""),
    ]

    for description, test_path in test_cases:
        print(f"\nTesting: {description}")
        print(f"  Path: {test_path}")

        try:
            result = analyzer.analyze(test_path, mode="fast", save_output=False)

            if result["success"]:
                print(f"  ✓ Success (unexpected)")
            else:
                print(f"  ✗ Failed as expected: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"  ✗ Exception: {type(e).__name__}: {e}")

    print()


def main():
    """Run all examples."""
    print("Math Paper Analyzer - Usage Examples")
    print("=" * 50)

    # Check dependencies
    print("Checking dependencies...")
    try:
        import fitz

        print("✓ PyMuPDF (fitz) available")
    except ImportError:
        print("✗ PyMuPDF not installed. Install with: pip install pymupdf")

    try:
        import httpx

        print("✓ httpx available")
    except ImportError:
        print("✗ httpx not installed. Install with: pip install httpx")

    print()

    # Run examples
    example_basic_usage()
    example_with_llm()
    example_batch_processing()
    example_custom_configuration()
    example_error_handling()

    print("=" * 50)
    print("Examples completed.")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure environment: cp .env.example .env")
    print("3. Update PDF paths in examples")
    print("4. Run: python examples/usage_example.py")


if __name__ == "__main__":
    main()
