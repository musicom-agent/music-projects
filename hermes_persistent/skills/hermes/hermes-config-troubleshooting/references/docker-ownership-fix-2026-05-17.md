# Docker Config Ownership Fix — 2026-05-17

## Root Cause

In the Docker container environment, `/opt/data/config.yaml` was owned by `root:root`
with `600` permissions. Hermes Agent runs as user `hermes` (uid 10000), which
meant the agent could **neither read nor write** its own configuration file.

## Symptoms Observed

- `hermes config set model <value>` appeared to succeed but the setting was lost on restart
- `hermes model` always showed default/empty, prompting setup each session
- The gateway fell back to `cli-config.yaml` (which has an empty `model.default`)
- Recurring "Please configure your model" prompts on every startup

## Diagnosis

```bash
# What we found:
ls -la /opt/data/config.yaml
# -rw------- 1 root root 7887 May 15 11:37 /opt/data/config.yaml
# ^^^ root:root ownership, hermes user (10000) cannot access

# Backup files confirmed the LAST GOOD config was:
ls -la /opt/data/config.yaml.bak.*
# All owned by hermes:hermes — confirm the problem is isolated to the active file
```

## Fix Applied

```bash
# 1. Remove the root-owned file (hermes user can delete because parent dir is hermes-owned)
rm /opt/data/config.yaml

# 2. Recreate with correct ownership (write_file from hermes user creates proper ownership)
# Model was restored from backup: qwen/qwen3.6-35b-a3b on OpenRouter
```

## Prevention

- Docker entrypoint should drop privileges **before** creating any config files
- After container startup, verify: `ls -la $HERMES_HOME/config.yaml` shows `hermes:hermes`
- If using Docker volumes, ensure host directory uid/gid matches the hermes user (10000)
- Consider adding a startup health check that validates config file ownership

## Related Skill
- `hermes-config-troubleshooting` — general config troubleshooting guide and prevention patterns