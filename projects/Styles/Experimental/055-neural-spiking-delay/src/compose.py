# -*- coding: utf-8 -*-
"""
Project 055: Neural Spiking + Feedback Delay Line
Composition Method: 037 (FitzHugh-Nagumo Neural Spiking - FHNS)
Sound Production: SP-013 (Feedback Delay Line with HF Damping)

FitzHugh-Nagumo equations simulate neural membrane potential dynamics.
Voltage threshold crossings -> rhythmic events.
Voltage levels -> pitch mapping (quantized to E minor scale).
Refractory periods -> natural rhythmic gaps.

SP-013: Post-render damped delay applied to WAV output.
"""
import os
import numpy as np

from structures import MusicUnit, MusicEvent, MidiInstrument
from workflows.unitmatrix_composer import (
    UnitMatrixComposer, create_note_unit, create_chord_unit, create_empty_unit,
)
from ai.utils.visualizer import write_grid_visualization
from workflows.provenance import write_provenance, AI_ASSISTED

# ---------------------------------------------------------------- CONFIG -----
PROJECT_NAME = "055-neural-spiking-delay"
OUTPUT_DIR = f"/opt/data/projects/Styles/Experimental/{PROJECT_NAME}"
BPM = 100
TICKS_PER_BEAT = 480
BEATS_PER_BAR = 4
BAR = TICKS_PER_BEAT * BEATS_PER_BAR  # 1920

# Key: E minor (aeolian)
KEY_ROOT = 4  # E
SCALE = [0, 2, 3, 5, 7, 8, 10]  # E F# G A B C D

# --- FitzHugh-Nagumo Parameters ---
# dv/dt = v - v^3/3 - w + I
# dw/dt = (v + a - b*w) / tau
FHN_A = 0.7
FHN_B = 0.8
FHN_TAU = 12.5
FHN_DT = 0.01  # integration timestep

# External drive per neuron (creates different firing rates)
# Neuron1: moderate, Neuron2: fast, Bass: slow, Pad: very slow
I_DRIVES = {
    "Lead": 0.6,
    "Tenor": 0.8,
    "Bass": 0.35,
    "Pad": 0.25,
}

# Voltage threshold for spike detection
SPIKE_THRESHOLD = 0.5

# Refractory period in ticks (minimum gap between events)
REFRACTORY_TICKS = {
    "Lead": 120,   # eighth note min gap
    "Tenor": 180,  # dotted eighth
    "Bass": 480,   # quarter note
    "Pad": 960,    # half note
}

# Base octaves and velocities per voice
VOICE_CONFIG = {
    "Lead":  {"octave": 4, "vel": 95, "program": 73, "dur": 180},  # flute
    "Tenor": {"octave": 3, "vel": 80, "program": 0,  "dur": 240},  # piano
    "Bass":  {"octave": 2, "vel": 100,"program": 33, "dur": 720},  # bass
    "Pad":   {"octave": 3, "vel": 65, "program": 48, "dur": 1440}, # strings
}


def fitzhugh_nagumo_step(v, w, I_ext):
    """Single FHN integration step."""
    dv = v - v**3 / 3.0 - w + I_ext
    dw = (v + FHN_A - FHN_B * w) / FHN_TAU
    return v + FHN_DT * dv, w + FHN_DT * dw


def generate_voltage_trace(n_steps, I_ext, v0=-0.5, w0=-0.3):
    """Generate FHN voltage trace for given number of steps."""
    v_trace = np.zeros(n_steps)
    w_trace = np.zeros(n_steps)
    v_trace[0] = v0
    w_trace[0] = w0
    
    for i in range(n_steps - 1):
        v_trace[i+1], w_trace[i+1] = fitzhugh_nagumo_step(
            v_trace[i], w_trace[i], I_ext
        )
    
    return v_trace


def detect_spikes(v_trace, threshold, refractory_steps):
    """Detect upward threshold crossings with refractory period."""
    spikes = []
    last_spike = -refractory_steps
    
    for i in range(1, len(v_trace)):
        if v_trace[i-1] < threshold and v_trace[i] >= threshold:
            if i - last_spike >= refractory_steps:
                spikes.append(i)
                last_spike = i
    
    return spikes


def voltage_to_midi(v_value, scale, key_root, base_octave):
    """Map voltage to nearest scale degree."""
    # Normalize v to [0, 1] (v typically -2 to +2)
    norm = (v_value + 2.0) / 4.0
    norm = np.clip(norm, 0.0, 0.99)
    
    # Map to scale degree
    degree = int(norm * len(scale))
    octave_offset = degree // len(scale)
    degree_in_scale = degree % len(scale)
    
    midi = 12 * (base_octave + octave_offset + 1) + key_root + scale[degree_in_scale]
    return max(36, min(84, midi))


