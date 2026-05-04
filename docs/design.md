# Design

`pdf-knowledge-stock` converts slide-style PDFs into cleaner Markdown notes.

The implementation focuses on a narrow path:

1. Read one PDF from the local filesystem.
2. Convert it to Markdown with PyMuPDF4LLM.
3. Add source metadata as YAML front matter.
4. Optionally export page images.
5. Clean the generated Markdown with OpenAI by default.
6. Write the result under `data/markdown/`.

Local-only conversion remains available with `--no-clean`.
