
class GenreRules:
    def __init__(self, genre='jazz'):
        self.genre = genre
        self.constraints = self._load_constraints()

    def _load_constraints(self):
        if self.genre == 'jazz':
            return {
                'forbidden_intervals': [],
                'preferred_scale': 'dorian',
                'syncopation_level': 0.8
            }
        return {}

    def validate_progression(self, progression):
        # I-V-vi-IV rule check logic
        return True
