---
name: musicom-theory-kb
type: Skill
title: Musicom Theory Knowledge Base
description: Unified repository containing canonical scales, progressions, and execution rules for algorithmic music composition.
resource: https://github.com/axelwiertz/musicom
tags: [music, theory, scales, logic, okf]
timestamp: 2026-07-15T20:45:00Z
---

# Unified Architecture

```
MUSICOM KNOWLEDGE BASE (OKF)
│
├── 1. 12TET SYSTEM
│     ├── musicom/structures/pitch.py — MusicPitchClass, MusicPitchGrid
│     └── musicom_ai/core/tet_system.py — PitchClass, Interval, Scale
│
├── 2. PATTERN CONCEPTS (scales, chords, progressions as patterns)
│     ├── PatternType enum — all interval, triad, 7th, scale pattern types
│     └── PatternRegistry — CHROMATIC > HEPTATONIC > PENTATONIC hierarchy
│
├── 3. MUSICAL STRUCTURES (data objects)
│     └── musicom: MusicEvent → MusicUnit → MusicVoice → UnitMatrix
```

## 1. 12TET Pitch System
*   **Pitch Classes:** `C=0, C#=1, D=2, D#=3, E=4, F=5, F#=6, G=7, G#=8, A=9, A#=10, B=11`.
*   **Middle C (C4):** MIDI number 60.

## 2. Diatonic Degree Pitch Indexing
Avoid octave wrapping transposition errors. Calculate absolute pitches using:
$$\text{pitch} = \text{key\_root} + \left( \left\lfloor \frac{\text{degree\_index}}{7} \right\rfloor \times 12 \right) + \text{scale\_intervals}\left[ \text{degree\_index} \pmod 7 \right]$$

## 3. High-Quality FluidSynth Rendering (Pillar 6)
Render symbolic matrices using micromamba FluidSynth and local soundfonts:
*   **Binary:** `/opt/data/micromamba/envs/musicom/bin/fluidsynth`
*   **SoundFont:** `/opt/data/.local/lib/python3.13/site-packages/pretty_midi/TimGM6mb.sf2`
*   **Volume Gain Rule:** Explicitly pass `-g 1.3` higher volume gain. Default low gain values can cut off extremely quiet decay tails of pads and drones prematurely, leading to short file perception.
*   **Opus Delivery:** Convert output master WAV to `.ogg` using `ffmpeg` with `-application voip` flag for Telegram streaming compatibility.

## 4. Matrical Time-Grid Verification & Track Padding
When compiling multi-track timelines using the `UnitMatrix` or `UnitMatrixComposer`, all voices (Lead, Pad, Bass, Percussion) MUST have exactly identical tick boundaries down to the final column section:
1. **The Truncation Issue**: Inactive or repetitive voices (like a snare drum playing once on Beat 3) can complete early, causing a timeline alignment error on compile (e.g. track length mismatch: 61440 vs 58560).
2. **The Matrical Pad Solution**: To guarantee zero-drift length symmetry, explicitly append a final resting note-on/note-off pair (`pitch=0, volume=0` or a silent hit `pitch=38, volume=0`) at the absolute boundaries of the section column (`total_section_ticks - 1` to `total_section_ticks`). This forces the composer to compute identical boundaries without timeline warping.
3. **Strict Validation**: Always execute `composer.validate()` to verify that all tracks are perfectly aligned before committing to MIDI compilation.
4. **Version Control Suffixes**: Always isolate, organize, and version-number all sound (WAV/OGG) and symbolic (MIDI) composition outputs under dedicated versioned subfolders (e.g. `/opt/data/projects/Research/outputs/v1/`) rather than flat roots, protecting past iterations from being overwritten.

