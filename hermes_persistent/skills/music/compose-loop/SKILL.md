---
name: compose-loop
description: "Rapid 4/8/16-bar pattern-centric composition using Musicom framework. UnitMatrix-first workflow with dual-mode delivery (MIDI + Audio + MusicXML) and optional Flat.io sync."
version: 0.1.0
author: Axel Wiertz
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: []
  commands: [python3, ffmpeg]
dependencies:
  - music21
  - mido
  - numpy
  - networkx
  - librosa
  - scipy
metadata:
  hermes:
    tags: [music, composition, generative, MIDI, AudioCraft, numpy, pitch-pattern, rhythm-pattern, musicom, loop]
    related_skills: [musicom-composer, musicom-theory-kb, audiocraft-audio-generation]
triggers:
  - compose loop
  - generate loop
  - 4-bar pattern
  - 8-bar pattern
  - 16-bar pattern
  - rapid composition
  - music loop
  - pattern loop
references:
  - references/technical-notes.md
  - references/unitmatrix-first-composer-workflow.md
  - references/flat-io-token-persistence.md
  - references/working-regen-template.py
scripts:
  - scripts/generate_loop.py
---

# Compose Loop — Rapid Pattern-Centric Composition

## Purpose

Generate **4/8/16-bar loops** using the **Musicom pattern-centric workflow** (PitchPattern × RhythmPattern → MelodicPhrase → Harmony → Structure → Export).
- **Style-First Rule**: Use 'Style' instead of 'Genre'. Organize loops under `/opt/data/projects/Styles/[StyleName]/[ProjectName]`.
- **Reference Pattern**: Place detailed style pattern descriptions in the parent Style folder (e.g., `Styles/Country/Analysis/patterns.md`).
- **Consolidation Rule**: When a loop iterates or clones a previous one, merge or append into a single project folder rather than creating redundant top-level projects (e.g., `012-country-full-16bar` merged previous loop drafts).
- **Workflow Invariant**: Always include `MIDI`, `Audio`, `Analysis`, `Notes`, `Scores`, `src`, and `index.html`.
- **Metrical Gravity Viz**: Visualize rhythmic onsets in the dashboard using high-contrast ASCII markers (█ and ░).
## Workflow

```text
1. Concept → Brief (genre, mood, key, tempo, bars)
2. Scale → Mode → Tonic (MusicPitchClassSet)
3. Skeleton → Fill UnitMatrix: 1 pitch/set + 1 Rhythm Pattern per unit (NEW)
   - Shows: Form, Phrases/Sentences, Rhythm Grid
4. Pitch Pattern → Interval contour (derived from skeleton)
5. Rhythm Pattern → Refine skeleton grid (e.g., augmentation)
...
```

## Skeleton-First Rapid Workflow
1. **Concept**: Define key/tempo/bars.
2. **Skeleton**: Fill UnitMatrix with **one pitch/set + one rhythmic seed** per unit. Define **Phrases and Sentences**.
3. **Refine**: Apply transformations (Retrograde, Inversion) to expand the skeleton into 16 bars.
4. **Export**: Full bundle (MIDI, Audio, MusicXML, Dashboard).

## Style Integrity
- Loops must be categorized under `/opt/data/projects/Styles/`.
- Similar loops should be appended into longer compositions to demonstrate structural development.
- Always include `src/regen.py`.
...
- **Iterative Refinement**: Refine the skeleton into full patterns in the next step.
```

## Example: 4-Bar D Dorian Loop (90 BPM)

```python
import sys
sys.path.insert(0, '/root/musicom')

from structures.pitchclass import MusicPitchClassSet, PatternType
from generators import RhythmGenerator
from converters.music21_score import unit_to_stream
from music21 import midi
import itertools

# 1. Concept
concept = {
    'genre': 'ambient jazz',
    'mood': 'calm, mysterious',
    'tonic': 2,  # D
    'mode': 'dorian',
    'tempo': 90,
    'bars': 4
}

# 2. Scale
scale = MusicPitchClassSet(
    name="D Dorian", 
    definition=PatternType.HEPTATONIC,
    rotation=1,  # Dorian mode
    initial=2    # D
)

# 3. Pitch Pattern
pitch_pattern = (2, 3, -2, 0, 5)  # step, skip, step, stay, leap

# 4. Rhythm Pattern
rhythm = RhythmGenerator(onsets=5, timesteps=8).generate()[0]

# 5. Phrase
pitch_cycle = itertools.cycle(pitch_pattern)
current_pitch = 62  # D4
melody_events = []
tick = 0
step = 60  # ticks per beat

for onset_interval in rhythm.onset_intervals:
    interval = next(pitch_cycle)
    pitch = current_pitch + interval
    pitch = max(48, min(84, pitch))  # Clamp to D3-D5
    melody_events.append(MusicEvent(
        pitch=pitch, volume=90,
        start_tick=tick, end_tick=tick + step
    ))
    tick += int(step * onset_interval / 2)

