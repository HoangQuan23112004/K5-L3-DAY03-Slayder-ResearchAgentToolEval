---
name: format
track: core
kind: local_formatter
requires_env: []
inputs: [items, template, headline]
outputs: [markdown, item_count]
side_effect: false
---
# format

Formats already-collected items into a markdown digest. It does not fetch data.
Use when the user requests presentation of existing items; do not invent sources
or use this tool to search or publish. Retrieve missing data first when requested.
Templates: `brief`, `sections` (group by `section`), `bullets`, `thread` (numbered),
and `daily_ai_vn`. Preserve actual titles, links, sources and summaries.
