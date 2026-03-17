"""OCR-based PDF text extractor for math papers.

Simplified module that extracts text with LaTeX formulas preserved using external OCR API.
This module only handles OCR extraction, no LLM integration.
"""

import base64
import logging
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import httpx

logger = logging.getLogger(__name__)

DEFAULT_OCR_URL = "https://edusys5.sii.edu.cn/ocr"


def _ocr_page_image(b64_png: str, ocr_url: str, timeout: float) -> Optional[str]:
    """Send a base64-encoded PNG to the OCR API and return recognised text."""
    try:
        resp = httpx.post(
            ocr_url,
            json={"image_base64": b64_png},
            timeout=timeout,
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                return data.get("result", "")
        logger.warning(
            "OCR request failed (status %s): %s", resp.status_code, resp.text[:200]
        )
    except Exception as e:
        logger.warning("OCR request error: %s", e)
    return None


class OCRExtractor:
    """PDF text extractor using OCR with LaTeX math formula preservation."""

    def __init__(
        self,
        ocr_url: str = DEFAULT_OCR_URL,
        dpi: int = 200,
        max_workers: int = 4,
        request_timeout: float = 60.0,
    ):
        self.ocr_url = ocr_url
        self.dpi = dpi
        self.max_workers = max_workers
        self.request_timeout = request_timeout

    def _render_page_to_b64(self, page) -> str:
        """Render PDF page to base64 PNG."""
        try:
            import fitz  # PyMuPDF

            mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            return base64.b64encode(pix.tobytes("png")).decode("utf-8")
        except ImportError:
            raise ImportError(
                "PyMuPDF (fitz) is required for PDF rendering. Install with: pip install pymupdf"
            )

    def _ocr_single_page(self, page_index: int, b64_png: str) -> tuple[int, str]:
        """OCR one page; returns (page_index, text)."""
        text = _ocr_page_image(b64_png, self.ocr_url, self.request_timeout)
        if text is None:
            logger.warning("Page %d: OCR failed, returning empty", page_index + 1)
            return page_index, ""
        return page_index, text

    def extract(self, pdf_path: str | Path) -> Dict[str, Any]:
        """
        Extract OCR text from PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with structured OCR data:
            {
                "metadata": {
                    "source": "file.pdf",
                    "pages": 10,
                    "extraction_time": "2025-03-17T20:00:00Z"
                },
                "pages": [
                    {
                        "number": 1,
                        "text": "page text content...",
                        "formulas": ["$$E=mc^2$$", ...]
                    },
                    ...
                ]
            }
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF (fitz) is required for PDF rendering. Install with: pip install pymupdf"
            )

        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        logger.info("Extracting OCR from PDF: %s", pdf_path.name)

        # Open PDF
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        # Extract metadata
        metadata = {
            "source": str(pdf_path),
            "pages": total_pages,
            "extraction_time": None,  # Will be set later
        }

        # Render pages to images
        page_images = []
        for page_idx in range(total_pages):
            page = doc[page_idx]
            b64_png = self._render_page_to_b64(page)
            page_images.append((page_idx, b64_png))

        # OCR in parallel
        pages_data: List[Optional[Dict[str, Any]]] = [None] * total_pages

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._ocr_single_page, idx, img): idx
                for idx, img in page_images
            }
            for future in as_completed(futures):
                page_idx, text = future.result()
                # Extract LaTeX formulas from text
                formulas = self._extract_formulas(text)
                page_data = {
                    "number": page_idx + 1,
                    "text": text,
                    "formulas": formulas,
                }
                pages_data[page_idx] = page_data

        # Filter out None values (shouldn't happen, but just in case)
        pages_data = [page for page in pages_data if page is not None]

        doc.close()

        # Update metadata with completion time
        from datetime import datetime

        metadata["extraction_time"] = datetime.now().isoformat()

        return {
            "metadata": metadata,
            "pages": pages_data,
        }

    def _extract_formulas(self, text: str) -> List[str]:
        """Extract LaTeX display formulas from text."""
        import re

        # Pattern for display math: $$...$$ or \[...\]
        display_math_pattern = re.compile(r"\$\$(.+?)\$\$|\\\[(.+?)\\\]", re.DOTALL)

        formulas = []
        for match in display_math_pattern.finditer(text):
            # Get the formula content (group 1 for $$, group 2 for \[)
            formula = match.group(1) or match.group(2)
            if formula:
                formulas.append(formula.strip())

        return formulas

    def extract_bytes(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """
        Extract OCR text from PDF bytes.

        Args:
            pdf_bytes: PDF file content as bytes

        Returns:
            Same structure as extract()
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF (fitz) is required for PDF rendering. Install with: pip install pymupdf"
            )

        logger.info("Extracting OCR from PDF bytes")

        # Open PDF from bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = len(doc)

        # Extract metadata
        metadata = {
            "source": "bytes",
            "pages": total_pages,
            "extraction_time": None,
        }

        # Render and OCR pages
        pages_data = []
        for page_idx in range(total_pages):
            page = doc[page_idx]
            b64_png = self._render_page_to_b64(page)
            text = _ocr_page_image(b64_png, self.ocr_url, self.request_timeout) or ""
            formulas = self._extract_formulas(text)

            pages_data.append(
                {
                    "number": page_idx + 1,
                    "text": text,
                    "formulas": formulas,
                }
            )

        doc.close()

        # Update metadata
        from datetime import datetime

        metadata["extraction_time"] = datetime.now().isoformat()

        return {
            "metadata": metadata,
            "pages": pages_data,
        }


def extract_ocr(pdf_path: str, ocr_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function for OCR extraction.

    Args:
        pdf_path: Path to PDF file
        ocr_url: Optional custom OCR URL

    Returns:
        Structured OCR data
    """
    extractor = OCRExtractor(ocr_url=ocr_url or DEFAULT_OCR_URL)
    return extractor.extract(pdf_path)
