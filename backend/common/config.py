import os

# Prometheus
PROMETHEUS_ENABLED = os.getenv("PROMETHEUS_ENABLED", True)
PROMETHEUS_PORT = os.getenv("PROMETHEUS_PORT", 8126)

# Logging config
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")