## 5. Chaotic-Harmonic Smoothing (Method 028 Hybridisation)
When asked to smooth chaotic nature-led systems (e.g. Hénon/Lorenz Attractors) with classical harmonic stability:
1. **Timing (Unpredictable/Chaotic)**: Retain the attractor's raw coordinates to map organic, volatile grain durations (e.g. mapping $x_n$ to inter-onset intervals between $120$ and $960$ ticks).
2. **Pitches (Diatonic/Stable)**: Map the chaotic state variable strictly to *scale degree offsets relative to the chord root* of the active section's progression. Clamp target steps to stable chord tones (Root, 3rd, 5th, or 7th) to dissolve dissonance:
   ```python
   # Chaotic offset clamped to stable chord intervals (0=Root, 2=3rd, 4=5th, 6=7th step above root)
   chaotic_chord_offset = int(normalized_attractor_state * 4) * 2
   target_degree = section_chord_root_degree + chaotic_chord_offset
   pitch = get_diatonic_note(key_root, scale_intervals, target_degree)
   ```

## 6. Continuous Portamento & L-System Hybridisation (Methods 019 & 029)
When merging deterministic fractals with sliding continuous portamento:
1. **The L-System Framework**: Generate structural note nodes (e.g., quarter-note divisions) using Lindenmayer production strings (`F -> F+F-F+F`).
2. **The Portamento Interpolation**: Instead of jumping cleanly between successive fractal pitch nodes ($P_1 \to P_2$), subdivide the inner duration of each L-System cell into micro-steps (e.g., `steps = 4`) and smoothly interpolate the pitch frequencies across those steps.
3. **Outcome**: Achieves fluid, sliding organic movements while maintaining strict self-similar fractal patterns over macro timelines.

## 7. Open Knowledge Format (OKF) v0.1 Conformance
Structure organizational knowledge as portable, directory-based markdown graphs:
*   **Header Frontmatter**: Every concept file MUST contain valid YAML frontmatter with `type`, `title`, `description`, and `timestamp`.
*   **Interoperable Linking**: Concept files cross-reference via relative markdown links: `[Text](/path/to/concept.md)`.
*   **Flat Directory Indexing**: Root folders should maintain an `index.md` entry point mapping back to nested assets.

## 8. Folk Hardstyle & Indie-Folk Hybrid Formatting (v2/v3 Styles)
When constructing modern hybrid genres (e.g. Noah Kahan style Folk Hardstyle / Balfolk Electronic drops):
1. **Genre Decoupling**: Avoid the flat, conjunct violin jigs of Balfolk unless requested. Use rapid, dynamic acoustic banjo arpeggiated rolls (Noah Kahan style) combined with steady nylon guitar fingerpicking.
2. **Tempo & Key**: Select a slower, anthemic indie-folk tempo ($140$–$150$ BPM) in bittersweet nostalgic keys like **G Major** or **A Dorian**.
3. **The Climax Drop Form**:
   * *Stage 1 (Verse/Intro)*: Minimalistic acoustic instrumentation with simple tambourine/tambourine offbeats.
   * *Stage 2 (Climax Drop)*: Erupts with heavy gated four-on-the-floor bass kicks and pumping saw-bass offbeats beneath the fingerpicked strings.
4. **Strict Boundary Clamping (Snare & Kick Alignment)**:
   * Percussion and bass tracks MUST have an explicit silent trigger (`pitch=0, volume=0`) written at the absolute tail boundary of every cell (`total_section_ticks - 10`) to satisfy timing validations and prevent timeline drift.

## 9. Expressive Build-to-Drop Dynamics (Crescendo Snare Rolls)
When transitioning from an acoustic intro to an intense drop section:
1. **Snare-Roll Acceleration**: Step snare triggers dynamically over the build section (e.g., Quarter notes $\to$ Eighth notes $\to$ Sixteenth notes).
2. **Volume Crescendo**: Scale note velocities smoothly upwards (e.g., $60 \to 108$) over successive sub-divisions to simulate increasing physical performance intensity.
3. **Pre-Drop Silence (The Vocal Gap)**: Cut all snare triggers completely during the final two sixteenth sub-divisions (e.g. last 240 ticks of a 4/4 bar). This creates a brief, tense pocket of absolute silence that dramatically increases the acoustic impact of the ensuing drop.
4. **Suspense Cymbal**: Trigger a crashing suspended cymbal (pitch 49) on the pre-drop silence boundary, allowing its decay tail to bleed across the drop transition.


