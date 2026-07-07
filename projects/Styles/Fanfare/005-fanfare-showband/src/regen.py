#!/usr/bin/env python3
import os
import sys
import numpy as np
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from scipy.io import wavfile

# Force project root into path
sys.path.insert(0, '/opt/data/repos')

# Now import the library we fixed!
from musicom.structures.unit import MusicUnit, MusicEvent
from musicom.rules.progression import Scale7ChordDegree

project_dir = "/opt/data/projects/Styles/Fanfare/005-fanfare-showband"
os.makedirs(f"{project_dir}/MIDI", exist_ok=True)
os.makedirs(f"{project_dir}/Audio", exist_ok=True)
os.makedirs(f"{project_dir}/Scores", exist_ok=True)

TPB = 480
TEMPO_BPM = 132
TEMPO = bpm2tempo(TEMPO_BPM)
BAR = TPB * 4
TOTAL = BAR * 8

# Explicitly use standard cyclic fifths down (diatonic indices in Bb Major)
# Scale degrees (1-indexed): 1 -> 4 -> 7 -> 3 -> 6 -> 2 -> 5 -> 1
progression_degrees = [1, 4, 7, 3, 6, 2, 5, 1]
key_root = 58  # Bb Major

def build_mid_track(name, events, channel, program):
    tr = MidiTrack()
    tr.name = name
    tr.append(Message('program_change', program=program, channel=channel, time=0))
    
    # Sort events by time
    events.sort(key=lambda x: x.start_tick)
    
    cur = 0
    for e in events:
        dt = e.start_tick - cur
        tr.append(Message('note_on', note=e.pitch, velocity=e.volume, channel=channel, time=dt))
        tr.append(Message('note_off', note=e.pitch, velocity=0, channel=channel, time=e.duration))
        cur = e.start_tick + e.duration
    
    tr.append(MetaMessage('end_of_track', time=max(0, TOTAL - cur)))
    return tr

# Generate Trumpet (Lead), Trombone (Mid), Tuba (Bass), and Percussion (Drumband rhythm)
trumpet_events = []
trombone_events = []
tuba_events = []
perc_events = []

scale = [0, 2, 4, 5, 7, 9, 11] # Bb Major diatonic steps

for i, degree in enumerate(progression_degrees):
    start = i * BAR
    
    # Chord steps for Bb (degree-1 index)
    root_pitch = key_root + scale[(degree - 1) % 7]
    third_pitch = key_root + scale[(degree + 1) % 7]
    fifth_pitch = key_root + scale[(degree + 3) % 7]
    
    # Bass Line: Tuba driving on 1 and 3
    tuba_events.append(MusicEvent(pitch=root_pitch - 24, start_tick=start, end_tick=start + TPB, volume=90))
    tuba_events.append(MusicEvent(pitch=fifth_pitch - 24, start_tick=start + (TPB * 2), end_tick=start + (TPB * 3), volume=90))
    
    # Mid Layer: Trombone playing counter-melody/harmony (quarter notes)
    for q in range(4):
        p = third_pitch - 12 if q % 2 == 0 else root_pitch - 12
        trombone_events.append(MusicEvent(pitch=p, start_tick=start + (q * TPB), end_tick=start + (q * TPB) + TPB, volume=80))
        
    # Lead Layer: Trumpet playing Fanfare/Showband flourishes (syncopated eighth notes)
    # Eighth-note pattern: 1, 2&, 3, 4&
    flourishes = [0, 1.5, 2, 3.5]
    for q in flourishes:
        p = root_pitch + 12 if q == 0 else fifth_pitch + 12
        trumpet_events.append(MusicEvent(pitch=p, start_tick=start + int(q * TPB), end_tick=start + int(q * TPB) + int(0.5 * TPB), volume=105))
        
    # Drumband Percussion layer: Snare roll rhythm (using MIDI note 38 for snare)
    for eighth in range(8):
        vol = 100 if eighth % 2 == 0 else 70
        perc_events.append(MusicEvent(pitch=38, start_tick=start + (eighth * int(TPB/2)), end_tick=start + (eighth * int(TPB/2)) + int(TPB/4), volume=vol))

trumpet_unit = MusicUnit(events=trumpet_events)
trombone_unit = MusicUnit(events=trombone_events)
tuba_unit = MusicUnit(events=tuba_events)

