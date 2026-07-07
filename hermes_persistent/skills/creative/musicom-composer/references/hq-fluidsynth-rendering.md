# Musicom: High-Quality Synthesis Pipeline Best Practices

When writing python scripts in the sandbox using `fluidsynth`, follow this HQ rendering pipeline to ensure broadcast-quality (normalized, deep, rich) audio output suitable for the final Discord/Telegram OGG delivery.

## 1. Engine & Data Types
- ALWAYS load the shared library dynamically via `ctypes.CDLL('libfluidsynth.so.3')`.
- Do NOT use the 16-bit integer rendering (`fluid_synth_write_s16`); the symbol structure frequently causes `AttributeError`. 
- **Use `fluid_synth_write_float`** to render stereophonic 32-bit floats natively.

## 2. Gain and Mastering
- Built-in FluidSynth gain is often too quiet (resulting in -40dB files). 
- Use `lib.fluid_settings_setnum(settings, b"synth.gain", 1.0)` early.
- Perform a Peak Normalization as the very last step in Numpy. Scale the highest absolute peak in the master float array to **0.89** (approx -1.0dB headroom) before casting to `int16`. 
- Never let audio clip (clip values outside `-1.0, 1.0` before int cast).

## 3. Acoustic Release Tails (The NoteOff Gap)
- Standard MIDI-to-Wav logic loops over `(noteOn, extract_samples(duration), noteOff)`.
- If you stop extracting the exact moment `noteOff` fires, you chop the acoustic resonance/decay off the sample (violins stop instantly, pianos don't sustain).
- **Mandatory Logic**: After calling `fluid_synth_noteoff`, ALWAYS write a 100ms - 200ms "tail block" (`fluid_synth_write_float` again) to capture the natural decay of the SoundFont instrument *before* advancing the time clock for the next note.

## 4. Master Wash (Reverb)
- Enable Freeverb via `lib.fluid_synth_set_reverb(synth, 0.9, 0.5, 1.0, 0.8)` (especially for Cinematic / Jazz tracks).
- Extend the master audio buffer by ~3.0 seconds beyond the final note.
- After all notes have been sequenced, write a final 2.0 to 3.0 second empty block into the synthesizer and capture the output to capture the resolving reverb tail of the room.

## 5. File Delivery
- Export the raw HQ `.wav` file locally.
- Run it through `ffmpeg` using `-codec:a libopus -application voip -b:a 48k` to create the OGG.
- Use `ffplay -af "volumedetect"` via CLI to verify the `mean_volume` is somewhere between `-12dB` and `-18dB`.