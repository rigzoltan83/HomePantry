# HomePantry deployment

## Application service

HomePantry runs with Gunicorn under systemd.

The application directory is:

```text
/opt/homepantry
```

The application listens on:

```text
0.0.0.0:8084
```

This allows direct LAN access while also allowing a local Tailscale Serve proxy to reach the application.

## Install the systemd service

Copy the provided service file:

```bash
sudo cp \
  /opt/homepantry/deploy/homepantry.service \
  /etc/systemd/system/homepantry.service
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable HomePantry at boot:

```bash
sudo systemctl enable homepantry
```

Start the service:

```bash
sudo systemctl start homepantry
```

Check status:

```bash
sudo systemctl status homepantry --no-pager -l
```

View logs:

```bash
sudo journalctl \
  -u homepantry \
  -n 100 \
  --no-pager
```

Restart after application changes:

```bash
sudo systemctl restart homepantry
```

## LAN access

The application can be accessed directly on the LAN using:

```text
http://SERVER_IP:8084/
```

## Tailscale Serve

HomePantry can also be published under a path on an existing Tailscale Serve HTTPS endpoint.

Example:

```bash
sudo tailscale serve \
  --bg \
  --set-path=/homepantry \
  http://127.0.0.1:8084
```

Check the active Tailscale Serve configuration:

```bash
sudo tailscale serve status
```

Example result:

```text
https://HOSTNAME.TAILNET.ts.net
|-- /homepantry proxy http://127.0.0.1:8084
```

## Application prefix

When HomePantry is exposed through Tailscale Serve under:

```text
/homepantry
```

set the following in:

```text
/opt/homepantry/.env
```

```env
APPLICATION_PREFIX=/homepantry
```

The HomePantry middleware keeps direct LAN access mounted at `/` while restoring `/homepantry` as `SCRIPT_NAME` for requests received through the local HTTPS reverse proxy.

This allows the same running application to generate correct URLs for:

```text
LAN:
http://SERVER_IP:8084/

Tailscale:
https://HOSTNAME.TAILNET.ts.net/homepantry/
```

including:

- login redirects
- logout
- static files
- form actions
- Flask `url_for()` results

## Health check

LAN:

```bash
curl http://127.0.0.1:8084/health
```

Expected:

```json
{"application":"HomePantry","status":"ok"}
```

When accessed through Tailscale Serve, the external URL becomes:

```text
https://HOSTNAME.TAILNET.ts.net/homepantry/health
```

## Data and media considerations

Recipe imports must normalize source measurement units into HomePantry's canonical internal units. The import layer must distinguish metric, US customary, and UK imperial units where their definitions differ.

Image upload support should be optional and designed as a reusable application capability. It should be available for ingredients, prepared foods, and other relevant entities where an image can improve identification or usability.
