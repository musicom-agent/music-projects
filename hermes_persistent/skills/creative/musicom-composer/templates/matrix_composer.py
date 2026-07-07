import numpy as np
import wave
import os

SAMPLE_RATE = 44100
TEMPO = 100
BEAT_DUR = 60.0 / TEMPO
MEASURE_DUR = BEAT_DUR * 4

def midi_to_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0)) if midi > 0 else 0

def synth(midi, dur, type='lead'):
    n = int(dur * SAMPLE_RATE)
    if midi <= 0 or n <= 0: return np.zeros(n)
    freq = midi_to_freq(midi)
    t = np.linspace(0, dur, n, endpoint=False)
    tone = np.sin(2 * np.pi * freq * t)
    # Simple ADSR
    env = np.ones(n)
    a = min(int(0.01 * SAMPLE_RATE), n)
    r = min(int(0.1 * SAMPLE_RATE), n)
    if a > 0: env[:a] = np.linspace(0, 1, a)
    if r > 0: env[-r:] = np.linspace(1, 0, r)
    return tone * env * 0.2

def render_matrix(matrix):
    # matrix: { "Track": [[m1_events], [m2_events]...] }
    num_measures = len(next(iter(matrix.values())))
    total_samples = int(num_measures * MEASURE_DUR * SAMPLE_RATE)
    master_mix = np.zeros(total_samples)
    
    for track_name, measures in matrix.items():
        track_samples = np.array([])
        for m_idx, events in enumerate(measures):
            step_dur = MEASURE_DUR / len(events)
            for event in events:
                track_samples = np.concatenate([track_samples, synth(event, step_dur)])
        
        len_to_mix = min(len(track_samples), len(master_mix))
        master_mix[:len_to_mix] += track_samples[:len_to_mix]
    return master_mix
