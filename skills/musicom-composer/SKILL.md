---
name: musicom-composer
description: "End-to-end music composition workflow using the Musicom framework (musicom + musicom_ai + musicom_research). Pattern-centric pipeline: pitch patterns × rhythm patterns → melodic phrases → harmony → structure → MIDI/audio export. Includes minimal-deps fallback when music21/musicpy unavailable."
version: 0.1.0
author: Axel Wiertz
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [PYTHONPATH pointing to /root/musicom]
  commands: [python3, ffmpeg, ffplay]
dependencies:
  - music21 (for MIDI/MusicXML export)
  - musicpy (alternative to music21)
  - numpy (required for fallback synthesis)
metadata:
  hermes:
    tags: [music, composition, generative, MIDI, AudioCraft, numpy, pitch-pattern, rhythm-pattern, musicom]
    related_skills: [musicom-theory-kb, audiocraft-audio-generation, songwriting-and-ai-music, songsee, heartmula]
triggers:
  - composing music
  - music composition
  - generate music
  - MIDI export
  - chord progression
  - music theory
  - song structure
  - musicom
references:
  - references/ai-music-models-landscape.md
  - references/env-status-2026-05-17.md
  - references/lyria-3-model-clarification.md
  - references/music21-v10-api-notes.md
  - references/improvement-plan.md
  - references/official-skill-standards.md
---

# Musicom Composer — End-to-End Music Composition

## Recent Learning

### Lyria 3 Is NOT a Music Model — Clarification

User question: "Can Lyria 3 be used as a composer skill, not full generation from a prompt?"

**Answer: No. Lyria 3 (`google/lyria-3-pro-preview`, `google/lyria-3-clip-preview`) is Google's AI video generation model. It generates video frames from text/image prompts. It has zero music capability — no MIDI, no audio synthesis, no melody/harmony/rhythm understanding.**

For structured composition (not black-box generation), use **Musicom's pattern-centric pipeline** — pitch patterns × rhythm patterns → melodic phrases → harmony → structure → MIDI/audio. This gives full creative control.

For AI-generated music from text, use `audiocraft-audio-generation` (MusicGen) or `heartmula`.
For full songs with vocals, use `songwriting-and-ai-music` (Suno).

See `references/lyria-3-model-clarification.md` for full breakdown.

## Purpose

Orchestrates the full music composition workflow across the three Musicom repos. **The core principle: every musical element is a Pattern.** Pitch patterns and rhythm patterns are first-class compositional elements that combine into melodic phrases, which then flow through harmony, structure, and transformation stages to produce a complete composition as MIDI + audio, or exported to MusicXML/PianoRoll.

## When to Use

- Composing original music from a concept
- Generating chord progressions with musicom's theory engine
- Creating MIDI files from pattern-based compositions
- Converting between musical formats (MIDI ↔ MusicXML ↔ audio)
- Exploring music theory concepts (scales, modes, intervals)
- Building multi-section arrangements with pattern transformations

## Look Elsewhere First For

- Lyrics writing → use `songwriting-and-ai-music`
- AI-generated audio from text → use `audiocraft-audio-generation`
- Suno AI prompts → use `songwriting-and-ai-music`
- Audio feature analysis → use `songsee`
- Smart home audio playback → use platform-specific skills
- Human-like vocals → use `heartmula`

## Installation & Setup

### 1. Clone Musicom Repos

If not already present:

```bash
git clone https://github.com/axelwiertz/musicom.git /root/musicom
git clone https://github.com/axelwiertz/musicom_ai.git /root/musicom_ai
git clone https://github.com/axelwiertz/musicom_research.git /root/musicom_research
```

### 2. Install Dependencies

Choose one music library (both work, music21 preferred for MIDI):

```bash
pip install music21    # preferred for MIDI/MusicXML features
# OR
pip install musicpy    # alternative, more Pythonic API

# Required always
pip install numpy
```

### 3. Verify Setup

