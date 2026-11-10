---
name: clarify
track: core
kind: control
requires_env: []
inputs: [question, response_type, options]
outputs: [question, response_type, options, awaiting_user]
side_effect: false
---
# clarify

Returns a question to the user and pauses until the next user turn.
`response_type` is free text, yes/no, or a choice from `options`.

For a new publishing request, first use `yes_no` to confirm intent and destination.
If content is missing, collect it next using `text`, then confirm the final text
before sending. Confirmation of intent alone never authorizes sending unseen text.
For other missing details, such as an account or URL, use `text` immediately.
