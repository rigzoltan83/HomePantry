#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="/opt/homepantry"
COMPOSE_FILE="$PROJECT_DIR/deploy/libretranslate-compose.yml"

echo "=== HomePantry LibreTranslate setup ==="

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: Docker is not installed."
    exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
    echo "ERROR: Docker Compose plugin is not available."
    exit 1
fi

TOTAL_MEM_KB="$(
    awk '/MemTotal/ {print $2}' /proc/meminfo
)"

SWAP_TOTAL_KB="$(
    awk '/SwapTotal/ {print $2}' /proc/meminfo
)"

if (
    ( TOTAL_MEM_KB < 4194304 )
    && ( SWAP_TOTAL_KB < 1048576 )
); then
    echo
    echo "WARNING:"
    echo "Less than 4 GB RAM and less than 1 GB swap detected."
    echo "LibreTranslate may need additional swap space."
    echo
fi

echo
echo "Starting LibreTranslate..."

docker compose \
    -f "$COMPOSE_FILE" \
    up -d

echo
echo "Waiting for LibreTranslate..."

for attempt in $(seq 1 60); do
    if curl -fsS \
        http://127.0.0.1:5000/languages \
        >/dev/null 2>&1
    then
        echo
        echo "LibreTranslate is ready."
        exit 0
    fi

    sleep 2
done

echo
echo "ERROR: LibreTranslate did not become ready in time."
echo
echo "Check logs with:"
echo
echo "docker compose -f $COMPOSE_FILE logs --tail=100"
exit 1
