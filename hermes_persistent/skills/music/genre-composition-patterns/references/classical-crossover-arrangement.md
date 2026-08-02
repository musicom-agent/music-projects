# Classical Crossover Arrangement Reference

Derived from `studio_grand.mid` extension (8-bar piano sketch → 32-bar multi-instrument).

## Style Classification

**Classical Crossover**: Piano-led with orchestral accompaniment.
- Key: C major (bright, diatonic)
- Tempo: 110 BPM (moderate)
- Instrumentation: Piano, Strings, Bass, Drums, Flute (Lead), Flute (Countermelody)
- Harmony: Diatonic progressions (C-G-F-Am)
- Form: Intro(4) + V1(8) + Chorus(8) + V2(8) + Outro(4)

## Chord Voicings (from source MIDI)

| Chord | Bass | Notes |
|-------|------|-------|
| C | C2 (36) | C3 G3 C4 E4 (48, 55, 60, 64) |
| G | G2 (43) | G2 D3 G3 B3 (43, 50, 55, 59) |
| F | F2 (41) | F2 C3 F3 A3 (41, 48, 53, 57) |
| Am | A2 (45) | A2 E3 A3 C4 (45, 52, 57, 60) |

## Progression by Section

| Section | Bars | Chords |
|---------|------|--------|
| Intro | 1-4 | C C G G |
| V1a | 5-8 | C C G G |
| V1b | 9-12 | C C F C |
| ChA | 13-16 | F C G Am |
| ChB | 17-20 | F C G C |
| V2a | 21-24 | C Am G G |
| V2b | 25-28 | C Am F C |
| Outro | 29-32 | F C G C |

## Harmony Analysis (Bars 10-11)

**Context**: V1b, chord = C major [C3 G3 C4 E4]

**Lead melody** (ascending pattern):
- Beat 1: C4 (60) — ROOT ✓
- Beat 2: D4 (62) — 9th (passing tone) ✓
- Beat 3: E4 (64) — 3rd ✓
- Beat 4: F4 (65) — 4th/11th (passing tone) ✓

**Verdict**: Sound. Passing tones (D, F) are classical-acceptable over tonic. No harsh dissonances (no minor 2nds, no tritones).

## Progressive Dropout Order (Outro)

| Bar | Piano | Strings | Lead | Drums | Bass | Countermelody |
|-----|-------|---------|------|-------|------|---------------|
| 0 | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| 1 | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| 2 | ✓ | ✓ | — | ✓ | ✓ | — |
| 3 | ✓ | — | — | — | — | — |

**Logic**: Melodic voices exit first, rhythm section follows, harmonic foundation (piano) last.

## Strings Articulation Map

| Section | Articulation | Pattern |
|---------|-------------|---------|
| Intro | Fade in | Sustained, bars 2-3 only |
| V1a | Sustained pad | Whole notes |
| V1b | Staccato | Quarter notes |
| ChA | Tremolo | Eighth notes, ±10 vol modulation |
| ChB | Staccato | Quarter notes |
| V2a | Sustained pad | Whole notes |
| V2b | Staccato | Quarter notes |
| Outro | Fade out | Sustained, bars 0-2 only |
