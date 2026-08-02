---
name: genre-composition-patterns
description: "Genre-specific composition density requirements and algorithmic method hybridization patterns. Use when composing in a specific style (disco, blues, jazz, etc.) to ensure appropriate texture density and avoid sparse/staccato results."
version: 1.0.0
author: Axel Wiertz
license: MIT
platforms: [linux]
prerequisites:
  env_vars: []
  commands: [/opt/data/micromamba/envs/musicom/bin/python]
dependencies: []
metadata:
  hermes:
    tags: [music, composition, genre, density, methods, hybridization]
    related_skills: [musicom-method-master-map, compose-loop, musicom-theory-kb]
triggers:
  - disco composition
  - blues composition
  - genre-specific
  - sparse composition
  - staccato
  - continuous flow
  - method hybridization
---

# Genre-Specific Composition Patterns

Genre-specific density requirements and algorithmic method hybridization for the musicom engine.

## Critical: Genre Density Requirements

Different genres require different minimum density thresholds to avoid sparse/staccato textures:

| Genre | Min Density (Harmonic Voices) | Continuous Layer Required |
|-------|-------------------------------|---------------------------|
| **Disco** | 100% (strings/pads/arps) | Yes — arpeggios or sustained pads |
| **Blues** | 75% (rhythm section) | Optional — shuffle feel provides motion |
| **Jazz** | 85% (comping instruments) | Optional — swing feel provides motion |
| **Ambient** | 95% (all voices) | Yes — drones/pads essential |
| **Minimal** | 40-60% (intentional sparse) | No — silence is structural |

### Pitfall: Sparse Rhythmic Patterns in Dance Genres

**Problem**: Using only sparse rhythmic patterns (e.g., Euclidean E(5,16) = 31% density) for harmonic voices creates staccato, disconnected texture in dance genres.

**Solution**: Layer continuous-flow methods on top of sparse rhythmic foundations:
- **Disco**: Euclidean drums (75%) + DPSM arpeggios (100%) + sustained pad (100%)
- **House**: Four-on-the-floor (100%) + filtered arpeggios (100%) + sidechained pads (100%)
- **Techno**: Sparse percussion (60%) + continuous drones (100%) + filtered noise (100%)

## Method Hybridization Patterns

### Pattern 1: Euclidean + DPSM (Disco/House)

**Use when**: Need rhythmic precision + continuous harmonic flow

**Structure**:
1. **Euclidean foundation** (Method 011): Sparse rhythmic patterns for drums/bass
   - Kick: E(4,16) or E(5,16)
   - Hi-hat: E(7,16) or E(9,16)
   - Snare: E(3,8) rotated for backbeat
2. **DPSM continuous layer** (Method 026): Phase-shifted arpeggios
   - 3 layers offset by 1/3 beat each
   - Continuous 8th or 16th notes
   - Cycle through chord tones
3. **Sustained pad**: Full-voiced chords, 2-bar durations

**Example** (Disco):
```python
# Layer 1: Euclidean drums (75% density)
drum_unit = build_euclidean_drums(...)  # E(4,16) kick, E(7,16) hat

# Layer 2: DPSM arpeggios (100% density)
arp_unit = build_dpsm_arpeggios(...)    # 3 phases × continuous 8th notes

# Layer 3: Sustained strings (100% density)
pad_unit = build_string_pad(...)        # Full chords, 2-bar sustain
```

### Pattern 2: Markov + Tendency Masking (Jazz/Blues)

**Use when**: Need probabilistic melody within bounded range

**Structure**:
1. **Tendency Masking** (Method 023): Define pitch corridor L(t) to U(t)
2. **Markov transitions** (Method 002): Generate melodic paths within corridor
3. **Walking bass**: Continuous 8th-note arpeggiation (100% density)

### Pattern 3: Xenakis Sieve + Isorhythmic Talea-Color (Contemporary)

**Use when**: Need complex polyrhythmic structures

**Structure**:
1. **Xenakis Sieve** (Method 025): Generate pitch sets via modular congruence
2. **Isorhythmic Talea-Color** (Method 032): Decouple rhythm (talea) from pitch (color)
3. **Continuous drone**: Sustained bass note or fifth (100% density)

## Genre-Specific Patterns

### Disco (1977-86)

**Essential elements**:
- Four-on-the-floor kick (100% or Euclidean E(4,16))
- Syncopated bass (Euclidean E(5,16) + walking fills)
- Continuous harmonic layer (DPSM arpeggios OR sustained strings)
- Brass/string stabs on offbeats (Euclidean E(3,8))

**Density targets**:
- Drums: 75-100%
- Bass: 100% (with fills)
- Harmonic voices: 100% (arps or pads)
- Accent voices (brass): 12-50% (intentional sparse)

