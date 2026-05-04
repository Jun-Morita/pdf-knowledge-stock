from pathlib import Path

from pdf_knowledge_stock.cli import build_parser
from pdf_knowledge_stock.openai_cleanup import OpenAICleanupError


def test_cli_uses_openai_cleanup_by_default() -> None:
    args = build_parser().parse_args(["data/raw/sample.pdf"])

    assert args.clean is True


def test_cli_can_disable_openai_cleanup() -> None:
    args = build_parser().parse_args(["data/raw/sample.pdf", "--no-clean"])

    assert args.clean is False


def test_openai_cleanup_error_keeps_output_paths() -> None:
    error = OpenAICleanupError(
        "failed",
        raw_markdown_path=Path("data/markdown/sample.md"),
        clean_markdown_path=Path("data/markdown/sample.clean.md"),
    )

    assert str(error) == "failed"
    assert error.raw_markdown_path == Path("data/markdown/sample.md")
    assert error.clean_markdown_path == Path("data/markdown/sample.clean.md")