```bash
python3 -c "import music21; import numpy; print('All OK')" 2>&1
which ffmpeg && echo "ffmpeg OK"
which ffplay && echo "ffplay OK"
```

If `music21` fails, check version: `pip show music21` — v8+ changed some import paths.

## Quick Reference — Pattern-Centric Pipeline

```
Step 1: CONCEPT   — define genre, mood, key, tempo, form, instrumentation
Step 2: SCALE     — pick scale(s), mode, tonic (pitch-class foundation)
Step 3: PITCH PATTERN — define melodic motif/interval contour (NEW core step)
Step 4: RHYTHM PATTERN — define groove, Euclidean pattern, swing feel (NEW core step)
Step 5: PHRASE    — combine pitch pattern × rhythm pattern → MelodicPhrase
Step 6: HARMONY   — chord progression supporting the melodic phrase
Step 7: ARRANGE   — structure into sections (intro, verse, chorus, etc.)
Step 8: TRANSFORM — embellish, transpose, canon, retrograde, augment
Step 9: VOICE     — assign to instruments, add countermelodies
Step 10: EXPORT   — MIDI file, audio (numpy+ffplay or AudioCraft), MusicXML
```

**Key shift:** Steps 3-5 are now the compositional core. Melody is no longer "generated" as a side effect of scale patterns — it is explicitly constructed from a pitch pattern applied to a rhythmic pattern, then refined.

## The Three Repos

| Repo | Path | Role |
|------|------|------|
| **musicom** | `/root/musicom/` | Core data structures, generators, transformers, rules, analysis |
| **musicom_ai** | `/root/musicom_ai/` | High-level structures (Note, Chord, Phrase, Score), AI generators, MIDI I/O |
| **musicom_research** | `/root/musicom_research/` | Research examples, advanced patterns, quick reference |

## Step-by-Step Compositions

### Step 1: Define the Concept

Ask the user (or decide):
- **Genre**: classical, jazz, pop, electronic, ambient, folk, etc.
- **Mood**: happy, sad, tense, calm, energetic, mysterious
- **Key/Tonic**: C, D, G, A minor, etc.
- **Tempo**: BPM (quarter notes per minute)
- **Form**: binary (AB), ternary (ABA), verse-chorus, through-composed
- **Instrumentation**: piano, strings, synth, ensemble

```python
# Concept parameters
CONCEPT = {
    'genre': 'ambient jazz',
    'mood': 'calm, mysterious',
    'tonic': 0,        # 0=C, 1=C#, 2=D, ... 10=A, 11=B
    'mode': 'aeolian', # major, aeolian, dorian, phrygian, lydian, mixolydian
    'tempo': 90,       # BPM
    'form': 'ABA',
    'instruments': ['piano'],
}
```

### Step 2: Choose Scales and Modes

#### Using musicom (if available)

```python
import sys
sys.path.insert(0, '/root/musicom')

from structures.pitchclass import MusicPitchClassSet, PatternType
from structures.pitch import MusicPitchClass

# Create a scale: tonic pitch class + pattern type + rotation (mode)
# Mode indices: ionian=0 (major), dorian=1, phrygian=2, lydian=3,
#               mixolydian=4, aeolian=5 (natural minor), locrian=6

# Example: C major scale (tonic=C=0, ionian/major=rotation 0)
major_scale = MusicPitchClassSet(
    name="C Major",
    definition=PatternType.HEPTATONIC,
    rotation=0,   # ionian/major mode
    initial=0     # C = pitch class 0
)
print(major_scale.pitch_classes)
# (0, 2, 4, 5, 7, 9, 11) = [C, D, E, F, G, A, B]

# To get absolute pitches in an octave:
pitches = major_scale.get_pitches_in_octave(4)
print(pitches)  # MIDI pitches: [60, 62, 64, 67, 69, 71, 76]

# NOTE: music21 v10 installed separately.
#   MajorScale is NOT iterable in v10.
#   Use .getPitches() or access .pitch_classes directly.
#   MIDI write uses mf.write(fp=path) not mf.write() then mf.close().
#   See references/music21-v10-api-notes.md for full mapping.
```

