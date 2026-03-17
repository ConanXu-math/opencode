"""OCR-based PDF processor for math papers.

Simplified version of the original OcrPDFReader, focused on single paper analysis.
"""

import base64
import logging
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Tuple

import fitz  # PyMuPDF
import httpx

logger = logging.getLogger(__name__)

DEFAULT_OCR_URL = "https://edusys5.sii.edu.cn/ocr"


def _ocr_page_image(b64_png: str, ocr_url: str, timeout: float = 60.0) -> Optional[str]:
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


class OcrPDFProcessor:
    """PDF processor that uses OCR to extract text with LaTeX math formulas.

    Simplified version for single paper analysis without agno dependencies.
    """

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
        self.pages: List[str] = []

    def _render_page_to_b64(self, page: fitz.Page) -> str:
        """Render PDF page to base64 PNG."""
        mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        return base64.b64encode(pix.tobytes("png")).decode("utf-8")

    def _ocr_single_page(self, page_index: int, b64_png: str) -> Tuple[int, str]:
        """OCR one page; returns (page_index, text)."""
        text = _ocr_page_image(b64_png, self.ocr_url, self.request_timeout)
        if text is None:
            logger.warning("Page %d: OCR failed, returning empty", page_index + 1)
            return page_index, ""
        return page_index, text

    def process_pdf(self, pdf_path: str) -> List[str]:
        """Process PDF file and return list of OCR text per page.

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of OCR text strings, one per page
        """
        self.pages = []

        try:
            doc = fitz.open(pdf_path)
            total_pages = len(doc)

            print(f"[OCR] Processing {total_pages} pages...")

            # Render all pages to images
            page_images = []
            for i in range(total_pages):
                page = doc.load_page(i)
                b64_png = self._render_page_to_b64(page)
                page_images.append((i, b64_png))

            # OCR pages in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self._ocr_single_page, idx, img): idx
                    for idx, img in page_images
                }

                # Collect results in order
                results: List[Optional[str]] = [None] * total_pages
                for future in as_completed(futures):
                    idx, text = future.result()
                    results[idx] = text
                    # Progress feedback
                    if (idx + 1) % 5 == 0 or idx + 1 == total_pages:
                        print(f"[OCR] Processed {idx + 1}/{total_pages} pages")

                self.pages = [text if text is not None else "" for text in results]

            doc.close()
            print(f"[OCR] Completed, got {len(self.pages)} pages of text")
            return self.pages

        except Exception as e:
            logger.error("PDF processing failed: %s", e)
            raise

    def process_pdf_bytes(self, pdf_bytes: bytes) -> List[str]:
        """Process PDF from bytes and return list of OCR text per page.

        Args:
            pdf_bytes: PDF file content as bytes

        Returns:
            List of OCR text strings, one per page
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name

        try:
            return self.process_pdf(tmp_path)
        finally:
            # Clean up temporary file
            Path(tmp_path).unlink(missing_ok=True)
