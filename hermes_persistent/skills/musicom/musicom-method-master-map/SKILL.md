---
name: musicom-method-master-map
type: Method Map
title: Musicom Method Master Map
description: Canonical index of stochastic, rules-based, and nature-led algorithmic music composition methods.
resource: https://github.com/axelwiertz/musicom
tags: [music, algorithms, methods, master-map, okf]
timestamp: 2026-07-15T20:45:00Z
---

# Musicom Method Master Map (OKF)

Every algorithmic composition method used inside the Musicom framework must map to one of three core paradigms:

## 1. Stochastic (Probabilistic)
*   **002 Markov Transitions:** Generates probabilistic harmonic/melodic paths based on state weights.
*   **023 Tendency Masking:** Generates pitch clouds bounded by moving corridors $L(t)$ and $U(t)$.
*   **039 Spectral Morphology Analysis (SMA):** Derives musical material from FFT analysis of source audio — spectral peaks drive pitch, spectral flux drives rhythm, inharmonicity ratio drives harmony, and band energy drives texture.
*   **041 Ant Colony Optimization Path Finding (ACOPF):** Swarm of ant agents traverse musical graphs depositing pheromones on successful paths. Iterative optimization converges on coherent melodies, voice-leading, and chord progressions while evaporation prevents stagnation.

## 2. Rules-Based (Deterministic)
*   **001 Skeleton-First:** Forms structural grids from DNA pitch and rhythm seeds.
*   **011 Euclidean Groove:** Evaluates rhythmic cycles using pulse and hit counts.
*   **025 Xenakis Sieve:** Generates scales/grids using modular congruence formulas.
*   **032 Isorhythmic Talea-Color Mapping (ITCM):** Decouples rhythmic loop (talea) and pitch loop (color) of coprime lengths to generate non-repeating shifting melodic motifs.
*   **033 Wave Function Collapse Grid Synthesis (WFCGS):** Collapses a grid of voice and section superpositions using strict vertical/horizontal adjacency constraints.
*   **034 Probabilistic Context-Free Grammar (PCFG) Recursion:** Recursively expands non-terminal symbols into hierarchical pitch, rhythm, and structural trees using Chomskyan rewrite rules with weighted branching probabilities.
*   **044 Persistent Homology and Topological Data Analysis (PHTDA):** Embeds musical parameters as point clouds, constructs Vietoris-Rips simplicial complexes at multiple scales, computes Betti numbers and persistence diagrams to extract topological features (connected components, loops, voids). Persistent features map to structural coherence; transient features drive ornamentation and texture.

## 3. Nature-Led (Physical/Emergent)
*   **026 DPSM (Phase-Shift Minimalism):** Emerges dynamic polyrhythms via misaligned phase offsets.
*   **030 Reaction-Diffusion Turing Patterns (RDTP):** Generates musical structures and textures from localized chemical concentrations evolving over a 2D reaction-diffusion grid (Gray-Scott model).
*   **031 Swarm Intelligence Flocking (Boids):** Simulates Reynolds' flocking algorithm (separation, alignment, cohesion) to guide multiple autonomous musical agents in a multi-dimensional pitch-time-velocity space.
*   **035 Physarum Polycephalum Transport Network Optimization (PPTNO):** Simulates slime mold protoplasmic tube growth, thickness, and contractive oscillations between pitch-coordinate food sources to optimize path-based voice leading and rhythmic density.
*   **036 Abelian Sandpile Avalanche Rhythmics (ASAR):** Simulates sand accumulation, toppling thresholds, and critical avalanche cascades on a 2D grid to model musical tension, rhythmic triggers, and polyphonic density.
*   **037 FitzHugh-Nagumo Neural Spiking (FHNS):** Simulates membrane potential dynamics and refractory recovery periods of neural spiking cells to trigger rhythmic impulses, modulate velocities, and map voltages to pitch contours.
*   **038 Kuramoto Oscillator Phase Synchronization (KOPS):** Simulates coupled limit-cycle oscillators to model collective synchronization, rhythmic lock-in, and harmonic transitions.
*   **043 Strange Attractor Trajectory Mapping (SATM):** Uses deterministic chaotic dynamical systems (Lorenz, Rössler attractors) to generate bounded, aperiodic trajectories in 3D phase space. Coordinates map to pitch, velocity drives rhythm, attractor topology governs macro-form.

## Method Hybridization Patterns

Sparse rhythmic methods (011 Euclidean, 032 Isorhythmic) produce staccato, gap-filled textures. User rejected sparse-only output as "staccato instead of flowing."

**Solution**: Combine sparse rhythmic methods with continuous fill methods:
- **Sparse rhythmic layer**: Euclidean groove (kick/snare), isorhythmic talea (melodic motif)
- **Continuous fill layer**: DPSM phase-shifted arpeggios (3 layers offset by 1/3 beat), sustained string pads, walking bass fills
- **Result**: Rhythmic interest from sparse method + flowing texture from continuous method

**Example**: Disco v2 (Euclidean only) → 75% drums, 25% bass/strings = staccato. Disco v3 (Euclidean + DPSM) → 75% drums, 100% bass/arpeggios/strings = flowing groove.

**Rule**: When using methods 011, 032, or other sparse rhythmic generators, always add at least one continuous layer (026 DPSM, sustained pad, or walking bass) to maintain flow.

---

## Technical Pitfall: MIDI Tail Truncation
When compiling cells, short active phrases stop playing before the global track boundary, causing DAW timeline drift on export.
*   **Fix:** Append an absolute silent padding event (`pitch=0, volume=0`) at `total_section_ticks - 1` to ensure perfect track-length symmetry across all rows.
