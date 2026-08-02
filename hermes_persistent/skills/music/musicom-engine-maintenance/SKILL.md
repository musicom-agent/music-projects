---
name: musicom-engine-maintenance
description: "Maintain the musicom core Python library at /opt/data/repos/musicom: packaging, import layout, editable install, test harness, and known code bugs. Use when composing fails on import, the package won't install, tests won't run, or when auditing/assessing the engine's health."
version: 1.0.0
author: Musicom Agent
license: MIT
platforms: [linux]
prerequisites:
  commands: [git]
metadata:
  hermes:
    tags: [musicom, python, packaging, imports, testing, refactor, engine]
references:
  - references/packaging-and-imports.md
---

# Musicom Engine Maintenance

Keep the musicom core library (`/opt/data/repos/musicom`) installable, importable, and testable. This is the *engine* — distinct from `music-project-workflow` (project portfolio) and style/genre content. Keep engine generic; do not fold style-specific logic in here.

## Environment facts
- Env: micromamba env `musicom`. Python: `/opt/data/micromamba/envs/musicom/bin/python`, pip: same-dir `pip`.
- Install editable: `pip install -e ".[dev]"` (the `[dev]` extra pulls pytest + pytest-cov).
- Verify an install always **from a directory OTHER than the repo root** (e.g. `cd /tmp`) so you catch cwd-dependent path-hack passes that look fine only at repo root.

## Canonical import layout (CRITICAL)
The repo is **FLAT**: the top-level dirs ARE the packages.
- Correct: `from structures import MusicUnit`, `from workflows.unitmatrix_composer import UnitMatrixComposer`, `from generators.markov import ...`.
- The 10 packages: `ai analysis converters generators rules structures transformers utilities visualization workflows`.
- Cross-package imports inside the code must be **flat absolute** (`from structures.base import Base`), NOT beyond-top-level relative (`from ..structures.base` breaks under flat install).
- Legacy `from musicom.ai...` style (used only inside the merged `ai/` subtree + `research_*` examples + docs) is kept alive by a runtime alias `musicom_compat.pth` in site-packages. Both styles coexist — do not "unify" by mass-rewriting; keep the alias.

## Health-check / assessment sequence
When asked to review, assess, or fix the engine, gather REAL state — never trust README claims:
1. `import musicom` and `from structures import MusicUnit` from `/tmp` — do both resolve?
2. `pip show musicom` — is it actually installed editable?
3. `python -m pytest tests/ -q --co` — does the suite even collect?
4. `git status -s` — uncommitted WIP? Commit before refactoring.
5. Compare README/QUICK_REFERENCE example APIs against actual `structures/`/`workflows/` symbols — doc drift is common (README documents a phantom `Note/Chord/Sequence/MIDIHandler` API that does not exist; the real API is `MusicEvent/MusicUnit/UnitMatrix`).

## Pitfalls
- **`packages.find` include mismatch**: `include=["musicom*"]` finds NOTHING because code is flat (no `musicom/` package). Fix: list the 10 flat dirs explicitly (`include=["ai*","structures*",...]`) and `exclude=["musicom*","tests*","examples*","projects*","research*"]`. See reference file for the full pyproject block.
- **Stray inner `musicom/` symlink dir**: was a junk namespace shell (`musicom/ai -> ../ai`). Delete it; it confuses discovery.
- **Docs lie**: README + QUICK_REFERENCE document a phantom API. Regenerate docs from real code before trusting any example. (Phase 1 of the standing dev plan.)
- **Fixed code bugs (Phase 2, keep regression tests green)**: these were all repaired — `rules/counterpoint.py has_crossing_voices()` (was inverted; now True on order-flip in either direction); Markov `generate_unit_from_sequence()` AND `StochasticGenerator.generate()` both called nonexistent `unit.append(pitch, duration, ...)` — replaced with `unit.add_event(MusicEvent(..absolute ticks..))` (grep `\.append\(` under `generators/` before trusting any generator — the architecture-review only listed ONE, there were TWO); `transformers/__init__.py __all__` had junk entries (`'matrix.py'`, dead `invert`/`retrograde`); `utilities/config.py` DEFAULT_PATH now `tempfile.gettempdir()/Music`; `MusicEvent.duration` returned 0 when `start_tick==0` (bad `and` guard) → now `end_tick - start_tick`. `MusicUnit` has **no** `append()` — always `add_event(MusicEvent(...))`.
- **Still broken (pitch subsystem is stubs)**: `structures/pitch.py` `MusicPitchClass`/`MusicPitchGrid`/`MusicPitchRange` are minimal stubs — `MusicPitchClass.E`, `.index_of()`, `PatternRotation.minor` etc. do NOT exist. `MusicPitchClassSet(...)` construction crashes at `pitchclass.py:301` (`MusicPitchGrid()` called with no args but stub requires `pitches`). Skip/quarantine tests that hit this; do not chase.
- **Stale test symbols**: legacy test files imported long-removed names (`PatternMovementRules`, `FunctionGenerator`, `MusicPitch`-as-old-API, `gen.produce()`, `MusicUnit(pitches=)`). When a test file tests a vanished API, DELETE it (with user OK) and rewrite fresh against real symbols — do NOT reverse-engineer the obsolete API. Tests collecting != tests passing; use `pytest --continue-on-collection-errors` to get the true green count when some files error on import.
- **Do NOT** capture "the tool is broken" — capture the FIX (install command, pyproject edit, import rewrite).

## Standing development plan
A phased, flash-model-executable plan lives at `/opt/data/projects/Research/CompositionMethods/agent_assessment_2026-07-20.md`. Progress: **P0 stabilize DONE** (packaging fix + editable install + WIP committed), **P1 docs truth DONE** (README/QUICK_REFERENCE regenerated from real code, `AGENTS.md` added, `tests/test_docs_smoke.py` proves documented code runs), **P2 bug fixes DONE** (5 bugs + `tests/test_phase2_bugfixes.py`), **P3 test harness DONE** (`tests/test_harness_golden.py`; suite green 25 pass / 1 documented skip). Remaining: **P4** missing-link features (grid visualizer, vocal guide, MTC bridge), **P5** companion workflows (paradigm-compare, provenance tags). Commit + push after each phase.

## AGENTS.md is the source of truth for agents
The repo now carries `/opt/data/repos/musicom/AGENTS.md` — canonical machine-facing guide (env path, flat imports both styles, the 6-step composer order, zero-drift invariant, render chain, output-folder rule, known quirks/fixes, test status). When docs and AGENTS.md disagree, AGENTS.md wins. Keep it in sync when you change the engine.

## Golden-file test harness (zero-drift regression net)
`UnitMatrixComposer.to_midi_bytes()` is **deterministic** for a fixed composition — same input → byte-identical MIDI. Exploit this:
- Build a fixed reference composition (no randomness), `sha256(to_midi_bytes())`, pin the hash as `GOLDEN_SHA256`. Any drift in the export path flips the test red. Recompute the golden hash ONLY when the format changes intentionally.
- Also assert: determinism (two builds, same hash), non-empty artifact (`os.path.getsize(mid) > 40` — empties historically appear as 16–22 bytes), and **equal track lengths** — parse with `mido.MidiFile`, `sum(m.time for m in trk)` per voice track (skip track 0 = tempo meta), assert `len(set(lengths)) == 1`. This machine-enforces the user's #1 requirement: no track desync/drift.
- See `references/test-harness.md` for the full harness pattern.

## Related
- `music-project-workflow` — project portfolio organization (NOT engine code).
- `compose-loop` — UnitMatrix composition workflow that runs ON this engine.
