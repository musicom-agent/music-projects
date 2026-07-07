# Session Notes: Role-Based Framework & Rule Engine (2026-05-21)

## Context
User requested a CrewAI-style workflow for music composition. Since external agents weren't directly controllable, we implemented an internal role-delegation pattern.

## Theoretician's Insights
- **Patterns as DNA**: A motif is a "Scale-Index Sequence" independent of the root.
- **Harmonic Windows**: Chords are temporary windows through which the DNA is viewed.
- **Transformations**: Inversion, Retrograde, and Transposition are the primary "Rules" for generating variation.

## Architecture
Local library extension created at `/opt/data/projects/composer-crew-framework/lib/musicom/` to bypass permission issues with `/root/musicom`.

- `patterns/pitch_pattern.py`: Implements `PitchPattern` with `.invert()` and `.retrograde()`.
- `rules/genre_rules.py`: Implements `GenreRules` for Jazz/Ambient constraints.
- `rule_engine_composer.py`: Demonstrates the mapping of "Transformation Rules" to "Melodic DNA".
