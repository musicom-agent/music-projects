# VoiceAudio Transcription & Humanization Recipe

The specific workflow developed in Project 005 for converting human-played audio into structured Balfolk ensembles.

### 1. Neural Extraction (The Frame)
Use `basic-pitch` inside the `musicom` Micromamba env (py3.11) to avoid build errors.
```bash
/opt/data/bin/micromamba run -r /opt/data/micromamba -n musicom basic-pitch ./output/ ./input.wav
```

### 2. Modal Transformation
Apply the "Dorian Mutation" using `mutate_mode.py`. Toggles E->Eb and B->Bb to shift from Ionian to Dorian while keeping the Major 6th (A).

### 3. Structural Alignment
1. **Grid Snap**: Snap to 16th note grid using `align_rhythm.py` (quantization factor 4).
2. **6/8 Retiming**: Force TimeSignature and apply "Jig Gravity" (Stronger velocity on beats 1 and 4).

### 4. Orchestrative Splitting
Use `orchestrate.py` to split the vertical DNA:
- **Lead**: Highest pitch at any offset -> Violin.
- **Bass**: Lowest pitch -> Contrabass (transposed to register < 48).
- **Harmony**: Interior pitches -> Piano.

### 5. Balfolk Pulse Calibration
Final tempo set at **115 BPM (Dotted Quarter)** for energetic jig movement.
