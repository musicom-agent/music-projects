# UnitMatrix-first composer workflow

## Core rule
Use `UnitMatrix` as the top-level composition model.

- Rows = voices / pattern layers
- Columns = form sections / time blocks
- Cells = explicit musical material built from `PitchPattern` and `RhythmPattern`

## Canonical build order
1. Define project brief: genre, mood, key, tempo, meter, form.
2. Build UnitMatrix rows and columns.
3. Fill each cell with pitch and rhythm patterns.
4. Render MIDI by emitting low-level MIDI events.
5. For percussion, write explicit GM channel 10 note events.
6. Verify MIDI before audio render.
7. Render OGG from the same MIDI path.
8. Promote the draft into a real numbered project with README, dashboard, analysis, notes, scripts.

## Percussion rule
Do not trust high-level score metadata for percussion routing. Use low-level MIDI event writing.

- Channel: 9 (GM Channel 10)
- Notes: standard GM percussion keys
- Verify: parser must find percussion note_on events before render

## Section rule
For 2-minute pieces, do not loop one pattern.
Use an explicit form, usually:

- Intro
- A
- B
- A'
- Outro

## Verification rule
The workflow is not complete until:

- MIDI exists at the final project path
- percussion events exist in the exported MIDI
- OGG is rendered from that same MIDI path
- project dashboard exists
- generator script is saved in the project
