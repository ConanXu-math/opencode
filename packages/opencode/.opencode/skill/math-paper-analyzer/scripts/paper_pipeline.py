"""Paper analysis pipeline for math papers.

This module provides a unified pipeline for extracting and analyzing math papers.
It integrates OCR extraction and structure extraction, and prepares data for
LLM analysis (which will be handled by opencode).
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from .ocr_extractor import OCRExtractor, extract_ocr
from .structure_extractor import extract_structure, format_structure_for_display

logger = logging.getLogger(__name__)


class PaperPipeline:
    """Unified pipeline for math paper analysis."""

    def __init__(
        self,
        ocr_url: str = "https://edusys5.sii.edu.cn/ocr",
        temp_dir: Optional[str] = None,
    ):
        """
        Initialize paper pipeline.

        Args:
            ocr_url: OCR API endpoint
            temp_dir: Temporary directory for processing
        """
        self.ocr_url = ocr_url
        self.extractor = OCRExtractor(ocr_url=ocr_url)

        # Set up temp directory
        if temp_dir:
            self.temp_dir = Path(temp_dir)
        else:
            import tempfile

            self.temp_dir = Path(tempfile.gettempdir()) / "math-paper-analyzer"

        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, pdf_path: str | Path) -> Dict[str, Any]:
        """
        Extract OCR text and structure from PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with extracted data:
            {
                "metadata": {
                    "source": "file.pdf",
                    "extraction_time": "...",
                    "pipeline_version": "1.0"
                },
                "ocr": {...},  # Output from OCRExtractor
                "structure": {...},  # Output from structure_extractor
                "formatted_text": "..."  # Text for LLM analysis
            }
        """
        logger.info("Starting extraction: %s", pdf_path)
        start_time = datetime.now()

        # Step 1: OCR extraction
        logger.info("Step 1: OCR extraction")
        try:
            ocr_data = self.extractor.extract(pdf_path)
        except Exception as e:
            logger.error("OCR extraction failed: %s", e)
            raise

        # Step 2: Structure extraction
        logger.info("Step 2: Structure extraction")
        try:
            structure_data = extract_structure(ocr_data)
        except Exception as e:
            logger.error("Structure extraction failed: %s", e)
            raise

        # Step 3: Format for display/LLM analysis
        logger.info("Step 3: Formatting for analysis")
        formatted_text = format_structure_for_display(structure_data)

        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()

        result = {
            "metadata": {
                "source": str(pdf_path),
                "extraction_time": start_time.isoformat(),
                "duration_seconds": duration,
                "pipeline_version": "1.0",
                "pages": len(ocr_data.get("pages", [])),
            },
            "ocr": ocr_data,
            "structure": structure_data,
            "formatted_text": formatted_text,
        }

        logger.info("Extraction completed in %.1f seconds", duration)
        return result

    def extract_and_save(
        self, pdf_path: str | Path, output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract data and save to files.

        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save output (default: temp_dir)

        Returns:
            Extraction result with added file paths
        """
        # Determine output directory
        if output_dir:
            out_dir = Path(output_dir)
        else:
            out_dir = self.temp_dir / "extractions"

        out_dir.mkdir(parents=True, exist_ok=True)

        # Generate base filename from PDF name
        pdf_name = Path(pdf_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{pdf_name}_{timestamp}"

        # Extract data
        result = self.extract(pdf_path)

        # Save files
        output_files = {}

        # Save full result as JSON
        json_path = out_dir / f"{base_name}_full.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        output_files["full_json"] = str(json_path)

        # Save formatted text for LLM
        text_path = out_dir / f"{base_name}_formatted.txt"
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(result["formatted_text"])
        output_files["formatted_text"] = str(text_path)

        # Save structure data
        structure_path = out_dir / f"{base_name}_structure.json"
        with open(structure_path, "w", encoding="utf-8") as f:
            json.dump(result["structure"], f, indent=2, ensure_ascii=False)
        output_files["structure_json"] = str(structure_path)

        # Save OCR data (optional, can be large)
        ocr_path = out_dir / f"{base_name}_ocr.json"
        with open(ocr_path, "w", encoding="utf-8") as f:
            json.dump(result["ocr"], f, indent=2, ensure_ascii=False)
        output_files["ocr_json"] = str(ocr_path)

        # Add file paths to result
        result["output_files"] = output_files

        logger.info("Saved extraction results to: %s", out_dir)
        return result

    def analyze_with_llm(
        self, extracted_data: Dict[str, Any], analysis_type: str = "standard"
    ) -> str:
        """
        Prepare data for LLM analysis.

        Note: This method doesn't actually call LLM. It prepares the data
        and returns instructions for how to use opencode's LLM.

        Args:
            extracted_data: Output from extract() method
            analysis_type: Type of analysis ("standard", "detailed", "learning")

        Returns:
            Instructions for LLM analysis
        """
        formatted_text = extracted_data.get("formatted_text", "")

        # Create analysis prompt based on type
        if analysis_type == "detailed":
            prompt = self._create_detailed_analysis_prompt(formatted_text)
        elif analysis_type == "learning":
            prompt = self._create_learning_analysis_prompt(formatted_text)
        else:  # standard
            prompt = self._create_standard_analysis_prompt(formatted_text)

        return prompt

    def _create_standard_analysis_prompt(self, formatted_text: str) -> str:
        """Create prompt for standard analysis."""
        return f"""# 数学论文分析任务

## 输入数据
以下是论文的结构化提取信息：

{formatted_text}

## 分析要求
请基于以上信息，生成一份详细的数学论文分析报告，包含以下部分：

1. **论文概览**
   - 标题识别（如果可以从数据中推断）
   - 作者信息整理
   - 摘要总结
   - 关键词整理

2. **数学领域识别**
   - 识别论文所属的主要数学分支（如：图论、组合优化、代数几何、数论等）
   - 识别具体研究问题

3. **结构分析**
   - 整理章节结构，说明各章节主要内容
   - 建立定理、定义、证明之间的关联

4. **核心内容分析**
   - 总结主要定理及其意义
   - 分析证明思路和核心技巧
   - 提取关键定义和概念

5. **学习价值评估**
   - 评估论文难度级别
   - 推荐适合的学习路径
   - 指出需要的前置知识

## 输出格式
请使用Markdown格式，包含清晰的标题和结构。使用LaTeX格式显示数学公式。
"""

    def _create_detailed_analysis_prompt(self, formatted_text: str) -> str:
        """Create prompt for detailed analysis."""
        return f"""# 数学论文深度分析任务

## 输入数据
以下是论文的结构化提取信息：

{formatted_text}

## 深度分析要求
请进行深度分析，包含以下内容：

1. **创新点分析**
   - 识别论文的主要贡献
   - 与相关工作的比较
   - 技术突破点

2. **证明技巧分类**
   - 归纳法、反证法、构造法、概率方法等
   - 技巧的应用场景和效果

3. **定理关系图谱**
   - 建立定理之间的依赖关系
   - 识别核心定理和辅助引理

4. **公式分析**
   - 解释关键公式的意义
   - 分析公式推导过程

5. **应用前景**
   - 潜在的应用领域
   - 后续研究方向

## 输出格式
详细的Markdown报告，包含多级标题、表格、列表等。
"""

    def _create_learning_analysis_prompt(self, formatted_text: str) -> str:
        """Create prompt for learning-focused analysis."""
        return f"""# 数学论文学习材料生成任务

## 输入数据
以下是论文的结构化提取信息：

{formatted_text}

## 学习材料生成要求
请生成适合数学学习者使用的材料：

1. **学习路线图**
   - 建议的学习顺序
   - 各阶段的学习目标
   - 预计学习时间

2. **概念解释**
   - 用通俗语言解释复杂概念
   - 提供直观例子

3. **定理证明解析**
   - 逐步解析证明过程
   - 指出关键步骤
   - 提供证明思路总结

4. **练习题设计**
   - 基础练习题（理解概念）
   - 中等练习题（应用定理）
   - 挑战练习题（扩展思考）

5. **常见误区**
   - 学习者容易误解的地方
   - 常见错误分析

## 输出格式
适合自学的Markdown材料，包含示例、练习、提示等。
"""

    def batch_extract(
        self, pdf_paths: List[str | Path], parallel: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Extract multiple PDFs.

        Args:
            pdf_paths: List of PDF file paths
            parallel: Whether to process in parallel

        Returns:
            List of extraction results
        """
        results = []

        if parallel:
            # Simple parallel processing (for demonstration)
            # In production, use proper parallel processing
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_path = {
                    executor.submit(self.extract, path): path for path in pdf_paths
                }

                for future in concurrent.futures.as_completed(future_to_path):
                    path = future_to_path[future]
                    try:
                        result = future.result()
                        results.append(result)
                        logger.info("Completed: %s", path)
                    except Exception as e:
                        logger.error("Failed to extract %s: %s", path, e)
                        results.append(
                            {
                                "metadata": {
                                    "source": str(path),
                                    "error": str(e),
                                    "success": False,
                                }
                            }
                        )
        else:
            # Sequential processing
            for path in pdf_paths:
                try:
                    result = self.extract(path)
                    results.append(result)
                    logger.info("Completed: %s", path)
                except Exception as e:
                    logger.error("Failed to extract %s: %s", path, e)
                    results.append(
                        {
                            "metadata": {
                                "source": str(path),
                                "error": str(e),
                                "success": False,
                            }
                        }
                    )

        return results


def create_pipeline_from_env() -> PaperPipeline:
    """Create PaperPipeline from environment variables."""
    import os

    ocr_url = os.getenv("MATH_PAPER_OCR_URL", "https://edusys5.sii.edu.cn/ocr")
    temp_dir = os.getenv("MATH_PAPER_TEMP_DIR")

    return PaperPipeline(ocr_url=ocr_url, temp_dir=temp_dir)
