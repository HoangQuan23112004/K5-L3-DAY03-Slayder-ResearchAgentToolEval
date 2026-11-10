"""Streamlit UI for the live Research Agent chat."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
PROMPT_PATH = ROOT / "artifacts" / "system_prompt.md"
TOOLS_PATH = ROOT / "artifacts" / "tools.yaml"
TRANSCRIPTS_DIR = ROOT / "transcripts"
HISTORY_WINDOW = 5
MAX_TOOL_ROUNDS = 4
VERSION = "v3"

st.set_page_config(page_title="Slayder · Research Agent", page_icon="✦", layout="wide")
load_lab_env(ROOT)

st.markdown(
    """
    <style>
      :root { color-scheme: light; }
      body, .stApp, [data-testid="stAppViewContainer"] { background: #fff !important; color: #1f1f1f !important; }
      [data-testid="stHeader"], [data-testid="stBottom"],
      [data-testid="stBottom"] > div { background: #fff !important; }
      .block-container { max-width: 860px; padding-top: 2.2rem; padding-bottom: 8rem; }
      [data-testid="stSidebar"] { background: #f0f4f9 !important; border-right: 0; color: #1f1f1f !important; }
      [data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }
      [data-testid="stSidebar"] label, [data-testid="stSidebar"] p,
      [data-testid="stSidebar"] span { color: #263238 !important; }
      .sidebar-brand { display: flex; align-items: center; gap: .7rem; margin-bottom: .4rem; }
      .brand-mark { color: #3971db; font-size: 1.6rem; line-height: 1; }
      .brand-name { color: #202124; font-size: 1rem; font-weight: 700; }
      .sidebar-note { color: #526174 !important; font-size: .86rem; margin: 0 0 1.3rem; }
      .welcome { padding: 5.2rem .3rem 1.5rem; }
      .welcome-kicker { font-size: 2.5rem; font-weight: 700; letter-spacing: -.045em;
                        background: linear-gradient(90deg, #4285f4, #9169cf 52%, #d96570);
                        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
      .welcome-title { margin: .1rem 0 0; color: #40444b; font-size: 2.5rem;
                       font-weight: 650; letter-spacing: -.045em; line-height: 1.25; }
      .welcome-copy { margin-top: 1rem; color: #596579 !important; font-size: 1rem; line-height: 1.6; }
      .chat-heading { color: #353a43; font-size: 1.35rem; font-weight: 650; margin: .25rem 0 1.6rem; }
      [data-testid="stButton"] button { min-height: 3.7rem; background: #f0f4f9 !important;
                                         border: 1px solid #e4e9f1 !important; border-radius: 17px;
                                         color: #27313f !important; font-weight: 600; box-shadow: none; }
      [data-testid="stButton"] button p { color: #27313f !important; }
      [data-testid="stButton"] button:hover { background: #e7eefb !important; border-color: #c9d8f5 !important; }
      [data-testid="stSidebar"] [data-testid="stButton"] button { min-height: 2.9rem;
                                                                     background: #e3eaf5 !important; border: 0 !important; }
      [data-testid="stChatMessage"] { background: transparent !important; border: 0;
                                       box-shadow: none; color: #202124 !important; margin-bottom: .75rem; }
      [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
          background: #f0f4f9 !important; border-radius: 22px; }
      [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li,
      [data-testid="stChatMessage"] strong, [data-testid="stChatMessage"] span {
          color: #202124 !important; }
      [data-testid="stChatMessage"] a { color: #175cd3 !important; }
      [data-testid="stChatInput"] { background: #fff !important; border: 1px solid #d9e1ec;
                                    border-radius: 24px; box-shadow: 0 3px 15px rgba(32, 50, 76, .08); }
      [data-testid="stChatInput"] textarea { color: #202124 !important; background: transparent !important; }
      [data-testid="stChatInput"] textarea::placeholder { color: #697586 !important; opacity: 1; }
      [data-testid="stChatInput"] button { color: #3068d6 !important; }
      [data-testid="stExpander"] { background: transparent !important; border-color: #e1e6ee !important; }
      [data-testid="stExpander"] p { color: #3d4654 !important; }
      @media (max-width: 640px) {
        .block-container { padding-top: 1.2rem; }
        .welcome { padding-top: 3rem; }
        .welcome-kicker, .welcome-title { font-size: 2rem; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def start_session(provider_name: str, model: str | None, version: str) -> None:
    artifact_version = build_artifact_version(version, PROMPT_PATH, TOOLS_PATH)
    selected_model = model or getattr(make_provider(provider_name), "default_model", None)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join((safe_slug(version), safe_slug(provider_name), timestamp))
    st.session_state.history = []
    st.session_state.turns = []
    st.session_state.transcript_path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": selected_model,
        "system_prompt": str(PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": HISTORY_WINDOW,
        "max_tool_rounds": MAX_TOOL_ROUNDS,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": st.session_state.turns,
    }
    st.session_state.config = (provider_name, model, version, artifact_version.artifact_version)


def show_turn(turn: dict[str, Any]) -> None:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        if turn["status"] == "provider_error":
            st.error(turn["error"])
        else:
            st.write(turn.get("assistant_text") or "Agent chưa trả lời.")
        if turn.get("tool_events"):
            with st.expander("Xem thao tác của agent"):
                for event in turn["tool_events"]:
                    st.write(f"**{event['tool']}**")
                    st.json({"args": event["args"], "result": event["result"]})


with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand"><div class="brand-mark">✦</div>'
        '<div class="brand-name">Slayder Research</div></div>'
        '<p class="sidebar-note">Trợ lý tìm kiếm và tổng hợp thông tin.</p>',
        unsafe_allow_html=True,
    )
    reset = st.button("＋  Cuộc trò chuyện mới", use_container_width=True)
    with st.expander("Cài đặt"):
        provider_name = st.selectbox("Nguồn AI", ("openrouter", "openai", "anthropic", "gemini", "ollama"))
        model = st.text_input("Model (để trống để dùng mặc định)").strip() or None

version = VERSION

current_artifact = build_artifact_version(version, PROMPT_PATH, TOOLS_PATH)
config = (provider_name, model, version, current_artifact.artifact_version)
if reset or st.session_state.get("config") != config:
    start_session(provider_name, model, version)

sample_prompt = None
if not st.session_state.turns:
    st.markdown(
        '<div class="welcome"><div class="welcome-kicker">Chào bạn, mình là Slayder</div>'
        '<div class="welcome-title">Hôm nay bạn muốn tìm hiểu điều gì?</div>'
        '<p class="welcome-copy">Tìm tin mới, đọc bài viết và khám phá các nghiên cứu cùng trợ lý của bạn.</p></div>',
        unsafe_allow_html=True,
    )
    suggestions = (
        ("📰  Tin AI hôm nay", "Tin tức AI hôm nay có gì nổi bật?"),
        ("📚  Paper về AI agent", "Tìm paper về đánh giá research agent trên arXiv."),
        ("🔗  Tóm tắt bài viết", "Tóm tắt bài viết này giúp mình."),
    )
    for column, (label, prompt) in zip(st.columns(3), suggestions):
        with column:
            if st.button(label, use_container_width=True):
                sample_prompt = prompt
else:
    st.markdown('<div class="chat-heading">Slayder</div>', unsafe_allow_html=True)

for turn in st.session_state.turns:
    show_turn(turn)

if user_text := st.chat_input("Bạn muốn tìm hiểu điều gì?") or sample_prompt:
    user_text = user_text.strip()
    if user_text:
        system_prompt = PROMPT_PATH.read_text(encoding="utf-8")
        tools = to_openai_tools(load_tool_declarations(TOOLS_PATH))
        messages = [
            {"role": "system", "content": system_prompt},
            *trim_history(st.session_state.history, HISTORY_WINDOW),
            {"role": "user", "content": user_text},
        ]
        turn: dict[str, Any] = {
            "turn_index": len(st.session_state.turns) + 1,
            "started_at": now_iso(),
            "user": user_text,
            "status": "started",
            "assistant_text": None,
            "rounds": [],
            "tool_events": [],
        }
        with st.spinner("Agent đang xử lý..."):
            try:
                result = run_model_tool_loop(
                    provider=make_provider(provider_name),
                    messages=messages,
                    tools=tools,
                    model=model,
                    max_tool_rounds=MAX_TOOL_ROUNDS,
                )
                turn.update(result)
                st.session_state.history.extend((
                    {"role": "user", "content": user_text},
                    {"role": "assistant", "content": result["assistant_text"]},
                ))
            except Exception as exc:
                turn.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
        turn["ended_at"] = now_iso()
        st.session_state.turns.append(turn)
        st.session_state.transcript["turns"] = list(st.session_state.turns)
        write_transcript(st.session_state.transcript_path, st.session_state.transcript)
        st.rerun()
