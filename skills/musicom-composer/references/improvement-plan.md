---
name: musicom-composer-improvement-plan
description: "Gap analysis and improvement roadmap for the musicom-composer skill"
---

# Musicom Composer — Improvement Plan

## Current State

The skill provides a **pattern-centric composition workflow** across three Musicom repos:
- **musicom**: Core data structures, generators, transformers, rules, analysis
- **musicom_ai**: High-level structures, AI generators, MIDI I/O
- **musicom_research**: Research examples, advanced patterns, quick reference

Plus a standalone numpy-only fallback (`live_test.py`) that generates a 20s ambient jazz piece with layering (pad, bass, chord, melody, harmonics), exports WAV + OGG (Opus for Telegram), no external deps beyond numpy.

## Critical Gaps

### 1. **PitchPattern and RhythmPattern classes don't exist**
The SKILL.md references `PitchPattern` and `RhythmPattern` as core compositional primitives (Steps 3-5), but there's no `class PitchPattern` anywhere in the referenced repos. The code snippets show **tuple-based intervals** `(2, 3, -2, -1, 2)` being passed around but never wrapped in a class with methods like `.retrograde()`, `.invert()`, `.rotate()`.

**Fix**: Create `patterns/pitch_pattern.py` and `patterns/rhythm_pattern.py` in the musicom repo with proper classes:
- `PitchPattern` with methods: `retrograde()`, `invert()`, `rotate()`, `apply_to_scale(scale, tonic)`, `contour_notation()`, `similar_to(other)` (contour comparison)
- `RhythmPattern` with methods: `augment(scale_factor)`, `diminish(scale_factor)`, `displace(ticks)`, `cross_rhythm(other)`, `onset_positions()`

### 2. **MelodicPhrase is underspecified**
Step 6 shows `MelodicPhrase = PitchPattern × RhythmPattern` but the code snippet in Step 6 uses raw `itertools.cycle` and manual `MusicEvent` construction. There's no `class MelodicPhrase` that encapsulates this combination logic.

**Fix**: Create `structures/melodic_phrase.py`:
```python
class MelodicPhrase:
    def __init__(self, pitch_pattern, rhythm_pattern, scale, tonic=0, start_octave=4)
    def build(self) -> MusicUnit  # combines pitch × rhythm into events
    def transpose(self, semitones) -> MelodicPhrase
    def variation(self, mutation_rate=0.2) -> MelodicPhrase
    def fit_to_chord_progression(self, chords) -> List[MelodicPhrase]
```

### 3. **No Phrase → Harmony relationship**
The workflow describes melody first, then harmony (Steps 5-6), but there's no mechanism to check if a melody's notes fit the chosen chord progression, or to extract suggested chords from an existing melody.

**Fix**: Add `generators/harmony_from_melody.py`:
- Extract implied harmony from a MelodicPhrase (chord tone analysis)
- Suggest chord progressions that support a given melody
- Voice-leading quality metrics

