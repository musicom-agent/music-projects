# Rock Apprenticeship Study Pattern

Use this when user wants to learn rock while composing, not just receive theory.

## Session shape

1. Create a numbered project under `/opt/data/projects/NNN-rock-*`.
2. Teach by building one short study: riff → backbeat → bass lock → power chords → form.
3. Export paired files: `.mid` for DAW + `.ogg` for Telegram playback.
4. Add `index.html` dashboard with high-contrast Rhythm DNA grids using `█` and `░`.
5. Keep lesson notes short and action-oriented: concept, pattern grid, listening task, next subgenre choice.

## First study defaults

- Genre: classic hard rock / garage rock
- Key: E minor / E blues
- Tempo: 128 BPM
- Meter: 4/4
- Form: Intro x2, Verse x4, Chorus x4, Outro x2
- Scale: E blues = E G A Bb B D

## Rock teaching primitives

- Backbeat: snare on beats 2 and 4.
- Kick anchors 1 and 3, then locks to bass/riff.
- Hi-hat/ride supplies steady eighth-note grid.
- Power chord: root + fifth (+ octave); no third, so melody supplies major/minor color.
- Riff test: recognizable after two loops, rhythm has at least one rest, playable in guitar/bass register.
- Blues flat fifth (`Bb` in E) gives grind; use briefly unless aiming for heavy chromatic tension.

## Rhythm DNA starter

```text
Count:  1 & 2 & 3 & 4 &
Kick:   █ ░ ░ ░ █ ░ ░ ░
Snare:  ░ ░ █ ░ ░ ░ █ ░
Hat:    █ █ █ █ █ █ █ █
```

2-bar riff grid:

```text
Slots:  1 & 2 & 3 & 4 & | 1 & 2 & 3 & 4 &
Onset:  █ ░ █ █ ░ █ █ ░ | █ ░ █ ░ █ █ ░ █
Pitch:  E - E G - A Bb- | B - D - B A - E
```

## Environment fallback

If `pretty_midi`, `soundfile`, or `mido` are absent in the active Hermes venv, use `music21` for MIDI export and pure Python `wave` + `math` synthesis for a quick preview. Distortion can be approximated with `tanh()` clipping over summed harmonics. This is not HQ synthesis, but works for fast lesson previews. Prefer FluidSynth when available for final renders.

## Next-step prompt

After delivering Study 01, ask user to pick a branch:

- blues rock
- punk
- hard rock
- grunge
- prog rock
- folk-rock fusion
