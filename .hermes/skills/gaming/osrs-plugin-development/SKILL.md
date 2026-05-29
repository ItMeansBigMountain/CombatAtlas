---
name: osrs-plugin-development
category: gaming
description: Develop Runelite plugins for Old School RuneScape using the DMM Timer as boilerplate template
tags: [osrs, runelite, pvp, java]
version: 1.0.0
author: hermes-agent
dependencies: [brew install tree, sdk install java 11.0.22-zulu]
---

# OSRS Plugin Development

## Trigger
When developing Runelite plugins for Old School RuneScape, especially PvP utility plugins like ice barrage timers, spell trackers, or combat overlays.

## Plugin Structure
All OSRS plugins follow the Runelite plugin descriptor pattern:
```java
@PluginDescriptor(
    name = "Plugin Name",
    description = "Plugin description",
    tags = {"tag1", "tag2", "pvp"}
)
public class PluginNamePlugin extends Plugin
{
    @Inject private Client client;
    @Inject private ConfigManager configManager;
    @Inject private PluginNameConfig config;
    @Inject private OverlayManager overlayManager;
}
```

## Core Components
1. **Main Plugin Class** - `@PluginDescriptor`, event handlers
2. **Config Class** - Annotation-based configuration
3. **Overlay Class** - Visual representation
4. **Utility Classes** - API clients, data models

## Event Handling Patterns
- `@Subscribe public void onChatMessage(ChatMessage event)` - Detect combat hits, spell casts
- `@Subscribe public void onGameTick(GameTick tick)` - Timer updates, periodic checks
- `@Subscribe public void onConfigChanged(ConfigChanged event)` - Config updates

## Starter Template
Use `osrs-plugins-boilerplate` directory or copy `DeadmanBreachPlugin.java` as starting point.

## References
- `references/api-patterns.md` - TempleOSRS and WiseOldMan API endpoint patterns
- `references/combat-message-formats.md` - Common OSRS chat message formats for spells
- `templates/IceBarrageTimerPlugin.java` - Timer plugin boilerplate