### 4. **live_test.py is too simplistic for a "composer" skill**
The fallback script generates one fixed 20s loop (C Major, 4-chord progression, static melody). It's a proof-of-concept but not useful for actual composition because:
- No variation (same melody repeats every 8 beats)
- No section structure (no intro/verse/chorus/bridge)
- No parameterization (can't choose genre, mood, key)
- No dynamic layering (all layers always active at same intensity)
- Uses only `sin()` waveforms — no timbral variety

**Fix**: Create `scripts/composer_fallback.py` (replacement for live_test.py):
```python
# Fully parameterized numpy-only composer
composer = FallbackComposer(
    genre='ambient_jazz', mood='calm', tonic=0, mode='aeolian',
    tempo=90, form='ABA', duration_seconds=60
)
composition = composer.compose(
    progressions=[['C', 'G', 'Am', 'F'], ['Am', 'F', 'C', 'G']],
    melody_variations=3,
    layer_mix={'pad': 0.06, 'bass': 0.2, 'chord': 0.12, 'melody': 0.2, 'harmonics': 0.04}
)
composition.export_wav('/tmp/output.mid')
composition.export_ogg('/tmp/output.ogg')
```

### 5. **Missing: AI Integration Layer**
The musicom_ai repo is mentioned but the skill never shows how AI generators integrate into the workflow. There should be a bridge between pattern-based composition and AI-assisted generation:

**Fix**: Add `ai_generator.py`:
```python
from musicom_ai.generators import LLMComposer, MusicGenExporter

# AI-assisted pattern generation
patterns = LLMComposer.generate_patterns(
    prompt="5-bar blues progression in Dorian mode, tension-building",
    max_patterns=3
)

# AI-assisted arrangement
arranged = LLMComposer.arrange(
    phrases=phrase_list,
    form='verse-chorus-verse-chorus-bridge-chorus',
    target_genre='neo-soul'
)
```

### 6. **Missing: MIDI/Audio Quality Pipeline**
Current MIDI export (`music21_score.py`) and AudioCraft audio generation are mentioned but disconnected. The pipeline should be:
```
Composition → MIDI export → DAW import → AudioCraft refinement → Final audio
```

**Fix**: Create `exporters/quality_pipeline.py`:
```python
pipeline = AudioExportPipeline()
pipeline.add_source(midi_path)
pipeline.add_layer('AudioCraft', prompt=CONCEPT['mood'], style=CONCEPT['genre'])
pipeline.add_layer('MIDI-to-audio', sfz_instrument='grand_piano')
pipeline.export_final('/tmp/composition_final.wav', format=['mp3', 'ogg', 'flac'])
```

### 7. **No Analysis or Feedback Loop**
After generating a composition, there's no way to:
- Check if the melody is too repetitive
- Analyze chord progression strength (novelty, predictability)
- Measure harmonic tension/release curve
- Compare against reference pieces

**Fix**: Add `analyzers/quality_metrics.py`:
```python
metrics = CompositionAnalyzer(composition)
print(metrics.intervals_used())        # pitch class distribution
print(metrics.chord_progressions())    # I-V-vi-IV analysis
print(metrics.rhythmic_complexity())   # onsets per bar, syncopation index
print(metrics.section_balance())       # ABA symmetry score
```

## High-Priority Additions

### 8. **Pattern Library**
Create a library of pre-defined, tested patterns that users can load and remix:
- `patterns/classic_openings.py`: Beethoven, Bach, Mozart motifs
- `patterns/blues.py`: Standard blues licks and turnaround patterns
- `patterns/jazz.py`: Coltrane changes, ii-V-I variations
- `patterns/electronic.py**: Techno, house, ambient rhythm templates

### 9. **Interactive REPL/CLI Tool**
A `musicom-compose` CLI that walks through the 10-step pipeline:
```bash
$ musicom-compose
> Genre? ambient
> Mood? mysterious
> Key? A minor
> Tempo? 72
> Form? ABA
> Melody type? stepwise with occasional leaps
> Rhythm? Euclidean 5/8
...
✓ Composition saved to /tmp/hermes/songs/ambient_mystery.mid
✓ Audio rendered to /tmp/hermes/songs/ambient_mystery.ogg
```

### 10. **Integration Tests**
The skill has `live_test.py` but no proper test suite. Add:
```
tests/
  test_pitch_patterns.py       # interval arithmetic, contour operations
  test_rhythm_patterns.py      # Euclidean distribution, scaling
  test_phrase_generation.py    # pitch × rhythm combination
  test_chord_progressions.py   # diatonic harmony, voice leading
  test_midi_export.py          # roundtrip MIDI → stream → MIDI
  test_audio_render.py         # numpy synthesis correctness
```

### 11. **Documentation Improvements**
- **Flowchart**: Add a visual pipeline diagram showing how data flows between repos
- **Error handling**: Document common failure modes (scale out of range, rhythm too sparse, etc.) and recovery
- **Examples directory**: Add `examples/` with complete compositions from concept to audio:
  - `examples/01_simple_melody.py` — 8-bar C major melody
  - `examples/02_jazz_standard.py` — ii-V-I turnaround with melody
  - `examples/03_ambient_drone.py` — texture-based composition
  - `examples/04_cross_genre.py` — blend classical + electronic

## Medium-Priority Improvements

### 12. **Real-time Preview**
Allow listening to compositions incrementally during the pipeline:
```python
from musicom.preview import LivePreview

preview = LivePreview(tempo=120)
for phrase in composition.phrases:
    preview.play(phrase)
    # user presses Enter to continue or space to stop
```

### 13. **Multi-Instrument Arrangement**
Step 9 mentions assigning instruments but only shows `MusicVoice`. Expand to:
```python
arranger = MultiInstrumentArranger(project)
arranger.assign('piano', range='C3-C7', velocity_curve='expressive')
arranger.assign('strings', range='G2-D6', articulation='legato')
arranger.assign('synth_lead', range='C4-C6', waveform='sawtooth')
arranger.add_countermelody(source_phrase, interval=5, voice='alto')
```

### 14. **Genre-Specific Rules**
Add genre-aware constraints:
```python
from musicom.rules import GenreRules

rules = GenreRules('jazz')
rules.enforce('no_parallel_fifths')
rules.enforce('chord_tones_on_strong_beats')
rules.allow('extensions_7th_plus')

rules = GenreRules('techno')
rules.enforce('4_on_floor_bass')
rules.allow('repetition_and_variation')
rules.allow('dissonance')
```

## Implementation Order

1. **Phase 1 (Pattern Classes)** — Fix the core abstraction gap. Without real `PitchPattern`/`RhythmPattern`/`MelodicPhrase` classes, the "pattern-centric" workflow is just comments and pseudocode.
2. **Phase 2 (Better Fallback)** — Replace `live_test.py` with a fully parameterized numpy composer so the skill works end-to-end even without music21/musicpy.
3. **Phase 3 (AI Bridge)** — Connect musicom_ai generators into the pipeline.
4. **Phase 4 (Quality & Analysis)** — Add feedback loops so compositions improve iteratively.
5. **Phase 5 (CLI & Examples)** — Polish for usability.
