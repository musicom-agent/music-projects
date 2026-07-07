---
name: musicom-theory-kb
description: "Knowledge base for the musicom music composition framework — theory concepts, pattern classes, chord progressions, generators, and transformations. Consolidating musicom + musicom_ai + musicom_research into a single repo (axelwiertz/musicom)."
references:
  - references/ai-composition-tools-2025.md
  - references/style-kb-standard.md
  - references/musicom-repository-structure.md
tags: [music, theory, scales, progressions, patterns, composition, ai]
---

# Musicom — Combined Knowledge Base

## Primary: Consolidated Canonical Repo

The ecosystem has been consolidated into a single core library: **`axelwiertz/musicom`**.

| subpackage | Source Repo (Archived) | Content |
|---|---|---|
| **`musicom.ai`** | `musicom_ai` | AI generators, tet_system, rules, integration bridge |
| **`musicom.analysis`** | `musicom` | Music21/MusicXML/RN analysis |
| **`musicom.generators`** | `musicom` | Basic Markov, genetic, chord generators |
| **`musicom.structures`** | `musicom` | UnitMatrix, MusicUnit, MusicEvent, **TimeConverter (2026-06-27)** |
| **`musicom.workflows`** | `musicom` | **UnitMatrixComposer (2026-06-27)** |
| **`examples/history`** | `musicom_research` | Historical research examples |

## Current Clones (local filesystem)

| Type | Path | Remote |
|---|---|---|
| Core library | `/opt/data/repos/musicom/` | `git@github.com:axelwiertz/musicom.git` |
| Project portfolio | `/opt/data/repos/musicom-agent/music-projects/` | `git@github.com:musicom-agent/music-projects.git` |
| Agent workspace | `/opt/data/repos/musicom-agent/` | Handover/docs/skills |

**Rule:** Ensure `PYTHONPATH` includes `/opt/data/repos/musicom` and that all imports use the `from musicom.ai...` namespace.

## Unified Architecture

