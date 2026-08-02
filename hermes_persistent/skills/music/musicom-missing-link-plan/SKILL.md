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

> **STATUS: IMPLEMENTED (Phase 4/5).** All three areas now ship as real,
> tested code in `/opt/data/repos/musicom`. Use these entry points:
> - Area 1 vocal: `ai/generators/vocal_synth.py` — `FormantVocalGuide.render_melody(unit, path, vowels=[...])` and `.render_syllable(freq, dur, vowel, path)`. Sine fallback when scipy missing; stdlib `wave` write fallback.
> - Area 2 grid: `ai/utils/visualizer.py` — `render_grid(matrix, ...)` (string, with per-voice Density %) + `write_grid_visualization(matrix, path)`.
> - Area 3 sync: `ai/integration/daw_sync.py` — `DAWClockBridge(bpm).run_clock(pulses, dry_run=)`, 24 PPQN MIDI clock, headless fallback.
> - Bonus: `workflows/paradigm_compare.py` (Stochastic/Rules/Nature compare) + `workflows/provenance.py` (AI-labeling sidecars).
> Tests: `tests/test_phase4_features.py`, `tests/test_phase5_companion.py`. Golden-file regression: `tests/test_harness_golden.py`.
> See repo `AGENTS.md` for the canonical usage guide.

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
