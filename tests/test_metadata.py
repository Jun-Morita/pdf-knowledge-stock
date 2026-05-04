from pathlib import Path

from pdf_knowledge_stock.convert import (
    output_markdown_path,
    page_image_markdown_link,
    remove_omitted_picture_markers,
    render_page_sections,
)
from pdf_knowledge_stock.images import page_image_dir, page_image_path
from pdf_knowledge_stock.metadata import build_source_metadata, render_front_matter


def test_build_source_metadata_uses_pdf_name_and_path() -> None:
    metadata = build_source_metadata(
        Path("data/raw/sample.pdf"),
        created_at="2026-05-04T00:00:00+09:00",
    )

    assert metadata["source_file"] == "sample.pdf"
    assert metadata["source_path"] == "data/raw/sample.pdf"
    assert metadata["doc_type"] == "slide_pdf"
    assert metadata["conversion_backend"] == "pymupdf4llm"
    assert metadata["created_at"] == "2026-05-04T00:00:00+09:00"
    assert metadata["status"] == "raw_conversion"


def test_render_front_matter_quotes_values() -> None:
    rendered = render_front_matter({"source_file": "sample.pdf"})

    assert rendered == '---\nsource_file: "sample.pdf"\n---'


def test_output_markdown_path_uses_pdf_stem() -> None:
    assert output_markdown_path(Path("data/raw/sample.pdf")) == Path("data/markdown/sample.md")


def test_page_image_paths_use_pdf_stem_and_page_number() -> None:
    pdf_path = Path("data/raw/sample.pdf")

    assert page_image_dir(pdf_path) == Path("data/images/sample")
    assert page_image_path(pdf_path, 3) == Path("data/images/sample/page_003.png")


def test_page_image_markdown_link_is_relative_to_markdown_file() -> None:
    link = page_image_markdown_link(
        Path("data/images/sample/page_001.png"),
        Path("data/markdown/sample.md"),
        1,
    )

    assert link == "![Page 1](../images/sample/page_001.png)"


def test_render_page_sections_adds_page_boundaries_and_images() -> None:
    rendered = render_page_sections(
        [
            {"metadata": {"page_number": 1}, "text": "# Title"},
            {"metadata": {"page_number": 2}, "text": "Body"},
        ],
        markdown_path=Path("data/markdown/sample.md"),
        pdf_path=Path("data/raw/sample.pdf"),
        include_images=True,
    )

    assert "## Page 1\n\n![Page 1](../images/sample/page_001.png)\n\n# Title" in rendered
    assert "## Page 2\n\n![Page 2](../images/sample/page_002.png)\n\nBody" in rendered


def test_remove_omitted_picture_markers_keeps_picture_text() -> None:
    cleaned = remove_omitted_picture_markers(
        "**==> picture [849 x 156] intentionally omitted <==**\n\n"
        "**----- Start of picture text -----**<br>\n"
        "Diagram text<br>\n"
        "**----- End of picture text -----**<br>\n"
    )

    assert "intentionally omitted" not in cleaned
    assert "Diagram text" in cleaned
