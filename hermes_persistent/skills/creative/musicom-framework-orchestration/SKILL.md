---
name: musicom-framework-orchestration
description: "Orchestration of musicom-composer workflows using Role-Based AI Agents (Theoretician, Melodist, Arranger), project setup, and publication pipelines."
version: 1.1.0
author: Musicom Agent
license: MIT
metadata:
  hermes:
    tags: [musicom, orchestration, counterpoint, DNA, matrix, automation, onboarding, flat.io, publication]
    related_skills: [musicom-composer, music-project-workflow, architecture-diagram]
---

# Musicom Framework Orchestration

Standardized multi-agent workflow for the Musicom music composition framework. This skill governs how Hermes internalizes specialized personas to execute complex, multi-layered musical tasks, from first-time onboarding through score publication.

## Orchestration Roles

### 1. Music Theoretician
- **Goal**: Establish the harmonic environment and rule sets.
- **Tasks**: Tonic selection, modal decisions (e.g. Dorian/Phrygian), and rule definition (e.g. "Always use inverse motion for bass").
- **Output**: Tonality JSON, Harmonic Matrix.

### 2. Melodic Composer (Melodist)
- **Goal**: Construct melodic DNA and rhythmic grooves.
- **Tasks**: Creating `PitchPattern` intervals and `RhythmPattern` Euclidean sequences (E(k, n)).
- **Output**: Melodic DNA scripts, Rhythmic Grids.

### 3. Arranger & Export Specialist
- **Goal**: Synthesize multi-track audio and manage project publication.
- **Tasks**: Implementing Matrix renders, applying `CounterpointTransformers`, and publishing dashboards.
- **Output**: Mixed audio, project index, notation exports.

## Project Organization & Structure

To ensure clarity for the user and autonomous agents, follow this rigorous directory structure:

### 1. Root Classification
- **/opt/data/repos/**: Reserved strictly for code repositories and framework libraries.
- **/opt/data/projects/**: Exclusive home for creative music projects. Standard naming: `NNN-kebab-name`.

### 2. Project Granularity
- **One Folder per Project**: Every music project must have exactly one top-level directory within `/opt/data/projects/`.
- **Standardized Content**: Every project should follow the `000-project-template` structure:
  - `src/`: Python composition/synthesis scripts.
  - `midi/`: Source and generated MIDI.
  - `audio/`: Rendered `.wav` and `.ogg` files.
  - `analysis/`: Visualizations and JSON data.
  - `index.html`: Project dashboard at the root.

### 3. Dashboard Centralization
- **Master Index**: Maintain a central `index.html` at `/opt/data/projects/` linking to all project pages.
- **Syncing**: Mirror creative work in `/opt/data/projects/` to `repos/musicom-agent/music-projects/` for hosting.

## Synthesis & Audio Standards

- **Default Pipeline**: `pretty_midi` (using bundled `TimGM6mb.sf2`) -> `soundfile` -> `ffmpeg` (OGG Opus).
- **Fallback When `music21`/`pretty_midi` Missing**: Use `mido` to create deterministic multitrack MIDI, then render with FluidSynth if available, normalize with `ffmpeg`, encode OGG/Opus, and delete raw intermediate WAV before publishing.
- **Acoustic Fidelity**: Strictly adhere to 5.5Hz vibrato at 0.8% depth for violin to maintain natural resonance.
- **Instrument Mapping**: Use General MIDI program numbers for standardized rendering.
- **Blues/Rock Apprenticeship Note**: For blues rock studies, model shuffle as exact triplet math (`2/3 + 1/3` beat), use 12-bar I-IV-V form, and publish Rhythm-DNA dashboards using high-contrast `█`/`░` markers. See `references/014-blues-rock-shuffle-session.md`.

## Shared Onboarding Flow

Use this subsection when adding a new human composer to the Musicom project.

### Composer Setup
- Confirm access to the canonical repositories.
- Verify the environment stack needed for symbolic logic and audio rendering.
- Start new work from the project template rather than improvising directory structure.
- Use absolute paths under `/opt/data/projects/` and `/opt/data/repos/`.
- Prefer OGG/Opus for Telegram delivery; keep WAV for archive/high-fidelity only.

### First DNA-Centric Run
1. Define pitch DNA in the composition script.
2. Define rhythm DNA with a Euclidean pattern.
3. Apply rules for harmonic direction and variation.
4. Render the project dashboard and audio artifacts.

## Onboarding Notes from `musicom-onboarding`

- Repository access commonly centers on the core logic repo and the portfolio/output repo.
- The environment checklist should explicitly verify the symbolic stack, audio stack, and FluidSynth fallback.
- Project bootstrapping should begin from the canonical project template, not an ad hoc folder.
- A first-pass render should produce a playable audio artifact plus a dashboard for inspection.

## Pitfalls & Permissions

- **Root Locks**: If skills like `musicom-composer` show permission errors, ownership may need to be fixed via container root.
- **Telegram Delivery**: Never send WAV; always convert to OGG/Opus for instant playback.
- **DNA Drift**: Ensure theory notes match code and rendered output.
- **Flat.io Publication Copy**: For rich scores, create a Flat.io-safe MusicXML copy before upload; if the dense master fails, upload the simplified copy instead.

## Publication and Score Sync

### Flat.io Integration
- Use a personal access token with Bearer auth.
- Prefer MusicXML when transferring notation to Flat.io.
- If the Flat.io SDK is flaky or dependencies are missing, verify with cURL.
- Keep the canonical full-fidelity local score; treat the cloud copy as a publication copy.

### Reference Material
- `references/014-blues-rock-shuffle-session.md` — blues-rock rhythm and dashboard notes.
- `references/flatio-safe-publication.md` — simplified upload checklist.
- `references/flatio-lead-sheet-recipe.md` — publish-copy pattern that succeeded.
- `references/flat-io-publish-2026-06-17.md` — token verification and score upload steps.
- `references/publish-safety.md` — publication safety checklist.
- `references/lead-sheet-lyrics-publish.md` — lyric-first export pattern.
- `references/musicom-onboarding.md` — composer onboarding notes and environment checklist.
