# Roadmap

## Phase 1: Minimum Local Converter

- Accept one PDF path from the CLI.
- Convert it to Markdown with PyMuPDF4LLM.
- Add YAML front matter.
- Write the result to `data/markdown/`.

## Phase 2: Knowledge Note Format

- Add stable sections for summaries, key takeaways, slide-by-slide notes,
  important terms, and follow-up questions.
- Support `--note-format knowledge` for editable knowledge-note skeletons.

## Phase 3: Image Export

- Add `--export-images`.
- Save page images under `data/images/<pdf_stem>/`.

## Phase 4: Optional LLM Cleanup

- Add opt-in cleanup and summarization.
- Keep local conversion working without API keys.

## Phase 5: Codex Skill

- Package the stable workflow as a reusable Codex skill.
