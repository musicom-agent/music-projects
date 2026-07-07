# Project 018: Landal-Roompot-Polo Hybrid Transcription

## DNA Extraction Logic
- **Melody A (Berendans):** Traditional Dutch Folk, Bb Major, intervals [0, 2, 4, 0] (Bb-C-D-Bb). Sine wave instrument at 100-120 BPM.
- **Melody B (Koos Roompot):** Minidisco/Euro-Schlager, Bb Major (transposed for merge), intervals [7, 7, 7, 12] (F-F-F-Bb) in octave 5. High-intensity sawtooth.
- **Melody C (Polo Beer):** Voice-message derived motif. Bb Major, intervals [0, 4, 7, 5, 2] (Bb-D-F-Eb-C).

## Weaving Strategy (V7 Protocol)
1. **Foundation:** 4/4 Minidisco Kick + Clap on 2 & 4. Root-Fifth Bass (Bb-F).
2. **Separated Exposure:** Introduce themes one by one (4-bar blocks) to ensure recognizable identity before convergence.
3. **Instrumentation:**
   - Folk: Violin + Piano (FluidR3_GM).
   - Minidisco: Sawtooth/Square Synth.
   - User-Voice: Steel Guitar (Karplus-Strong focus).

## FluidSynth CLI Command
```bash
fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 midi_file.mid -F output_wav.wav -r 44100
```
