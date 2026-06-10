package com.itmeansbigmountain.osrsapi;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.net.URI;
import java.util.Arrays;
import java.util.Set;
import java.util.stream.Collectors;

/** Offline smoke tests run by Gradle's smokeTest task. */
public final class ApiClientSmokeTest {
    private ApiClientSmokeTest() {
    }

    public static void main(String[] args) {
        assertEquals(
            URI.create("https://api.wiseoldman.net/v2/player/Oyama/stats"),
            WOMApiClient.uri("/player/Oyama/stats"),
            "Wise Old Man URI construction"
        );
        assertEquals(
            URI.create("https://templeosrs.com/api/v2/player/Oyama/info"),
            TempleApiClient.uri("/player/Oyama/info"),
            "TempleOSRS URI construction"
        );
        assertEquals("OSRS-Plugin/1.0", WOMApiClient.USER_AGENT, "Wise Old Man user agent");
        assertEquals("OSRS-Plugin/1.0", TempleApiClient.USER_AGENT, "TempleOSRS user agent");

        assertPublicMethods(WOMApiClient.class,
            "getPlayerInfo", "getPlayerStats", "getPlayerGains", "getPlayerAchievements", "getPlayerNames");
        assertPublicMethods(TempleApiClient.class,
            "getPlayerInfo", "getPlayerStats", "getPlayerGains", "getPlayerNames", "getPlayerCurrentTop",
            "getRecentRecords", "getSkillHiscores", "getGroupInfo", "getGroupMemberStats", "getPetLeaderboard",
            "getCollectionLog");
    }

    private static void assertPublicMethods(Class<?> type, String... expectedMethods) {
        Set<String> publicMethods = Arrays.stream(type.getDeclaredMethods())
            .filter(method -> Modifier.isPublic(method.getModifiers()))
            .map(Method::getName)
            .collect(Collectors.toSet());
        for (String expectedMethod : expectedMethods) {
            if (!publicMethods.contains(expectedMethod)) {
                throw new AssertionError(type.getSimpleName() + " missing public method " + expectedMethod);
            }
        }
    }

    private static void assertEquals(Object expected, Object actual, String label) {
        if (!expected.equals(actual)) {
            throw new AssertionError(label + " expected <" + expected + "> but was <" + actual + ">");
        }
    }
}
