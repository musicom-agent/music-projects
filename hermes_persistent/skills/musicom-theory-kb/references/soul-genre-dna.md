# Soul Genre Patterns (Musicom)

## PC Set & Scale
- **Pillar**: Minor Pentatonic + Blue Note (b5).
- **Scale Degrees**: 1, b3, 4, b5, 5, b7.
- **Musicom PC_Set**: `[0, 3, 5, 6, 7, 10]`.

## PatternMovementRules
### Gospel Pillar (Plagal)
Focus on the stable IV-I relationship.
- `I`: [`IV`, `vi`, `ii`]
- `IV`: [`I`, `V`]
- `V`: [`I`, `IV`]

### Blues Delta (Dominant)
Focus on cyclic Dominant 7th tension.
- `I7`: [`IV7`]
- `IV7`: [`I7`, `V7`]
- `V7`: [`IV7`, `I7`]

## UnitMatrix Architecture
Standard 4x4 or 4x8 Soul block:
- **Lead**: Row 0 - Melismatic Lead (PatternType.BLUES, high event density).
- **Brass**: Row 1 - Horn Stabs (PatternType.DOM7, rhythmic accents).
- **Bass**: Row 2 - Syncopated Bass (Euclidean E(3,8) or root-fifth walks).
- **Rhythm**: Row 3 - Backbeat Drums (Snare on 2 and 4).
