# 026 — Bossa Nova UnitMatrix

## Concept
Bossa Nova study built from a UnitMatrix-first workflow. Rows = Guitar, Bass, Percussion. Columns = Intro, A, B, A', Outro.

## DNA
- **PitchPattern:** retrograde-inverted bossa motif, clamped to playable guitar register.
- **RhythmPattern:** syncopated bossa pulse with explicit percussion row.
- **UnitMatrix:** rows are voices, columns are form sections.
- **Meter:** 4/4
- **Tempo:** 80 BPM
- **Form:** Intro (4) -> A (12) -> B (8) -> A' (12) -> Outro (4)

## Instrumentation
- Nylon guitar
- Acoustic bass
- Bossa percussion: kick, side stick, hi-hat, conga, shaker

## Files
- [MIDI](MIDI/v1_bossa_nova_unitmatrix.mid)
- [Audio](Audio/v1_bossa_nova_unitmatrix.ogg)
- [Renders](Renders/v1_bossa_nova_unitmatrix.wav)
- [Analysis](Analysis/v1_analysis.md)
- [Generator](Scripts/generate_v1.py)

## Workflow correction
This project uses the corrected composer workflow:
1. build UnitMatrix
2. emit MIDI with explicit percussion channel 9
3. verify MIDI percussion events
4. render audio from the exact same MIDI path
5. promote into a numbered real project
