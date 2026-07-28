"""
extractors — Turn any supported upload (PDF / CSV / TXT) into plain text
for the LLM. Adding a format = add a function + one dispatch line.
"""
from __future__ import annotations

import io

import pdfplumber


def _pdf_to_text(data: bytes) -> str:
    """Extract text page by page; append detected tables as pipe-separated rows
    (tables carry most of the financial signal in filings)."""
    parts: list[str] = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            parts.append(f"[Page {i}]\n{text}")
            for table in page.extract_tables():
                rows = [" | ".join("" if c is None else str(c).strip() for c in row) for row in table]
                parts.append("[Table]\n" + "\n".join(rows))
    return "\n\n".join(parts)


def _csv_to_text(data: bytes) -> str:
    """Pass CSV through as text (already structured); tolerate odd encodings."""
    return data.decode("utf-8", errors="replace")


def _txt_to_text(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


_DISPATCH = {
    "pdf": _pdf_to_text,
    "csv": _csv_to_text,
    "txt": _txt_to_text,
}

SUPPORTED_EXTENSIONS = sorted(_DISPATCH)


def extract_text(data: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in _DISPATCH:
        raise ValueError(f"Unsupported file type '.{ext}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}")
    text = _DISPATCH[ext](data)
    if not text.strip():
        raise ValueError("No text could be extracted from the document (is it a scanned image PDF?)")
    return text
