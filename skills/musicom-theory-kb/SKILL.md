---
name: musicom-theory-kb
description: "Knowledge base for the musicom music composition framework — theory concepts, pattern classes, chord progressions, generators, and transformations. Covers three repos: musicom (core), musicom_ai (generators), musicom_research (reference)."
tags: [music, theory, scales, progressions, patterns, composition, ai]
---

# Musicom — Combined Knowledge Base

## Three Repositories Merged

| Repo | Location | Focus | Status |
|---|---|---|---|
| **musicom** | `/root/musicom/` | Core framework — data structures, generators, transformers, rules, analysis | Production codebase |
| **musicom_ai** | `/root/musicom_ai/` | AI composition assistant — Tet system, structures, generators, harmony, melody, rhythm, MIDI I/O | Phase 1-2 complete |
| **musicom_research** | `/root/musicom_research/` | Research examples, quick reference, integration patterns | Examples & reference |

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

## Practical Audio Generation (Minimal Dependencies)

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

### Pitfall

`/root` is **not accessible** in the sandbox — the musicom repos live there. Always check `os.listdir(".")` and use relative or `/tmp/` paths. If the musicom generators are unusable, fall back to pure numpy synthesis as a working alternative.

### Telegram Audio Sending (Voice Bubbles)

When sending audio to Telegram, **WAV files do not render as voice bubbles** — they must be converted to **OGG (Opus)** first.

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
