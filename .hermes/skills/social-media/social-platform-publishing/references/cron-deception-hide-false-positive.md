# Cron Prompt-Injection Scanner False Positive: Deception Phrase

Context: A daily content-upload cron job can be blocked before execution when the assembled cron prompt includes attached skill text matching Hermes' cron prompt-injection scanner.

Observed pattern:

```py
(r'do\s+not\s+tell\s+the\s+user', "deception_hide")
```

Practical lesson for skills used by cron jobs:

- Avoid writing safety guidance using the literal phrase `do not tell the user ...`.
- Use transparent alternatives such as:
  - `Never claim ...`
  - `Do not claim ...`
  - `Report ... clearly`
  - `If blocked, say ...`
- This does **not** mean the publishing workflow is malicious; it is a defensive scanner catching a phrase commonly used in hidden/deceptive instructions.
- When a cron job fails with `deception_hide`, inspect both the job prompt and any attached skill markdown. The job prompt may be clean while a skill's pitfall wording trips the assembled-prompt scanner.
- After rephrasing, re-run the cron scanner or manually trigger the job before declaring it fixed.

Example fix:

```md
# Before
- Do not tell the user they are ready for TikTok upload when only `video.list` is available.

# After
- Never claim TikTok upload readiness when only `video.list` is available.
```
