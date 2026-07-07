#!/usr/bin/env python3
import os
import sys
import numpy as np
from mido import bpm2tempo
from scipy.io import wavfile

# Force project root into path
sys.path.insert(0, '/opt/data/repos')

# Now import the core library classes
from musicom.structures.unit import MusicUnit, MusicEvent
from musicom.structures.matrix import UnitMatrix
from musicom.workflows.unitmatrix_composer import UnitMatrixComposer

project_dir = "/opt/data/projects/Styles/Fanfare/005-fanfare-showband"
os.makedirs(f"{project_dir}/MIDI", exist_ok=True)
os.makedirs(f"{project_dir}/Audio", exist_ok=True)
os.makedirs(f"{project_dir}/Scores", exist_ok=True)

TPB = 480
TEMPO_BPM = 132
BAR_TICKS = TPB * 4

# Initialize the UnitMatrixComposer
composer = UnitMatrixComposer(
    bpm=TEMPO_BPM,
    ticks_per_beat=TPB,
    beats_per_bar=4
)

# 4 rows: 0=Trumpet (Lead), 1=Trombone (Mid), 2=Tuba (Bass), 3=Snare (Percussion)
# 8 columns: 8 Sections of 1 bar each
composer.create_matrix(num_voices=4, num_sections=8)

# Define our voices
composer.add_voice("Trumpet", program=56, channel=0)
composer.add_voice("Trombone", program=57, channel=1)
composer.add_voice("Tuba", program=58, channel=2)
composer.add_voice("Snare", program=0, channel=9)

# Define 8 sections, 1 bar each
for col in range(8):
    composer.add_section(f"Bar {col+1}", bars=1)

# Cyclic Fifths Down Chord degrees (1-indexed diatonic scale degrees)
progression = [1, 4, 7, 3, 6, 2, 5, 1]
key_root = 58  # Bb Major
scale = [0, 2, 4, 5, 7, 9, 11] # Bb Major diatonic steps

# Helper to find absolute pitch in diatonic key without wrapping transposition errors
def get_diatonic_note(degree_index):
    octave_shift = degree_index // 7
    scale_step = degree_index % 7
    return key_root + (octave_shift * 12) + scale[scale_step]

# Populate each of the 8 bar columns
for col, degree in enumerate(progression):
    # Absolute chord step indices (root, third, fifth)
    root_idx = degree - 1
    third_idx = degree + 1
    fifth_idx = degree + 3
    
    # 1. Tuba (Bass) Unit (Row 2): Driving downbeat pulses (exactly 1 bar length)
    # Beats 1 and 3 are on, beats 2 and 4 are silent.
    # Note offsets are start_tick, end_tick (MUST SUM UP / COVER ENTIRE CELL LENGTH)
    # Tuba notes must span ticks 0 -> BAR_TICKS in some form, or we must ensure the unit's internal len_ticks matches BAR_TICKS.
    # To keep exact lengths, let's span them precisely:
    bass_events = [
        MusicEvent(pitch=get_diatonic_note(root_idx) - 24, start_tick=0, end_tick=TPB, volume=95),
        # Silent gap (Beat 2): represented by empty tick space up to Beat 3, but the final event must close at BAR_TICKS to define length!
        MusicEvent(pitch=get_diatonic_note(fifth_idx) - 24, start_tick=TPB * 2, end_tick=TPB * 4, volume=95)
    ]
    composer.set_unit(2, col, MusicUnit(events=bass_events))
    
    # 2. Trombone (Mid) Unit (Row 1): Quarter note harmonies (exactly 1 bar length)
    mid_events = []
    for q in range(4):
        p = get_diatonic_note(third_idx) - 12 if q % 2 == 0 else get_diatonic_note(root_idx) - 12
        mid_events.append(MusicEvent(pitch=p, start_tick=q * TPB, end_tick=(q + 1) * TPB, volume=85))
    composer.set_unit(1, col, MusicUnit(events=mid_events))
    
    # 3. Trumpet (Lead) Unit (Row 0): Syncopated flourishes
    # Eighth-note grid: 0, 1.5, 2, 3.5. 
    # To ensure it reaches BAR_TICKS, the last syncopated note must hold or we add a tiny quiet note to close at BAR_TICKS (or simple end_tick alignment).
    lead_events = [
        MusicEvent(pitch=get_diatonic_note(root_idx) + 12, start_tick=0, end_tick=int(0.5 * TPB), volume=110),
        MusicEvent(pitch=get_diatonic_note(fifth_idx) + 12, start_tick=int(1.5 * TPB), end_tick=int(2.0 * TPB), volume=110),
        MusicEvent(pitch=get_diatonic_note(fifth_idx) + 12, start_tick=int(2.0 * TPB), end_tick=int(2.5 * TPB), volume=110),
        # Extend final syncopated note precisely to BAR_TICKS (4 * TPB) to maintain exact unit length!
        MusicEvent(pitch=get_diatonic_note(root_idx) + 12, start_tick=int(3.5 * TPB), end_tick=int(4.0 * TPB), volume=110)
    ]
    composer.set_unit(0, col, MusicUnit(events=lead_events))
    
    # 4. Snare Drum Unit (Row 3): Percussion rolls
    snare_events = []
    for eighth in range(8):
        vol = 100 if eighth % 2 == 0 else 70
        snare_events.append(MusicEvent(
            pitch=38, 
            start_tick=eighth * int(TPB/2), 
            end_tick=(eighth + 1) * int(TPB/2), # Complete eighth notes to cover the whole bar precisely
            volume=vol
        ))
    composer.set_unit(3, col, MusicUnit(events=snare_events))

# Export clean MIDI via UnitMatrix architecture
composer.to_midi(f"{project_dir}/MIDI/loop.mid")
print("Matrix validation and MIDI export: PASS")

# ----------------- FluidSynth Rendering Pipeline -----------------
sf2_path = "/opt/data/.local/lib/python3.13/site-packages/pretty_midi/TimGM6mb.sf2"
wav_path = f"{project_dir}/Audio/loop.wav"

if os.path.exists(sf2_path):
    print("SoundFont found. Invoking FluidSynth for authentic audio...")
    cmd = f"fluidsynth -ni '{sf2_path}' '{project_dir}/MIDI/loop.mid' -F '{wav_path}' -r 44100 2>&1"
    os.system(cmd)
else:
    print("Warning: SoundFont missing. Falling back to synth emulation...")
    # Math synthesis backup
    sr = 44100
    TOTAL_TICKS = BAR_TICKS * 8
    total_dur_s = (TOTAL_TICKS / TPB * 60 / TEMPO_BPM)
    audio = np.zeros(int(sr * total_dur_s), dtype=np.float32)
    m2f = lambda n: 440.0 * (2 ** ((n - 69) / 12.0))
    
    for track_idx in range(4):
        aligned_events = composer.matrix.get_row_events(track_idx)
        for e in aligned_events:
            st = int(e.start_tick / TPB * 60 / TEMPO_BPM * sr)
            dur_s = (e.end_tick - e.start_tick) / TPB * 60 / TEMPO_BPM
            en = st + int(dur_s * sr)
            if en > len(audio): continue
            t = np.arange(en - st) / sr
            if track_idx == 3: # Snare
                tone = np.random.uniform(-1, 1, en - st)
            else: # Brass
                freq = m2f(e.pitch)
                tone = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(4 * np.pi * freq * t)
            audio[st:en] += tone * (e.volume / 127.0) * 0.1
            
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio * 0.95 / max_val
    wavfile.write(wav_path, sr, audio.astype(np.float32))

print("ok")
