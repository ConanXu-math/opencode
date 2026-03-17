"""Unified paper analysis pipeline for math papers.

Provides three analysis modes:
1. Fast mode: OCR + regex structure extraction only
2. Standard mode: OCR + regex + LLM structure refinement
3. Deep mode: OCR + full structure + LLM summary generation
"""

import os
import logging
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from datetime import datetime

# Local imports
try:
    from .ocr_pdf_reader import OcrPDFReader
    from .structure_extractor import (
        extract_paper_structure,
        extract_paper_summary,
        format_structure_for_display,
        format_summary_for_display,
    )
except ImportError:
    # Fallback for direct script execution
    from ocr_pdf_reader import OcrPDFReader
    from structure_extractor import (
        extract_paper_structure,
        extract_paper_summary,
        format_structure_for_display,
        format_summary_for_display,
    )

logger = logging.getLogger(__name__)


class PaperAnalyzer:
    """Main paper analysis pipeline."""

    def __init__(
        self,
        ocr_url: str = "https://edusys5.sii.edu.cn/ocr",
        llm_api_key: Optional[str] = None,
        llm_base_url: Optional[str] = None,
        llm_model: Optional[str] = None,
        temp_dir: Optional[str] = None,
    ):
        """
        Initialize paper analyzer.

        Args:
            ocr_url: OCR API endpoint
            llm_api_key: OpenAI API key (optional for standard/deep modes)
            llm_base_url: OpenAI compatible API base URL
            llm_model: Model ID
            temp_dir: Temporary directory for processing
        """
        self.ocr_url = ocr_url
        self.llm_api_key = llm_api_key
        self.llm_base_url = llm_base_url
        self.llm_model = llm_model
        self.temp_dir = (
            Path(temp_dir)
            if temp_dir
            else Path(tempfile.gettempdir()) / "math-paper-analyzer"
        )
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        self.ocr_reader = OcrPDFReader(
            ocr_url=ocr_url,
            dpi=200,
            max_workers=4,
            request_timeout=60.0,
        )

        self.has_llm = bool(llm_api_key and llm_base_url and llm_model)

    def analyze(
        self,
        pdf_path: str | Path | bytes,
        mode: str = "standard",
        save_output: bool = True,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a math paper.

        Args:
            pdf_path: Path to PDF file, or PDF bytes
            mode: Analysis mode: "fast", "standard", "deep"
            save_output: Whether to save output to files
            output_dir: Directory to save output (default: temp_dir)

        Returns:
            Dictionary with analysis results
        """
        start_time = datetime.now()

        # Validate mode
        if mode not in ["fast", "standard", "deep"]:
            raise ValueError(
                f"Invalid mode: {mode}. Must be 'fast', 'standard', or 'deep'"
            )

        # Check LLM availability for standard/deep modes
        if mode in ["standard", "deep"] and not self.has_llm:
            logger.warning("LLM not configured, falling back to fast mode")
            mode = "fast"

        logger.info("Starting %s analysis", mode)

        # Step 1: OCR
        logger.info("Step 1: OCR processing")
        try:
            if isinstance(pdf_path, bytes):
                pages = self.ocr_reader.read_bytes(pdf_path)
                paper_source = "bytes"
            else:
                pdf_path = Path(pdf_path)
                if not pdf_path.exists():
                    raise FileNotFoundError(f"PDF file not found: {pdf_path}")
                pages = self.ocr_reader.read(pdf_path)
                paper_source = str(pdf_path)
        except Exception as e:
            logger.error("OCR failed: %s", e)
            return {
                "success": False,
                "error": f"OCR failed: {str(e)}",
                "mode": mode,
                "timestamp": start_time.isoformat(),
            }

        # Step 2: Structure extraction
        logger.info("Step 2: Structure extraction")
        try:
            if mode == "fast":
                structure = extract_paper_structure(pages)
            else:
                structure = extract_paper_structure(
                    pages,
                    llm_api_key=self.llm_api_key,
                    llm_base_url=self.llm_base_url,
                    llm_model=self.llm_model,
                )
        except Exception as e:
            logger.error("Structure extraction failed: %s", e)
            return {
                "success": False,
                "error": f"Structure extraction failed: {str(e)}",
                "ocr_pages": len(pages),
                "mode": mode,
                "timestamp": start_time.isoformat(),
            }

        # Step 3: Summary generation (deep mode only)
        summary = None
        if mode == "deep":
            logger.info("Step 3: Summary generation")
            try:
                # Check LLM configuration is available
                if self.llm_api_key and self.llm_base_url and self.llm_model:
                    # Assert for type checker
                    assert self.llm_api_key is not None
                    assert self.llm_base_url is not None
                    assert self.llm_model is not None
                    summary = extract_paper_summary(
                        pages,
                        structure,
                        llm_api_key=self.llm_api_key,
                        llm_base_url=self.llm_base_url,
                        llm_model=self.llm_model,
                    )
                else:
                    logger.warning("LLM not configured for summary generation")
            except Exception as e:
                logger.error("Summary generation failed: %s", e)
                # Continue without summary

        # Step 4: Format output
        logger.info("Step 4: Formatting output")
        structure_md = format_structure_for_display(structure)

        summary_md = None
        if summary:
            summary_md = format_summary_for_display(summary)
            full_md = f"{summary_md}\n\n{structure_md}"
        else:
            full_md = structure_md

        # Prepare result
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        result = {
            "success": True,
            "mode": mode,
            "paper_source": paper_source,
            "pages": len(pages),
            "structure": structure,
            "summary": summary,
            "markdown": full_md,
            "structure_markdown": structure_md,
            "summary_markdown": summary_md if summary else None,
            "timestamp": start_time.isoformat(),
            "duration_seconds": duration,
            "has_llm": self.has_llm,
        }

        # Save output if requested
        if save_output:
            self._save_output(result, output_dir)

        logger.info("Analysis completed in %.1f seconds", duration)
        return result

    def _save_output(
        self, result: Dict[str, Any], output_dir: Optional[str] = None
    ) -> None:
        """Save analysis results to files."""
        if output_dir:
            output_path = Path(output_dir)
        else:
            output_path = self.temp_dir / "output"

        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename
        if (
            isinstance(result["paper_source"], str)
            and result["paper_source"] != "bytes"
        ):
            paper_name = Path(result["paper_source"]).stem
        else:
            paper_name = f"paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Save markdown
        md_file = output_path / f"{paper_name}_analysis.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(result["markdown"])

        # Save JSON data
        import json

        json_file = output_path / f"{paper_name}_data.json"
        # Convert to serializable format
        json_data = {
            "success": result["success"],
            "mode": result["mode"],
            "paper_source": result["paper_source"],
            "pages": result["pages"],
            "structure": result["structure"],
            "summary": result["summary"],
            "timestamp": result["timestamp"],
            "duration_seconds": result["duration_seconds"],
            "has_llm": result["has_llm"],
        }
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        result["output_files"] = {
            "markdown": str(md_file),
            "json": str(json_file),
        }

        logger.info("Output saved to: %s", output_path)

    def analyze_multiple(
        self,
        pdf_paths: list[str | Path],
        mode: str = "standard",
        parallel: bool = False,
        max_workers: int = 4,
    ) -> list[Dict[str, Any]]:
        """
        Analyze multiple papers.

        Args:
            pdf_paths: List of PDF file paths
            mode: Analysis mode
            parallel: Whether to process in parallel
            max_workers: Maximum parallel workers

        Returns:
            List of analysis results
        """
        if parallel:
            # Simple parallel processing
            import concurrent.futures

            results = []
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=max_workers
            ) as executor:
                future_to_path = {
                    executor.submit(self.analyze, path, mode, save_output=False): path
                    for path in pdf_paths
                }
                for future in concurrent.futures.as_completed(future_to_path):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        path = future_to_path[future]
                        logger.error("Analysis failed for %s: %s", path, e)
                        results.append(
                            {
                                "success": False,
                                "error": str(e),
                                "paper_source": str(path),
                                "mode": mode,
                            }
                        )
            return results
        else:
            # Sequential processing
            results = []
            for path in pdf_paths:
                try:
                    result = self.analyze(path, mode, save_output=False)
                    results.append(result)
                except Exception as e:
                    logger.error("Analysis failed for %s: %s", path, e)
                    results.append(
                        {
                            "success": False,
                            "error": str(e),
                            "paper_source": str(path),
                            "mode": mode,
                        }
                    )
            return results


def create_analyzer_from_env() -> PaperAnalyzer:
    """Create PaperAnalyzer from environment variables."""
    ocr_url = os.getenv("MATH_PAPER_OCR_URL", "https://edusys5.sii.edu.cn/ocr")
    llm_api_key = os.getenv("MATH_PAPER_LLM_API_KEY")
    llm_base_url = os.getenv("MATH_PAPER_LLM_BASE_URL")
    llm_model = os.getenv("MATH_PAPER_LLM_MODEL")

    # Fallback to OpenAI env vars
    if not llm_api_key:
        llm_api_key = os.getenv("OPENAI_API_KEY")
    if not llm_base_url:
        llm_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    if not llm_model:
        llm_model = os.getenv("OPENAI_MODEL", "gpt-4o")

    return PaperAnalyzer(
        ocr_url=ocr_url,
        llm_api_key=llm_api_key,
        llm_base_url=llm_base_url,
        llm_model=llm_model,
    )


def analyze_paper_cli():
    """Command-line interface for paper analysis."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze math papers")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument(
        "--mode",
        choices=["fast", "standard", "deep"],
        default="standard",
        help="Analysis mode (default: standard)",
    )
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument(
        "--ocr-url", default="https://edusys5.sii.edu.cn/ocr", help="OCR API URL"
    )
    parser.add_argument("--llm-api-key", help="LLM API key")
    parser.add_argument("--llm-base-url", help="LLM base URL")
    parser.add_argument("--llm-model", help="LLM model")

    args = parser.parse_args()

    # Create analyzer
    analyzer = PaperAnalyzer(
        ocr_url=args.ocr_url,
        llm_api_key=args.llm_api_key,
        llm_base_url=args.llm_base_url,
        llm_model=args.llm_model,
    )

    # Analyze
    result = analyzer.analyze(
        pdf_path=args.pdf_path,
        mode=args.mode,
        save_output=True,
        output_dir=args.output_dir,
    )

    if result["success"]:
        print(f"Analysis completed successfully!")
        print(f"Mode: {result['mode']}")
        print(f"Pages: {result['pages']}")
        print(f"Duration: {result['duration_seconds']:.1f} seconds")
        if "output_files" in result:
            print(f"Markdown output: {result['output_files']['markdown']}")
            print(f"JSON data: {result['output_files']['json']}")

        # Print summary if available
        if result.get("summary_markdown"):
            print("\n" + "=" * 80)
            print(result["summary_markdown"])
    else:
        print(f"Analysis failed: {result.get('error', 'Unknown error')}")
        return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(analyze_paper_cli())
