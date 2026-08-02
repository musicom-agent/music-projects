import os

filepath = "/opt/data/projects/Research/CompositionMethods/methods_db.md"

with open(filepath, "r") as f:
    content = f.read()

# 1. Insert SP-022 into the Sound Production Methods table
sp021_row = "| **SP-021** | Binaural Woodworth-Schlosberg Spatialization | **Post-Processing / DSP** | 3D Binaural Stereo Render | Applies Head-Related Transfer Function (HRTF) emulation via Woodworth-Schlosberg ITD and frequency-dependent ILD head-shadowing filters for realistic 3D acoustic placement. |"
sp022_row = "| **SP-022** | Wave Terrain Synthesis (WTS) | **Synthesis Engines** | Dynamic / Evolving Rich Timbres | Generates complex, organic waveforms by scanning a 2D mathematical surface (the terrain) with a 2D trajectory orbit. |"

if sp021_row in content:
    # We find where sp021_row ends and insert sp022_row on a new line
    idx = content.find(sp021_row)
    insert_pos = idx + len(sp021_row)
    # Check if there is already a newline after sp021_row
    new_content = content[:insert_pos] + "
" + sp022_row + content[insert_pos:]
    print("Inserted SP-022 into table successfully!")
else:
    print("Error: SP-021 row not found in file!")
    # Fallback search
    lines = content.splitlines()
    found = False
    for i, line in enumerate(lines):
        if "SP-021" in line:
            lines.insert(i + 1, sp022_row)
            new_content = "\n".join(lines) + "\n"
            found = True
            print("Found via fallback search and inserted.")
            break
    if not found:
        raise Exception("Could not find SP-021 anywhere!")