**Key signatures**: D minor, E minor, A minor, C major

**Tempo**: 118-126 BPM

### Blues (12-bar, 32-bar)

**Essential elements**:
- Shuffle rhythm (2:1 long-short eighth notes)
- Walking bass (continuous 8th notes, 100% density)
- Block chords or shuffle comping
- Blue-note slides (b3 → 3 grace notes)

**Density targets**:
- Drums: 100% (shuffle pattern)
- Bass: 100% (walking)
- Chords: 75-100%
- Lead: 75-95% (expressive, not continuous)

**Key signatures**: C blues, E blues, A blues

**Tempo**: 80-120 BPM (shuffle feel)

## Implementation Checklist

When composing in a specific genre:

1. **Check density requirements** — does the genre need continuous flow?
2. **Select method hybridization** — which methods combine for this genre?
3. **Build sparse foundation** — Euclidean/Markov for rhythmic structure
4. **Add continuous layer** — DPSM/sustained pads for flow
5. **Validate density** — check grid visualization, ensure harmonic voices ≥ genre minimum
6. **Render and verify** — listen for staccato gaps, add fills if needed

## Arrangement Techniques

### Progressive Instrument Dropout (Outro)

**Use when**: Need gradual ending instead of fade-out or abrupt stop

**Pattern**: Silence instruments one by one over final section (typically 4 bars):

**Dropout order** (front to back):
1. **Countermelody/Lead**: Drops first (bar 1-2)
2. **Drums**: Drop after bar 2
3. **Bass**: Drop after bar 2-3
4. **Strings/Pad**: Drop after bar 2-3
5. **Piano/Primary**: Plays all bars, often with ritardando

**Implementation**:
```python
def build_outro_with_dropout(section_name, bar_idx):
    if section_name == 'Outro':
        # Lead: bars 0-1 only
        if bar_idx < 2:
            build_lead_pattern(...)
        
        # Drums: bars 0-2 only
        if bar_idx < 3:
            build_drum_pattern(...)
        
        # Bass: bars 0-2 only
        if bar_idx < 3:
            build_bass_pattern(...)
        
        # Piano: all 4 bars with ritardando
        dur = BAR + bar_idx * 200  # Gradually longer
        build_piano_pattern(dur=dur)
```

**Effect**: Creates organic decay, each layer exits at musically logical point.

### Section-Specific Articulation Variation

**Use when**: Need textural contrast between sections without changing harmony

**Pattern**: Vary articulation per section for same instrument:

**Strings example**:
- **Intro**: Fade in, sustained (bars 2-3 only)
- **Verse A**: Sustained pad (whole notes)
- **Verse B**: Staccato chords (quarter notes)
- **Chorus A**: Sustained + tremolo (eighth notes, volume modulation)
- **Chorus B**: Staccato chords
- **Outro**: Sustained, then dropout

**Implementation**:
```python
def build_strings(chord_name, section_name):
    if section_name in ['V1a', 'V2a']:
        # Sustained pad
        for bar in range(4):
            for p in chord_notes:
                events.append(sustained_note(p, dur=BAR))
    
    elif section_name in ['V1b', 'V2b', 'ChB']:
        # Staccato chords
        for bar in range(4):
            for beat in range(4):
                for p in chord_notes:
                    events.append(staccato_note(p, dur=QUARTER//2))
    
    elif section_name == 'ChA':
        # Tremolo effect
        for bar in range(4):
            for eighth in range(8):
                vol = base_vol + (10 if eighth%2==0 else -10)
                events.append(note(vol=vol, dur=EIGHTH))
```

**Effect**: Maintains harmonic continuity while creating dynamic contrast.

## Pitfalls

- **Sparse Euclidean alone**: Creates staccato feel in dance genres. Always add continuous layer.
- **Over-dense minimal**: Minimalist genres need intentional sparse texture (40-60%).
- **Wrong tempo range**: Disco at 100 BPM sounds like ballad. Check genre tempo bounds.
- **Missing continuous layer**: If grid shows <80% density on harmonic voices in disco/house, add DPSM arpeggios or sustained pads.
- **Uniform articulation**: Same articulation across all sections = monotonous. Vary per section (sustained vs staccato vs tremolo).
- **Fade-out outro**: Lazy ending. Use progressive dropout for organic decay.

## References

- `references/disco-density-analysis.md` — Density comparison across disco versions (v1 vs v2 vs v3)
- `references/method-hybridization-examples.md` — Code examples for Euclidean+DPSM, Markov+Tendency Masking
- `references/classical-crossover-arrangement.md` — Classical crossover arrangement: chord voicings, progressive dropout, strings articulation map, harmony analysis
