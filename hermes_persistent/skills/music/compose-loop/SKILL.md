---
name: compose-loop
description: "Rapid 4/8/16-bar loop composition using the musicom UnitMatrix engine. Zero-drift guaranteed."
version: 2.0.0
author: Axel Wiertz
license: MIT
platforms: [linux]
prerequisites:
  env_vars: []
  commands: [/opt/data/micromamba/envs/musicom/bin/python, /opt/data/micromamba/envs/musicom/bin/fluidsynth, ffmpeg]
dependencies: []
metadata:
  hermes:
    tags: [music, composition, generative, MIDI, musicom, loop, zero-drift]
    related_skills: [musicom-theory-kb, music-companion-role-spec, musicom-missing-link-plan]
triggers:
  - compose loop
  - generate loop
  - 4-bar pattern
  - 8-bar pattern
  - 16-bar pattern
  - rapid composition
  - music loop
---

# Compose Loop — Rapid Pattern-Centric Composition (v2)

## CRITICAL: use the musicom engine, never raw mido

The musicom package is installed editable. Imports resolve from any cwd.
Do NOT use `sys.path.insert(...)`, do NOT construct `mido.MidiTrack()` manually.

**Python env:** `/opt/data/micromamba/envs/musicom/bin/python`

### Required imports

```python
from structures import MusicUnit, MusicEvent, UnitMatrix, MidiInstrument, MidiPercussion
from workflows.unitmatrix_composer import (
    UnitMatrixComposer, create_note_unit, create_chord_unit, create_empty_unit,
)
from ai.utils.visualizer import write_grid_visualization
from workflows.provenance import write_provenance, AI_ASSISTED
```

### The only sanctioned workflow

```python
composer = UnitMatrixComposer(bpm=BPM, ticks_per_beat=480, beats_per_bar=4)
composer.create_matrix(num_voices=N, num_sections=M)
composer.add_voice("Lead", program=MidiInstrument.FLUTE, channel=0)
composer.add_voice("Drums", program=0, channel=9)  # percussion channel
composer.add_section("A", bars=4)
composer.fill_voice_section("Lead", "A", melody_unit)
composer.fill_voice_section("Drums", "A", drum_unit)
ok, msg = composer.validate()     # MUST be True — zero-drift gate
composer.to_midi(out_path)
```

**Order:** `create_matrix → add_voice → add_section → fill_voice_section → validate → to_midi`.

## Building MusicUnits

```python
# From explicit events (absolute ticks)
BAR = 480 * 4   # 1 bar at 480 tpb, 4/4
melody = MusicUnit(events=[
    MusicEvent(pitch=60, volume=90, start_tick=0, end_tick=480),
    MusicEvent(pitch=62, volume=90, start_tick=480, end_tick=960),
    ...
])

# From generators
from generators.stochastic import StochasticGenerator
from generators.schillinger import SchillingerGenerator
from generators.tendency_masking import TendencyMaskingGenerator
from generators.markov import MarkovGenerator
```

### Unit operations (in-place)
```python
melody.transpose(12)    # up octave
melody.retrograde()     # reverse
melody.invert(60)       # mirror around C4
melody.augment(2.0)     # stretch durations x2
```

## Rendering MIDI → Audio

```bash
PY=/opt/data/micromamba/envs/musicom/bin
$PY/fluidsynth -ni -g 1.2 -F out.wav TimGM6mb.sf2 out.mid
ffmpeg -y -i out.wav out.ogg
```

**FluidSynth IS installed.** Gain `-g 1.2` prevents decay tail truncation.

## Output location & structure (hard rule)

- **Research experiments** → `/opt/data/projects/Research/outputs/<project>/`
- **Style compositions** → `/opt/data/projects/Styles/<Style>/<project>/` (MIDI/, Audio/, etc. in-project)

```
<project>/
├── <name>.mid
├── <name>.wav / .ogg
├── grid_visualization.txt
├── <name>.mid.provenance.json
└── README.md (optional)
```

## Verify-don't-trust (mandatory)

```python
import os
assert os.path.getsize(midi_path) > 40, "empty/corrupt — regenerate"
```

## Visualize before trusting

```python
from ai.utils.visualizer import write_grid_visualization
write_grid_visualization(composer.matrix, f"{out_dir}/grid_visualization.txt",
                         ticks_per_character=240, voice_names=["Lead","Bass"], bpm=BPM)
```

## Provenance sidecar