```
MUSICOM KNOWLEDGE BASE
│
├── 1. 12TET SYSTEM (pitch, intervals, scales, keys, modes)
│     ├── musicom/structures/pitch.py — MusicPitchClass, MusicPitchGrid
│     ├── musicom_ai/core/tet_system.py — PitchClass, Interval, Scale, Key, TimeSignature
│     └── musicom/structures/pitchclass.py — PatternType, PatternDefinition, PatternRegistry
│
├── 2. PATTERN CONCEPTS (scales, chords, progressions as patterns)
│     ├── PatternType enum — all interval, triad, 7th, scale pattern types
│     ├── PatternRegistry — CHROMATIC > HEPTATONIC > PENTATONIC hierarchy
│     ├── MusicPitchClassSet — pitch classes with rotation/mode support
│     └── PatternMovement — common chord progressions
│
├── 3. MUSICAL STRUCTURES (data objects)
│     ├── musicom: MusicEvent → MusicUnit → MusicVoice → MusicSection → MusicProject → UnitMatrix
│     ├── musicom_ai: Note → Rest → Chord → Phrase → Progression → Voice → Score
│     └── musicom_research: Note, Chord, Scale, Sequence (simplified)
│
├── 4. HARMONY & RULES (chord movement, counterpoint, voice leading)
│     ├── Scale7PitchDegree — active/stable degrees, movement rules
│     ├── PatternMovementRules — scale degree next-chord rules
│     ├── Scale7ChordDegree — diatonic chord functions (tonic, dominant, subdominant)
│     ├── Counterpoint — parallel fifths/octaves detection
│     └── musicom_ai/rules/ — voice leading, harmonic rules (planned)
│
├── 5. GENERATORS (algorithmic composition)
│     ├── musicom: Pattern, MarkovChain, Genetic, Harmonics, Stochastic, ChordDegree, Rhythm
│     ├── musicom_ai: RandomWalk, ScaleBased, MarkovChain (melody), Progression, Voicing (harmony), RhythmicPattern (rhythm)
│     └── musicom_research: MelodyGenerator, ChordProgressionGenerator, RhythmGenerator, PatternGenerator
│
├── 6. TRANSFORMERS (modifications)
│     ├── musicom: Canon, Embellishment, Matrix, Pitch transformations, PitchSequence
│     ├── musicom_ai: pitch_transformers (planned)
│     └── musicom_research: Transposition, Time, Dynamics, Harmonic, Rhythmic, Pattern transformers
│
├── 7. RHYTHM & TIME
│     ├── musicom: MusicTimeGrid, MusicRhythmPattern, Euclidean rhythm
│     ├── musicom_ai: RhythmicPatternGenerator (Euclidean, swing, polyrhythms, clave)
│     └── musicom_research: TimeGrid, rhythm quantization
│
├── 8. I/O & FORMATS
│     ├── musicom: MIDI, MusicXML (via music21), MIDI instrument/percussion mappings
│     ├── musicom_ai: MIDIReader, MIDIWriter, PianoRoll (via PyPianoroll), MusicXML
│     └── musicom_research: MIDIHandler, MusicXMLHandler, PianoRollHandler
│
├── 9. ANALYSIS
│     ├── musicom: score_analyze (music21), piece_analyze (musicpy), key/chord detection, roman numeral
│     ├── musicom_ai: contour analysis, range, chord quality, harmonic function
│     └── musicom_research: rule-based validation (voice leading, harmonic, melodic)
│
└── 10. COMPOSITION WORKFLOWS (bridging approaches)
      ├── Pattern-first: scale → chord progression → melody → transform → export
      ├── Melody-first: generate melody → harmonize → rhythm → arrange → export
      ├── Rhythm-first: create pattern → generate pitches → chordalize → arrange → export
      ├── Matrix-first: UnitMatrix → fill cells → apply transforms → extract → export
      ├── Analysis-first: load MIDI → analyze → transform → regenerate → export
      └── Style-learning: train Markov on data → generate → refine → export
```

## Quick Reference

### Pitch Classes
```
C=0, C#=1, D=2, D#=3, E=4, F=5, F#=6, G=7, G#=8, A=9, A#=10, B=11
```

### MIDI Octaves
```
C4 = 60 (middle C), A4 = 69 (440Hz)
octave = (midi // 12) - 1
pitch_class = midi % 12
```

### 14 Scale Patterns
```
major:         [0,2,4,5,7,9,11]    (2,2,1,2,2,2,1)
natural_minor: [0,2,3,5,7,8,10]    (2,2,1,2,2,1,2)
harmonic_minor:[0,2,3,5,7,8,11]    (2,2,1,2,1,3,1)
melodic_minor: [0,2,3,5,7,9,11]    (2,2,1,2,2,1,2)
dorian:        [0,2,3,5,7,9,10]    (2,1,2,2,2,1,2)
phrygian:      [0,1,3,5,7,8,10]    (1,2,2,2,1,2,2)
lydian:        [0,2,4,6,7,9,11]    (2,2,2,1,2,2,1)
mixolydian:    [0,2,4,5,7,9,10]    (2,2,1,2,2,1,2)
locrian:       [0,1,3,5,6,8,10]    (1,2,2,1,2,2,2)
aeolian:       same as natural_minor
ionian:        same as major
pentatonic_major:  [0,2,4,7,9]      (2,2,3,2,3)
pentatonic_minor:  [0,3,5,7,10]     (3,2,2,3,2)
blues:         [0,3,5,6,7,10]       (3,2,1,1,3,2)
whole_tone:    [0,2,4,6,8,10]       (2,2,2,2,2,2)
chromatic:     [0,1,2,3,4,5,6,7,8,9,10,11]
```

