---
name: hermes-config-troubleshooting
description: "Troubleshooting Hermes Agent configuration persistence, file ownership, and Docker pitfalls."
tags: [hermes, config, troubleshooting, docker, permissions, persistence]
references:
  - references/config-ownership-pitfall-docker.md
  - references/docker-ownership-fix-2026-05-17.md
  - references/gateway-telegram-recovery.md
  - references/kilocode-provider-setup.md
---

# Hermes Config Troubleshooting

Common issues with `config.yaml` persistence — especially in Docker/container
environments — and how to fix them.

## Recent Session Fixes

### Telegram deaf after updates (2026-07-03)

If the Telegram gateway is running but deaf/silent (not responding to messages):
1. **Check Logs First**: Run `tail -n 120 /opt/data/logs/gateway.log`. Look for `No messaging platforms enabled`, `Telegram ✗ not configured`, or `No env user allowlists configured`.
2. **Key Causes**: Updating Hermes or container restarts can clear `TELEGRAM_BOT_TOKEN` in the active shell environment, or recreate a blank/default `.env` file without the bot variables.
3. **Recovery Sequence**:
   - Check standard active config: `/opt/hermes/.venv/bin/hermes config env-path` to verify active path.
   - Inspect `.env` (usually `/opt/data/.env` or `~/.hermes/.env`) and ensure `TELEGRAM_BOT_TOKEN="your_token"` exists.
   - Add user permission variables: `TELEGRAM_ALLOWED_USERS="8684633270"` (from prior log sessions for Axel) or globally `GATEWAY_ALLOW_ALL_USERS=true`.
   - Run `/opt/hermes/.venv/bin/hermes gateway restart` to restart gateway and apply edits.

### Docker Ownership Fix (2026-05-17)

In a Docker environment running as `hermes` (uid 10000), the config file at
`/opt/data/config.yaml` was found owned by `root:root` with `600` permissions.
Fix: `rm /opt/data/config.yaml` — Hermes recreated it with correct ownership.
Model restored: `qwen/qwen3.6-35b-a3b` on OpenRouter.

See `references/docker-ownership-fix-2026-05-17.md` for full diagnosis.

## ⚠️ Config File Ownership (Most Common Issue)

When Hermes runs inside Docker (or any container), `config.yaml` can end up
owned by `root:root` with `600` permissions. Since Hermes runs as user `hermes`
(uid 10000), it **cannot read or write** its own config file.

### Symptoms

- `hermes config set model X` appears to succeed but the setting is lost on restart
- `hermes model` always shows default/empty, prompting setup each session
- The gateway falls back to `cli-config.yaml` (empty model) every time
- Users see recurring "Please configure your model" prompts

### Root Cause

`save_config_value()` in `cli.py` skips writing if the active config path is
read-only. The fallback to `cli-config.yaml` (which has an empty `model.default`)
masks the problem — settings silently vanish.

In Docker, the entrypoint may create `config.yaml` as root before dropping to the
`hermes` user, leaving root-owned files in `$HERMES_HOME`.

### Fix

```bash
# Option A: Delete and let Hermes recreate with correct ownership
rm $HERMES_HOME/config.yaml
# Next save will create it as the hermes user

# Option B: Fix ownership (if sudo is available)
sudo chown hermes:hermes $HERMES_HOME/config.yaml
sudo chmod 600 $HERMES_HOME/config.yaml

# Option C: Recreate from a backup
cp $HERMES_HOME/config.yaml.bak.<timestamp> $HERMES_HOME/config.yaml
chown hermes:hermes $HERMES_HOME/config.yaml
```

### Prevention

- Ensure Docker entrypoint drops privileges **before** any config files are created
- Run `ls -la $HERMES_HOME/config.yaml` after container startup to verify ownership
- If using Docker volumes, ensure host directory has correct uid/gid mapping
- `HERMES_ALLOW_ROOT_GATEWAY=1` should only be used intentionally

## Config File Locations

| File | Priority | Description |
|------|----------|-------------|
| `$HERMES_HOME/config.yaml` | 1st (user config) | All user customizations go here |
| `<project>/cli-config.yaml` | Fallback | Shipped defaults, used if no user config |

`$HERMES_HOME` defaults to `~/.hermes` but can be overridden via `HERMES_HOME`
env var (in Docker containers it is typically `/opt/data`).

## Messaging Platform Config Pitfall

Telegram and other gateway platforms often depend on `.env` credentials and runtime allowlists, not just `config.yaml`.

When a gateway is alive but Telegram does not answer:
- check `hermes status --all`
- look for `No messaging platforms enabled.` in the gateway log
- verify `TELEGRAM_BOT_TOKEN` plus an allow path such as `TELEGRAM_ALLOWED_USERS` or `GATEWAY_ALLOW_ALL_USERS`
- restart the gateway after `.env` edits

See `references/gateway-telegram-troubleshooting.md` for the Telegram-specific diagnosis flow.

## Verifying Your Config Is Working

```bash
# Check which config file is active
hermes config path

# View current model setting
hermes config | grep -A2 "^model:"

# Check file ownership
ls -la $(hermes config path)
```