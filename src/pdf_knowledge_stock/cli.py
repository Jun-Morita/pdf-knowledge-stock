"""Command-line interface for PDF conversion."""

from __future__ import annotations

import argparse
from pathlib import Path

from pdf_knowledge_stock.config import DEFAULT_IMAGE_DIR, DEFAULT_MARKDOWN_DIR
from pdf_knowledge_stock.convert import convert_pdf_to_markdown_file
from pdf_knowledge_stock.notes import NOTE_FORMATS, RAW_NOTE_FORMAT


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a slide-style PDF into a Markdown knowledge note.",
    )
    parser.add_argument("pdf_path", type=Path, help="Path to the source PDF.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_MARKDOWN_DIR,
        help="Directory for generated Markdown files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the generated Markdown file if it already exists.",
    )
    parser.add_argument(
        "--export-images",
        action="store_true",
        help="Render each PDF page to a PNG image and link it from Markdown.",
    )
    parser.add_argument(
        "--image-dir",
        type=Path,
        default=DEFAULT_IMAGE_DIR,
        help="Base directory for exported page images.",
    )
    parser.add_argument(
        "--image-dpi",
        type=int,
        default=150,
        help="DPI for exported page images.",
    )
    parser.add_argument(
        "--note-format",
        choices=NOTE_FORMATS,
        default=RAW_NOTE_FORMAT,
        help="Markdown note format to generate.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    output_path = convert_pdf_to_markdown_file(
        args.pdf_path,
        output_dir=args.output_dir,
        image_dir=args.image_dir,
        export_images=args.export_images,
        image_dpi=args.image_dpi,
        note_format=args.note_format,
        force=args.force,
    )
    print(output_path)