#### Scale Pattern Reference

| PatternType | Intervals | Common Names |
|-------------|-----------|--------------|
| `HEPTATONIC` | (2,2,1,2,2,2,1) | major/ionian |
| `HEPTATONIC` + rot 5 | (2,2,1,2,2,1,2) | natural minor/aeolian |
| `HEPTATONIC` + rot 1 | (2,1,2,2,2,1,2) | dorian |
| `HEPTATONIC` + rot 2 | (1,2,2,2,1,2,2) | phrygian |
| `HEPTATONIC` + rot 3 | (2,2,2,1,2,2,1) | lydian |
| `HEPTATONIC` + rot 4 | (2,2,1,2,2,1,2) | mixolydian |
| `HEPTATONIC` + rot 6 | (1,2,2,1,2,2,2) | locrian |
| `PENTATONIC` | (2,2,3,2,3) | major pentatonic |
| `PENTATONIC` + rot 2 | (3,2,2,3,2) | minor pentatonic |
| `CHROMATIC` | (1,1,1,1,1,1,1,1,1,1,1,1) | all 12 notes |

#### Triads and Seventh Chords

```python
from structures.pitchclass import ChordQuality

# Triad definitions are in MusicPattern.dict:
# MAJOR: (4,3,5), MINOR: (3,4,5), DIMINISHED: (3,3,6),
# AUGMENTED: (4,4,4), SUS2: (2,5,5), SUS4: (5,2,5)

# 7th chords:
# MAJOR7: (4,3,4,1), MINOR7: (3,4,3,2), DOMINANT7: (4,3,3,2),
# MINOR7_FLAT5 (half-dim): (3,3,4,2)

# Diatonic chords in major key:
# I=Maj, ii=Min, iii=Min, IV=Maj, V=Maj, vi=Min, vii°=Dim
```

### Step 3: Chord Progressions

#### Using ChordDegreeGenerator

```python
from musicom.generators import ChordDegreeGenerator
from musicom.structures import MusicTimeGrid

# Create a time grid (4 beats per bar, 480 ticks per quarter note)
time_grid = MusicTimeGrid(timesteps=480)

# C major scale
scale = MusicPitchClassSet(
    name="C Major",
    definition=PatternType.HEPTATONIC,
    rotation=0,
    initial=0
)

# Progression: I - V - vi - IV (1 - 5 - 6 - 4)
chord_degrees = [1, 5, 6, 4]
gen = ChordDegreeGenerator(
    time_grid=time_grid,
    pattern=scale,
    chord_degrees=chord_degrees
)
unit = gen.generate()
```

#### Common Progressions

```
Bestseller:        1 - 5 - 6 - 4
Fifties:           1 - 6 - 2 - 5
Fifths down:       1 - 4 - 7 - 3 - 6 - 2 - 5
Flamenco:          1 - 7 - 6 - 5
Jazz turnaround:   1 - 3 - 6 - 2 - 5 - 1
12-Bar Blues:      I I I I | IV IV I I | V IV I I
Cyclic Fifths:     1 4 7 3 6 2 5 1
```

#### Movement Rules (valid next chords)

```
I (tonic)     → any degree
ii (2)        → IV(4), V(5), vii°(7)
iii (3)       → I(1), ii(2), IV(4), vi(6)
IV (4)        → I(1), ii(2), iii(3), V(5), vii°(7)
V  (5)        → I(1)
vi (6)        → I(1), ii(2), iii(3), IV(4), V(5)
vii° (7)      → I(1)
```

### Step 4: Pitch Patterns — Melodic DNA (NEW CORE STEP)

Pitch patterns store **intervallic contour** independently of scale or octave. They are the melodic DNA of your composition — define the shape once, then apply it to any scale/key/tempo.

