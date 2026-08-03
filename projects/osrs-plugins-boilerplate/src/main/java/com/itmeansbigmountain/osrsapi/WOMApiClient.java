package com.itmeansbigmountain.osrsapi;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

/**
 * Minimal Wise Old Man API helper for RuneLite and other OSRS Java projects.
 *
 * <p>The client intentionally returns raw JSON strings so plugin authors can choose their
 * own JSON library and data model. Every call uses a shared Java 11 {@link HttpClient}, a
 * 10 second connection timeout, a 15 second request timeout, and the default
 * {@code OSRS-Plugin/1.0} user agent.</p>
 */
public class WOMApiClient {
    static final String BASE_URL = "https://api.wiseoldman.net/v2";
    static final String USER_AGENT = "OSRS-Plugin/1.0";

    private static final HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(10))
        .build();

    static URI uri(String path) {
        return URI.create(BASE_URL + path);
    }

    private static String get(String path) throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(uri(path))
            .header("User-Agent", USER_AGENT)
            .timeout(Duration.ofSeconds(15))
            .GET()
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        return response.body();
    }

    /**
     * Fetches the Wise Old Man profile document for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerInfo(String username) throws Exception {
        return get("/player/" + username);
    }

    /**
     * Fetches skill and activity snapshots for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/stats}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerStats(String username) throws Exception {
        return get("/player/" + username + "/stats");
    }

    /**
     * Fetches Wise Old Man gains for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/gains}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerGains(String username) throws Exception {
        return get("/player/" + username + "/gains");
    }

    /**
     * Fetches recent Wise Old Man achievements for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/achievements}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerAchievements(String username) throws Exception {
        return get("/player/" + username + "/achievements");
    }

    /**
     * Fetches Wise Old Man name history for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/names}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerNames(String username) throws Exception {
        return get("/player/" + username + "/names");
    }
}
