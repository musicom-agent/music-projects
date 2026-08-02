---
name: python-package-rehabilitation
description: "Rehabilitate a broken/undocumented Python package repo: fix packaging + imports so it installs and imports cwd-independently, make docs match real code, then fix bugs — each phase gated by verified real output. For flat-layout repos, editable-install failures, phantom-API docs, and known-bug backlogs."
version: 1.0.0
author: "Musicom Agent"
metadata:
  hermes:
    tags: [python, packaging, imports, documentation, refactor, testing, workflow]
---

# Python Package Rehabilitation

Bring a neglected/broken Python package back to a state where it installs,
imports from any working directory, has docs that match the code, and has a
regression net. Phased, each phase gated by **real tool output** — never
proceed on assumption.

## When to use
- `pip install -e .` produces an importable package with **no usable exports**, or examples only run via `sys.path` hacks.
- Two competing import layouts coexist (flat top-level dirs vs a `pkg.sub` namespace).
- README / quickstart documents an API that **does not exist** in the code (doc drift).
- A backlog of "known bugs" listed in an architecture-review doc that were never fixed.
- Test suite can't even collect (stale symbols, missing test runner).

## Core principle: verify, don't trust
Every phase ends with a command whose **real** output you paste. If a doc code
block, an import, or a bugfix isn't backed by a passing run, it isn't done.
Source doc examples from a script you actually ran, not from memory of the API.

## Phase 0 — Stabilize packaging & imports (blocks everything)
1. Inspect reality before editing `pyproject.toml`:
   - `search_files(target=files)` for top-level dirs containing `__init__.py` — those are the real packages.
   - Read `[tool.setuptools.packages.find]`. A common breakage: `include = ["pkgname*"]` matching **nothing** because code lives in flat dirs (`structures/`, `workflows/`, ...), not under a `pkgname/` dir.
   - Watch for a stray inner `pkg/` dir that's just symlinks — the "namespace shell" that fools `import pkg` into succeeding with zero exports.
2. Decide ONE canonical layout. Flat (each top dir its own package) usually matches the examples; prefer it — zero code changes to call sites.
3. Fix `include`/`exclude` to enumerate the real flat packages; `exclude` the junk shell + `tests*`/`examples*`. Add a `[project.optional-dependencies] dev = ["pytest", ...]`.
4. `pip install -e ".[dev]"`. Verify imports **from a neutral cwd** (e.g. `/opt/data`, NOT the repo root) so you prove cwd-independence, not an accidental cwd match.
5. Fix cross-package relative imports that break under flat layout: `from ..structures.base import Base` → `from structures.base import Base`. Grep `from \.\.\w+` to find them all (usually few).
6. Keep a legacy `pkg.sub` import style working *alongside* flat via a runtime alias — see `references/dual-import-compat.md`.
7. Commit uncommitted WIP first thing (a rehab often starts on a dirty tree) and again after each phase.

## Phase 1 — Doc truth (cheap, high leverage)
1. Read the ACTUAL signatures from source (`structures/*.py`, `workflows/*.py`, package `__init__.py` `__all__`). Never trust README as the API source.
2. Write ONE end-to-end script exercising the real API. Run it. Fix it until it passes. This script IS the ground truth.
   - Expect to discover real behaviors mid-run (e.g. a `duration` property that returns 0 when `start_tick==0` due to a bad guard). Document them truthfully; log the buggy ones for the bug-fix phase.
3. Replace phantom doc examples with the verified snippets, verbatim.
4. Add an `AGENTS.md` at repo root: env path, canonical import rules (both styles), the one true workflow order, invariants, render/build commands, output-location rule, known quirks, and a "verify-don't-trust" clause. This is the machine-facing entry point; state it wins over README on conflict.
5. Convert the ground-truth script into a **doc-smoke pytest** (`tests/test_docs_smoke.py`) so docs can't silently drift again.

## Phase 2 — Fix known bugs (one edit + one asserting test each)
1. Do NOT trust the bug list blindly — grep the codebase to confirm and to find duplicates the review missed (e.g. a phantom `unit.append()` flagged in one file but present in TWO).
2. Fix, then write a regression test asserting the corrected behavior. One test file `tests/test_phaseN_bugfixes.py`, one test per bug.
3. When a fix changes documented behavior, update the doc-smoke assertion AND the AGENTS quirks section in the same commit — flip "quirk (awaiting fix)" to "✅ fixed".

## Phase 3 — Test harness (regression safety)
- Resurrect non-collecting test files (stale symbol names, changed signatures).
- Golden-file test: deterministic-seed generate → hash output bytes → assert equal on rerun (proves zero-drift / no regression).
- Non-empty artifact guard: after any file write, `assert os.path.getsize(path) > threshold` (empties historically show as 16–22 bytes).
- Run full suite with `--continue-on-collection-errors` to get the true green count when some files still don't collect; report pass/fail/error split and attribute each to a phase.

## Pitfalls
- **cwd-dependent import illusion**: imports "work" only because you're standing in the repo root. Always verify from a neutral directory.
- **Namespace-shell success**: `import pkg` returns a module with `__path__` but no exports. Not the same as installed.
- **`/tmp` may be write-guarded** in some sandboxes — use a scratch dir under the project's designated output area instead.
- **TOML conflict**: you cannot have both `[tool.setuptools.packages.find]` and `[tool.setuptools.packages]`. Pick one.
- **`.pth` cannot alias a name** by itself; use a `.pth` line `import <module>` that runs a tiny module installing a meta-path finder. See references.
- **LSP diagnostics from a different env** are noise — the code runs in the target venv, not the LSP's.
- **Don't over-assert file size**: a valid 1-bar multi-track MIDI can be ~80 bytes. Set the empty-guard threshold low (>40), not >100.

## User conventions (Axel / Musicom)
- Caveman reply style: short technical fragments, no filler, "I" not "me", high accuracy.
- Prefer autonomous, VERIFIED artifacts — paste real command output, never fabricate.
- Zero-drift is sacred: equal-length tracks/rows, absolute-tick timing.
- Composition outputs go under `/opt/data/projects/Research/outputs/<project>/`, never in the repo.
- Commit after each logical phase; push when asked.

## References
- [dual-import-compat.md](references/dual-import-compat.md) — keep flat `from structures import` AND legacy `from pkg.ai import` both working via a site-packages `.pth` + meta-path finder.
- [musicom-repo-map.md](references/musicom-repo-map.md) — the specific musicom flat layout, env path, and canonical composer workflow discovered this session.
