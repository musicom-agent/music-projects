# Session Auto-Reset (Autoreset) Configuration

This reference documents the auto-reset policies, modes, configuration steps, and gateway restart behaviors of Hermes Agent.

## Session Auto-Reset Modes

The `session_reset` section in `config.yaml` dictates when a session's context is automatically cleared/reset:

| Mode | Behavior |
|---|---|
| `none` | Auto-reset disabled. Sessions are persistent until manually flushed using `/new` or `/reset`. |
| `both` | Sessions automatically reset after `idle_minutes` of inactivity OR daily at `at_hour:00`. |
| `idle` | Sessions automatically reset after `idle_minutes` of inactivity. |
| `daily` | Sessions automatically reset daily at `at_hour:00`. |

## How to Configure Autoreset

### ⚠️ Security Guardrail
Standard file tools (`patch`, `write_file`) are blocked from editing the active config file `/opt/data/config.yaml` to prevent security-sensitive modifications.

### Recommended Edit Method
Always use the `hermes config` CLI inside a `terminal` tool call to modify configuration:

```bash
# Enable both idle and daily auto-reset
hermes config set session_reset.mode both

# Verify the config was written correctly
hermes config | grep -A3 "^session_reset:"
```

## Gateway Applying & Process Blockers

When running inside a messaging gateway (like Telegram or Discord):
1. **Config changes are not live automatically**: The gateway process reads `config.yaml` at startup and needs to be restarted to apply changes.
2. **`hermes gateway restart` terminal block**: Attempting to run `/opt/hermes/.venv/bin/hermes gateway restart` from a terminal tool call inside a gateway session will fail. The runner will block it with:
   `Blocked: cannot restart or stop the gateway from inside the gateway process. The gateway would kill this command before it could complete (SIGTERM propagates to child processes).`
3. **Correct workflow**: Inform the user to manually send the `/restart` slash command in the gateway chat to cleanly bounce the gateway process.
