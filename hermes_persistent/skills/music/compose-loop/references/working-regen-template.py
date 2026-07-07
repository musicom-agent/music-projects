#!/usr/bin/env python3
"""Working regen.py template for Country loop.
Verified 2025-07-03 — MIDI + real WAV output.
"""
import os
import sys
sys.path.insert(0, '/opt/data/repos/musicom')

import numpy as np
from structures.unit import MusicEvent, MusicUnit
from structures.project import MusicVoice
from structures.matrix import UnitMatrix
from converters import export_midi, export_audio, export_musicxml
from visualization.dashboard import generate_dashboard

# Fallback RhythmGenerator — musicpy not installed
class RhythmGenerator:
    def __init__(self, onsets=8, timesteps=16):
        self.onsets = onsets
        self.timesteps = timesteps
    def generate(self):
        grid = np.zeros(self.timesteps)
        for i in range(self.timesteps):
            grid[i] = 0.5 if i % 2 == 1 else 1.0
        return [type('obj', (object,), {'onset_intervals': grid.tolist()})()]

# Fallback MusicPitchClassSet — avoids broken relative import
class MusicPitchClassSet:
    def __init__(self, name, definition, rotation, initial):
        self.name = name
        self.initial = initial
    def get_chord(self, degree, octave=5):
        notes = [7, 9, 11, 12, 14, 16, 18]  # G Ionian
        idx = (degree - 1) % 7
        base = notes[idx]
        return [base + 12 * o for o in range(3)]

PatternType = type('PatternType', (), {'HEPTATONIC': 1})()

# --- Concept ---
scale = MusicPitchClassSet(
    name="G Ionian",
    definition=PatternType.HEPTATONIC,
    rotation=0,
    initial=7
)

chord_degrees = [1, 4, 1, 5, 4, 1, 5, 1]
pitch_pattern = (0, 7, 12, 7, 2, 7, 0, 7)
rhythm = RhythmGenerator(onsets=8, timesteps=16).generate()[0]

# --- Build Melody ---
current_pitch = 67
melody_events = []
tick = 0
step = 60

for i, onset_interval in enumerate(rhythm.onset_intervals):
    interval = pitch_pattern[i % len(pitch_pattern)]
    pitch = max(55, min(83, current_pitch + interval))
    melody_events.append(MusicEvent(
        pitch=pitch, volume=100,
        start_tick=tick, end_tick=tick + step
    ))
    tick += int(step * onset_interval)
melody = MusicUnit(events=melody_events)

# --- Build Harmony ---
chord_events = []
tick = 0
for degree in chord_degrees:
    for pitch in scale.get_chord(degree, octave=5):
        chord_events.append(MusicEvent(
            pitch=pitch, volume=90,
            start_tick=tick, end_tick=tick + step * 4
        ))
    tick += step * 2
chords = MusicUnit(events=chord_events)

# --- Build Bass ---
bass_events = []
tick = 0
for degree in chord_degrees:
    for pitch in scale.get_chord(degree, octave=3):
        bass_events.append(MusicEvent(
            pitch=pitch, volume=110,
            start_tick=tick, end_tick=tick + step
        ))
    tick += step * 2
bass = MusicUnit(events=bass_events)

# --- Build Drums ---
drum_events = []
tick = 0
for bar in range(16):
    for beat in [0, 2]:
        drum_events.append(MusicEvent(
            pitch=36, volume=100,
            start_tick=tick + beat * step,
            end_tick=tick + beat * step + step // 2
        ))
    for beat in [1, 3]:
        drum_events.append(MusicEvent(
            pitch=38, volume=90,
            start_tick=tick + beat * step,
            end_tick=tick + beat * step + step // 2
        ))
    tick += step * 4
drums = MusicUnit(events=drum_events)

# --- Structure ---
matrix = UnitMatrix(shape=(4, 1))
matrix.set_unit((0, 0), melody)
matrix.set_unit((1, 0), chords)
matrix.set_unit((2, 0), bass)
matrix.set_unit((3, 0), drums)

# --- Export ---
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(f"{project_dir}/MIDI", exist_ok=True)
os.makedirs(f"{project_dir}/Audio", exist_ok=True)

export_midi(matrix, f"{project_dir}/MIDI/loop.mid")

# Render real WAV from MIDI
from music21 import converter
from scipy.io import wavfile

score = converter.parse(f"{project_dir}/MIDI/loop.mid")
sr = 44100
duration = 10.0
t = np.linspace(0, duration, int(sr * duration), endpoint=False)
audio = np.zeros_like(t)

for n in score.flatten().notesAndRests:
    if hasattr(n, 'pitch'):
        freq = n.pitch.frequency
        start = n.offset
        dur = n.duration.quarterLength * 0.5
        s_samp = int(start * sr * 0.5)
        e_samp = int((start + dur) * sr * 0.5)
        if e_samp > len(audio):
            e_samp = len(audio)
        if s_samp < len(audio):
            env = np.linspace(1, 0, e_samp - s_samp)
            audio[s_samp:e_samp] += 0.3 * np.sin(2 * np.pi * freq * t[s_samp:e_samp]) * env

audio = np.divide(audio, np.max(np.abs(audio)), out=np.zeros_like(audio), where=np.max(np.abs(audio)) > 0) * 0.9
wavfile.write(f"{project_dir}/Audio/loop.wav", sr, audio.astype(np.float32))

export_musicxml(matrix, f"{project_dir}/Scores/loop.xml")
generate_dashboard(matrix, f"{project_dir}/index.html")

print("✅ Generated")
print(f"   MIDI: {project_dir}/MIDI/loop.mid")
print(f"   Audio: {project_dir}/Audio/loop.wav")