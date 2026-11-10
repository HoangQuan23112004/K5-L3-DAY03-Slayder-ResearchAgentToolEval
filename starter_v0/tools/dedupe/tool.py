from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TOOL_NAME = "dedupe"
DEFAULT_THRESHOLD = 0.8
TRACKING_PARAMS = frozenset({"fbclid", "gclid", "ref", "ref_src", "igshid", "mc_cid", "mc_eid"})
TRACKING_PREFIXES = ("utm_",)


def _error(message: str) -> dict[str, Any]:
    return {"tool": TOOL_NAME, "error": message}


def normalize_url(url: Any) -> str:
    """Return a canonical URL, or an empty string for missing or non-string input."""
    if not isinstance(url, str) or not url.strip():
        return ""
    raw = url.strip()
    try:
        parts = urlsplit(raw)
        query = sorted(
            (key, value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if key.lower() not in TRACKING_PARAMS
            and not key.lower().startswith(TRACKING_PREFIXES)
        )
        host = parts.netloc.lower().removeprefix("www.")
        return urlunsplit((
            parts.scheme.lower(),
            host,
            parts.path.rstrip("/"),
            urlencode(query),
            "",
        ))
    except ValueError:
        return raw.lower().rstrip("/")


def _item_tokens(item: dict[str, Any]) -> set[str]:
    title = item.get("title")
    body = item.get("text") or item.get("content") or item.get("summary")
    text = " ".join(value for value in (title, body) if isinstance(value, str))
    return set(re.findall(r"\w+", text.lower()))


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if left and right else 0.0


def _parse_threshold(value: Any) -> float:
    if value is None:
        return DEFAULT_THRESHOLD
    if isinstance(value, bool):
        raise ValueError(f"threshold must be a number between 0 and 1, got {value!r}")
    try:
        threshold = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"threshold must be a number between 0 and 1, got {value!r}") from None
    if not 0.0 <= threshold <= 1.0:
        raise ValueError(f"threshold must be between 0 and 1, got {value!r}")
    return threshold


def _error_result(item: dict[str, Any]) -> dict[str, Any]:
    result = dict(item)
    result["tool"] = TOOL_NAME
    result.pop("items", None)
    return result


def dedupe_items(items: Any = None, threshold: Any = DEFAULT_THRESHOLD) -> dict[str, Any]:
    try:
        if isinstance(items, dict) and "error" in items:
            return _error_result(items)
        if items is None:
            items = []
        if not isinstance(items, list):
            return _error(f"items must be a list of objects, got {type(items).__name__}")

        try:
            limit = _parse_threshold(threshold)
        except ValueError as exc:
            return _error(str(exc))

        kept: list[dict[str, Any]] = []
        kept_tokens: list[set[str]] = []
        seen_urls: dict[str, int] = {}
        removed: list[dict[str, Any]] = []
        skipped_invalid = 0

        for item in items:
            if not isinstance(item, dict):
                skipped_invalid += 1
                continue
            if "error" in item:
                return _error_result(item)

            url = normalize_url(item.get("url"))
            tokens = _item_tokens(item)
            duplicate_of: int | None = seen_urls.get(url) if url else None
            reason = "same_url"

            if duplicate_of is None:
                for index, other_tokens in enumerate(kept_tokens):
                    if _jaccard(tokens, other_tokens) >= limit:
                        duplicate_of, reason = index, "similar_text"
                        break

            if duplicate_of is None:
                kept.append(item)
                kept_tokens.append(tokens)
                if url:
                    seen_urls[url] = len(kept) - 1
            else:
                removed.append({
                    "item": item,
                    "duplicate_of": duplicate_of,
                    "reason": reason,
                })

        return {
            "tool": TOOL_NAME,
            "items": kept,
            "removed_count": len(removed),
            "removed": removed,
            "skipped_invalid": skipped_invalid,
        }
    except Exception as exc:
        return _error(f"dedupe failed: {type(exc).__name__}: {exc}")