#### Concept: PitchPattern

```python
# Patterns are interval sequences — positive = up, negative = down (in semitones)
# These are compositional motifs, not tied to a specific scale yet

# Ascending stepwise motif
ascending_step = (2, 2, 2, 2)        # C→D→E→F in C major

# Signature leap motif (think Beethoven 5: short-short-short-LONG)
beethoven_fate = (0, 0, 0, -3)      # G→G→G→Eb

# Blues bend pattern
blues_bend = (3, -1, 2, -1, 3)      # characteristic blues contour

# Arch contour (rise then fall)
arch = (2, 2, 2, -2, -2, -2)        # up 3, down 3

# Wave contour (oscillating)
wave = (2, -2, 2, -2, 2, -2)        # stepwise oscillation
```

#### Using PitchPattern with a Scale

```python
from structures.pitchclass import MusicPitchClassSet, PatternType

# Define scale
scale = MusicPitchClassSet(
    name="D Dorian",
    definition=PatternType.HEPTATONIC,
    rotation=1,   # Dorian mode
    initial=2     # D
)
print(f"Dorian pitches: {scale.pitch_classes}")
# (2, 4, 5, 7, 9, 11, 1) = D E F G A B C

# Define a pitch pattern (interval motif)
motif_intervals = (2, 3, -2, -1, 2)  # up step, skip, down step, down, up

# Apply pattern to scale: walk the motif through scale degrees
# Start on degree 1 (D), then apply intervals constrained to scale tones
# Result: D(62) → F(65) → A(69) → G(67) → F(65) → G(67)
```

#### Contour Patterns (Abstract Shape)

For quick melodic sketching, use abstract contour notation:

```
U = Up one scale step
D = Down one scale step
S = Same (repeat)
L = Leap (jump of 3+ scale degrees)

Contour "UUDDLSSL" → rise, rise, fall, fall, same, same, leap up, fall
```

#### Pitch Pattern Transformations

```python
# Retrograde a pitch pattern
retro = motif.retrograde()     # intervals reversed

# Invert a pitch pattern
inv = motif.invert()           # up becomes down, down becomes up

# Rotate (mode change)
rotated = motif.rotate(2)      # shift starting point in the interval cycle
```

### Step 5: Rhythm Patterns — Groove DNA (NEW CORE STEP)

Rhythm patterns are now **first-class compositional elements**, not just an afterthought applied to existing melodies.

#### Using RhythmGenerator (Euclidean rhythms)

```python
from musicom.generators import RhythmGenerator

# 5 hits in 8 steps = pentatonic rhythm (like clave)
rhythm_gen = RhythmGenerator(onsets=5, timesteps=8)
units = rhythm_gen.generate()
# Result: onset pattern distributed evenly (e.g., 3-2 son clave)

# 4 hits in 4 steps = straight quarter notes
rhythm_gen = RhythmGenerator(onsets=4, timesteps=4)

# 3 hits in 4 steps = cross-rhythm (hemiola feel)
rhythm_gen = RhythmGenerator(onsets=3, timesteps=4)

# 7 hits in 16 steps = dense Latin feel
rhythm_gen = RhythmGenerator(onsets=7, timesteps=16)
```

#### Named Rhythmic Patterns

```python
from structures.timegrid import MusicRhythmPattern

# Access pre-defined styles
rhythm = MusicRhythmPattern(time_grid=time_grid, name='Son Clave')
rhythm = MusicRhythmPattern(time_grid=time_grid, name='Bossa Nova')
rhythm = MusicRhythmPattern(time_grid=time_grid, name='Samba')
rhythm = MusicRhythmPattern(time_grid=time_grid, name='Steve Reich')
rhythm = MusicRhythmPattern(time_grid=time_grid, name='Shiko')
rhythm = MusicRhythmPattern(time_grid=time_grid, name='Rumba')
# Each provides onset positions within a cycle
```

#### Rhythm Pattern Reference

