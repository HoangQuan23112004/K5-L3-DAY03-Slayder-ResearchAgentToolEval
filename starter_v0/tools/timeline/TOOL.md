---
name: timeline
track: core
kind: live_api
provider: RapidAPI Twitter API45
requires_env: [RAPIDAPI_KEY, RAPIDAPI_TWITTER_HOST]
inputs: [screenname, limit]
outputs: [items]
side_effect: false
---
# timeline

Fetches recent posts from a single account. `screenname` is an account handle
without `@`.
Use for posts BY an identified account; use `social_search` for posts ABOUT a topic
and `lookup` for web news. Strip a supplied `@`; map a known name only when certain
(Sam Altman = `sama`). Ask `clarify(text)` if the account is unspecified or ambiguous.
