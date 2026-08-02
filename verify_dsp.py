import numpy as np
import math

def run_resonator_bank():
    fs = 44100
    duration = 0.5
    n_samples = int(fs * duration)
    
    # Excitation: short burst of white noise (10ms) to excite resonators
    excitation_len = int(fs * 0.01)
    x = np.zeros(n_samples)
    x[:excitation_len] = np.random.uniform(-1.0, 1.0, excitation_len)
    
    # Chord frequencies (C4, E4, G4)
    freqs = [261.63, 329.63, 392.00]
    r = 0.995 # Decay control (pole radius)
    
    y_total = np.zeros(n_samples)
    
    for f in freqs:
        theta = 2.0 * math.pi * f / fs
        # Difference equation coefficients
        # y[n] = g*x[n] + 2*r*cos(theta)*y[n-1] - r^2*y[n-2]
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
        
    # Analyze spectrum using FFT to verify peaks
    fft_vals = np.abs(np.fft.rfft(y_total))
    fft_freqs = np.fft.rfftfreq(n_samples, 1.0/fs)
    
    # Find top 3 peak frequencies
    peaks = []
    # Simple threshold and peak finding
    for idx in range(1, len(fft_vals)-1):
        if fft_vals[idx] > fft_vals[idx-1] and fft_vals[idx] > fft_vals[idx+1] and fft_vals[idx] > 0.1:
            peaks.append((fft_vals[idx], fft_freqs[idx]))
            
    peaks.sort(key=lambda x: x[0], reverse=True)
    
    print("Resonator bank target freqs:", freqs)
    print("Detected peak frequencies in DSP output:")
    for val, freq in peaks[:5]:
        print(f"  Freq: {freq:.2f} Hz, Amplitude: {val:.2f}")

if __name__ == "__main__":
    run_resonator_bank()
