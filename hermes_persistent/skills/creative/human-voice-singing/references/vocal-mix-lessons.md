# Vocal Mix & Phrasing (2026-05-25)

## Mix Hierarchy
The user preferred the **Voice as Lead** (80% volume) and **Instrument as Backing** (20% volume) for the "Rainbow" project. Previous 70/30 or 50/50 mixes were not as effective for lyrical clarity.

## Word Simulation via Vowel Shifts
The transition between vowels is the key to recognizable words in formant synthesis:
1. **"Over"**: Needs a fast transition from **[O]** (onset) to **[E]** (offset).
2. **"Rainbow"**: Needs a shift from **[A]** (rain-) to **[O]** (-bow).

## Envionment Pitfall
`scipy` is installed in `/opt/data/.local/lib/python3.13/site-packages`. 
Always use:
```python
import sys
sys.path.append('/opt/data/.local/lib/python3.13/site-packages')
from scipy import signal
```
Failure to add the path will cause `ModuleNotFoundError`.
