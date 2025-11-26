# Superset + Trino Docker Compose Stack

This repository provides a simple, local development stack that runs Apache Superset and Trino in Docker containers. The Superset image is extended to include the Trino driver and is configured to connect to a Trino catalog (e.g., a MongoDB connector configured in Trino).

> ⚠️ Note: This is intended as a developer / demo setup. For production use, secure secrets, enable CSRF, and follow Superset and Trino best practices.

---

## What this project does

- Runs a Trino server (with a MongoDB connector) and Apache Superset using `docker-compose`.
- Builds a custom Superset image (in `superset-stack/`) that installs `sqlalchemy-trino` and pins `SQLAlchemy` for compatibility.
- Persists Superset metadata and dashboards to a local `superset_data` directory.
- Mounts a local Superset config file to allow simple local overrides.

---

## Repo structure (key files)

- `docker-compose.yml` — Orchestrates the `trino` and `superset` services and volume mappings.
- `superset-stack/Dockerfile` — Builds a custom Superset image that installs the Trino driver and copies a configuration file into the container.
- `superset-stack/superset_config.py` — Superset config used by the image.
- `superset_config_docker.py` — Local config mounted into the running Superset container (overrides image config).
- `trino/mongodb.properties` — Example Trino catalog config for the MongoDB connector (contains a connection URI; replace with your credentials).
- `superset_data/` — Persisted Superset metadata database (sqlite by default) and other Superset-related files.

---

## Prerequisites

- Docker (20.x+ recommended)
- Docker Compose (v1 or v2) or the `docker compose` plugin
- Internet access (to pull images and Pip packages during build)
- A MongoDB instance or other data source that Trino can connect to (optional — you can still run Superset without data sources).

---

## Quickstart (local development)

1. Start the stack (from the repository root):

```bash
# With the new Docker Compose plugin
docker compose up --build

# or (legacy)
docker-compose up --build
```

This will:
- Build the Superset image from `superset-stack/Dockerfile`.
- Start Trino on `localhost:8080` and Superset on `localhost:8088`.
- Create an admin user (username `admin`, password `admin`) and run `superset db upgrade` + `superset init` — configured in the `docker-compose.yml` service `command`.

2. Open Superset UI:
- http://localhost:8088 — login with `admin` / `admin` (change the password ASAP)

3. Open Trino UI:
- http://localhost:8080 — Trino HTTP web UI (catalogs, connectors, etc.)

---

## How to add a Trino data source in Superset

1. In Superset, go to Data -> Databases -> + Database.
2. Use the SQLAlchemy URI format for Trino:

```
trino://<username>@trino:8080/<catalog>/<schema>
```

Example using credentials in the repository (replace with your own):

```
trino://faishion@trino:8080/mongodb/<database>
```

Notes:
- The `catalog` name is determined by the filename in `/etc/trino/catalog` (the file name without the `.properties` extension). In this repo the file is `trino/mongodb.properties`, so the Trino catalog name will be `mongodb`.
- Replace credentials and values with your real connection data.

---

## Configuring Superset and Trino

- `superset_config_docker.py` is mounted into the container and includes a small set of development settings:
  - `ENABLE_PROXY_FIX = True`
  - `TALISMAN_ENABLED = False` (disables HTTPS enforcement)
  - `WTF_CSRF_ENABLED = False` (disables CSRF protection for dev / tunnels)
  - `PREVENT_UNSAFE_DB_CONNECTIONS = False`

These settings are convenient for local development and tunneling with tools like ngrok but are not suitable for production.

- To change `SUPERSET_SECRET_KEY`, `TALISMAN_ENABLED`, or other environment settings, edit `docker-compose.yml` or pass environment variables into the running container.

- To modify the Trino configuration for a connector, edit `trino/mongodb.properties`. Keep sensitive credentials out of VCS in production — use environment variables or a secret manager.

---

## Troubleshooting & Tips

- If Superset can't connect to Trino:
  - Confirm that the Trino catalog file exists in `trino/*.properties` and that Trino picks it up (check the Trino web UI).
  - Confirm that the connection string you use in Superset uses the right `catalog` and `schema`.
  - If queries fail due to SQLAlchemy incompatibilities, the Dockerfile pins `SQLAlchemy==1.4.49` and installs `sqlalchemy-trino` to ensure compatibility.

- If you get permission issues when copying config into the container, permissions are adjusted in the Dockerfile (`chown -R superset:superset /app/pythonpath`).

- On macOS, file permissions with mounted volumes can cause issues; if you run into permission errors, check the mount and possibly adapt volume mapping.

- To reinitialize or clear Superset state during development:

```bash
# Stop the containers
docker compose down

# (Optional) Remove persisted superset DB and data
rm -rf superset_data/

# Start fresh
docker compose up --build
```

---

## Security considerations

This repo intentionally disables some security protections (e.g., CSRF) to simplify local development and tunneling. For production deployments:

- Do NOT disable CSRF (set `WTF_CSRF_ENABLED = True`).
- Do NOT disable Talisman or HTTPS enforcement.
- Use a secure, random `SUPERSET_SECRET_KEY` and store it safely (environment variables or secret manager).
- Use an external database (PostgreSQL or MySQL) for Superset metadata instead of the included local SQLite database.
- Avoid storing database credentials in files; prefer environment variables or a secrets manager.

---

## Customization

- To change the default admin user, modify the `command` in `docker-compose.yml` or manually create users using `superset fab create-admin` inside the container.

- To add new Trino catalogs, add a new `*.properties` file to `trino/` and restart Trino. For example, `trino/your_catalog.properties`.

- To install additional Python packages into the Superset image, update `superset-stack/Dockerfile` and rebuild.

---

## Example useful commands

```bash
# Build and run
docker compose up --build

# Start in detached mode
docker compose up -d --build

# View logs
docker compose logs -f --tail=200

# Run a command in the running superset container
docker exec -it superset bash

# Create or manage admin user manually
docker exec -it superset superset fab create-admin --username admin --firstname Admin --lastname User --email admin@example.com --password 'your-secret-password'

# Reinitialize database (in the running container)
docker exec -it superset superset db upgrade

docker exec -it superset superset init
```

---

## License & Contributing

This repo is provided without a license. If you plan to share or use it publicly, add your preferred open source license (e.g., MIT, Apache 2.0) and update the `README` accordingly.

Contributions: feel free to raise issues or PRs for improvements. Avoid committing credentials or secrets.

---

## Summary

This repo is a minimal local developer stack that helps you evaluate and prototype Apache Superset with Trino (MongoDB connector) using Docker Compose. It includes a custom Superset image with the Trino driver installed and demonstrates mounting a local config file and persisting Superset state.

For production, please follow the standard Superset and Trino architecture documentation and security guidance.
