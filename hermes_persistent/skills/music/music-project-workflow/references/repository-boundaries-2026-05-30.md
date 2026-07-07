# Musicom Repository Boundaries — 2026-05-30

## Boundary rule

- `musicom-agent/music-projects`: canonical portfolio/project repo.
  - Numbered project folders: `NNN-project-name/`
  - MIDI, MusicXML, audio renders, stems
  - Project analysis, notes, dashboards
  - Project-local generation scripts
  - Portfolio `index.html`
- `axelwiertz/musicom-agent`: Musicom agent documentation and handover repo.
  - Agent introduction
  - Composer skill docs and references
  - Onboarding/handover notes for other agents
  - Session logs and research notes
  - Framework documentation/prototypes

Do not store generated project portfolio folders inside `axelwiertz/musicom-agent`.

## Session learning

The user corrected the agent after it asked for repo ownership details that were already available in memory/session history. For future repo-boundary tasks, inspect memory, session history, local remotes, and GitHub auth before asking clarifying questions.

## Verification pattern used

```bash
ssh -T git@github.com

git ls-remote git@github.com:musicom-agent/music-projects.git HEAD
git ls-remote git@github.com:axelwiertz/musicom-agent.git HEAD

# Clone clean working copies before large reorg.
git clone git@github.com:musicom-agent/music-projects.git /opt/data/work/reorg-YYYYMMDD/projects
git clone git@github.com:axelwiertz/musicom-agent.git /opt/data/work/reorg-YYYYMMDD/handover

# After commits and pushes, verify local HEAD equals remote main.
git rev-parse --short HEAD
git ls-remote origin main | cut -f1 | cut -c1-7
```

## Reorganization performed

- Pushed `musicom-agent/music-projects` commit `9e70543`: `Reorganize repository as Musicom project portfolio`.
- Pushed `axelwiertz/musicom-agent` commit `42dcec4`: `Refocus repository on Musicom agent handover docs`.
- Added repo-boundary docs to `README.md` and `handover/REPOSITORY_BOUNDARIES.md`.

## Pitfalls

- Avoid asking for GitHub org/user if memory already names the repos.
- Do not attempt imaginary `github_repo_management` tool calls. Use `git`, `gh`, or `curl` per GitHub skills.
- For large reorganizations, clone clean working copies under `/opt/data/work/...` rather than mutating ambiguous nested local repos.
- Remove nested `.git` directories copied from project folders before committing to a parent repo.
