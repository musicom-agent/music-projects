# Concept: Modal Interchange as Pattern Gating

## Overview
Modal interchange is the practice of borrowing chords from a parallel mode (sharing the same tonic). In the Musicom framework, this is treated as a logic-gate that allows Chromatic Voice Leading without losing the sense of "Key."

## The Logic-Mechanical Split
| Layer | Domain | Description |
|---|---|---|
| **Logic (The What)** | Modal Interchange | Substituting a Pattern (e.g., swapping a Major IV for a Minor iv). |
| **Mechanics (The How)** | Chromatic Voice Leading | The specific semitone movement (e.g., A -> Ab) that resolves the tension. |

## The 12-TET Distance
Standard Diatonic Distance (Major):
- IV [5, 9, 0]
- V [7, 11, 2]
- Move: [5->7, 9->11, 0->2] (All whole steps/diatonic)

Interchange Distance (Borrowing from Minor):
- iv [5, 8, 0]
- V [7, 11, 2]
- Move: [5->7, 8->7/11?, 0->2]
- Key Move: **8 -> 7** (Ab -> G). This is a chromatic pull that provides stronger directional "gravity" than A -> G.

## Implementation in Scripts
When generating interchange, prioritize the voice leading of the "signature note" (the 3rd of the borrowed chord) to resolve by semitone to a stable degree in the parent scale.
