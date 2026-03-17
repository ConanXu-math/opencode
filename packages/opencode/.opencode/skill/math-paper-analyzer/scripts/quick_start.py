"""Quick start example for the refactored math paper analyzer."""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from paper_pipeline import PaperPipeline


def example_basic_extraction():
    """Example 1: Basic extraction."""
    print("=== Example 1: Basic Extraction ===")

    # Create pipeline
    pipeline = PaperPipeline()

    # Path to a PDF file (replace with actual path)
    pdf_path = "path/to/your/math_paper.pdf"

    if not Path(pdf_path).exists():
        print(f"⚠ PDF file not found: {pdf_path}")
        print("Please update the path to a real PDF file.")
        return

    try:
        # Extract data
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

        # Preview formatted text
        preview = result["formatted_text"][:300]
        print(f"\nPreview (first 300 chars):")
        print("-" * 50)
        print(preview)
        if len(result["formatted_text"]) > 300:
            print("...")
        print("-" * 50)

    except Exception as e:
        print(f"✗ Extraction failed: {e}")


def example_with_saving():
    """Example 2: Extract and save to files."""
    print("\n=== Example 2: Extract and Save ===")

    pipeline = PaperPipeline()

    pdf_path = "path/to/your/math_paper.pdf"

    if not Path(pdf_path).exists():
        print(f"⚠ PDF file not found: {pdf_path}")
        return

    try:
        # Extract and save
        result = pipeline.extract_and_save(pdf_path, output_dir="./extracted_data")

        print(f"✓ Extraction and save successful!")
        print(f"  Output files:")
        for file_type, file_path in result.get("output_files", {}).items():
            print(f"    {file_type}: {file_path}")

    except Exception as e:
        print(f"✗ Failed: {e}")


def example_generate_analysis_prompt():
    """Example 3: Generate analysis prompt for opencode."""
    print("\n=== Example 3: Generate Analysis Prompt ===")

    pipeline = PaperPipeline()

    # First extract data
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
        print(f"  Copy the content and ask opencode to analyze the paper")

    except Exception as e:
        print(f"✗ Failed: {e}")


def example_full_workflow():
    """Example 4: Full workflow with opencode integration."""
    print("\n=== Example 4: Full Workflow ===")

    print("""
Full workflow for analyzing a math paper with opencode:

1. **Extract data from PDF**
   ```bash
   python -m scripts.cli extract paper.pdf --output-dir ./extracted
   ```

2. **Generate analysis prompt**
   ```bash
   python -m scripts.cli analyze ./extracted/paper_formatted.txt --type standard --output prompt.txt
   ```

3. **Use with opencode**
   - Copy the prompt content
   - Ask opencode: "Please analyze this math paper using the provided prompt"
   - Paste the prompt when requested

4. **Alternative: Single command**
   ```bash
   python -m scripts.cli full paper.pdf --type detailed --output-dir ./analysis
   ```
   This creates a complete analysis package with instructions.

Key points:
- Python scripts handle OCR and structure extraction
- opencode handles LLM analysis using generated prompts
- No LLM configuration needed in Python scripts
- Output includes formatted text ready for LLM analysis
""")


def main():
    """Run all examples."""
    print("Math Paper Analyzer - Quick Start Examples")
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
    example_basic_extraction()
    example_with_saving()
    example_generate_analysis_prompt()
    example_full_workflow()

    print("\n" + "=" * 50)
    print("Quick start examples completed.")
    print("\nTo use with actual PDF files:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Update PDF paths in the examples")
    print("3. Run: python scripts/quick_start.py")


if __name__ == "__main__":
    main()
