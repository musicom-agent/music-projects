
class MelodicPhrase:
    def __init__(self, pitch_pattern, rhythm_pattern):
        self.pitch_pattern = pitch_pattern
        self.rhythm_pattern = rhythm_pattern

    def render_to_midi_sequence(self, root_note, scale):
        """
        Combines Pitch DNA and Rhythm DNA
        Returns list of (midi_note, duration_steps)
        """
        sequence = []
        p_idx = 0
        p_ints = self.pitch_pattern.intervals
        
        for step in self.rhythm_pattern.onsets:
            if step == 1:
                interval = p_ints[p_idx % len(p_ints)]
                # Map interval to scale tone relative to root_note
                # (Conceptual mapping)
                note = root_note + interval 
                sequence.append((note, 1)) # 1 beat duration
                p_idx += 1
            else:
                sequence.append((0, 1)) # Rest
        return sequence
