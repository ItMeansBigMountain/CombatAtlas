package com.itmeansbigmountain.rivalradar;

import net.runelite.client.config.Config;
import net.runelite.client.config.ConfigGroup;
import net.runelite.client.config.ConfigItem;

@ConfigGroup("rivalradar")
@Config(
    name = "Rival Radar",
    description = "Compares XP gains with rival players"
)
public interface RivalRadarConfig {
    @ConfigItem(
        keyName = "rivalNames",
        name = "Rival Names",
        description = "Comma-separated list of rival player names to track"
    )
    String rivalNames();

    @ConfigItem(
        keyName = "refreshInterval",
        name = "Refresh Interval (seconds)",
        description = "How often to auto-refresh rival XP data"
    )
    default int refreshInterval() {
        return 300; // 5 minutes
    }

    @ConfigItem(
        keyName = "notificationThreshold",
        name = "Notification Threshold",
        description = "XP difference threshold for notifications"
    )
    default double notificationThreshold() {
        return 100000.0; // 100k XP
    }

    @ConfigItem(
        keyName = "showOverlay",
        name = "Show Overlay",
        description = "Display the XP comparison overlay"
    )
    default boolean showOverlay() {
        return true;
    }
}