# Matrix Architecture for Automated Composition

Important Musicom vocabulary correction: `MusicMatrix` / `UnitMatrix` is reserved for the core Musicom structure, not a generic table.

From `axelwiertz/musicom` (`structures/matrix.py::UnitMatrix`):
- **Rows**: voices / pitch-space layers.
- **Columns**: measures or sections / time-space segments.
- **Cells**: `MusicUnit` objects or measure-level musical material.

The genre matrix is a semantic layer that fits inside this: rhythm/bass/harmony/melody/timbre tags annotate the actual voice-by-measure MusicMatrix cells.

## Implementation Pattern
```python
MATRIX = {
    "Lead": [[60, 62], [64, 65]], # Measure 1: C, D; Measure 2: E, F
    "Bass": [[36, 36], [41, 41]]  # Measure 1: C, C; Measure 2: F, F
}
```

## Advantages
1. **Structural Clarity**: Simplifies the orchestration of complex layers.
2. **Role Delegation**: Theoretician defines the chord row, Melodist defines the lead row, Arranger merges them.
3. **Modular Transformations**: Easy to transpose or repeat specific measures by manipulating the list indices.
