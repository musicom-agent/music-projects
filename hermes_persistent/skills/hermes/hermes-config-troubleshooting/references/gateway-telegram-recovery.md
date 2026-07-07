# Telegram gateway recovery notes

## Symptom cluster
- `hermes status --all` shows Telegram not configured.
- `gateway.log` shows `No messaging platforms enabled.` or `No env user allowlists configured.`
- Gateway process exists, but Telegram does not answer.

## Recovery sequence
1. Confirm the gateway is running and whether Telegram is enabled.
2. Confirm the running process has `TELEGRAM_BOT_TOKEN` and an allow path:
   - `TELEGRAM_ALLOWED_USERS=<telegram_user_id>`
   - or `GATEWAY_ALLOW_ALL_USERS=true` with open platform policy.
3. If the token was added to `/opt/data/.env`, restart from a shell outside the gateway process so the new env is loaded.
4. Recheck `hermes status --all` and the gateway log for `✓ telegram connected`.

## Restart pitfall
- Do **not** call `hermes gateway restart` from inside the same gateway process / TUI session. The command can self-terminate before restart completes.
- Use a separate shell, or stop the gateway first and start it again from outside the running process.

## Provider alias note
- For Kilo Code / KiloGateway, the canonical Hermes provider alias is `kilo-gateway`.
- Backing credential: `KILOCODE_API_KEY`.

## Validation
- `hermes config path`
- `hermes status --all`
- `tail -n 40 /opt/data/logs/gateway.log`
- `python -c 'import yaml; print(yaml.safe_load(open("/opt/data/config.yaml")).get("model"))'`
