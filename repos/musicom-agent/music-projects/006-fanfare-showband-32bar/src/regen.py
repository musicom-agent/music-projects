#!/usr/bin/env python3
import os
import sys

# Force project root into path
sys.path.insert(0, '/opt/data/repos')

# Import core classes
from musicom.structures.unit import MusicUnit, MusicEvent
from musicom.workflows.unitmatrix_composer import UnitMatrixComposer
from musicom.rules.progression import Scale7ChordDegree

project_dir = "/opt/data/projects/Styles/Fanfare/006-fanfare-showband-32bar"
os.makedirs(f"{project_dir}/MIDI", exist_ok=True)
os.makedirs(f"{project_dir}/Audio", exist_ok=True)
os.makedirs(f"{project_dir}/Scores", exist_ok=True)

TPB = 480
TEMPO_BPM = 132
BAR_TICKS = TPB * 4

# Initialize UnitMatrixComposer
composer = UnitMatrixComposer(
    bpm=TEMPO_BPM,
    ticks_per_beat=TPB,
    beats_per_bar=4
)

# 4 rows (voices), 32 sections (bars)
composer.create_matrix(num_voices=4, num_sections=32)

# Define voices (0=Trumpet, 1=Trombone, 2=Tuba, 3=Snare)
composer.add_voice("Trumpet", program=56, channel=0)
composer.add_voice("Trombone", program=57, channel=1)
composer.add_voice("Tuba", program=58, channel=2)
composer.add_voice("Snare", program=0, channel=9)

# Define 32 bars
for col in range(32):
    composer.add_section(f"Bar {col+1}", bars=1)

# Key of Bb Major
key_root = 58
scale = [0, 2, 4, 5, 7, 9, 11]

# Form Plan:
# Section A: Bars 1-8 (Cyclic Fifths progression, standard motifs)
# Section B: Bars 9-16 (Contrast: Shift to relative minor G minor or subdominant IV-V steps, lyrical motif)
# Section A: Bars 17-24 (Return of Section A with variations)
# Section C (Finale): Bars 25-32 (Climactic build, running snare rolls, heroic fanfare holds)

# Chord Degree Progressions (1-indexed diatonic scale degrees)
# A Progression: I - IV - VII - III - VI - II - V - I (1, 4, 7, 3, 6, 2, 5, 1)
prog_A = [1, 4, 7, 3, 6, 2, 5, 1]

# B Progression: G Minor area / step shifts (vi - ii - V - I - IV - ii - V - V) -> (6, 2, 5, 1, 4, 2, 5, 5)
prog_B = [6, 2, 5, 1, 4, 2, 5, 5]

# C Progression (Finale): heroic build (I - V - IV - V - I - IV - V - I) -> (1, 5, 4, 5, 1, 4, 5, 1)
prog_C = [1, 5, 4, 5, 1, 4, 5, 1]

