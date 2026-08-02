# Dual import compat: flat + legacy namespace

Problem: a repo has two historical import styles that must both keep working:
- flat absolute (core engine): `from structures import MusicUnit`
- legacy namespace (merged subtree): `from pkg.ai.core import ...`

Flat is made importable by the editable install (packages enumerated in
`pyproject.toml`). The legacy `pkg.` prefix needs a runtime alias.

## Solution: `.pth` + meta-path finder

A `.pth` line beginning with `import` executes at interpreter startup. Point it
at a tiny module that installs an `importlib` finder mapping `pkg.<flat>` →
flat `<flat>`.

### 1. Module in site-packages (`<env>/lib/pythonX/site-packages/pkg_compat.py`)
```python
import importlib, sys, types

_FLAT = ("ai", "structures", "generators", "rules", "workflows")  # real top dirs

def _install():
    if "pkg" in sys.modules:
        return
    p = types.ModuleType("pkg")
    p.__path__ = []          # marks it a package
    sys.modules["pkg"] = p

    class _Finder:
        def find_module(self, fullname, path=None):
            return self if fullname == "pkg" or fullname.startswith("pkg.") else None
        def load_module(self, fullname):
            if fullname in sys.modules:
                return sys.modules[fullname]
            if fullname == "pkg":
                return sys.modules["pkg"]
            target = fullname[len("pkg."):]
            if target.split(".", 1)[0] not in _FLAT:
                raise ImportError(fullname)
            mod = importlib.import_module(target)
            sys.modules[fullname] = mod
            return mod

    sys.meta_path.append(_Finder())

_install()
```

### 2. The `.pth` (`<site-packages>/pkg_compat.pth`)
```
import pkg_compat
```

## Gotchas
- A `.pth` CANNOT alias a name on its own — it can only add paths or run an
  `import` line. The name aliasing must happen in the imported module.
- `find_module`/`load_module` is the legacy finder API; it still works on
  3.11. Pyright will warn it doesn't satisfy `MetaPathFinderProtocol`
  (`find_spec` missing) — harmless noise.
- Do NOT try to do this via `[tool.setuptools.package-dir]` + `packages.find`
  together — the two TOML tables conflict and setuptools errors out.
- Reinstall editable (`pip install -e ".[dev]"`) after changing pyproject so
  the metadata refreshes; the `.pth` is independent and persists.

## Verify
From a neutral cwd (not the repo root):
```bash
python -c "from structures import MusicUnit; print('flat ok')"
python -c "import pkg; from pkg.ai.core.tet_system import PitchClass; print('legacy ok')"
```
