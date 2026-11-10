"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_dedupe_removes_tracking_url_and_similar_content_duplicates() -> None:
    result = TOOL_FUNCTIONS["dedupe"](items=[
        {
            "title": "AI research update",
            "summary": "Researchers released a new AI research update today.",
            "url": "https://www.example.com/news?utm_source=feed&id=1",
        },
        {
            "title": "AI research update",
            "summary": "Researchers released a new AI research update today.",
            "url": "https://example.com/news?id=1&fbclid=tracking",
        },
        {
            "title": "AI research update",
            "summary": "Researchers released a new AI research update today!",
            "url": "https://other.example/story",
        },
    ])

    assert result["removed_count"] == 2
    assert len(result["items"]) == 1
    assert result["skipped_invalid"] == 0
    assert result["removed"][0]["reason"] == "same_url"
    assert result["removed"][1]["reason"] == "similar_text"
    assert all(item["duplicate_of"] == 0 for item in result["removed"])


def test_dedupe_invalid_items_returns_error_dict() -> None:
    result = TOOL_FUNCTIONS["dedupe"](items="not a list")

    assert result["tool"] == "dedupe"
    assert "items must be a list" in result["error"]
    assert "items" not in result

    bad_threshold = TOOL_FUNCTIONS["dedupe"](items=[], threshold=1.1)
    assert bad_threshold["tool"] == "dedupe"
    assert "threshold" in bad_threshold["error"]

def test_dedupe_failure_returns_error_dict(monkeypatch) -> None:
    from tools.dedupe import tool as dedupe_tool

    def fail(_item):
        raise RuntimeError("tokenizer failed")

    monkeypatch.setattr(dedupe_tool, "_item_tokens", fail)
    result = TOOL_FUNCTIONS["dedupe"](items=[{"title": "AI news"}])

    assert result["tool"] == "dedupe"
    assert "RuntimeError" in result["error"]
    assert "tokenizer failed" in result["error"]


def test_sentiment_scores_english_and_vietnamese_items() -> None:
    result = TOOL_FUNCTIONS["sentiment"](items=[
        {"title": "Great release", "text": "Users love the new app, really fast and helpful"},
        {"title": "Sản phẩm tuyệt vời", "text": "Giao diện đẹp và mượt"},
        {"title": "Meeting notes", "text": "The meeting is at noon"},
        {"title": "Terrible outage", "text": "The service crashed and users are angry"},
    ])

    assert "error" not in result
    assert [item["sentiment"]["label"] for item in result["items"]] == [
        "positive", "positive", "neutral", "negative",
    ]
    assert result["overall"]["counts"] == {
        "positive": 2, "neutral": 1, "negative": 1,
    }
    assert result["skipped_invalid"] == 0


def test_sentiment_invalid_input_returns_error_dict() -> None:
    result = TOOL_FUNCTIONS["sentiment"](items="not an item list")

    assert result["tool"] == "sentiment"
    assert "items must be a list" in result["error"]
    assert "overall" not in result


def test_sentiment_failure_returns_error_dict(monkeypatch) -> None:
    from tools.sentiment import tool as sentiment_tool

    def fail(*_args, **_kwargs):
        raise RuntimeError("sentiment scorer failed")

    monkeypatch.setattr(sentiment_tool, "_score_text", fail)
    result = TOOL_FUNCTIONS["sentiment"](text="This is great")

    assert result["tool"] == "sentiment"
    assert "RuntimeError" in result["error"]
    assert "sentiment scorer failed" in result["error"]


def test_export_file_writes_json_without_overwriting(monkeypatch, tmp_path) -> None:
    import json

    monkeypatch.setenv("EXPORT_DIR", str(tmp_path))

    first = TOOL_FUNCTIONS["export_file"](
        content='[{"title": "AI update"}]',
        filename="../../digest.pdf",
        format="json",
    )
    second = TOOL_FUNCTIONS["export_file"](
        content='[{"title": "AI update"}]',
        filename="../../digest.pdf",
        format="json",
    )
    pdf = TOOL_FUNCTIONS["export_file"](
        content="# AI update\nA useful summary.",
        filename="digest",
        format="pdf",
        title="Research digest",
    )
    html = TOOL_FUNCTIONS["export_file"](
        content="# AI update\n<script>alert('unsafe')</script>",
        filename="digest",
        format="html",
        title="Research digest",
    )

    assert first["filename"] == "digest.json"
    assert second["filename"] == "digest_1.json"
    assert first["format"] == "json"
    assert first["bytes"] > 0
    assert first["warnings"] == []
    assert json.loads((tmp_path / first["filename"]).read_text(encoding="utf-8")) == [
        {"title": "AI update"},
    ]
    assert pdf["format"] == "pdf"
    assert pdf["filename"] == "digest.pdf"
    assert (tmp_path / pdf["filename"]).read_bytes().startswith(b"%PDF")
    assert html["format"] == "html"
    assert html["filename"] == "digest.html"
    html_text = (tmp_path / html["filename"]).read_text(encoding="utf-8")
    assert "<h1>Research digest</h1>" in html_text
    assert "&lt;script&gt;" in html_text
    assert "<script>" not in html_text


def test_export_file_rejects_bad_format_and_empty_content() -> None:
    bad_format = TOOL_FUNCTIONS["export_file"](content="some content", format="docx")
    empty_content = TOOL_FUNCTIONS["export_file"](content="  ")

    assert "format must be one of" in bad_format["error"]
    assert "content is empty" in empty_content["error"]


def test_export_file_write_failure_returns_error_dict(monkeypatch, tmp_path) -> None:
    from tools.export_file import tool as export_tool

    monkeypatch.setenv("EXPORT_DIR", str(tmp_path))

    def fail(_directory, _filename):
        raise OSError("disk unavailable")

    monkeypatch.setattr(export_tool, "_unique_path", fail)
    result = TOOL_FUNCTIONS["export_file"](content='{"ready": true}', format="json")

    assert result["tool"] == "export_file"
    assert "could not write file" in result["error"]
    assert "disk unavailable" in result["error"]
