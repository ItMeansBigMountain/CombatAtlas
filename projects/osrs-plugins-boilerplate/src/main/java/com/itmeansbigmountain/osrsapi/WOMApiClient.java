package com.itmeansbigmountain.osrsapi;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class WOMApiClient {
    private static final String BASE_URL = "https://api.wiseoldman.net/v2";
    private static final HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(10))
        .build();

    public static String getPlayerInfo(String username) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/player/" + username))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getPlayerStats(String username) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/player/" + username + "/stats"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getPlayerGains(String username) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/player/" + username + "/gains"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getPlayerAchievements(String username) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/player/" + username + "/achievements"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getPlayerNames(String username) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/player/" + username + "/names"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }
}
