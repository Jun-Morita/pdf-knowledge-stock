"""Page image export helpers."""

from __future__ import annotations

from pathlib import Path

import pymupdf

from pdf_knowledge_stock.config import DEFAULT_IMAGE_DIR


def page_image_dir(pdf_path: Path, image_dir: Path = DEFAULT_IMAGE_DIR) -> Path:
    """Return the directory used for full-page images of a PDF."""
    return Path(image_dir) / Path(pdf_path).stem


def page_image_path(pdf_path: Path, page_number: int, image_dir: Path = DEFAULT_IMAGE_DIR) -> Path:
    """Return the image path for a one-based page number."""
    return page_image_dir(pdf_path, image_dir) / f"page_{page_number:03d}.png"


def export_page_images(
    pdf_path: Path,
    *,
    image_dir: Path = DEFAULT_IMAGE_DIR,
    dpi: int = 150,
) -> list[Path]:
    """Render each PDF page to a PNG image."""
    source_path = Path(pdf_path)
    output_dir = page_image_dir(source_path, image_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image_paths: list[Path] = []
    with pymupdf.open(source_path) as document:
        for page_index in range(document.page_count):
            output_path = page_image_path(source_path, page_index + 1, image_dir)
            pixmap = document[page_index].get_pixmap(dpi=dpi)
            pixmap.save(output_path)
            image_paths.append(output_path)

    return image_paths
