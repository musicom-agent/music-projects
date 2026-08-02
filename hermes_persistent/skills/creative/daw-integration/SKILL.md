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
| **REAPER** | Lua / ReaScript CLI, OSC | ✅ Installed (Headless) | **Definitively Selected Desktop Production Target** |
| **ACE-Step** | Zustand window.__store, React, MIDI | ✅ Verified (Local Repo) | **Primary Web-Native Agent Sandboxed Workspace** |
| **openDAW** | WebAudio, Apparat JS Scriptable Synth | ✅ Verified (OpenSource) | **Pure DSP / Modular JavaScript Audio Engine** |

## Silent Padding & Track Alignment Pitfall (CRITICAL)

When using the `UnitMatrix` workflow, different tracks often have different silent/active sections (e.g., a lead instrument rests during the intro while rhythm instruments play).

### The Desync Bug
If an empty section is represented by an empty `MusicUnit` (`events=[]`) or dummy notes with `pitch=0` or `volume=0`, the MIDI encoder's duration calculations may skip these rests. As a result, the timeline offset for that track **does not advance** by the expected section ticks, leading to severe track length mismatches and desynchronization (desync) upon import into desktop DAWs.

### The Structural Fix in Core Library (Upgraded July 2026)
This timing fix has been permanently implemented at the class level within the core Musicom workflow (`UnitMatrixComposer.to_midi()` under `/opt/data/repos/musicom/workflows/unitmatrix_composer.py`).

1. **Absolute Milestone Mapping:** Instead of relying on sequential incremental delta-times which accumulate rounding errors, the exporter harvests all absolute `start_tick` and `end_tick` parameters across all sections for a given voice row.
2. **Chronological Sorting:** It flattens the absolute event boundaries into an explicit chronological `timeline` array containing `on` and `off` milestones. Crucially, it sorts `off` events to execute strictly *before* `on` events occurring on the same tick to prevent overlapping node conflicts.
3. **Automatic Silent Tail Padding:** Upon completing the event queue, it calculates the remaining ticks required to reach the expected project length (`total_ticks_expected - current_tick`). If any gap exists, it automatically appends a silent padding milestone:
   ```python
   # Append silent tail padding to guarantee exact down-to-the-tick track synchronization
   track.append(mido.Message('note_on', note=0, velocity=0, channel=voice['channel'], time=remaining_ticks))
   track.append(mido.Message('note_off', note=0, velocity=0, channel=voice['channel'], time=0))
   ```
4. **Usage:** Always use the class-level `composer.to_midi(output_path)` method rather than scripting ad-hoc manual MIDI track writers inside project execution playbooks. This keeps all timing logic perfectly unified and robust.

## Headless REAPER (Definitive Desktop Target)

REAPER is selected as the primary professional desktop production DAW. It is installed on the local system under `/opt/data/tools/reaper/REAPER/`.

### Headless Execution Mechanism
We built a custom headless GDK-free interface driver (`libSwell.so`) with `NOGDK=1` compiled from Cockos WDL.
- This allows full CLI command execution and headless Lua/ReaScript execution.
- Config directory: `~/.config/REAPER/`
- Audio fallback mode: `dummy` (Crucial to prevent rendering/batch engines blocking on active hardware drivers).

### reaper.ini Headless Configuration
To run headless commands without a physical audio device, verify `~/.config/REAPER/reaper.ini` matches:
```ini
[reaper]
libsndcards=0
linux_audio_mode=3
linux_hw_driver=dummy
linux_hw_device=
linux_hw_out_device=
linux_hw_srate=44100
linux_hw_blocksize=512
linux_hw_periods=3
```

### Automation Workflows
1. **RPP Construction:** Rather than spawning slow GUI subprocesses, programmatic agents can write plain-text `.RPP` files containing raw `<TRACK>` and `<ITEM>` definitions directly in Python.
2. **ReaScript Execution:** REAPER supports running Python / Lua scripts via CLI:
   ```bash
   /opt/data/tools/reaper/REAPER/reaper /path/to/project.rpp /path/to/script.lua
   ```
3. **Headless Limit Pitfall:** Render operations (`-renderproject` or `-peaktest`) may hang in containerized environments if the audio system (dummy driver) has configuration mismatching state. For safe delivery, write plain-text `.RPP` and export raw `.mid` files directly so the user can double-click and render locally with desktop hardware drivers.

## Web-Native Agent Workspace: ACE-Step & openDAW

When operating in our containerized/agentic sandboxes, local UI-less operation makes traditional desktop DAWs sluggish. **ACE-Step** and **openDAW** act as the perfect web-native canvases.

### ACE-Step Zustand Store Integration
ACE-Step exposes its complete audio timeline, tempo, track allocation, and MIDI grids via Zustand on the client window (`window.__store`). 
- **Track Appending:** Add tracks using `addTrack(displayName, type)` where type is `'pianoRoll' | 'sample'`.
- **Note Placement:** Use `ensureMidiClip(trackId)` to instantiate a MIDI container, then inject notes atomically via `addMidiNote(clipId, { pitch, startBeat, durationBeats, velocity })`.
- **Zero-Drift Execution:** Standardize on **Option A** (delivering absolute-aligned MIDI files under `/StagedMidi/`) to import instantly into local Logic Pro setups. We fall back to **Option B** (feeding `window.__store` JSON structures via Developer Console/Web Sockets) once browser/HTTP connection endpoints are fully wired.

### openDAW & Apparat Scripting
openDAW features the **Apparat** plugin—a fully programmable synthesizer and sampler scripted entirely in raw **JavaScript**.
- Musicom can programmatically generate standard JS DSP logic files (e.g. implementing procedural FM operators, Karplus-Strong string synthesis, or custom envelopes) and inject them straight into the browser audio graph.

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
