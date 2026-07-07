---
name: midi-analysis
description: "Analyze existing MIDI files: parse tracks, notes, tempo, key, rhythm distribution, melodic contour, note frequency, and duration patterns. Uses the mido Python library."
version: 0.2.0
author: community
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  commands: [python3]
  pip_packages: [mido]
references: []
---

# MIDI File Analysis

## When to Use

- User asks to analyze, inspect, or review a `.mid`/`.midi` file
- User wants to understand structure, notes, tempo, key, or rhythm of an existing MIDI
- User wants a quick breakdown of a MIDI file's contents

**Not for composing** — use `musicom-composer` for generating new music. This skill is for *reading/analyzing* existing MIDI files only.

## Prerequisites

Install mido if not available:
```bash
pip3 install mido --break-system-packages
```

Note: `mido` is a system Python package. The venv at `/opt/hermes/.venv/` may not have it. Use `/usr/bin/python3` (system Python) for mido-based scripts.

## Pitfalls — MIDO API Gotchas

- **`mido.tempo2bpm()`** — the function is `tempo2bpm`, NOT `tempo_to_bpm` (which doesn't exist).
- **No `mido.mid2note()`** — mido does NOT provide a built-in MIDI-to-note-name converter. You must build one:
  ```python
  NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
  def mid_to_note(n):
      return f"{NOTE_NAMES[n%12]}{n//12-1}"
  ```
- **`key_signature` returns a string** — not an int. `msg.key` is something like `'F'`, not `5`. Do not compare it with `>= 0` as an integer.
- **Sandbox environment** — Hermes's execute_code sandbox may lack system pip-installed packages. Use `terminal` with `/usr/bin/python3` instead.
- **⚠ Pitch classes are ABSOLUTE (C=0), NOT relative to key center** — This is THE most common gotcha in chord-tone analysis. A common trap: labeling pc 0 as "A (root)" when analyzing in A, but pc 0 is always C. The mapping is C=0, C#=1, D=2, D#/Eb=3, E=4, F=5, F#/Gb=6, G=7, G#/Ab=8, A=9, A#/Bb=10, B=11. For key-of-A analysis: A=pc9, C=pc0, D=pc2, Eb=pc3, E=pc4, G=pc7. Write chord pitch-class definitions in absolute terms (e.g. A7 = {9, 1, 4, 7}), not relative intervals.

## Analysis Checklist

When analyzing a MIDI file, cover these areas:

1. **File structure** — type (0/1/2), track count, ticks per beat
2. **Track listing** — name, message count, message type breakdown
3. **Tempo map** — all `set_tempo` messages, BPM at each point
4. **Time signatures** — all `time_signature` messages
5. **Key signatures** — all `key_signature` messages
6. **Program changes** — instrument assignments per channel
7. **Note analysis per channel** — unique notes, note names, velocity range, note-on count, note duration stats, note range
8. **Note frequency** — how often each note appears (with bar chart)
9. **Duration distribution** — categorize into 16th/8th/quarter/half/whole with percentages
10. **Melodic contour** — show first ~40 notes with delta times
11. **Marker/section analysis** — if `marker` meta events exist, report each section's bar range, duration, note count, density, dominant pitch classes, and orchestration footprint
12. **Density and tutti analysis** — count notes per 4/8-bar window and identify large simultaneous attacks (e.g. 12+ notes at same tick) to support orchestration critique
13. **Chromatic load** — compare pitch classes against declared key/scale and report outside-scale percentages per section; use as a clue, not a verdict (MIDI lacks enharmonic spelling)
14. **Summary** — total duration in beats/seconds, total note events, channels used, average BPM
15. **Chord-tone analysis (harmony vs lead)** — For multi-track compositions with a defined chord progression:
    - Map each bar to its chord (pitch class set in ABSOLUTE terms, C=0)
    - Per track, count what percentage of notes fall inside vs outside the current chord
    - Flag non-chord tones as either "inside scale" (stylistic passing tones/blues notes) or "truly outside"
    - Per-bar breakdown reveals section-level chord-tone density patterns
    - Cross-track clash detection: flag simultaneous m2/M7/tritone intervals across tracks as potential voicing issues
    - Use `scripts/harmony_lead_check.py` for automated analysis
16. **Form-length check** — Compare per-track end ticks and bar counts. If melody extends past accompaniment, call it a form mismatch or missing loop, not a timing bug. When user asks for "other bars", inspect the full progression, not only the reported trouble spots.

## Getting the MIDI File

If the file isn't already on this system, try these methods in order:

### Method 0: Chat platform blocks `.mid`
Some chat/document gateways reject raw MIDI uploads with "Unsupported document type '.mid'". Do not keep asking for a plain `.mid` upload. Ask for one of these instead:
- zip the MIDI and upload the `.zip`
- rename a copy to `.mid.txt` if `.txt` is accepted
- provide a download link
- place the file on disk and give the path, then search that directory with `find /path -iname '*.mid*'`

### Method 1: User pastes inline
For small MIDI files (< 100KB), the user can paste the raw binary/base64 directly in chat. Save to a temp path and analyze.

### Method 2: File already on disk
Ask the user for the path, or check if an email with the file was just sent.

### Method 3: Email via himalaya
If the user emailed the MIDI to a configured himalaya account:
```bash
# List recent emails with attachments
himalaya envelope list --output json 2>&1 | grep has_attachment

# Download attachment (replace <ID> with the email ID)
himalaya attachment download <ID> -d /tmp

# Find the downloaded file
find /tmp -name "*.mid*" -newer /tmp -ls
```
Then analyze with `/usr/bin/python3` as usual.

### Method 4: User uploads to container
User sends the file via scp, or places it in a known directory. Ask for the path.

## Typical Workflow

For quick facts, use the inline workflow below. For deeper review of a full orchestral/long-form MIDI, use the packaged helper first:

```bash
# Structural analysis
/usr/bin/python3 /opt/data/skills/midi-analysis/scripts/midi_deep_review.py /path/to/file.mid
```

It prints file structure, tempo/time/key maps, marker-defined section stats, chromatic-load estimates, density windows, track ranges, and large simultaneous attacks. Use those outputs to make musical critique concrete rather than impressionistic.

For chord-tone analysis (harmony vs lead melody):

```bash
# With explicit chord progression
/usr/bin/python3 /opt/data/skills/midi-analysis/scripts/harmony_lead_check.py \
  /path/to/file.mid \
  --chords "A7,A7,D7,A7,D7,A7,E7,A7" \
  --scale-pcs "9,0,2,3,4,7"
```

The `--scale-pcs` flag is optional but critical for style-specific genres (blues, jazz, modal). It separates authentic non-chord passing tones from truly outside-scale errors. A Blues Hexatonic in A = pcs 9,0,2,3,4,7 (A,C,D,Eb,E,G).

```bash
# Auto-infer from key signature (simple I-IV-V-I)
/usr/bin/python3 /opt/data/skills/midi-analysis/scripts/harmony_lead_check.py /path/to/file.mid
```

## Output Format

Present results as plain text (terminal-friendly):
- Use sections with `=== HEADER ===`
- Note names as `C4`, `D#3` etc.
- Include percentages for distributions
- Brief plain-text summary at the end
- Keep it readable — no markdown tables

## Common Insights to Report

- **Range** — narrow (< 1 octave) = simple/pedagogical; wide (> 2 octaves) = complex
- **Velocity uniformity** — all same velocity = no dynamics (common in student MIDI)
- **Note frequency** — identifies tonal center (most frequent note)
- **Duration balance** — mostly quarter notes = straightforward; many 16ths = busy/ornate
- **Key vs actual notes** — does the melody actually use the declared key?
- **Long-form structure** — marker durations and note counts reveal whether a piece behaves like sonata, suite, fantasia, tone poem, etc.; do not force a formal label that the data does not support
- **Chromatic load by section** — high outside-scale percentage can signal development/crisis, modal mixture, enharmonic spelling loss, or incoherence; phrase it as evidence to inspect, not automatic error
- **Tutti density** — many 12+ note simultaneous attacks often means overused block orchestration; recommend reserving true tutti for structural arrivals and staggering/layering other attacks
- **Percussion realism** — unusually dense timpani/bass drum repeated notes can sound machine-like in MIDI; evaluate avg duration/velocity and suggest thinning if it masks orchestral form
- **Blues/style-specific context** — "outside chord" does NOT mean "wrong" in blues, jazz, or modal music. In Delta blues, the melody deliberately plays b3 (C natural) against the chord's major 3rd (C#). This b3-vs-M3 cross-relation is the defining harmonic gesture. Always check non-chord tones against the composition's declared scale BEFORE flagging them as errors. A 40-60% chord-tone rate in a blues lead is authentic; 100% would be sterile.

## Reference: MIDI Program Numbers (Common)

| Prog | Instrument |
|------|-----------|
| 0 | Acoustic Grand Piano |
| 24 | Acoustic Guitar (Nylon) |
| 25 | Acoustic Guitar (Steel) |
| 40 | Violin |
| 48 | Accordion |
| 56 | Trombone |
| 73 | Electric Piano |
| 80 | Lead (square) |
| 88 | Synth Pad |
| 128 | All drums (channel 10) |
