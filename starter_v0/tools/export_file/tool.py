from __future__ import annotations

import json
import os
import re
from html import escape as escape_html
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


TOOL_NAME = "export_file"
SUPPORTED_FORMATS = ("pdf", "json", "html")
KNOWN_EXTENSIONS = ("pdf", "json", "html", "md", "csv", "txt")
DEFAULT_EXPORT_DIR = "exports"
MAX_STEM_LEN = 100
FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
)


def _error(message: str) -> dict[str, Any]:
    return {"tool": TOOL_NAME, "error": message}


def _is_empty(content: Any) -> bool:
    if content is None:
        return True
    if isinstance(content, str):
        return not content.strip()
    return len(content) == 0


def _input_error(content: Any) -> tuple[bool, Any]:
    if isinstance(content, dict):
        return ("error" in content, content.get("error"))
    if isinstance(content, str):
        try:
            parsed = json.loads(content)
        except ValueError:
            return False, None
        if isinstance(parsed, dict):
            return ("error" in parsed, parsed.get("error"))
    return False, None


def _safe_filename(name: Any, fmt: str) -> str:
    base = re.split(r"[\\/]", name if isinstance(name, str) else "")[-1].strip()
    for extension in KNOWN_EXTENSIONS:
        if base.lower().endswith(f".{extension}"):
            base = base[: -(len(extension) + 1)]
            break
    base = re.sub(r"[^\w.\- ]", "_", base).lstrip(". ")[:MAX_STEM_LEN].rstrip(". ")
    return f"{base or 'digest'}.{fmt}"


def _unique_path(directory: Path, filename: str) -> Path:
    path = directory / filename
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    for index in range(1, 1000):
        candidate = directory / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
    raise FileExistsError(f"too many files named {filename}")


def _to_json_text(content: Any) -> str:
    data: Any = content
    if isinstance(content, str):
        try:
            parsed = json.loads(content)
        except ValueError:
            parsed = None
        data = parsed if isinstance(parsed, (list, dict)) else {"content": content}
    return json.dumps(data, ensure_ascii=False, indent=2)


def _item_lines(item: Any) -> list[str]:
    if not isinstance(item, dict):
        return [f"- {item}"]
    title, url = item.get("title"), item.get("url")
    summary = item.get("summary") or item.get("text")
    lines: list[str] = []
    if title or url:
        lines.append(f"- {title or url}")
    if title and url:
        lines.append(f"  {url}")
    if summary:
        lines.append(f"  {summary}")
    return lines or [f"- {json.dumps(item, ensure_ascii=False)}"]


def _to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(line for item in content for line in _item_lines(item))
    return json.dumps(content, ensure_ascii=False, indent=2)


def _to_html(content: Any, title: str) -> str:
    text = _to_text(content)
    body: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if heading:
            level = min(len(heading.group(1)), 6)
            body.append(f"<h{level}>{escape_html(heading.group(2))}</h{level}>")
        elif stripped.startswith(("- ", "* ")):
            body.append(f"<p>{escape_html(stripped[2:])}</p>")
        else:
            body.append(f"<p>{escape_html(stripped)}</p>")
    safe_title = escape_html(title.strip() or "Digest")
    return (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"  <title>{safe_title}</title>\n"
        "</head>\n"
        "<body>\n"
        f"  <h1>{safe_title}</h1>\n"
        f"  {' '.join(body)}\n"
        "</body>\n"
        "</html>\n"
    )


def _load_reportlab() -> dict[str, Any] | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError:
        return None
    return {
        "A4": A4,
        "ParagraphStyle": ParagraphStyle,
        "mm": mm,
        "pdfmetrics": pdfmetrics,
        "TTFont": TTFont,
        "Paragraph": Paragraph,
        "SimpleDocTemplate": SimpleDocTemplate,
        "Spacer": Spacer,
    }


def _register_font(rl: dict[str, Any]) -> str | None:
    candidates = [os.environ.get("EXPORT_FONT_PATH", ""), *FONT_CANDIDATES]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            try:
                rl["pdfmetrics"].registerFont(rl["TTFont"]("ExportFont", candidate))
                return "ExportFont"
            except Exception:
                continue
    return None


def _render_pdf(text: str, title: str, path: Path, rl: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    font = _register_font(rl)
    if font is None:
        font = "Helvetica"
        if any(ord(char) > 255 for char in f"{title}{text}"):
            warnings.append(
                "No Unicode font found, Vietnamese characters may not render; "
                "set EXPORT_FONT_PATH to a .ttf font such as DejaVuSans."
            )

    style = rl["ParagraphStyle"]
    body = style("body", fontName=font, fontSize=10.5, leading=15, spaceAfter=3)
    h1 = style("h1", parent=body, fontSize=18, leading=22, spaceAfter=8)
    h2 = style("h2", parent=body, fontSize=13, leading=17, spaceBefore=6, spaceAfter=4)

    story: list[Any] = []
    if title.strip():
        story.append(rl["Paragraph"](escape(title.strip()), h1))
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            story.append(rl["Spacer"](1, 6))
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if heading:
            heading_style = h1 if len(heading.group(1)) == 1 else h2
            story.append(rl["Paragraph"](escape(heading.group(2)), heading_style))
        else:
            paragraph = re.sub(r"^[-*]\s+", "• ", stripped)
            story.append(rl["Paragraph"](escape(paragraph), body))

    margin = 20 * rl["mm"]
    document = rl["SimpleDocTemplate"](
        str(path),
        pagesize=rl["A4"],
        title=title.strip() or "Digest",
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin,
    )
    try:
        document.build(story)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return warnings


def export_file(
    content: Any = None,
    filename: Any = "digest",
    format: Any = "json",  # noqa: A002 - matches the tool argument name
    title: Any = "",
) -> dict[str, Any]:
    try:
        fmt = format.strip().lower() if isinstance(format, str) and format.strip() else "json"
        if fmt not in SUPPORTED_FORMATS:
            return _error(f"format must be one of: {', '.join(SUPPORTED_FORMATS)}, got {format!r}")
        if content is not None and not isinstance(content, (str, list, dict)):
            return _error(f"content must be a string, list or object, got {type(content).__name__}")
        if _is_empty(content):
            return _error("content is empty; nothing to export")
        if title is not None and not isinstance(title, str):
            return _error(f"title must be a string, got {type(title).__name__}")
        has_input_error, input_error = _input_error(content)
        if has_input_error:
            return _error(f"input contains error: {input_error}")

        rl = None
        if fmt == "pdf":
            rl = _load_reportlab()
            if rl is None:
                return _error("PDF export needs the 'reportlab' package (pip install reportlab); use format='json' instead")

        directory = Path(os.environ.get("EXPORT_DIR") or DEFAULT_EXPORT_DIR)
        directory.mkdir(parents=True, exist_ok=True)
        path = _unique_path(directory, _safe_filename(filename, fmt))

        warnings: list[str] = []
        if fmt == "json":
            path.write_text(_to_json_text(content), encoding="utf-8")
        elif fmt == "html":
            path.write_text(_to_html(content, title or ""), encoding="utf-8")
        else:
            warnings = _render_pdf(_to_text(content), title or "", path, rl)

        return {
            "tool": TOOL_NAME,
            "path": str(path),
            "filename": path.name,
            "format": fmt,
            "bytes": path.stat().st_size,
            "warnings": warnings,
        }
    except OSError as exc:
        return _error(f"could not write file: {type(exc).__name__}: {exc}")
    except Exception as exc:
        return _error(f"export_file failed: {type(exc).__name__}: {exc}")
