#!/usr/bin/env bash

set -euo pipefail


APP_NAME="${HOMEPANTRY_APP_NAME:-homepantry}"
APP_USER="${HOMEPANTRY_APP_USER:-homepantry}"
APP_GROUP="${HOMEPANTRY_APP_GROUP:-homepantry}"

APP_DIR="${HOMEPANTRY_APP_DIR:-/opt/homepantry}"
VENV_DIR="${HOMEPANTRY_VENV_DIR:-${APP_DIR}/venv}"

ENV_DIR="${HOMEPANTRY_ENV_DIR:-/etc/homepantry}"
ENV_FILE="${HOMEPANTRY_ENV_FILE:-${ENV_DIR}/homepantry.env}"

SERVICE_NAME="${HOMEPANTRY_SERVICE_NAME:-homepantry.service}"
SERVICE_SOURCE="${HOMEPANTRY_SERVICE_SOURCE:-${APP_DIR}/deploy/homepantry.service}"
SERVICE_TARGET="${HOMEPANTRY_SERVICE_TARGET:-/etc/systemd/system/${SERVICE_NAME}}"

DB_NAME="${HOMEPANTRY_DB_NAME:-homepantry}"
DB_USER="${HOMEPANTRY_DB_USER:-homepantry_user}"
DB_PORT="${HOMEPANTRY_DB_PORT:-}"

PORT="${HOMEPANTRY_PORT:-8084}"


log()
{
    echo
    echo "==> $*"
}


fail()
{
    echo
    echo "ERROR: $*" >&2
    exit 1
}


require_root()
{
    if [ "${EUID}" -ne 0 ]; then
        fail "Run this installer as root or with sudo."
    fi
}


generate_secret()
{
    python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
}


generate_db_password()
{
    python3 - <<'PY'
import secrets
print(secrets.token_hex(32))
PY
}


install_packages()
{
    log "Installing system packages"

    apt-get update

    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y \
        python3 \
        python3-venv \
        python3-pip \
        python3-dev \
        build-essential \
        libpq-dev \
        postgresql \
        postgresql-contrib \
        curl
}


create_service_user()
{
    log "Creating application user"

    if ! getent group "${APP_GROUP}" >/dev/null; then
        groupadd --system "${APP_GROUP}"
    fi

    if ! id "${APP_USER}" >/dev/null 2>&1; then
        useradd \
            --system \
            --gid "${APP_GROUP}" \
            --home-dir "${APP_DIR}" \
            --shell /usr/sbin/nologin \
            "${APP_USER}"
    fi
}


check_application_directory()
{
    log "Checking application directory"

    if [ ! -d "${APP_DIR}" ]; then
        fail "${APP_DIR} does not exist."
    fi

    if [ ! -f "${APP_DIR}/requirements.txt" ]; then
        fail "requirements.txt not found."
    fi

    if [ ! -f "${APP_DIR}/wsgi.py" ]; then
        fail "wsgi.py not found."
    fi

    if [ ! -f "${SERVICE_SOURCE}" ]; then
        fail "Systemd service template not found."
    fi
}


setup_postgresql()
{
    log "Preparing PostgreSQL"

    systemctl enable --now postgresql


    if [ -z "${DB_PORT}" ]; then
        DB_PORT="$(
            sudo -u postgres \
                psql -Atqc "SHOW port"
        )"
    fi

    if [ -z "${DB_PORT}" ]; then
        fail "Could not determine PostgreSQL port."
    fi

    echo "Using PostgreSQL port ${DB_PORT}."

    DB_PASSWORD=""

    if [ -f "${ENV_FILE}" ]; then
        echo "Existing HomePantry environment found."

        if ! sudo -u postgres \
            psql -p "${DB_PORT}" -tAc \
            "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" \
            | grep -q 1
        then
            fail "Database role ${DB_USER} is missing while ${ENV_FILE} already exists."
        fi
    else
        DB_PASSWORD="$(generate_db_password)"

        if sudo -u postgres \
            psql -p "${DB_PORT}" -tAc \
            "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" \
            | grep -q 1
        then
            echo "Database role ${DB_USER} already exists."
            echo "Setting a new password for the fresh HomePantry configuration."

            sudo -u postgres \
                psql -p "${DB_PORT}" \
                --set=ON_ERROR_STOP=1 \
                --command="
                    ALTER ROLE ${DB_USER}
                    PASSWORD '${DB_PASSWORD}';
                "
        else
            sudo -u postgres \
                psql -p "${DB_PORT}" \
                --set=ON_ERROR_STOP=1 \
                --command="
                    CREATE ROLE ${DB_USER}
                    LOGIN
                    PASSWORD '${DB_PASSWORD}';
                "
        fi
    fi

    if sudo -u postgres \
        psql -p "${DB_PORT}" -tAc \
        "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" \
        | grep -q 1
    then
        echo "Database ${DB_NAME} already exists."
    else
        sudo -u postgres \
            createdb -p "${DB_PORT}" \
            --owner="${DB_USER}" \
            "${DB_NAME}"
    fi
}

