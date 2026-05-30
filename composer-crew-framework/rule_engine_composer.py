
import numpy as np
import wave

SAMPLE_RATE = 44100
TEMPO = 110
BEAT_DUR = 60.0 / TEMPO

def midi_to_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0)) if midi > 0 else 0

def synth(midi, dur, type='sine'):
    n = int(dur * SAMPLE_RATE)
    if midi <= 0 or n <= 0: return np.zeros(n)
    freq = midi_to_freq(midi)
    t = np.linspace(0, dur, n, endpoint=False)
    # Simple warm synth
    tone = np.sin(2 * np.pi * freq * t) + 0.2 * np.sin(2 * np.pi * freq * 2 * t)
    # Basic envelope
    env = np.ones(n)
    a = min(int(0.01 * SAMPLE_RATE), n)
    r = min(int(0.1 * SAMPLE_RATE), n)
    if a > 0: env[:a] = np.linspace(0, 1, a)
    if r > 0: env[-r:] = np.linspace(1, 0, r)
    return tone * env * 0.2

# --- THE THEORETICIAN'S RULE ENGINE ---

D_DORIAN = [62, 64, 65, 67, 69, 71, 72] # i, ii, III, IV, v, vi, VII

# 1. HARMONIC PROGRESSION (The Windows)
# Format: (Degree, Quality) 
PROGRESSION = [1, 4, 7, 3] # i -> iv -> VII -> III

# 2. SEED PATTERN (The Melodic DNA)
# Intervallic distances relative to scale indices (0, 1, 2...)
MELODIC_DNA = [0, 2, 4, 2] # Root -> 3rd -> 5th -> 3rd

# 3. RULE-BASED MATRIX
MATRIX_RULES = {
    "Lead": [
        "FOLLOW_CHORD",      # M1: Direct mapping
        "INVERT_CONTOUR",    # M2: Play mirror of DNA
        "TRANSPOSE_UP_2",    # M3: DNA shifted up 2 scale degrees
        "FOLLOW_CHORD"       # M4: Resolve
    ],
    "Bass": [
        "ROOT_ONLY",
        "ROOT_AND_FIFTH",
        "WALKING",
        "ROOT_ONLY"
    ]
}

def render_rule_based():
    master_audio = np.array([])
    
    for m_idx in range(len(PROGRESSION)):
        chord_root_idx = PROGRESSION[m_idx] - 1 # 0-indexed degree
        root_midi = D_DORIAN[chord_root_idx]
        
        # Calculate Lead Note based on Rule
        rule = MATRIX_RULES["Lead"][m_idx]
        measure_audio = np.zeros(int(BEAT_DUR * 4 * SAMPLE_RATE))
        
        # Apply Logic to Melodic DNA
        transformed_pitches = []
        for i, scale_offset in enumerate(MELODIC_DNA):
            if rule == "FOLLOW_CHORD":
                # Relative to current chord root
                p = D_DORIAN[(chord_root_idx + scale_offset) % len(D_DORIAN)]
            elif rule == "INVERT_CONTOUR":
                # Mirror around root
                p = D_DORIAN[(chord_root_idx - scale_offset) % len(D_DORIAN)]
            elif rule == "TRANSPOSE_UP_2":
                # DNA + 2 degrees
                p = D_DORIAN[(chord_root_idx + scale_offset + 2) % len(D_DORIAN)]
            else:
                p = root_midi
            transformed_pitches.append(p)
            
        # Synthesize Measure
        for p in transformed_pitches:
            measure_audio = np.concatenate([measure_audio, synth(p, BEAT_DUR)])
            
        master_audio = np.concatenate([master_audio, measure_audio])

    return master_audio

# Execute
audio = render_rule_based()
out_path = '/tmp/hermes/songs/rule_based_composition.wav'
with wave.open(out_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    wf.writeframes(audio_int16.tobytes())

print(f"DONE Rule-Based Logic: {out_path}")
