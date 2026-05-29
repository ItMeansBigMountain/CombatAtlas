# OSRS RuneLite Plugins

This directory is a local parent folder for multiple independent RuneLite plugin repositories.

Each child directory is its own Git repo with a standard RuneLite/Gradle structure based on `breach-check-osrs`:

- `build.gradle`
- `settings.gradle`
- `gradlew` / `gradlew.bat`
- `gradle/wrapper/`
- `runelite-plugin.properties`
- `src/main/java/`
- `src/test/java/`
- `src/test/resources/logback-test.xml`

The parent HeRmEz workspace intentionally ignores plugin internals so each plugin can later be pushed to its own GitHub repository or moved under an organization.
