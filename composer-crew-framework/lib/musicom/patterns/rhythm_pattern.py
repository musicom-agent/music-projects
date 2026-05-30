
class RhythmPattern:
    def __init__(self, onsets, total_steps=16):
        """
        onsets: List of binary steps [1, 0, 1, 0...] or indices
        """
        self.onsets = list(onsets)
        self.total_steps = total_steps

    @classmethod
    def euclidean(cls, k, n):
        """Generates a Euclidean rhythm E(k, n)"""
        pattern = []
        counts = [1] * k + [0] * (n - k)
        # Simplified Euclidean distribution
        for i in range(n):
            pattern.append(counts[(i * k) % n])
        return cls(pattern, n)

    def augment(self, factor=2):
        """Slows down the rhythm by inserting gaps"""
        new_onsets = []
        for val in self.onsets:
            new_onsets.append(val)
            new_onsets.extend([0] * (factor - 1))
        return RhythmPattern(new_onsets, self.total_steps * factor)

    def __repr__(self):
        return f"RhythmPattern({self.onsets})"
