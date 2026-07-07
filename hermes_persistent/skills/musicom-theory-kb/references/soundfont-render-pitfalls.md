# SoundFont Rendering Pitfalls (May 2026)

### Environment Constraints
In sandboxed environments (like this one), rendering `.sf2` files is difficult due to missing shared libraries.

- **FluidSynth Requirement**: Most Python SoundFont loaders (`sf2_loader`, `musicpy`) are wrappers for `libfluidsynth.so`. Without sudo, installing this is impossible. 
- **Static Binaries**: Static builds of FluidSynth often fail due to ALSA/Jack dependencies or architecture mismatches.
- **Pure Python Fallback**: Libraries like `sf2-parser` can read metadata but do not provide a DSP engine for pitch-shifting and rendering PCM.

### Workarounds
1. **Web Sampling**: Harvest notes from GitHub-hosted sample libraries (e.g., `tonejs.github.io/audio/salamander/`) using `ffmpeg`.
2. **Mathematical Synthesis**: Implement Karplus-Strong or Additive synthesis for lead instruments where full control (vibrato depth) is required.
3. **MIDI-Only**: Generate the MIDI structure and provide it to the user to render in their local SAW/DAW.