### 20+ Chord Qualities
```
Triads:     major[0,4,7], minor[0,3,7], diminished[0,3,6], augmented[0,4,8], sus2[0,2,7], sus4[0,5,7]
7ths:       maj7[0,4,7,11], min7[0,3,7,10], dom7[0,4,7,10], dim7[0,3,6,9],
            half_dim7[0,3,6,10], min_maj7[0,3,7,11], aug7[0,4,8,10], maj6[0,4,7,9], min6[0,3,7,9]
Extended:   maj9, min9, dom9, maj11, min11, dom11, maj13, min13, dom13
```

### Diatonic Chords in Major Key
```
Degree  I    ii   iii   IV   V    vi   vii°
Qual.   Maj  min  min   Maj  Maj  min  dim
7th     Imaj7 ii7  iii7  IVmaj7 V7  vi7  viiø7
Function Tonic SubDom  Dom  Dom  Tonic  Dom
```

### Diatonic Degree Pitch Indexing
When translating scale degrees (e.g., $1 \to 4 \to 7$) into absolute MIDI notes, never use raw modulo wrapping like `scale[(degree - 1) % 7]` directly. This causes octave inversion errors for wrapping degrees (such as $vii^\circ$ and $iii$), throwing notes into the incorrect octave below the root.

Use an octave-aware scaling indexer:
```python
def get_diatonic_note(degree_index, key_root, scale):
    octave_shift = degree_index // 7
    scale_step = degree_index % 7
    return key_root + (octave_shift * 12) + scale[scale_step]
```

### High-Quality FluidSynth Rendering
When generating audio loop previews, avoid using simple mathematical sine oscillators, which sound synthetic and hollow. Instead, render directly using FluidSynth and local General MIDI SoundFonts:
* Standard workspace SoundFont: `/opt/data/.local/lib/python3.13/site-packages/pretty_midi/TimGM6mb.sf2` (or similar env paths).
* FluidSynth Fast-Render Command syntax:
  ```bash
  fluidsynth -ni -F output.wav -r 44100 path_to_soundfont.sf2 input.mid
  ```
* Standardize channel mapping: Channel 0 for Trumpet/Lead, Channel 1 for Trombone/Mid, Channel 2 for Tuba/Bass, Channel 9 (MIDI 10) for Snare/Drumband percussion.

### UnitMatrix Timing Constraints
Always enforce absolute start/end timing alignments in cell populating scripts. Every `MusicUnit` assigned to a column in the `UnitMatrix` must span exactly the column's assigned tick length (e.g., `BAR_TICKS`), or the composer's internal `validate_timing()` sanity checks will fail during MIDI export. Ensure empty beats are filled or notes are explicitly padded to the end boundary.

### Common Progressions
```
Bestseller:        1 - 5 - 6 - 4
Fifties:           1 - 6 - 2 - 5
Fifths down:       1 - 4 - 7 - 3 - 6 - 2 - 5
Flamenco:          1 - 7 - 6 - 5
Lounge Jazz 1:     7 - 3 - 6 - 2 - 5 - 1
12-Bar Blues:      I I I I | IV IV I I | V IV I I
Cyclic Fifths:     1 4 7 3 6 2 5 1
```

### Cadences
```
Perfect: 5→1  (V→I)
Plagal:  4→1  (IV→I)
Imperfect: any→5
Interrupted: 5→4 or 5→6
```

### Movement Rules (Scale Degrees in Major)
```
I (tonic)  → any degree
ii (2)     → IV(4), V(5), vii°(7)
iii (3)    → I(1), ii(2), IV(4), vi(6)
IV (4)     → I(1), ii(2), iii(3), V(5), vii°(7)
V  (5)     → I(1)
vi (6)     → I(1), ii(2), iii(3), IV(4), V(5)
vii° (7)   → I(1)
```

