package com.itmeansbigmountain.osrsapi;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

/**
 * Minimal TempleOSRS API helper for RuneLite and other OSRS Java projects.
 *
 * <p>The client intentionally returns raw JSON strings so plugin authors can choose their
 * own JSON library and data model. Every call uses a shared Java 11 {@link HttpClient}, a
 * 10 second connection timeout, a 15 second request timeout, and the default
 * {@code OSRS-Plugin/1.0} user agent.</p>
 */
public class TempleApiClient {
    static final String BASE_URL = "https://templeosrs.com/api/v2";
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
     * Fetches TempleOSRS profile information for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/info}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerInfo(String username) throws Exception {
        return get("/player/" + username + "/info");
    }

    /**
     * Fetches TempleOSRS stats for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/stats}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerStats(String username) throws Exception {
        return get("/player/" + username + "/stats");
    }

    /**
     * Fetches TempleOSRS gains for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/gains}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerGains(String username) throws Exception {
        return get("/player/" + username + "/gains");
    }

    /**
     * Fetches TempleOSRS name history for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/names}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerNames(String username) throws Exception {
        return get("/player/" + username + "/names");
    }

    /**
     * Fetches the current TempleOSRS top player leaderboard snapshot.
     *
     * @return raw JSON response body from {@code /current-top}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPlayerCurrentTop() throws Exception {
        return get("/current-top");
    }

    /**
     * Fetches recent TempleOSRS records.
     *
     * @return raw JSON response body from {@code /recent-records}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getRecentRecords() throws Exception {
        return get("/recent-records");
    }

    /**
     * Fetches TempleOSRS hiscores for a skill.
     *
     * @param skill TempleOSRS skill key, for example {@code attack}, {@code mining}, or {@code overall}
     * @return raw JSON response body from {@code /skill-hiscores?skill={skill}}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getSkillHiscores(String skill) throws Exception {
        return get("/skill-hiscores?skill=" + skill);
    }

    /**
     * Searches TempleOSRS groups by name.
     *
     * @param groupid group name/search value passed to the current helper implementation
     * @return raw JSON response body from {@code /groups?name={groupid}}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getGroupInfo(String groupid) throws Exception {
        return get("/groups?name=" + groupid);
    }

    /**
     * Fetches member stats for a TempleOSRS group.
     *
     * @param groupid TempleOSRS group identifier
     * @return raw JSON response body from {@code /groups/{groupid}/memberstats}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getGroupMemberStats(String groupid) throws Exception {
        return get("/groups/" + groupid + "/memberstats");
    }

    /**
     * Fetches TempleOSRS pet leaderboard data.
     *
     * @return raw JSON response body from {@code /pets/leaderboards}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getPetLeaderboard() throws Exception {
        return get("/pets/leaderboards");
    }

    /**
     * Fetches TempleOSRS collection log data for an OSRS player.
     *
     * @param username current or recent in-game username
     * @return raw JSON response body from {@code /player/{username}/collections}
     * @throws Exception if the request URI is invalid or the HTTP call fails
     */
    public static String getCollectionLog(String username) throws Exception {
        return get("/player/" + username + "/collections");
    }
}
