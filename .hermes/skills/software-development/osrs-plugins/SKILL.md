---
name: osrs-plugins
description: OSRS RuneLite plugin development guide covering project structure, API integration, and publishing workflow.
tags: [runescape, osrs, plugin-development, runelite]
---
# OSRS RuneLite Plugin Development Guide

## Project Structure

```
my-plugin/
├── src/main/java/com/example/myplugin/
│   ├── MyPluginPlugin.java        # Main plugin class
│   ├── MyPluginConfig.java        # Configuration interface
│   └── MyPluginOverlay.java       # Optional UI overlay
├── plugin.json                    # Plugin metadata descriptor
├── README.md                      # Documentation
└── build.gradle                   # Build configuration
```

## Plugin Development Patterns

### 1. Plugin Entry Point
```java
@Slf4j
@PluginDescriptor(
    name = "My Plugin",
    description = "Brief description of functionality",
    tags = {"tag1", "tag2"}
)
public class MyPluginPlugin extends Plugin {
    @Inject private Client client;
    @Inject private MyPluginConfig config;
    
    @Override
    protected void startUp() { /* initialization */ }
    @Override
    protected void shutDown() { /* cleanup */ }
}
```

### 2. Configuration Interface
```java
@ConfigGroup("myplugin")
public interface MyPluginConfig extends Config {
    @ConfigItem("showOverlay", "Show Overlay")
    @Slider(base = 1, max = 10, step = 1, raw = false)
    default int showOverlay() { return 5; }
}
```

### 3. Event Handling
```java
@Subscribe
public void onChatMessage(ChatMessage event) {
    // Handle chat events
}

@Subscribe
public void onGameTick(GameTick event) {
    // Handle periodic game events
}
```

## API Integration

### Shared Clients
- **WOMApiClient**: Accesses WiseOldMan API for player data and competition tracking
- **TempleApiClient**: Accesses TempleOSRS API for boss kill counts and competition data

### Example API Usage
```java
// Get player XP from WiseOldMan
String response = WOMApiClient.getPlayerGains(playerName);
double xp = parseXPFromResponse(response);

// Parse numeric values from API response
private static final Pattern XP_PATTERN = Pattern.compile("(?:total_gained|xp)\\s*[:=]\\s*(\\d+)", Pattern.CASE_INSENSITIVE);
private double parseXPFromResponse(String response) {
    Matcher m = XP_PATTERN.matcher(response);
    if (m.find()) {
        try {
            return Double.parseDouble(m.group(1));
        } catch (NumberFormatException ignored) {}
    }
    return 0;
}

// Combine data from both APIs for robust results
double combinedXP = (womXP + templeXP) / 2.0;
```

## Publishing Workflow

1. **Fork** the `runelite/plugin-hub` repository
2. **Create** a new plugin directory under `plugins/`
3. **Add** required files: `src/`, `plugin.json`, `README.md`, `build.gradle`
4. **Verify** build with `./gradlew assemble`
5. **Submit** a Pull Request with:
   - Clear description of functionality
   - Screenshots or GIFs demonstrating features
   - Explanation of API usage (if applicable)
6. **Address** any feedback from maintainers

## Best Practices

- **Performance**: Minimize game thread blocking; use background executors for API calls
- **Memory Management**: Clear caches and resources during `shutdown()`
- **User Experience**: Provide meaningful notifications and visual feedback
- **Error Handling**: Gracefully handle API failures with user-friendly messages
- **Versioning**: Follow semantic versioning and update `plugin.json` accordingly
- **Documentation**: Keep README updated with usage examples and configuration options
- **Testing**: Implement verification scripts to validate API integrations

## Common Issues & Troubleshooting

- **API Rate Limits**: Implement caching strategies and respect API usage policies
- **Network Failures**: Use fallback mechanisms and provide user feedback
- **Plugin Conflicts**: Ensure proper dependency isolation and version checking
- **Build Failures**: Verify Gradle configuration and dependency versions
- **Runtime Errors**: Check plugin logs and use `notifier.notify()` for user feedback

## Resources

- [RuneLite Client API Documentation](https://github.com/runelite/client)
- [WiseOldMan API Documentation](https://oldschool.runescape.wiki/w/Wise_Old_Man_API)
- [TempleOSRS API Documentation](https://oldschool.runescape.wiki/w/TempleOSRS_API)
- [RuneLite Plugin Hub](https://github.com/runelite/plugin-hub)