### Generator Summary
```
musicom:               musicom_ai:
  PatternGenerator        RandomWalkGenerator (weighted random walk)
  MarkovChainGenerator    ScaleBasedGenerator (4 patterns)
  GeneticGenerator        MarkovChainGenerator (style learning)
  HarmonicsGenerator
  StochasticGenerator
  ChordDegreeGenerator    ProgressionGenerator (functional/jazz/modal)
  RhythmGenerator         VoicingGenerator (close/open/drop2/drop3/spread)
                          RhythmicPatternGenerator (Euclidean/swing/polyrhythms/clave)
```

### Transformer Summary
```
musicom:               musicom_research:       musicom_ai:
  CanonTransformer      TranspositionTransformer pitch_transformers (planned)
  Embellishment         TimeTransformer
  Matrix operations     DynamicsTransformer
  Pitch transforms      HarmonicTransformer
  PitchSequence (IRI)   PatternTransformer
  Time transforms
```

### Composition Workflow Bridging
The knowledge base is designed to support switching between approaches mid-flow:

1. **Start pattern-first** (scale → chords), then switch to **melody-first** (generate motif, develop)
2. **Start with a MIDI file**, analyze it, transform it, regenerate with different generators
3. **Use UnitMatrix** for systematic composition, then extract and embellish
4. **Train Markov chains** on an existing piece, generate new material, validate with rules
5. **Generate rhythm first**, then overlay patterns, harmonize with progression generators

## Extended Python Library Landscape (2025)

Discovered via web research June 2026. Not yet integrated into musicom.

### DawDreamer — Python DAW (JUCE backend)
`pip install dawdreamer` — Linux x86_64, Python 3.11-3.14
- VST3 instrument+effects hosting with **audio-rate parameter automation**
- FAUST DSP synthesis, time-stretch, pitch-warp, MIDI playback
- Multiprocessing support — faster than Pedalboard for batch renders
- Superset of Pedalboard for complex signal chains
- GitHub: `DBraun/DawDreamer`

### xenharmlib — Microtonal / Xenharmonic Theory
`pip install xenharmlib`
- Equal-division tunings: 24-TET (Arabic Maqam), 53-TET (Turkish Makam), Bohlen-Pierce
- Western + Up/Down notation, posttonal set theory, interval analysis
- Modulation suggestions for arbitrary key changes
- Covers: Maqam, Turkish Makam, xenharmonic scales
- **Key gap filler**: musicom is 12-TET only; xenharmlib enables non-Western tuning systems
- Docs: `xenharmlib.readthedocs.io`

### partitura — Score / MusicXML Specialist
`pip install partitura`
- Deep MusicXML read/write, staff notation handling
- Score-to-performance alignment, expressive performance data
- Better than music21 for complex score operations
- GitHub: `CPJKU/partitura`

### compIAM — Indian Art Music Toolkit (MTG)
`pip install compIAM`
- Carnatic + Hindustani computational analysis
- Pitch, rhythm, intonation, melodic pattern tools
- Raga identification, tala structure analysis
- GitHub: `MTG/compIAM`

### mirdata — MIR Dataset Loaders
`pip install mirdata`
- Unified loaders for 100+ MIR datasets
- Includes Indian Classical, gamelan-adjacent datasets
- GitHub: `mir-dataset-loaders/mirdata`

### Practical Audio Generation (Minimal Dependencies)

When `music21`, `musicpy`, `soundfile`, and other audio libraries are **not available** in the sandbox, you can still generate and play audio using only **numpy** + **ffplay**:

### Step-by-step recipe

1. **Synthesize audio with numpy** — use `np.sin()` for tone generation, `np.linspace()` for ADSR envelopes, `np.int16` for 16-bit PCM conversion
2. **Write a WAV file** with the built-in `wave` module (no dependencies needed)
3. **Play the file** via `ffplay -nodisp -autoexit <path>` or `ffmpeg -hide_banner -loglevel error -i <path> -f null -`

### Key details

