# MusicMatrix Genre Matrix Workflow

Session learning: Project 014 converted a genre education matrix into the reserved Musicom `UnitMatrix` / `MusicMatrix` model.

## Canonical semantics

Source repo:

```text
/opt/data/repos/musicom
```

Core files:

```text
structures/unit.py    -> MusicEvent, MusicUnit
structures/matrix.py  -> UnitMatrix
```

Reserved meaning:

```text
Rows    = voices / pitch-space layers
Columns = measures or sections / time-space segments
Cells   = MusicUnit bar material
```

Genre matrices should be treated as semantic overlays on this grid, not as a separate generic table.

Example mapping:

```text
MusicMatrix row       Genre annotation
Foot Pulse / Drums -> Rhythm DNA
Bass Voice         -> Bass DNA
Harmony Voice      -> Harmony DNA
Lead Voice         -> Melody DNA
Pad/Texture        -> Timbre DNA
```

## Python environment split

System Python:

```text
/usr/bin/python3
mido: yes
numpy: yes
music21: no
```

Hermes venv:

```text
/opt/hermes/.venv/bin/python3
music21 10.1.0: yes
numpy: yes
mido: no
pip: no
```

Use Hermes venv for `music21` export. Use system Python for existing mido fallback scripts unless mido is installed into the venv.

## Direct-load workaround for Musicom core classes

Full `from structures import ...` can fail because `structures/__init__.py` imports optional theory dependencies such as `networkx` through `pitchclass.py`. For MusicMatrix-only work, load only required files.

Pattern:

```python
import sys, types, importlib.util
from pathlib import Path

MUSICOM = Path('/opt/data/repos/musicom')

# Stub visualization.Cycle for timegrid.py if needed.
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
MusicEvent, MusicUnit, UnitMatrix = unit_mod.MusicEvent, unit_mod.MusicUnit, matrix_mod.UnitMatrix
```

## UnitMatrix construction pitfall

Do not instantiate with nested `MusicUnit` lists if cells are heterogeneous; `np.asarray(data)` may raise shape errors.

Use explicit object-shaped matrix:

```python
def make_matrix(rows):
    m = UnitMatrix(shape=(len(rows), len(rows[0])))
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            m.set_unit((r, c), cell)
    return m
```

## MusicEvent numeric pitfall

`MusicEvent` stores values in numpy uint types. Convert to plain `int` before using with music21:

```python
pitches = [int(e.pitch) for e in events]
vel = int(sum(int(e.volume) for e in events) / len(events))
```

Otherwise music21 can reject values such as `np.uint8(50)` with `TypeError: Could not process input argument 50`, and velocity sums can overflow.

## Export pipeline

1. Build a `UnitMatrix` where each row is a voice and each column is a measure.
2. Convert each `MusicUnit` cell into `music21.note.Note` or `music21.chord.Chord` using column offset.
3. Create a `music21.stream.Score` with one `Part` per matrix row.
4. Export MIDI using music21 v10 API:

```python
mf = midi.translate.streamToMidiFile(score)
Path(out).write_bytes(mf.writestr())
```

5. Render MIDI to audio:

```bash
fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 input.mid -F output.wav -r 44100
ffmpeg -y -i output.wav -codec:a libopus -application voip -b:a 64k output.ogg
```

## Project 014 pattern

Exercise 1 used three matrices:

```text
A Balfolk rows: Foot Pulse | Bass Voice | Harmony Voice | Lead Voice
B Jazz rows:    Ride+Backbeat | Walking Bass | Piano Harmony | Sax Lead
C Hybrid rows:  Jig Pulse | Modal Bass | Jazz Color Harmony | Folk Lead
```

Hybrid operation:

```text
Keep Balfolk rows: rhythm, bass, lead contour
Replace/extend row: harmony -> Dm9, Cmaj7, G13
```

This gives a controllable genre exercise: change one MusicMatrix row at a time and listen to identity shift.
