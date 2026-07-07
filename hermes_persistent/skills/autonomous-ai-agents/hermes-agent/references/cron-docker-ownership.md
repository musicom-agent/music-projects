# Cron Jobs in Docker: Ownership & No-Sudo Pitfalls

## Problem: Cron jobs fail or can't be triggered because data is root-owned

### Symptoms
- `cronjob` tool fails: `Permission denied: '/opt/data/cron/jobs.json'`
- `hermes cron list` returns permission errors
- Cannot fix ownership because `sudo: command not found`

### Root Cause
The official Docker image creates `$HERMES_HOME` (`/opt/data` by default) as root.
The `cron/` subdirectory and its files inherit root ownership. When the gateway
switches to the `hermes` user, it can't read cron data.

### Fix Attempt 1: chown
```bash
chown -R hermes:hermes /opt/data/cron
```
**This usually works if the `hermes` user has sufficient permissions.**

### Fix Attempt 2: sudo (usually fails in Docker)
```bash
sudo chown -R hermes:hermes /opt/data/cron
```
**`sudo` is typically NOT installed in the Hermes Docker image.** Do not rely on it.

### Fix Attempt 3: Run as root (not recommended)
```bash
export HERMES_ALLOW_ROOT_GATEWAY=1
# Then run as root — see docker-gateway-troubleshooting.md
```

### Recovery: Reconstructing Job Configs When `jobs.json` Is Inaccessible
If cron fails due to permissions and you need to know what jobs existed, inspect session data:

1. **Cron output directory** — `ls -la /opt/data/cron/output/` lists session subdirs
2. **Session dump JSON** — files at `/opt/data/sessions/request_dump_cron_<ID>_*.json` contain the full request (model, prompt, tools, skill invocations) — useful for reconstructing the job's purpose
3. **Session transcript** — `/opt/data/sessions/session_cron_<ID>_*.json` contains the full conversation, including the job's output
4. **Reconstruct** — from the dump JSON, read the `body.messages[].content` field to find the user prompt and skill content used. This tells you what the job did (schedule, delivery, toolset).

**Note:** This recovers job *purpose*, not exact config fields (schedule, delivery target, etc.). For those, the fix must be outside the container (see above).

### Pitfall
If you're inside the container as the `hermes` user and cron fails:
1. Check ownership: `ls -la /opt/data/cron/`
2. If root-owned, you likely CANNOT fix it — `sudo` is unavailable
3. The only reliable fix is outside the container (Docker Compose/user config)
4. As a workaround, run the cron job's task directly with the relevant skill
   (e.g., `web-research` for news tasks) rather than via the cron tool