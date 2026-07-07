---
name: music-project-workflow
description: "End-to-end music project organization: set up GitHub repos, project templates, MIDI analysis pipeline, and BandLab integration. Covers project structure conventions, agent collaboration patterns, and iterative versioning."
version: 1.0.0
author: community
license: MIT
platforms: [linux]
prerequisites:
  commands: [git]
  services: [GitHub account, himalaya email client]
references:
  - templates/project-readme.md
  - templates/bandlab-link.md
  - references/vst-summation.md
  - references/composition-methods-database.md
  - references/dashboard-standardization-2026-06-24.md
  - references/lead-sheet-lyrics-publish.md
---

# Music Project Workflow

## Reporting & Documentation Standardization (2026-06-24)

### 1. Delivery Tiering
For creative and research tasks, use two-tier reporting to manage Telegram noise:
- **Telegram (Compact)**: Return bulleted key-value pairs of major parameters only. Minimize descriptions. One or two audio/file attachments maximum.
- **Local (Full)**: Log exhaustive technical detail, formulas, and full reasoning to a project-local `logs/` directory using `dsp-daily-$(date +%F).md` naming.

### 2. Composition Validation
Always perform a "White Box" analysis of generated MIDI:
- Check lead non-chord-tones against the declared scale.
- Verify harmonic support (Bass/Harmony) for 100% chord-tone accuracy (unless the genre logic specifically dictates otherwise).
- Log these accuracy percentages in the daily summary.
- If the project is lyrics-driven, validate prosody fit too: stress, punctuation, question/answer phrasing, and singability.

### 3. Repository Separation
Distribute complex composer interfaces into three distinct repositories:
- `[project]-core`: The Python logic/library.
- `[project]-api-backend`: FastAPI/REST wrapper for headless orchestration.
- `[project]-web-portal`: React/Next.js frontend for human-composer steering.

## Common Pitfalls
- **Workdir confusion**: When running background services (e.g., Uvicorn), `cd` into the directory explicitly or use absolute paths for the APP target; do not rely on `--workdir` flags which may not be supported by all server versions.
- **Missing OGG**: Ensure `ffmpeg` converts the primary WAV to OGG for Telegram instant-play.
- **UnitMatrix-first documentation**: When adding composition methods to `methods_db.md`, write each method as a class-level pattern, not as a one-off artifact. Include all five Musical Elements plus a clear UnitMatrix mapping with rows=voices and columns=sections.
- **Method synthesis standard**: Prefer a genuinely new method class over duplicating an existing heading. Use the stable database template: Source → Workflow → Description → Filling the Elements → UnitMatrix Mapping → Best Use. Verify the inserted heading before notification.
- **Research-backed method entries**: Prefer a fresh, externally sourced method update over inventing a duplicate of an existing technique. If the page or paper is about Transformer or deep-learning composition, capture the exact contribution and the evaluation metrics or control mechanism that matter.
- **Telegram delivery in cron**: If a message must go out from a scheduled job, keep it compact and verify the bot path/allowlist in the running gateway environment before assuming delivery. A session can have credentials in a shell but still lack them in the active gateway process.
- **Notification fallback**: If Telegram env is missing in the runtime, report the delivery gap explicitly instead of assuming the bot is down. Probe the runtime env first, then send the smallest possible message once a valid chat target exists.

Organize music composition projects in a GitHub repository with standardized structure, agent analysis, and BandLab production pipeline.

## When to Use

- User wants to start organizing music projects in GitHub
- User has a MIDI file that needs analysis and version control
- User wants a repeatable pipeline for new compositions
- User needs to set up project templates and folder structure

## Project Portfolio & Style Structure

- **Terminology Rule**: Use **'Style'** instead of 'Genre' as the primary classifier.
- **Canonical Hierarchy**: All active music projects live in `/opt/data/projects/Styles/`.
- **Mirroring**: Mirror local `/opt/data/projects/` to `musicom-agent/music-projects` via `git push origin main`.
- **Root Comparison**: `/opt/data/projects/Styles/_Comparison/` contains cross-style analysis and dashboards.
- **Style Folders**: Every folder (e.g., `/Styles/Country/`) must contain:
    - `/Analysis/patterns.md`: Machine-readable Rhythm patterns, Scales, and metrical gravity.
    - `/Analysis/theory.md`: Deeper stylistic logic and examples.
- **Daily Experiments**: Move daily work deep within the specific style folder (e.g., `/Styles/Latin/bossa-nova-daily`). Never use a root-level `Experiments/` folder.
- **Data Dataset**: Pattern datasets live at `/opt/data/projects/Styles/_Data_Patterns`.

