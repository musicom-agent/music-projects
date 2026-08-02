---
name: github-repo-management
description: "Clone/create/fork repos; manage remotes, releases."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Repositories, Git, Releases, Secrets, Configuration]
    related_skills: [github-auth, github-pr-workflow, github-issues]
---

# GitHub Repository Management

Create, clone, fork, configure, and manage GitHub repositories. Each section shows `gh` first, then the `git` + `curl` fallback.

## References
- `references/github-api-cheatsheet.md` (GitHub API curl references)
- `references/multi-repo-audit.md` (fragmented repositories cleanup)
- `references/secret-leak-remediation.md` (remediation workflow for GitGuardian alerts/secrets committed)

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)

### Setup

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

# Get your GitHub username (needed for several operations)
if [ "$AUTH" = "gh" ]; then
  GH_USER=$(gh api user --jq '.login')
else
  GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")
fi
```

If you're inside a repo already:

```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

---

## User/Repo Context Pitfall

Before asking the user for GitHub owner/org details, inspect available memory, session history, local remotes, and `git ls-remote` access. In the Musicom workflow, the stable account is `musicom-agent`; `musicom-agent/music-projects` is the project portfolio repo and `axelwiertz/musicom-agent` is the handover/docs repo.

Do not invent non-existent tool calls for repository edits. This environment may only expose generic terminal/process tools plus skills; use `git`, `gh`, or `curl` commands from this skill.

## Orphan Repo Merge Pitfall (Import Rewriting)

When merging an orphan package into a subpackage (e.g. `musicom_ai` → `musicom/ai/`), the orphan's internal imports point to its old top-level namespace. These will break at runtime unless rewritten. After copying the files, run:

```bash
find ai/ -name '*.py' -not -path '*__pycache__*' \
  -exec sed -i 's/from musicom_ai\./from musicom.ai./g' {} + \
  -exec sed -i 's/import musicom_ai/import musicom.ai/g' {} +
```

Also check for hardcoded logger strings (`logging.getLogger('musicom_ai')`) — these are not import statements and won't be caught by the sed patterns above. See `references/multi-repo-audit.md` Step 6 for the full workflow.

## 1. Cloning Repositories

Cloning is pure `git` — works identically either way:

```bash
# Clone via HTTPS (works with credential helper or token-embedded URL)
git clone https://github.com/owner/repo-name.git

# Clone into a specific directory
git clone https://github.com/owner/repo-name.git ./my-local-dir

# Shallow clone (faster for large repos)
git clone --depth 1 https://github.com/owner/repo-name.git

# Clone a specific branch
git clone --branch develop https://github.com/owner/repo-name.git

# Clone via SSH (if SSH is configured)
git clone git@github.com:owner/repo-name.git
```

**With gh (shorthand):**

```bash
gh repo clone owner/repo-name
gh repo clone owner/repo-name -- --depth 1
```

## 2. Creating Repositories

**With gh:**

```bash
# Create a public repo and clone it
gh repo create my-new-project --public --clone

# Private, with description and license
gh repo create my-new-project --private --description "A useful tool" --license MIT --clone

# Under an organization
gh repo create my-org/my-new-project --public --clone

# From existing local directory
cd /path/to/existing/project
gh repo create my-project --source . --public --push
```

**With git + curl:**

```bash
# Create the remote repo via API
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{
    "name": "my-new-project",
    "description": "A useful tool",
    "private": false,
    "auto_init": true,
    "license_template": "mit"
  }'

# Clone it
git clone https://github.com/$GH_USER/my-new-project.git
cd my-new-project

# -- OR -- push an existing local directory to the new repo
cd /path/to/existing/project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/$GH_USER/my-new-project.git
git push -u origin main
```

To create under an organization:

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/orgs/my-org/repos \
  -d '{"name": "my-new-project", "private": false}'
```

### From a Template

**With gh:**

```bash
gh repo create my-new-app --template owner/template-repo --public --clone
```

**With curl:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/template-repo/generate \
  -d '{"owner": "'"$GH_USER"'", "name": "my-new-app", "private": false}'
```

## 3. Forking Repositories

**With gh:**

```bash
gh repo fork owner/repo-name --clone
```

**With git + curl:**

```bash
# Create the fork via API
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo-name/forks

# Wait a moment for GitHub to create it, then clone
sleep 3
git clone https://github.com/$GH_USER/repo-name.git
cd repo-name

# Add the original repo as "upstream" remote
git remote add upstream https://github.com/owner/repo-name.git
```

### Keeping a Fork in Sync

```bash
# Pure git — works everywhere
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

**With gh (shortcut):**

```bash
gh repo sync $GH_USER/repo-name
```


## Repository Strategy Confirmation

When managing multiple repositories or reorganizing their purpose, explicitly confirm the intended role of each repository with the user. Verify existing ownership and collaboration status to ensure the correct repositories are modified or utilized.

### Special: Musicom Project Tiers

The Musicom ecosystem is strictly divided into three tiers:
1. **Core Library:** `axelwiertz/musicom`. Pure Python package. Subpackages include `ai/`, `analysis/`, `converters/`, `generators/`, `rules/`, `structures/`, `transformers/`, `utilities/`, `visualization/`.
2. **Project Portfolio:** `musicom-agent/music-projects`. Numbered composition folders (e.g., `030-balfolk-suite/`) containing MIDI, Audio, Analysis, and VoltAgent dashboards.
3. **Agent Workspace:** `musicom-agent/musicom-agent`. Internal skills, docs, and handover artifacts.

**Rule:** Do not mix portfolio projects into the library repo or library code into the project portfolio. 

## Multi-Repo Audit & Consolidation
Large musicom/framework projects often suffer from repo fragmentation. Follow the systematic workflow:
1. **Discovery**: Use `ls /opt/data/repos` and `git remote -v` to map the landscape.
2. **Comparison**: Check `pyproject.toml` and directory trees to find overlapping "library" code vs "agent" cruft.
3. **Local Cleanup**: Remove non-library files (cron scripts, mailers, tarballs, release.html) before merging.
4. **Merge & Fix**: Use `cp -a` to merge sub-packages, then perform a global `sed` or Python replacement on import strings (e.g., `musicom_ai` -> `musicom.ai`). Check `__init__.py` in the root and in the merged subpackage for namespace exports.
5. **Update Build System**: Add the new subpackages to the `packages` list in `pyproject.toml`.
6. **Archive**: Once merged, archive orphan repos via GitHub API or CLI to prevent further drift.

### Import Rewriting Script
Use this for bulk updates after a merge:
```bash
find ai/ -name "*.py" -not -path "*__pycache__*" -exec sed -i "s/from musicom_ai\./from musicom.ai./g" {} +
find ai/ -name "*.py" -not -path "*__pycache__*" -exec sed -i "s/import musicom_ai/import musicom.ai/g" {} +
```
Also verify logger namings (`logging.getLogger("musicom.ai")`) and docstrings.

### Pitfalls & Troubleshooting
- **Dubious Ownership**: Git may block operations on repos owned by `root`. Use `chown -R hermes:hermes .` to fix before acting.
- **Stale Credentials**: GitHub PATs in `.git-credentials` may expire. If `gh` is missing, verify token validity with `curl -I -H "Authorization: token $TOKEN" https://api.github.com/user`.
- **Pages 404**: If a repo's GitHub Pages shows 404, it likely isn't enabled in settings or is pointing to the wrong branch/path. Check `GET /repos/{owner}/{repo}/pages`.

