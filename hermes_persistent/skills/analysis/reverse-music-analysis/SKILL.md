---
name: reverse-music-analysis
description: "Reverse-engineering audio/MIDI files back into Musicom UnitMatrix and pattern structures (PitchPattern, RhythmPattern, Scale). Supports source-to-style deconstruction."
version: 0.1.0
author: Musicom Agent
license: MIT
platforms: [linux]
prerequisites:
  commands: [python3, ffmpeg, ffprobe]
dependencies:
  - basic-pitch (Neural transcription)
  - music21 (Symbolic analysis)
  - numpy (Matrix math)
  - scipy (Signal processing)
references:
  - references/midi-deconstruction-logic.md
---

# Reverse Music Analysis — Source to UnitMatrix

## Purpose
Analyze an existing **audio file** or **MIDI file** to extract its "DNA" and map it back into the Musicom `UnitMatrix` framework. This allows for style cloning, variation generation, and structural learning.

## Workflow

### 1. Source Acquisition
- **Audio**: Neural Transcription (Basic-Pitch) -> MIDI.
- **MIDI**: Direct parsing via `music21` or `mido`.

### 2. Feature Extraction
- **Temporal**: BPM detection, meter (4/4, 6/8), and bar-line alignment.
- **Pitch**: Key detection, Scale identification (MusicPitchClassSet), and Interval Contour (PitchPattern).
- **Rhythm**: Onset detection, quantization to grid, and Euclidean density analysis.

### 3. Matrix Mapping
- Segment the data into `MusicUnit` blocks (usually 1 or 2 bars).
- Populate the `UnitMatrix`:
    - **Rows**: Instrumental voices extracted (Lead, Bass, Chords).
    - **Columns**: Sections (Intro, Phrase A, Phrase B).
- Identify **Sentences** and **Developing Variations** (Retrograde, Inversion, Sequencing).

## Technical Implementation

### Audio to MIDI (Neural)
```bash
basic-pitch /path/to/output/ /path/to/source.wav
```

### Pattern Inference
1. **RhythmPattern**: Calculate `onset_intervals` between notes.
2. **PitchPattern**: Map MIDI notes to semitone offsets relative to the detected `tonic`.
3. **Scale**: Histogram analysis of pitch classes to find the closest match in `PatternRegistry`.

## Analysis Artifacts
- **DNA Catalog**: A JSON representation of the patterns.
- **Visual Dashboard**: ASCII grid of the reconstructed matrix.
- **src/regen.py**: A script that can re-synthesize a similar piece using the extracted rules.