melody = MusicUnit(events=melody_events)

# 6. Harmony
chords = ChordDegreeGenerator(scale, [1, 4, 7, 3]).generate()  # Dm, Gm, C, E

# 7. Structure
matrix = UnitMatrix(voices=2, sections=1)  # Lead + Harmony
matrix.set_cell(0, 0, melody)
matrix.set_cell(1, 0, chords)

# 8. Transform
melody_retro = melody.retrograde()
matrix.set_cell(0, 1, melody_retro)

# 9. Voice
lead = MusicVoice("Lead", [melody, melody_retro], instrument="Acoustic Grand Piano")
harmony = MusicVoice("Harmony", [chords], instrument="Electric Piano")

# 10. Export
project_dir = "/opt/data/projects/031-d-dorian-loop"
os.makedirs(f"{project_dir}/MIDI", exist_ok=True)
os.makedirs(f"{project_dir}/Audio", exist_ok=True)
os.makedirs(f"{project_dir}/Scores", exist_ok=True)
os.makedirs(f"{project_dir}/src", exist_ok=True)

# MIDI
export_midi(matrix, f"{project_dir}/MIDI/loop.mid")

# Audio (HQ FluidSynth)
export_audio(matrix, f"{project_dir}/Audio/loop.ogg")

# MusicXML
export_musicxml(matrix, f"{project_dir}/Scores/loop.xml")

# Flat.io (if token valid)
publish_flat_io(f"{project_dir}/Scores/loop.xml", "031-d-dorian-loop-v1")

# 11. Dashboard
generate_dashboard(matrix, f"{project_dir}/index.html")

# Regeneration Script
with open(f"{project_dir}/src/regen.py", "w") as f:
    f.write('''
import sys
sys.path.insert(0, '/root/musicom')

from structures.pitchclass import MusicPitchClassSet, PatternType
from generators import RhythmGenerator
from converters.music21_score import unit_to_stream
from music21 import midi
import itertools

# 1. Scale
scale = MusicPitchClassSet("D Dorian", PatternType.HEPTATONIC, rotation=1, initial=2)

# 2. Pitch Pattern
pitch_pattern = (2, 3, -2, 0, 5)

# 3. Rhythm Pattern
rhythm = RhythmGenerator(onsets=5, timesteps=8).generate()[0]

# 4. Phrase
pitch_cycle = itertools.cycle(pitch_pattern)
current_pitch = 62
melody_events = []
tick = 0
step = 60

for onset_interval in rhythm.onset_intervals:
    interval = next(pitch_cycle)
    pitch = max(48, min(84, current_pitch + interval))
    melody_events.append(MusicEvent(pitch=pitch, volume=90, start_tick=tick, end_tick=tick + step))
    tick += int(step * onset_interval / 2)

melody = MusicUnit(events=melody_events)

# 5. Export MIDI
s = unit_to_stream(melody)
mf = midi.translate.streamToMidiFile(s)
with open('../MIDI/loop.mid', 'wb') as f:
    f.write(mf.writestr())

print("Regenerated: MIDI/loop.mid")
''')
```

## Output Structure

```text
031-d-dorian-loop/
├── README.md              # Concept, status, files
├── MIDI/                  # loop.mid
├── Audio/                 # loop.ogg, loop.wav
├── Scores/                # loop.xml
├── src/                   # regen.py
└── index.html             # Dashboard
```

## Seamless Loop Pattern

For loops where the end flows naturally into the beginning:

1. **Chord resolution**: Last chord must resolve to the first chord. Keep the final bar harmonically identical to bar 1 or cadentially closed into the tonic.
2. **Melody return**: End phrase on tonic or a stable chord tone. Prefer phrases that land on the same pickup logic the next bar expects.
3. **Bass walking**: Bass should close on the tonic/root motion that restarts cleanly at bar 1.
4. **Drum continuity**: Drum loop must be explicitly length-matched to the intended bar count. Do not let a 4-bar or 16-bar drum layer silently diverge from the loop length.
5. **Percussion channel**: In MIDI export, percussion must be forced to **GM channel 10** (`channel=9` in mido) and should not inherit piano defaults.
6. **Track naming**: Verify the MIDI track name and program after export. A percussion layer that renders as piano usually means the channel or instrument mapping was lost.

### Verified Fanfare Loop Example
- Style: Fanfare
- Key: Bb Major, 132 BPM
- 8 bars percussion + 8 bars brass/harmony loop material
- Percussion track verified on channel 9 with drum hits aligned to beats 1-4
- See `references/working-regen-template.py` for the current verified regeneration pattern.

- Rapid prototyping of musical ideas
- Teaching a genre through short loops
- Generating material for DAW import
- Creating background music for videos/games
- Exploring pattern transformations

## When NOT to Use

- Full songs with vocals → use `songwriting-and-ai-music`
- AI-generated audio from text → use `audiocraft-audio-generation`
- Complex orchestral scores → use `musicom-composer`

## Dependencies

```bash
# System Python is externally managed (PEP 668). Always use venv:
python3 -m venv /tmp/musicom-venv
source /tmp/musicom-venv/bin/activate
pip install music21 mido numpy networkx librosa scipy
deactivate
```

### Current API Reality (as of 2025-07-03)

The skill example above uses OLD APIs that no longer work. The code below is the **verified working pattern**:

#### Imports
```python
import sys
sys.path.insert(0, '/opt/data/repos/musicom')  # NOT /root/musicom

