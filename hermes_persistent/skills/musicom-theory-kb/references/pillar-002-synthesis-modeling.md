# Synthesis Modeling (Pillar 002)

Notes from the implementation of Piano and Guitar synthesis without external libraries.

## Karplus-Strong Guitar Modeling
To simulate a plucked string:
1. Initialize a ring buffer of size `L = sample_rate / frequency` with white noise.
2. Output the first sample of the buffer.
3. Calculate a new sample: `new = 0.5 * (buffer[0] + buffer[1]) * decay_factor`.
4. A `decay_factor` of `0.996` is effective for a standard acoustic guitar sound.
5. Append `new` to the buffer and remove the first element.

## Additive Piano Modeling
1. Use a fundamental sine wave at `freq`.
2. Add harmonics at `2*freq` (50% amplitude) and `3*freq` (10-20% amplitude).
3. Apply a sharp percussive envelope: `amplitude * np.exp(-4 * t)`.
4. For better realism, add a slight noise burst at the attack to simulate the hammer strike.

## Session Pitfalls
- **Absolute Paths**: Telegram media delivery via `MEDIA:` requires absolute file paths. Relative paths will cause the platform to skip the attachment.
- **Git Commit Quoting**: When using `terminal` via Python/code tools, ensure commit messages with spaces are handled without shell backgrounding interference (avoid `&` in the same string as the commit command).
