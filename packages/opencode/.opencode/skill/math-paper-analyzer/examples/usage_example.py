"""Math Paper Analyzer - Updated Usage Examples

This file demonstrates how to use the refactored math paper analyzer skill.
Note: LLM analysis is now handled by opencode, not by Python scripts.
"""

import os
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from paper_pipeline import PaperPipeline, create_pipeline_from_env


def example_basic_extraction():
    """Example 1: Basic extraction."""
    print("=== Example 1: Basic Extraction ===")

    # Create pipeline with default settings
    pipeline = PaperPipeline()

    # Extract from a paper
    pdf_path = "path/to/your/math_paper.pdf"

    if Path(pdf_path).exists():
        try:
            result = pipeline.extract(pdf_path)

            print(f"✓ Extraction successful!")
            print(f"  Source: {result['metadata']['source']}")
            print(f"  Pages: {result['metadata']['pages']}")
            print(f"  Duration: {result['metadata']['duration_seconds']:.1f}s")

            # Show structure summary
            structure = result["structure"]
            print(f"\nExtracted structure:")
            print(f"  Sections: {len(structure.get('sections', []))}")
            print(f"  Theorems: {len(structure.get('theorems', []))}")
            print(f"  Definitions: {len(structure.get('definitions', []))}")
            print(f"  Equations: {len(structure.get('equations', []))}")

            # Print preview
            preview = (
                result["formatted_text"][:500] + "..."
                if len(result["formatted_text"]) > 500
                else result["formatted_text"]
            )
            print(f"\nPreview:\n{preview}")
        except Exception as e:
            print(f"✗ Extraction failed: {e}")
    else:
        print(f"⚠ PDF file not found: {pdf_path}")
        print("Please update the path to a real PDF file.")

    print()


def example_with_saving():
    """Example 2: Extract and save to files."""
    print("=== Example 2: Extract and Save ===")

    pipeline = PaperPipeline()
    pdf_path = "path/to/your/math_paper.pdf"

    if Path(pdf_path).exists():
        try:
            result = pipeline.extract_and_save(pdf_path, output_dir="./extracted_data")

            print(f"✓ Extraction and save successful!")
            print(f"  Output files:")
            for file_type, file_path in result.get("output_files", {}).items():
                print(f"    {file_type}: {file_path}")
        except Exception as e:
            print(f"✗ Failed: {e}")
    else:
        print(f"⚠ PDF file not found: {pdf_path}")

    print()


def example_generate_analysis_prompt():
    """Example 3: Generate analysis prompt for opencode."""
    print("=== Example 3: Generate Analysis Prompt ===")

    pipeline = PaperPipeline()
    pdf_path = "path/to/your/math_paper.pdf"

    if not Path(pdf_path).exists():
        print(f"⚠ PDF file not found: {pdf_path}")
        return

    try:
        # Extract data
        print("Extracting data from PDF...")
        result = pipeline.extract(pdf_path)

        # Generate analysis prompt
        print("Generating analysis prompt...")
        prompt = pipeline.analyze_with_llm(result, analysis_type="standard")

        print(f"✓ Analysis prompt generated!")
        print(f"  Analysis type: standard")
        print(f"  Prompt length: {len(prompt)} characters")

        # Save prompt to file
        output_file = "analysis_prompt.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(prompt)

        print(f"  Prompt saved to: {output_file}")
        print(f"\nNext step: Use this prompt with opencode's LLM")

    except Exception as e:
        print(f"✗ Failed: {e}")

    print()


def example_batch_processing():
    """Example 4: Batch processing multiple papers."""
    print("=== Example 4: Batch Processing ===")

    pipeline = PaperPipeline()

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

    print(f"Extracting {len(existing_files)} papers...")

    # Extract in sequence
    results = pipeline.batch_extract(existing_files, parallel=False)

    # Print summary
    successful = sum(1 for r in results if "error" not in r.get("metadata", {}))
    print(f"\nBatch extraction complete:")
    print(f"  Total papers: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(results) - successful}")

    for i, result in enumerate(results):
        if "error" in result.get("metadata", {}):
            status = "✗"
            source = result["metadata"]["source"]
        else:
            status = "✓"
            source = result["metadata"]["source"]
        print(f"  {status} {source}")

    print()


def example_custom_configuration():
    """Example 5: Custom configuration."""
    print("=== Example 5: Custom Configuration ===")

    # Create pipeline with custom settings
    pipeline = PaperPipeline(
        ocr_url="https://edusys5.sii.edu.cn/ocr",  # Default OCR service
        temp_dir="/tmp/my_paper_analysis",  # Custom temp directory
    )

    print(f"Pipeline configured:")
    print(f"  OCR URL: {pipeline.ocr_url}")
    print(f"  Temp dir: {pipeline.temp_dir}")

    # Test with a sample PDF if available
    sample_pdfs = list(Path(".").glob("*.pdf"))
    if sample_pdfs:
        pdf_path = sample_pdfs[0]
        print(f"\nTesting with: {pdf_path.name}")

        try:
            result = pipeline.extract_and_save(
                pdf_path,
                output_dir="./analysis_output",
            )

            if "output_files" in result:
                print(f"✓ Output saved to:")
                for file_type, file_path in result["output_files"].items():
                    print(f"  {file_type}: {file_path}")
        except Exception as e:
            print(f"✗ Failed: {e}")
    else:
        print("\n⚠ No PDF files found in current directory.")

    print()


def example_from_environment():
    """Example 6: Create pipeline from environment variables."""
    print("=== Example 6: From Environment Variables ===")

    # Set environment variables for testing
    os.environ["MATH_PAPER_OCR_URL"] = "https://edusys5.sii.edu.cn/ocr"
    os.environ["MATH_PAPER_TEMP_DIR"] = "/tmp/env_test"

    pipeline = create_pipeline_from_env()

    print(f"Pipeline created from environment:")
    print(f"  OCR URL: {pipeline.ocr_url}")
    print(f"  Temp dir: {pipeline.temp_dir}")

    # Clean up environment variables
    del os.environ["MATH_PAPER_OCR_URL"]
    del os.environ["MATH_PAPER_TEMP_DIR"]

    print()


def main():
    """Run all examples."""
    print("Math Paper Analyzer - Updated Usage Examples")
    print("=" * 50)
    print("Note: LLM analysis is handled by opencode, not Python scripts")
    print("=" * 50)

    # Check dependencies
    print("\nChecking dependencies...")
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
    example_basic_extraction()
    example_with_saving()
    example_generate_analysis_prompt()
    example_batch_processing()
    example_custom_configuration()
    example_from_environment()

    print("=" * 50)
    print("Examples completed.")
    print("\nKey changes in refactored version:")
    print("1. LLM analysis moved to opencode (no LLM config in Python)")
    print("2. New PaperPipeline class replaces PaperAnalyzer")
    print("3. Three analysis types: standard, detailed, learning")
    print("4. Output includes formatted text for LLM prompts")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure environment: cp .env.example .env")
    print("3. Update PDF paths in examples")
    print("4. Run: python examples/usage_example.py")


if __name__ == "__main__":
    main()
