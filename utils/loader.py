from __future__ import annotations

from pathlib import Path


def load_file(path: str) -> str:
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix in {".md", ".txt"}:
        return file_path.read_text(encoding="utf-8")

    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ImportError(
                "Missing dependency 'pypdf'. Install it with: ./.venv/bin/pip install pypdf"
            ) from exc

        reader = PdfReader(str(file_path))
        pages_text: list[str] = []
        for page in reader.pages:
            text = page.extract_text() or ""
            pages_text.append(text)

        return "\n\n".join(pages_text).strip()

    raise ValueError(f"Unsupported file type: {suffix}")
