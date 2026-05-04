# AGENTS.md

## Project Goal

Build a local-first PDF-to-Markdown knowledge stock tool for slide-style PDF
documents such as company IR materials, AI / LLM seminar slides, and technical
study materials.

The tool should help users convert PDFs into Markdown notes that are useful for:

- Reading and search
- Obsidian or LLM wiki workflows
- Company and technical document analysis
- Future RAG-ready document preparation
- Future reuse as a Codex skill

## Core Principles

1. Local-first
   - The core workflow must work without external APIs or API keys.
   - Do not send PDFs, extracted text, images, or generated notes to external
     services by default.
   - Optional API-based cleanup or summarization may be added later, but it must
     be explicit, documented, and disabled by default.

2. Source preservation
   - Keep original PDFs out of Git.
   - Preserve source metadata in every generated Markdown file.
   - Do not overwrite user-provided source files.

3. Reproducibility
   - Conversion must be executable from the CLI.
   - The same input, backend, and config should produce similar output.
   - Prefer explicit command options over hidden runtime behavior.

4. Markdown as knowledge
   - Generated Markdown should be useful as a note, not only as a raw text dump.
   - Preserve page boundaries when possible.
   - Prefer clear headings, source metadata, and stable file paths.

5. Small steps
   - Start with a minimum PDF-to-Markdown converter.
   - Add structured note cleanup, indexing, and RAG formats in
     separate steps.

## Development Rules

- Prefer simple, readable Python.
- Use `uv` for environment and dependency management.
- Keep comments in English.
- Do not require external APIs for the core workflow.
- Do not hardcode API keys, local absolute paths, or user-specific secrets.
- Keep CLI commands reproducible.
- Add focused tests when adding core logic.
- Prefer existing standard-library modules unless a dependency clearly improves
  PDF conversion quality or maintainability.
- Keep generated outputs deterministic enough for review and repeat runs.

## Environment

Primary development environment:

- Windows 11 host
- Ubuntu / WSL development shell
- Python managed by `uv`

Common commands should work from the repository root.

## Initial Backend Policy

- Start with PyMuPDF4LLM for Phase 1.
- Use PyMuPDF directly where it is a better fit for page rendering or image
  export.
- Add MarkItDown, Docling, or other backends only after the minimum converter
  works.
- If multiple conversion backends are added, keep backend selection explicit in
  CLI options and output metadata.

## Directory Policy

Expected project structure:

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

## Git and Data Policy

Do not commit actual PDFs or generated knowledge files by default.

`.gitignore` should include:

```gitignore
.venv/
__pycache__/
*.pyc
.env

data/raw/
data/markdown/
data/images/
data/metadata/
data/summaries/

*.pdf
```

If examples are needed later, use tiny synthetic fixtures or clearly licensed
sample files.

## CLI Policy

Current conversion command:

```bash
uv run python scripts/convert_pdf.py data/raw/sample.pdf
```

Default output:

```text
data/markdown/sample.md
```

Current options:

- `--output-dir data/markdown`
- `--export-images`
- `--image-dir data/images`
- `--image-dpi 150`
- `--force` to overwrite existing generated files

Expected future options:

- `--backend pymupdf4llm`
- `--clean` for optional LLM cleanup, disabled by default

Do not overwrite generated files silently unless the command clearly documents
that behavior.

## Output Policy

Generated Markdown must include YAML front matter.

Minimum fields:

```yaml
---
source_file: sample.pdf
source_path: data/raw/sample.pdf
doc_type: slide_pdf
conversion_backend: pymupdf4llm
created_at: "2026-05-04T00:00:00+09:00"
status: raw_conversion
page_count: 10
pdf_creator: Microsoft PowerPoint
pdf_producer: Microsoft PowerPoint
pdf_creation_date: D:20260127231601+09'00'
---
```

Current raw conversion format:

```markdown
## Page 1

![Page 1](../images/sample/page_001.png)

Page-level converted Markdown...
```

Recommended future structured note format:

```markdown
# Title

## Executive Summary

## Key Takeaways

## Slide-by-slide Notes

## Important Terms

## Follow-up Questions
```

In Phase 1, summary sections may be empty placeholders or omitted if the output
is explicitly marked as `raw_conversion`.

## Phase Plan

### Phase 1: Minimum Local Converter

Goal: convert one PDF into one Markdown file.

Status: implemented.

Acceptance criteria:

- CLI accepts a PDF path.
- Markdown is written to `data/markdown/`.
- YAML front matter is added.
- Page boundaries are preserved when practical.
- Works without external API keys.

### Phase 2: Better Knowledge Note Format

Goal: convert raw Markdown into structured knowledge notes.

Status: next planned phase.

Acceptance criteria:

- Output has stable sections for reading and analysis.
- Raw conversion status is clear.
- Manually editable summary sections are supported.

### Phase 3: Image and Page Snapshot Support

Goal: support slide PDFs where diagrams, charts, and tables matter.

Status: implemented for full-page snapshots.

Expected output:

```text
data/images/sample/
  page_001.png
  page_002.png
```

Acceptance criteria:

- Optional `--export-images` flag.
- Page images are saved under `data/images/<pdf_stem>/`.
- Markdown references exported images from each page section.

### Phase 4: Optional LLM Cleanup

Goal: optionally clean raw Markdown into richer knowledge notes.

Acceptance criteria:

- LLM use is opt-in.
- Local conversion still works without API keys.
- API-based processing is separated from local conversion code.
- Prompts and model settings are documented and reproducible.

### Phase 5: Codex Skill

Goal: convert the stable workflow into a reusable Codex skill.

Skill responsibilities may include:

- Read a PDF
- Convert it to Markdown
- Preserve metadata
- Save page images
- Generate a knowledge-note structure
- Update index files
- Prepare RAG-ready outputs

## Testing Policy

- Add unit tests for metadata generation, path handling, and front matter.
- Add integration tests for CLI behavior when practical.
- Use tiny synthetic PDFs for tests.
- Do not add real IR materials, proprietary slides, or large PDFs to the repo.
- Tests should run with `uv run --extra dev pytest`.

## Security and Privacy Policy

- Never hardcode API keys.
- Use `.env.example` only for documented configuration names.
- Treat PDFs, extracted text, images, and generated Markdown as potentially
  private user data.
- Keep external network calls out of the default path.

## License Policy

The repository license is defined by the `LICENSE` file.

If the license is still undecided, do not describe the project as open-source in
documentation until the license is selected. For a public developer tool, MIT or
Apache-2.0 are both reasonable defaults:

- MIT is simple and permissive.
- Apache-2.0 is also permissive and includes an explicit patent grant.

Prefer Apache-2.0 if patent clarity matters; prefer MIT if simplicity matters
more.