# 2. Append SP-022 description to the end of the file
sp022_section = """

---

# Wave Terrain Synthesis (WTS) (Method SP-022)

### **Description**
Wave Terrain Synthesis (WTS) is an advanced audio synthesis method that generates dynamic, evolving, and highly complex timbres by using a 2D trajectory (an orbit) to scan a 2D mathematical surface (the terrain). 
The terrain is defined as a function $z = f(x, y)$ over a bounded domain (e.g., $[-1.0, 1.0] \\times [-1.0, 1.0]$). As a particle or orbit moves along a path $(x(t), y(t))$ on this terrain, the height of the terrain at the current position is read out as the audio amplitude $s(t) = f(x(t), y(t))$.
If the orbit is periodic, the resulting waveform will also be periodic. By dynamically changing the size, shape, position, or frequency of the orbit (using LFOs, envelopes, or MIDI controllers), or by dynamically altering the terrain itself, WTS generates highly expressive sweeps, vocal formants, and rich harmonic spectra that are difficult to achieve with standard oscillators.

### **Technical Mechanics**
1. **The Terrain Function $f(x, y)$**:
   A terrain can be defined using algebraic, trigonometric, or polynomial functions. To avoid harsh clipping, the function is typically designed or normalized to lie within the range $[-1.0, 1.0]$.
   Examples of classic terrain functions:
   - Sine-product terrain (vocal-like or multi-modal):
     $$f(x, y) = \\sin(\\pi \\cdot x) \\cdot \\cos(\\pi \\cdot y)$$
   - Polynomial/Waveshaping terrain (rich odd/even harmonics):
     $$f(x, y) = x^3 - 3xy^2$$ (Monkey Saddle)
   - Concentric ripples (bell-like, FM-like sidebands):
     $$f(x, y) = \\cos(\\pi \\sqrt{x^2 + y^2})$$

2. **The Scanning Orbit $(x(t), y(t))$**:
   The orbit determines the fundamental frequency $f_0$ of the generated sound.
   - Circular orbit (generates simple or low-order harmonic spectra):
     $$x(t) = r(t) \\cdot \\cos(2\\pi f_0 t + \\phi_x)$$
     $$y(t) = r(t) \\cdot \\sin(2\\pi f_0 t + \\phi_y)$$
     where $r(t) \\in [0.0, 1.0]$ is the radius parameter.
   - Lissajous orbit (generates complex harmonic structures and frequency modulation effects):
     $$x(t) = r_x(t) \\cdot \\sin(2\\pi f_x t + \\theta_x)$$
     $$y(t) = r_y(t) \\cdot \\sin(2\\pi f_y t + \\theta_y)$$
     where $f_x$ and $f_y$ are in a specific ratio (e.g., $2:3$, $3:4$), and $f_0 = \\gcd(f_x, f_y)$ represents the fundamental frequency.

3. **Dynamic Modulation**:
   As $r(t)$ or orbit center offsets $(x_0(t), y_0(t))$ are modulated dynamically:
   $$x_m(t) = x_0(t) + x(t)$$
   $$y_m(t) = y_0(t) + y(t)$$
   the orbit traverses different regions of the 2D surface, generating continuous and expressive timbral morphing.

### **Implementation Requirements (Python/NumPy)**
```python
import numpy as np

def wave_terrain_synthesis(freq, sr, duration, terrain_func, orbit_type="circular", r_mod=1.0, x_offset=0.0, y_offset=0.0, ratio_y=1.0):
    """
    Generates a sound wave using Wave Terrain Synthesis.
    
    Parameters:
    -----------
    freq : float
        Fundamental frequency of the orbit (Hz).
    sr : float
        Sampling rate in Hz.
    duration : float
        Duration of the generated signal in seconds.
    terrain_func : callable
        A function f(x, y) representing the 2D wave terrain, mapping R^2 to [-1.0, 1.0].
    orbit_type : str
        Type of scanning orbit: "circular" or "lissajous".
    r_mod : float or np.ndarray
        Orbit scale/radius modulation. Can be static or a time-varying envelope.
    x_offset : float or np.ndarray
        Horizontal center offset of the orbit in the terrain.
    y_offset : float or np.ndarray
        Vertical center offset of the orbit in the terrain.
    ratio_y : float
        Frequency multiplier for the y-axis in Lissajous mode (freq_y = freq * ratio_y).
        
    Returns:
    --------
    y : np.ndarray
        1D array of synthesised audio samples.
    """
    n_samples = int(sr * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # 1. Define orbital trajectories
    phase_x = 2.0 * np.pi * freq * t
    phase_y = 2.0 * np.pi * freq * ratio_y * t
    
    if orbit_type == "circular":
        x_orbit = np.cos(phase_x)
        y_orbit = np.sin(phase_x)
    elif orbit_type == "lissajous":
        x_orbit = np.sin(phase_x)
        y_orbit = np.sin(phase_y)
    else:
        x_orbit = np.cos(phase_x)
        y_orbit = np.sin(phase_x)
        
    # Apply dynamic radius and offset modulations
    x = x_offset + r_mod * x_orbit
    y = y_offset + r_mod * y_orbit
    
    # Keep trajectory within normal boundaries of terrain
    x = np.clip(x, -1.0, 1.0)
    y = np.clip(y, -1.0, 1.0)
    
    # 2. Read the audio height from the terrain function
    audio_out = terrain_func(x, y)
    
    # Normalize to prevent clipping
    max_val = np.max(np.abs(audio_out))
    if max_val > 0:
        audio_out = audio_out / max_val
        
    return audio_out

# Example Terrain Functions
def terrain_monkey_saddle(x, y):
    return x**3 - 3.0 * x * (y**2)

def terrain_ripples(x, y):
    r = np.sqrt(x**2 + y**2)
    return np.cos(3.0 * np.pi * r)

def terrain_fourier_sum(x, y):
    return 0.5 * np.sin(np.pi * x) * np.cos(np.pi * y) + 0.5 * np.cos(2.0 * np.pi * x) * np.sin(2.0 * np.pi * y)
```
"""

# Append to end of content
new_content = new_content.rstrip() + sp022_section

with open(filepath, "w") as f:
    f.write(new_content)

print("Appended SP-022 detailed description successfully!")
