---
name: sentiment
track: core
kind: transform
requires_env: []
inputs: [items, text, lexicon_extra]
outputs: [items, overall, skipped_invalid, error]
side_effect: false
---
# sentiment

Lexicon-based sentiment for English and Vietnamese, with negation,
intensifiers and a few emoji. No API key, network, or side effect. Results are
indicative and do not reliably capture sarcasm or domain context.

Each item receives `sentiment: {"score": ..., "label": ...}`. Labels are
`positive` at scores >= 0.15, `negative` at scores <= -0.15, and `neutral`
otherwise. Item text is its `title` plus the first available of `content`,
`text`, or `summary`.

When both non-empty `items` and `text` are provided, items take precedence.
`lexicon_extra` adds words with valences in [-5, 5]. Non-object items are
skipped and counted; errors in retrieved items are passed through.
