"""Markdown note rendering helpers."""

from __future__ import annotations

from pathlib import Path


RAW_NOTE_FORMAT = "raw"
KNOWLEDGE_NOTE_FORMAT = "knowledge"
NOTE_FORMATS = (RAW_NOTE_FORMAT, KNOWLEDGE_NOTE_FORMAT)


def note_title_from_pdf(pdf_path: Path) -> str:
    """Create a readable fallback note title from a PDF file name."""
    return Path(pdf_path).stem.replace("_", " ").replace("-", " ").strip()


def render_knowledge_note(page_sections: str, *, title: str) -> str:
    """Render a structured knowledge note around page-level raw conversion."""
    return "\n\n".join(
        [
            f"# {title}",
            "## Executive Summary",
            "",
            "## Key Takeaways",
            "",
            "## Slide-by-slide Notes",
            page_sections.strip(),
            "## Important Terms",
            "",
            "## Follow-up Questions",
            "",
        ]
    ).strip()