## Workflow Consolidation Invariant
- **Merging Rule**: When a new composition is an iteration or variation of a previous one, **merge or append** into the existing project folder rather than creating redundant top-level numbered projects (e.g., `012-country-full-16bar` consolidated two previous loop drafts).
- **Full Production Workflow**: For every composition, maintain:
  - `MIDI/`: Editable files.
  - `Audio/`: HQ Renders (**WAV strictly for quality**, OGG for voice bubbles).
  - `Analysis/`: Patterns and metrical grids.

### VST & FluidSynth Pitfalls
- **Piano Default**: FluidSynth defaults to Program 0 (Piano). Force Orchestral Strings (Patch 48) via `-o synth.midi-bank-select=gm`.
- **VST Monophony**: Headless VSTs (Kars/Nekobi) often lock to the first note. Use "Summation" method (see `references/vst-summation.md`).
  - `Notes/`: Dev log and logic.
  - `Scores/`: MusicXML.
  - `src/`: Regeneration scripts.
  - `index.html`: VoltAgent Dashboard.
- **Visualization**: Use high-contrast ASCII markers (█ and ░) for rhythmic pattern visualization in all dashboards.

## Repository Boundary Convention

The canonical project repository is `musicom-agent/music-projects`. It stores numbered composition projects, MIDI/MusicXML, audio renders, analysis, dashboards, notes, and project-local scripts.

**Canonical local workspace:** `/opt/data/projects/`. This folder is mirrored to the `music-projects` repo. Create, move, edit, and verify numbered project folders here first. Do **not** treat ad-hoc clones such as `/root/projects/music-projects` or `~/projects/music-projects` as the canonical workspace unless the user explicitly asks for a separate clone. If you accidentally create project content elsewhere, move it into `/opt/data/projects/<NNN-project-name>/`, verify file counts, and remove or reset the stray clone so future agents do not work in the wrong tree.

The handover/documentation repository is `axelwiertz/musicom-agent`. It stores Musicom agent introduction, composer skill docs and references, onboarding/handover notes, session logs, and framework documentation/prototypes. Do **not** embed project portfolio folders inside this repo.

If repo ownership/context is unclear, check memory/session history and remotes before asking the user. The stable known owner/account is `musicom-agent`; the handover repo lives under `axelwiertz`.

See `references/repository-boundaries-2026-05-30.md` for the reorganization record and verification pattern. See `references/canonical-local-project-workspace.md` for the `/opt/data/projects/` correction and wrong-clone recovery steps.

## Project Structure Convention

### Top-Level Location Rules

The `/opt/data/projects/` tree has four top-level branches with distinct purposes:

| Branch | Purpose | Numbering |
|--------|---------|-----------|
| `Styles/{Name}/` | Genre/style composition projects, pattern datasets, daily composition experiments | Per-style folders, no global NNN prefix |
| `Genres/{Name}/` | DNA-first genre categorization for composition projects (compatible with old convention) | `NNN-project-name` inside genre folders |
| `Research/` | **DSP research, virtual instrument synthesis, technical/engineering experiments** — NOT composition projects | `NNN-project-name` sequential |
| `Knowledge/` | Reference docs, theory notes, external resources | Per-topic folders |

**Critical boundary: DSP research NEVER goes under `Genres/Research/`.** The `Genres/` tree is for composition projects and style studies only. Virtual instrument development, audio DSP scripts, physical modeling experiments belong under `Research/` as numbered projects (e.g., `Research/014-virtual-instruments-dsp/`). Do not create a `Genres/Research/` subfolder — it's a path error that gets corrected.

When in doubt: if it produces a musical composition, it goes in `Genres/` or `Styles/`. If it produces a synthesizer/instrument/audio-engine, it goes in `Research/`.

- **Repository Boundaries**: 
  - `musicom-agent/music-projects`: Canonical repo for numbered composition projects (001, 002...).
  - `axelwiertz/musicom-agent`: Agent role/config and composer skill docs.
  - **Do NOT** embed project portfolio folders inside `axelwiertz/musicom-agent`.
