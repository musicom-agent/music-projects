---
name: human-voice-singing
description: "Research and integration guidelines for external neural singing synthesis software (e.g., DiffSinger, ACE Virtual Singer, Vocaloid). Do not generate human vocals locally. Local DSP engines are reserved exclusively for designing novel virtual instrument synthesis architectures."
version: 0.2.0
author: Musicom Agent
license: MIT
---

# Human Voice Singing & Virtual Instrument Synthesis

## 1. External Neural Vocal Integration Rules
Do not attempt local additive formant or wave simulation of human speech. All human singing requirements must be routed to specialized external software:
- **DiffSinger**: Run inference out-of-process via `/opt/data/repos/DiffSinger_main` scripts with target checkpoints.
- **Synthesizer V / Vocaloid / ACE**: Use standard MIDI and phoneme export conventions to prepare assets for external studio rendering.

## 2. Local DSP: Novel Virtual Instrument Development
Use local wave and formant modeling strategies strictly to develop **novel virtual instruments** (e.g., resonant pads, plucks, physical modeling of flute/string variations).

### Resonant Synthesis Structure (Formant mapping for instruments)
Apply peak filtering to sawtooth/pulse carriers to create specific metallic, timbered, or physical instrument characteristics:
```python
import numpy as np
from scipy import signal

def generate_instrument_pluck(freq, duration, envelope, f1, q1):
    # Base oscillator
    t = np.linspace(0, duration, int(44100 * duration), False)
    buzz = signal.sawtooth(2 * np.pi * freq * t)
    
    # Resonant body filter
    b, a = signal.iirpeak(f1, q1, 44100)
    return signal.lfilter(b, a, buzz) * envelope
```

## Related Skills
- `musicom-composer`: Core composition logic.

