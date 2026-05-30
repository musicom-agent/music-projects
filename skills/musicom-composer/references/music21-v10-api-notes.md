# Music21 v10 API Notes

## Quick Reference

**Version:** 10.1.0 (installed via `pip3 install --target /opt/hermes/.venv/lib/python3.13/site-packages music21 numpy`)

## Breaking Changes from v8

### MajorScale is NOT iterable
```python
# v8 (worked):
for n in music21.scale.MajorScale("C4"): ...

# v10 (fails):
for n in music21.scale.MajorScale("C4"): ...  # TypeError

# v10 fix:
pitches = music21.scale.MajorScale("C4").getPitches()
```

### streamToMidiFile().write() signature changed
```python
# v8 (worked):
mf = music21.midi.translate.streamToMidiFile(stream)
mf.open(path, 'wb')
mf.write()
mf.close()

# v10 (fails):
mf = music21.midi.translate.streamToMidiFile(stream)
mf.open(path, 'wb')  # still works but not required
mf.write()           # TypeError: write() takes 1 positional argument

# v10 fix — two options:
# Option A: use fp= keyword
mf.write(fp=path)

# Option B: write directly (no open/close needed)
mf = music21.midi.translate.streamToMidiFile(stream)
with open(path, 'wb') as f:
    mf.write(f)

# Option C: just pass path to streamToMidiFile
# (if available in your version)
```

### Other v10 notes
- Chord.pitchNames still works: `chord.Chord(["C4","E4","G4"]).pitchNames`
- Stream iteration still works: `for n in stream: ...`
- note.Note and chord.Chord constructors are unchanged

## Pip Installation in Docker

The Hermes venv (`/opt/hermes/.venv/`) ships without pip. Fix:
```bash
# 1. Install system pip (if missing)
apt-get install -y python3-pip

# 2. Install into venv via --target (do NOT use venv pip directly)
pip3 install --target /opt/hermes/.venv/lib/python3.13/site-packages music21 numpy
```

## Verification

```python
import sys
sys.path.insert(0, "/opt/hermes/.venv/lib/python3.13/site-packages")
import music21
print(music21.__version__)  # Should print 10.1.0 or similar
```