def build_neural_unit(v_trace, section_ticks, voice_name, steps_per_tick):
    """
    Convert voltage trace to MusicUnit.
    Spikes become note onsets. Voltage at spike determines pitch.
    """
    config = VOICE_CONFIG[voice_name]
    refractory_steps = int(REFRACTORY_TICKS[voice_name] * steps_per_tick)
    
    # Detect spikes
    spike_indices = detect_spikes(v_trace, SPIKE_THRESHOLD, refractory_steps)
    
    events = []
    for sp_idx in spike_indices:
        # Convert step index to tick
        tick = int(sp_idx / steps_per_tick)
        tick = max(0, min(tick, section_ticks - 20))
        
        # Get voltage at spike for pitch
        v_at_spike = v_trace[min(sp_idx, len(v_trace)-1)]
        midi_pitch = voltage_to_midi(v_at_spike, SCALE, KEY_ROOT, config["octave"])
        
        # Velocity from voltage magnitude
        vel = int(config["vel"] * (0.5 + 0.5 * abs(v_at_spike) / 2.0))
        vel = max(40, min(127, vel))
        
        # Duration
        dur = config["dur"]
        
        # Prevent overlap
        if events and tick <= events[-1].end_tick:
            tick = events[-1].end_tick + 10
        if tick + dur > section_ticks:
            dur = section_ticks - tick
        if dur < 20:
            continue
        
        events.append(MusicEvent(
            pitch=midi_pitch,
            volume=vel,
            start_tick=tick,
            end_tick=tick + dur
        ))
    
    # Ensure unit fills to section_ticks: add silent padding event
    if events:
        last_end = events[-1].end_tick
        if last_end < section_ticks:
            events.append(MusicEvent(
                pitch=0, volume=0,
                start_tick=section_ticks - 1,
                end_tick=section_ticks
            ))
    else:
        # Empty section: single silent event spanning full length
        events.append(MusicEvent(
            pitch=0, volume=0,
            start_tick=0,
            end_tick=section_ticks
        ))
    
    return MusicUnit(events=events)


def build_composer():
    """Build the full composition using FHN neural spiking."""
    c = UnitMatrixComposer(bpm=BPM, ticks_per_beat=TICKS_PER_BEAT, beats_per_bar=BEATS_PER_BAR)
    c.create_matrix(num_voices=4, num_sections=3)
    
    # Voices
    c.add_voice("Lead", program=VOICE_CONFIG["Lead"]["program"], channel=0)
    c.add_voice("Tenor", program=VOICE_CONFIG["Tenor"]["program"], channel=1)
    c.add_voice("Bass", program=VOICE_CONFIG["Bass"]["program"], channel=2)
    c.add_voice("Pad", program=VOICE_CONFIG["Pad"]["program"], channel=3)
    
    # Sections: A (4 bars), B (8 bars), A' (4 bars)
    c.add_section("A", bars=4)
    c.add_section("B", bars=8)
    c.add_section("Ap", bars=4)
    
    section_bars = {"A": 4, "B": 8, "Ap": 4}
    section_ticks = {k: v * BAR for k, v in section_bars.items()}
    
    # FHN simulation: steps per tick determines resolution
    # We want ~100 steps per tick for smooth dynamics
    steps_per_tick = 100
    
    # Generate voltage traces per voice per section
    # Different I_drives create different firing patterns
    voice_names = ["Lead", "Tenor", "Bass", "Pad"]
    
    for sec_name in ["A", "B", "Ap"]:
        sec_ticks = section_ticks[sec_name]
        n_steps = int(sec_ticks * steps_per_tick)
        
        for v_name in voice_names:
            # Generate FHN trace with voice-specific drive
            v0 = -0.5 + 0.1 * voice_names.index(v_name)
            w0 = -0.3 + 0.05 * voice_names.index(v_name)
            v_trace = generate_voltage_trace(
                n_steps, I_DRIVES[v_name], v0=v0, w0=w0
            )
            
            # Convert to musical unit
            unit = build_neural_unit(v_trace, sec_ticks, v_name, steps_per_tick)
            c.fill_voice_section(v_name, sec_name, unit)
    
    return c


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "MIDI"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "Audio"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "Analysis"), exist_ok=True)
    
    composer = build_composer()
    
    # Zero-drift gate
    ok, msg = composer.validate()
    if not ok:
        raise SystemExit(f"Validation failed: {msg}")
    
    midi_path = os.path.join(OUTPUT_DIR, "MIDI", f"{PROJECT_NAME}.mid")
    composer.to_midi(midi_path)
    
    size = os.path.getsize(midi_path)
    if size <= 40:
        raise SystemExit(f"MIDI empty/corrupt: {size} bytes")
    
    # Grid visualization
    write_grid_visualization(
        composer.matrix,
        os.path.join(OUTPUT_DIR, "Analysis", "grid_visualization.txt"),
        ticks_per_character=240, bpm=BPM
    )
    
    # Provenance
    write_provenance(
        midi_path, classification=AI_ASSISTED,
        generator=f"{PROJECT_NAME}/src/compose.py",
        parameters={
            "bpm": BPM,
            "method": "037-FHNS",
            "sp_method": "SP-013-FDL",
            "key": "E minor (aeolian)",
            "form": "A(4)-B(8)-A'(4)",
            "fhn_params": {"a": FHN_A, "b": FHN_B, "tau": FHN_TAU, "dt": FHN_DT},
            "i_drives": I_DRIVES,
            "spike_threshold": SPIKE_THRESHOLD,
            "refractory_ticks": REFRACTORY_TICKS,
            "voices": {
                "Lead": "Flute (73)",
                "Tenor": "Piano (0)",
                "Bass": "Electric Bass (33)",
                "Pad": "Strings (48)"
            },
        },
        notes="FitzHugh-Nagumo neural spiking drives rhythmic events. "
              "Voltage threshold crossings = note onsets. "
              "Voltage level = pitch (E minor quantized). "
              "Refractory periods create natural rhythmic gaps. "
              "SP-013: Feedback Delay with HF damping applied post-render."
    )
    
    print(f"OK: {midi_path} ({size} bytes)")
    print(f"Validation: {ok} - {msg}")


if __name__ == "__main__":
    main()
