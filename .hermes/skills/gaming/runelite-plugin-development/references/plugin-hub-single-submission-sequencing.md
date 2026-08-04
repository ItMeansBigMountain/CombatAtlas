# Plugin Hub single-submission sequencing

Use this when several RuneLite plugins are ready but Plugin Hub permits only one active submission for the author.

## Separate the two constraints

1. **One plugin per PR:** inspect the live PR file list. A correct Plugin Hub PR normally changes exactly one marker such as `plugins/<plugin-id>`.
2. **One open PR per author:** this is a queue/concurrency rule. Two separate one-marker PRs can each be structurally correct while still violating the open-PR limit.

Do not tell the user a PR contains two plugins unless the live changed-file list proves it. Read issue comments, reviews, inline comments, PR state, and files before acting.

## Priority and closure sequence

When the user explicitly prioritizes plugin A over plugin B:

1. Verify A’s child commit, prior technical feedback, branch existence, and marker diff.
2. Add a concise comment to B explaining it is being closed temporarily under the one-open-PR rule.
3. Close B.
4. Attempt to reopen A only if preserving its review history is useful.
5. If GitHub returns HTTP 422 or the maintainer requested a fresh submission, create a replacement branch from current upstream `master`; do not combine plugins.
6. Add exactly one marker and cite the earlier PR plus resolved feedback in the replacement body.
7. Verify the live PR file list is exactly `[plugins/<plugin-id>]`.
8. Reintroduce B as its own PR only after A is merged/closed.

Preserve an existing PR’s queue position by default, but explicit user priority overrides that default. Do not argue for preserving the lower-priority PR after the user has chosen the order.

## Immutable child SHA update loop

For any child change after submission, including README-only documentation:

1. Inspect source and make the child change.
2. Run appropriate validation; documentation-only changes still need `git diff --check`, while code changes need the Java 11 clean build.
3. Commit and push the child first.
4. Update only `commit=<full-child-sha>` in the Plugin Hub marker branch.
5. Commit and push the marker update.
6. Read back the live PR files and marker content; confirm no second plugin entered the PR.
7. Recheck the official Plugin Hub build and every feedback surface.

## Documenting network/API usage

When asked what APIs a plugin contacts, inspect actual HTTP clients, URL constants, request builders, and browser-open links. Distinguish:

- external API endpoints actually called;
- public web pages merely opened on click;
- local RuneLite Client API integrations that are not network requests;
- build dependencies that are not contacted services.

README documentation should state endpoint families, purpose, HTTP behavior, fallback behavior, and whether the plugin has a custom backend, authentication/API keys, uploads, or telemetry. Never infer “no telemetry” from dependencies alone—search the source.
