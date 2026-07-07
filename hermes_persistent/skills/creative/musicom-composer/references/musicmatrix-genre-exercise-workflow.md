# MusicMatrix Genre Exercise Workflow

Session-derived workflow from Project 014: genre education through Musicom `UnitMatrix` + `music21` renders.

## Core semantic correction

`MusicMatrix` / `UnitMatrix` is reserved for the Musicom structure:

- rows = voices / pitch-space layers
- columns = measures or sections / time-space segments
- cells = `MusicUnit` bar/section material

A genre matrix is an annotation layer over this grid, not a competing generic table.

Example mapping:

```text
MusicMatrix row 1 = percussion/foot pulse -> Rhythm DNA
MusicMatrix row 2 = bass voice            -> Bass DNA
MusicMatrix row 3 = harmony/chords        -> Harmony DNA
MusicMatrix row 4 = lead voice            -> Melody DNA
```

## Python environment split

In the verified container:

```text
/usr/bin/python3:
  mido: yes
  numpy: yes
  music21: no

/opt/hermes/.venv/bin/python3:
  music21 10.1.0: yes
  numpy: yes
  mido: no
```

Use `/opt/hermes/.venv/bin/python3` for `music21` score/MIDI generation. Use `/usr/bin/python3` only for fallback mido scripts unless packages are aligned.

## Direct UnitMatrix loading workaround

Full `from structures import UnitMatrix` may fail because `structures/__init__.py` imports optional theory dependencies such as `networkx` through `pitchclass.py`.

For matrix-only composition, load only the needed files from `axelwiertz/musicom`:

```python
from pathlib import Path
import sys, types, importlib.util

MUSICOM = Path('/opt/data/repos/musicom')

# timegrid imports visualization.Cycle; stub if not needed
vis = types.ModuleType('visualization')
class Cycle:
    def __init__(self, *a, **k): pass
    def show(self, *a, **k): pass
vis.Cycle = Cycle
sys.modules.setdefault('visualization', vis)

pkg = types.ModuleType('structures')
pkg.__path__ = [str(MUSICOM / 'structures')]
sys.modules['structures'] = pkg

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

load('structures.timegrid', MUSICOM / 'structures' / 'timegrid.py')
unit_mod = load('structures.unit', MUSICOM / 'structures' / 'unit.py')
matrix_mod = load('structures.matrix', MUSICOM / 'structures' / 'matrix.py')
MusicEvent = unit_mod.MusicEvent
MusicUnit = unit_mod.MusicUnit
UnitMatrix = matrix_mod.UnitMatrix
```

## Construct UnitMatrix safely

Passing nested `MusicUnit` lists to `UnitMatrix(data=rows)` can fail with NumPy inhomogeneous-shape errors. Prefer explicit shape + `set_unit`:

```python
def make_matrix(rows):
    m = UnitMatrix(shape=(len(rows), len(rows[0])))
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            m.set_unit((r, c), cell)
    return m
```

## MusicEvent type pitfall

`MusicEvent` stores fields in NumPy scalar types. Cast to builtin `int` before passing pitches/velocities to `music21.note.Note` or `music21.chord.Chord`:

```python
pitches = [int(e.pitch) for e in events]
velocity = int(sum(int(e.volume) for e in events) / len(events))
```

Without this, `music21.chord.Chord([np.uint8(50), ...])` can throw:

```text
TypeError: Could not process input argument 50
```

## Iterative exercise pattern

1. Start with short A/B/C compare:
   - A = base genre body (Balfolk jig)
   - B = contrast genre force (Jazz harmonic pull)
   - C = hybrid row substitution
2. Ask 4 structured feedback fields:
   - most danceable
   - strongest harmonic pull
   - hybrid identity
   - next transformation
3. Change only requested rows:
   - "brighter" -> harmony/melody color row
   - "more dance" -> percussion/bass rows
   - "add melody answer" -> lead row and form rows
   - "AABB" -> column expansion/repetition with variation
4. Preserve accepted qualities explicitly.

## Telegram delivery preference

For music iterations in Telegram, send one audio MEDIA item only.

- If comparing versions, send only the compare file as MEDIA.
- Mention alternate files/MIDI paths as text only.
- Do not send both compare and clean render unless the user asks.

## Verified render chain

```text
UnitMatrix/MusicUnit -> music21 Score -> MIDI -> FluidSynth FluidR3_GM.sf2 -> WAV -> ffmpeg OGG/Opus
```

Always verify:

```bash
ffmpeg -v error -i <audio.ogg> -f null -
wc -c <file.mid>
```
