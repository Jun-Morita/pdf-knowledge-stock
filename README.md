# pdf-knowledge-stock

## What it is

A local-first tool for converting slide-style PDF documents into Markdown-based knowledge notes.

## Why it matters

IR materials, AI seminar slides, and technical PDFs often contain valuable knowledge, but they are difficult to search, summarize, and reuse as-is.

This project converts PDF documents into structured Markdown notes that can be used with Obsidian, LLM wiki workflows, and future RAG pipelines.

## Key features

- Convert PDF files into Markdown
- Preserve source metadata
- Export page-level notes
- Save extracted images or page snapshots
- Generate cleaned knowledge notes for long-term reuse

## Quick start

```bash
uv venv
source .venv/bin/activate
uv pip install pymupdf pymupdf4llm markitdown
````

```bash
python scripts/convert_pdf.py data/raw/sample.pdf
```
