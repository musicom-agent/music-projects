# Sound Synthesis Implementation Recipes

## Karplus-Strong Guitar (Numpy)
```python
def guitar_ks(freq, duration, sample_rate=44100):
    N = int(sample_rate / freq)
    ring_buf = np.random.uniform(-1, 1, N)
    num_samples = int(duration * sample_rate)
    samples = np.zeros(num_samples)
    for i in range(num_samples):
        samples[i] = ring_buf[0]
        # Low-pass filter (averaging) + slight energy loss
        avg = 0.5 * (ring_buf[0] + ring_buf[1]) * 0.996
        ring_buf = np.append(ring_buf[1:], avg)
    return samples
```

## Subtle Violin Vibrato (FM)
```python
# Refined for natural timbre
vibrato_rate = 5.5
vibrato_depth = freq * 0.008 # 0.8%
vibrato = vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t)
# Summation with warmer roll-off
amp = 1.0 / (h ** 1.1)
```

## Git Profile Scrub
```bash
git config --global user.name "Musicom Agent"
git config --global user.email "musicom@wiertz.tech"
# To fix misattributed history
git commit --amend --no-edit --author="Musicom Agent <musicom@wiertz.tech>"
```
