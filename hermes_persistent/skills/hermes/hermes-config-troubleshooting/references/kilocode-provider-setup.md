# Kilo Gateway Provider Configuration Setup (2026-07-03)

## Finding
When setting up Kilo Code provider for the first time, use the configuration structure correctly:
- Register under `model.provider` with value `kilo-gateway` (canonical alias).
- The credentials must be placed inside native `.env` under key `KILOCODE_API_KEY`.

## Setup Steps Applied
1. Run setting:
   ```bash
   hermes config set model.provider kilo-gateway
   ```
2. Place Kilo Code JWT token in `/opt/data/.env`:
   ```bash
   KILOCODE_API_KEY=eyJhbGciOiJIUzI1NiIsIn...
   ```
3. Use `/opt/hermes/.venv/bin/python3 -c "import yaml; yaml.safe_load(open('/opt/data/config.yaml'))"` to verify syntax structure is valid after any edits.
