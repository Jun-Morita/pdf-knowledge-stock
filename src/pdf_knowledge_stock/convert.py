"""PDF conversion orchestration."""

from __future__ import annotations

import os
import re
from pathlib import Path

import pymupdf4llm

from pdf_knowledge_stock.config import (
    DEFAULT_BACKEND,
    DEFAULT_CLEAN_MAX_IMAGES,
    DEFAULT_IMAGE_DIR,
    DEFAULT_MARKDOWN_DIR,
)
from pdf_knowledge_stock.images import export_page_images, page_image_path
from pdf_knowledge_stock.metadata import (
    build_source_metadata,
    read_pdf_metadata,
    render_front_matter,
)
from pdf_knowledge_stock.openai_cleanup import clean_markdown_with_openai
from pdf_knowledge_stock.notes import (
    KNOWLEDGE_NOTE_FORMAT,
    RAW_NOTE_FORMAT,
    note_title_from_pdf,
    render_knowledge_note,
)


def output_markdown_path(pdf_path: Path, output_dir: Path = DEFAULT_MARKDOWN_DIR) -> Path:
    """Return the default Markdown output path for a source PDF."""
    return Path(output_dir) / f"{Path(pdf_path).stem}.md"


def convert_pdf_to_markdown_text(pdf_path: Path) -> str:
    """Convert a PDF to Markdown text using PyMuPDF4LLM."""
    return pymupdf4llm.to_markdown(str(pdf_path))


def convert_pdf_to_page_markdown(pdf_path: Path) -> list[dict[str, object]]:
    """Convert a PDF to page-level Markdown chunks using PyMuPDF4LLM."""
    return pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)


def page_image_markdown_link(image_path: Path, markdown_path: Path, page_number: int) -> str:
    """Return a Markdown image link from a note to a page snapshot."""
    relative_path = os.path.relpath(image_path, start=markdown_path.parent)
    return f"![Page {page_number}]({relative_path.replace(os.sep, '/')})"


def remove_omitted_picture_markers(markdown_text: str) -> str:
    """Remove PyMuPDF4LLM image omission placeholders from Markdown text."""
    return re.sub(
        r"^\*\*==> picture \[[^\]]+\] intentionally omitted <==\*\*\s*\n*",
        "",
        markdown_text,
        flags=re.MULTILINE,
    ).strip()


def render_page_sections(
    page_chunks: list[dict[str, object]],
    *,
    markdown_path: Path,
    pdf_path: Path,
    image_dir: Path = DEFAULT_IMAGE_DIR,
    include_images: bool = False,
) -> str:
    """Render page-level Markdown sections with optional page image links."""
    sections: list[str] = []
    for index, page_chunk in enumerate(page_chunks, start=1):
        page_number = page_chunk.get("metadata", {}).get("page_number", index)
        section_lines = [f"## Page {page_number}", ""]
        if include_images:
            image_path = page_image_path(pdf_path, int(page_number), image_dir)
            section_lines.extend(
                [
                    page_image_markdown_link(image_path, markdown_path, int(page_number)),
                    "",
                ]
            )
        page_text = str(page_chunk.get("text", "")).strip()
        if include_images:
            page_text = remove_omitted_picture_markers(page_text)
        section_lines.append(page_text)
        sections.append("\n".join(section_lines).rstrip())
    return "\n\n".join(sections).strip()


def convert_pdf_to_markdown_file(
    pdf_path: Path,
    *,
    output_dir: Path = DEFAULT_MARKDOWN_DIR,
    image_dir: Path = DEFAULT_IMAGE_DIR,
    export_images: bool = False,
    image_dpi: int = 150,
    note_format: str = RAW_NOTE_FORMAT,
    clean: bool = False,
    clean_model: str | None = None,
    clean_max_images: int = DEFAULT_CLEAN_MAX_IMAGES,
    force: bool = False,
) -> Path:
    """Convert one PDF into one Markdown file with YAML front matter."""
    source_path = Path(pdf_path)
    if not source_path.exists():
        raise FileNotFoundError(f"PDF not found: {source_path}")
    if source_path.suffix.lower() != ".pdf":
        raise ValueError(f"Input must be a PDF file: {source_path}")

    output_path = output_markdown_path(source_path, output_dir)
    if output_path.exists() and not (force or clean):
        raise FileExistsError(f"Output already exists: {output_path}")

    metadata = build_source_metadata(source_path, backend=DEFAULT_BACKEND)
    if note_format == KNOWLEDGE_NOTE_FORMAT:
        metadata["status"] = "knowledge_skeleton"
    elif note_format != RAW_NOTE_FORMAT:
        raise ValueError(f"Unsupported note format: {note_format}")
    metadata.update(read_pdf_metadata(source_path))
    page_chunks = convert_pdf_to_page_markdown(source_path)
    include_images = export_images or clean
    if include_images:
        export_page_images(source_path, image_dir=image_dir, dpi=image_dpi)
    page_sections = render_page_sections(
        page_chunks,
        markdown_path=output_path,
        pdf_path=source_path,
        image_dir=image_dir,
        include_images=include_images,
    )
    if note_format == KNOWLEDGE_NOTE_FORMAT:
        body = render_knowledge_note(page_sections, title=note_title_from_pdf(source_path))
    else:
        body = page_sections
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"{render_front_matter(metadata)}\n\n{body}", encoding="utf-8")
    if clean:
        return clean_markdown_with_openai(
            output_path,
            model=clean_model,
            max_images=clean_max_images,
        )
    return output_path