| Style | onsets/steps | Character |
|-------|-------------|-----------|
| `Four` | 4/16 | Straight quarter notes |
| `Two` | 2/8 | Half notes |
| `Son Clave` | 5/16 | Afro-Cuban foundation |
| `Rumba` | 5/16 | Cuban rumba |
| `Bossa Nova` | 5/16 | Brazilian syncopation |
| `Samba` | 7/16 | Dense Brazilian |
| `Shiko` | 5/16 | Nigerian bell |
| `Steve Reich` | 8/12 | Minimalist phasing |
| `Tresillo` | 3/8 | Basic Cuban cell |
| `Euclidean(3,8)` | 3/8 | Tresillo variant |
| `Euclidean(7,16)` | 7/16 | Dense Latin |

#### Rhythm Pattern Transformations

```python
# Stretch a pattern (augmentation — half speed)
augmented = MusicRhythmPattern(time_grid=time_grid, name='Son Clave')
augmented.scale(2.0)  # Each onset interval doubled

# Compress a pattern (diminution — double speed)
diminished = MusicRhythmPattern(time_grid=time_grid, name='Son Clave')
diminished.scale(0.5)  # Each onset interval halved

# Shift all onsets by n ticks (displacement)
shifted = rhythm.displace(240)  # shift by half a beat
```

### Step 6: Phrase — Combine Pitch × Rhythm (NEW)

**This is the compositional core.** A `MelodicPhrase` combines a pitch pattern with a rhythm pattern into a complete musical idea.

#### Concept

```
MelodicPhrase = PitchPattern × RhythmPattern

Each onset in the rhythm gets a pitch from the pitch pattern (cycling if needed).
Each rest creates a gap.
```

#### Building a Phrase Programmatically

```python
import itertools
from structures.unit import MusicUnit, MusicEvent

# 1. Define pitch pattern (interval motif in semitones)
pitch_pattern = (2, 3, -2, -1, 2)

# 2. Get rhythm onsets (from Euclidean or named pattern)
from generators import RhythmGenerator
rhythm_unit = RhythmGenerator(onsets=5, timesteps=8).generate()[0]
# rhythm_unit.onset_intervals gives the timing between onsets

# 3. Map pitches to rhythm — cycle through pitch pattern
pitch_cycle = itertools.cycle(pitch_pattern)
current_pitch = 62  # Start note (D4)
step = 60  # ticks per beat

melody_events = []
tick = 0
for onset_interval in rhythm_unit.onset_intervals:
    interval = next(pitch_cycle)
    pitch = current_pitch + interval
    pitch = max(48, min(84, pitch))  # Clamp to comfortable MIDI range
    melody_events.append(MusicEvent(
        pitch=pitch, volume=90,
        start_tick=tick, end_tick=tick + step
    ))
    current_pitch = pitch
    tick += int(step * onset_interval / 2)

phrase = MusicUnit(events=melody_events)
```

### Step 7: Harmony

#### Using ChordDegreeGenerator

(Same as before — no change needed. Chord progressions support the melodic phrase.)

### Step 8: Structure and Arrangement

#### Using MusicVoice, MusicSection, MusicProject

```python
from musicom.structures import MusicVoice, MusicSection, MusicProject

# Create a voice with your melodic phrase
voice = MusicVoice(name="Lead", units=[phrase_unit])

# Create a section
section = MusicSection(
    name="Verse",
    voices=[voice],
    tempo=CONCEPT['tempo']
)

# Build the project with multiple sections
project = MusicProject(name="My Composition")
project.add_section(verse_section)
project.add_section(chorus_section)
project.add_section(verse_section)  # ABA form
```

### Step 9: Transformations

#### Pattern-Level Transformations

Transformations now operate on **PitchPatterns and RhythmPatterns** as compositional primitives:

