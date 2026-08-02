# Multi-Method Form Composition

Building large forms (32-64+ bars) where each section uses a different algorithmic method.

## Pattern: Section-per-Method

Each section gets its own builder function returning one MusicUnit per voice. The main script assembles them into the UnitMatrix.

```python
def build_section_a():
    """Markov transitions — probabilistic melody."""
    section_ticks = BAR * 16
    # ... generate events ...
    piano_unit = MusicUnit(events=pad_to_section(piano_events, section_ticks))
    strings_unit = MusicUnit(events=pad_to_section(string_events, section_ticks))
    bass_unit = MusicUnit(events=pad_to_section(bass_events, section_ticks))
    perc_unit = MusicUnit(events=pad_to_section(perc_events, section_ticks))
    return piano_unit, strings_unit, bass_unit, perc_unit

# Repeat for each section with different method...

# Assembly
piano_a, strings_a, bass_a, perc_a = build_section_a()
piano_b, strings_b, bass_b, perc_b = build_section_b()
# ...

composer.add_section("A", bars=16)
composer.add_section("B", bars=16)
composer.fill_voice_section("Piano", "A", piano_a)
composer.fill_voice_section("Strings", "A", strings_a)
# ... fill all voice×section combos
```

## Method Selection Guide (by form function)

| Form Function | Recommended Methods | Why |
|---------------|-------------------|-----|
| Exposition / Theme | 002 Markov, 001 Skeleton-First | Clear melodic identity, probabilistic variation |
| Development I | 032 Isorhythmic Talea-Color, 033 WFCGS | Structural complexity, non-repeating patterns |
| Development II | 026 DPSM Phase-Shift, 030 Reaction-Diffusion | Textural density, continuous flow |
| Recapitulation / Tension | 025 Xenakis Sieve, 036 Sandpile | Modular pitch sets, building energy |
| Coda / Resolution | 001 Skeleton-First DNA, 029 L-System | Return to seed material, closure |

## Key Modulation Arc

Classical forms modulate across sections. Plan key changes:
- Section A: Tonic (C major)
- Section B: Subdominant or relative minor (F major or A minor)
- Section C: Dominant or distant key (G major or E minor)
- Section D: Return to tonic (C major)
- Section E: Tonic resolution (C major)

## Density Targets by Section

| Section | Target Density | Rationale |
|---------|---------------|-----------|
| Exposition | 60-75% | Clear melody + accompaniment, room to breathe |
| Development | 85-100% | Maximum textural interest, continuous flow |
| Recap | 75-90% | Building tension, denser than exposition |
| Coda | 50-70% | Resolution, progressive dropout |

## Verified Example: 64-bar Classic (5 methods)

File: `projects/Styles/Classic/classical_64bar_5methods/v1/compose.py`

| Section | Bars | Method | Key | Density |
|---------|------|--------|-----|---------|
| A | 16 | Markov Transitions | C major | 66% |
| B | 16 | Isorhythmic Talea(7)×Color(5) | F major | 66% |
| C | 16 | DPSM Phase-Shift (3 layers) | G major | 100% |
| D | 8 | Xenakis Sieve {x%3=0}∪{x%5=2} | C major | 75% |
| E | 8 | Skeleton-First DNA transforms | C major | 55% |

Voices: Strings (48), Piano (0), Bass (32), Percussion (ch9).
Result: 16.9KB MIDI, 2:24 duration, validation PASS.
