
import sys
import os
import wave
import numpy as np

# Mocking the Musicom paths 
sys.path.insert(0, '/root/musicom')

SAMPLE_RATE = 44100

def midi_to_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0)) if midi > 0 else 0

def make_envelope(length, attack_s=0.01, release_s=0.1):
    env = np.ones(length) * 0.7
    attack_samples = min(int(attack_s * SAMPLE_RATE), length)
    release_samples = min(int(release_s * SAMPLE_RATE), length)
    if attack_samples > 0:
        env[:attack_samples] = np.linspace(0, 1, attack_samples)
    if release_samples > 0:
        env[-release_samples:] = np.linspace(0.7, 0, release_samples)
    return env

def generate_tone(midi_note, duration_s, gain=0.2):
    n = int(duration_s * SAMPLE_RATE)
    if midi_note <= 0: return np.zeros(n)
    freq = midi_to_freq(midi_note)
    t = np.linspace(0, duration_s, n, endpoint=False)
    tone = (np.sin(2 * np.pi * freq * t) + 
            0.1 * np.sin(2 * np.pi * freq * 2 * t) +
            0.05 * np.sin(2 * np.pi * freq * 3 * t))
    return tone * make_envelope(n) * gain

# --- Role Implementations ---

class Theoretician:
    def __init__(self):
        self.role = "Music Theoretician"
        self.context = "Mysterious Ambient Jazz"
    
    def decide_tonality(self):
        # Decisions for "Mysterious Ambient Jazz"
        return {"tonic": "D", "mode": "Dorian", "scale": [62, 64, 65, 67, 69, 71, 72, 74]}

class Melodist:
    def __init__(self, scale):
        self.role = "Melodic Composer"
        self.scale = scale
    
    def create_patterns(self):
        # Pitch pattern (motif): up 1, up 2, down 1, stay
        pitch_pattern = [0, 2, 4, 3, 3] # scale indices
        # Rhythm: Euclidean(3, 8)
        rhythm_steps = [1, 0, 0, 1, 0, 0, 1, 0] # 1=onset, 0=rest
        return pitch_pattern, rhythm_steps

class Arranger:
    def __init__(self, scale, melody_pattern, rhythm):
        self.role = "Arranger & Export Specialist"
        self.scale = scale
        self.melody_pattern = melody_pattern
        self.rhythm = rhythm
    
    def compose(self):
        output = np.array([])
        beat_dur = 0.5 
        pattern_len = len(self.rhythm)
        
        # 4 bars of melody
        for i in range(16): # 16 steps total
            step = i % pattern_len
            if self.rhythm[step] == 1:
                # Get pitch from pattern (cycling)
                p_idx = (i // 2) % len(self.melody_pattern)
                pitch = self.scale[self.melody_pattern[p_idx]]
                output = np.concatenate([output, generate_tone(pitch, beat_dur)])
            else:
                output = np.concatenate([output, np.zeros(int(beat_dur * SAMPLE_RATE))])
        return output

# --- Execution ---
print("--- Musicom Composer Framework (Internal Roles) ---")

theory = Theoretician()
tonality = theory.decide_tonality()
print(f"[{theory.role}]: Decided on {tonality['tonic']} {tonality['mode']}")

melodist = Melodist(tonality['scale'])
p_pattern, rhythm = melodist.create_patterns()
print(f"[{melodist.role}]: Created pitch motif {p_pattern} with rhythm {rhythm}")

arranger = Arranger(tonality['scale'], p_pattern, rhythm)
audio = arranger.compose()
print(f"[{arranger.role}]: Arrangement complete. Exporting audio...")

# Save Result
out_path = '/tmp/hermes/songs/mysterious_jazz_internal.wav'
with wave.open(out_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    wf.writeframes(audio_int16.tobytes())

print(f"DONE: {out_path}")