- **Note frequency:** `f = 440.0 * (2.0 ** ((midi - 69) / 12.0))`
- **WAV header:** 16-bit, mono, set via `wave.setsampwidth(2)`, `wave.setnchannels(1)`
- **Envelope:** add attack (5ms) and release (20ms) with `np.linspace` to avoid clicking at note boundaries
- **Note gap:** insert 30ms rest between quarter notes by reducing `note_duration_samples = int(beat_duration * sample_rate) - gap_samples`
- **Clamp before int16:** `np.clip(samples, -1.0, 1.0)` then `(samples * 32767).astype(np.int16)`
- **Sandbox paths:** write to `/tmp/hermes/songs/` (create dir with `os.makedirs`)
- **Instrument-Specific Modeling Envelopes**:
  - **Piano**: Fundamental + harmonics $[1, 2, 3]$ with rapid exponential decay ($e^{-4t}$).
  - **Guitar**: Karplus-Strong algorithm using filtered noise loops; decay factor $\approx 0.996$ for natural string sustain.
  - **Violin**: Sawtooth harmonic summation ($1/n^{1.1}$) with subtle vibrato ($5.5\text{Hz}$ at $0.8\%$ depth) and slow attack ($250\text{ms}$) for bowing simulation.
  - **Brass / Showband Instruments**: Bright sawtooth approximations combining fundamental with strong second and third harmonics ($1.0$, $0.5$, $0.25$) with quick decay and rapid release ADSR profiles ($50\text{ms}$ attack, $100\text{ms}$ decay, $150\text{ms}$ release) to mimic physical tongue-and-lip articulations.
  - **Drumband Snare**: White noise pulses modulated with a percussion ADSR envelope ($5\text{ms}$ fast attack, $50\text{ms}$ decay, $50\text{ms}$ release) to simulate dynamic military-style rolls and ghost notes.

### Pitfalls

- **Venv and Pytest imports**: When running test suites, imports like `librosa` or relative package modules might fail or raise `ModuleNotFoundError`. Always ensure the editable development package is synchronized in the local python binary environment by running `uv pip install -e .` against the specific virtual environment path (`.venv/bin/python`).
- **`MEDIA:/` in send_message is UNRELIABLE.** It reports success but the file may not appear in the chat. This is a known issue — don't debug it, just fall back.
- **NEVER retry a send more than once.** One attempt, if it fails silently, fall back to telling the user the path. Sending the same message 5+ times is worse than not sending at all.
- Always use `-application voip` flag for best Telegram voice bubble quality
- Use `target: "telegram:Axel (dm)"` when available instead of bare chat IDs — it is the canonical handle
- **Always verify audio works via ffplay before attempting to send to user** — don't send broken audio

### Web Search for AI Music Research (No browser, no pip)

In Docker sandboxes with no `web_search` tool, no Chrome, and no pip, use DuckDuckGo Lite via `curl` + Python's `html.parser`. The parser extracts results from `<span class='link-text'>` (URLs) and `<a class='result-link'>` (titles). Key pattern:

```
1. Fetch: curl -s https://lite.duckduckgo.com/lite/ -d 'q=QUERY' -H 'User-Agent: Mozilla/5.0'
2. Parse with Python html.parser — look for span.link-text (URL) + a.result-link (title) + td.result-snippet
3. BeautifulSoup is ideal but not available; Python's built-in HTMLParser works fine
4. Write raw HTML to /tmp/ first for debugging, then parse
5. Results may have empty titles — URL slug is a fallback title
```

See `references/ai-composition-tools-2025.md` for the full research summary found this way.

### Pitfall

```bash
ffmpeg -i /tmp/hermes/songs/melody.wav -codec:a libopus -application voip -b:a 48k /tmp/hermes/songs/melody.ogg -y -loglevel error 2>&1
```

### Send via send_message tool

```
target: "telegram:Axel (dm)"
message: "Your melody! 🎵\nMEDIA:/tmp/hermes/songs/melody.ogg"
```