- **Project Numbering Verification**: Before initializing a new project (e.g., `mkdir 016-...`), always check the existing project list in `music-projects` to prevent number collisions. If a collision occurs, rename the new project immediately to the next available integer.
- **Path**: Use `/opt/data/projects/` as the persistent root.
- **Style-First Organization**: Create project folders within `/opt/data/projects/Styles/[StyleName]/[NNN-project-name]/`. (Example: `/opt/data/projects/Styles/Rock/001-here-comes-the-sun/`).
- **Initial Analysis**: Immediately run `midi-analysis` on source MIDI and save to `Analysis/midi-analysis.txt`.
- **UnitMatrix-first composition**: For any music project, treat rows as voices/pattern layers and columns as sections/time blocks. The project files should document that matrix explicitly so the dashboard and analysis mirror the real musical architecture.
- **Daily-to-project promotion**: When a daily draft is keep-worthy, promote it into a numbered real project with `README.md`, `index.html`, `Analysis/`, `Notes/`, `MIDI/`, `Audio/`, `Scores/`, `Scripts/`, and `BandLab/`. Do not leave the work in a loose daily folder if it is now a project.
- **Style-First Categorization**: Daily and standard composition projects are organized under `/opt/data/projects/Styles/[StyleName]/[NNN-project-name]/` instead of leaving them scattered in ad-hoc subdirectories or root-level daily dirs.
- **Multitrack Setup Requirements**: Daily composition experiments should target a complete multitrack arrangement mapping typical style instrumentation: a clear rhythm track (on percussion channel 10 for MIDI), a distinct melody line, and clear harmonic/chordal support.
- **Same workflow everywhere**: Use the same promotion and documentation workflow for daily experiments and on-demand composer tasks.
- **Global Project Index**: The root `index.html` in `Styles/` (or root projects dir) is a global dashboard listing all projects. Each project folder contains its own `index.html` for project-specific details. When adding a new project, merge its entry into the global `index.html` to maintain a single source of truth for all projects.
- **Conflict Resolution**: If `git pull` results in an `add/add` conflict in `index.html`, resolve by merging the new project entry into the global list. Use the global `index.html` as the base and add the new project's section to it. Do not overwrite the global index with a project-specific version.

```
music-projects/                          # Single GitHub repo for all projects
├── README.md                            # Overview + status table of all projects
├── templates/
│   └── project-template/
│       └── README.md                    # Template for new projects
└── NNN-project-name/                    # Each project gets its own folder
    ├── README.md                        # Concept, key, tempo, references, notes
    ├── MIDI/
    │   └── original.mid                 # Source MIDI file
    ├── Analysis/
    │   └── midi-analysis.txt            # Agent-generated analysis
    ├── Notes/
    │   ├── concept.md                   # Mood, target audience, ideas
    │   └── references.md                # Inspiration sources
    ├── BandLab/
    │   └── link.md                      # BandLab project URL
    ├── Stems/                           # (empty, for future audio stems)
    └── Renders/                         # (empty, for final audio)
```

**Folder naming convention:** `/opt/data/projects/Styles/{StyleName}/`. Use `patterns.md` and `theory.md` for style specs.

### Technical workflow
- **Research & Extraction**: Consolidate multi-file datasets into single `knowledge.json` files per sub-style.
- **Visualization**: Generate a `VISUALIZATION.md` in each style folder to provide a readable summary of rhythm and pitch properties.
- **Job Synchronization**: Ensure automated composition jobs scan the `Styles/` tree for source material.
- **Caveman Style**: Use minimum tokens for high accuracy in reports. Stop filler.


## Authentication Setup

### GitHub PAT (Primary Method)

The agent needs a GitHub Personal Access Token with:
- `repo` scope (full repository access)
- `write:packages` if using GitHub Packages

Store the token and construct the remote URL:
```bash
git remote set-url origin "https://musicom-agent:<TOKEN>@github.com/<OWNER>/<REPO>.git"
```

### SSH Key (Fallback)

If a GitHub SSH key exists, verify it works:
```bash
ssh -T git@github.com
# Should show: "Hi <username>! You've successfully authenticated..."
```

If SSH works but repo doesn't exist, create it via API with PAT first, then switch to SSH.

## Adding a New Project (Step-by-Step)

For generated drafts that already have paired MIDI/audio in `/tmp/hermes/songs`, see `references/promote-generated-draft-to-project.md`. Use the canonical `~/projects/music-projects` clone, copy all generated artifacts into `NNN-project-name`, add a dashboard, commit with Musicom Agent identity, and push `main`.

1. **Get the MIDI file** — if not on disk, use email (himalaya), paste, or scp
2. **Create folder structure in the canonical local workspace:**
   ```bash
   cd /opt/data/projects
   mkdir -p <NNN-project-name>/{MIDI,Audio,Stems,Renders,Notes,BandLab,Analysis,Scripts,Scores}
   ```
