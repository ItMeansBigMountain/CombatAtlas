# RuneLite Side Panel UI Guidelines

Working notes for HeRmEz OSRS plugins after inspecting RuneLite client constants and Plugin Hub guidance.

## Authoritative panel dimensions

RuneLite `PluginPanel` in the current workspace client jar exposes these constants:

- `PluginPanel.PANEL_WIDTH = 225`
- `PluginPanel.SCROLLBAR_WIDTH = 17`
- `PluginPanel.BORDER_OFFSET = 6`

For scrollable side panels, design for a safe content width rather than the full 225 px. The current HeRmEz default is:

```text
safe content width = 225 - 17 - (6 * 2) - (4 * 2) = 188 px
```

Use a shared per-plugin dimensions helper when building custom Swing panels so labels, dropdowns, and action buttons do not accidentally expand wider than the sidebar.

## Layout rules for our OSRS plugins

- Fit inside the default RuneLite sidebar: no horizontal scrolling.
- Prefer `JScrollPane.HORIZONTAL_SCROLLBAR_NEVER` for side panels.
- Use `BorderLayout` rows with fixed compact action buttons on the east side.
- Keep action buttons about 24–26 px wide/tall.
- Keep top controls around 24 px tall.
- Put long copy inside HTML labels with an explicit body width equal to the safe content width.
- Use compact dropdowns instead of multiple wide toggles.
- Use icons/symbols for scan/activity state in the row; put verbose details behind click-to-detail.
- Start panels empty with real status messages; do not seed fake players or demo data.
- If a plugin contacts third-party services, Plugin Hub guidance requires a clear warning describing what data is sent.

## Current WhosGrindingPanel dimensions

`WhosGrindingPanelDimensions` is the working implementation pattern:

```text
CONTENT_WIDTH = 188
CONTROL_HEIGHT = 24
ROW_ACTION_WIDTH = 26
ROW_GAP = 3
ROW_HORIZONTAL_PADDING = 8
MEMBER_TEXT_WIDTH = 151
```

This leaves enough row width for a compact remove/action button while giving member names and source/activity text more space than the old 96 px label width.

## Checklist before shipping side-panel UI changes

1. Add or update a dimensions/unit test for the width budget.
2. Run `./gradlew test assemble --no-daemon --console=plain` with Java 11.
3. Confirm no `Clan`-only wording remains in user-facing text unless the plugin is truly clan-specific.
4. Confirm side panel starts empty and uses actual RuneLite data sources only.
5. Push the child plugin repo first; then update the HeRmEz parent submodule pointer.
