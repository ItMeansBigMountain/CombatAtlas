package com.itmeansbigmountain.icebarragetimer;

import com.google.inject.Provides;
import lombok.extern.slf4j.Slf4j;
import net.runelite.api.*;
import net.runelite.api.events.*;
import net.runelite.client.Notifier;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.events.ConfigChanged;
import net.runelite.client.eventbus.Subscribe;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import net.runelite.client.ui.overlay.OverlayManager;

import javax.inject.Inject;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;

@Slf4j
@PluginDescriptor(
        name = "Ice Barrage Timer",
        description = "Tracks Ice Barrage and Teleblock usage on players",
        tags = {"ice", "barrage", "teleblock", "pvp", "timer"}
)
public class IceBarrageTimerPlugin extends Plugin
{
    @Inject private Client client;
    @Inject private IceBarrageTimerConfig config;
    @Inject private OverlayManager overlayManager;
    @Inject private IceBarrageTimerOverlay overlay;
    @Inject private Notifier notifier;

    // Track when players were frozen
    private Map<String, Instant> frozenPlayers = new HashMap<>();
    private Map<String, Instant> teleblockedPlayers = new HashMap<>();
    
    @Provides
    IceBarrageTimerConfig provideConfig(ConfigManager configManager)
    {
        return configManager.getConfig(IceBarrageTimerConfig.class);
    }

    @Override
    protected void startUp()
    {
        if (config.showOverlay())
        {
            overlayManager.add(overlay);
        }
    }

    @Override
    protected void shutDown()
    {
        overlayManager.remove(overlay);
        frozenPlayers.clear();
        teleblockedPlayers.clear();
    }

    @Subscribe
    public void onConfigChanged(ConfigChanged event)
    {
        if (!event.getGroup().equals("icebarragetimer"))
            return;

        if (event.getKey().equals("showOverlay"))
        {
            if (config.showOverlay())
                overlayManager.add(overlay);
            else
                overlayManager.remove(overlay);
        }
    }

    @Subscribe
    public void onChatMessage(ChatMessage event)
    {
        if (event.getType() == ChatMessageType.GAMEMESSAGE)
        {
            String message = event.getMessage().replaceAll("<[^>]*>", "");
            
            // Check for Ice Barrage hit
            if (message.contains("Your Ice Barrage hits")) {
                String playerName = extractPlayerName(message);
                if (playerName != null) {
                    freezePlayer(playerName);
                }
            }
            
            // Check for Teleblock hit
            if (message.contains("Your Teleblock hits")) {
                String playerName = extractPlayerName(message);
                if (playerName != null) {
                    teleblockPlayer(playerName);
                }
            }
        }
    }

    @Subscribe
    public void onGameTick(GameTick tick)
    {
        // Clean up expired timers
        Instant now = Instant.now();
        
        frozenPlayers.entrySet().removeIf(entry -> {
            Duration elapsed = Duration.between(entry.getValue(), now);
            return elapsed.toSeconds() > config.barrageDuration();
        });
        
        teleblockedPlayers.entrySet().removeIf(entry -> {
            Duration elapsed = Duration.between(entry.getValue(), now);
            return elapsed.toSeconds() > config.teleblockDuration();
        });
    }

    private String extractPlayerName(String message)
    {
        // Extract player name from chat message
        // Format: "Your Ice Barrage hits [player] for [damage]"
        String[] parts = message.split(" ");
        for (int i = 0; i < parts.length; i++)
        {
            if (parts[i].equals("hits") && i + 1 < parts.length)
            {
                return parts[i + 1].replaceAll("[^a-zA-Z]", "");
            }
        }
        return null;
    }

    private void freezePlayer(String playerName)
    {
        frozenPlayers.put(playerName, Instant.now());
        if (config.enableNotification())
        {
            notifier.notify("Froze " + playerName + " for " + config.barrageDuration() + " seconds!");
        }
    }

    private void teleblockPlayer(String playerName)
    {
        teleblockedPlayers.put(playerName, Instant.now());
        if (config.enableNotification())
        {
            notifier.notify("Teleblocked " + playerName + " for " + config.teleblockDuration() + " seconds!");
        }
    }

    public Map<String, Instant> getFrozenPlayers()
    {
        return frozenPlayers;
    }

    public Map<String, Instant> getTeleblockedPlayers()
    {
        return teleblockedPlayers;
    }
}