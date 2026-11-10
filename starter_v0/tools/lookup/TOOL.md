---
name: lookup
track: core
kind: live_api
provider: Tavily
requires_env: [TAVILY_API_KEY]
inputs: [query, topic, timeframe, max_results]
outputs: [items]
side_effect: false
---
# lookup

Searches the web via Tavily. Has a `topic` (`general` or `news`) and a
`timeframe` argument.
Use `topic="news"` for news requests. Map today to `day`, this week to `week`,
this month to `month`, and this year to `year`. Keep the subject in `query` and
use the dedicated arguments for filters. When the user switches from Twitter to
web, retain the subject and applicable filters but do not also call `social_search`.
For reading a specific URL, use `fetch`.
