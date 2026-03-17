"""OCR-based PDF Reader for math papers - Simplified standalone version.

Extracts text from PDF with LaTeX formulas preserved using external OCR API.
"""

import base64
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional, List
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


class OcrPDFReader:
    """Standalone PDF reader that uses OCR to extract text with LaTeX math formulas."""

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
        self.last_ocr_pages: List[str] = []

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

    def read(self, pdf_path: str | Path) -> List[str]:
        """
        Read PDF file and return list of OCR text per page.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of OCR text strings, one per page
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

        logger.info("Reading PDF: %s", pdf_path.name)

        # Open PDF
        doc = fitz.open(pdf_path)

        # Render all pages to images
        page_images = []
        for i, page in enumerate(doc):
            b64_png = self._render_page_to_b64(page)
            page_images.append((i, b64_png))

        # OCR pages in parallel
        ocr_results: List[Optional[str]] = [None] * len(page_images)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_map = {}
            for idx, b64 in page_images:
                future = executor.submit(self._ocr_single_page, idx, b64)
                future_map[future] = idx

            for future in as_completed(future_map):
                page_idx = future_map[future]
                try:
                    _, text = future.result()
                    ocr_results[page_idx] = text
                except Exception as e:
                    logger.error("OCR failed for page %s: %s", page_idx + 1, e)
                    ocr_results[page_idx] = ""

        # Ensure all pages have results
        pages = []
        for i, text in enumerate(ocr_results):
            if text is None:
                logger.warning("Page %d: No OCR result, using empty", i + 1)
                pages.append("")
            else:
                pages.append(text)

        doc.close()
        self.last_ocr_pages = pages
        return pages

    def read_bytes(self, pdf_bytes: bytes) -> List[str]:
        """
        Read PDF from bytes and return list of OCR text per page.

        Args:
            pdf_bytes: PDF file content as bytes

        Returns:
            List of OCR text strings, one per page
        """
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError(
                "PyMuPDF (fitz) is required for PDF rendering. Install with: pip install pymupdf"
            )

        logger.info("Reading PDF from bytes (%d bytes)", len(pdf_bytes))

        # Open PDF from bytes
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Render all pages to images
        page_images = []
        for i, page in enumerate(doc):
            b64_png = self._render_page_to_b64(page)
            page_images.append((i, b64_png))

        # OCR pages in parallel
        ocr_results: List[Optional[str]] = [None] * len(page_images)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_map = {}
            for idx, b64 in page_images:
                future = executor.submit(self._ocr_single_page, idx, b64)
                future_map[future] = idx

            for future in as_completed(future_map):
                page_idx = future_map[future]
                try:
                    _, text = future.result()
                    ocr_results[page_idx] = text
                except Exception as e:
                    logger.error("OCR failed for page %s: %s", page_idx + 1, e)
                    ocr_results[page_idx] = ""

        # Ensure all pages have results
        pages = []
        for i, text in enumerate(ocr_results):
            if text is None:
                logger.warning("Page %d: No OCR result, using empty", i + 1)
                pages.append("")
            else:
                pages.append(text)

        doc.close()
        self.last_ocr_pages = pages
        return pages
