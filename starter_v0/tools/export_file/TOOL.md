---
name: export_file
track: core
kind: output
requires_env: []
inputs: [content, filename, format, title]
outputs: [path, filename, format, bytes, warnings, error]
side_effect: true
---
# export_file

Writes already-collected content to a local file as PDF, HTML, or JSON. No API key
or network; this tool only writes locally. Use only when the user asks to save
or export content, and never use it to send or publish externally.

`EXPORT_DIR` optionally sets the output directory (default `exports/`).
`EXPORT_FONT_PATH` optionally points to a TrueType font for Vietnamese PDF
characters. PDF output requires the `reportlab` package.

Filenames are sanitized, forced to the selected extension, and never
overwritten; a numeric suffix is added when a file already exists. Empty
content, unsupported formats, and input errors return an error result.
JSON strings containing a list or object are stored as JSON; other strings
are stored as `{"content": "..."}`. PDF content is rendered as paragraphs,
with `#` / `##` headings and list items rendered as title, URL, and summary.
HTML content is escaped before it is embedded in a simple document, so input
markup is displayed as text rather than executed.
