# Musicom Repo Engineering Notes

Durable engineering facts for working on the `musicom` codebase. These are
design decisions and reusable procedures, not transient environment failures.

## Package layout: FLAT (top-level dirs ARE packages)

The repo does NOT nest code under a `musicom/` package. The importable
packages are the top-level directories themselves:

```python
from structures import MusicUnit, MusicEvent, UnitMatrix, MidiInstrument
from workflows.unitmatrix_composer import UnitMatrixComposer, create_note_unit
```

Rules:
- ✅ flat absolute: `from structures import ...`, `from workflows.x import ...`
- ✅ legacy `from musicom.ai.core... import ...` works via a compat alias
- ❌ never `from ..structures import ...` → raises "attempted relative import
  beyond top-level package" under flat layout. Convert any `..pkg` cross-package
  import to flat absolute (`from structures.base import Base`).
- ❌ `from musicom import UnitMatrix` does NOT work — `musicom` is an alias
  namespace only, not a re-exporting package.

## Packaging fix pattern (flat-layout setuptools)

Symptom that hides for a long time: `import musicom` "succeeds" as an empty
namespace package, `pip show musicom` says not installed, every entrypoint
relies on `sys.path.insert` hacks + a bare-cwd run.

Root cause seen here: `pyproject.toml` had
`[tool.setuptools.packages.find] include = ["musicom*"]` which matched NOTHING
because the real code is in flat top-level dirs.

Fix:
1. `[tool.setuptools.packages.find]` with `where=["."]` and `include=[...]`
   listing each real top-level package (`ai*`, `structures*`, `workflows*`, ...),
   `exclude=["tests*","examples*",...]`.
2. Add `[project.optional-dependencies] dev = ["pytest","pytest-cov"]`.
3. `pip install -e ".[dev]"`.
4. Remove any stray inner `musicom/` symlink-shell dir that created the empty
   namespace illusion.
5. To keep a legacy `from musicom.<pkg>...` import style alive without moving
   code: ship a runtime alias module + a `.pth` in site-packages that installs
   a `meta_path` finder mapping `musicom.<flat>` → the flat top-level package.
6. Verify imports from a NEUTRAL cwd (e.g. `/opt/data`, not the repo root) to
   prove cwd-independence — running from repo root masks the bug.

Do NOT reintroduce a nested `musicom/` package dir as the "fix"; that fights the
flat layout and the examples. Keep flat; alias for compatibility only.

## Docs-truth workflow (verify BEFORE documenting)

Musicom docs (README, QUICK_REFERENCE) drifted badly: they documented a
fictional API (Note/Chord/Scale/MelodyGenerator/MIDIHandler/Sequence) that does
not exist. Any agent trusting the docs writes code that fails and produces empty
files.

Procedure to regenerate docs safely:
1. Read the REAL signatures from source before writing a single doc line:
   `structures/unit.py`, `structures/__init__.py`,
   `workflows/unitmatrix_composer.py`, `structures/matrix.py`,
   `structures/instrument.py`.
2. Write one runnable verification script exercising every snippet you intend to
   document; run it from a neutral cwd; fix docs to match ACTUAL output.
3. Land the verification as a repo test (`tests/test_docs_smoke.py`) so docs
   cannot silently drift again — this is the durable guard.
4. Document real quirks truthfully instead of asserting the "nice" value.

Verified quirks found (candidates for a code fix, but document until fixed):
- `MusicEvent.duration` returns **0** when `start_tick == 0` (guard is
  `start!=0 and end!=0` in `structures/unit.py`). `MusicUnit([...start=0...]).durations`
  → `[0, 480, 480]`, not `[480, 480, 480]`. Compute `end-start` yourself if needed.
- A valid 1-bar 2-track MIDI is ~80 bytes; empty/corrupt files are 16–22 bytes.
  Use `assert os.path.getsize(path) > 40` as the non-empty guard, not `> 100`.
- Known-broken tests: `test_generators.py`, `test_transformators.py`,
  `test_visualization.py` fail COLLECTION on stale symbol `MusicPitch`.
