# Audio Generation with Minimal Dependencies

When `music21`, `musicpy`, `soundfile`, and other audio libraries aren't available, generate and play audio using only `numpy` + `wave` + `ffplay`.

## Full Working Script

```python
import numpy as np
import wave
import os

# --- Parameters ---
sample_rate = 44100
bpm = 120
beat_duration = 60.0 / bpm  # 0.5 s per quarter note
gap_samples = int(0.03 * sample_rate)  # 30ms gap between notes
attack_samples = int(0.005 * sample_rate)  # 5ms attack
release_samples = int(0.02 * sample_rate)  # 20ms release

# --- Synthesis function ---
def note_wave(freq, duration_samples, attack, release, volume=0.25):
    t = np.arange(duration_samples)
    env = np.ones(duration_samples)
    if attack > 0:
        env[:attack] = np.linspace(0, 1, attack)
    if release > 0:
        env[-release:] = np.linspace(1, 0, min(release, duration_samples))
    return volume * np.sin(2 * np.pi * freq * t / sample_rate) * env

# --- Build melody ---
melody = [60, 62, 64, 67, 69, 67, 64, 62, 60, 64, 67, 72, 71, 67, 64, 60]  # C major
note_dur = int(beat_duration * sample_rate) - gap_samples
total = int(beat_duration * sample_rate * len(melody))
samples = np.zeros(total, dtype=np.float32)

for i, midi in enumerate(melody):
    freq = 440.0 * (2.0 ** ((midi - 69) / 12.0))
    start = i * int(beat_duration * sample_rate)
    n = note_wave(freq, note_dur, attack_samples, release_samples, volume=0.25)
    samples[start:start+len(n)] += n

# --- Export & play ---
samples = np.clip(samples, -1.0, 1.0)
path = "/tmp/hermes/songs/melody.wav"
os.makedirs(os.path.dirname(path), exist_ok=True)
with wave.open(path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sample_rate)
    wf.writeframes(samples.astype(np.int16).tobytes())
```

## Quick Ref

| Task | Code |
|---|---|
| MIDI → freq | `440.0 * (2.0 ** ((midi - 69) / 12.0))` |
| Note duration (samples) | `int(beat_duration * sample_rate)` |
| ADSR envelope | `np.linspace(0, 1, attack)` / `np.linspace(1, 0, release)` |
| 16-bit conversion | `np.clip(s, -1, 1) * 32767`.astype(np.int16) |
| Play in sandbox | `ffplay -nodisp -autoexit <path>` |
| Write WAV | `wave.open(path, 'w')` + `setnchannels`, `setsampwidth`, `setframerate`, `writeframes` |

## Sandbox constraints

- `/root` is **not accessible** — musicom repos live there
- Write to `/tmp/hermes/songs/` (create dir first)
- Only `numpy` + stdlib guaranteed; no `soundfile`, `pydub`, `simpleaudio`, `pygame`