```python
# Retrograde a pitch pattern
retro_motif = motif_pattern.retrograde()  # intervals reversed

# Invert a pitch pattern
inv_motif = motif_pattern.invert()  # up becomes down, down becomes up

# Augment a rhythm pattern (slow down)
slow_rhythm = rhythm.augment(2.0)  # twice as slow

# Diminish a rhythm pattern (speed up)
fast_rhythm = rhythm.diminish(0.5)  # twice as fast

# Displace a rhythm (shift all onsets by n ticks)
shifted = rhythm.displace(240)  # shift by half a beat
```

#### Traditional Stream Transformations

```python
from musicom.transformers import CanonTransformer, EmbellishmentTransformer
from musicom.transformers.pitch import transpose_note, invert_note

# Canon (voice imitation)
canon = CanonTransformer(source_unit=melody, imitation_interval=480)
canon_results = canon.transform()

# Embellish melody (add neighbor tones, passing tones)
embellish = EmbellishmentTransformer(unit=melody)
embellished = embellish.transform()

# Transpose entire melody
transposed = transpose_note(melody, semitones=5)  # up a perfect fourth

# Invert (mirror around a pitch axis)
inverted = invert_note(melody, axis=60)  # invert around C4
```

### Step 10: Export

#### Export to MIDI (music21 v10)

```python
from musicom.converters.music21_score import unit_to_stream

s = unit_to_stream(melody)
mf = midi.translate.streamToMidiFile(s)
mf.write(fp='/tmp/hermes/songs/my_composition.mid')
```

#### Export to PianoRoll (numpy array)

```python
from musicom.converters.pypianoroll_converter import unit_to_pianoroll
pr = unit_to_pianoroll(melody)
```

#### Export to MusicXML

```python
s = unit_to_stream(melody)
s.write('musicxml', fp='/tmp/hermes/songs/my_composition.xml')
```

## Pattern Architecture (Reference)

```
PATTERN SYSTEM
│
├── PitchPattern (interval sequence)
│   ├── ScalePattern (full scale interval sequence)
│   ├── MelodicMotif (short interval contour: e.g., 2,3,-2,-1,2)
│   ├── ArpeggioPattern (chord tones in sequence)
│   └── ContourPattern (abstract: UUDDLSSL)
│
├── RhythmPattern (onset interval sequence)
│   ├── EuclideanPattern (k hits in n steps)
│   ├── StylePattern (clave, bossa, samba, swing)
│   ├── PolymetricPattern (nested metric layers)
│   └── GroovePattern (swing grid + micro-timing)
│
├── CompositePattern
│   ├── MelodicPhrase (pitch × rhythm → complete musical idea)
│   ├── HarmonicPattern (chord progression + voicing rhythm)
│   └── VoicePattern (full voice = pitched events over time)
│
└── TransformPattern
    ├── Retrograde (reverse sequence)
    ├── Inversion (negate intervals)
    ├── Augmentation (× duration factor)
    ├── Diminution (÷ duration factor)
    └── Transposition (shift pitch)
```

## Minimal Dependencies Fallback

When `music21`, `musicpy`, and other audio libraries are **not available**, generate audio using only **numpy** + **ffplay**:

