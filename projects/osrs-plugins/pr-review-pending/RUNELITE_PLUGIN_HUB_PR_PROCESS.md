# RuneLite Plugin Hub PR process

Source references checked:

- RuneLite Plugin Hub repository README: https://github.com/runelite/plugin-hub
- RuneLite Developer Guide: https://github.com/runelite/runelite/wiki/Developer-Guide

## When a plugin belongs in `pr-review-pending/`

Move a plugin here only after local development is considered complete: code is committed, pushed, tests/build pass, README/properties are ready, and the next remaining work is official RuneLite Plugin Hub submission/review.

## Required plugin repository state

RuneLite's Plugin Hub flow expects the plugin itself to live in a public GitHub repository generated from, or compatible with, the example plugin layout.

Before submission, verify the plugin repo has:

1. Public GitHub repository.
2. Java 11-compatible build.
3. `runelite-plugin.properties` filled out, especially:
   - `displayName`
   - `author`
   - `description`
   - `tags`
   - `plugins=<fully.qualified.PluginClass>`
   - optional `version=`
   - `build=standard`
4. Useful `README.md` describing the plugin and any third-party data/API usage.
5. Optional `icon.png` at repository root, max 48x72 px.
6. Clean commit pushed to the plugin repo.
7. Full 40-character commit hash for the submitted version.

## Official Plugin Hub PR steps

1. Fork/clone `runelite/plugin-hub`.
2. Add one manifest file under `plugins/`.
3. The manifest file contains:

```properties
repository=https://github.com/<owner>/<plugin-repo>.git
commit=<40-character commit hash>
```

4. Run the Plugin Hub repository checks/tooling if available locally.
5. Commit the manifest file on a branch.
6. Open a PR against `runelite/plugin-hub`.
7. Watch CI/reviewer feedback and update the plugin repo commit + manifest commit as requested.
8. After the PR is approved/merged and the plugin is available/shareable through the official Plugin Hub, move the plugin folder from `pr-review-pending/` to `completed/` and update `.gitmodules`.

## Notes for Who's Grinding Panel

The plugin uses Wise Old Man and official OSRS hiscores for selected-player grinding summaries. The README/properties should be explicit that player names may be sent to third-party services when a user expands/fetches a player card. Avoid polling every visible player; keep click-to-fetch, caching, and explicit refresh behavior.
