# Workspace Audit — June 23, 2026

## Trigger
Full review of `/opt/data/projects/` and `/opt/data/repos/` before a model switch.
Looked for: duplicate clones, stale backups, misplaced scripts, config bloat, dead repos.

## Findings & Disposal

### Deleted (~2GB reclaimed)

| Path | Size | Reason |
|------|------|--------|
| `/opt/data/work/reorg-20260530/` | 349MB | Stale May 30 workspace, never cleaned |
| `/opt/data/repos/DiffSinger` | 73MB | Non-main clone, zero references in active skills |
| `/opt/data/repos/musicom_ai` | ~800K | Merged into axelwiertz/musicom per June 20 consolidation |
| `/opt/data/repos/musicom_research` | ~400K | Same — merged |
| `/opt/data/repos/musicom_repos` | 4K | Empty shell |
| `/opt/data/repos/musicom-agent-handovers-private-20260518194735` | 220K | Dated snapshot, superseded |
| `/opt/data/repos/handover_repo` | 2.3M | Redundant clone of axelwiertz/musicom-agent |
| `/opt/data/repos/musicom-agent-handover` | 800K | Same remote as handover_repo — both removed |
| `/opt/data/projects/Styles/_Backup/` | 134 files | Git history IS the backup; _Backup folders prohibited |
| 7× `config.yaml.bak.*` | trivial | Kept 2 newest (20260604, 20260620) |

### Reorganized

| Action | Detail |
|--------|--------|
| `projects/documentation/` removed | Rogue clone of axelwiertz/musicom-agent inside projects/; canon at repos/musicom-agent |
| `/opt/data/composer-crew-framework/` removed | Root-level duplicate; repos/composer-crew-framework is canonical |
| `check_mail.py`, `check_mail_all.py`, `check_recent.py`, `fetch_msg13.py` → `scripts/` | Loose scripts moved from /opt/data root |
| `projects/notion_sync.py` → `scripts/` | Same |
| `016-genre-pattern-dataset/` → `projects/Styles/016-genre-pattern-dataset/` | Numbered project was at projects root; moved into Styles/ |
| `Research/CompositionMethods/.telegram_summary.md` + `send_telegram.py` deleted | Stale session artifacts |

### State After Cleanup

- `repos/` retained: DiffSinger_main, composer-crew-framework, musicom, musicom-agent, musicom_framework, musicom_platform
- `projects/` top-level: Knowledge/, Research/, Styles/ + index.html only
- `scripts/` count: 29 files
- Disk: 87% (42G/48G) — DiffSinger_main (1.5GB) is remaining big item, kept for SVS

## Verification Commands
```bash
# Check nothing stray at projects root
ls /opt/data/projects/

# Confirm scripts moved
ls /opt/data/scripts/ | grep -E 'check_mail|notion_sync'

# Confirm no _Backup exists
find /opt/data/projects -type d -name '_Backup'

# Confirm no rogue docs clone
find /opt/data/projects -name '.git' -maxdepth 2 -type d
```