3. **Copy MIDI to MIDI/original.mid** and any listenable render to `Audio/`
4. **Create README.md** with concept, key, tempo, references
5. **Run MIDI analysis** using `midi-analysis` skill
6. **Save analysis** to `Analysis/midi-analysis.txt`
7. **Create Notes/concept.md** with mood, audience, improvement ideas
8. **Placeholder BandLab link** in `BandLab/link.md`
9. **Commit and push:**
   ```bash
   git add -A
   git commit -m "<NNN>: add <project-name>"
   git push origin main
   ```

## Project README Template

Use `references/templates/project-readme.md` as the base for each project's README:

Required sections:
- **Title** with project number and name
- **Concept** — what's the idea, mood, genre, target audience
- **Key & Tempo** — key signature, BPM, time signature
- **Instrument** — program number and instrument name
- **Notes** — important observations about the piece
- **References** — inspiration sources
- **BandLab** — link to cloud DAW project
- **Variations** — v1, v2, v3... for documenting iterations

## Agent's Role in the Pipeline

| Stage | What the Agent Does | Output |
|-------|---------------------|--------|
| Receive | Accept MIDI via email, paste, or disk | File on disk |
| Analyze | Full MIDI analysis (structure, tempo, key, notes, rhythm) | `Analysis/midi-analysis.txt` |
| Document | Create concept notes and improvement suggestions | `Notes/concept.md` |
| Version | Git commit/push with descriptive messages (Backup to branches on conflict) | Git history |
| Iterate | Accept new MIDI for v2, diff against previous, suggest changes | Updated files |

## Dual Export Protocol (Mandatory)
Every generated composition or audio sequence MUST be exported as a paired set:
1. **Audio (`.ogg`/`.mp3`)**: For instant Telegram playback (voice bubble).
2. **MIDI (`.mid`)**: For DAW import and editing, generated via `music21` alongside the audio.
Never generate an audio file without its matching MIDI file in the same directory. Note: The user wants a MIDI file for EVERY audio file.

## Generate & Stream Step (Continuous Mode)

For projects requiring continuous generation + mobile streaming, add this as a standard pipeline step after composition and export.

### Architecture (Firewall-Proof)

```
Generator (Python/algorithmic)
    │ runs every 60-120s
    ▼
Audio file (live_render.ogg or .mp3)
    │
    ├── ► Flask Radio Server (port 8001 on VPS)
    │     Requires open port in Hostinger hPanel (Security > Firewall > Add TCP 8001)
    │     URL: http://<VPS_IP>:8001/stream.ogg
    │     iOS: Safari/Firefox -- must be MP3 not OGG for reliable playback
    │
    └── ► Discord Push (no ports needed)
          Generator → Send to discord:#channel via hermes messaging
          User plays chunk directly in Discord mobile app
```

### Generic Stream Script Template

Place a `radio_server.py` in every project's `src/` when continuous streaming is desired:

```python
import os, time, subprocess
from flask import Flask, Response

PROJECT_DIR = "/opt/data/projects/Genres/<Genre>/NNN-project-name"
ENGINE = os.path.join(PROJECT_DIR, "src/stream_engine.py")
AUDIO = os.path.join(PROJECT_DIR, "Audio/live_render.mp3")

app = Flask(__name__)

@app.route("/")
def index():
    return "<audio controls autoplay src='/stream.mp3'></audio>"

@app.route("/stream.mp3")
def stream():
    def gen():
        while True:
            subprocess.run(["python3", ENGINE], check=True)
            with open(AUDIO, "rb") as f:
                yield f.read()
            time.sleep(60)
    return Response(gen(), mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, threaded=True)
```

### Delivery Configuration

| Method | Setup Required | Reliability | 
|--------|---------------|-------------|
| **Flask radio (port 8001)** | Hostinger firewall rule (TCP 8001) | Good (direct URL) |
| **Discord push (every 2m)** | Hermes Discord integration active | Excellent (mobile-friendly) |
| **Telegram push** | Hermes Telegram integration active | Excellent (always reachable) |
| **Cron-driven** | `hermes cron create` with `every 2m` schedule | Good (but `hermes` CLI unavailable in cron) |

### Cron-Free Streaming (Background Process)

The `hermes` CLI is unavailable in cron subprocesses. For reliable headless streaming, use a background `while` loop via terminal:

```bash
terminal(command="while true; do python3 stream_engine.py; sleep 120; done", background=true)
```

Then deliver chunks via the agent's `send_message` tool on a periodic cron that only verifies engine health and triggers delivery, without needing to call the `hermes` binary.

### iOS-Specific Notes

- **OGG** (.ogg/.opus): Works in Discord, Telegram. NOT supported in Safari/Firefox.
- **MP3**: Works in ALL iOS browsers. Always use `.mp3` + `audio/mpeg` for direct URL streaming.
- **Background Playback**: Discord app keeps playing in background. Safari may pause when tab is inactive.
- **AirPlay**: Cast from Discord or Safari to HomePod/Sonos.

