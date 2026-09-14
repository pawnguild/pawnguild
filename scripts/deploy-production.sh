#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# Existing infrastructure/data are prerequisites, never created or replaced here.
docker image inspect "${PAWNGUILD_IMAGE:-pawnguild_web}" >/dev/null
docker network inspect pawnguild_default shared_web_frontend >/dev/null
docker volume inspect pawnguild_postgres_data pawnguild_static_files pawnguild_media_files >/dev/null
if [ "$(docker inspect --format '{{.State.Running}}' postgres)" != true ]; then
    echo 'The existing database is not running; investigate without resetting it.' >&2
    exit 1
fi
docker-compose -p pawnguild -f docker-compose.prod.yml config --quiet
# Scope changes to the app; do not rebuild dependencies, stop the stack, or migrate.
docker-compose -p pawnguild -f docker-compose.prod.yml up -d --no-build --no-deps web
docker exec web python manage.py collectstatic --no-input
# Gunicorn is PID 1 under this production Compose file. Refresh workers for bind-mounted code.
docker kill --signal=HUP web >/dev/null
