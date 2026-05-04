# Design

`pdf-knowledge-stock` is a local-first converter for slide-style PDFs.

The first implementation focuses on a narrow path:

1. Read one PDF from the local filesystem.
2. Convert it to Markdown with PyMuPDF4LLM.
3. Add source metadata as YAML front matter.
4. Write the result under `data/markdown/`.

Future phases can add page snapshots, structured cleanup, indexing, and
RAG-ready exports without changing the local-first default.
