# Docker Gateway Troubleshooting

## Problem: Gateway refuses to start inside Docker

### Symptom
```
✗ Refusing to run the Hermes gateway as root inside the official Docker image.
  The image entrypoint normally drops privileges to the 'hermes' user.
  If you override entrypoint in Docker Compose, include
  /opt/hermes/docker/entrypoint.sh before the Hermes command.
  Set HERMES_ALLOW_ROOT_GATEWAY=1 only if you intentionally accept this risk.
```

### Root Cause
The official Docker image's entrypoint (`/opt/hermes/docker/entrypoint.sh`) switches
from root to the `hermes` user. If you override the entrypoint (e.g. in Docker
Compose), the gateway runs as root and refuses to start for security reasons.

Additionally, all files in `$HERMES_HOME` (`/opt/data` by default) are owned by root
because they were created before the user switch. The `hermes` user cannot read them.

### Fix Procedure

1. **Fix file ownership:**
   ```bash
   chown -R hermes:hermes /opt/data
   chmod 755 /opt/data /opt/data/sessions /opt/data/skills /opt/data/logs
   ```

2. **Run as the hermes user:**
   ```bash
   su -s /bin/bash hermes -c \
     'export HERMES_HOME=/opt/data && /opt/hermes/.venv/bin/hermes gateway run'
   ```

3. **Or fix the entrypoint** in Docker Compose:
   ```yaml
   entrypoint: ["/opt/hermes/docker/entrypoint.sh"]
   command: ["/opt/hermes/.venv/bin/hermes", "gateway", "run"]
   ```

### Quick Check
Always check file ownership when gateway won't start in Docker:
```bash
ls -la /opt/data/  # Are files owned by root? → chown -R hermes:hermes /opt/data
```

### Pitfall
Simply switching to the `hermes` user is not enough — the `$HERMES_HOME` files must
also be owned by that user. The gateway fails silently with a PermissionError on
`.env` or `config.yaml` if ownership is wrong.