Key: the `MEDIA:/absolute/path/to-file` prefix tells the platform to send the file natively. `.ogg` sends as a **voice bubble**. `.mp4` plays inline. `.png`/`.webp`/`.jpg` appear as photos.

### Send Workflow — DO NOT RETRY

1. Convert WAV → OGG via ffmpeg
2. Verify file exists: `ls -la /tmp/hermes/songs/melody.ogg`
3. **Play it first** via `ffplay -nodisp -autoexit /tmp/hermes/songs/melody.ogg` — confirm it works locally before sending
4. Send once with `MEDIA:/` prefix
5. **If it doesn't arrive — DO NOT RETRY.** Tell the user the file path directly and stop. Spamming is worse than not sending.

### Pitfalls

- **`MEDIA:/` in send_message is UNRELIABLE.** It reports success but the file may not appear in the chat. This is a known issue — don't debug it, just fall back.
- **NEVER retry a send more than once.** One attempt, if it fails silently, fall back to telling the user the path. Sending the same message 5+ times is worse than not sending at all.
- Always use `-application voip` flag for best Telegram voice bubble quality
- Use `target: "telegram:Axel (dm)"` when available instead of bare chat IDs — it is the canonical handle
- **Always verify audio works via ffplay before attempting to send to user** — don't send broken audio

## 11. Modal Interchange & Chromatic Patterns
Modal interchange is the temporary substitution of a scale's native pitch classes with those from a parallel mode (same tonic).

### Best Practices for "Off-Scale" Patterns
1. **Chromatic Gravity (Directional Resolution)**: 
   * **Raised notes** (e.g., Lydian #4) should resolve **UP** (F# -> G).
   * **Lowered notes** (e.g., Aeolian b6) should resolve **DOWN** (Ab -> G).
2. **Law of Conservation of Identity**: Maintain at least one **Common Tone** (pivot bulb) between diatonic and borrowed chords to prevent jarring transitions.
3. **The "Brief Visit" Protocol**: Surround off-scale patterns with stable diatonic anchors (I or V) to maintain tonal center.
4. **Emotional Matrix**:
   * **Lydian (Raise 4th)**: Heroic, Wonder, Ethereal.
   * **Aeolian (Lower 6th/b6)**: Melancholy, Depth, Romanticism.
   * **Phrygian (Lower 2nd/b2)**: Mystery, Tension, Ancient.
   * **Mixolydian (Lower 7th/b7)**: Bluesy, Soul, Stable.

### Pitch Class Matrix Visualization
Treat the 12-TET space as a 12-row "Light Bulb Matrix". Interchange is the toggling of specific bulbs (e.g., Row 9 OFF, Row 8 ON) while maintaining the root (Row 0).

## 12. Hostinger VPS & Docker Environment Update-Proofing
To ensure persistent configuration and memory storage across Docker container updates/re-deployments on VPS, follow this strict storage pattern:

### Storage Separation Rule
All configuration, state DBs, memories, sessions, and active skills must live in a persistent mount `/opt/data/hermes_persistent/` mapped back to expected run paths via symbolic links.

### Expected Link Structure
- `/opt/data/.env` -> `/opt/data/hermes_persistent/.env`
- `/opt/data/config.yaml` -> `/opt/data/hermes_persistent/config.yaml`
- `/opt/data/memories` -> `/opt/data/hermes_persistent/memories`
- `/opt/data/sessions` -> `/opt/data/hermes_persistent/sessions`
- `/opt/data/skills` -> `/opt/data/hermes_persistent/skills`
- `/opt/data/state.db` -> `/opt/data/hermes_persistent/state.db`
- `/opt/data/state.db-shm` -> `/opt/data/hermes_persistent/state.db-shm`
- `/opt/data/state.db-wal` -> `/opt/data/hermes_persistent/state.db-wal`

### Verification
If verifying local active state, check `/opt/data/` symlink endpoints rather than raw files to ensure you do not overwrite ephemeral root-mount configuration.
