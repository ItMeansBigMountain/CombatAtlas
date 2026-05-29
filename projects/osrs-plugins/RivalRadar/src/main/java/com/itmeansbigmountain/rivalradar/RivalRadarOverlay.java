package com.itmeansbigmountain.rivalradar;

import net.runelite.api.Client;
import net.runelite.client.ui.overlay.Overlay;
import net.runelite.client.ui.overlay.OverlayLayer;
import net.runelite.client.ui.overlay.OverlayPosition;
import net.runelite.client.ui.overlay.components.LineComponent;
import net.runelite.client.ui.overlay.components.TitleComponent;
import net.runelite.client.ui.overlay.components.Component;
import net.runelite.client.plugins.Plugin;
import lombok.extern.slf4j.Slf4j;
import javax.inject.Inject;
import java.awt.Dimension;
import java.awt.Color;
import java.util.Map;

@Slf4j
public class RivalRadarOverlay extends Overlay
{
    private final RivalRadarPlugin plugin;
    private final RivalRadarConfig config;
    private final PanelComponent panelComponent = new PanelComponent();

    @Inject
    public RivalRadarOverlay(RivalRadarPlugin plugin, RivalRadarConfig config)
    {
        this.plugin = plugin;
        this.config = config;
        setPosition(OverlayPosition.TOP_LEFT);
        setLayer(OverlayLayer.ABOVE_WIDGETS);
        setPriority(Overlay.PRIORITY_LOW);
    }

    @Override
    public Dimension render(Graphics2D graphics)
    {
        panelComponent.getChildren().clear();

        // Header
        panelComponent.getChildren().add(TitleComponent.builder()
                .text("Rival Radar")
                .color(Color.CYAN)
                .build());

        // Local player info
        String local = plugin.getLocalPlayerName();
        double localXP = plugin.getLocalPlayerXP();
        panelComponent.getChildren().add(LineComponent.builder()
                .left("You")
                .right(String.format("%.0f XP", localXP))
                .style(Color.WHITE)
                .build());

        // Rival entries
        for (Map.Entry<String, Double> entry : plugin.getRivalXPCache().entrySet())
        {
            String name = entry.getKey();
            double xp = entry.getValue();
            double diff = xp - plugin.getLocalPlayerXP();
            String diffStr = String.format("%+.0f", diff);
            Color color = diff >= 0 ? Color.GREEN : Color.RED;

            panelComponent.getChildren().add(LineComponent.builder()
                    .left(name)
                    .right(diffStr + " XP")
                    .style(color)
                    .build());
        }

        return panelComponent.render(graphics);
    }
}