# Genre Pattern Matrix Exercises

Use when the user wants to learn genres and compose from them using Musicom patterns and a matrix.

## Core frame

A genre is a bundle of inspectable DNA patterns:

- Rhythm DNA: pulse, subdivision, swing/dotted/Euclidean grid, metrical gravity.
- Pitch DNA: scale/mode, contour, interval vocabulary, chromatic color.
- Harmony DNA: chord loop, function/modal behavior, cadence or pedal.
- Bass DNA: root/drone/walk/ostinato behavior.
- Timbre DNA: acoustic/electronic/orchestral/hybrid role.
- Form DNA: AABB, 12-bar, AABA, build/drop, narrative arc.

A composition matrix makes it teachable:

```text
Rows: Rhythm | Bass | Harmony | Melody | Timbre | Form
Cols: Bar 1  | Bar 2 | Bar 3   | ...
```

Each cell states what that layer does in that bar. Compose by filling cells, then render.

## First exercise template: Balfolk vs Jazz vs Hybrid

Create three short 8-bar studies plus one compare render:

1. **Balfolk Dorian Jig**
   - D Dorian, 6/8, jig gravity `█░░█░░`.
   - Chords: `Dm | C | Dm | G | Dm | C | G | Dm`.
   - Melody: stepwise fiddle, accents on counts 1 and 4.
   - Teaching goal: body pulse + modal color.

2. **Jazz ii-V-I Swing**
   - C major, 4/4 swing, backbeat on 2 and 4.
   - Chords: `Dm7 | G7 | Cmaj7 | Cmaj7 | Em7 | A7 | Dm7-G7 | Cmaj7`.
   - Melody: target chord tones on strong points; approach tones on weak points.
   - Teaching goal: harmonic pull and resolution.

3. **Hybrid Balfolk-Jazz**
   - Keep Balfolk 6/8 body and folk-simple melody.
   - Borrow Jazz color harmony: `Dm9 | Cmaj7 | Dm9 | G13 | ...`.
   - Teaching goal: separate rows that define genre identity from rows that add color.

## Delivery pattern

For each study project:

- Make `Notes/genre-kb.md` with genre DNA summary.
- Make `Analysis/rhythm-dna.md` with high-contrast `█` / `░` grids.
- Make `Exercises/exercise-01-*.md` with listening tasks.
- Export paired `.mid` and `.ogg` for every version.
- Add a dashboard `index.html` linking audio and MIDI.

## Guided listening questions

Ask the user to answer:

1. Most danceable: A / B / C?
2. Strongest harmonic pull: A / B / C?
3. Hybrid feels: more Balfolk / more Jazz / balanced?
4. Next transformation: darker / brighter / more dance / more jazz?

Map answers to next version:

- darker -> lower b6 / Aeolian color / lower register.
- brighter -> Lydian #4 or higher register.
- more dance -> stronger metrical gravity and percussion on genre pulses.
- more jazz -> more chromatic approach tones, extensions, turnarounds.

## Minimal implementation notes

If `music21`, `pretty_midi`, or `soundfile` are missing but `mido`, `fluidsynth`, and `ffmpeg` exist:

1. Generate MIDI with `mido`.
2. Render with `fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 input.mid -F output.wav -r 44100`.
3. Convert with `ffmpeg -i output.wav -codec:a libopus -application voip -b:a 64k output.ogg`.
4. Verify OGG with `ffmpeg -v error -i output.ogg -f null -`.

This proved sufficient for a genre-matrix exercise when only `mido` + `numpy` + FluidSynth CLI were available.