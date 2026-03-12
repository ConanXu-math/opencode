"""Structure extraction for math papers using regex patterns only.

This module extracts sections, theorems, definitions, proofs, and equations
from OCR text using regex patterns. No LLM integration.
"""

import re
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


# ── Regex patterns for structure extraction ──────────────────────────────

_SECTION_RE = re.compile(
    r"^(?:#{1,3}\s+)?"
    r"(\d+(?:\.\d+)*)"
    r"\.?\s+"
    r"(.+)",
    re.MULTILINE,
)

_THEOREM_RE = re.compile(
    r"(?P<type>Theorem|Lemma|Proposition|Corollary|定理|引理|命题|推论)"
    r"\s+(?P<label>[\d.]+)"
    r"[.:\s]*(?P<statement>[^\n]*(?:\n(?!Proof|证明|Definition|定义|Theorem|Lemma|Proposition|Corollary)[^\n]*){0,5})",
    re.IGNORECASE,
)

_PROOF_RE = re.compile(
    r"(?P<keyword>Proof|证明)[.\s:]*",
    re.IGNORECASE,
)

_DEFINITION_RE = re.compile(
    r"(?P<type>Definition|定义)\s+(?P<label>[\d.]+)"
    r"[.:\s]*(?P<content>[^\n]*(?:\n(?!Theorem|Lemma|Proof|Definition|定义|定理|引理)[^\n]*){0,4})",
    re.IGNORECASE,
)

_DISPLAY_MATH_RE = re.compile(
    r"\$\$(.+?)\$\$|\\\[(.+?)\\\]",
    re.DOTALL,
)

# Pattern for inline math (for reference)
_INLINE_MATH_RE = re.compile(r"\$(.+?)\$|\\\((.+?)\\\)", re.DOTALL)

# Pattern for references (e.g., [1], [2-5], etc.)
_REFERENCE_RE = re.compile(r"\[(\d+(?:-\d+)?(?:,\s*\d+)*)\]")

# Pattern for authors and affiliations
_AUTHOR_RE = re.compile(
    r"^(?:(?:By\s+)|(?:Authors?:\s*))?(.+?)(?:\s*,\s*(.+))?$",
    re.IGNORECASE | re.MULTILINE,
)

# Pattern for abstract
_ABSTRACT_RE = re.compile(
    r"^(?:Abstract|摘要)[:\s]*\n*(.+?)(?=\n\n|\n\s*\d|$)",
    re.IGNORECASE | re.DOTALL,
)

# Pattern for keywords
_KEYWORDS_RE = re.compile(
    r"^(?:Keywords?|关键词)[:\s]*\n*(.+?)(?=\n\n|$)",
    re.IGNORECASE | re.MULTILINE,
)


def _level_from_label(label: str) -> int:
    """Calculate section level from label (e.g., '1.2.3' -> level 3)."""
    return label.count(".") + 1