prepare_environment()
{
    log "Preparing environment configuration"

    install \
        -d \
        -o root \
        -g "${APP_GROUP}" \
        -m 0750 \
        "${ENV_DIR}"

    if [ -f "${ENV_FILE}" ]; then
        echo "${ENV_FILE} already exists."
        echo "Keeping existing configuration."

        DB_PASSWORD=""
        return
    fi

    SECRET_KEY="$(generate_secret)"

    cat > "${ENV_FILE}" <<EOF
FLASK_ENV=production
SECRET_KEY=${SECRET_KEY}

DATABASE_URL=postgresql+psycopg://${DB_USER}:${DB_PASSWORD}@127.0.0.1:${DB_PORT}/${DB_NAME}

APPLICATION_PREFIX=
DEFAULT_TIMEZONE=Europe/Budapest

RECIPE_TRANSLATION_API_URL=http://127.0.0.1:5000
EOF

    chown root:"${APP_GROUP}" "${ENV_FILE}"
    chmod 0640 "${ENV_FILE}"
}


prepare_directories()
{
    log "Preparing application directories"

    install \
        -d \
        -o "${APP_USER}" \
        -g "${APP_GROUP}" \
        -m 0755 \
        "${APP_DIR}/var"

    install \
        -d \
        -o "${APP_USER}" \
        -g "${APP_GROUP}" \
        -m 0755 \
        "${APP_DIR}/var/uploads"

    install \
        -d \
        -o "${APP_USER}" \
        -g "${APP_GROUP}" \
        -m 0755 \
        "${APP_DIR}/var/uploads/products"

    install \
        -d \
        -o "${APP_USER}" \
        -g "${APP_GROUP}" \
        -m 0755 \
        "${APP_DIR}/var/uploads/recipes"

    install \
        -d \
        -o "${APP_USER}" \
        -g "${APP_GROUP}" \
        -m 0755 \
        "${APP_DIR}/var/uploads/storage-locations"
}


create_virtualenv()
{
    log "Preparing Python virtual environment"

    if [ ! -x "${VENV_DIR}/bin/python" ]; then
        python3 -m venv "${VENV_DIR}"
    fi

    "${VENV_DIR}/bin/pip" install --upgrade pip

    "${VENV_DIR}/bin/pip" install \
        -r "${APP_DIR}/requirements.txt"
}


run_migrations()
{
    log "Running database migrations"

    set -a
    # shellcheck disable=SC1090
    source "${ENV_FILE}"
    set +a

    cd "${APP_DIR}"

    sudo -u "${APP_USER}" \
        --preserve-env=DATABASE_URL,SECRET_KEY,APPLICATION_PREFIX,DEFAULT_TIMEZONE,RECIPE_TRANSLATION_API_URL \
        env FLASK_SKIP_DOTENV=1 \
        "${VENV_DIR}/bin/flask" db upgrade
}


seed_reference_data()
{
    log "Seeding reference data"

    set -a
    # shellcheck disable=SC1090
    source "${ENV_FILE}"
    set +a

    cd "${APP_DIR}"

    sudo -u "${APP_USER}" \
        --preserve-env=DATABASE_URL,SECRET_KEY,APPLICATION_PREFIX,DEFAULT_TIMEZONE,RECIPE_TRANSLATION_API_URL \
        env FLASK_SKIP_DOTENV=1 \
        "${VENV_DIR}/bin/python" \
        scripts/seed_reference_data.py
}


install_service()
{
    log "Installing systemd service"

    cat > "${SERVICE_TARGET}" <<EOF
[Unit]
Description=HomePantry Gunicorn service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple

User=${APP_USER}
Group=${APP_GROUP}

WorkingDirectory=${APP_DIR}
Environment=HOME=${APP_DIR}
EnvironmentFile=${ENV_FILE}

ExecStart=${VENV_DIR}/bin/gunicorn \
    --workers 2 \
    --bind 0.0.0.0:${PORT} \
    --access-logfile - \
    --error-logfile - \
    wsgi:app

Restart=on-failure
RestartSec=3

PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

    chmod 0644 "${SERVICE_TARGET}"

    systemctl daemon-reload

    systemctl enable "${SERVICE_NAME}"

    systemctl restart "${SERVICE_NAME}"
}

health_check()
{
    log "Checking HomePantry health"

    for attempt in $(seq 1 30); do
        if curl \
            --fail \
            --silent \
            "http://127.0.0.1:${PORT}/health" \
            | grep -q '"status":"ok"'
        then
            echo
            echo "HomePantry is running successfully."
            echo
            echo "Local URL:"
            echo "http://SERVER_IP:${PORT}/"
            echo
            echo "Optional recipe translation:"
            echo "sudo ${APP_DIR}/deploy/install-libretranslate.sh"
            echo
            return
        fi

        sleep 1
    done

    systemctl status \
        "${SERVICE_NAME}" \
        --no-pager \
        -l || true

    journalctl \
        -u "${SERVICE_NAME}" \
        -n 100 \
        --no-pager || true

    fail "HomePantry did not pass the health check."
}


main()
{
    require_root
    check_application_directory
    install_packages
    create_service_user
    setup_postgresql
    prepare_environment
    prepare_directories
    create_virtualenv
    run_migrations
    seed_reference_data
    install_service
    health_check
}


main "$@"
