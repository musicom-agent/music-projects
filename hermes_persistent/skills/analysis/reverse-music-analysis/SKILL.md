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

### Noise Isolation and Pre-filtering (DSP)
For real-world field recordings or noisy snips (e.g., wind rumble, bird chirps, background chatter) before transcription/feature-extraction:
1. **Harmonic / Percussive Separation (HPSS):**
   * Sustained melodic parts (`y_harm`) carry pitch DNA.
   * Transient, non-pitched parts (`y_perc`) contain drums or transient noise (like high-pitched bird chirps).
2. **Frequency Bandpass Filter:**
   * Limit analysis window to the vocal/instrumental register (e.g., **150Hz – 1600Hz**).
   * Removing `< 150Hz` cuts wind/low-rumble.
   * Removing `> 1600Hz` cuts high-frequency bird chirps, hiss, and transient crackles.
3. **Onsets & Pitch Tracking Windowing:**
   * For highly noisy audio, run peak onset-strength detection (`librosa.onset.onset_strength`) followed by localized windowing (e.g., +/- 100ms) to run pitch detection algorithms (`librosa.pyin` or YIN) on specific voiced slices only, rather than analyzing continuous silence and background noise.
4. **Python Implementation (librosa + soundfile):**
   ```python
   import librosa, numpy as np, soundfile as sf
   y, sr = librosa.load("input.wav", sr=22050)
   y_harm, y_perc = librosa.effects.hpss(y, margin=(2.0, 4.0)) # isolate sustained tones
   D = librosa.stft(y_harm, n_fft=2048, hop_length=512)
   S, phase = np.abs(D), np.angle(D)
   freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
   low_idx, high_idx = np.where(freqs >= 150)[0][0], np.where(freqs <= 1600)[0][-1]
   S_clean = np.zeros_like(S)
   S_clean[low_idx:high_idx, :] = S[low_idx:high_idx, :]
   y_clean = librosa.istft(S_clean * np.exp(1j * phase), hop_length=512)
   sf.write("isolated.wav", y_clean, sr)
   ```

### Pattern Inference
1. **RhythmPattern**: Calculate `onset_intervals` between notes.
2. **PitchPattern**: Map MIDI notes to semitone offsets relative to the detected `tonic`.
3. **Scale**: Histogram analysis of pitch classes to find the closest match in `PatternRegistry`.

## Pitfalls & Workarounds
- **TimeConverter Chords Bug**: When using `TimeConverter.events_to_delta` (or core `UnitMatrixComposer.to_midi`) on cells containing simultaneous chords or overlapping notes, the engine generates wrong, negative delta times or huge overflow ticks. This results in empty or corrupted MIDI files with track length drift.
  * *Workaround*: Bypass the core exporter. Gather all absolute `MusicEvent` objects across the matrix, convert chord groups into clean, sequentialized events (or sort all note_on and note_off events on a strict timeline), then calculate the chronological offsets manually using raw `mido` track writing. Ensure empty tracks are padded to the overall expected composition tick length.
  * *Permanent Library Fix*: Correct `/opt/data/repos/musicom/structures/time.py` by converting events to sequential milestones (flat list of `on`/`off` events), sorting them chronologically (with `off` events preceding `on` events at the same tick), and processing step-by-step to emit positive chronological delta steps. This turns overlap issues into clean standard polyphony inside MIDI parsers.

## Analysis Artifacts
- **DNA Catalog**: A JSON representation of the patterns.
- **Visual Dashboard**: ASCII grid of the reconstructed matrix.
- **src/regen.py**: A script that can re-synthesize a similar piece using the extracted rules.
