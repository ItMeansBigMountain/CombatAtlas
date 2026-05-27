package com.itmeansbigmountain.osrsapi;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class TempleApiClient {
    private static final String BASE_URL = "https://templeosrs.com/api/v2";
    private static final HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(10))
        .build();

    public static String getPlayerInfo(String username) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/player/" + username + "/info"))
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

    public static String getPlayerCurrentTop() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/current-top"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getRecentRecords() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/recent-records"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getSkillHiscores(String skill) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/skill-hiscores?skill=" + skill))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getGroupInfo(String groupid) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/groups?name=" + groupid))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getGroupMemberStats(String groupid) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/groups/" + groupid + "/memberstats"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getPetLeaderboard() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/pets/leaderboards"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    public static String getCollectionLog(String username) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(java.net.URI.create(BASE_URL + "/player/" + username + "/collections"))
            .header("User-Agent", "OSRS-Plugin/1.0")
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }
}
