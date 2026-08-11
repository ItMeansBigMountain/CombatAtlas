# Git-Only Authentication Optimization

When the `gh` CLI is unavailable, prioritize Git-only authentication with these adjustments:

1. **Quick validation** – check for `~/.git-credentials`; if present, skip `gh` setup.
2. **Credential helper preference** – favor `credential.helper store` over `cache` when the token must persist.
3. **Manual identity note** – Git-only workflows require explicit `user.name` and `user.email` configuration.

*Add this section to the `github-auth` skill’s README to guide users in environments without `gh`.*