```python
import numpy as np
import wave
import os

SAMPLE_RATE = 44100

def midi_to_freq(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def generate_note(midi_note, duration, sample_rate=SAMPLE_RATE, gain=0.3):
    freq = midi_to_freq(midi_note)
    n = int(duration * sample_rate)
    t = np.linspace(0, duration, n, False)
    note = np.sin(2 * np.pi * freq * t)
    attack_samples = min(int(0.005 * sample_rate), n)
    release_samples = min(int(0.02 * sample_rate), n)
    attack = np.linspace(0, 1, attack_samples)
    release = np.linspace(1, 0, release_samples)
    sustain_len = n - attack_samples - release_samples
    sustain = np.full(max(0, sustain_len), 0.7)
    envelope = np.concatenate([attack, sustain, release])
    envelope = envelope[:n]
    if len(envelope) < n:
        envelope = np.pad(envelope, (0, n - len(envelope)))
    return note * envelope * gain

def generate_chord(midi_notes, duration, sample_rate=SAMPLE_RATE, gain=0.15):
    parts = [generate_note(n, duration, sample_rate, gain=gain) for n in midi_notes]
    return sum(parts)

def save_wav(filename, samples, sample_rate=44100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        audio = np.clip(samples, -1.0, 1.0)
        audio_int16 = (audio * 32767).astype(np.int16)
        wf.writeframes(audio_int16.tobytes())

# === Pattern-based composition example ===
# Pitch pattern: ascending arpeggio motif
pitch_pattern = (0, 4, 7, 12)  # root, major third, fifth, octave

# Chord sequence with pattern-based rhythm
root = 60
chord_sequence = [
    [60, 64, 67],  # C
    [62, 65, 69],  # Dm
    [64, 68, 71],  # Em
    [65, 69, 72],  # F
]

all_samples = np.array([])
BEAT_DURATION = 60.0 / 120
for chord in chord_sequence:
    chord_samples = generate_chord(chord, BEAT_DURATION)
    gap = np.zeros(int(SAMPLE_RATE * 0.03))
    all_samples = np.concatenate([all_samples, chord_samples, gap])

save_wav('/tmp/hermes/songs/pattern_composition.wav', all_samples)
```

## AudioCraft Integration (for high-quality audio)

When the `audiocraft-audio-generation` skill is available.

## Complete Example: Ambient Jazz Piece (Pattern-Centric)

```python
import sys, itertools
sys.path.insert(0, '/root/musicom')

from structures.pitchclass import MusicPitchClassSet, PatternType
from structures.unit import MusicUnit, MusicEvent
from structures.timegrid import MusicTimeGrid
from generators.chord_degrees import ChordDegreeGenerator
from generators import RhythmGenerator
from converters.music21_score import unit_to_stream
from music21 import midi

# 1. Concept: C Dorian, ambient jazz, 80 BPM
TONIC = 2  # D

# 2. Create D Dorian scale
dorian = MusicPitchClassSet(
    name="D Dorian", definition=PatternType.HEPTATONIC,
    rotation=1, initial=2
)

# 3. Define pitch pattern (motif interval contour)
#    Motif: step up, skip up, step down, stay, leap up
pitch_pattern = (2, 3, -2, 0, 5)

# 4. Define rhythm pattern (Euclidean: 5 hits in 8 = clave feel)
rhythm_unit = RhythmGenerator(onsets=5, timesteps=8).generate()[0]
rhythm_onsets = rhythm_unit.onset_intervals

# 5. Combine: map pitch pattern onto rhythm onsets
pitch_cycle = itertools.cycle(pitch_pattern)
current_pitch = 62  # D4
melody_events = []
tick = 0
step = 60

for onset_interval in rhythm_onsets:
    interval = next(pitch_cycle)
    pitch = max(48, min(84, current_pitch + interval))
    melody_events.append(MusicEvent(
        pitch=pitch, volume=90,
        start_tick=tick, end_tick=tick + step
    ))
    current_pitch = pitch
    tick += int(step * onset_interval / 2)

melody = MusicUnit(events=melody_events)

# 6. Generate chord progression: I - iv - VII - III (Dm - Gm - C - E)
time_grid = MusicTimeGrid(timesteps=480)
gen = ChordDegreeGenerator(
    time_grid=time_grid, pattern=dorian,
    chord_degrees=[1, 4, 7, 3]
)
harmony = gen.generate()

# 7. Convert to MIDI (music21 v10 API)
stream_out = unit_to_stream(melody)
mf = midi.translate.streamToMidiFile(stream_out)
mf.write(fp='/tmp/hermes/songs/dorian_jazz_pattern.mid')
```

## Output Formats & Locations

Default output directory: `/tmp/hermes/songs/`

