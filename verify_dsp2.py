import numpy as np
import math

def run_resonator_bank():
    fs = 44100
    duration = 2.0
    n_samples = int(fs * duration)
    
    # Excitation: Dirac delta (single impulse at sample 0)
    x = np.zeros(n_samples)
    x[0] = 1.0
    
    # Chord frequencies (C4, E4, G4)
    freqs = [261.63, 329.63, 392.00]
    r = 0.999 # Very narrow band, long decay
    
    y_total = np.zeros(n_samples)
    
    for f in freqs:
        theta = 2.0 * math.pi * f / fs
        g = 1.0 - r
        coeff_y1 = 2.0 * r * math.cos(theta)
        coeff_y2 = - (r ** 2)
        
        y = np.zeros(n_samples)
        y_1 = 0.0
        y_2 = 0.0
        
        for n in range(n_samples):
            y[n] = g * x[n] + coeff_y1 * y_1 + coeff_y2 * y_2
            y_2 = y_1
            y_1 = y[n]
            
        y_total += y
        
    # Analyze spectrum
    fft_vals = np.abs(np.fft.rfft(y_total))
    fft_freqs = np.fft.rfftfreq(n_samples, 1.0/fs)
    
    # Check magnitude near target frequencies
    print("Checking magnitude at target frequencies:")
    for f in freqs:
        idx = np.argmin(np.abs(fft_freqs - f))
        print(f"  Target: {f:.2f} Hz -> Nearest FFT Bin: {fft_freqs[idx]:.2f} Hz, Amplitude: {fft_vals[idx]:.4f}")
        
    # Find actual top global peaks
    peak_indices = np.argsort(fft_vals)[::-1]
    print("\nTop 5 absolute peak bins in the spectrum:")
    count = 0
    seen_freqs = []
    for idx in peak_indices:
        freq = fft_freqs[idx]
        # Avoid printing adjacent bins
        if any(abs(freq - sf) < 5 for sf in seen_freqs):
            continue
        print(f"  Freq: {freq:.2f} Hz, Amplitude: {fft_vals[idx]:.4f}")
        seen_freqs.append(freq)
        count += 1
        if count >= 5:
            break

if __name__ == "__main__":
    run_resonator_bank()
