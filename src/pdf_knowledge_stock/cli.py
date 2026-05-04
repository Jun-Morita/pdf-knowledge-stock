"""Command-line interface for PDF conversion."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pdf_knowledge_stock.config import (
    DEFAULT_CLEAN_MAX_IMAGES,
    DEFAULT_IMAGE_DIR,
    DEFAULT_MARKDOWN_DIR,
    DEFAULT_OPENAI_MODEL,
)
from pdf_knowledge_stock.convert import convert_pdf_to_markdown_file
from pdf_knowledge_stock.notes import NOTE_FORMATS, RAW_NOTE_FORMAT
from pdf_knowledge_stock.openai_cleanup import OpenAICleanupError


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
    clean_group = parser.add_mutually_exclusive_group()
    clean_group.add_argument(
        "--clean",
        dest="clean",
        action="store_true",
        default=True,
        help="Use OpenAI to refine the generated Markdown. This is the default.",
    )
    clean_group.add_argument(
        "--no-clean",
        dest="clean",
        action="store_false",
        help="Run only the local PDF-to-Markdown conversion without OpenAI.",
    )
    parser.add_argument(
        "--clean-model",
        default=None,
        help=f"OpenAI model for cleanup. Defaults to OPENAI_MODEL or {DEFAULT_OPENAI_MODEL}.",
    )
    parser.add_argument(
        "--clean-max-images",
        type=int,
        default=DEFAULT_CLEAN_MAX_IMAGES,
        help="Maximum number of page images to send to OpenAI.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        output_path = convert_pdf_to_markdown_file(
            args.pdf_path,
            output_dir=args.output_dir,
            image_dir=args.image_dir,
            export_images=args.export_images,
            image_dpi=args.image_dpi,
            note_format=args.note_format,
            clean=args.clean,
            clean_model=args.clean_model,
            clean_max_images=args.clean_max_images,
            force=args.force,
        )
    except OpenAICleanupError as exc:
        print(str(exc), file=sys.stderr)
        print(f"Raw Markdown was still written to: {exc.raw_markdown_path}", file=sys.stderr)
        print(f"Cleaned Markdown was not written to: {exc.clean_markdown_path}", file=sys.stderr)
        print("Local-only fallback:", file=sys.stderr)
        print(f"  uv run python scripts/convert_pdf.py {args.pdf_path} --no-clean --force", file=sys.stderr)
        raise SystemExit(1) from exc
    print(output_path)