| Format | Extension | Use Case | Quality |
|--------|-----------|----------|---------|
| MIDI | `.mid` | DAW import, edit | Lossless, editable |
| WAV | `.wav` | Raw audio, editing | Lossless PCM |
| OGG (Opus) | `.ogg` | Telegram voice bubbles | Compressed, voice-optimized |
| MP3 | `.mp3` | General sharing | Compressed, universal |
| FLAC | `.flac` | Archival | Lossless compression |
| MusicXML | `.xml` | Sheet music export | Lossless, notation |

For Telegram voice bubbles:
```bash
ffmpeg -i /tmp/hermes/songs/output.wav -codec:a libopus -application voip -b:a 48k /tmp/hermes/songs/output.ogg -y -loglevel error
```

## Notes

- **music21 v10.x installed**: API changed from v8. `MajorScale` is no longer iterable (use `.getPitches()`), `MidiFile.write()` requires `fp=` kwarg. See `references/music21-v10-api-notes.md` for the full mapping.
- **Venv has no pip**: Use `apt-get install -y python3-pip` then `pip3 install --target /opt/hermes/.venv/lib/python3.13/site-packages <pkg>`. Never call `/opt/hermes/.venv/bin/pip` directly (binary doesn't exist).
- **MIDI clock drift**: When chaining multiple MusicUnits, ensure `MusicTimeGrid(timesteps=480)` is consistent across all
- **Envelope clicks**: The numpy fallback uses sine waves — always add ADSR envelopes (attack ~5ms, release ~20ms) to prevent clicking
- **Scale overflow**: `get_pitches_in_octave()` returns MIDI pitches; ensure your pattern intervals don't push pitches outside 0-127
- **Pattern cycling**: When rhythm has more onsets than pitch pattern intervals, pitches cycle automatically — this is by design, but may produce unexpected results if not intentional
- **AudioCraft quality**: Text-to-music works best with genre + mood + instrumentation + dynamics described in the prompt; avoid artist names (copyright)
- **Path issues**: Musicom repos at `/root/musicom/`. Use `sys.path.insert(0, '/root/musicom')`
- **numpy not in system Python**: Use `/opt/hermes/.venv/bin/python3`
- **Generator returns multiple units**: PatternGenerator returns `List[MusicUnit]` — iterate or concatenate

## ⚠️ Known Implementation Gaps

- `PitchPattern`, `RhythmPattern`, and `MelodicPhrase` are documented as core classes but **do not exist as implemented classes** — the workflow uses tuple-based intervals and manual construction instead
- `live_test.py` is a fixed 20s loop; no parameterized fallback composer exists for arbitrary genre/mood/form
- No bridge between musicom_ai generators and the pattern pipeline
- No composition quality analysis or feedback loop

## AI Music Model Landscape — What Can & Can't Compose

See `references/ai-music-models-landscape.md` for the full breakdown. **Key takeaway: Lyria 3 (Google) is a video generation model, not a music model — it cannot be used as a composer skill.**

### Models That CAN Generate Music
- **MusicGen / AudioGen (Meta)** — via `audiocraft-audio-generation` skill
- **Suno AI** — via `songwriting-and-ai-music` skill
- **HeartMuLa** — via `heartmula` skill
- **Musicom (local)** — via this skill (`musicom-composer`)

### Models That CANNOT Compose Music
- **Lyria 3 (Google)** — AI video generation only
- **Ring-2.6-1T** — reasoning language model
- **Qwen 3.6 35B** — general-purpose LLM
- **TTS models** — speech synthesis only

## Version History

### v0.1.2 (2026-05-17)
- Added Lyria 3 correction section (NOT a music model — video generation only)
- Added `lyria-3-model-clarification.md` reference with model comparison table
- Updated references frontmatter to include all session-specific detail files

### v0.1.1 (2026-05-17)
- Added AI music model landscape reference (Lyria 3 is NOT a music model)
- Added environment status reference (missing repos, config persistence fix)
- Warning: Musicom repos need to be re-cloned