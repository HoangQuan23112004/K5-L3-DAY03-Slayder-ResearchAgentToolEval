---
name: dedupe
track: core
kind: transform
requires_env: []
inputs: [items, threshold]
outputs: [items, removed_count, removed, skipped_invalid, error]
side_effect: false
---
# dedupe

Removes duplicate items from `lookup` / `social_search` results. Keeps the
first occurrence and drops later ones. No API key, no network, no side effect.

Two items are duplicates when either:
1. their URLs are equal after normalization (lowercase host, `www.` and
   trailing `/` removed, fragment and tracking params such as `utm_*`,
   `fbclid`, `gclid` dropped, query params sorted), or
2. the Jaccard similarity of their word sets (`title` + `text`/`content`/
   `summary`) is >= `threshold`.

## Output

Success:

    {"tool": "dedupe", "items": [...], "removed_count": 2,
     "removed": [{"item": {...}, "duplicate_of": 0, "reason": "same_url"}],
     "skipped_invalid": 0}

`duplicate_of` is the index in the returned `items` list. `reason` is
`same_url` or `similar_text`. Entries in `items` that are not dicts are
skipped and counted in `skipped_invalid`.

Failure (never raises):

    {"tool": "dedupe", "error": "items must be a list of objects, got str"}

## Notes
- `items` empty or None returns an empty result, not an error.
- `threshold` accepts a number or numeric string in [0, 1]; anything else is
  an error.
- Pairwise comparison is O(n^2); fine for the few hundred items a digest has.
