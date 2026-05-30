
import numpy as np
import wave
import os

SAMPLE_RATE = 44100
TEMPO = 100
BEAT_DUR = 60.0 / TEMPO  # 0.6s
MEASURE_DUR = BEAT_DUR * 4 # 2.4s

def midi_to_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0)) if midi > 0 else 0

def make_envelope(length, attack=0.01, release=0.1):
    env = np.ones(length) * 0.7
    a_s = min(int(attack * SAMPLE_RATE), length)
    r_s = min(int(release * SAMPLE_RATE), length)
    if a_s > 0: env[:a_s] = np.linspace(0, 1, a_s)
    if r_s > 0: env[-r_s:] = np.linspace(0.7, 0, r_s)
    return env

def synth(midi, dur, type='sine'):
    n = int(dur * SAMPLE_RATE)
    if midi <= 0 or n <= 0: return np.zeros(n)
    freq = midi_to_freq(midi)
    t = np.linspace(0, dur, n, endpoint=False)
    
    if type == 'bass':
        tone = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
        gain = 0.3
    elif type == 'pad':
        tone = np.sin(2 * np.pi * freq * t) + np.sin(2 * np.pi * freq * 1.005 * t)
        gain = 0.1
    else: # lead
        tone = np.sin(2 * np.pi * freq * t) + 0.1 * np.sin(2 * np.pi * freq * 3 * t)
        gain = 0.2
        
    return tone * make_envelope(n) * gain

# --- MATRIX ARCHITECTURE ---
# Rows = Tracks (Lead, Pad, Bass)
# Columns = Measures (1, 2, 3, 4)

D_DORIAN = [62, 64, 65, 67, 69, 71, 72] # D4, E4, F4, G4, A4, B4, C5

MATRIX = {
    "Lead": [
        [62, 0, 65, 0], # M1
        [67, 69, 71, 0],# M2
        [72, 0, 69, 67],# M3
        [65, 64, 62, 0] # M4
    ],
    "Pad": [
        [(50, 53, 57), (50, 53, 57)], # M1 (D minor)
        [(55, 58, 62), (55, 58, 62)], # M2 (G minor-ish / C dominant)
        [(53, 57, 60), (53, 57, 60)], # M3 (F major)
        [(50, 53, 57), (50, 53, 57)]  # M4 (Return)
    ],
    "Bass": [
        [38, 38, 41, 43], # M1
        [45, 45, 43, 41], # M2
        [38, 38, 41, 43], # M3
        [38, 0, 0, 0]      # M4
    ]
}

def render_matrix(matrix):
    num_measures = 4
    total_samples = int(num_measures * MEASURE_DUR * SAMPLE_RATE)
    master_mix = np.zeros(total_samples)
    
    for track_name, measures in matrix.items():
        print(f"Rendering Track: {track_name}")
        track_samples = np.array([])
        
        for m_idx, events in enumerate(measures):
            # Calculate duration per event in this measure
            step_dur = MEASURE_DUR / len(events)
            for event in events:
                if isinstance(event, tuple): # Chord
                    chord_sum = np.zeros(int(step_dur * SAMPLE_RATE))
                    for note in event:
                        chord_sum += synth(note, step_dur, type='pad' if track_name=='Pad' else 'lead')
                    track_samples = np.concatenate([track_samples, chord_sum])
                else: # Single Note
                    s_type = 'bass' if track_name == 'Bass' else 'lead'
                    track_samples = np.concatenate([track_samples, synth(event, step_dur, type=s_type)])
        
        # Mix track into master
        len_to_mix = min(len(track_samples), len(master_mix))
        master_mix[:len_to_mix] += track_samples[:len_to_mix]
        
    return master_mix

# Execution
audio = render_matrix(MATRIX)
out_path = '/tmp/hermes/songs/matrix_jazz_layered.wav'
with wave.open(out_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    wf.writeframes(audio_int16.tobytes())

print(f"DONE Matrix Render: {out_path}")
