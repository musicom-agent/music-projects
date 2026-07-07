# Country Music Pattern Logic

## Rhythm Patterns
### Boom-Chicka (2/4 Feel)
- The core of traditional country and bluegrass.
- **Beat 1**: Root Bass (Boom)
- **Beat 2**: High-string strum or Snare (Chicka)
- **Beat 3**: Fifth Bass (Boom)
- **Beat 4**: Strum or Snare (Chicka)
- **Implementation (Ticks)**: Onsets at `[0, 480, 960, 1440]` in a 480 PPQ grid.

## Harmony Patterns
### I - IV - V - I (The Three Chords)
- Standard 16-bar flow (AABB variation):
  - Bars 1-4: I - I - IV - I
  - Bars 5-8: I - I - V - I
  - Bars 9-12: IV - IV - I - I
  - Bars 13-16: V - V - I - I

## Voice Roles
- **Lead (Accordion/Fiddle)**: Program 21. Uses 1-3-5-3 arpeggio contours.
- **Harmony (Acoustic Guitar)**: Program 24. Strummed triads on the backbeat (2 and 4).
- **Pad (Choir)**: Program 52. Subdued sustained triads (velocity ~50-60) to fill mid-range.
- **Drums**: Channel 10. Alternating Kick (36) and Snare (38).

## Registration
- **Bass**: G1 - G2
- **Chords**: G3 - B4
- **Lead**: G4 - D5
- **Choir**: G3 - G4 (Sustained)
