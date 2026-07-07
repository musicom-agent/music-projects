# Musicom Style Knowledge Base (KB) Standard

## Organization
Every Style must follow the folder structure:
`/opt/data/projects/Styles/[StyleName]/Analysis/`
- `patterns.md`: Concrete rhythm, pitch, and structural patterns.
- `kb_theory.md`: Deeper theoretical foundations (scale origins, rhythmic gravity).

## Standard Patterns
- **Jazz**: Swing, Bebop, ii-V-I.
- **Flamenco**: 12-beat Compas, Phrygian Dominant, Rasgueado.
- **Irish Traditional**: Jig (6/8), Reel (4/4), Mixolydian/Dorian, Cuts/Rolls ornamentation.
- **Latin**: Clave (3-2, 2-3), Montuno, syncopated bass.

## Encoding Guidelines
- **Rhythm**: Define Euclidean parameters (onsets, timesteps) or fixed beat indices (Compas accents).
- **Pitch**: Map characteristic scales to MIDI.
- **Texture**: Define VST patches and articulation rules.
