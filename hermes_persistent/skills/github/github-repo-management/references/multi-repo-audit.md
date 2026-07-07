# Multi-Repo Audit & Consolidation

Systematic method for discovering, mapping, and merging related Git repos.

## When to Use

- User says "improve and merge repos" or "consolidate"
- You encounter many clones with unknown relationships
- Need to understand full landscape before planning changes

## Step 1: Map All Local Clones

```bash
find /opt/data/repos/ -maxdepth 1 -type d | sort
```

Check each one:

```bash
for d in /opt/data/repos/*/; do
  echo "=== $d ==="
  cd "$d" && git remote -v 2>/dev/null && \
  echo "Branches:" && git branch -a 2>/dev/null && \
  echo "Recent:" && git log --oneline -3 2>/dev/null
  echo ""
done
```

## Step 2: Identify Redundant/Empty Clones

Look for:
- Same remote across multiple local dirs (duplicate clones)
- Empty dirs (only `.git`, no source files)
- Misnamed clones (e.g. `musicom_framework` pointing to `music-projects`)
- Stale repos with no remote configured

Cross-reference with `find . -not -path './.git/*' -type f | wc -l` to gauge content volume.

## Step 3: Inspect Distinct Content

For each unique remote, examine its package/module structure:

```bash
find . -name '*.py' -not -path './.git/*' -not -path './venv/*' | sort
```

Look for:
- Overlapping module structures (same `generators/`, `rules/`, `structures/`)
- Unique modules present in one repo but not another
- Isolated utility code that should be shared

## Step 4: Propose Consolidation Plan

Use a table format:

| Repo | Role | Content | Action |
|------|------|---------|--------|
| `owner/repo-a` | Core library | structure/ | Keep |
| `owner/repo-b` | AI extension | generators/, io/ | Merge into repo-a |
| `owner/repo-c` | Research | examples/ | Merge into repo-a |

**Merge strategy:**
1. Source → target path mapping (which subdirs go where)
2. Resolve import path conflicts
3. Concatenate `pyproject.toml` dependencies
4. Archive/delete source repos on GitHub after merge
5. Update all skill references to the single repo

## Step 5: Clean Local Cruft Before Pushing

Local clones accumulate operational files (cron scripts, mail checkers, tarballs, release.html dumps, `__pycache__`). Before committing:

```bash
# Check what doesn't belong in the library
git status --short

# Remove operational files
git rm --cached check_assignments.py cron_*.py debug_*.py mail_*.py parse_*.py
git rm --cached *.tar.gz release.html himalaya/
```

**CRITICAL:** Run `git ls-files` on each pattern first — if the files were never tracked (local-only), `git rm --cached` will error. Use `rm -rf <path>` instead for untracked files:

```bash
# Check if files are tracked
git ls-tree -r HEAD --name-only | grep -E "(himalaya|release\\.html|\\.tar\\.gz)"

# If grep returns nothing, they're local-only — just delete
rm -rf himalaya/ himalaya*.tar.gz release.html check_assignments.py
```

## Step 6: Merge Orphan Repos as Subpackages

When consolidating an orphan repo into an existing project:

### 6a. Plan the target namespace

Map source paths to target paths. If the orphan uses a package name like `musicom_ai` but the target is `musicom`, the natural target is `musicom/ai/`:

| Source | Target | Reason |
|--------|--------|--------|
| `musicom_ai/musicom_ai/core/*` | `musicom/ai/core/` | Same domain, different design |
| `musicom_ai/musicom_ai/generators/*` | `musicom/ai/generators/` | New generators not in main |
| `musicom_ai/musicom_ai/io/*` | `musicom/ai/io/` | Novel module (MIDI I/O, audio analysis) |
| `musicom_research/examples.py` | `musicom/examples/research_*.py` | Standalone reference code |

### 6b. Copy, don't move

Work from the target repo:

```bash
cd /opt/data/repos/musicom
cp -a /opt/data/repos/musicom_ai/musicom_ai/* ai/
```

### 6c. Rewrite imports

The orphan's internal imports reference its old top-level package. One `sed` pass fixes everything:

```bash
find ai/ -name '*.py' -not -path '*__pycache__*' \
  -exec sed -i 's/from musicom_ai\./from musicom.ai./g' {} + \
  -exec sed -i 's/import musicom_ai/import musicom.ai/g' {} +
```

Also fix hardcoded logger namespace strings (e.g. `logging.getLogger('musicom_ai')` → `logging.getLogger('musicom.ai')`).

Update docstrings referencing the old package name — these are cosmetic but project the consolidated identity.

### 6d. Remove stale doc references

The orphan's `DOC.md` or `README.md` may mention external tools it doesn't actually use (PyPianoRoll, AIVA, LilyPond, Mingus, Abjad). Strip these — they mislead future developers.

### 6e. Update pyproject.toml

Add every new subpackage to the `[tool.setuptools] packages` list:

```toml
packages = [
    "musicom",
    "musicom.ai",
    "musicom.ai.core",
    "musicom.ai.generators",
    # ... every subpackage depth level
    "musicom.visualization",
]
```

Omitting intermediate subpackages (e.g. `musicom.ai` without `musicom.ai.core`) can cause missing-module errors on install.

### 6f. Update the parent README

Add the new subpackage to the project structure tree, feature list, and examples list. Fix any stale clone URLs (orphan repos often reference `github.com/musicom/musicom` which 404s).

## Step 7: Commit and Push

```bash
git add -A
git status --short   # Verify: no unexpected deletions, no pycache
git commit -m "refactor: consolidate <repo_a> + <repo_b> into main

Phase 1 — Cleanup:
- Remove local-only cruft
- Add .gitignore
- Fix pyproject.toml URLs and stale deps

Phase 2 — Consolidation:
- Merge <repo_a> as musicom/<subdir>/ subpackage
- Merge <repo_b> examples as examples/<name>_*.py"
git push origin main
```

### Pitfall: Ownership Issues

If files are owned by `root`, `chown` may fail. Try without `sudo` first:

```bash
chown -R hermes:hermes .
# If that works, fine. Otherwise try sudo (if available) or skip.
```

## Step 8 (Optional): Archive Source Repos on GitHub

After the merge is pushed, archive the orphan repos so they're read-only:

```bash
# Requires valid GitHub PAT with repo scope
TOKEN="ghp_..."
curl -s -X PATCH \
  -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/owner/orphan-repo \
  -d '{"archived": true, "description": "[ARCHIVED] Merged into owner/target-repo as subpackage"}'
```

If the token is expired or scoped to a different user, archive manually via GitHub web UI → Settings → Archive this repository.

## Pitfalls

- **Ownership issues**: `git config --global --add safe.directory /path/to/repo` needed when repos owned by different users
- **Empty repos that are not `.git` dirs**: Some cloneless dirs may have been created by `mkdir` with no remote at all
- **Submodule ghosts**: Stale submodule references in `.gitmodules` will cause CI failures; use `git rm --cached <path>` to detach
- **Don't delete remotes until confirmed**: Verify destination repo has all unique content before deleting source repos from GitHub
- **pyproject.toml package references**: When merging packages, update `[tool.setuptools.packages]` to include new subpackages