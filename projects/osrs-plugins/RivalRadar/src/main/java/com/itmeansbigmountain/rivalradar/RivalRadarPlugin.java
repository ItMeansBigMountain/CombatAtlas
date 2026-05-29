package com.itmeansbigmountain.rivalradar;

import com.google.inject.Provides;
import com.itmeansbigmountain.osrsapi.WOMApiClient;
import com.itmeansbigmountain.osrsapi.TempleApiClient;
import lombok.extern.slf4j.Slf4j;
import net.runelite.api.*;
import net.runelite.api.events.*;
import net.runelite.client.Notifier;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.config.Config;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import net.runelite.client.ui.overlay.OverlayManager;
import net.runelite.client.ui.overlay.Overlay;

import javax.inject.Inject;
import java.time.Instant;
import java.time.Duration;
import java.util.*;
import java.io.IOException;

/**
 * Rival Radar - compares XP gains between players using WiseOldMan and TempleOSRS APIs.
 * Shows notifications when rivals gain significant XP.
 */
@Slf4j
@PluginDescriptor(
    name = "Rival Radar",
    description = "Compares XP gains with rival players using TWOM and TempleOSRS APIs",
    tags = {"xp", "rival", "comparison", "osrs"}
)
public class RivalRadarPlugin extends Plugin {

    @Inject private Client client;
    @Inject private RivalRadarConfig config;
    @Inject private OverlayManager overlayManager;
    @Inject private Notifier notifier;

    private Map<String, Double> rivalXPCache = new HashMap<>();
    private Instant lastRefresh = Instant.EPOCH;

    @Provides
    RivalRadarConfig provideConfig(ConfigManager configManager) {
        return configManager.getConfig(RivalRadarConfig.class);
    }

    @Override
    protected void startUp() throws Exception {
        log.info("Rival Radar starting up...");
        refreshRivals();
        if (config.showOverlay()) {
            overlayManager.add(new RivalRadarOverlay(this, config));
        }
    }

    @Override
    protected void shutDown() throws Exception {
        log.info("Rival Radar shutting down...");
        overlayManager.removeIf(RivalRadarOverlay.class::isInstance);
        rivalXPCache.clear();
    }

    @Subscribe
    public void onChatMessage(ChatMessage event) {
        if (event.getType() != ChatMessageType.GAMEMESSAGE) {
            return;
        }

        String msg = event.getMessage().replaceAll("<[^>]*>", "").toLowerCase();
        
        // Command to trigger manual rival comparison
        if (msg.startsWith("!rival ")) {
            String rivalName = msg.substring(7).trim();
            compareWithRival(rivalName);
        }
    }

    @Subscribe
    public void onGameTick(GameTick event) {
        // Auto-refresh rivals periodically
        if (Duration.between(lastRefresh, Instant.now()).getSeconds() >= config.refreshInterval()) {
            refreshRivals();
        }
    }

    /**
     * Refreshes XP data for all configured rivals.
     */
    private void refreshRivals() {
        String rivalNames = config.rivalNames();
        if (rivalNames == null || rivalNames.trim().isEmpty()) {
            return;
        }

        String[] names = rivalNames.split(",");
        for (String name : names) {
            name = name.trim();
            if (name.isEmpty()) continue;
            
            try {
                double xp = get7DayXP(name);
                rivalXPCache.put(name, xp);
            } catch (Exception e) {
                log.warn("Failed to get XP for rival {}: {}", name, e.getMessage());
            }
        }

        lastRefresh = Instant.now();
        log.info("Refreshed rivals: {}", rivalXPCache.keySet());
    }

    /**
     * Compares local player's XP with a specific rival.
     */
    private void compareWithRival(String rivalName) {
        try {
            // Get rival's 7-day XP
            double rivalXP = get7DayXP(rivalName);
            rivalXPCache.put(rivalName, rivalXP);

            // Get local player's 7-day XP
            String localName = client.getLocalPlayer().getName();
            double localXP = get7DayXP(localName);

            double difference = rivalXP - localXP;
            
            if (Math.abs(difference) > config.notificationThreshold()) {
                String direction = difference > 0 ? "ahead of you" : "behind you";
                String amount = String.format("%.0f", Math.abs(difference));
                notifier.notify(String.format("%s is %s XP %s!", rivalName, amount, direction));
            }

            // Refresh overlay if shown
            if (config.showOverlay()) {
                overlayManager.refresh();
            }

        } catch (Exception e) {
            log.error("Failed to compare with rival {}: {}", rivalName, e.getMessage());
            notifier.notify("Failed to get rival data: " + e.getMessage());
        }
    }

    /**
     * Gets the 7-day XP gain for a player from the combined TWOM and TempleOSRS APIs.
     */
    private double get7DayXP(String playerName) throws Exception {
        try {
            // Try WiseOldMan API first
            String womResponse = WOMApiClient.getPlayerGains(playerName);
            double womXP = parseXPFromResponse(womResponse);
            
            // Try TempleOSRS API as fallback
            double templeXP = 0;
            try {
                String templeResponse = TempleApiClient.getPlayerGains(playerName);
                templeXP = parseXPFromResponse(templeResponse);
            } catch (Exception e) {
                log.debug("TempleOSRS API failed for {}: {}", playerName, e.getMessage());
            }
            
            // Return average if both APIs succeeded, otherwise use the one that worked
            if (templeXP > 0) {
                return (womXP + templeXP) / 2.0;
            } else {
                return womXP;
            }
        } catch (Exception e) {
            log.error("Failed to get 7-day XP for {}: {}", playerName, e.getMessage());
            throw e;
        }
    }

    /**
     * Parses XP from API response (simplified - in production you'd want proper JSON parsing).
     */
    private double parseXPFromResponse(String response) {
        // This is a simplified parser - in a real implementation you'd use JSON parsing
        // For now, extract numbers from the response string
        try {
            // Look for patterns like "total_gained": 12345 or "xp": 12345
            java.util.regex.Pattern pattern = java.util.regex.Pattern.compile("(?:total_gained|xp)\\s*[:=]\\s*(\\d+)");
            java.util.regex.Matcher matcher = pattern.matcher(response);
            
            if (matcher.find()) {
                return Double.parseDouble(matcher.group(1));
            }
        } catch (Exception e) {
            log.debug("Failed to parse XP from response: {}", e.getMessage());
        }
        
        return 0;
    }

    // Accessors for overlay
    public Map<String, Double> getRivalXPCache() {
        return rivalXPCache;
    }

    public String getLocalPlayerName() {
        return client.getLocalPlayer() != null ? client.getLocalPlayer().getName() : "Unknown";
    }

    public double getLocalPlayerXP() {
        try {
            return get7DayXP(getLocalPlayerName());
        } catch (Exception e) {
            return 0;
        }
    }
}