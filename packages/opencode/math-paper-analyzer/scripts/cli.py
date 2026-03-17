#!/usr/bin/env python3
"""Command-line interface for math paper analyzer."""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.paper_analyzer import MathPaperAnalyzer, create_analyzer_from_env


def main():
    parser = argparse.ArgumentParser(description="Analyze mathematical papers")
    parser.add_argument("pdf_file", help="Path to PDF file")
    parser.add_argument(
        "--mode",
        choices=["fast", "standard", "deep"],
        default="standard",
        help="Analysis mode (default: standard)",
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory (default: same as PDF)",
    )
    parser.add_argument(
        "--ocr-url",
        default="https://edusys5.sii.edu.cn/ocr",
        help="OCR API URL",
    )
    parser.add_argument(
        "--llm-api-key",
        help="LLM API key (or set OPENAI_API_KEY env var)",
    )
    parser.add_argument(
        "--llm-base-url",
        help="LLM base URL (or set OPENAI_BASE_URL env var)",
    )
    parser.add_argument(
        "--llm-model",
        default="gpt-4o",
        help="LLM model (default: gpt-4o)",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save output to files",
    )

    args = parser.parse_args()

    # Check if file exists
    pdf_path = Path(args.pdf_file)
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    # Get LLM config from args or env
    llm_api_key = args.llm_api_key or os.getenv("OPENAI_API_KEY")
    llm_base_url = args.llm_base_url or os.getenv("OPENAI_BASE_URL")
    llm_model = args.llm_model

    # Check if LLM is needed but not configured
    if args.mode in ["standard", "deep"] and not (llm_api_key and llm_base_url):
        print("Warning: LLM API key and base URL are required for standard/deep mode.")
        print("You can:")
        print("  1. Use --llm-api-key and --llm-base-url arguments")
        print("  2. Set OPENAI_API_KEY and OPENAI_BASE_URL environment variables")
        print("  3. Switch to fast mode with --mode fast")

        if args.mode == "deep":
            print("\nSwitching to standard mode (LLM required for deep mode)...")
            args.mode = "standard"
        elif args.mode == "standard":
            print("\nSwitching to fast mode (no LLM required)...")
            args.mode = "fast"

    # Create analyzer
    analyzer = MathPaperAnalyzer(
        ocr_url=args.ocr_url,
        llm_api_key=llm_api_key,
        llm_base_url=llm_base_url,
        llm_model=llm_model,
    )

    # Analyze paper
    results = analyzer.analyze_paper(
        pdf_path=str(pdf_path),
        mode=args.mode,
        save_output=not args.no_save,
        output_dir=args.output_dir,
    )

    # Print errors if any
    if results.get("errors"):
        print("\n=== 错误信息 ===")
        for error in results["errors"]:
            print(f"- {error}")

    # Print full report to console
    print("\n" + "=" * 60)
    print("分析报告:")
    print("=" * 60)
    print(results["output"]["full_report"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
