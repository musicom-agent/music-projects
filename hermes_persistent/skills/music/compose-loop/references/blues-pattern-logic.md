# Blues Pattern Logic — 5 Core Patterns for UnitMatrix

Key: C Blues (C Eb F F# G Bb). Shuffle feel 2:1 (long=160, short=80 ticks at 480tpb).

## Pattern 1: 5th–6th–♭7th Shuffle (Lead / Guitar comping)
Root+5th power chord, pinky alternates 6th and ♭7th.
```
C5 → C6 → C♭7 → C6  (swing rhythm)
```
**Tick layout per beat pair (long-short):**
- Beat N: Root+5th (long 160 ticks)
- Beat N+: 6th or ♭7th (short 80 ticks)
- Alternate 6th ↔ ♭7th on successive offbeats

**Voice mapping:** Lead (TRUMPET or raw program=30 for guitar), or Chords (PIANO).

## Pattern 2: Walking Bass Line (1-3-5-6-♭7)
Ascending/descending arpeggio with passing tones.
```
Ascending:  C → E → G → A → B♭ → A → G → E
Descending: B♭ → G → E → C → (chromatic approach) → C → E → G
```
**Per bar:** 8 swing eighth notes. Alternate up/down on successive bars.
**Voice:** Bass (BASS instrument, octave 2).

## Pattern 3: Boogie-Woogie Bassline
Continuous rolling left-hand pattern.
```
Option A (octave rock): Low C → High C → Low C → High C ...
Option B (5th-6th rock): C → G → C → A → C → G → B♭ → F
```
**Per bar:** 8 swing eighths. Bass voice, octave 1-2.

## Pattern 4: Block Chords (Triplet Pulse / Slow Blues)
Full dom7 chords struck on triplet subdivisions.
```
C7: C-E-G-B♭ block, pulsing 1-and-a 2-and-a ...
```
**Tick layout:** triplet = 160 ticks. Accent beat 1, pulse through.
**Voice:** Chords (PIANO).

## Pattern 5: Blue-Note Sliding / Grace Notes (♭3→3)
Expressive lead: slide from minor 3rd to major 3rd, then resolve.
```
C → (E♭ grace → E) → G → B♭
```
**Implementation:** Short grace note (80 ticks, vol 70) → target (240 ticks, vol 90) → resolve (480 ticks).
**Voice:** Lead.

## Shuffle Rhythm Constants (480 tpb, 120 BPM)
```python
EIGHTH = 240
LONG_EIGHTH = 160   # 2/3 of beat
SHORT_EIGHTH = 80   # 1/3 of beat
QUARTER = 480
HALF = 960
```

## Drum Pattern (Shuffle)
- **Ride (51):** every 8th in swing (long-short)
- **Snare (38):** beats 2 & 4
- **Kick (36):** beats 1 & 3
- **Hi-hat (42):** beats 2 & 4 (with snare)

## 12-Bar Blues Progression (C)
```
| C7  | F7  | C7  | C7  |
| F7  | F7  | C7  | G7  |
| F7  | C7  | G7  | C7  |
```
For 32-bar form: repeat AABA or expand with turnaround variations.

## Chord Tone Reference (C Blues)
| Chord | Root | 3rd | 5th | ♭7 |
|-------|------|-----|-----|----|
| C7 | C (48/60) | E (52/64) | G (55/67) | B♭ (58/70) |
| F7 | F (53/65) | A (57/69) | C (60/72) | E♭ (63/75) |
| G7 | G (55/67) | B (59/71) | D (62/74) | F (65/77) |
