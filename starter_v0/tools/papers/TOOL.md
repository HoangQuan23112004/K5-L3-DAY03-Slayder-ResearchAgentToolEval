---
name: papers
track: bonus
kind: live_api
provider: arXiv API
requires_env: [ARXIV_USER_AGENT]
inputs: [query, max_results, sort_by]
outputs: [items, total_results]
side_effect: false
---
# papers

Searches arXiv via the official Atom API. Rate-limited (waits ~3s between
in-process requests).
Use for topic-based scientific paper discovery; results contain metadata and
abstracts, not extracted full text. Use `paper_text` for an identified arXiv paper's
PDF content and `lookup` for web news. Sort by `relevance`, `submittedDate` for
new submissions, or `lastUpdatedDate` for recently updated papers.
