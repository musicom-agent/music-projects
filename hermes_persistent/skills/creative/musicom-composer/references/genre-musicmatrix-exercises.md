# Genre MusicMatrix Exercises — Project 014 Session Notes

Use this when teaching genres through Musicom composition exercises.

## Core framing

- `MusicMatrix` / `UnitMatrix` is reserved Musicom vocabulary.
- Rows = voices / pitch-space layers.
- Columns = measures or sections / time-space segments.
- Cells = `MusicUnit` bar/measure material.
- A genre matrix is a semantic education overlay on top of MusicMatrix cells, not a separate competing structure.

Example mapping:

```text
MusicMatrix row 1 = percussion/pulse voice -> Rhythm DNA
MusicMatrix row 2 = bass voice             -> Bass DNA
MusicMatrix row 3 = harmony voice          -> Harmony DNA
MusicMatrix row 4 = lead voice             -> Melody DNA
MusicMatrix row 5 = counter/pad voice      -> Timbre/Form support
Columns          = bars or sections
```

## Musicom repo import workaround

For `axelwiertz/musicom`, local path used:

```text
/opt/data/repos/musicom
```

`structures/__init__.py` imports optional theory dependencies such as `networkx`. In restricted Hermes venv, this can fail even when `UnitMatrix`, `MusicUnit`, and `MusicEvent` are usable.

Workaround: load only needed files directly.

```python
import sys, types, importlib.util
from pathlib import Path

MUSICOM = Path('/opt/data/repos/musicom')

# timegrid.py imports visualization.Cycle; stub when only unit/matrix are needed
vis = types.ModuleType('visualization')
class Cycle:
    def __init__(self, *args, **kwargs): pass
    def show(self, *args, **kwargs): pass
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

Create matrices with object cells via `shape`, not raw nested lists, because `np.asarray(data)` can infer an inhomogeneous shape when cells contain `MusicUnit` objects with different event counts.

```python
def make_matrix(rows):
    m = UnitMatrix(shape=(len(rows), len(rows[0])))
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            m.set_unit((r, c), cell)
    return m
```

## Python environment discovery

On this stack, `music21` was available in Hermes venv, not system Python:

```text
/opt/hermes/.venv/bin/python3  -> music21 10.1.0, numpy yes, mido no
/usr/bin/python3               -> mido yes, numpy yes, music21 no
```

Use `/opt/hermes/.venv/bin/python3` for music21/MusicMatrix work. Use system `python3` for mido fallback only.

`music21` v10 MIDI export worked with:

```python
from music21 import midi
mf = midi.translate.streamToMidiFile(score)
Path(path).write_bytes(mf.writestr())
```

## Genre exercise workflow

1. Build a MusicMatrix with voice rows and bar columns.
2. Add genre tags in docs/dashboard as semantic overlay: Rhythm DNA, Bass DNA, Harmony DNA, Melody DNA, Timbre/Form.
3. Generate one short study first, then iterate from user feedback.
4. Change one or two matrix rows per iteration.
5. Keep each iteration teachable: state exactly which row changed and why.

Project 014 examples:

- Exercise 1 Balfolk/Jazz/Hybrid:
  - A = Balfolk rhythm + modal melody.
  - B = Jazz swing + ii-V-I harmonic pull.
  - C = hybrid: Balfolk rhythm/lead with Jazz color harmony.
  - Later v4 = AABB + bass variation.
- Exercise 2 Classical:
  - Motif `U U D = G A B A`.
  - Rows: motor Alberti, functional bass, harmony blocks, counterline, motif lead.
  - Columns: 8-bar period; bars 1-4 antecedent, bars 5-8 consequent.

## Telegram delivery preference

Generate all artifacts, but send only **one** `MEDIA:` soundfile per turn unless user explicitly asks for more.

- For version comparison: send the compare OGG only.
- For final clean render: send the final OGG only.
- Mention alternate MIDI/OGG paths as text.

This avoids Telegram clutter while preserving dual-export discipline.
