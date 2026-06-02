
# Hermes CLI
export PATH="/opt/hermes/.venv/bin:/opt/data/.local/bin:$PATH"

# Java 11 for RuneLite plugins
export JAVA_HOME="/opt/data/jdks/current-java11"
export PATH="/opt/hermes/.venv/bin:/opt/data/.local/bin:/opt/data/jdks/current-java11/bin:$PATH"

# Correct container home for hermes user
export HOME="/opt/data"
