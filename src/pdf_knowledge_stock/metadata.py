"""Metadata and YAML front matter helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pymupdf

from pdf_knowledge_stock.config import DEFAULT_BACKEND, DEFAULT_DOC_TYPE, DEFAULT_STATUS


def current_timestamp() -> str:
    """Return an ISO-8601 timestamp for generated metadata."""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def build_source_metadata(
    pdf_path: Path,
    *,
    backend: str = DEFAULT_BACKEND,
    doc_type: str = DEFAULT_DOC_TYPE,
    status: str = DEFAULT_STATUS,
    created_at: str | None = None,
) -> dict[str, object]:
    """Build the minimum metadata saved with a generated Markdown note."""
    source_path = Path(pdf_path)
    return {
        "source_file": source_path.name,
        "source_path": source_path.as_posix(),
        "doc_type": doc_type,
        "conversion_backend": backend,
        "created_at": created_at or current_timestamp(),
        "status": status,
    }


def read_pdf_metadata(pdf_path: Path) -> dict[str, object]:
    """Read basic metadata from a PDF file."""
    with pymupdf.open(pdf_path) as document:
        metadata = document.metadata or {}
        return {
            "page_count": document.page_count,
            "pdf_title": metadata.get("title") or "",
            "pdf_author": metadata.get("author") or "",
            "pdf_creator": metadata.get("creator") or "",
            "pdf_producer": metadata.get("producer") or "",
            "pdf_creation_date": metadata.get("creationDate") or "",
            "pdf_mod_date": metadata.get("modDate") or "",
        }


def _render_yaml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int | float):
        return str(value)
    escaped = str(value).replace('"', '\\"')
    return f'"{escaped}"'


def render_front_matter(metadata: dict[str, object]) -> str:
    """Render a small YAML front matter block without adding a YAML dependency."""
    lines = ["---"]
    for key, value in metadata.items():
        lines.append(f"{key}: {_render_yaml_value(value)}")
    lines.append("---")
    return "\n".join(lines)
