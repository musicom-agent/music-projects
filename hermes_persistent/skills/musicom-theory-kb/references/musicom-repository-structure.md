# Musicom Repository Structure — 2026-06-27 Update

## Current State

### Local Clone
- **Path**: `/opt/data/repos/musicom/`
- **Structure**: Flat layout with subdirectories at root level
- **PYTHONPATH**: Must include `/opt/data/repos/musicom` for imports to work

### Directory Structure
```
/opt/data/repos/musicom/
├── __init__.py                    # Makes repo root a package
├── pyproject.toml                 # Package metadata
├── structures/                    # Core data structures
│   ├── __init__.py
│   ├── base.py
│   ├── instrument.py
│   ├── matrix.py                 # UnitMatrix class
│   ├── pitch.py
│   ├── pitchclass.py
│   ├── time.py                   # TimeConverter class added 2026-06-27
│   ├── timegrid.py               # Fixed broken visualization import
│   └── unit.py                   # MusicEvent, MusicUnit
├── workflows/                     # High-level workflows (NEW 2026-06-27)
│   ├── __init__.py
│   └── unitmatrix_composer.py    # UnitMatrixComposer class
├── ai/                           # AI extensions
│   ├── __init__.py
│   └── core/
│       └── tet_system.py
├── musicom/                      # Nested package (legacy)
│   └── ...
└── utilities/
    ├── __init__.py
    └── helpers.py
```

## Import Patterns

### From Repo Root
```python
# Working directory: /opt/data/repos/musicom
from structures import MusicEvent, MusicUnit, UnitMatrix, TimeConverter
from workflows.unitmatrix_composer import UnitMatrixComposer
```

### From External Scripts
```python
import sys
sys.path.insert(0, '/opt/data/repos/musicom')
from structures import MusicEvent, MusicUnit, UnitMatrix
```

### From PYTHONPATH
```bash
export PYTHONPATH=/opt/data/repos/musicom:$PYTHONPATH
python3 your_script.py
```

## 2026-06-27 Additions

### New Files
1. **`workflows/unitmatrix_composer.py`** - High-level UnitMatrix workflow
2. **`workflows/__init__.py`** - Package init

### Modified Files
1. **`structures/time.py`** - Added `TimeConverter` class
2. **`structures/matrix.py`** - Added validation methods to `UnitMatrix`
3. **`structures/timegrid.py`** - Removed broken `visualization.cycle` import
4. **`structures/pitchclass.py`** - Lazy import for helpers to avoid circular deps
5. **`pyproject.toml`** - Added `workflows` to packages list

### New Classes

#### TimeConverter (`structures/time.py`)
- `events_to_delta(events)` → List[(delta, pitch, duration)]
- `unit_to_delta_events(unit)` → List[(delta, pitch, duration)]
- `align_units_to_track(units)` → List[MusicEvent]
- `track_to_midi_messages(delta_events, program, channel)` → List[mido.Message]
- `validate_track_length(tracks)` → bool
- `get_track_length(events)` → int

#### UnitMatrix Methods (`structures/matrix.py`)
- `get_row_length(row)` → int
- `get_all_row_lengths()` → List[int]
- `validate_timing()` → bool
- `get_row_events(row)` → List[MusicEvent]
- `get_all_track_events()` → List[List[MusicEvent]]
- `get_track_length()` → int
- `to_midi_track_messages(row, program, channel)` → List[mido.Message]

#### UnitMatrixComposer (`workflows/unitmatrix_composer.py`)
- `create_matrix(num_voices, num_sections)`
- `add_voice(name, program, channel)`
- `add_section(name, bars)`
- `set_unit(row, col, unit)`
- `validate()` → (bool, str)
- `to_midi(path)`
- `get_track_length_ticks()` → int
- `get_track_length_bars()` → float

### Helper Functions (`workflows/unitmatrix_composer.py`)
- `create_blues_form_matrix(bpm)` → (UnitMatrixComposer, dict)
- `create_empty_unit()` → MusicUnit
- `create_note_unit(pitch, duration_ticks)` → MusicUnit
- `create_chord_unit(pitches, duration_ticks)` → MusicUnit

## Known Issues

### Relative Import Problem
The repo has files at both:
- `/opt/data/repos/musicom/structures/` (flat)
- `/opt/data/repos/musicom/musicom/structures/` (nested)

This causes confusion. The **flat structure** is the working one.

### Package Installation
`pip install -e .` may fail because:
1. `musicom.ai` package listed but `musicom/ai/` directory exists
2. Missing `workflows` in original pyproject.toml
3. Broken imports in some modules

**Workaround**: Use flat imports with PYTHONPATH, or fix pyproject.toml.

## Migration Notes

### Old Workflow (Before 2026-06-27)
```python
# Manual track building, no validation
# Easy to create timing mismatches
```

### New Workflow (2026-06-27+)
```python
from workflows.unitmatrix_composer import UnitMatrixComposer

composer = UnitMatrixComposer(bpm=80)
composer.create_matrix(3, 3)
composer.add_voice('Lead', program=30)
composer.add_voice('Bass', program=33)
composer.add_voice('Drums', channel=9)

# Fill cells...

# CRITICAL: Validate before export
if composer.validate()[0]:
    composer.to_midi('output.mid')
```

## Repository Tiers (Reminder)

1. **Core Library** (`axelwiertz/musicom`): Canonical Python package
   - Structures, AI, rules, generators
   - Local: `/opt/data/repos/musicom/`

2. **Project Portfolio** (`musicom-agent/music-projects`): Creative work
   - Numbered projects (027-delta-blues, 039-electric-blues, etc.)
   - MIDI/audio renders, analyses, dashboards

3. **Workspace** (`musicom-agent/musicom-agent`): Agent skills/docs
   - Agent documentation, skill references
   - Session artifacts, handover docs

**Rule**: Do NOT embed project folders inside workspace repo.
