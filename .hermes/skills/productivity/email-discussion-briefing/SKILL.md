---
name: email-discussion-briefing
description: Read the user's current Gmail profiles read-only, summarize what matters, and prepare discussion topics without deleting or modifying email.
version: 1.0.0
created_by: agent
---

# Email Discussion Briefing

Use this skill when the user asks to read through email, discuss current email, summarize inbox state, identify important messages, or decide what to do with emails.

## Scope and safety

- Default to read-only Gmail access.
- Do not trash, archive, label, unsubscribe, report spam, send replies, or modify messages unless the user explicitly approves the exact action and scope.
- Exception only if a separate established pipeline rule applies, such as newsletter source emails being trashed after verified YouTube upload.
- Never expose OAuth tokens, auth URLs, recovery codes, passwords, or credential filenames that reveal secrets.
- For `personal-main / affan.fareed@gmail.com`, respect Gmail read-only policy.

## User's known Gmail profiles

Use these profile tokens under `/opt/data/google_profiles/<profile>/google_token.json` when present:

- `personal-main` → `affan.fareed@gmail.com`, primary personal, Gmail read-only.
- `personal-secondary` → `fareed320@gmail.com`, newsletter/source account.
- `trapiistan` → `trapiistan@gmail.com`, Trapiistan/Sosai automation account.
- `classicalechos` → `classicalechos@gmail.com`, Classical Echos channel/account.
- `burner` → `laflametoast@gmail.com`, temporary/burner.
- `hermes-agent` → automation-linked communications; token may need repair if refresh fails.

## Read-only audit workflow

1. Load `google-workspace` first.
2. Read profile inventory from `/opt/data/google_profiles` and ignore old backup profiles unless needed.
3. For each active profile, verify Gmail identity with `users.getProfile`.
4. Count true Inbox using `messages.list(labelIds=['INBOX'])` paging; do not use broad `messagesTotal` as Inbox count.
5. Pull unread and recent Inbox samples with metadata/snippets first:
   - `is:unread newer_than:30d`
   - `newer_than:7d`
   - Apply `labelIds=['INBOX']` where possible.
6. Classify messages into:
   - urgent/action-needed,
   - money/account/security,
   - work/business/vendor,
   - content/newsletter source,
   - shopping/subscriptions,
   - junk/low-priority,
   - needs user review.
7. Only fetch full bodies for messages that need deeper discussion or where snippets are insufficient.
8. Write a local non-secret audit JSON under `/opt/data/HeRmEz/projects/_ops/` when useful.
9. Report concise account-by-account bullets in Discord, not big tables.

## Discussion style

- Start with what requires the user's attention.
- Separate actual account/security/money emails from newsletters.
- For newsletters, suggest possible video/topic use only; do not delete unless a verified upload happened or user approves.
- For suspected junk, say why it looks low-priority and ask before cleanup unless user has explicitly pre-approved that exact junk scope.
- Offer next actions: reply draft, calendar task, cleanup proposal, video topic, or ignore.
- When the user agrees to a proposed newsletter/video cleanup path, follow `references/email-discussion-to-newsletter-pipeline-handoff.md`: upload first, verify YouTube IDs, keep source cleanup bounded to newsletter pipeline rules, and report read-only Gmail cleanup failures separately from successful uploads.

## Verification checklist

- [ ] Gmail profiles checked live.
- [ ] Inbox counts are true INBOX counts.
- [ ] Important messages surfaced first.
- [ ] No destructive action taken without approval.
- [ ] Any auth failures reported with profile name only, no secrets.
