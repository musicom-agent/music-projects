# Environment Status — 2026-05-17

## Current State

### Missing Repos
The Musicom framework repos are **not cloned** in this environment:

```
/root/musicom          — NOT FOUND
/root/musicom_ai       — NOT FOUND
/root/musicom_research — NOT FOUND
```

**Impact:** The `musicom-composer` skill and `musicom-theory-kb` knowledge base
cannot execute any generators, transformers, or MIDI export code without these
repos. The theory KB works standalone for reference, but practical composition
requires the code.

**Fix:**
```bash
git clone https://github.com/axelwiertz/musicom.git /root/musicom
git clone https://github.com/axelwiertz/musicom_ai.git /root/musicom_ai
git clone https://github.com/axelwiertz/musicom_research.git /root/musicom_research
```

### Config Persistence Fix Applied

**Problem:** `/opt/data/config.yaml` was owned by `root:root` with `600` perms.
Hermes runs as user `hermes` (uid 10000) and couldn't read/write the config,
so model settings never persisted across restarts.

**Fix applied:** Deleted root-owned file and recreated it with correct ownership.
Model now set to `qwen/qwen3.6-35b-a3b` on OpenRouter.

See `references/config-ownership-pitfall-docker.md` for full details.

### Active Model

- **Model:** `qwen/qwen3.6-35b-a3b`
- **Provider:** OpenRouter
- **Config path:** `/opt/data/config.yaml` (now properly owned by hermes:hermes)

### Installed Music Skills

| Skill | Status | Notes |
|---|---|---|
| `musicom-theory-kb` | ✅ Installed | Theory reference (works without repos) |
| `musicom-composer` | ✅ Installed | Composition workflow (needs repos to execute) |
| `audiocraft-audio-generation` | ✅ Installed | Meta MusicGen/AudioGen |
| `songwriting-and-ai-music` | ✅ Installed | Songwriting craft + Suno prompts |
| `heartmula` | ✅ Installed | Suno-like song generation |
| `songsee` | ✅ Installed | Audio spectrogram analysis |