```python
from workflows.provenance import write_provenance, AI_ASSISTED
write_provenance(midi_path, AI_ASSISTED, "compose-loop/<project>",
                 parameters={"bpm": BPM, "key": "C major"})
```

## Run preflight before finishing

```bash
/opt/data/micromamba/envs/musicom/bin/python \
  /opt/data/projects/Research/preflight_check.py <your_project_dir>
```

Exit 0 = compliant. Non-zero = fix violations.

## Starter template

Copy `/opt/data/projects/Research/_TEMPLATE/` for a ready-to-fill scaffold.

## When NOT to use

- Full songs with vocals → use `songwriting-and-ai-music`
- Complex orchestral scores → use the same engine with more voices/sections
- Analysis-only tasks → `mido` import for reading is fine (not authoring)

## Pitfalls (verified)

- `MusicUnit` has NO `append()` — use `add_event(MusicEvent(...))`
- Percussion = channel 9, program 0. Use `MidiPercussion.BASS_DRUM` etc.
- `MusicEvent.duration` = `end_tick - start_tick` (fixed; works at start_tick=0 now)
- All rows in UnitMatrix MUST have equal total length — `validate()` catches drift
- Avoid `UnitMatrix(voices=4, sections=1)` — use `UnitMatrix(shape=(4, 1))`
- `MusicPitchClassSet` construction currently broken (pitchclass.py:301 stub bug) — avoid for now; use explicit pitch lists instead
- **MidiInstrument enum is limited** — only 10 values: `ACOUSTIC_GUITAR, BASS, CHURCH_ORGAN, FLUTE, PERCUSSION, PIANO, STRING_ENSEMBLE, SYNTH_PAD, TRUMPET, VIOLIN`. No `DISTORTION_GUITAR`, `ELECTRIC_PIANO`, `ELECTRIC_BASS_FINGER`, `SYNTH_BASS_1`, `SQUARE_LEAD`, `WARM_PAD`. Use `TRUMPET` for brass leads, `PIANO` for keys, `BASS` for bass. For GM program numbers not in enum, pass raw int (e.g. `program=30` for distortion guitar, `program=38` for synth bass 1, `program=80` for square lead, `program=89` for warm pad).
- **FluidSynth timeout on large compositions** — 32-bar compositions with 4+ voices can timeout during MIDI→WAV rendering (180s limit). Symptoms: command times out, WAV file is huge (4GB+), MIDI file is small (11KB). Workaround: skip audio rendering for multi-section compositions, or render in background with `notify_on_complete=True`. Verify MIDI is valid first: `assert os.path.getsize(midi_path) > 40`.
- **Section splitting requires tick offset** — when splitting a long event list into two sections (A and B), events in section B have absolute ticks starting at `SECTION`. Must offset them back to 0: `pad_unit(events, SECTION, offset=SECTION)` subtracts the offset from all ticks. Without this, section B events overflow and cause track length mismatch. Pattern:
  ```python
  def pad_unit(events, section_ticks, offset=0):
      for e in events:
          e.start_tick = max(0, e.start_tick - offset)
          e.end_tick = max(0, e.end_tick - offset)
          if e.end_tick > section_ticks:
              e.end_tick = section_ticks
      if not events or events[-1].end_tick < section_ticks:
          events.append(MusicEvent(pitch=0, volume=0, start_tick=section_ticks-10, end_tick=section_ticks))
      return events
  
  unit_a = MusicUnit(events=pad_unit(all_events[:len(all_events)//2], SECTION, offset=0))
  unit_b = MusicUnit(events=pad_unit(all_events[len(all_events)//2:], SECTION, offset=SECTION))
  ```
- **Every unit builder MUST pad to exact section boundary** — pattern: `pad_to_section(events)` first CLAMPS any `end_tick > SECTION` to `SECTION`, then appends `MusicEvent(pitch=0, volume=0, start_tick=SECTION-10, end_tick=SECTION)`. Without clamping, variable-length patterns (ritardando, phase-shifted layers, generators) overflow and cause track length mismatch. Full pattern:
  ```python
  def pad_to_section(events):
      for e in events:
          if e.end_tick > SECTION:
              e.end_tick = SECTION
      if not events or events[-1].end_tick < SECTION:
          events.append(MusicEvent(pitch=0, volume=0, start_tick=SECTION-10, end_tick=SECTION))
  ```
