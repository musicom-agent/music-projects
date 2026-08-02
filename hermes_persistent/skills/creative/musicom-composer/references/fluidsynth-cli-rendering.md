# FluidSynth CLI Rendering Protocol

For reliable MIDI to Audio rendering in sandbox environments.

## Command Template
```bash
/opt/data/micromamba/envs/musicom/bin/fluidsynth -ni -F <OUTPUT_WAV> -r 44100 <SOUNDFONT> <INPUT_MIDI>
```
*Note: Sourced native micromamba FluidSynth location `/opt/data/micromamba/envs/musicom/bin/fluidsynth` is highly reliable for container rendering. SoundFont usually lives at `/opt/data/pretty_midi/TimGM6mb.sf2` or `/opt/data/.local/lib/python3.13/site-packages/pretty_midi/TimGM6mb.sf2`.*

## Conversion to OGG (Telegram)
```bash
ffmpeg -i <OUTPUT_WAV> \
    -codec:a libopus \
    -application voip \
    -b:a 48k \
    <OUTPUT_OGG> \
    -y -loglevel error
```

## Troubleshooting
- **Error: Filter not found (peaknorm)**: Use `loudnorm` or remove volume filters.
- **Error: ctypes.ArgumentError**: Switch from Python `ctypes` bridge to this CLI method.
- **Error: Traceback numpy missing**: Run scripts using the micromamba environment python: `/opt/data/micromamba/envs/musicom/bin/python`.
- **Error: Timing validation failed (Track length mismatch)**: In `UnitMatrixComposer`, make sure events inside `MusicUnit` are exactly aligned to boundaries. Ensure durations and `end_tick` calculations do not overshoot or undershoot section sizes (like `BAR_TICKS = 1920` for 1 bar at 480 TPB). Be precise with off-by-one subtractions on consecutive notes.

