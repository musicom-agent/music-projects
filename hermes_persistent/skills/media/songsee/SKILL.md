---
name: songsee
description: "Audio spectrograms/features (mel, chroma, MFCC) via CLI."
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Audio, Visualization, Spectrogram, Music, Analysis]
    homepage: https://github.com/steipete/songsee
prerequisites:
  commands: [songsee]
---

# songsee

Generate spectrograms and multi-panel audio feature visualizations from audio files.

## Prerequisites

Requires [Go](https://go.dev/doc/install):
```bash
go install github.com/steipete/songsee/cmd/songsee@latest
```

Optional: `ffmpeg` for formats beyond WAV/MP3.

## Quick Start

```bash
# Basic spectrogram
songsee track.mp3

# Save to specific file
songsee track.mp3 -o spectrogram.png

# Multi-panel visualization grid
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux

# Time slice (start at 12.5s, 8s duration)
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg

# From stdin
cat track.mp3 | songsee - --format png -o out.png
```

## Visualization Types

Use `--viz` with comma-separated values:

| Type | Description |
|------|-------------|
| `spectrogram` | Standard frequency spectrogram |
| `mel` | Mel-scaled spectrogram |
| `chroma` | Pitch class distribution |
| `hpss` | Harmonic/percussive separation |
| `selfsim` | Self-similarity matrix |
| `loudness` | Loudness over time |
| `tempogram` | Tempo estimation |
| `mfcc` | Mel-frequency cepstral coefficients |
| `flux` | Spectral flux (onset detection) |

Multiple `--viz` types render as a grid in a single image.

## Common Flags

| Flag | Description |
|------|-------------|
| `--viz` | Visualization types (comma-separated) |
| `--style` | Color palette: `classic`, `magma`, `inferno`, `viridis`, `gray` |
| `--width` / `--height` | Output image dimensions |
| `--window` / `--hop` | FFT window and hop size |
| `--min-freq` / `--max-freq` | Frequency range filter |
| `--start` / `--duration` | Time slice of the audio |
| `--format` | Output format: `jpg` or `png` |
| `-o` | Output file path |

## Notes

- WAV and MP3 are decoded natively; other formats require `ffmpeg`
- Output images can be inspected with `vision_analyze` for automated audio analysis
- Useful for comparing audio outputs, debugging synthesis, or documenting audio processing pipelines

## Fallback: librosa Analysis When `songsee` Is Unavailable or Too Coarse

For short incoming voice/sound clips that must become musical material, use Python feature extraction directly:

```bash
ffmpeg -y -i "$IN" -ac 1 -ar 22050 /tmp/source_voice.wav -loglevel error
/opt/data/micromamba/envs/musicom/bin/python - <<'PY'
import librosa, numpy as np
src = '/tmp/source_voice.wav'
y, sr = librosa.load(src, sr=22050, mono=True)
y, _ = librosa.effects.trim(y, top_db=28)
on_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=256)
peaks = librosa.util.peak_pick(on_env, pre_max=3, post_max=3, pre_avg=8, post_avg=8, delta=0.18, wait=3)
onsets = librosa.times_like(on_env, sr=sr, hop_length=256)[peaks]
f0, voiced, prob = librosa.pyin(y, fmin=librosa.note_to_hz('E2'), fmax=librosa.note_to_hz('E5'), sr=sr, frame_length=2048, hop_length=256)
centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=256)[0]
flatness = librosa.feature.spectral_flatness(y=y, hop_length=256)[0]
print({'duration': len(y)/sr, 'onsets': onsets.tolist(), 'median_f0': float(np.nanmedian(f0)), 'centroid': float(np.median(centroid)), 'flatness': float(np.median(flatness))})
PY
```

Use extracted onsets as rhythm DNA and pitch trace as contour DNA. Quantize into the active project scale before composing. Telegram cache audio may live under `/opt/data/cache/audio/audio_*.mp3`; inspect with `ffprobe` because extension and codec can disagree.
