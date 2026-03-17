"""Unified paper analysis pipeline for math papers.

Three-level analysis mode:
1. Fast mode: regex extraction only (no LLM)
2. Standard mode: regex + LLM structure refinement
3. Deep mode: full analysis with summary and multi-dimensional tags
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .ocr_pdf_processor import OcrPDFProcessor
from .structure_analyzer import (
    extract_paper_structure,
    extract_paper_summary,
    format_structure_for_display,
    format_summary_for_display,
)


class MathPaperAnalyzer:
    """Main analyzer for mathematical papers with three-level analysis mode."""

    def __init__(
        self,
        ocr_url: str = "https://edusys5.sii.edu.cn/ocr",
        dpi: int = 200,
        max_workers: int = 4,
        llm_api_key: Optional[str] = None,
        llm_base_url: Optional[str] = None,
        llm_model: Optional[str] = None,
    ):
        """Initialize the analyzer.

        Args:
            ocr_url: OCR API endpoint
            dpi: DPI for PDF rendering
            max_workers: max parallel workers for OCR
            llm_api_key: OpenAI API key (optional for fast mode)
            llm_base_url: OpenAI base URL (optional for fast mode)
            llm_model: Model ID (optional for fast mode)
        """
        self.ocr_processor = OcrPDFProcessor(
            ocr_url=ocr_url,
            dpi=dpi,
            max_workers=max_workers,
        )
        self.llm_api_key = llm_api_key
        self.llm_base_url = llm_base_url
        self.llm_model = llm_model

        # Check if LLM is available
        self.llm_available = all([llm_api_key, llm_base_url, llm_model])

    def analyze_paper(
        self,
        pdf_path: str,
        mode: str = "standard",
        save_output: bool = True,
        output_dir: Optional[str] = None,
    ) -> Dict:
        """Analyze a mathematical paper.

        Args:
            pdf_path: Path to PDF file
            mode: Analysis mode - "fast", "standard", or "deep"
            save_output: Whether to save output to files
            output_dir: Directory to save output (default: same as PDF)

        Returns:
            Dictionary containing analysis results
        """
        print(f"=== 开始分析: {Path(pdf_path).name} ===")
        print(f"模式: {mode}")

        start_time = time.time()
        results = {
            "paper_name": Path(pdf_path).stem,
            "mode": mode,
            "timing": {},
            "errors": [],
        }

        try:
            # Step 1: OCR processing
            print("\n[1/3] OCR 处理中...")
            ocr_start = time.time()
            pages = self.ocr_processor.process_pdf(pdf_path)
            ocr_time = time.time() - ocr_start
            results["timing"]["ocr"] = ocr_time
            results["page_count"] = len(pages)
            print(f"✓ OCR 完成: {len(pages)} 页, 耗时 {ocr_time:.1f}秒")

            # Step 2: Structure extraction
            print("\n[2/3] 结构提取中...")
            struct_start = time.time()

            use_llm = mode in ["standard", "deep"] and self.llm_available
            structure = extract_paper_structure(
                pages=pages,
                use_llm=use_llm,
                llm_api_key=self.llm_api_key if use_llm else None,
                llm_base_url=self.llm_base_url if use_llm else None,
                llm_model=self.llm_model if use_llm else None,
            )

            struct_time = time.time() - struct_start
            results["timing"]["structure"] = struct_time
            results["structure"] = structure

            # Count elements
            n_sections = len(structure.get("sections", []))
            n_theorems = len(structure.get("theorems", []))
            n_definitions = len(structure.get("definitions", []))
            n_proofs = len(structure.get("proofs", []))
            n_equations = len(structure.get("key_equations", []))

            print(f"✓ 结构提取完成:")
            print(f"  - 章节: {n_sections}")
            print(f"  - 定理/引理: {n_theorems}")
            print(f"  - 定义: {n_definitions}")
            print(f"  - 证明: {n_proofs}")
            print(f"  - 关键公式: {n_equations}")
            print(f"  耗时 {struct_time:.1f}秒")

            # Step 3: Summary extraction (deep mode only)
            summary = None
            if (
                mode == "deep"
                and self.llm_available
                and self.llm_api_key
                and self.llm_base_url
                and self.llm_model
            ):
                print("\n[3/3] 深度摘要生成中...")
                summary_start = time.time()

                summary = extract_paper_summary(
                    pages=pages,
                    structure=structure,
                    llm_api_key=self.llm_api_key,
                    llm_base_url=self.llm_base_url,
                    llm_model=self.llm_model,
                )

                summary_time = time.time() - summary_start
                results["timing"]["summary"] = summary_time
                results["summary"] = summary

                if summary:
                    print(f"✓ 深度摘要完成:")
                    print(f"  - 标题: {summary.get('title', 'N/A')}")
                    print(f"  - 领域标签: {', '.join(summary.get('field_tags', []))}")
                    print(f"  - 核心方法: {len(summary.get('core_techniques', []))} 个")
                    print(f"  耗时 {summary_time:.1f}秒")
                else:
                    print("✗ 深度摘要生成失败")
                    results["errors"].append("深度摘要生成失败")

            # Generate output
            print("\n[4/4] 生成输出...")
            output_start = time.time()

            # Format structure display
            structure_md = format_structure_for_display(structure)
            results["output"] = {
                "structure_markdown": structure_md,
            }

            # Add summary if available
            if summary:
                summary_md = format_summary_for_display(summary)
                results["output"]["summary_markdown"] = summary_md

                # Combine full report
                full_report = f"""# 数学论文分析报告

## 基本信息
- **论文**: {Path(pdf_path).name}
- **分析模式**: {mode}
- **总页数**: {len(pages)} 页
- **分析耗时**: {time.time() - start_time:.1f} 秒

{summary_md}

