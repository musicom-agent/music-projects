
import itertools

class PitchPattern:
    def __init__(self, intervals):
        self.intervals = list(intervals)
    
    def retrograde(self):
        return PitchPattern(self.intervals[::-1])
    
    def invert(self):
        return PitchPattern([-i for i in self.intervals])
    
    def rotate(self, n):
        n = n % len(self.intervals)
        return PitchPattern(self.intervals[n:] + self.intervals[:n])

    def __repr__(self):
        return f"PitchPattern({self.intervals})"
