---
name: musicom-missing-link-plan
description: "Implementation plan to fix the vocal gap, render real-time grid visualizers, and establish DAW/MTC sync."
version: 1.0.0
author: "Musicom Agent"
metadata:
  hermes:
    tags: [plan, workflow, visualization, dsp, sync]
---

# Architecture Plan: Musicom Missing Links

## Area 1: Low-Memory Vocal Guide Synthesizer (The Vocal Gap)
Integrate a lightweight, local-first vocal guide oscillator using a singing formant filter pipeline. Avoids heavy DiffSinger RAM bounds.

### Implementation
- **Input**: MusicUnit containing melody track + parallel phonetic lyric string list.
- **Engine**: Formant-filtered subtractive synthesis (comb filter + resonant bandpass filters for vowels [a, e, i, o, u]).
- **Output**: Monophonic guide vocal `.wav` track mixed directly into final master.

---

## Area 2: Interactive High-Contrast Grid Visualizer (Live Feedback)
Real-time console-based ASCII tracker showing detailed grid state before WAV rendering.

### Visualization Structure
```text
[Section 1: Intro] [BPM: 120] [Mode: Phrygian]
Voice 1 (Lead)  : ██████░░████░░░░ (Density: 62%)
Voice 2 (Chord) : █░░░█░░░█░░░█░░░ (Density: 25%)
Voice 3 (Bass)  : █░░██░░██░░██░░░ (Density: 50%)
```

### Implementation
- Build Python validator printing live timelines to console prior to run execution.
- Implement automated `/opt/data/projects/.../Analysis/grid_visualization.txt` generation.

---

## Area 3: OSC / MIDI Time Code (MTC) Sync Bridge
Dynamic bidirectional clock sync between local algorithmic loops and running external DAWs.

### Implementation
- **Clock**: `python-osc` or `mido` virtual ports emitting MIDI Clock (0xF8) or MTC quarter-frame messages (0xF1).
- **Target**: Sync local engines with external environments (Reaper, Ableton, Bitwig).
#
