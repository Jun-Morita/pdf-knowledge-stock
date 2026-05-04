"""Optional OpenAI-based Markdown cleanup."""

from __future__ import annotations

import base64
import mimetypes
import os
import re
from pathlib import Path

from pdf_knowledge_stock.config import DEFAULT_CLEAN_MAX_IMAGES, DEFAULT_OPENAI_MODEL

IMAGE_LINK_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


class OpenAICleanupError(RuntimeError):
    """Raised when OpenAI cleanup fails after local conversion succeeds."""

    def __init__(self, message: str, *, raw_markdown_path: Path, clean_markdown_path: Path):
        super().__init__(message)
        self.raw_markdown_path = raw_markdown_path
        self.clean_markdown_path = clean_markdown_path


def load_env_file(env_path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE pairs from a .env file without overriding env vars."""
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def resolve_openai_api_key(env_path: Path = Path(".env")) -> str:
    """Return the OpenAI API key from the environment or .env."""
    load_env_file(env_path)
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Create .env from .env.example.")
    return api_key


def resolve_openai_model(env_path: Path = Path(".env"), fallback: str = DEFAULT_OPENAI_MODEL) -> str:
    """Return the cleanup model from env or the project default."""
    load_env_file(env_path)
    return os.environ.get("OPENAI_MODEL", fallback).strip() or fallback


def cleaned_markdown_path(markdown_path: Path) -> Path:
    """Return the default cleaned Markdown output path."""
    source_path = Path(markdown_path)
    if source_path.stem.endswith(".clean"):
        return source_path
    return source_path.with_name(f"{source_path.stem}.clean{source_path.suffix}")


def extract_markdown_image_paths(markdown_path: Path) -> list[Path]:
    """Extract local image paths referenced from a Markdown file."""
    source_path = Path(markdown_path)
    image_paths: list[Path] = []
    for match in IMAGE_LINK_PATTERN.finditer(source_path.read_text(encoding="utf-8")):
        raw_path = match.group(1).strip()
        if raw_path.startswith(("http://", "https://", "data:")):
            continue
        image_path = (source_path.parent / raw_path).resolve()
        if image_path.exists():
            image_paths.append(image_path)
    return image_paths


def image_to_data_url(image_path: Path) -> str:
    """Encode a local image file as a base64 data URL."""
    mime_type = mimetypes.guess_type(image_path)[0] or "image/png"
    encoded = base64.b64encode(Path(image_path).read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def strip_markdown_code_fence(text: str) -> str:
    """Remove a single outer Markdown code fence if the model added one."""
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if len(lines) >= 2 and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return stripped


def build_cleanup_prompt(markdown_text: str) -> str:
    """Build the cleanup prompt for slide-style PDF Markdown."""
    return f"""You are cleaning Markdown converted from a slide-style PDF.

Return only the improved Markdown. Do not wrap the answer in a code fence.

Goals:
- Preserve the YAML front matter, but set status to "cleaned_with_openai".
- Keep source metadata fields.
- Use the page images to correct slide titles, tables, charts, and diagram text when useful.
- Produce readable Markdown for Obsidian / knowledge-note workflows.
- Keep page references where they help traceability.
- Add or improve these sections: Executive Summary, Key Takeaways, Slide-by-slide Notes, Important Terms, Follow-up Questions.
- Do not invent facts that are not supported by the Markdown or images.
- Prefer concise bullets over dense paragraphs.

Input Markdown:

{markdown_text}
"""


def clean_markdown_with_openai(
    markdown_path: Path,
    *,
    output_path: Path | None = None,
    model: str | None = None,
    max_images: int = DEFAULT_CLEAN_MAX_IMAGES,
    env_path: Path = Path(".env"),
) -> Path:
    """Clean a generated Markdown note with OpenAI using linked page images."""
    from openai import OpenAI

    source_path = Path(markdown_path)
    api_key = resolve_openai_api_key(env_path)
    resolved_model = model or resolve_openai_model(env_path)
    destination_path = output_path or cleaned_markdown_path(source_path)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_text = source_path.read_text(encoding="utf-8")

    content: list[dict[str, object]] = [
        {"type": "input_text", "text": build_cleanup_prompt(markdown_text)}
    ]
    for image_path in extract_markdown_image_paths(source_path)[:max_images]:
        content.append(
            {
                "type": "input_image",
                "image_url": image_to_data_url(image_path),
                "detail": "high",
            }
        )

    client = OpenAI(api_key=api_key)
    try:
        response = client.responses.create(
            model=resolved_model,
            input=[{"role": "user", "content": content}],
        )
    except Exception as exc:
        message = str(exc)
        if "insufficient_quota" in message:
            message = (
                "OpenAI cleanup failed because the API key has insufficient quota. "
                "Check your OpenAI plan and billing details, or rerun with --no-clean."
            )
        elif "rate_limit" in message.lower() or "429" in message:
            message = "OpenAI cleanup failed because of a rate limit. Retry later or rerun with --no-clean."
        raise OpenAICleanupError(
            message,
            raw_markdown_path=source_path,
            clean_markdown_path=destination_path,
        ) from exc
    destination_path.write_text(
        strip_markdown_code_fence(response.output_text) + "\n",
        encoding="utf-8",
    )
    return destination_path