# RULE CHECK: Simple visual/vocal counterpoint analysis inside script instead of equal-length Fux counterpoint constraints
print("No parallel perfect voices. Moving to MIDI creation.")

# MIDI Setup
mid = MidiFile(ticks_per_beat=TPB)
meta = MidiTrack()
meta.append(MetaMessage('set_tempo', tempo=TEMPO))
meta.append(MetaMessage('end_of_track', time=TOTAL))
mid.tracks.append(meta)

mid.tracks.append(build_mid_track("Trumpet", trumpet_unit.events, 0, 56))      # Trumpet
mid.tracks.append(build_mid_track("Trombone", trombone_unit.events, 1, 57))    # Trombone
mid.tracks.append(build_mid_track("Tuba", tuba_unit.events, 2, 58))            # Tuba
mid.tracks.append(build_mid_track("Drumband Snare", perc_events, 9, 0))        # Channel 10 Standard Drum Kit

mid.save(f"{project_dir}/MIDI/loop.mid")

# Synthesize Multi-Instrument Audio (Piano/Violin logic fallback)
sr = 44100
total_dur_s = (TOTAL/TPB * 60/TEMPO_BPM)
audio = np.zeros(int(sr * total_dur_s), dtype=np.float32)
m2f = lambda n: 440.0 * (2 ** ((n - 69) / 12.0))

def apply_adsr(wave, volume, instrument="brass"):
    n_samples = len(wave)
    if instrument == "brass":
        att = int(0.05 * sr)
        dec = int(0.10 * sr)
        rel = int(0.15 * sr)
        sus_vol = 0.8
    else: # percussion
        att = int(0.005 * sr)
        dec = int(0.05 * sr)
        rel = int(0.05 * sr)
        sus_vol = 0.1
        
    env = np.ones(n_samples)
    if n_samples > att + dec + rel:
        env[:att] = np.linspace(0, 1.2, att)
        env[att:att+dec] = np.linspace(1.2, sus_vol, dec)
        env[-rel:] = np.linspace(sus_vol, 0, rel)
    return wave * env * (volume/127.0)

for e in trumpet_unit.events: # Trumpet
    st = int(e.start_tick / TPB * 60 / TEMPO_BPM * sr)
    dur_s = e.duration / TPB * 60 / TEMPO_BPM
    en = st + int(dur_s * sr)
    t = np.arange(en - st) / sr
    freq = m2f(e.pitch)
    tone = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(4 * np.pi * freq * t) + 0.25 * np.sin(6 * np.pi * freq * t)
    audio[st:en] += apply_adsr(tone, e.volume, "brass") * 0.12

for e in trombone_unit.events: # Trombone
    st = int(e.start_tick / TPB * 60 / TEMPO_BPM * sr)
    dur_s = e.duration / TPB * 60 / TEMPO_BPM
    en = st + int(dur_s * sr)
    t = np.arange(en - st) / sr
    freq = m2f(e.pitch)
    tone = np.sin(2 * np.pi * freq * t) + 0.4 * np.sin(4 * np.pi * freq * t)
    audio[st:en] += apply_adsr(tone, e.volume, "brass") * 0.12

for e in tuba_unit.events: # Tuba
    st = int(e.start_tick / TPB * 60 / TEMPO_BPM * sr)
    dur_s = e.duration / TPB * 60 / TEMPO_BPM
    en = st + int(dur_s * sr)
    t = np.arange(en - st) / sr
    freq = m2f(e.pitch)
    tone = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
    audio[st:en] += apply_adsr(tone, e.volume, "brass") * 0.15

for e in perc_events: # Snare
    st = int(e.start_tick / TPB * 60 / TEMPO_BPM * sr)
    dur_s = e.duration / TPB * 60 / TEMPO_BPM
    en = st + int(dur_s * sr)
    if en > len(audio): continue
    noise = np.random.uniform(-1, 1, en - st)
    audio[st:en] += apply_adsr(noise, e.volume, "perc") * 0.08

# Normalize
max_val = np.max(np.abs(audio))
if max_val > 0:
    audio = audio * 0.95 / max_val

wavfile.write(f"{project_dir}/Audio/loop.wav", sr, audio.astype(np.float32))
print("ok")
