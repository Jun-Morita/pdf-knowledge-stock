# pdf-knowledge-stock

A PDF-to-Markdown tool for converting slide-style PDF documents into
Markdown-based knowledge notes, with OpenAI cleanup enabled by default.

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
- Future Codex skills

## Principles

- OpenAI-enhanced by default: the CLI refines generated Markdown with OpenAI
  unless `--no-clean` is passed.
- Local conversion remains available: use `--no-clean` to run without external
  APIs or API keys.
- Source-preserving: original PDFs stay outside Git, and generated notes keep
  source metadata.
- Reproducible: conversions should run from the CLI with explicit options.
- Markdown-first: output should be useful as knowledge notes, not just raw text.
- Incremental: start with simple conversion, then add images and optional
  OpenAI-based Markdown cleanup.

## Current Features

- Convert one PDF into one Markdown file.
- Add YAML front matter with source metadata.
- Preserve page boundaries as `## Page N` sections.
- Export page snapshots for slide-heavy PDFs with `--export-images`.
- Link exported page images from the generated Markdown.
- Generate a structured knowledge-note skeleton with `--note-format knowledge`.
- Improve generated Markdown with the OpenAI API using converted text and page
  images as input by default.

## Next Focus

- Tune the OpenAI cleanup prompt for IR decks, AI seminar slides, and technical
  study materials.
- Improve cleaned Markdown quality while keeping the local conversion path
  unchanged.

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
`Key Takeaways` can be added with `--note-format knowledge`.

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
```

## Quick Start

The CLI runs through `uv`.

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

Convert a PDF and refine the generated Markdown with OpenAI:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf
```

Default output:

```text
data/markdown/sample.clean.md
```

Run only the local PDF-to-Markdown conversion:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf --no-clean
```

Local-only output:

```text
data/markdown/sample.md
```

Export page images and link them from Markdown:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf --export-images
```

Generate an editable knowledge-note skeleton:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf --note-format knowledge
```

OpenAI cleanup implies page image export. Re-running the default command
overwrites both the intermediate raw Markdown and the cleaned Markdown output.

Overwrite an existing generated Markdown file:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf --force
```

## OpenAI Cleanup

The default command uses OpenAI cleanup and reads `OPENAI_API_KEY` from `.env`.
Use `--no-clean` for local-only conversion without API keys.

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5-mini
```

Do not commit `.env`.

The default cleanup sends the generated Markdown and up to `--clean-max-images`
linked page images to OpenAI. The original PDF is not sent by the cleanup step.

If OpenAI returns `insufficient_quota`, check your OpenAI billing / usage limits
or rerun local-only conversion with `--no-clean`.

Useful options:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf --clean --clean-max-images 5
uv run python scripts/convert_pdf.py data/raw/sample.pdf --clean --clean-model gpt-5-mini
uv run python scripts/convert_pdf.py data/raw/sample.pdf --no-clean
```

## Data Policy

Do not commit source PDFs or generated knowledge files by default.

The project is designed around this layout:

```text
data/raw/        # input PDFs, ignored by Git
data/markdown/   # generated Markdown, ignored by Git
data/images/     # exported page images, ignored by Git
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

Status: implemented as an editable skeleton.

- Add stable sections for summaries, takeaways, slide notes, terms, and follow-up
  questions.
- Keep raw conversion status clear so users can manually edit notes later.

### Phase 3: Image and Page Snapshot Support

Status: implemented for full-page snapshots.

- Add `--export-images`.
- Save page images under `data/images/<pdf_stem>/`.
- Reference useful page images from Markdown when appropriate.

### Phase 4: OpenAI Cleanup

Status: implemented as the default CLI path.

- Add OpenAI cleanup that uses generated Markdown and page images.
- Keep API-based processing separate from local conversion.
- Keep local conversion usable without API keys via `--no-clean`.

### Phase 5: Codex Skill

- Package the stable workflow as a reusable Codex skill.
- Support PDF reading, Markdown conversion, metadata preservation, image export,
  and optional Markdown cleanup.

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
