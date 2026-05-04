# pdf-knowledge-stock

A local-first tool for converting slide-style PDF documents into
Markdown-based knowledge notes.

This project is intended for materials such as company IR decks, AI / LLM study
slides, technical seminar PDFs, and other documents that are useful to keep as a
searchable personal or team knowledge base.

> Status: early development. The minimum local converter and page image export
> are available.

## Why

Important information is often locked inside PDF slide decks. They are easy to
read once, but hard to search, compare, annotate, summarize, and reuse later.

`pdf-knowledge-stock` aims to turn those PDFs into Markdown notes that can be
used with:

- Obsidian or other Markdown note systems
- Local document analysis workflows
- LLM wiki / knowledge stock workflows
- Future RAG-ready datasets
- Future Codex skills

## Principles

- Local-first: the core workflow must work without external APIs or API keys.
- Source-preserving: original PDFs stay outside Git, and generated notes keep
  source metadata.
- Reproducible: conversions should run from the CLI with explicit options.
- Markdown-first: output should be useful as knowledge notes, not just raw text.
- Incremental: start with simple conversion, then add images, cleanup, indexing,
  and RAG formats.

## Current Features

- Convert one PDF into one Markdown file.
- Add YAML front matter with source metadata.
- Preserve page boundaries as `## Page N` sections.
- Export page snapshots for slide-heavy PDFs with `--export-images`.
- Link exported page images from the generated Markdown.

## Planned Features

- Generate structured note sections for analysis and review.
- Keep optional LLM cleanup separate from the local conversion path.

## Target Output

```markdown
---
source_file: sample.pdf
source_path: data/raw/sample.pdf
doc_type: slide_pdf
conversion_backend: pymupdf4llm
created_at: "2026-05-04T00:00:00+09:00"
status: raw_conversion
page_count: 10
---

## Page 1

![Page 1](../images/sample/page_001.png)

# Title

Page-level converted Markdown...
```

Structured knowledge-note sections such as `Executive Summary` and
`Key Takeaways` are planned for a later phase.

## Repository Layout

Repository structure:

```text
pdf-knowledge-stock/
  README.md
  AGENTS.md
  pyproject.toml
  .gitignore
  .env.example

  src/
    pdf_knowledge_stock/
      __init__.py
      convert.py
      config.py
      metadata.py

  scripts/
    convert_pdf.py

  docs/
    design.md
    roadmap.md

  examples/
    README.md

  data/
    raw/
    markdown/
    images/
    metadata/
    summaries/
```

## Quick Start

The CLI runs through `uv`.

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

Convert a PDF:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf
```

Default output:

```text
data/markdown/sample.md
```

Export page images and link them from Markdown:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf --export-images
```

Overwrite an existing generated Markdown file:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf --force
```

## Data Policy

Do not commit source PDFs or generated knowledge files by default.

The project is designed around this layout:

```text
data/raw/        # input PDFs, ignored by Git
data/markdown/   # generated Markdown, ignored by Git
data/images/     # exported page images, ignored by Git
data/metadata/   # generated metadata, ignored by Git
data/summaries/  # generated summaries, ignored by Git
```

PDFs, extracted text, images, and generated notes should be treated as private
user data unless explicitly shared by the user.

## Roadmap

### Phase 1: Minimum Local Converter

Status: implemented.

- Accept a PDF path from the CLI.
- Convert the PDF to Markdown with PyMuPDF4LLM.
- Write Markdown to `data/markdown/`.
- Add YAML front matter.
- Work without external API keys.

### Phase 2: Knowledge Note Format

Status: planned.

- Add stable sections for summaries, takeaways, slide notes, terms, and follow-up
  questions.
- Keep raw conversion status clear so users can manually edit notes later.

### Phase 3: Image and Page Snapshot Support

Status: implemented for full-page snapshots.

- Add `--export-images`.
- Save page images under `data/images/<pdf_stem>/`.
- Reference useful page images from Markdown when appropriate.

### Phase 4: Optional LLM Cleanup

- Add opt-in cleanup or summarization.
- Keep API-based processing separate from local conversion.
- Keep local conversion usable without API keys.

### Phase 5: Codex Skill

- Package the stable workflow as a reusable Codex skill.
- Support PDF reading, Markdown conversion, metadata preservation, image export,
  indexing, and RAG-ready outputs.

## Development

See [AGENTS.md](AGENTS.md) for project rules and implementation policy.

Expected tooling:

- Python
- `uv`
- PyMuPDF4LLM for the first conversion backend
- PyMuPDF for page rendering and image export

Once tests are added, the intended command is:

```bash
uv run --extra dev pytest
```

## License

This repository currently uses the MIT License. See [LICENSE](LICENSE).

If the licensing policy changes before wider release, update both `LICENSE` and
this section together.
