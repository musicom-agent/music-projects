# Packaging & Imports — the working fix (2026-07-20)

Reproduction of the Phase-0 packaging fix that made musicom installable and
importable cwd-independently. Copy with modifications.

## Symptom
- `import musicom` "succeeds" but exposes zero symbols (namespace shell).
- `from musicom import UnitMatrix` / `from musicom.workflows...` → ImportError.
- `pip show musicom` → not installed.
- Examples only run from repo root via `sys.path` hacks (`from workflows import ...`).
- Root cause: `[tool.setuptools.packages.find] include = ["musicom*"]` matched
  NOTHING — real code lives in flat top-level dirs, no `musicom/` package. A
  stray `musicom/` dir held only a junk symlink `ai -> ../ai`.

## Fix 1 — pyproject.toml (flat-layout discovery)
```toml
[project.optional-dependencies]
dev = ["pytest", "pytest-cov"]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

# Flat layout: each top-level dir is its own importable package.
[tool.setuptools.packages.find]
where = ["."]
include = [
    "ai*", "analysis*", "converters*", "generators*", "rules*",
    "structures*", "transformers*", "utilities*", "visualization*",
    "workflows*",
]
exclude = ["musicom*", "tests*", "examples*", "projects*", "research*"]
```
Do NOT also add `[tool.setuptools.packages]` — it conflicts with
`packages.find` and raises `TOMLDecodeError: Cannot overwrite a value`.

## Fix 2 — delete stray shell + convert bad relative imports
```bash
cd /opt/data/repos/musicom
rm -rf musicom/            # junk namespace shell (only held ai symlink)
```
Convert every beyond-top-level import to flat absolute. Find them with a
content search for `from \.\.\w+`. In this repo there were exactly 3:
- `rules/counterpoint.py`:  `from ..structures.unit import MusicUnit` → `from structures.unit import MusicUnit`
- `rules/progression.py`:   `from ..structures.base import Base`     → `from structures.base import Base`
- `structures/pitchclass.py`: `from ..utilities.helpers import ...`  → `from utilities.helpers import ...`

## Fix 3 — legacy `musicom.` alias (keep both styles alive)
The `ai/` subtree + `research_*` examples import `from musicom.ai.core...`.
Rather than mass-rewrite, install a runtime meta-path alias so `musicom.<pkg>`
resolves to the flat `<pkg>`.

`<site-packages>/musicom_compat.py`:
```python
import importlib, sys, types
_FLAT = ("ai","analysis","converters","generators","rules",
         "structures","transformers","utilities","visualization","workflows")
def _install():
    if "musicom" in sys.modules: return
    pkg = types.ModuleType("musicom"); pkg.__path__ = []
    sys.modules["musicom"] = pkg
    class _Finder:
        def find_module(self, fullname, path=None):
            return self if fullname == "musicom" or fullname.startswith("musicom.") else None
        def load_module(self, fullname):
            if fullname in sys.modules: return sys.modules[fullname]
            if fullname == "musicom": return sys.modules["musicom"]
            target = fullname[len("musicom."):]
            if target.split(".",1)[0] not in _FLAT: raise ImportError(fullname)
            mod = importlib.import_module(target); sys.modules[fullname] = mod; return mod
    sys.meta_path.append(_Finder())
_install()
```
Register it (a `.pth` line starting with `import` executes at interpreter start):
```bash
SP=/opt/data/micromamba/envs/musicom/lib/python3.11/site-packages
echo "import musicom_compat" > "$SP/musicom_compat.pth"
```

## Install + verify
```bash
cd /opt/data/repos/musicom
/opt/data/micromamba/envs/musicom/bin/pip install -e ".[dev]"
cd /tmp   # verify from OUTSIDE repo root — catches cwd-dependent passes
PY=/opt/data/micromamba/envs/musicom/bin/python
$PY -c "from structures import MusicUnit; from workflows.unitmatrix_composer import UnitMatrixComposer; print('FLAT OK')"
$PY -c "import musicom; from musicom.ai.core.tet_system import PitchClass; from musicom.structures import MusicUnit; print('NAMESPACED OK')"
$PY -c "import ai,analysis,converters,generators,rules,structures,transformers,utilities,visualization,workflows; print('ALL 10 OK')"
```
Expected: `FLAT OK`, `NAMESPACED OK`, `ALL 10 OK`. ALSA stderr noise is harmless — filter with `| grep -v ALSA`.

## Baseline note
After the fix, `pytest tests/ -q --co` collected 9 tests with 3 file-level
collection errors from stale symbol imports (`MusicPitch`). Tests-collect ≠
tests-pass; the stale symbols are Phase-3 cleanup.