import numpy as np
from structures.unit import MusicEvent, MusicUnit
from structures.project import MusicVoice
from structures.matrix import UnitMatrix
```

#### UnitMatrix
```python
# OLD (broken): UnitMatrix(voices=4, sections=1)
# NEW (working):
matrix = UnitMatrix(shape=(4, 1))  # (rows=voices, cols=sections)
matrix.set_unit((0, 0), melody)    # NOT set_cell(row, col, unit)
```

#### MusicVoice
```python
# OLD (broken): MusicVoice("Fiddle", [melody], instrument="Violin")
# NEW (working):
lead = MusicVoice("Fiddle", midi_instrument=56)  # GM instrument number
```

#### musicpy dependency
The `generators` and `converters` packages import `musicpy` which is **not installed**. Avoid importing from `generators.*` or `converters.musicpy_converter`. Use inline fallbacks:

```python
# RhythmGenerator fallback
class RhythmGenerator:
    def __init__(self, onsets=8, timesteps=16):
        self.onsets = onsets
        self.timesteps = timesteps
    def generate(self):
        grid = np.zeros(self.timesteps)
        for i in range(self.timesteps):
            grid[i] = 0.5 if i % 2 == 1 else 1.0
        return [type('obj', (object,), {'onset_intervals': grid.tolist()})()]

# MusicPitchClassSet fallback (avoids broken relative import in structures.pitchclass)
class MusicPitchClassSet:
    def __init__(self, name, definition, rotation, initial):
        self.name = name
        self.initial = initial
    def get_chord(self, degree, octave=5):
        notes = [7, 9, 11, 12, 14, 16, 18]  # G Ionian
        idx = (degree - 1) % 7
        base = notes[idx]
        return [base + 12 * o for o in range(3)]
```

#### Audio Rendering (no FluidSynth)
FluidSynth is **not installed**. Use music21 + numpy sine wave synthesis as fallback:

```python
from music21 import converter
from scipy.io import wavfile

score = converter.parse("MIDI/loop.mid")
sr = 44100
duration = 10.0
t = np.linspace(0, duration, int(sr * duration), endpoint=False)
audio = np.zeros_like(t)

for n in score.flatten().notesAndRests:
    if hasattr(n, 'pitch'):
        freq = n.pitch.frequency
        start = n.offset
        dur = n.duration.quarterLength * 0.5
        start_sample = int(start * sr * 0.5)
        end_sample = int((start + dur) * sr * 0.5)
        if end_sample > len(audio):
            end_sample = len(audio)
        if start_sample < len(audio):
            env = np.linspace(1, 0, end_sample - start_sample)
            audio[start_sample:end_sample] += 0.3 * np.sin(2 * np.pi * freq * t[start_sample:end_sample]) * env

audio = np.divide(audio, np.max(np.abs(audio)), out=np.zeros_like(audio), where=np.max(np.abs(audio)) > 0) * 0.9
wavfile.write("Audio/loop.wav", sr, audio.astype(np.float32))
```

#### converters/__init__.py
The converters package is empty by default. It needs explicit imports:
```python
from .midi_converter import export_midi
from .audio import export_audio
from .musicxml import export_musicxml
```

#### Missing modules
The following modules do NOT exist in the repo and need stub creation:
- `converters/audio.py` — stub with `def export_audio(matrix, path): ...`
- `converters/musicxml.py` — stub with `def export_musicxml(matrix, path): ...`
- `visualization/dashboard.py` — stub with `def generate_dashboard(matrix, path): ...`

### Pitfalls

- **System Python**: PEP 668 enforced. Always use `/tmp/musicom-venv`.
- **music21 import**: Must be `from music21 import converter` (not `from music21 import midi, converter` — the `midi` submodule is separate).
- **MIDI Percussion**: Channel 10 (`channel=9` in mido). GM mapping: Kick=36, Snare=38.
- **FFmpeg loudnorm**: Parameter `I` must be between -70 and -5. Setting `I=-1.0` fails. Use `I=-16`.
- **Absolute paths**: Always use absolute paths for file I/O in sandboxed execution.
- **structures.pitchclass relative import**: `MusicPitchClassSet` from the repo has a broken `from ..utilities.helpers import` — use the inline fallback above.
- **Empty file verification**: After writing MIDI/WAV, `stat` the file to confirm non-zero size. If 16-22 bytes, it's corrupt.