"""Command-line interface for math paper analysis."""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .paper_pipeline import PaperPipeline, create_pipeline_from_env
from .ocr_extractor import extract_ocr
from .structure_extractor import extract_structure, format_structure_for_display


def extract_command(args):
    """Handle extract command."""
    pipeline = create_pipeline_from_env()

    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = None

    try:
        result = pipeline.extract_and_save(
            args.pdf_path, str(output_dir) if output_dir else None
        )

        print(f"✓ Extraction completed successfully!")
        print(f"  Source: {args.pdf_path}")
        print(f"  Pages: {result['metadata']['pages']}")
        print(f"  Duration: {result['metadata']['duration_seconds']:.1f}s")

        if "output_files" in result:
            print(f"\nOutput files:")
            for file_type, file_path in result["output_files"].items():
                print(f"  {file_type}: {file_path}")

        # Print preview of formatted text
        if args.preview and "formatted_text" in result:
            preview = result["formatted_text"][:500]
            print(f"\nPreview (first 500 chars):")
            print("-" * 50)
            print(preview)
            if len(result["formatted_text"]) > 500:
                print("...")
            print("-" * 50)

        return 0

    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return 1


def analyze_command(args):
    """Handle analyze command."""
    # Load extracted data
    if args.input.endswith(".json"):
        with open(args.input, "r", encoding="utf-8") as f:
            extracted_data = json.load(f)
    else:
        print(f"✗ Input file must be JSON: {args.input}")
        return 1

    pipeline = create_pipeline_from_env()

    try:
        # Generate LLM analysis prompt
        prompt = pipeline.analyze_with_llm(extracted_data, analysis_type=args.type)

        # Save prompt to file
        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(prompt)
            print(f"✓ Analysis prompt saved to: {output_path}")
        else:
            # Print to stdout
            print(prompt)

        print(f"\nℹ️  Analysis type: {args.type}")
        print(f"ℹ️  Use this prompt with opencode's LLM for analysis")

        return 0

    except Exception as e:
        print(f"✗ Analysis failed: {e}")
        return 1


def full_command(args):
    """Handle full analysis command."""
    pipeline = create_pipeline_from_env()

    # Create output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(".") / "analysis_output"

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Step 1: Extract
        print("Step 1: Extracting OCR and structure...")
        extract_result = pipeline.extract_and_save(args.pdf_path, str(output_dir))

        if "output_files" not in extract_result:
            print("✗ Extraction failed to produce output files")
            return 1

        print(f"✓ Extraction completed")

        # Step 2: Generate analysis prompt
        print("\nStep 2: Generating analysis prompt...")
        prompt = pipeline.analyze_with_llm(extract_result, analysis_type=args.type)

        # Save prompt
        pdf_name = Path(args.pdf_path).stem
        prompt_path = output_dir / f"{pdf_name}_analysis_prompt.txt"
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)

        print(f"✓ Analysis prompt saved to: {prompt_path}")

        # Create README with instructions
        readme_path = output_dir / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"""# Math Paper Analysis Results

## Source PDF
- File: {args.pdf_path}
- Pages: {extract_result["metadata"]["pages"]}
- Extraction time: {extract_result["metadata"]["extraction_time"]}

## Generated Files
1. **Full extraction data**: `{Path(extract_result["output_files"]["full_json"]).name}`
2. **Formatted text for LLM**: `{Path(extract_result["output_files"]["formatted_text"]).name}`
3. **Structure data**: `{Path(extract_result["output_files"]["structure_json"]).name}`
4. **OCR data**: `{Path(extract_result["output_files"]["ocr_json"]).name}`
5. **Analysis prompt**: `{prompt_path.name}`

## Next Steps
1. Use the analysis prompt with opencode's LLM
2. Copy the prompt content and ask opencode to analyze the paper
3. The LLM will generate a detailed analysis report

## Analysis Prompt Preview
```
{prompt[:200]}...
```

## Usage Example
```bash
# Copy the prompt and use with opencode
cat "{prompt_path.name}" | pbcopy  # On macOS
# Then ask opencode: "Please analyze this math paper using the provided prompt"
```
""")

        print(f"\n✓ Full analysis completed!")
        print(f"  Output directory: {output_dir}")
        print(f"  Analysis type: {args.type}")
        print(f"  Next step: Use the prompt with opencode's LLM")

        return 0

    except Exception as e:
        print(f"✗ Full analysis failed: {e}")
        return 1