## BandLab Integration

BandLab is a cloud-based DAW that supports collaboration. The agent does NOT directly interact with BandLab — instead:

1. Store BandLab project URL in `BandLab/link.md`
2. Agent provides analysis and suggestions; user applies them in BandLab
3. When user exports a new version, email it back or place it on disk
4. Agent analyzes the revision and creates v2 entry

## Troubleshooting

- **Git auth fails:** PAT may be expired. User must generate a fresh token at github.com/settings/tokens
- **Repo doesn't exist:** Create it manually at github.com/new, then clone and set remote
- **MIDI file not found:** Check if it was emailed — use `himalaya` to download attachments
## Pitfalls

*   **Pathing Error:** Avoid using `/root/projects/` (agent default). Always enforce the canonical path `/opt/data/projects/` for persistence and mirroring.
*   **Cron Alignment:** When configuring cron jobs for composition, explicitly include the absolute path `/opt/data/projects/` in the prompt/task to prevent the agent from defaulting to temporary or root storage.
*   **Artifact Discovery:** If a cron job or script reports success but files are missing from expected paths, search `/root/projects/` and `/tmp/hermes/` as secondary locations before assuming failure.
*   **DSP/Research Pathing Error:** Never place DSP virtual instrument work under `Genres/Research/`. The `Genres/` tree is for composition projects only. DSP/synthesis research always goes to `Research/NNN-project-name/`.** Install with `pip3 install mido --break-system-packages`; use `/usr/bin/python3` not venv
*   **Duplicate repo clones at different names:** If two repos have the same remote (verified via `git -C <path> remote -v`), one is redundant and safe to delete. Check before cleanup: `git -C <repo> remote -v` for both.
*   **Handover repo proliferation:** Dated handover snapshots (e.g. `musicom-agent-handovers-private-20260518194735`) accumulate. They are point-in-time copies of the main handover repo. Safe to delete once the main handover repo is confirmed intact.
*   **config.yaml backup accumulation:** Hermes auto-creates `config.yaml.bak.*` on config changes. Keep max 2 (the 2 newest). Prune with: `ls -t config.yaml.bak.* | tail -n +3 | xargs rm`.
*   **work/ scratch dirs from reorg:** Reorg sessions leave large git objects in `/opt/data/work/`. These can reach 350MB+. Safe to delete after confirming the reorg was completed and pushed. These accumulate 100+ files and become dead weight.
*   **No repo clones inside projects/:** Never clone a GitHub repo into `/opt/data/projects/`. Clones belong in `/opt/data/repos/`. (The `documentation/` subfolder was a rogue clone of `axelwiertz/musicom-agent` — same repo already at `repos/musicom-agent`.)
*   **Loose scripts at root:** Any `.py` helper that isn't project-specific belongs in `/opt/data/scripts/`, not scattered at `/opt/data/` root.
*   **All numbered projects inside Styles/:** Never create a numbered project folder at `/opt/data/projects/` root. It goes under `Styles/{StyleName}/`. (e.g. `016-genre-pattern-dataset` was wrongly placed at root.)
*   **Duplicate root-level copies of repos:** If a repo exists in `repos/`, do not also keep a root-level copy (e.g., `composer-crew-framework/` at `/opt/data/` root). One canonical location only.

## Workspace Hygiene Audit Checklist

Run periodically or before major sessions:

```bash
# Stray numbered projects at projects/ root (should be empty except index.html)
ls /opt/data/projects/*.py /opt/data/projects/[0-9]* 2>/dev/null

# _Backup folders (should not exist)
find /opt/data/projects -type d -name '_Backup'

# Repo clones inside projects/ (wrong)
find /opt/data/projects -maxdepth 2 -name '.git' -type d

# Loose scripts at /opt/data root (should go to scripts/)
ls /opt/data/*.py 2>/dev/null

# Excessive config backups (keep ≤ 2)
ls /opt/data/config.yaml.bak.* | wc -l

# Old work/ scratch dirs
du -sh /opt/data/work/*/
```

See `references/workspace-audit-2026-06-23.md` for the June 2026 audit findings and disposal log.

- `references/git-conflict-resolution-2026-06-17.md` — Steps to resolve `add/add` conflicts in the global `index.html` file.

## Related Skills

- **midi-analysis** — Analyze MIDI files (structure, notes, tempo, key, rhythm)
- **himalaya** — Download MIDI attachments from email
- **github-auth** — Set up GitHub authentication for repo operations
