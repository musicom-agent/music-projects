---
name: musicom-method-master-map
description: Master map of Musicom composition and analysis methods, including roundtrip, daily selection, and researched method variants.
version: 0.1.0
author: Musicom Agent
license: MIT
---

# Musicom Method Master Map

## Environment & Implementation
- **Python:** 3.13 strictly required.
- **Dependency Management:** Use `uv` with an editable install (`pip install -e .`). 
- **Core Dependencies:** `numpy`, `mido`, `scipy`, `music21`, `networkx`, `pandas`, `matplotlib`.
- **Constraint:** `librosa` and `numba` are incompatible with Python 3.13; bypass for core generation.
- **Import Pattern:** Use absolute imports (`from musicom.rules import ...`) and ensure `sys.path.insert(0, '/opt/data/repos')` in standalone scripts.

## Workflow: The 5-Step Loop
1. **Environment Setup**
   ```bash
   source /opt/data/repos/musicom/.venv/bin/activate
   export PYTHONPATH=$PYTHONPATH:/opt/data/repos
   ```

2. **Rule Integration**
   - **Active Usage:** Do not hard-code notes. Use `musicom.rules.progression` for chord degrees and `musicom.rules.counterpoint` to validate intervals.
   - **Verification:** Always run `Counterpoint(unit1, unit2).has_parallel_perfect_intervals()` to ensure classical voice-leading compliance.

## Purpose
Single source of truth for all researched Musicom composition, variation, and reverse-analysis methods.

## Scope
Covers methods for:
- composition
- variation generation
- reverse analysis
- roundtrip comparison
- daily iterative selection
- prosody / lyrics-driven mapping
- hierarchical diffusion-style composition

## Method Index

### 001 Skeleton-First Refinement
- Input: DNA, pitch seed, rhythm seed
- Output: UnitMatrix skeleton
- Best for: baseline form-first drafting
- Roundtrip fit: high

### 002 Markov Probabilistic Transitions
- Input: prior state / local context
- Output: probabilistic pitch and harmony continuation
- Best for: local variation, stochastic fill
- Roundtrip fit: medium

### 003 Genetic Genome Selection
- Input: candidate population
- Output: selected and mutated winner
- Best for: version evolution, compare-select loops
- Roundtrip fit: high

### 004 Prosodic Narrative Coupling
- Input: lyrics, stress, punctuation, narrative arc
- Output: melody, rhythm, contour, call-response mapping
- Best for: lyric-first composition
- Roundtrip fit: high

### 005 Prosodic Syntax Mapping
- Input: punctuation, syntax, clause boundaries
- Output: cadence types, rests, contour shifts
- Best for: text-to-phrase translation
- Roundtrip fit: high

### 006 Cadence and Closure Mapping
- Input: phrase endings, closure strength
- Output: tonic / non-tonic closure behavior
- Best for: end-phrase planning
- Roundtrip fit: high

### 007 Narrative Arc Register Planning
- Input: story arc / section arc
- Output: register and tension distribution
- Best for: large-scale form control
- Roundtrip fit: medium-high

### 008 Call-Response Voice Allocation
- Input: dialogue / phrase pairs
- Output: distributed voice roles and alternation
- Best for: conversational music, antiphony
- Roundtrip fit: high

### 009 Rhyme Density Control
- Input: rhyme clusters, word repetition density
- Output: rhythmic density and accent shaping
- Best for: lyrical propulsion
- Roundtrip fit: medium-high

### 010 Hierarchical Diffusion Composition
- Input: multi-level symbolic plan
- Output: macro form, meso skeleton, lead sheet, accompaniment
- Best for: whole-song hierarchical generation
- Roundtrip fit: medium

### 011 Euclidean Groove Locking
- Input: pulse count, hit count, offset
- Output: locked rhythmic cycle
- Best for: percussion, ostinato, groove design
- Roundtrip fit: high

### 012 Inversion / Retrograde / Sequencing Transform
- Input: motif or pitch set
- Output: transformed variant family
- Best for: classical development and motif mutation
- Roundtrip fit: high

### 013 Negative Harmony Mapping
- Input: tonal center and harmonic axis
- Output: mirrored harmony set
- Best for: tonal contrast and reharmonization
- Roundtrip fit: medium

### 014 Ostinato Constraint Writing
- Input: loop cell or repeating cell
- Output: stable repeated pattern under variation above
- Best for: trance, modal, accompaniment beds
- Roundtrip fit: high

### 015 Groove-Locked Pattern Writing
- Input: rhythmic anchor + syncopation rules
- Output: stable groove patterns across sections
- Best for: dance music and section glue
- Roundtrip fit: high

### 016 Cascaded Diffusion Hierarchical Composition
- Input: 4-level symbolic hierarchy
- Output: macro-form, meso-development, lead sheet, accompaniment
- Best for: whole-song generation
- Roundtrip fit: medium-high

### 017 Schillinger System of Musical Design
- Input: Generator numbers (a, b) and axis trajectories
- Output: Resultant rhythms, coordinate-projected pitches, strata density
- Best for: Systematic/mathematical algorithmic composition
- Roundtrip fit: High (mathematical precision)

## Recommended Routing

### Composition
- Start with 001 for stable DNA
- Use 012 for motif development
- Use 011, 014, 015 for groove and repetition
- Use 004, 005, 008, 009 for lyric-driven work
- Use 010 or 016 for large-scale hierarchical planning
- Use 003 for compare-select evolution

### Reverse Analysis
- Audio -> transcription -> feature extraction -> 001 or 004 mapping
- Use 002 for probabilistic inference on uncertain regions
- Use 011, 014, 015 to recover rhythmic identity
- Use 012 and 013 to explain transformation relations

### Roundtrip Evaluation
- Compare candidates with the same analysis pass
- Score pitch, rhythm, harmony, structure, texture, and text fit
- Feed winner back into next cycle

## Folder Merge Rule
All method notes, reports, and research summaries must live under one merged folder:
- `references/methods/`

Recommended contents:
- `index.md` — master map
- `daily.md` — daily research log
- `roundtrip.md` — compare-select-feedback protocol
- `analysis/` — reverse-analysis notes
- `composition/` — forward composition notes
- `prosody/` — lyric and text mapping notes
- `hierarchical/` — diffusion / multi-level planning notes
- `methods/` — generic research notes (e.g. `method-015-schillinger.md`)

## Operating Rule
If a new method appears in any report, add it to this master map and place the source note in the merged folder.

## Research-to-Database Bridge
When a method is appended to `methods_db.md`, mirror the method name and short summary into the master map in the same session when practical. Keep the master map as the index; keep long method prose in the database file. If the append flow needs verification or notification handling, use the Musicom Composer support note: `references/method-addition-verification.md`.
