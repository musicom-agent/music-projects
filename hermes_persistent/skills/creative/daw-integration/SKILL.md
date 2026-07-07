---
name: daw-integration
description: "DAW integration options for headless Docker AI music composition — MusicXML, MIDI export, FluidSynth, BandLab, Flat.io, OSC, and SoundFont pipelines."
version: 1.0.0
author: Musicom Agent
license: MIT
metadata:
  hermes:
    tags: [daw, midi, fluidsynth, musescore, bandlab, flat.io, osc, soundfont, music, composition]
    related_skills: [musicom-framework-orchestration, musicom-theory-kb, songsee]
---

# DAW Integration for Musicom Agent

DAW integration strategies for the Musicom AI composition workflow in a headless Docker environment.

## Environment Reality Check (Verified May 2026)

### Currently Installed (Verified May 2026)
| Tool | Status | Notes |
|------|--------|-------|
| ffmpeg 7.1 | ✅ | WAV↔OGG conversion, web-sample fetch |
| music21 10.1.0 | ✅ | Theory, score analysis, MusicXML export |
| musicpy 7.12 | ✅ | Chord/melody gen, MIDI I/O |
| mido | ✅ | Low-level MIDI read/write |
| numpy 2.4.5 | ✅ | Raw additive/subtractive synthesis |
| **pretty_midi** | ✅ | MIDI build + SF2 synthesis (bundled TimGM6mb.sf2) |
| **soundfile** | ✅ | WAV I/O |
| **librosa 0.11.0** | ✅ | Audio feature extraction, chroma, tempo |
| pyfluidsynth | ⚠️ installed but needs libfluidsynth.so (no root) | Use pretty_midi instead |
| fluidsynth binary | ❌ | Needs apt-get (no root) |
| GM SoundFont (system) | ❌ | TimGM6mb.sf2 bundled in pretty_midi is sufficient |
| songsee | ❌ | Not installed — use librosa for audio analysis |

## Install Priority (Run Once to Unlock Full Stack)

```bash
# SoundFont rendering pipeline (most impactful upgrade)
apt-get install -y fluidsynth fluid-soundfont-gm
pip install pyfluidsynth --break-system-packages

# Richer MIDI + audio analysis
pip install pretty_midi soundfile librosa --break-system-packages

# Spectrogram CLI (requires Go)
go install github.com/steipete/songsee/cmd/songsee@latest
```

## MIDI → Audio Pipelines

### Pipeline A: numpy synthesis (current default, no extra deps)
Use `musicom-theory-kb` scripts: `scripts/synthesis_engine.py`, `scripts/pillar2_synthesis_engines.py`
- Piano (additive harmonics + decay), Guitar (Karplus-Strong), Violin (sawtooth+vibrato 5.5Hz/0.8%)
- Good for quick prototypes. Limited realism.

### Pipeline B: Native FluidSynth (✅ HIGHEST QUALITY — Use this)
Native `fluidsynth` binary and `FluidR3_GM.sf2` are now installed in the Docker environment.

```bash
# Render MIDI to WAV with high-quality SoundFont
fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 composition.mid -F output.wav -r 44100

# Step-up to OGG Opus for Telegram
ffmpeg -i output.wav -codec:a libopus -application audio -b:a 128k output.ogg -y
```

**Python Implementation:**
```python
import subprocess

def render_native(midi_path, ogg_path):
    wav_path = ogg_path.replace(".ogg", ".wav")
    sf2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
    
    # Cli render for best stability
    subprocess.run(["fluidsynth", "-ni", sf2, midi_path, "-F", wav_path, "-r", "44100"], check=True)
    subprocess.run(["ffmpeg", "-i", wav_path, "-codec:a", "libopus", "-b:a", "128k", ogg_path, "-y"], check=True)
```

### Currently Installed (Verified May 2026)
| Tool | Status | Notes |
|------|--------|-------|
| fluidsynth | ✅ Installed | Native C binary available |
| libfluidsynth-dev | ✅ Installed | Development headers present |
| FluidR3_GM.sf2 | ✅ Installed | At /usr/share/sounds/sf2/ |
| pretty_midi | ✅ Installed | Use for MIDI construction |
| pyfluidsynth | ✅ Installed | Python bindings for libfluidsynth |
| ffmpeg 7.1 | ✅ Installed | Use for OGG conversion |
|-----|--------|-----------|----------|
| **BandLab** | Manual MIDI/MP3 import | ❌ web UI | Primary collaboration DAW |
| **MuseScore** | MusicXML file exchange | ✅ CLI render | Notation export |
  92| | **Flat.io** | REST API + MusicXML | ✅ | Use `references/flat-io-api.md` |
  93| | **DAW API** | Headless score management | ✅ | See Flat.io |
| **LMMS** | CLI + project files | ✅ Linux | Could be installed |
| **Ardour** | OSC + JACK | ✅ Linux | Advanced option |

## Flat.io API

```bash
# Create score
curl -X POST https://api.flat.io/v2/scores \
  -H "Authorization: Bearer $FLAT_IO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Project Title", "privacy": "public"}'
# Upload MusicXML
curl -X POST https://api.flat.io/v2/scores/{scoreId}/revisions \
  -H "Authorization: Bearer $FLAT_IO_API_KEY" \
  -F "data=@score.musicxml"
```
Set `FLAT_IO_API_KEY` in `/opt/data/.env`.

## Recommended Full Workflow

```
Theoretician → harmonic_matrix.json + mode/meter rules
    ↓
Melodist → PitchPattern + RhythmPattern → .mid (mido/musicpy)
    ↓
Arranger → MIDI → WAV (fluidsynth or numpy) → OGG (ffmpeg)
    ↓
Dashboard → music21 piano_roll.png + volume_graph.png → index.html
    ↓
Sync → rsync /opt/data/projects/ → repos/musicom-agent/music-projects/ → git push
    ↓
Telegram → MEDIA:/opt/data/projects/NNN/audio/output.ogg
```

## BandLab Integration

BandLab is Axel's primary external DAW. Dashboard standard:
- Always include BandLab URL: `https://www.bandlab.com/axelwiertz/{project-slug}`
- Import MIDI or OGG manually into BandLab
- Link prominently in project `index.html`

## Pitfalls

- **No fluidsynth**: Fall back to numpy synthesis (musicom-theory-kb scripts)
- **No soundfonts**: Use web-sample fetch via ffmpeg as fallback
- **WAV on Telegram**: MUST convert to OGG/Opus — WAV won't render as voice bubble
- **PEP 668 pip blocks**: Add `--break-system-packages` for quick installs
- **MusicXML roundtrip**: Verify music21 export in MuseScore before sharing with Axel
