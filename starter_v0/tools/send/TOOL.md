---
name: send
track: bonus
kind: action
provider: Telegram Bot API
requires_env: [TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]
inputs: [text, confirmed]
outputs: [status]
side_effect: true
requires_confirmation: true
---
# send

Posts text to a Telegram channel. The message is only sent when `confirmed` is true.
The model must obtain explicit confirmation of the final content and destination
before setting `confirmed=true`. The initial request or an intent-only confirmation
does not qualify. Use `clarify(response_type="yes_no")` for confirmation and never
invent missing content. This tool is not a way to reply in chat.
