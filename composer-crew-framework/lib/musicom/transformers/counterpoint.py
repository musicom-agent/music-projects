
class CounterpointTransformer:
    @staticmethod
    def create_bass_phrase(lead_phrase, scale_transpose=-7):
        """
        Generates a complementary bass voice:
        1. Inverts the Lead Pitch DNA.
        2. Simplifies the Rhythm to a pulse foundation.
        3. Transposes down (default 1 octave).
        """
        from patterns.pitch_pattern import PitchPattern
        from patterns.rhythm_pattern import RhythmPattern
        from structures.melodic_phrase import MelodicPhrase
        
        # Invert the DNA
        bass_dna = lead_phrase.pitch_pattern.invert()
        
        # Grounded Rhythm: Just hits on 1 and 5 of an 8-step bar
        bass_rhythm = RhythmPattern([1, 0, 0, 0, 1, 0, 0, 0], total_steps=8)
        
        return MelodicPhrase(bass_dna, bass_rhythm)
