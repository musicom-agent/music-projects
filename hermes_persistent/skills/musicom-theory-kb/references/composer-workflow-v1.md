# Musicom Composer Workflow Framework (v1.0)

This framework provides a repeatable pipeline for moving from theoretical seeds to playable dashboards.

## Phase 1: The Seed (Input & Intent)
- **Source**: Check `musicom@wiertz.tech` via `himalaya` or direct prompts.
- **Definition**: Establish Scale/Mode (e.g., D-Dorian), Meter (4/4, 7/8), and BPM.
- **Notion**: Sync entry to 'Musicom Project Master'.

## Phase 2: Structural Pillars (Generation)
- **Pillar 1 (Pitch)**: Generate chords (e.g., `Scale7ChordDegree`) and melody (e.g., `MarkovChain`).
- **Pillar 2 (Rhythm)**: Map pitches to time grids using Euclidean rhythms (e.g., 3,8 Tresillo). Apply velocity envelopes.

## Phase 3: Synthesis & Audition (Instant Playback)
- **Synthesis**: Use `musicom_synthesis.py` (Additive/Subtractive or Karplus-Strong).
- **Format**: WAV first, then convert to OGG (Opus) via `ffmpeg -codec:a libopus -application voip -b:a 48k`.
- **Delivery**: Send via Telegram using `MEDIA:/path/to/file.ogg`.

## Phase 4: Visualization & Analysis (Dashboard)
- **Location**: `projects/[id]-[name]/index.html`.
- **Aesthetic**: Slate-950 background, Cyan (#22d3ee) and Rose (#fb7185) accents.
- **Components**: Analytical overview (Scale/Progression), Piano Roll, Volume Graph.

## Phase 5: Handoff (DAW Integration)
- **Repo**: Commit to `music-projects` or `musicom-agent`.
- **External**: Provide BandLab revision link for human touch.

---
*Derived during Project Dorian walkthrough (May 2026).*
