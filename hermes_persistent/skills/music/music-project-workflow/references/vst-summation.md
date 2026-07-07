# VST Polyphony Summing (Headless)

When `pedalboard` or DPF-plugins (Nekobi, Kars) fail to process simultaneous MIDI notes in a single block:

1. **Split MIDI**: Separate the MIDI file into individual mono-voice tracks (S, A, T, B).
2. **Sequential Render**: 
   ```python
   for track in tracks:
       audio = plugin(track_midi)
       buffers.append(audio)
   ```
3. **NumPy Sum**:
   ```python
   final = np.sum(buffers, axis=0) / len(buffers)
   ```
4. **FluidSynth String Patch**:
   - `Patch 48`: String Ensemble.
   - CLI: `fluidsynth -ni font.sf2 mid.mid -F out.wav -o synth.midi-bank-select=gm`
