import mido
from mido import Message, MidiFile, MidiTrack

def produce_aligned_composition():
    mid = MidiFile()
    track_melody = MidiTrack()
    track_rhythm = MidiTrack()
    track_drone = MidiTrack()
    mid.tracks.extend([track_melody, track_rhythm, track_drone])

    def add_note(track, pitch, duration, time=0, vel=70, channel=0):
        track.append(Message('note_on', note=pitch, velocity=vel, time=time, channel=channel))
        track.append(Message('note_off', note=pitch, velocity=0, time=duration, channel=channel))

    # Unit 1: Bollo (Dutch Folk) - D4 E4 F4 D4
    # Unit 2: Koos (Dutch Clubsong) - C4 G4 E4 C4
    # Unit 3: Indian (Popular/Classical) - D4 Eb4 D4 F#4
    # Unit 4: Blended (Fusion) - D4 Eb4 F4 F#4 (Melisma style)
    
    melody_units = [[62, 64, 65, 62], [60, 67, 64, 60], [62, 63, 62, 66], [62, 63, 65, 66]]
    
    for unit in melody_units:
        for p in unit:
            add_note(track_melody, p, 480)

    # 8-beat Bollywood Pattern (Metrical Gravity: █ ░ █ █ ░ █ ░ ░)
    rhythm_pattern = [1, 0, 1, 1, 0, 1, 0, 0] * 8
    for beat in rhythm_pattern:
        if beat:
            add_note(track_rhythm, 42, 240, vel=80) 
        else:
            track_rhythm.append(Message('note_off', note=0, velocity=0, time=240))

    # Drone on D2 (Tanpura style)
    for _ in range(8):
        add_note(track_drone, 38, 960, vel=35)

    mid.save('../MIDI/composition_aligned.mid')

if __name__ == "__main__":
    produce_aligned_composition()
