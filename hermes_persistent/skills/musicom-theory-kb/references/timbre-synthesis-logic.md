# Instrument Timbre Synthesis Algorithms

Research and implementation notes from Pillar 2: Sound Synthesis.

## 1. Guitar (Karplus-Strong Physics)
The Karplus-Strong algorithm simulates a plucked string by cycling noise through a filtered delay line.
- **Excitation**: White noise buffer of length $L = f_s / f_{pitch}$.
- **Feedback**: $y[n] = 0.5 \cdot (y[n-L] + y[n-L-1]) \cdot \text{decay}$.
- **Decay Factor**: $0.996$ is a good baseline for acoustic guitar; lower values simulate palm muting.

## 2. Violin (Bowed String Modeling)
Bowed strings are characterized by "stick-slip" motion and high harmonic density.
- **Waveform**: Sawtooth-like (sum of many harmonics).
- **Harmonic Roll-off**: $1/n$ or $1/n^{1.1}$ for a warmer tone.
- **Bowing Envelope**: Slow attack ($150\text{--}250\text{ms}$) to simulate the bow overcoming static friction.
- **Vibrato**: Frequency Modulation (FM). 
    - *Natural settings*: $5.5\text{Hz}$ rate, $0.5\text{--}1.0\%$ depth.

## 4. Synthesis Pitfalls (Acoustic Realism)
- **The "Singing Saw" Effect**: Avoid perfect sawtooth/square waves or constant-rate FM vibrato for violins; they sound synthetic. Use formant filtering (~280Hz/3kHz), harmonic phase smearing, and "bow hair" noise (15% white noise).
- **Static Onset**: Acoustic instruments rarely start at full timbre; use blooming attacks (parabolic/sine-squared, 400-600ms) for bowed strings.
- **Perfect Harmony**: Ideal integer harmonics sound like an organ. Use inharmonicity models (Piano B-constant) and detuning to create an acoustic "wood and wire" feel.
- **Hammer transients**: Pianos need a 10-15ms low-passed noise burst to simulate the hammer strike.
