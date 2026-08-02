import numpy as np

def run_preverb():
    # Generate a simple drum transient (short pulse at start, silence after)
    fs = 44100
    duration = 1.0
    n_samples = int(fs * duration)
    x = np.zeros(n_samples)
    # A simple click/pulse at 0.5s
    click_idx = int(fs * 0.5)
    x[click_idx] = 1.0
    
    # 1. Reverse input
    x_rev = x[::-1]
    
    # 2. Simple feedback comb filter as reverb/echo
    # y[n] = x_rev[n] + feedback * y[n - delay]
    delay_samples = int(fs * 0.08) # 80ms delay
    feedback = 0.8
    
    y_rev = np.zeros(n_samples)
    for n in range(n_samples):
        if n >= delay_samples:
            y_rev[n] = x_rev[n] + feedback * y_rev[n - delay_samples]
        else:
            y_rev[n] = x_rev[n]
            
    # 3. Reverse back to get preverb/riser
    y = y_rev[::-1]
    
    # Let us check when the energy rises and peaks
    # Since the click was at 0.5s, the preverb should swell BEFORE 0.5s!
    print("Checking signal energy around click (0.5s):")
    # Let us compute energy in 50ms windows from 0.2s to 0.6s
    window_size = int(fs * 0.05)
    for t in [0.2, 0.3, 0.4, 0.45, 0.5, 0.55]:
        idx = int(fs * t)
        energy = np.sum(y[idx:idx+window_size]**2)
        print(f"  Time: {t:.2f}s -> Energy: {energy:.6f}")

if __name__ == "__main__":
    run_preverb()
