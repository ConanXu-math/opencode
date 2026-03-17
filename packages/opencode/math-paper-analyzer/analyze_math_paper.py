#!/usr/bin/env python3
"""
Math Paper Analyzer - Main entry point for skill usage.

This is the main entry point when the skill is triggered.
It provides a fully automated, user-friendly interface.
"""

import os
import sys
from pathlib import Path


def main():
    """Main entry point for the skill."""
    print("🔍 Math Paper Analyzer")
    print("=" * 50)

    # Check if PDF path is provided
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else None
        return analyze_paper(pdf_path, mode)

    # Interactive mode
    print("\n📚 Welcome to Math Paper Analyzer!")
    print("\nI can help you analyze mathematical papers and extract:")
    print("  • Theorems, definitions, and proofs")
    print("  • Paper structure and key formulas")
    print("  • Proof approaches and core techniques (with LLM)")

    # Ask for PDF path
    while True:
        pdf_path = input("\n📄 Enter the path to your PDF paper: ").strip()

        if not pdf_path:
            print("Please provide a PDF file path.")
            continue

        pdf_path_obj = Path(pdf_path)
        if not pdf_path_obj.exists():
            print(f"File not found: {pdf_path}")
            response = input("Try again? [Y/n]: ").strip().lower()
            if response in ["n", "no"]:
                return 1
            continue

        if pdf_path_obj.suffix.lower() != ".pdf":
            print("Please provide a PDF file (.pdf extension).")
            response = input("Try again? [Y/n]: ").strip().lower()
            if response in ["n", "no"]:
                return 1
            continue

        break

    # Ask for analysis mode
    print("\n🔧 Analysis Modes:")
    print("  1. Fast - Basic structure extraction (no LLM, <30s)")
    print("  2. Standard - Enhanced analysis with LLM (1-3min)")
    print("  3. Deep - Complete analysis with summaries (3-5min)")

    mode_map = {"1": "fast", "2": "standard", "3": "deep"}

    while True:
        choice = input("\nSelect mode [1-3, default=2]: ").strip()
        if not choice:
            mode = "standard"
            break
        if choice in mode_map:
            mode = mode_map[choice]
            break
        print("Please enter 1, 2, or 3")

    return analyze_paper(pdf_path, mode)


def analyze_paper(pdf_path: str, mode: str = None) -> int:
    """Analyze a paper using the auto analyzer."""
    try:
        # Import auto analyzer
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))

        from scripts.auto_analyzer import AutoMathPaperAnalyzer

        print(f"\n🚀 Starting analysis...")
        print(f"   Paper: {Path(pdf_path).name}")
        print(f"   Mode: {mode if mode else 'auto'}")

        # Create and run analyzer
        analyzer = AutoMathPaperAnalyzer()
        results = analyzer.analyze(pdf_path, mode)

        # Handle results
        if "error" in results:
            print(f"\n❌ Analysis failed: {results['error']}")

            # Provide helpful suggestions
            if "dependencies" in results["error"].lower():
                print("\n💡 Try running the setup wizard:")
                print("   python scripts/interactive_setup.py")
            elif "llm" in results["error"].lower():
                print("\n💡 LLM configuration required for this mode.")
                print("   You can:")
                print("   1. Set OPENAI_API_KEY environment variable")
                print("   2. Run: python scripts/interactive_setup.py")
                print(
                    "   3. Use fast mode: python analyze_math_paper.py paper.pdf fast"
                )

            return 1

        # Show success
        print("\n✅ Analysis completed successfully!")

        # Show output information
        paper_name = Path(pdf_path).stem
        output_dir = analyzer.config.get("output_dir", str(Path(pdf_path).parent))
        output_path = Path(output_dir)

        print(f"\n📁 Results saved to: {output_path}")

        mode_used = results.get("analysis_info", {}).get("mode", "unknown")

        # List output files
        files_found = []
        for ext, desc in [
            (f"{paper_name}_{mode_used}_analysis.md", "Full report"),
            (f"{paper_name}_structure.md", "Structure only"),
            (f"{paper_name}_summary.md", "Summary only")
            if mode_used == "deep"
            else None,
            (f"{paper_name}_analysis.json", "Raw data"),
        ]:
            if desc and (output_path / ext).exists():
                files_found.append((ext, desc))

        if files_found:
            print("\n📄 Generated files:")
            for filename, desc in files_found:
                print(f"  • {filename} ({desc})")

        # Show timing
        if "timing" in results:
            print(f"\n⏱️  Processing time:")
            total = 0
            for stage, time in results["timing"].items():
                if stage != "total":
                    print(f"    {stage:12}: {time:.1f}s")
                    total += time
            print(f"    {'total':12}: {total:.1f}s")

        # Show analysis summary
        if "structure" in results:
            struct = results["structure"]
            print(f"\n📊 Analysis summary:")
            stats = [
                ("Sections", len(struct.get("sections", []))),
                ("Theorems", len(struct.get("theorems", []))),
                ("Definitions", len(struct.get("definitions", []))),
                ("Proofs", len(struct.get("proofs", []))),
                ("Key formulas", len(struct.get("key_equations", []))),
            ]
            for name, count in stats:
                if count > 0:
                    print(f"    {name}: {count}")

        # Offer to open the report
        if files_found:
            response = input("\n📖 Open the main report? [Y/n]: ").strip().lower()
            if not response or response in ["y", "yes"]:
                report_file = output_path / f"{paper_name}_{mode_used}_analysis.md"
                if report_file.exists():
                    try:
                        # Try to open with default application
                        if sys.platform == "darwin":  # macOS
                            os.system(f"open '{report_file}'")
                        elif sys.platform == "win32":  # Windows
                            os.startfile(report_file)
                        else:  # Linux
                            os.system(f"xdg-open '{report_file}'")
                        print("Opened report in default application.")
                    except:
                        print(f"Could not open automatically. File: {report_file}")

        print("\n🎉 Done! You can now explore the analysis results.")

        return 0

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if the PDF file is valid and not corrupted")
        print("   2. Ensure you have internet connection (for OCR)")
        print("   3. Run setup: python scripts/interactive_setup.py")
        print("   4. Try fast mode: python analyze_math_paper.py paper.pdf fast")
        return 1


if __name__ == "__main__":
    # Make script directory available for imports
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))

    # Run main function
    sys.exit(main())
