import sys
from music21 import stream, note, chord, instrument, midi, tempo

def create_song_scaffold(project_path, bpm=110):
    """
    Standard scaffold for multitrack pop/country MIDI.
    Tracks: Vocal (Lead), Acoustic Guitar (Harmony), Electric Bass (Foundation).
    """
    score = stream.Score()
    score.insert(0, tempo.MetronomeMark(number=bpm))

    # Vocal
    v_part = stream.Part()
    v_part.insert(0, instrument.Vocalist() if hasattr(instrument, 'Vocalist') else instrument.Instrument())
    v_part.partName = "Lead Vocal"

    # Guitar
    g_part = stream.Part()
    g_part.insert(0, instrument.AcousticGuitar())
    g_part.partName = "Acoustic Guitar"

    # Bass
    b_part = stream.Part()
    b_part.insert(0, instrument.ElectricBass())
    b_part.partName = "Bass"

    score.insert(0, v_part)
    score.insert(0, g_part)
    score.insert(0, b_part)

    # Export
    mf = midi.translate.streamToMidiFile(score)
    with open(project_path, "wb") as f:
        f.write(mf.writestr())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        create_song_scaffold(sys.argv[1])
