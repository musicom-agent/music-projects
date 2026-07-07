# Telegram Gateway Not Responding: Diagnosis

## Symptom
Gateway process alive, but Telegram messages get no reply.

## Fast checks
1. `hermes status --all`
   - If it shows `Telegram ✗ not configured`, the gateway has no Telegram platform config loaded.
2. `gateway.log`
   - `No messaging platforms enabled.` means the gateway started, but zero chat platforms were enabled.
   - `No env user allowlists configured...` means platform authz is default-deny until allowlists or open policy are set.
3. Process env
   - Verify `TELEGRAM_BOT_TOKEN` exists in the running gateway environment.
   - Verify one of the allow paths exists:
     - `TELEGRAM_ALLOWED_USERS=<telegram_user_id>`
     - `GATEWAY_ALLOW_ALL_USERS=true` plus platform open policy

## Common root causes
- Token only present in a shell, not in the gateway process environment.
- `/opt/data/config.yaml` has telegram display settings only, not bot credentials.
- Gateway restarted before `.env` changes were loaded.
- Allowlist missing, so Telegram authz silently blocks unknown senders.

## Recovery sequence
```bash
# Locate active env path
/opt/hermes/.venv/bin/hermes config env-path

# Verify if TELEGRAM_BOT_TOKEN and perm vars are inside active env
cat /opt/data/.env

# Restart gateway to load environment changes
/opt/hermes/.venv/bin/hermes gateway restart
```

## Useful log signatures
- `No messaging platforms enabled.`
- `Telegram ✗ not configured`
- `No env user allowlists configured.`
- `Telegram network error ... reconnecting` (network layer issue, different class)

## Notes
- `telegram.reactions` and `telegram.allowed_chats` in config.yaml are not enough to bring Telegram up.
- Token and user allowlist live in the environment, not in the display config.
- Restart required after `.env` changes.