# Reverse Music Analysis: MIDI Deconstruction

## Core Extraction Pattern
To extract "DNA" from a MIDI source without specialized symbolic libraries:

1. **Harmonic Fingerprinting**:
   - Use `mido` to group `note_on` events into windows (e.g., 240 ticks / 8th notes).
   - Convert note values to pitch classes (`midi % 12`).
   - Count the frequency of pitch sets to identify primary chords and modal interchange.
   - Example: Frequent `[2, 5, 10]` indicates Bb Major (bIII in G major context).

2. **Rhythmic Density Mapping**:
   - Count notes per bar to categorize sections (e.g., Intro < 4, Chorus > 12).
   - Visualize as a UnitMatrix density grid using high-contrast ASCII:
     ```
     Bar 01: [████░░░░░░░░░░░░]
     ```

3. **Pitch Contour Analysis**:
   - Calculate interval vectors `[all_pitches[i] - all_pitches[i-1]]`.
   - Identify "stagnant" sections (0 intervals) vs "dramatic leaps" (>7 semitones) to match artist vocal/melodic style.

## Workflow: Backward Composition
1. File -> Detect Tonic -> Identify Scale.
2. Segment into bars -> Measure density per bar.
3. Map densities to UnitMatrix sections (Verse, Chorus).
4. Use extracted pitch sets (Harmonic DNA) as chord pools for the `Variation Generator`.