- **Sparse rhythmic methods need continuous fill layers** — Euclidean rhythms, isorhythmic talea, and other sparse methods produce staccato output. Combine with continuous layers (DPSM phase-shifted arpeggios, sustained pads, walking bass fills) to achieve flowing texture. User rejected sparse-only output as "staccato instead of flowing."
- **Timing constants must be explicit** — `HALF`, `QUARTER`, `EIGHTH`, `SIXTEENTH` are NOT provided by the engine. Define at top of every script: `HALF = BAR // 2`, `QUARTER = BAR // 4`, etc. When adapting from source MIDI with different TPB (e.g. 15360), recalculate all durations for the composer's TPB (480).
- **Markov transitions use degree indices, not pitch classes** — When building Markov transition tables for melodic generation, the state space must be scale degree indices (0-6 for heptatonic scales), NOT pitch class numbers (0,2,4,5,7,9,11). Common bug: defining transitions like `{0: [(2, 0.3), (4, 0.25), (7, 0.15)]}` which mixes degree 0 (C) with pitch classes 2 (D), 4 (E), 7 (G). Correct: `{0: [(2, 0.3), (4, 0.25), (5, 0.20), (1, 0.15), (0, 0.10)]}` where all values are valid degree indices 0-6. Then convert degrees to pitches via `diatonic(key_root, scale_intervals, degree_index)`.
- **Extending source MIDI to multi-section arrangement** — When given a short MIDI sketch (e.g. 8 bars) and asked to extend to 32 bars: (1) extract chord voicings with mido, (2) map to section progression (Intro/Verse/Chorus/Outro), (3) assign instruments per section with dynamic variation (intro=sparse, verse=moderate, chorus=full, outro=fade), (4) add countermelody using isorhythmic or other method for textural interest.
- **Progressive instrument dropout in outro** — User rejected volume fade ("do not fade the outro, silence the instruments one by one"). Instead of gradual volume reduction, drop instruments sequentially: bar 1 = all instruments, bar 2 = drop countermelody/lead, bar 3 = drop drums/bass, bar 4 = drop strings, final bar = piano only. Pattern:
  ```python
  # Outro: progressive dropout
  if section_name == 'Outro':
      if bar < 2:  # Lead plays bars 0-1
          lead_events = build_lead(...)
      if bar < 3:  # Drums/bass play bars 0-2
          drum_events = build_drums(...)
      if bar < 3:  # Strings play bars 0-2
          string_events = build_strings(...)
      # Piano plays all 4 bars
      piano_events = build_piano(...)
  ```
- **Section-specific texture variation** — User asked to "vary the strings drone once per section". Assign different textures to different sections:
  - Verse A: sustained pad (whole notes)
  - Verse B: staccato chords (quarter notes)
  - Chorus A: sustained + tremolo (eighth notes with volume oscillation)
  - Chorus B: staccato chords
  - Outro: sustained, then silent after bar 2
  Pattern: check `section_name` in builder function, branch to different event generation logic per section.
- **Full harmony analysis workflow** — When asked to "check the harmony" of a composition:
  1. Loop through all 32 bars, extract chord per bar from PROGRESSION array
  2. For each bar, analyze lead melody notes against chord tones:
     - Interval 0, 4, 7 (root, 3rd, 5th) = "✓ chord tone"
     - Interval 2, 5, 9 (2nd/9th, 4th/11th, 6th) = "○ passing tone"
     - Interval 1, 3, 6, 8, 10, 11 = "✗ tension"
  3. Analyze countermelody same way (if present)
  4. Report: chord progressions are diatonic, lead uses mostly chord tones + passing tones, countermelody creates controlled tension, no harsh dissonances (minor 2nds, tritones)
  5. Verdict: harmony is sound / needs fixing

## Genre pattern references

- `references/country-pattern-logic.md` — Country genre patterns
- `references/blues-pattern-logic.md` — Blues: shuffle, walking bass, boogie, block chords, blue-note slides
- `references/disco-pattern-logic.md` — Disco (4 variants): classic, funky, orchestral, modern/italo
- `references/multi-method-form-composition.md` — Multi-section forms (32-64+ bars) with different algorithmic methods per section

## Multi-version composition pattern

When asked to produce multiple versions of a style:
1. Create subfolders per variant: `Styles/<Genre>/<variant>/v1/`
2. Each variant gets its own `compose.py` with distinct methods/techniques
3. Render all, read grids, rank by **density contrast** (high contrast = punchier groove)
4. Report: ranking table + method comparison + grid of winner + all audio files
