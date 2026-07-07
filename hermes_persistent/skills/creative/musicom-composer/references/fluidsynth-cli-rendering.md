# FluidSynth CLI Rendering Protocol

For reliable MIDI to Audio rendering in sandbox environments.

## Command Template
```bash
fluidsynth -ni /usr/share/sounds/sf2/FluidR3_GM.sf2 \
    <INPUT_MIDI> \
    -F <OUTPUT_WAV> \
    -r 44100
```

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
