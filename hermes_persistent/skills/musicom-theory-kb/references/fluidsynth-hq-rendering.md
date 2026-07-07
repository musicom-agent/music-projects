# FluidSynth HQ Synthesis Protocol

## Best Practices
1. **Float Synthesis**: Use `fluid_synth_write_float` for full 32-bit internal resolution.
2. **Gain Calibration**: Standard gain between `0.9` and `1.2`. Normalize final WAV to `-1.0dB` peak.
3. **Reverb Scaling**: Apply `fluid_synth_set_reverb` (Room: 0.8, Level: 0.6) for Cinematic/Orchestral projects.
4. **Tail Management**: 
   - **Per-Note**: 100ms - 150ms buffer after `noteoff` to capture instrument release.
   - **Master**: 2.0s - 3.0s buffer at end of score to capture reverb wash.

## Python ctypes Implementation
```python
lib.fluid_settings_setnum(settings, b"synth.gain", 1.0)
lib.fluid_synth_set_reverb(synth, 0.8, 0.5, 1.0, 0.6)
# ... render loop ...
lib.fluid_synth_noteoff(synth, chan, pitch)
# write 150ms tail buffer
```
