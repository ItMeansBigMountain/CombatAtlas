# OSRS Plugins Boilerplate

Java 11 helper-library boilerplate for OSRS/RuneLite projects. It packages raw JSON API helpers for:

- `TempleApiClient` (`https://templeosrs.com/api/v2`)
- `WOMApiClient` (`https://api.wiseoldman.net/v2`)

This repository is intentionally scoped as a reusable Java helper library. It is not a Vercel app, web UI, or deployable frontend, so browser/Vercel smoke tests do not apply. It does not include a RuneLite `Plugin`, `PluginDescriptor`, or plugin-hub metadata; add those in a child plugin repository when turning these helpers into a full RuneLite plugin.

## Prerequisites

- Java 11 or newer on `PATH`.
- `curl` or `wget`; `unzip` or `python3` for the lightweight Gradle launcher (`./gradlew`) to download and extract Gradle on first use.
- No API keys or secrets are required for the included calls.

## Build

```bash
chmod +x gradlew
./gradlew build
```

The build compiles `src/main/java`, compiles offline smoke tests in `src/test/java`, runs the `smokeTest` task, and packages a JAR.

Generated artifacts:

- Main JAR: `build/libs/osrs-plugins-boilerplate-0.1.0.jar`
- Sources JAR: `build/libs/osrs-plugins-boilerplate-0.1.0-sources.jar`

Inspect the compiled classes with:

```bash
jar tf build/libs/osrs-plugins-boilerplate-0.1.0.jar
```

## JavaDoc

Generated JavaDoc is committed under `docs/`.

Open locally:

```bash
xdg-open docs/index.html
```

Regenerate JavaDoc for the committed `/docs` output:

```bash
javadoc -d docs \
  -sourcepath src/main/java \
  -subpackages com.itmeansbigmountain.osrsapi \
  -windowtitle "osrs-plugins-boilerplate API" \
  -doctitle "osrs-plugins-boilerplate API"
```

You can also generate Gradle's standard build-local JavaDoc output with:

```bash
./gradlew javadoc
```

## External APIs

Package: `com.itmeansbigmountain.osrsapi`. These synchronous helpers make read-only `GET` requests and return raw response bodies. Merely adding the library sends nothing; a consumer must call a method.

### Wise Old Man (`https://api.wiseoldman.net/v2`)

| Route | Purpose |
| --- | --- |
| `/player/{username}` | Public player profile. |
| `/player/{username}/stats` | Skills/activities. |
| `/player/{username}/gains` | Gains. |
| `/player/{username}/achievements` | Achievements. |
| `/player/{username}/names` | Name history. |

### TempleOSRS (`https://templeosrs.com/api/v2`)

| Route | Purpose |
| --- | --- |
| `/player/{username}/info`, `/stats`, `/gains`, `/names` | Public player profile datasets. |
| `/current-top`, `/recent-records` | Current top snapshot and records. |
| `/skill-hiscores?skill={skill}` | Skill hiscores. |
| `/groups?name={groupid}`, `/groups/{groupid}/memberstats` | Group search and member stats. |
| `/pets/leaderboards` | Pet leaderboard. |
| `/player/{username}/collections` | Collection-log data. |

Requests use Java `HttpClient`, 10-second connection and 15-second request timeouts, and `User-Agent: OSRS-Plugin/1.0`. No API key, cookie, authorization header, analytics, telemetry, write operation, cache, retry, status validation, or offline fallback is included. Player/group/skill values are transmitted in URLs and are currently concatenated without URL encoding; consumers must validate/encode them. Calls must run off the RuneLite game thread.

## Quick usage

```java
import com.itmeansbigmountain.osrsapi.WOMApiClient;
import com.itmeansbigmountain.osrsapi.TempleApiClient;

public class ExampleLookup {
    public static void main(String[] args) throws Exception {
        String username = "Oyama";

        String womProfileJson = WOMApiClient.getPlayerInfo(username);
        String templeStatsJson = TempleApiClient.getPlayerStats(username);

        System.out.println(womProfileJson);
        System.out.println(templeStatsJson);
    }
}
```

RuneLite plugin pattern:

```java
@Singleton
public final class PlayerLookupService {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    public CompletableFuture<String> fetchWomProfile(String username) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                return WOMApiClient.getPlayerInfo(username);
            } catch (Exception e) {
                throw new CompletionException(e);
            }
        }, executor);
    }
}
```

Do not run these HTTP calls on the RuneLite game thread. Use a background executor, cache successful responses where possible, and surface API failures with user-friendly plugin messages.

## Consuming from another project

### Gradle project dependency

If this repository lives next to a consuming plugin during local development:

```groovy
// settings.gradle in the consuming plugin
includeBuild('../osrs-plugins-boilerplate')
```

```groovy
// build.gradle in the consuming plugin
dependencies {
    implementation 'com.itmeansbigmountain:osrs-plugins-boilerplate:0.1.0'
}
```

### Gradle source-set include

For quick copy/source consumption before publication:

```groovy
sourceSets {
    main {
        java {
            srcDir '../osrs-plugins-boilerplate/src/main/java'
        }
    }
}
```

### Gradle dependency snippet after Maven/JitPack publication

```groovy
repositories {
    mavenCentral()
    // maven { url = uri("https://jitpack.io") } // if published through JitPack
}

dependencies {
    implementation "com.itmeansbigmountain:osrs-plugins-boilerplate:0.1.0"
}
```

### Maven dependency snippet after publication

```xml
<dependency>
  <groupId>com.itmeansbigmountain</groupId>
  <artifactId>osrs-plugins-boilerplate</artifactId>
  <version>0.1.0</version>
</dependency>
```

## Integration checklist for plugin developers

1. Add the helper package as source or as a versioned dependency.
2. Keep API calls off the RuneLite game thread.
3. Sanitize or URL-encode usernames/group IDs before adding new methods that accept arbitrary input.
4. Parse raw JSON into plugin-owned DTOs; do not make UI code depend directly on raw strings.
5. Add short request timeouts and user-facing fallback messages for network failures.
6. Respect API rate limits and cache repeated lookups.
7. Use OSRS-only sources and URLs when linking docs or UI elements.

## CI

GitHub Actions runs `./gradlew build` on pushes and pull requests using Java 11. See `.github/workflows/build.yml`.

## Project status

This project is an active reusable helper-library candidate, not an archive-only snippet. If maintainers decide to keep it as archive material instead, update this README with the archival decision and point developers to the active RuneLite plugin repositories that consume these clients.
