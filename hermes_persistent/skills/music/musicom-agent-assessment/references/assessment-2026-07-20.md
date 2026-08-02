# Worked example — assessment run 2026-07-20

First application of this skill. Full report written to
`/opt/data/projects/Research/CompositionMethods/agent_assessment_2026-07-20.md`.

## Verified findings (real probe output)
- `import musicom` OK but **namespace shell, zero top-level exports** (`__file__=None`, path `/opt/data/repos/musicom/musicom`).
- `from musicom import UnitMatrix` → FAIL. `from musicom.workflows...` → FAIL (no such module).
- `pip show musicom` → not installed. No `pip install -e .` in env `musicom`.
- pytest → **not installed in env** → test suite cannot run, coverage claims unverifiable.
- Examples import via `sys.path` hack + bare `from workflows` / `from structures` → competing layout vs the empty `musicom/musicom/` namespace dir.
- README + QUICK_REFERENCE document a **phantom API** (Note/Chord/Sequence/MIDIHandler) that does not match actual MusicEvent/MusicUnit/UnitMatrix.
- git: 9 modified + ~10 untracked new files (vocal_synth, daw_sync, visualizer, musicxml, audio, melodica_adapter) uncommitted.
- Render chain works: outputs/ has v1–v7 MIDI+WAV+OGG triplets. Output convention obeyed.
- Ecosystem sprawl: 9 repos (musicom, musicom-agent, musicom-api-backend, musicom-web-portal, composer-crew-framework, DiffSinger_main, musicom_framework, musicom_platform). composer-crew-framework duplicated 3×.
- Bugs from `plans/architecture-review.md` still unfixed: inverted `Counterpoint.has_crossing_voices()`, Markov `unit.append()` crash, missing `transformers/retrograde.py`, Windows path in `utilities/config.py`.

## Plan shape delivered (6 phases)
- P0 Stabilize: `pip install -e .`, install pytest, commit WIP. (blocks all)
- P1 Truth in docs: regen README/QUICK_REF from real code + add `AGENTS.md`.
- P2 Bug fixes: 4 known bugs, one edit + one test each.
- P3 Test harness: golden-file MIDI hash (proves zero-drift) + non-empty artifact guard (encodes the empty-file pitfall).
- P4 Missing links: grid visualizer (█/░), vocal guide synth, MTC bridge — all currently spec-only in `musicom-missing-link-plan`.
- P5 Companion: paradigm-compare command (Stochastic/Rules/Nature-led) + provenance.json tags.

## Lesson
The single highest-value finding was structural, not musical: the package is not installable/importable and docs lie. A flash model reading the docs to compose would fail immediately. Foundation checks (install/import/test/git/doc-drift) outrank feature review — always Phase 0 them.