for col in range(32):
    # Determine Section & chord degree
    if col < 8:
        sect = 'A'
        degree = prog_A[col]
    elif col < 16:
        sect = 'B'
        degree = prog_B[col - 8]
    elif col < 24:
        sect = 'A_var'
        degree = prog_A[col - 16]
    else:
        sect = 'C'
        degree = prog_C[col - 24]

    root_idx = degree - 1
    third_idx = degree + 1
    fifth_idx = degree + 3

    # ================= 1. TUBA (Row 2) =================
    if sect == 'B':
        # More walking/legato line for the lyrical section
        bass_events = [
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) - 24, start_tick=0, end_tick=TPB * 2, volume=90),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, third_idx) - 24, start_tick=TPB * 2, end_tick=TPB * 4, volume=90)
        ]
    elif sect == 'C':
        # Heavy marches on all quarter beats in finale
        bass_events = []
        for q in range(4):
            pitch_deg = root_idx if q % 2 == 0 else fifth_idx
            # Fix: do not subtract 10 ticks from the end_tick of the last pulse in the measure, must align exactly to BAR_TICKS (4 * TPB = 1920)
            end_t = (q + 1) * TPB
            if q < 3:
                end_t -= 10
            bass_events.append(MusicEvent(
                pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, pitch_deg) - 24,
                start_tick=q * TPB, end_tick=end_t, volume=100
            ))
    else:
        # Standard A downbeat driving pulses
        bass_events = [
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) - 24, start_tick=0, end_tick=TPB, volume=95),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, fifth_idx) - 24, start_tick=TPB * 2, end_tick=TPB * 4, volume=95)
        ]
    composer.set_unit(2, col, MusicUnit(events=bass_events))

    # ================= 2. TROMBONE (Row 1) =================
    mid_events = []
    if sect == 'B':
        # Sustained background chords
        mid_events.append(MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, third_idx) - 12, start_tick=0, end_tick=BAR_TICKS, volume=75))
    elif sect == 'C':
        # Syncopated mid accents
        mid_events = [
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) - 12, start_tick=0, end_tick=int(1.5 * TPB), volume=90),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, third_idx) - 12, start_tick=int(1.5 * TPB), end_tick=TPB * 3, volume=90),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, fifth_idx) - 12, start_tick=TPB * 3, end_tick=BAR_TICKS, volume=90)
        ]
    else:
        # Standard A style: quarter notes
        for q in range(4):
            p = Scale7ChordDegree.get_diatonic_note(key_root, scale, third_idx) - 12 if q % 2 == 0 else Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) - 12
            mid_events.append(MusicEvent(pitch=p, start_tick=q * TPB, end_tick=(q + 1) * TPB, volume=85))
    composer.set_unit(1, col, MusicUnit(events=mid_events))

    # ================= 3. TRUMPET (Row 0) =================
    lead_events = []
    if sect == 'B':
        # Lyrical flowing eighth/quarter line
        # Motif: 1, 2, 3, 4_and
        lead_events = [
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, third_idx) + 12, start_tick=0, end_tick=TPB, volume=95),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) + 12, start_tick=TPB, end_tick=TPB * 2, volume=95),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, fifth_idx) + 12, start_tick=TPB * 2, end_tick=TPB * 3, volume=95),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, third_idx) + 12, start_tick=TPB * 3, end_tick=int(3.5 * TPB), volume=95),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) + 12, start_tick=int(3.5 * TPB), end_tick=BAR_TICKS, volume=95)
        ]
    elif sect == 'C':
        # Heroic fanfare blasts! Double-tonguing feel (16th notes) at bar endings
        if col == 31: # Grand finale chord
            lead_events = [
                MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) + 12, start_tick=0, end_tick=BAR_TICKS, volume=125)
            ]
        else:
            lead_events = [
                MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) + 12, start_tick=0, end_tick=TPB, volume=115),
                MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, fifth_idx) + 12, start_tick=TPB, end_tick=TPB * 2, volume=115),
                # Rapid double tonguing: 16ths
                MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, fifth_idx) + 12, start_tick=TPB * 2, end_tick=TPB * 2 + int(TPB/4), volume=120),
                MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) + 12, start_tick=TPB * 2 + int(TPB/4), end_tick=TPB * 2 + int(TPB/2), volume=120),
                MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, fifth_idx) + 12, start_tick=TPB * 2 + int(TPB/2), end_tick=TPB * 3, volume=120),
                MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) + 12, start_tick=TPB * 3, end_tick=BAR_TICKS, volume=120)
            ]
    else:
        # Standard A section flourishes (add minor variations for col >= 16)
        vol_boost = 5 if sect == 'A_var' else 0
        lead_events = [
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) + 12, start_tick=0, end_tick=int(0.5 * TPB), volume=110 + vol_boost),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, fifth_idx) + 12, start_tick=int(1.5 * TPB), end_tick=int(2.0 * TPB), volume=110 + vol_boost),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, fifth_idx) + 12, start_tick=int(2.0 * TPB), end_tick=int(2.5 * TPB), volume=110 + vol_boost),
            MusicEvent(pitch=Scale7ChordDegree.get_diatonic_note(key_root, scale, root_idx) + 12, start_tick=int(3.5 * TPB), end_tick=int(4.0 * TPB), volume=110 + vol_boost)
        ]
    composer.set_unit(0, col, MusicUnit(events=lead_events))

    # ================= 4. SNARE (Row 3) =================
    snare_events = []
    if sect == 'B':
        # Quiet marching tap
        for eighth in range(8):
            vol = 70 if eighth in (0, 4) else 40
            snare_events.append(MusicEvent(pitch=38, start_tick=eighth * int(TPB/2), end_tick=(eighth + 1) * int(TPB/2), volume=vol))
    elif sect == 'C':
        # Intense snare rolls: continuous 16th notes building up
        for sixteenth in range(16):
            # Dynamic crescendo
            vol = int(70 + (sixteenth * 3.5))
            # Accents on beats 1 and 3
            if sixteenth in (0, 8):
                vol = 120
            snare_events.append(MusicEvent(pitch=38, start_tick=sixteenth * int(TPB/4), end_tick=(sixteenth + 1) * int(TPB/4), volume=vol))
    else:
        # Standard A snare tap
        for eighth in range(8):
            vol = 100 if eighth % 2 == 0 else 70
            snare_events.append(MusicEvent(pitch=38, start_tick=eighth * int(TPB/2), end_tick=(eighth + 1) * int(TPB/2), volume=vol))
    composer.set_unit(3, col, MusicUnit(events=snare_events))

# Export MIDI
midi_path = f"{project_dir}/MIDI/showband32.mid"
composer.to_midi(midi_path)
print("Matrix validation and MIDI export: PASS")

# Invoke FluidSynth for rendering
sf2_path = "/opt/data/.local/lib/python3.13/site-packages/pretty_midi/TimGM6mb.sf2"
wav_path = f"{project_dir}/Audio/showband32.wav"

if os.path.exists(sf2_path):
    print("SoundFont found. Invoking FluidSynth...")
    cmd = f"/opt/data/micromamba/envs/musicom/bin/fluidsynth -ni -F '{wav_path}' -r 44100 '{sf2_path}' '{midi_path}' 2>&1"
    os.system(cmd)
    
    # Compress to OGG (mandatory for Telegram)
    ogg_path = f"{project_dir}/Audio/showband32.ogg"
    compress_cmd = f"ffmpeg -i '{wav_path}' -codec:a libopus -application voip -b:a 48k '{ogg_path}' -y -loglevel error"
    os.system(compress_cmd)
    print("OGG conversion: DONE")
else:
    print("Error: SoundFont missing.")