def batch_command(args):
    """Handle batch processing command."""
    pipeline = create_pipeline_from_env()

    # Find PDF files
    pdf_files = []
    for pattern in args.pdf_patterns:
        for path in Path(".").glob(pattern):
            if path.suffix.lower() == ".pdf":
                pdf_files.append(path)

    if not pdf_files:
        print(f"✗ No PDF files found matching patterns: {args.pdf_patterns}")
        return 1

    print(f"Found {len(pdf_files)} PDF files to process")

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, pdf_path in enumerate(pdf_files):
        print(f"\n[{i + 1}/{len(pdf_files)}] Processing: {pdf_path.name}")

        try:
            result = pipeline.extract_and_save(pdf_path, str(output_dir))
            results.append(
                {
                    "file": str(pdf_path),
                    "success": True,
                    "output_files": result.get("output_files", {}),
                }
            )
            print(f"  ✓ Success")
        except Exception as e:
            results.append({"file": str(pdf_path), "success": False, "error": str(e)})
            print(f"  ✗ Failed: {e}")

    # Save batch results
    batch_results_path = output_dir / "batch_results.json"
    with open(batch_results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Print summary
    successful = sum(1 for r in results if r["success"])
    print(f"\n{'=' * 50}")
    print(f"Batch processing completed:")
    print(f"  Total files: {len(results)}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {len(results) - successful}")
    print(f"  Results saved to: {batch_results_path}")

    return 0 if successful > 0 else 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Math Paper Analyzer - Extract and analyze mathematical papers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract OCR and structure from a paper
  python -m scripts.cli extract paper.pdf --output-dir ./extracted
  
  # Generate analysis prompt from extracted data
  python -m scripts.cli analyze extracted.json --type standard --output prompt.txt
  
  # Full analysis (extract + generate prompt)
  python -m scripts.cli full paper.pdf --type detailed --output-dir ./analysis
  
  # Batch process multiple PDFs
  python -m scripts.cli batch "*.pdf" --output-dir ./batch_results
  
  # Preview extraction results
  python -m scripts.cli extract paper.pdf --preview
""",
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Extract command
    extract_parser = subparsers.add_parser(
        "extract", help="Extract OCR and structure from PDF"
    )
    extract_parser.add_argument("pdf_path", help="Path to PDF file")
    extract_parser.add_argument(
        "--output-dir", help="Output directory for extracted data"
    )
    extract_parser.add_argument(
        "--preview", action="store_true", help="Preview formatted text"
    )
    extract_parser.set_defaults(func=extract_command)

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Generate analysis prompt from extracted data"
    )
    analyze_parser.add_argument("input", help="Input JSON file from extract command")
    analyze_parser.add_argument(
        "--type",
        choices=["standard", "detailed", "learning"],
        default="standard",
        help="Type of analysis",
    )
    analyze_parser.add_argument("--output", help="Output file for analysis prompt")
    analyze_parser.set_defaults(func=analyze_command)

    # Full command
    full_parser = subparsers.add_parser(
        "full", help="Full analysis (extract + generate prompt)"
    )
    full_parser.add_argument("pdf_path", help="Path to PDF file")
    full_parser.add_argument(
        "--type",
        choices=["standard", "detailed", "learning"],
        default="standard",
        help="Type of analysis",
    )
    full_parser.add_argument("--output-dir", help="Output directory for all files")
    full_parser.set_defaults(func=full_command)

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Batch process multiple PDFs")
    batch_parser.add_argument(
        "pdf_patterns", nargs="+", help="PDF file patterns (e.g., '*.pdf')"
    )
    batch_parser.add_argument(
        "--output-dir", default="./batch_output", help="Output directory"
    )
    batch_parser.set_defaults(func=batch_command)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
