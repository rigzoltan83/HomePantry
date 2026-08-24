# HomePantry deployment

## Application service

HomePantry runs with Gunicorn under systemd.

The application directory is:

```text
/opt/homepantry

## Local recipe translation

HomePantry can use a local LibreTranslate service to translate imported
TheMealDB recipes from English to Hungarian.

The translation service is optional. If it is unavailable, HomePantry
keeps the original English recipe text.

### Install

Docker and the Docker Compose plugin are required.

Run:

```bash
cd /opt/homepantry
sudo ./deploy/install-libretranslate.sh
