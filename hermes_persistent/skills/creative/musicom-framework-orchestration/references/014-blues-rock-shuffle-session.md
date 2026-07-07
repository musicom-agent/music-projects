# Session Note — Project 014 Blues Rock Shuffle

## Context

Project: `/opt/data/projects/014-rock-apprenticeship`
Task: continue rock apprenticeship with blues rock.

## Working pipeline

Environment reality during session:
- `mido`: available
- `numpy`: available
- `ffmpeg`: available
- `fluidsynth`: available at `/usr/bin/fluidsynth`
- SoundFont: `/usr/share/sounds/sf2/FluidR3_GM.sf2`
- `music21`: not available in system `python3`
- `pretty_midi`: not available in system `python3`
- `soundfile`: not available in system `python3`
- `rsync`: not available

Use `mido` for deterministic multitrack MIDI generation when `music21` is missing. Render via FluidSynth CLI:

```bash
fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 input.mid -F raw.wav -r 44100
ffmpeg -y -i raw.wav -af 'volume=0.95,alimiter=limit=0.95' mastered.wav
ffmpeg -y -i mastered.wav -codec:a libopus -application voip -b:a 64k out.ogg
```

Delete raw intermediate WAV before committing/publishing.

## Blues rock pattern used

Study 02 specs:
- Key: E blues
- Tempo: 112 BPM
- Form: 24 bars = 12-bar blues x2
- Harmony: `E E E E | A A E E | B A E B`
- Feel: shuffle as triplet math: long-short = 2/3 + 1/3 beat
- Riff: root + moving upper note: 5 → 6 → b7 → 6
- Tracks: overdriven guitar, electric bass boogie lock, blues lead guitar, GM drums

Rhythm DNA visualization should use high-contrast `█` and `░` markers.

## Repo publishing quirk

`/opt/data/repos/musicom-agent` existed, but Git top-level was `/opt/data`, not the repo subdirectory. Use scoped git operations to avoid accidental massive adds:

```bash
cd /opt/data
git add repos/musicom-agent/music-projects/<project> repos/musicom-agent/music-projects/index.html
GIT_AUTHOR_NAME='Musicom Agent' GIT_AUTHOR_EMAIL='musicom@wiertz.tech' \
GIT_COMMITTER_NAME='Musicom Agent' GIT_COMMITTER_EMAIL='musicom@wiertz.tech' \
  git commit -m '<NNN>: <message>'
git push origin main
```

If `rsync` is missing, copy with Python `shutil.copytree()` and `shutil.copy2()`.
