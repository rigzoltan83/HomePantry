#!/bin/bash

set -euo pipefail

BACKUP_ROOT="/backup/homepantry"
SOURCE_DIR="/opt/homepantry"

TIMESTAMP="$(date '+%Y-%m-%d_%H-%M-%S')"
BACKUP_DIR="${BACKUP_ROOT}/${TIMESTAMP}"

DB_CONTAINER="family-db"
DB_NAME="homepantry"
DB_USER="homepantry_user"

LOG_FILE="${BACKUP_ROOT}/backup.log"


log()
{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" \
        >> "${LOG_FILE}"
}


cleanup_failed_backup()
{
    if [ -d "${BACKUP_DIR}" ]; then
        rm -rf "${BACKUP_DIR}"
    fi
}


mkdir -p "${BACKUP_ROOT}"

trap 'log "HIBA: a mentés megszakadt."; cleanup_failed_backup' ERR

mkdir -p "${BACKUP_DIR}"

log "HomePantry backup indul: ${TIMESTAMP}"


# PostgreSQL adatbázis

docker exec \
    "${DB_CONTAINER}" \
    pg_dump \
    -U "${DB_USER}" \
    -d "${DB_NAME}" \
    -Fc \
    > "${BACKUP_DIR}/homepantry.dump"


# Teljes alkalmazás, beleértve:
# - forráskód
# - .env
# - termékképek / feltöltött fájlok
# - migrations
# - Git repository
# - venv
#
# A futás közben változó / ideiglenes könyvtárakat kihagyjuk.

tar \
    --exclude='homepantry/.gunicorn' \
    --exclude='homepantry/.cache' \
    --exclude='homepantry/__pycache__' \
    --exclude='homepantry/app/__pycache__' \
    --exclude='homepantry/app/*/__pycache__' \
    -czf "${BACKUP_DIR}/homepantry-files.tar.gz" \
    -C /opt \
    homepantry


# Ellenőrizzük, hogy ténylegesen létrejöttek-e.

test -s "${BACKUP_DIR}/homepantry.dump"
test -s "${BACKUP_DIR}/homepantry-files.tar.gz"


# 3 napnál régebbi időbélyeges backup könyvtárak törlése.
# A backup.log megmarad.

find "${BACKUP_ROOT}" \
    -mindepth 1 \
    -maxdepth 1 \
    -type d \
    -mmin +4320 \
    -exec rm -rf {} \;


log "HomePantry backup sikeres: ${BACKUP_DIR}"

trap - ERR

exit 0
