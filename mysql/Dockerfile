FROM mysql:8.4

LABEL org.opencontainers.image.title="Hermes Calendar MySQL"
LABEL org.opencontainers.image.description="MySQL image for local Hermes Calendar development"

# utf8mb4 + UTC defaults aligned with the Hermes services.
COPY conf.d/ /etc/mysql/conf.d/

# Idempotent bootstrap scripts (run only on first container start, when the data volume is empty).
COPY init/ /docker-entrypoint-initdb.d/
