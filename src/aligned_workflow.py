import mido
from mido import Message, MidiFile, MidiTrack

def produce_expanded_composition():
    # 480 ticks per beat (TPB)
    mid = MidiFile(ticks_per_beat=480)
    
    # Tracks
    track_melody = MidiTrack()
    track_harmony = MidiTrack()
    track_rhythm = MidiTrack()
    track_drone = MidiTrack()
    mid.tracks.extend([track_melody, track_harmony, track_rhythm, track_drone])

    def add_note(track, pitch, duration, time=0, vel=70, channel=0):
        track.append(Message('note_on', note=pitch, velocity=vel, time=time, channel=channel))
        track.append(Message('note_off', note=pitch, velocity=0, time=duration, channel=channel))

    # SCALE: D Mixolydian/Minor Hybrid for Bollywood feel
    # D(1), E(2), F(b3), F#(3), G(4), A(5), Bb(b6), C(b7)
    
    # --- SECTION 1: BOLLO (4 BARS) ---
    # Harmony: I - IV (Dm - Gm)
    # Pattern: 4/4 Steady Quarter
    bollo_melody = [62, 64, 65, 62, 62, 64, 65, 67, 69, 67, 65, 64, 62, 62, 62, 62] # D E F D | D E F G | A G F E | D D D D
    bollo_chords = [(62, 65, 69), (67, 70, 74)] # Dm, Gm
    
    for i, p in enumerate(bollo_melody):
        add_note(track_melody, p, 480)
        # Harmony on each bar (every 4 beats)
        if i % 4 == 0:
            chord = bollo_chords[(i // 8) % 2]
            for cp in chord: add_note(track_harmony, cp-12, 1920, time=0)
            track_harmony[-1].time = 1920

    # --- SECTION 2: KOOS (4 BARS) ---
    # Harmony: VII - I (C - Dm)
    # Pattern: Jumpy / Syncopated
    koos_melody = [60, 67, 64, 60, 64, 65, 67, 67, 60, 67, 64, 60, 55, 60, 62, 62]
    koos_chords = [(60, 64, 67), (62, 65, 69)] # C, Dm
    
    for i, p in enumerate(koos_melody):
        add_note(track_melody, p, 480)
        if i % 4 == 0:
            chord = koos_chords[(i // 8) % 2]
            for cp in chord: add_note(track_harmony, cp-12, 1920, time=0)
            track_harmony[-1].time = 1920

    # --- SECTION 3: INDIAN (4 BARS) ---
    # Harmony: bII - I (Eb - D)
    # Pattern: 8-beat Bollywood (█░██░█░░)
    indian_melody = [62, 63, 62, 66, 67, 66, 63, 62] * 2 
    indian_chords = [(63, 67, 70), (62, 66, 69)] # Eb, D (Major)
    
    for i, p in enumerate(indian_melody):
        add_note(track_melody, p, 240) # 8th notes to allow rapid ornaments
        if i % 4 == 0:
            chord = indian_chords[(i // 8) % 2]
            for cp in chord: add_note(track_harmony, cp-12, 960, time=0)
            track_harmony[-1].time = 960

    # --- SECTION 4: BLENDED (4 BARS) ---
    # Harmony: VI - V - I (Bb - A - D)
    # Pattern: Fusion Poly-rhythm
    blend_melody = [62, 63, 65, 66, 67, 69, 70, 72, 74, 73, 70, 69, 67, 66, 63, 62]
    blend_chords = [(58, 62, 65), (57, 61, 64), (62, 66, 69)] # Bb, A, D
    
    for i, p in enumerate(blend_melody):
        add_note(track_melody, p, 480)
        if i % 4 == 0:
            chord = blend_chords[min(i // 5, 2)]
            for cp in chord: add_note(track_harmony, cp-12, 1920, time=0)
            track_harmony[-1].time = 1920

    # --- RHYTHM & DRONE ---
    pattern = [1, 0, 1, 1, 0, 1, 0, 0] * 16
    for strike in pattern:
        if strike:
            add_note(track_rhythm, 42, 240, vel=80, channel=9)
        else:
            track_rhythm.append(Message('note_off', note=0, velocity=0, time=240, channel=9))

    track_drone.append(Message('note_on', note=38, velocity=30, time=0))
    track_drone.append(Message('note_off', note=38, velocity=0, time=30720))

    mid.save('../MIDI/composition_expanded.mid')

if __name__ == "__main__":
    produce_expanded_composition()
