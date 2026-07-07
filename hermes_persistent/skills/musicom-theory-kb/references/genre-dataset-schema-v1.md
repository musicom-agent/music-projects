# Genre-Pattern Dataset Schema (Project 016)

## Overview
This schema is used in project `016-genre-pattern-dataset` to systematically catalog musical DNA across global genres.

## JSON Structure

```json
{
  "genre": "string",
  "subgenre": "string",
  "patterns": {
    "pitch": {
      "name": "string",
      "intervals": "list[int]",
      "contour": "string",
      "description": "string"
    },
    "rhythm": {
      "name": "string",
      "onsets": "int",
      "steps": "int",
      "dna": "string",
      "metrical_gravity": "list[float]"
    },
    "timbre": {
      "instrument": "string",
      "adsr": [attack, decay, sustain, release],
      "vibrato_hz": 5.5,
      "vibrato_depth": 0.008,
      "harmonic_profile": "string"
    }
  },
  "musicmatrix_mapping": {
    "rows": ["Lead", "Harmony", "Bass", "Percussion"],
    "cols": 8
  }
}
```

## Constants & Calibration
- **Vibrato Baseline**: 5.5Hz at 0.8% depth.
- **Rhythm Markers**: `█` (onset), `░` (rest).
- **Pitch Contours**: U (Up), D (Down), L (Leap), S (Same).
