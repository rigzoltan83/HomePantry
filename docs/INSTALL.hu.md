# HomePantry telepítés

Ez az útmutató az ajánlott Ubuntu 24.04 LTS telepítést írja le.

## 1. Repository klónozása

```bash
sudo git clone \
    https://github.com/rigzoltan83/HomePantry.git \
    /opt/homepantry

cd /opt/homepantry
```

## 2. Telepítő futtatása

```bash
sudo ./install.sh
```

A telepítő:

- felrakja a szükséges Ubuntu csomagokat
- létrehozza a `homepantry` rendszerfelhasználót
- előkészíti a PostgreSQL-t
- létrehozza az alkalmazás adatbázisát és DB-felhasználóját
- létrehozza az `/etc/homepantry/homepantry.env` konfigurációt
- létrehozza a Python virtual environmentet
- telepíti a Python függőségeket
- lefuttatja az adatbázis-migrációkat
- betölti a referenciaadatokat
- telepíti a systemd service-t
- elindítja a HomePantry-t
- health checket végez

## 3. HomePantry megnyitása

Alapértelmezett cím:

```text
http://SERVER_IP:8084/
```

Az első felhasználót a webes regisztrációs felületen lehet létrehozni.

Az első felhasználó új háztartást hoz létre, és annak tulajdonosa lesz.

## Konfiguráció

Az éles környezeti fájl:

```text
/etc/homepantry/homepantry.env
```

Tipikus konfiguráció:

```env
FLASK_ENV=production
SECRET_KEY=generated-secret
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@127.0.0.1:PORT/DATABASE
APPLICATION_PREFIX=
DEFAULT_TIMEZONE=Europe/Budapest
RECIPE_TRANSLATION_API_URL=http://127.0.0.1:5000
```

Éles jelszót vagy secretet ne commitolj Gitbe.

## Service kezelése

Állapot:

```bash
sudo systemctl status homepantry.service --no-pager -l
```

Újraindítás:

```bash
sudo systemctl restart homepantry.service
```

Log:

```bash
sudo journalctl \
    -u homepantry.service \
    -n 100 \
    --no-pager
```

Automatikus indulás:

```bash
sudo systemctl enable homepantry.service
```

## Health check

```bash
curl -sS http://127.0.0.1:8084/health
```

Elvárt válasz:

```json
{"application":"HomePantry","status":"ok"}
```

## Reverse proxy / application prefix

A HomePantry útvonal alá is kitehető, például:

```text
/homepantry
```

Beállítás:

```env
APPLICATION_PREFIX=/homepantry
```

Ezután:

```bash
sudo systemctl restart homepantry.service
```

A middleware lehetővé teszi, hogy reverse proxy mögött a beállított prefix
alatt működjön, miközben a közvetlen LAN-elérés továbbra is `/` alatt marad.

## Tailscale Serve példa

```bash
sudo tailscale serve \
    --bg \
    --set-path=/homepantry \
    http://127.0.0.1:8084
```

## Opcionális LibreTranslate

A LibreTranslate csak az importált angol receptek opcionális magyarításához
szükséges.

Telepítés:

```bash
cd /opt/homepantry
sudo ./deploy/install-libretranslate.sh
```

Az alapbeállítás helyben itt figyel:

```text
127.0.0.1:5000
```

Teszt:

```bash
curl -sS http://127.0.0.1:5000/languages
```

Ha a LibreTranslate nem elérhető, a HomePantry az eredeti angol
receptszöveget használja.

## Frissítés

Minden frissítés előtt:

1. Mentsd a PostgreSQL adatbázist.
2. Mentsd a feltöltött képeket.
3. Olvasd el a release notes fájlt.

Ezután:

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

Ellenőrzés:

```bash
curl -sS http://127.0.0.1:8084/health
```

## Biztonsági mentés

Legalább ezeket mentsd:

- PostgreSQL adatbázis
- feltöltött termékképek
- receptképek
- tárolóhely-képek
- éles konfiguráció

A Git repository önmagában nem adatmentés.

## Hibakeresés

Service:

```bash
sudo systemctl status homepantry.service --no-pager -l
```

Log:

```bash
sudo journalctl \
    -u homepantry.service \
    -n 200 \
    --no-pager
```

PostgreSQL clusterek:

```bash
pg_lsclusters
```

8084-es port:

```bash
ss -ltnp | grep ':8084'
```
