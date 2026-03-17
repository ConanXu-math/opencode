"""Legacy paper analyzer module - kept for backward compatibility.

This module provides backward compatibility with the old API.
New code should use paper_pipeline.PaperPipeline instead.
"""

import warnings
from typing import Dict, Any, Optional
from pathlib import Path

from .paper_pipeline import PaperPipeline

warnings.warn(
    "PaperAnalyzer is deprecated. Use PaperPipeline from paper_pipeline module instead.",
    DeprecationWarning,
    stacklevel=2,
)


class PaperAnalyzer:
    """Deprecated paper analyzer. Use PaperPipeline instead."""

    def __init__(
        self,
        ocr_url: str = "https://edusys5.sii.edu.cn/ocr",
        llm_api_key: Optional[str] = None,
        llm_base_url: Optional[str] = None,
        llm_model: Optional[str] = None,
        temp_dir: Optional[str] = None,
    ):
        """
        Initialize paper analyzer (deprecated).

        Note: LLM parameters are ignored in the refactored version.
        LLM analysis is handled by opencode, not this Python module.
        """
        warnings.warn(
            "PaperAnalyzer is deprecated. LLM parameters are ignored. "
            "Use PaperPipeline instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        self.pipeline = PaperPipeline(ocr_url=ocr_url, temp_dir=temp_dir)
        self.has_llm = False  # LLM analysis is handled by opencode

    def analyze(
        self,
        pdf_path: str | Path | bytes,
        mode: str = "standard",
        save_output: bool = True,
        output_dir: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze a math paper (deprecated).

        Note: 'mode' parameter is ignored in refactored version.
        All analysis uses the same extraction pipeline.
        LLM analysis is handled separately by opencode.
        """
        warnings.warn(
            f"'mode' parameter ({mode}) is ignored. "
            "All extraction uses the same pipeline. "
            "LLM analysis is handled by opencode.",
            DeprecationWarning,
            stacklevel=2,
        )

        if isinstance(pdf_path, bytes):
            raise NotImplementedError(
                "PDF bytes input not supported in refactored version. "
                "Save to file first."
            )

        try:
            if save_output:
                result = self.pipeline.extract_and_save(pdf_path, output_dir)
            else:
                result = self.pipeline.extract(pdf_path)

            # Convert to old format for compatibility
            return self._convert_to_old_format(result, mode)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "mode": mode,
            }

    def _convert_to_old_format(
        self, result: Dict[str, Any], mode: str
    ) -> Dict[str, Any]:
        """Convert new format to old format for backward compatibility."""
        formatted_text = result.get("formatted_text", "")

        return {
            "success": True,
            "mode": mode,
            "has_llm": False,  # LLM handled by opencode
            "pages": result.get("metadata", {}).get("pages", 0),
            "duration_seconds": result.get("metadata", {}).get("duration_seconds", 0),
            "paper_source": result.get("metadata", {}).get("source", ""),
            "structure": result.get("structure", {}),
            "formatted_text": formatted_text,
            "markdown": formatted_text,  # Alias for backward compatibility
            "output_files": result.get("output_files", {}),
        }

    def analyze_multiple(
        self,
        pdf_paths: list,
        mode: str = "fast",
        parallel: bool = True,
        max_workers: int = 2,
    ) -> list:
        """
        Analyze multiple papers (deprecated).
        """
        warnings.warn(
            "analyze_multiple is deprecated. Use pipeline.batch_extract instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        results = self.pipeline.batch_extract(pdf_paths, parallel=parallel)

        # Convert to old format
        old_format_results = []
        for result in results:
            if "error" in result.get("metadata", {}):
                old_format_results.append(
                    {
                        "success": False,
                        "error": result["metadata"]["error"],
                        "paper_source": result["metadata"]["source"],
                    }
                )
            else:
                old_format_results.append(self._convert_to_old_format(result, mode))

        return old_format_results


def create_analyzer_from_env():
    """Create PaperAnalyzer from environment variables (deprecated)."""
    warnings.warn(
        "create_analyzer_from_env is deprecated. "
        "Use paper_pipeline.create_pipeline_from_env instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    from .paper_pipeline import create_pipeline_from_env as create_pipeline

    pipeline = create_pipeline()

    # Create PaperAnalyzer wrapper
    return PaperAnalyzer(
        ocr_url=pipeline.ocr_url,
        temp_dir=str(pipeline.temp_dir) if pipeline.temp_dir else None,
    )


# Keep old CLI function for backward compatibility
def analyze_paper_cli():
    """Command-line interface for paper analysis (deprecated)."""
    warnings.warn(
        "analyze_paper_cli is deprecated. Use cli.main() instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Analyze math papers (deprecated)")
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument(
        "--mode",
        choices=["fast", "standard", "deep"],
        default="standard",
        help="Analysis mode (ignored in refactored version)",
    )
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument(
        "--ocr-url", default="https://edusys5.sii.edu.cn/ocr", help="OCR API URL"
    )

    # LLM args are kept for compatibility but ignored
    parser.add_argument("--llm-api-key", help="LLM API key (ignored)")
    parser.add_argument("--llm-base-url", help="LLM base URL (ignored)")
    parser.add_argument("--llm-model", help="LLM model (ignored)")

    args = parser.parse_args()

    # Warn about ignored parameters
    if args.llm_api_key or args.llm_base_url or args.llm_model:
        print(
            "Warning: LLM parameters are ignored. LLM analysis is handled by opencode."
        )

    if args.mode != "standard":
        print(
            f"Warning: Mode '{args.mode}' is ignored. Using standard extraction pipeline."
        )

    # Use new CLI
    from .cli import main as cli_main

    # Build arguments for new CLI
    sys.argv = ["cli", "extract", args.pdf_path]
    if args.output_dir:
        sys.argv.extend(["--output-dir", args.output_dir])
    if args.ocr_url and args.ocr_url != "https://edusys5.sii.edu.cn/ocr":
        sys.argv.extend(["--ocr-url", args.ocr_url])

    return cli_main()


if __name__ == "__main__":
    analyze_paper_cli()
