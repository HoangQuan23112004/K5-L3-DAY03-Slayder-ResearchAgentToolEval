---
name: social_search
track: core
kind: live_api
provider: RapidAPI Twitter API45
requires_env: [RAPIDAPI_KEY, RAPIDAPI_TWITTER_HOST]
inputs: [query, search_type, limit]
outputs: [items]
side_effect: false
---
# social_search

Searches posts by keyword. `search_type` orders results (`Latest` or `Top`).
Use `Latest` for recent posts and `Top` for popular posts. For posts by one known
account, use `timeline`. If the latest user intent cancels Twitter or switches to
web, stop calling this tool; retain the topic for `lookup` instead. Call both only
when both sources remain requested.
