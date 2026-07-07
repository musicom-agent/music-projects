# Music21 v10 API Notes

## Quick Reference

**Version:** 10.1.0 (installed via `pip3 install --target /opt/hermes/.venv/lib/python3.13/site-packages music21 numpy`)

## Breaking Changes from v8

### MajorScale is NOT iterable
```python
# v8 (worked):
for n in music21.scale.MajorScale("C4"): ...

# v10 (fails):
for n in music21.scale.MajorScale("C4"): ...  # TypeError: 'MajorScale' object is not iterable

# v10 fix — use .getPitches():
pitches = music21.scale.MajorScale("C4").getPitches()
```

### KeySignature → Key (string names no longer accepted)
```python
# v8 (worked):
melody.append(music21.key.KeySignature('C'))  # sharp count

# v10 (fails):
melody.append(music21.key.KeySignature('C'))  # ValueError: invalid literal for int() with base 10: 'C'

# v10 fix:
melody.append(music21.key.Key('C'))  # Key() accepts string names
```

### streamToMidiFile().write() — use writestr()
```python
# v8 (worked):
mf = music21.midi.translate.streamToMidiFile(stream)
mf.open(path, 'wb')
mf.write()
mf.close()

# v10 (all these fail):
mf = music21.midi.translate.streamToMidiFile(stream)
mf.write(fp=path)              # TypeError: unexpected keyword argument 'fp'
mf.open(path).write()          # TypeError: expected str, bytes or os.PathLike
mf.write()                     # TypeError: No file is open

# v10 fix — ONLY working method:
mf = music21.midi.translate.streamToMidiFile(stream)
midi_bytes = mf.writestr()  # returns raw MIDI bytes
with open(path, 'wb') as f:
    f.write(midi_bytes)
```

### Other v10 notes
- `Stream` iteration still works: `for n in stream: ...`
- `note.Note` and `chord.Chord` constructors are unchanged
- `chord.Chord(["C4","E4","G4"]).pitchNames` still works
- `stream.write('musicxml', fp=path)` still works
- `mf.open()` expects a string path (file object fails), `write()` takes no args

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
