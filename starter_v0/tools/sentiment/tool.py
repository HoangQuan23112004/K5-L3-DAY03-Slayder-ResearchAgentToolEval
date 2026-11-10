from __future__ import annotations

import math
import re
from typing import Any


TOOL_NAME = "sentiment"
POS_THRESHOLD = 0.15
MAX_VALENCE = 5.0

LEXICON: dict[str, float] = {
    "good": 1.9, "great": 3.1, "excellent": 3.2, "amazing": 3.0, "awesome": 3.1,
    "love": 3.0, "best": 3.2, "nice": 1.8, "happy": 2.7, "win": 2.8,
    "growth": 1.5, "improve": 1.8, "success": 2.7, "helpful": 1.9, "fast": 1.3,
    "bad": -2.5, "terrible": -3.4, "awful": -3.3, "worst": -3.1, "hate": -2.7,
    "bug": -1.8, "fail": -2.5, "crash": -2.6, "slow": -1.5, "scam": -3.2,
    "loss": -2.0, "risk": -1.2, "broken": -2.2, "disappointing": -2.5, "angry": -2.3,
    "tốt": 2.0, "hay": 1.8, "tuyệt": 3.0, "tuyệt vời": 3.2, "xuất sắc": 3.2,
    "thích": 2.0, "yêu": 2.8, "mượt": 1.8, "nhanh": 1.3, "ổn": 1.2, "đẹp": 2.0,
    "hữu ích": 2.0, "thành công": 2.7, "tăng trưởng": 1.5, "vui": 2.3,
    "tệ": -2.5, "dở": -2.3, "kém": -2.0, "chán": -2.0, "lỗi": -1.8,
    "chậm": -1.5, "lừa đảo": -3.2, "thất vọng": -2.8, "tức": -2.0, "giận": -2.3,
    "thua lỗ": -2.5, "rủi ro": -1.2, "hỏng": -2.2, "khủng khiếp": -3.2,
}
NEGATIONS = {
    "not", "no", "never", "don't", "doesn't", "didn't", "isn't", "wasn't",
    "can't", "won't", "without", "không", "chẳng", "chưa", "đâu", "hề",
}
BOOSTERS = {
    "very": 1.3, "really": 1.3, "extremely": 1.5, "so": 1.2, "super": 1.4,
    "rất": 1.3, "quá": 1.3, "cực": 1.5, "siêu": 1.4,
    "slightly": 0.7, "somewhat": 0.8, "hơi": 0.7, "khá": 0.85,
}
EMOJI = {
    "👍": 1.5, "❤": 2.0, "😍": 2.5, "🔥": 1.5, "😂": 1.0,
    "👎": -1.5, "😡": -2.5, "😢": -1.5, "💩": -2.0,
}


def _error(message: str) -> dict[str, Any]:
    return {"tool": TOOL_NAME, "error": message}


def _error_result(item: dict[str, Any]) -> dict[str, Any]:
    result = dict(item)
    result["tool"] = TOOL_NAME
    result.pop("items", None)
    return result


def _label(score: float) -> str:
    if score >= POS_THRESHOLD:
        return "positive"
    if score <= -POS_THRESHOLD:
        return "negative"
    return "neutral"


def _body(item: dict[str, Any]) -> str:
    title = item.get("title")
    main = item.get("content") or item.get("text") or item.get("summary")
    return " ".join(part for part in (title, main) if isinstance(part, str))


def _score_text(text: str, lexicon: dict[str, float]) -> float:
    tokens = re.findall(r"[\w']+", text.lower())
    total = sum(value * text.count(emoji) for emoji, value in EMOJI.items())
    index = 0
    while index < len(tokens):
        step, value = 1, None
        if index + 1 < len(tokens):
            bigram = f"{tokens[index]} {tokens[index + 1]}"
            if bigram in lexicon:
                value, step = lexicon[bigram], 2
        if value is None:
            value = lexicon.get(tokens[index])
        if value is not None:
            if any(token in NEGATIONS for token in tokens[max(0, index - 3):index]):
                value *= -0.74
            before = tokens[index - 1] if index > 0 else ""
            after = tokens[index + step] if index + step < len(tokens) else ""
            value *= BOOSTERS.get(before, 1.0) * BOOSTERS.get(after, 1.0)
            total += value
        index += step
    return total / math.sqrt(total * total + 15)


def _parse_lexicon_extra(value: Any) -> dict[str, float]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(
            f"lexicon_extra must be an object {{word: valence}}, got {type(value).__name__}"
        )
    parsed: dict[str, float] = {}
    for word, valence in value.items():
        if not isinstance(word, str) or not word.strip():
            raise ValueError(f"lexicon_extra keys must be non-empty strings, got {word!r}")
        if isinstance(valence, bool) or not isinstance(valence, (int, float)):
            raise ValueError(f"lexicon_extra[{word!r}] must be a number, got {valence!r}")
        if not math.isfinite(valence) or abs(valence) > MAX_VALENCE:
            raise ValueError(
                f"lexicon_extra[{word!r}] must be within [-{MAX_VALENCE:g}, {MAX_VALENCE:g}], got {valence!r}"
            )
        parsed[word.strip().lower()] = float(valence)
    return parsed


def analyze_sentiment(
    items: Any = None,
    text: Any = None,
    lexicon_extra: Any = None,
) -> dict[str, Any]:
    try:
        if text is not None and not isinstance(text, str):
            return _error(f"text must be a string, got {type(text).__name__}")
        if items is not None and not isinstance(items, list):
            return _error(f"items must be a list of objects, got {type(items).__name__}")
        try:
            lexicon = {**LEXICON, **_parse_lexicon_extra(lexicon_extra)}
        except ValueError as exc:
            return _error(str(exc))

        if items:
            output: list[dict[str, Any]] = []
            counts = {"positive": 0, "neutral": 0, "negative": 0}
            skipped_invalid = 0
            for item in items:
                if not isinstance(item, dict):
                    skipped_invalid += 1
                    continue
                if "error" in item:
                    return _error_result(item)
                score = round(_score_text(_body(item), lexicon), 4)
                label = _label(score)
                counts[label] += 1
                output.append({**item, "sentiment": {"score": score, "label": label}})
            if not output:
                return _error("items contains no valid objects")
            mean = round(sum(item["sentiment"]["score"] for item in output) / len(output), 4)
            return {
                "tool": TOOL_NAME,
                "items": output,
                "overall": {"score": mean, "label": _label(mean), "counts": counts},
                "skipped_invalid": skipped_invalid,
            }

        if text and text.strip():
            score = round(_score_text(text, lexicon), 4)
            return {
                "tool": TOOL_NAME,
                "items": [],
                "overall": {"score": score, "label": _label(score)},
                "skipped_invalid": 0,
            }
        return _error("provide non-empty text or items")
    except Exception as exc:
        return _error(f"sentiment failed: {type(exc).__name__}: {exc}")
