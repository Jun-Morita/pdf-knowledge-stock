"""Project defaults for file layout and conversion."""

from pathlib import Path

DEFAULT_MARKDOWN_DIR = Path("data/markdown")
DEFAULT_IMAGE_DIR = Path("data/images")
DEFAULT_DOC_TYPE = "slide_pdf"
DEFAULT_BACKEND = "pymupdf4llm"
DEFAULT_STATUS = "raw_conversion"
DEFAULT_OPENAI_MODEL = "gpt-5-mini"
DEFAULT_CLEAN_MAX_IMAGES = 10