def extract_structure(ocr_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract structured information from OCR text using regex patterns.

    Args:
        ocr_data: Output from OCRExtractor.extract()

    Returns:
        Dictionary with extracted structure
    """
    logger.info("Extracting structure from OCR data")

    # Initialize result structure
    result = {
        "metadata": {
            "extraction_time": datetime.now().isoformat(),
            "source": ocr_data.get("metadata", {}).get("source", "unknown"),
        },
        "sections": [],
        "theorems": [],
        "definitions": [],
        "proofs": [],
        "equations": [],
        "references": [],
        "abstract": "",
        "keywords": [],
        "authors": [],
    }

    # Extract from each page
    pages = ocr_data.get("pages", [])
    for page in pages:
        page_num = page.get("number", 0)
        text = page.get("text", "")

        if not text:
            continue

        # Extract sections
        for match in _SECTION_RE.finditer(text):
            label = match.group(1)
            title = match.group(2).strip()

            # Filter out very long or very short titles
            if len(title) > 200 or len(title) < 2:
                continue

            result["sections"].append(
                {
                    "id": f"sec{label}",
                    "label": label,
                    "title": title,
                    "level": _level_from_label(label),
                    "page": page_num,
                    "content_preview": text[:200] if text else "",
                }
            )

        # Extract theorems, lemmas, propositions, corollaries
        for match in _THEOREM_RE.finditer(text):
            thm_type = match.group("type")
            label = match.group("label")
            statement = match.group("statement").strip()

            # Find which section this theorem belongs to
            section_id = _find_parent_section(label, result["sections"])

            result["theorems"].append(
                {
                    "id": f"thm{label}",
                    "type": thm_type,
                    "label": label,
                    "statement": statement,
                    "page": page_num,
                    "section_id": section_id,
                }
            )

        # Extract definitions
        for match in _DEFINITION_RE.finditer(text):
            def_type = match.group("type")
            label = match.group("label")
            content = match.group("content").strip()

            section_id = _find_parent_section(label, result["sections"])

            result["definitions"].append(
                {
                    "id": f"def{label}",
                    "type": def_type,
                    "label": label,
                    "content": content,
                    "page": page_num,
                    "section_id": section_id,
                }
            )

        # Extract proofs
        for match in _PROOF_RE.finditer(text):
            # Get context around the proof keyword
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 300)
            context = text[start:end].strip()

            result["proofs"].append(
                {
                    "id": f"proof{len(result['proofs']) + 1}",
                    "keyword": match.group("keyword"),
                    "context": context,
                    "page": page_num,
                    "position": match.start(),
                }
            )

        # Extract display equations
        for match in _DISPLAY_MATH_RE.finditer(text):
            formula = match.group(1) or match.group(2)
            if formula:
                result["equations"].append(
                    {
                        "id": f"eq{len(result['equations']) + 1}",
                        "formula": formula.strip(),
                        "page": page_num,
                        "position": match.start(),
                        "type": "display",
                    }
                )

        # Extract references (only from first few pages typically)
        if page_num <= 3:  # References usually in first few pages
            for match in _REFERENCE_RE.finditer(text):
                ref_text = match.group(1)
                result["references"].append(
                    {
                        "id": f"ref{len(result['references']) + 1}",
                        "text": ref_text,
                        "page": page_num,
                        "position": match.start(),
                    }
                )

    # Extract metadata from first page
    if pages:
        first_page_text = pages[0].get("text", "")

        # Extract abstract
        abstract_match = _ABSTRACT_RE.search(first_page_text)
        if abstract_match:
            result["abstract"] = abstract_match.group(1).strip()

        # Extract keywords
        keywords_match = _KEYWORDS_RE.search(first_page_text)
        if keywords_match:
            keywords_text = keywords_match.group(1).strip()
            # Split by commas, semicolons, or newlines
            keywords = re.split(r"[,\n;]+", keywords_text)
            result["keywords"] = [k.strip() for k in keywords if k.strip()]

        # Extract authors (simple pattern)
        # Look for common author patterns in first 1000 chars
        first_part = first_page_text[:1000]
        for line in first_part.split("\n"):
            line = line.strip()
            if line and len(line) < 200:  # Reasonable author line length
                author_match = _AUTHOR_RE.match(line)
                if author_match:
                    author_info = author_match.group(1).strip()
                    result["authors"].append(
                        {
                            "name": author_info,
                            "affiliation": author_match.group(2).strip()
                            if author_match.group(2)
                            else "",
                        }
                    )

    logger.info(
        "Structure extraction completed: %d sections, %d theorems, %d definitions",
        len(result["sections"]),
        len(result["theorems"]),
        len(result["definitions"]),
    )

    return result


def _find_parent_section(label: str, sections: List[Dict]) -> Optional[str]:
    """
    Find the parent section for a theorem/definition label.

    Args:
        label: Theorem/definition label (e.g., "1.2.3")
        sections: List of extracted sections

    Returns:
        Section ID or None
    """
    if not sections:
        return None

    # Convert label to numeric parts
    label_parts = []
    for part in label.split("."):
        if part.isdigit():
            label_parts.append(int(part))
        else:
            break

    best_match = None
    best_score = -1

    for section in sections:
        section_label = section.get("label", "")
        section_parts = []
        for part in section_label.split("."):
            if part.isdigit():
                section_parts.append(int(part))
            else:
                break

        # Check if this section is a parent of the label
        if len(section_parts) <= len(label_parts):
            match = True
            for i in range(len(section_parts)):
                if i >= len(label_parts) or section_parts[i] != label_parts[i]:
                    match = False
                    break

            if match:
                # Score: more specific matches are better
                score = len(section_parts)
                if score > best_score:
                    best_score = score
                    best_match = section["id"]

    return best_match


def format_structure_for_display(structure: Dict[str, Any]) -> str:
    """
    Format extracted structure into readable text for LLM analysis.

    Args:
        structure: Output from extract_structure()

    Returns:
        Formatted text for LLM prompt
    """
    lines = []

    # Metadata
    lines.append("# Extracted Paper Structure")
    lines.append(f"Source: {structure.get('metadata', {}).get('source', 'unknown')}")
    lines.append(
        f"Extraction time: {structure.get('metadata', {}).get('extraction_time', 'unknown')}"
    )
    lines.append("")

    # Abstract
    abstract = structure.get("abstract", "")
    if abstract:
        lines.append("## Abstract")
        lines.append(abstract)
        lines.append("")

    # Keywords
    keywords = structure.get("keywords", [])
    if keywords:
        lines.append("## Keywords")
        lines.append(", ".join(keywords))
        lines.append("")

    # Authors
    authors = structure.get("authors", [])
    if authors:
        lines.append("## Authors")
        for author in authors:
            name = author.get("name", "")
            affiliation = author.get("affiliation", "")
            if affiliation:
                lines.append(f"- {name} ({affiliation})")
            else:
                lines.append(f"- {name}")
        lines.append("")

    # Sections
    sections = structure.get("sections", [])
    if sections:
        lines.append("## Sections")
        for sec in sorted(sections, key=lambda x: x.get("label", "")):
            indent = "  " * (sec.get("level", 1) - 1)
            lines.append(
                f"{indent}- **{sec['label']}** {sec.get('title', '')} (p.{sec.get('page', '?')})"
            )
        lines.append("")

    # Theorems
    theorems = structure.get("theorems", [])
    if theorems:
        lines.append("## Theorems, Lemmas, Propositions, Corollaries")
        for thm in sorted(theorems, key=lambda x: x.get("label", "")):
            thm_type = thm.get("type", "Theorem")
            label = thm.get("label", "")
            statement = thm.get("statement", "")[:150]
            section = (
                f" [Section {thm.get('section_id', '').replace('sec', '')}]"
                if thm.get("section_id")
                else ""
            )
            lines.append(
                f"- **{thm_type} {label}** (p.{thm.get('page', '?')}){section}: {statement}"
            )
        lines.append("")

    # Definitions
    definitions = structure.get("definitions", [])
    if definitions:
        lines.append("## Definitions")
        for d in sorted(definitions, key=lambda x: x.get("label", "")):
            def_type = d.get("type", "Definition")
            label = d.get("label", "")
            content = d.get("content", "")[:120]
            section = (
                f" [Section {d.get('section_id', '').replace('sec', '')}]"
                if d.get("section_id")
                else ""
            )
            lines.append(
                f"- **{def_type} {label}** (p.{d.get('page', '?')}){section}: {content}"
            )
        lines.append("")

    # Proofs
    proofs = structure.get("proofs", [])
    if proofs:
        lines.append("## Proof Contexts")
        for i, proof in enumerate(proofs):
            lines.append(f"### Proof {i + 1} (p.{proof.get('page', '?')})")
            lines.append(proof.get("context", "")[:200])
            lines.append("")

    # Equations
    equations = structure.get("equations", [])
    if equations:
        lines.append("## Key Equations")
        for i, eq in enumerate(equations[:10]):  # Show first 10 equations
            lines.append(
                f"{i + 1}. Page {eq.get('page', '?')}: $${eq.get('formula', '')}$$"
            )
        if len(equations) > 10:
            lines.append(f"... and {len(equations) - 10} more equations")
        lines.append("")

    # References
    references = structure.get("references", [])
    if references:
        lines.append("## References")
        ref_texts = sorted(set(ref.get("text", "") for ref in references))
        for ref_text in ref_texts[:20]:  # Show first 20 unique references
            lines.append(f"- [{ref_text}]")
        if len(ref_texts) > 20:
            lines.append(f"... and {len(ref_texts) - 20} more references")

    return "\n".join(lines)


def extract_structure_from_ocr(ocr_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for structure extraction.

    Args:
        ocr_data: Output from OCRExtractor.extract()

    Returns:
        Extracted structure
    """
    return extract_structure(ocr_data)
