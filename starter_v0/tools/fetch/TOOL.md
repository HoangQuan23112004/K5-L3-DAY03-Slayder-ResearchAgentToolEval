---
name: fetch
track: core
kind: live_api
provider: Firecrawl
requires_env: [FIRECRAWL_API_KEY]
inputs: [url]
outputs: [items]
side_effect: false
---
# fetch

Reads the content of a single URL via Firecrawl.
Use an existing full http/https URL supplied by the user or earlier retrieval.
For topic search use `lookup`; for arXiv PDF extraction use `paper_text`.
If the article URL is missing, use `clarify(text)` rather than inventing a URL.
