# Matrix & Rule Engine Implementation (2026-05-21)

## Architecture: Role-Play Matrix

The workflow uses an internal Role-Play model where the agent differentiates its logic into three personas to handle complex composition:

1. **Theoretician (Scale/Rule Logic)**:
   ```python
   class Theoretician:
       def decide_tonality(self):
           return {"tonic": "D", "mode": "Dorian", "scale": [...]}
   ```

2. **Melodist (DNA/Pattern Logic)**:
   ```python
   class Melodist:
       def create_patterns(self):
           pitch_pattern = [0, 2, 4, 3, 3] # Scale index intervals
           rhythm_steps = [1, 0, 0, 1, 0, 0, 1, 0] # Euclidean 3:8
           return pitch_pattern, rhythm_steps
   ```

3. **Arranger (Matrix/Render Logic)**:
   ```python
   MATRIX = {
       "Lead": [[...], [...]], 
       "Pad": [[...], [...]], 
       "Bass": [[...], [...]]
   }
   ```

## Algorithmic Intent (Transformation Rules)

Instead of static note entry, the Theoretician defines **Transformation Rules** applied to a **Melodic DNA** string:

| Rule | Description |
| :--- | :--- |
| `FOLLOW_CHORD` | $(DNA\_offset + chord\_root) \pmod{scale\_len}$ |
| `INVERT_CONTOUR` | $(chord\_root - DNA\_offset) \pmod{scale\_len}$ |
| `TRANSPOSE_UP_N` | $(chord\_root + DNA\_offset + N) \pmod{scale\_len}$ |

## Dashboard Publishing

Requirement: Generate a standalone `dashboard.html` in the project outputs directory using high-contrast themes (Slate-950, Cyan) to visualize the Role-Play status and current Matrix state.
