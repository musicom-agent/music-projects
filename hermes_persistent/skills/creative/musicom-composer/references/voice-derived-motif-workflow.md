# Voice-Derived Motif Workflow

Session source: Project 014 blues-rock continuation with an incoming Telegram voice/sound.

## Trigger

Use when user sends a short voice/audio clip and asks to analyze it, extract musical DNA, or compose a motif from it.

## Proven workflow

1. Locate the most recent incoming audio.
   - Telegram voice/audio may appear under `/opt/data/cache/audio/` as `audio_*.mp3` even when `ffprobe` reports PCM codec.
   - Also check `/opt/data/in/`, `/tmp/`, and common extensions: `.ogg`, `.oga`, `.mp3`, `.wav`, `.m4a`, `.opus`, `.webm`.

2. Convert to mono WAV for analysis:

```bash
ffmpeg -y -i "$IN" -ac 1 -ar 22050 "$OUT/source_voice.wav" -loglevel error
```

3. Prefer the `musicom` micromamba env for audio analysis when system Python lacks packages:

```bash
/opt/data/micromamba/envs/musicom/bin/python - <<'PY'
import librosa, scipy, numpy, matplotlib, soundfile, mido
print('audio analysis env OK')
PY
```

4. Extract features with librosa:
   - waveform duration
   - RMS / onsets via `librosa.onset.onset_strength` + `librosa.util.peak_pick`
   - pitch via `librosa.pyin`; fallback to `librosa.piptrack`
   - timbre via spectral centroid, flatness, zero crossing rate

5. Convert pitch to motif DNA:
   - Raw detected MIDI notes become contour evidence, not literal composition law.
   - Quantize to the project key/genre scale.
   - For Project 014 blues-rock, map to E blues: `E G A Bb B D`.
   - Stable repeated pitch can become a functional anchor. Example: stable D5 (~590 Hz) in E blues = b7 hook anchor.

6. Compose short motif:
   - Preserve attack count/rhythm in compressed musical time.
   - Preserve contour if varied; if source is monotone/stable, create call-response using the stable note as anchor then resolve.
   - Example from session:

```text
Input DNA: D5 D5 D5 D5
Motif:     D5 D5 D5 D5 | B4 Bb4 A4 G4 E4
Function:  b7 anchor   | 5  b5  4  b3 1
```

7. Export paired outputs:
   - MIDI via `mido`
   - WAV/OGG via FluidSynth CLI + `FluidR3_GM.sf2`
   - Analysis PNG + JSON/Markdown notes

8. Publish:
   - Add motif to project dashboard.
   - Mirror into `repos/musicom-agent/music-projects/`.
   - Remove intermediate `*-raw.wav` before commit.

## Pitfalls

- System Python may lack `librosa`, `scipy`, `matplotlib`, and `soundfile`; use `/opt/data/micromamba/envs/musicom/bin/python`.
- Do not trust the extension alone; inspect with `ffprobe`.
- Do not overfit noisy pitch tracks. A musically useful motif may require functional mapping into the project key.
- Intermediate raw FluidSynth renders are large and should not be committed.
