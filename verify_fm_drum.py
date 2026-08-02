import numpy as np
import math

def generate_fm_drum():
    fs = 44100
    duration = 0.3 # 300ms tom/drum
    n_samples = int(fs * duration)
    t = np.arange(n_samples) / fs
    
    # Pitch sweep parameters
    f_start = 250.0
    f_end = 60.0
    tau_pitch = 0.05 # 50ms pitch decay
    
    # Instantaneous frequency: f(t) = f_end + (f_start - f_end) * exp(-t / tau_pitch)
    # Phase is 2 * pi * integral of f(t)
    # integral is: f_end * t - (f_start - f_end) * tau_pitch * (exp(-t / tau_pitch) - 1)
    phase_carrier = 2.0 * math.pi * (f_end * t - (f_start - f_end) * tau_pitch * (np.exp(-t / tau_pitch) - 1.0))
    
    # Modulator parameters (Harmonic FM, e.g. ratio 1.5:1 for metallic clang)
    f_mod = 90.0
    phase_mod = 2.0 * math.pi * f_mod * t
    
    # Modulation index decay
    mod_index = 4.0
    tau_mod = 0.04
    index_env = mod_index * np.exp(-t / tau_mod)
    
    # Amplitude envelope
    tau_amp = 0.08
    amp_env = np.exp(-t / tau_amp)
    
    # Synthesized wave
    y = amp_env * np.sin(phase_carrier + index_env * np.sin(phase_mod))
    
    # Verify decay
    start_amp = np.max(np.abs(y[:int(fs*0.02)]))
    mid_amp = np.max(np.abs(y[int(fs*0.1):int(fs*0.12)]))
    end_amp = np.max(np.abs(y[int(fs*0.25):]))
    
    print(f"FM Drum Synthesis Verification:")
    print(f"  Start Amplitude (first 20ms): {start_amp:.4f}")
    print(f"  Mid Amplitude (100-120ms): {mid_amp:.4f}")
    print(f"  End Amplitude (after 250ms): {end_amp:.4f}")

if __name__ == "__main__":
    generate_fm_drum()
