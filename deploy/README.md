## Application service

HomePantry runs with Gunicorn under systemd.

The application directory is:

```text
/opt/homepantry
```

## Local recipe translation

HomePantry can use a local LibreTranslate service to translate imported
TheMealDB recipes from English to Hungarian.

The translation service is optional. If it is unavailable, HomePantry
keeps the original English recipe text.

### Install

Docker and the Docker Compose plugin are required.

Run:

    cd /opt/homepantry
    sudo ./deploy/install-libretranslate.sh

The service:

- listens only on `127.0.0.1:5000`
- loads only English and Hungarian language models
- stores downloaded language models in a persistent Docker volume
- restarts automatically unless stopped manually

The first startup may take longer while translation models are downloaded.

### Test

Check the available languages:

    curl -sS http://127.0.0.1:5000/languages

A successful setup should list `en` and `hu`.

Test an English-to-Hungarian translation:

    curl -sS \
      -X POST \
      http://127.0.0.1:5000/translate \
      -H "Content-Type: application/json" \
      -d '{
        "q": "Add the chicken and fry until golden brown.",
        "source": "en",
        "target": "hu",
        "format": "text"
      }'

The response should contain a Hungarian `translatedText` value.

### Configuration

The default translation service URL is:

    http://127.0.0.1:5000

It can be overridden with:

    RECIPE_TRANSLATION_API_URL=http://127.0.0.1:5000

If LibreTranslate is unavailable, recipe import remains functional and
HomePantry falls back to the original English recipe text.