## 详细结构
{structure_md}

---
*分析完成时间: {time.strftime("%Y-%m-%d %H:%M:%S")}*
"""
                results["output"]["full_report"] = full_report
            else:
                # Fast/standard mode report
                full_report = f"""# 数学论文结构分析

## 基本信息
- **论文**: {Path(pdf_path).name}
- **分析模式**: {mode}
- **总页数**: {len(pages)} 页
- **分析耗时**: {time.time() - start_time:.1f} 秒

## 论文结构
{structure_md}

---
*分析完成时间: {time.strftime("%Y-%m-%d %H:%M:%S")}*
*注: {mode} 模式仅提取基本结构，如需深度分析请使用 deep 模式*
"""
                results["output"]["full_report"] = full_report

            output_time = time.time() - output_start
            results["timing"]["output"] = output_time

            # Save output if requested
            if save_output:
                self._save_output(results, pdf_path, output_dir)

            total_time = time.time() - start_time
            results["timing"]["total"] = total_time

            print(f"\n✓ 分析完成! 总耗时: {total_time:.1f}秒")

            # Print timing summary
            print("\n=== 时间统计 ===")
            for stage, t in results["timing"].items():
                print(f"{stage:12}: {t:.1f}秒")

            return results

        except Exception as e:
            error_msg = f"分析过程中出错: {str(e)}"
            print(f"\n✗ {error_msg}")
            results["errors"].append(error_msg)
            return results

    def _save_output(
        self, results: Dict, pdf_path: str, output_dir: Optional[str] = None
    ) -> None:
        """Save analysis results to files."""
        from pathlib import Path

        if output_dir is None:
            output_dir = str(Path(pdf_path).parent)

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        paper_name = results["paper_name"]
        mode = results["mode"]

        # Save full report
        report_file = output_path / f"{paper_name}_{mode}_analysis.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(results["output"]["full_report"])

        # Save structure separately
        struct_file = output_path / f"{paper_name}_structure.md"
        with open(struct_file, "w", encoding="utf-8") as f:
            f.write(results["output"]["structure_markdown"])

        # Save summary if available
        summary_file = None
        if "summary_markdown" in results["output"]:
            summary_file = output_path / f"{paper_name}_summary.md"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(results["output"]["summary_markdown"])

        # Save raw data as JSON
        import json

        json_file = output_path / f"{paper_name}_analysis.json"
        with open(json_file, "w", encoding="utf-8") as f:
            # Remove pages from JSON to reduce size
            clean_results = results.copy()
            if "pages" in clean_results:
                del clean_results["pages"]
            json.dump(clean_results, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 输出已保存到: {output_path}")
        print(f"  - 完整报告: {report_file.name}")
        print(f"  - 结构分析: {struct_file.name}")
        if summary_file:
            print(f"  - 深度摘要: {summary_file.name}")
        print(f"  - 原始数据: {json_file.name}")

    def analyze_pdf_bytes(
        self,
        pdf_bytes: bytes,
        paper_name: str = "unknown",
        mode: str = "standard",
    ) -> Dict:
        """Analyze PDF from bytes.

        Args:
            pdf_bytes: PDF file content as bytes
            paper_name: Name for the paper (used in output)
            mode: Analysis mode

        Returns:
            Dictionary containing analysis results
        """
        # Process PDF bytes
        pages = self.ocr_processor.process_pdf_bytes(pdf_bytes)

        # Create a temporary results structure
        results = {
            "paper_name": paper_name,
            "mode": mode,
            "page_count": len(pages),
            "timing": {},
        }

        # Extract structure
        use_llm = mode in ["standard", "deep"] and self.llm_available
        structure = extract_paper_structure(
            pages=pages,
            use_llm=use_llm,
            llm_api_key=self.llm_api_key if use_llm else None,
            llm_base_url=self.llm_base_url if use_llm else None,
            llm_model=self.llm_model if use_llm else None,
        )
        results["structure"] = structure

        # Extract summary if deep mode
        summary = None
        if (
            mode == "deep"
            and self.llm_available
            and self.llm_api_key
            and self.llm_base_url
            and self.llm_model
        ):
            summary = extract_paper_summary(
                pages=pages,
                structure=structure,
                llm_api_key=self.llm_api_key,
                llm_base_url=self.llm_base_url,
                llm_model=self.llm_model,
            )
            results["summary"] = summary

        # Generate output
        structure_md = format_structure_for_display(structure)
        results["output"] = {
            "structure_markdown": structure_md,
        }

        if summary:
            summary_md = format_summary_for_display(summary)
            results["output"]["summary_markdown"] = summary_md

            full_report = f"""# 数学论文分析报告

## 基本信息
- **论文**: {paper_name}
- **分析模式**: {mode}
- **总页数**: {len(pages)} 页

{summary_md}

## 详细结构
{structure_md}
"""
            results["output"]["full_report"] = full_report
        else:
            full_report = f"""# 数学论文结构分析

## 基本信息
- **论文**: {paper_name}
- **分析模式**: {mode}
- **总页数**: {len(pages)} 页

## 论文结构
{structure_md}
"""
            results["output"]["full_report"] = full_report

        return results


def create_analyzer_from_env() -> MathPaperAnalyzer:
    """Create analyzer from environment variables."""
    import os

    ocr_url = os.getenv("MATH_PAPER_OCR_URL", "https://edusys5.sii.edu.cn/ocr")
    llm_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    llm_base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("LLM_BASE_URL")
    llm_model = os.getenv("OPENAI_MODEL") or os.getenv("LLM_MODEL_ID") or "gpt-4o"

    return MathPaperAnalyzer(
        ocr_url=ocr_url,
        llm_api_key=llm_api_key,
        llm_base_url=llm_base_url,
        llm_model=llm_model,
    )
