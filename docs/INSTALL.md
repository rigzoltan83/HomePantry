# HomePantry Installation

This guide describes the recommended installation on Ubuntu 24.04 LTS.

## 1. Clone the repository

```bash
sudo git clone \
    https://github.com/rigzoltan83/HomePantry.git \
    /opt/homepantry

cd /opt/homepantry
```

## 2. Run the installer

```bash
sudo ./install.sh
```

The installer:

- installs required Ubuntu packages
- creates the `homepantry` system user
- prepares PostgreSQL
- creates the application database and role
- creates `/etc/homepantry/homepantry.env`
- creates the Python virtual environment
- installs Python dependencies
- runs all database migrations
- seeds reference data
- installs the systemd service
- starts HomePantry
- performs a health check

## 3. Open HomePantry

By default:

```text
http://SERVER_IP:8084/
```

Register the first user through the web interface.

The first user creates a new household and becomes its owner.

## Configuration

The production environment file is:

```text
/etc/homepantry/homepantry.env
```

Typical configuration:

```env
FLASK_ENV=production
SECRET_KEY=generated-secret
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@127.0.0.1:PORT/DATABASE
APPLICATION_PREFIX=
DEFAULT_TIMEZONE=Europe/Budapest
RECIPE_TRANSLATION_API_URL=http://127.0.0.1:5000
```

Do not commit production secrets to Git.

## Service management

Status:

```bash
sudo systemctl status homepantry.service --no-pager -l
```

Restart:

```bash
sudo systemctl restart homepantry.service
```

Logs:

```bash
sudo journalctl \
    -u homepantry.service \
    -n 100 \
    --no-pager
```

Enable at boot:

```bash
sudo systemctl enable homepantry.service
```

## Health check

```bash
curl -sS http://127.0.0.1:8084/health
```

Expected response:

```json
{"application":"HomePantry","status":"ok"}
```

## Reverse proxy / application prefix

HomePantry can be served below a path such as:

```text
/homepantry
```

Set:

```env
APPLICATION_PREFIX=/homepantry
```

Then restart:

```bash
sudo systemctl restart homepantry.service
```

The middleware allows reverse-proxy access under the configured prefix
while preserving direct LAN access at `/`.

## Tailscale Serve example

```bash
sudo tailscale serve \
    --bg \
    --set-path=/homepantry \
    http://127.0.0.1:8084
```

## Optional LibreTranslate

LibreTranslate is only required for optional English-to-Hungarian
translation of imported recipes.

Install:

```bash
cd /opt/homepantry
sudo ./deploy/install-libretranslate.sh
```

The provided setup listens locally on:

```text
127.0.0.1:5000
```

Test:

```bash
curl -sS http://127.0.0.1:5000/languages
```

If LibreTranslate is unavailable, HomePantry keeps the original English
recipe text.

## Updating

Before every update:

1. Back up the PostgreSQL database.
2. Back up uploaded media.
3. Review the release notes.

Then update the source and migrations:

```bash
cd /opt/homepantry

sudo systemctl stop homepantry.service

git pull

/opt/homepantry/venv/bin/pip install -r requirements.txt

set -a
source /etc/homepantry/homepantry.env
set +a

sudo -u homepantry \
    env \
    FLASK_SKIP_DOTENV=1 \
    DATABASE_URL="$DATABASE_URL" \
    SECRET_KEY="$SECRET_KEY" \
    APPLICATION_PREFIX="${APPLICATION_PREFIX:-}" \
    DEFAULT_TIMEZONE="${DEFAULT_TIMEZONE:-Europe/Budapest}" \
    RECIPE_TRANSLATION_API_URL="${RECIPE_TRANSLATION_API_URL:-http://127.0.0.1:5000}" \
    /opt/homepantry/venv/bin/flask \
    --app wsgi:app \
    db upgrade

sudo systemctl start homepantry.service
```

Verify:

```bash
curl -sS http://127.0.0.1:8084/health
```

## Backup

Back up at least:

- PostgreSQL database
- uploaded product images
- recipe images
- storage-location images
- production environment configuration

Do not rely only on a copy of the Git repository as a backup.

## Troubleshooting

Check the service:

```bash
sudo systemctl status homepantry.service --no-pager -l
```

Check recent logs:

```bash
sudo journalctl \
    -u homepantry.service \
    -n 200 \
    --no-pager
```

Check PostgreSQL clusters:

```bash
pg_lsclusters
```

Check the application port:

```bash
ss -ltnp | grep ':8084'
```
