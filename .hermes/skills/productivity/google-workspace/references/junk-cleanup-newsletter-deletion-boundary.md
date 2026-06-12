# Junk cleanup approval + newsletter deletion boundary

Session update: the user approved cleanup of known junk/spam emails without requiring a per-item review each time. This changes the previous default for junk only; it does **not** make all Gmail deletion broadly approved.

## Apply this boundary

Allowed without per-item review when sender/category is clearly known junk/spam or marketing from the user's approved junk list:
- Trash/delete obvious promo/junk messages.
- Keep conservative guards for login/security/password/verification/receipt/charge/billing terms.
- Report concise counts and examples afterward.

Still require care/verification:
- Newsletter/source emails (TLDR, Daily Stoic, Kino Body, Grammarly Insights): summarize or use as content first. If creating YouTube videos, trash only after upload returns a verified YouTube `video_id`.
- Priority/admin/security/billing/finance/calendar/Drive actions still require explicit approval unless the user gave an exact scoped instruction.

## Verification pattern

After Gmail trash/delete actions, re-fetch the message metadata and confirm `labelIds` contains `TRASH` before reporting the item as cleaned up.
