# Musicom repo map (discovered during Phase 0–2 rehab)

## Env
- Python: `/opt/data/micromamba/envs/musicom/bin/python`
- Package `musicom` 0.1.0, editable install, FLAT layout.
- SoundFont: `TimGM6mb.sf2` via `/opt/data/micromamba/envs/musicom/bin/fluidsynth`.
- Repo root: `/opt/data/repos/musicom`.

## Import rules
- Flat: `from structures import MusicUnit, MusicEvent, UnitMatrix, MidiInstrument`
- `from workflows.unitmatrix_composer import UnitMatrixComposer, create_note_unit, create_chord_unit, create_empty_unit, create_blues_form_matrix`
- Legacy alias (works via `musicom_compat.pth`): `from musicom.ai.core.tet_system import ...`
- NEVER `from ..structures import ...` (beyond-top-level error under flat layout).
- `import musicom` is an alias namespace only — do NOT expect `from musicom import UnitMatrix`.

## Core model
- Time is ABSOLUTE ticks: `MusicEvent(pitch, volume, start_tick, end_tick)`.
- `UnitMatrix`: rows=voices, cols=sections, cells=`MusicUnit`. All rows MUST be equal length (zero-drift invariant).
- Standard: `ticks_per_beat=480`, `beats_per_bar=4` → BAR = 1920 ticks.
- `MusicUnit` has NO `append()` — use `add_event(MusicEvent(...))`.

## The one true composition workflow
```
create_matrix(num_voices, num_sections)
  -> add_voice(name, program=MidiInstrument.X, channel=N)
  -> add_section(name, bars=N)
  -> set_unit((row,col), unit) / fill_voice_section(voice, section, unit)
  -> validate()   # (True, "OK") — zero-drift gate, MUST pass
  -> to_midi(path)
```
Tempo meta in track 0. Percussion = channel 9.

## Cell helpers (workflows.unitmatrix_composer)
- `create_note_unit(pitch, duration_ticks, start_tick=0)`
- `create_chord_unit([p1,p2,p3], duration_ticks, start_tick=0)`
- `create_empty_unit(duration_ticks)` — silent rest, pitch=0
- `create_blues_form_matrix(bpm=80, num_bars=12)` → (composer, info dict)

## MidiInstrument program numbers
PIANO=1, CHURCH_ORGAN=20, ACOUSTIC_GUITAR=25, BASS=33, VIOLIN=41,
STRING_ENSEMBLE=49, TRUMPET=57, FLUTE=74, SYNTH_PAD=88.
MidiPercussion (ch 9): BASS_DRUM=36, ACOUSTIC_SNARE=38, CLOSED_HI_HAT=42,
CRASH_CYMBAL=49, RIDE_CYMBAL=51, LOW_TOM=45.

## Render MIDI → audio
```bash
PY=/opt/data/micromamba/envs/musicom/bin
$PY/fluidsynth -ni -g 1.2 -F out.wav TimGM6mb.sf2 out.mid   # -g 1.2 prevents decay-tail truncation
ffmpeg -y -i out.wav out.ogg
```

## Test suite state (as of Phase 2)
- Green: `tests/test_docs_smoke.py`, `tests/test_phase2_bugfixes.py`, `tests/test_project.py` (17 total).
- Pre-existing debt (Phase 3 targets): `test_structures.py` (stale `MusicPitch`, `MusicRhythmPattern` signature), and collection errors in `test_generators.py`, `test_transformators.py`, `test_visualization.py` (stale symbol imports).
- Run true count: `pytest tests/ -q --continue-on-collection-errors`.

## Fixed bugs (Phase 2)
- `MusicEvent.duration`: was 0 when start_tick==0 (bad `and` guard) → now `end_tick - start_tick`.
- `Counterpoint.has_crossing_voices()`: inverted logic → correct both-direction crossing detection.
- `chain.py` + `stochastic.py`: phantom `unit.append(...)` → `add_event(MusicEvent(..absolute ticks..))`.
- `utilities/config.py` DEFAULT_PATH: Windows path → `tempfile.gettempdir()/Music`.
- `transformers/__init__.py` `__all__`: removed dead entries `'matrix.py'`, `'invert'`, `'retrograde'`.
