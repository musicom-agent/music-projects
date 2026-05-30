---
name: musicom-theory-kb
description: "Knowledge base for the musicom music composition framework — theory concepts, pattern classes, chord progressions, generators, and transformations. Covers three repos: musicom (core), musicom_ai (generators), musicom_research (reference)."
tags: [music, theory, scales, progressions, patterns, composition, ai]
---

# Musicom — Combined Knowledge Base

## Three Repositories Merged

| Repo | Location | Focus | Status |
|---|---|---|---|
| **musicom** | `/root/musicom/` | Core framework — data structures, generators, transformers, rules, analysis | Production codebase |
| **musicom_ai** | `/root/musicom_ai/` | AI composition assistant — Tet system, structures, generators, harmony, melody, rhythm, MIDI I/O | Phase 1-2 complete |
| **musicom_research** | `/root/musicom_research/` | Research examples, quick reference, integration patterns | Examples & reference |
| **music-projects** | `gh:musicom-agent/music-projects` | Portfolio gallery — dashboards, MIDI, audio, analysis | Active Portfolio |

## Unified Architecture

```
MUSICOM KNOWLEDGE BASE
│
├── 1. 12TET SYSTEM (pitch, intervals, scales, keys, modes)
│     ├── musicom/structures/pitch.py — MusicPitchClass, MusicPitchGrid
│     ├── musicom_ai/core/tet_system.py — PitchClass, Interval, Scale, Key, TimeSignature
│     └── musicom/structures/pitchclass.py — PatternType, PatternDefinition, PatternRegistry
│
├── 2. PATTERN CONCEPTS (scales, chords, progressions as patterns)
│     ├── PatternType enum — all interval, triad, 7th, scale pattern types
│     ├── PatternRegistry — CHROMATIC > HEPTATONIC > PENTATONIC hierarchy
│     ├── MusicPitchClassSet — pitch classes with rotation/mode support
│     └── PatternMovement — common chord progressions
│
├── 3. MUSICAL STRUCTURES (data objects)
│     ├── musicom: MusicEvent → MusicUnit → MusicVoice → MusicSection → MusicProject → UnitMatrix
│     ├── musicom_ai: Note → Rest → Chord → Phrase → Progression → Voice → Score
│     └── musicom_research: Note, Chord, Scale, Sequence (simplified)
│
├── 4. HARMONY & RULES (chord movement, counterpoint, voice leading)
│     ├── Scale7PitchDegree — active/stable degrees, movement rules
│     ├── PatternMovementRules — scale degree next-chord rules
│     ├── Scale7ChordDegree — diatonic chord functions (tonic, dominant, subdominant)
│     ├── Counterpoint — parallel fifths/octaves detection
│     └── musicom_ai/rules/ — voice leading, harmonic rules (planned)
│
├── 5. GENERATORS (algorithmic composition)
│     ├── musicom: Pattern, MarkovChain, Genetic, Harmonics, Stochastic, ChordDegree, Rhythm
│     ├── musicom_ai: RandomWalk, ScaleBased, MarkovChain (melody), Progression, Voicing (harmony), RhythmicPattern (rhythm)
│     └── musicom_research: MelodyGenerator, ChordProgressionGenerator, RhythmGenerator, PatternGenerator
│
├── 6. TRANSFORMERS (modifications)
│     ├── musicom: Canon, Embellishment, Matrix, Pitch transformations, PitchSequence
│     ├── musicom_ai: pitch_transformers (planned)
│     └── musicom_research: Transposition, Time, Dynamics, Harmonic, Rhythmic, Pattern transformers
│
├── 7. RHYTHM & TIME
│     ├── musicom: MusicTimeGrid, MusicRhythmPattern, Euclidean rhythm
│     ├── musicom_ai: RhythmicPatternGenerator (Euclidean, swing, polyrhythms, clave)
│     └── musicom_research: TimeGrid, rhythm quantization
│
├── 8. I/O & FORMATS
│     ├── musicom: MIDI, MusicXML (via music21), MIDI instrument/percussion mappings
│     ├── musicom_ai: MIDIReader, MIDIWriter, PianoRoll (via PyPianoroll), MusicXML
│     └── musicom_research: MIDIHandler, MusicXMLHandler, PianoRollHandler
│
├── 9. ANALYSIS
│     ├── musicom: score_analyze (music21), piece_analyze (musicpy), key/chord detection, roman numeral
│     ├── musicom_ai: contour analysis, range, chord quality, harmonic function
│     └── musicom_research: rule-based validation (voice leading, harmonic, melodic)
│
└── 10. COMPOSITION WORKFLOWS (bridging approaches)
      ├── Pattern-first: scale → chord progression → melody → transform → export
      ├── Melody-first: generate melody → harmonize → rhythm → arrange → export
      ├── Rhythm-first: create pattern → generate pitches → chordalize → arrange → export
      ├── Matrix-first: UnitMatrix → fill cells → apply transforms → extract → export
      ├── Analysis-first: load MIDI → analyze → transform → regenerate → export
      └── Style-learning: train Markov on data → generate → refine → export

## 11. Modal Interchange & Chromatic Patterns
Modal interchange is the temporary substitution of a scale's native pitch classes with those from a parallel mode (same tonic).

### Best Practices for "Off-Scale" Patterns
1. **Chromatic Gravity (Directional Resolution)**: 
   * **Raised notes** (e.g., Lydian #4) should resolve **UP** (F# -> G).
   * **Lowered notes** (e.g., Aeolian b6) should resolve **DOWN** (Ab -> G).
2. **Law of Conservation of Identity**: Maintain at least one **Common Tone** (pivot bulb) between diatonic and borrowed chords to prevent jarring transitions.
3. **The "Brief Visit" Protocol**: Surround off-scale patterns with stable diatonic anchors (I or V) to maintain tonal center.
4. **Emotional Matrix**:
   * **Lydian (Raise 4th)**: Heroic, Wonder, Ethereal.
   * **Aeolian (Lower 6th/b6)**: Melancholy, Depth, Romanticism.
   * **Phrygian (Lower 2nd/b2)**: Mystery, Tension, Ancient.
   * **Mixolydian (Lower 7th/b7)**: Bluesy, Soul, Stable.

### Pitch Class Matrix Visualization
Treat the 12-TET space as a 12-row "Light Bulb Matrix". Interchange is the toggling of specific bulbs (e.g., Row 9 OFF, Row 8 ON) while maintaining the root (Row 0).
```

## Quick Reference

### Pitch Classes
```
C=0, C#=1, D=2, D#=3, E=4, F=5, F#=6, G=7, G#=8, A=9, A#=10, B=11
```

### MIDI Octaves
```
C4 = 60 (middle C), A4 = 69 (440Hz)
octave = (midi // 12) - 1
pitch_class = midi % 12
```

### 14 Scale Patterns
```
major:         [0,2,4,5,7,9,11]    (2,2,1,2,2,2,1)
natural_minor: [0,2,3,5,7,8,10]    (2,2,1,2,2,1,2)
harmonic_minor:[0,2,3,5,7,8,11]    (2,2,1,2,1,3,1)
melodic_minor: [0,2,3,5,7,9,11]    (2,2,1,2,2,1,2)
dorian:        [0,2,3,5,7,9,10]    (2,1,2,2,2,1,2)
phrygian:      [0,1,3,5,7,8,10]    (1,2,2,2,1,2,2)
lydian:        [0,2,4,6,7,9,11]    (2,2,2,1,2,2,1)
mixolydian:    [0,2,4,5,7,9,10]    (2,2,1,2,2,1,2)
locrian:       [0,1,3,5,6,8,10]    (1,2,2,1,2,2,2)
aeolian:       same as natural_minor
ionian:        same as major
pentatonic_major:  [0,2,4,7,9]      (2,2,3,2,3)
pentatonic_minor:  [0,3,5,7,10]     (3,2,2,3,2)
blues:         [0,3,5,6,7,10]       (3,2,1,1,3,2)
whole_tone:    [0,2,4,6,8,10]       (2,2,2,2,2,2)
chromatic:     [0,1,2,3,4,5,6,7,8,9,10,11]
```

### 20+ Chord Qualities
```
Triads:     major[0,4,7], minor[0,3,7], diminished[0,3,6], augmented[0,4,8], sus2[0,2,7], sus4[0,5,7]
7ths:       maj7[0,4,7,11], min7[0,3,7,10], dom7[0,4,7,10], dim7[0,3,6,9],
            half_dim7[0,3,6,10], min_maj7[0,3,7,11], aug7[0,4,8,10], maj6[0,4,7,9], min6[0,3,7,9]
Extended:   maj9, min9, dom9, maj11, min11, dom11, maj13, min13, dom13
```

### Diatonic Chords in Major Key
```
Degree  I    ii   iii   IV   V    vi   vii°
Qual.   Maj  min  min   Maj  Maj  min  dim
7th     Imaj7 ii7  iii7  IVmaj7 V7  vi7  viiø7
Function Tonic SubDom  Dom  Dom  Tonic  Dom
- **Circle of Fifths heatmap**: Use `songsee` or direct chroma plots to visualize harmonic distance from the tonic.
- **Instant Playback (OGG/Opus)**: Standardize audio delivery as OGG/Opus voice bubbles for internal review and Telegram compatibility.
- **Reference Files**:
  - `references/modal-interchange-mechanics.md`: High-level explanation of the logic-mechanical split in chromatic harmony.
  - `references/timbre-synthesis-logic.md`: Directives for instrument modeling (Piano, Violin, Guitar).

## Project Dashboards & Visualization
Always provide a visual and auditory "Workbench" for compositions:
1. **Piano Roll**: High-contrast pitch/time grid.
2. **Volume Graph**: Dynamic intensity envelope using rose color fills.
3. **Chroma/Contour**: Tonal saturation and melodic interval shape.
4. **Instant Playback**: Synthesize to OGG and send as a Telegram voice bubble.


### Modal Interchange & Chromatic Voice Leading
- **The "Light Bulb" Matrix**: Visualize 12-TET as a grid of 12 bulbs. Modal interchange is the toggling of these bulbs (e.g., swapping bulb 9/A for bulb 8/Ab).
- **Darkening vs. Brightening**:
    - *Darkening*: Lowering pitch classes (borrowing from parallel Aeolian/Minor).
    - *Brightening*: Raising pitch classes (borrowing from parallel Lydian).
- **Chromatic Voice Leading**: The mechanical movement (e.g., A -> Ab) made possible by the "permission" of the modal pattern substitution.
- **Visualization Rule**: Use High-Contrast Piano Rolls where "Borrowed" or "Interchanged" notes are highlighted in a contrasting accent color (e.g., Rose `#fb7185` against Cyan `#22d3ee`).

### Dashboard Implementation
- **Piano Roll (Light Bulb Matrix)**: Y-axis = 12-TET Pitch Classes (labeled C through B), X-axis = Time/Chords. Highlight the "interchange bits" to show the delta between the base scale and the borrowed chord.
- **Verification**: Always cross-reference the visual "Rose Bulb" with the synthesized frequency to ensure the "picture matches the sound."


### Cadences
```
Perfect: 5→1  (V→I)
Plagal:  4→1  (IV→I)
Imperfect: any→5
Interrupted: 5→4 or 5→6
```

- **Modal Interchange vs. Chromatic Voice Leading**:
  - **Modal Interchange** is the *Structural Justification* (the logical "permission" to use non-diatonic pitch classes). 
  - **Chromatic Voice Leading** is the *Mechanical Fulfillment* (the physical movement between pitch classes, e.g., $9 \to 8 \to 7$ or $A \to Ab \to G$).
  - **Distance**: Measured as Hamming/Manhattan distance on the 12-TET grid. A "borrowed" chord often has a distance of only 1 semitone from its diatonic counterpart.
- **Visual Synthesis Standards**:
  - Piano Roll: `#58C4DD` (Cyan) for notes.
  - Volume/Dynamics: `#fb7185` (Rose) alpha-filled graphs.
  - Pitch Class Bulbs: Visualize active pitch classes as a 0-11 bitmask or "lit bulbs" to show the geometric shift during interchange.

### Composition Analysis & Visualization Pipeline
When composing with patterns, always provide visual and auditory feedback to the user via a **GitHub Dashboard**:
1. **Piano Roll**: Use `music21` + `matplotlib` to plot pitch vs. time. Use a dark theme (facecolor: `#1e1e1e`, bars: `#58C4DD`).
2. **Volume Graph**: Plot note velocity/volume over time to show the "envelope" of the piece. Path usually `/tmp/musicom_report/volume_graph.png`. Use rose color `#fb7185`.
3. **Project Index**: Maintain a master `index.html` at the repository root linking to project-specific dashboards at `projects/[id]-[name]/index.html`.
4. **External Sync**: Each dashboard should include a direct BandLab URL linking to the project: `https://www.bandlab.com/musicom/[project-name]`.
5. **Instant Playback**:
   - Convert MIDI to WAV (synthesis fallback: `pure_tone_gen.py`).
   - Convert WAV to OGG (Opus) via `ffmpeg -codec:a libopus -b:a 48k`.
   - Send to Telegram with `MEDIA:/path/to/file.ogg` as a voice bubble.
### Composition Dashboard & Analysis
- **Piano Roll**: High-contrast dark theme (`#020617` bg, `#22d3ee` bars). Use `music21` to extract notes/chords and `matplotlib` for the grid.
- **Volume/Dynamics**: Plot note velocity over time using a rose-colored (`#fb7185`) filled area graph to show intensity flow.
- **Advanced Analysis**:
  - **Chroma Profile**: Histogram of pitch classes (0-11) to visualize scale/mode saturation.
  - **Melodic Contour**: Plot of intervallic jumps (semitones) between melodic notes to see the "shape" of the motif.
- **Dashboard Deployment**: Projects should be organized as `projects/[id]-[name]/` in the `music-projects` repository, each with a self-contained `index.html` dashboard linking to MIDI, OGG, and local analysis pngs.
- **BandLab Sync**: Add absolute BandLab track/project URLs to the dashboard for DAW collaboration.

### Notion Collaboration
- **Authentication**: Use `NOTION_API_KEY` (starts with `ntn_`).
- **Permissions**: Internal integrations cannot create top-level workspace pages. The user must manually create a "Parent" page and "Add Connection" to the agent before the agent can create sub-pages/databases.

## Practical Audio Generation

When `music21`, `musicpy`, `soundfile`, and other audio libraries are **not available** in the sandbox, you can still generate and play audio using only **numpy** + **ffplay**:

### Step-by-step recipe

1. **Synthesize audio with numpy** — use `np.sin()` for tone generation, `np.linspace()` for ADSR envelopes, `np.int16` for 16-bit PCM conversion
2. **Write a WAV file** with the built-in `wave` module (no dependencies needed)
3. **Play the file** via `ffplay -nodisp -autoexit <path>` or `ffmpeg -hide_banner -loglevel error -i <path> -f null -`

### Key details

- **Note frequency:** `f = 440.0 * (2.0 ** ((midi - 69) / 12.0))`
- **WAV header:** 16-bit, mono, set via `wave.setsampwidth(2)`, `wave.setnchannels(1)`
- **Envelope:** add attack (5ms) and release (20ms) with `np.linspace` to avoid clicking at note boundaries
- **Note gap:** insert 30ms rest between quarter notes by reducing `note_duration_samples = int(beat_duration * sample_rate) - gap_samples`
- **Clamp before int16:** `np.clip(samples, -1.0, 1.0)` then `(samples * 32767).astype(np.int16)`
- **Sandbox paths:** write to `/tmp/hermes/songs/` (create dir with `os.makedirs`)

### Visualization Dashboard Implementation
When presenting "composition shapes" or overviews, the user prefers a professional, standalone **GitHub Dashboard** (HTML/CSS) over raw text or individual images.
- **Visual Style**: Dark-themed (`#020617`), JetBrains Mono font, glowing accent indicators (cyan/rose).
- **Dashboard Components**:
    - **Piano Roll**: Pitch (midi number) vs. Time (quarter length) using `#58C4DD`.
    - **Volume/Dynamics Graph**: Velocity plotting with alpha-filled envelopes using `#fb7185`.
    - **Harmonic Flow**: Textual sequence of chords (e.g., `i7 -> IV7 -> i7`).
    - **Asset Linking**: Direct links to `.mid` and `.ogg` files in the repository.
    - **Vibrato Calibration**: User found >2% depth "unnatural". Preferred baseline: **5.5Hz at 0.8% depth**.

### Instant Playback & Synthesis Workflow
1. **Mathematical Representation**: Treat all musical elements as **Subsets** (Pitch Class Subsets or Time Grid Subsets).
2. **Low-Level Synthesis**: (See `references/timbre-synthesis-logic.md`)
   - **Piano**: Additive synthesis (fundamental + harmonics 2, 3) with aggressive exponential decay.
   - **Guitar (Karplus-Strong)**: Circular buffer of white noise averaged with a decay factor (e.g., `0.996`).
   - **Violin**: Sawtooth harmonic summation with **subtle vibrate** (5.5Hz, 0.8% depth) and bowing envelopes.
3. **Format Conversion**: Convert `.wav` -> `.ogg` (Opus) via `ffmpeg` with `-application voip -b:a 48k`.
4. **Delivery**: Use `MEDIA:/path/to/file.ogg` (use absolute paths to avoid "Media not found").
5. **Euclidean Rhythms**: Use the Euclidean algorithm to distribute pulses evenly across steps for grooves (e.g., Tresillo 3,8).
5. **Portfolio Integration**: Standardize the `music-projects` repo with `projects/[id]-[name]/` subfolders. Each project requires:
   - A dedicated `index.html` dashboard using the Musicom Dark-Kawaii theme.
   - Analysis assets: Piano Roll (`piano_roll.png`) and Volume Graph (`volume_graph.png`).
   - Metadata: Composer credited as "Musicom" with a BandLab link (`https://www.bandlab.com/musicom/[slug]`).

- **Instrument-Specific Modeling**:
  - **Piano**: Fundamental + harmonics $[1, 2, 3]$ with rapid exponential decay ($e^{-4t}$).
  - **Guitar**: Karplus-Strong algorithm using filtered noise loops; decay factor $\approx 0.996$ for natural string sustain.
  - **Violin**: Sawtooth harmonic summation ($1/n^{1.1}$) with subtle vibrato ($5.5\text{Hz}$ at $0.8\%$ depth) and slow attack ($250\text{ms}$) for bowing simulation.
- **Git Operations**: Ensure `user.name` is "Musicom Agent" and `user.email` is "musicom@wiertz.tech". Avoid committing as host users (e.g., Rafa-Ross).
- **Environment Management**: Clone secondary/framework repositories into local user projects (`~/musicom_framework/`) rather than `/root/` to maintain consistent permissions and access for the agent across tool calls.
- **Composer Workflow Framework**: Follow the 5-phase framework (Seed -> Pillars -> Synthesis -> Dashboard -> Handoff). See `references/composer-workflow-v1.md`.
- **Project Structure**: Centralize compositions in `projects/[id]-[name]/` (e.g., `010-project-dorian`). Each project requires an `index.html` dashboard, `.wav` master, and `.ogg` voice bubble.
- **Instrument modeling**:
    - *Guitar*: Ring buffer noise (pluck) + averaging filter (decay).
    - *Piano*: Additive harmonics (1.0, 0.4, 0.2) + exponential decay ($e^{-1.5t}$).
    - *Violin*: 10-12 harmonics (sawtooth $1/n^{1.1}$) + FM Vibrato (5.5Hz, 0.8% depth) + slow bowing attack (250ms).
- **Rhythm Generation**: Use Euclidean algorithms (e.g., `(pulses * i) % steps < pulses`) for grooves like Tresillo (3,8).
- **Ensemble Mixing**: Combine monophonic lead (violin), polyphonic chords (piano), and rhythmic bass (guitar) with gain scaling (roughly 0.3/0.3/0.4).
- **GitHub Projects**: Distinguish between "Handovers" (session state) and "Projects" (creative output). Publish creative work to `music-projects` and link visualizations to GitHub Pages.

- **Project Management**: Organize assets into `projects/[id]-[name]/`. Create a Master Index (index.html) in root.
- **Notion Integration**: Sync project status, Genre, Key, and BandLab/Dashboard links to 'Musicom Project Master'.
- **Email Workflow**: Use `himalaya` to download MIDI attachments to `/tmp/`, analyze, and update project folders.
- **Pattern Exploration**: Treat systematic theory exercises as 'Pillar' explorations (Scale/Chord subsets, Rhythm grids).
- **Templates**: See `templates/dashboards.md` for dark-themed visualization logic and HTML structures.

### Pitfalls
- **Dummy Files**: Musicom repos often use "Dummy MIDI" placeholders. Always verify MIDI headers before processing.
- **WAV Delivery**: Telegram does not render WAV files as playable bubbles; OGG is mandatory.
- **Auth Persistence**: GitHub PATs and SSH keys are often stored in past session context; search `session_search` if local `.env` is missing them.
- **Library Access**: If `pip install` is blocked by PEP 668, use `--break-system-packages` for quick terminal tasks or a venv for persistent work.

### Telegram Audio Sending (Voice Bubbles)

When sending audio to Telegram, **WAV files do not render as voice bubbles** — they must be converted to **OGG (Opus)** first.

### Email & Attachment Workflow (Himalaya)
- **Active Monitoring**: Regularly check the `musicom@wiertz.tech` inbox for new MIDI attachments.
- **Attachment Download**: Use `himalaya attachment download <ID>` to retrieve MIDI files.
- **Project Updates**: Upon receiving verified MIDI files via email, automatically update the corresponding `projects/` directory, regenerate all visualizations (Piano Roll/Volume), and refresh the project dashboard.

In Docker sandboxes with no `web_search` tool, no Chrome, and no pip, use DuckDuckGo Lite via `curl` + Python's `html.parser`. The parser extracts results from `<span class='link-text'>` (URLs) and `<a class='result-link'>` (titles). Key pattern:

```
1. Fetch: curl -s https://lite.duckduckgo.com/lite/ -d 'q=QUERY' -H 'User-Agent: Mozilla/5.0'
2. Parse with Python html.parser — look for span.link-text (URL) + a.result-link (title) + td.result-snippet
3. BeautifulSoup is ideal but not available; Python's built-in HTMLParser works fine
4. Write raw HTML to /tmp/ first for debugging, then parse
5. Results may have empty titles — URL slug is a fallback title
```

See `references/ai-composition-tools-2025.md` for the full research summary found this way.

### Instant Playback & Synthesis Workflow
- **Multi-instrument Ensemble**: Balance volumes when mixing (e.g., Piano 0.3, Guitar 0.4, Violin 0.3).
- **Subtle Vibrato**: For natural violin sounds, use ~5.5Hz vibrato with <1% depth. High vibrato (>2%) sounds "unnatural" or "synthetic" to the user.
- **Instrument Envelopes**: Piano/Guitar use fast exponential decay; Violin requires a "bowing" attack (~200ms) and release (~300ms).
- **Harmonic Profiles**: Violin (Sawtooth 1/n), Piano (Discrete additive 1, 0.5, 0.2), Guitar (Karplus-Strong Noise).

### Instant Playback & Synthesis Workflow
1. **Mathematical Representation**: Treat all musical elements as **Subsets** (Pitch Class Subsets or Time Grid Subsets).
2. **Low-Level Synthesis**: Use the specialized engines developed in Pillar 2:
   - **Piano**: Additive synthesis with fast decay.
   - **Guitar**: Karplus-Strong string modeling (filtered noise).
   - **Violin**: Sawtooth summation with FM vibrato (5.5Hz).
3. **Format Conversion**: Convert `.wav` -> `.ogg` (Opus) via `ffmpeg` with `-application voip -b:a 48k`.
4. **Delivery**: Use `MEDIA:/path/to/file.ogg` to deliver "voice bubbles" for instant user playback.
5. **Absolute Paths**: Always use absolute paths (e.g., `/opt/data/projects/...`) to avoid "Media not found" errors in Telegram blocks.
6. **Euclidean Rhythms**: Use the Euclidean algorithm to distribute pulses evenly across steps for grooves (e.g., Tresillo 3,8).

### Pillar 2: Low-Level Synthesis
- **Scripts**: See `scripts/pillar2_synthesis_engines.py` for standalone implementations of Guitar, Piano, and Violin.
- **Ensemble Setup**: Use `scripts/ensemble_synthesis.py` for mixing multiple synthesis sources.
- **Flat.io / MuseScore Integration**:
    - Use MusicXML as the bridge format. 
    - The `musicom.converters.music21_score` module in the core repository handles the `unit_to_stream` conversion.
    - **Note**: Ensure `PYTHONPATH` includes `/root/musicom` or relevant paths in `/opt/data/`.

### Composition Dashboarding (Project Hub)
For multi-session cooperation, maintain a centralized GitHub Pages dashboard:
1. **Project Index**: A root `index.html` linking to individual project folders.
2. **Project Workspace**: Each project in `projects/[id]-[name]/` containing its own `index.html` dashboard.
3. **Dashboard Standards**:
   - **Theme**: Dark, high-contrast (Slate-950 background, Cyan/Rose accents).
   - **Branding**: Credit "Musicom" as the composer; project name as title.
   - **Components**: Analytical Overview (Status/Mode/Meter), Advanced Analysis (Chroma Profile/Melodic Contour), Primary Visuals (Piano Roll/Volume Graph), and BandLab link.
4. **Pattern Exploration (Non-Compositional)**:
   - For theoretical exercises (Project 003+), organize by **Pillar 1 (Pitch)**: Catalog scales/modes/chords, and **Pillar 2 (Rhythm)**: Catalog meters/grooves/polyrhythms.

### External Platform Integration
- **Notion Hub**: Use a "Musicom Central Hub" parent page linked to the `Musicom Agent` integration.
- **Master Database**: Properties for Status, Genre, Key, Dashboard URL, and BandLab URL.
- **To-Do Sync**: Actively use the "To Do List DB" to track and update collaborative task status.
- **BandLab**: Always include direct track or revision URLs (e.g., `www.bandlab.com/axelwiertz/...`) in dashboards and Notion.

- **Project Management**: Organize assets into `projects/[id]-[name]/`. Create a Master Index (index.html) in root.
- **Notion Integration**: Sync project status, Genre, Key, and BandLab/Dashboard links to 'Musicom Project Master'.
- **Email Workflow**: Use `himalaya` to download MIDI attachments to `/tmp/`, analyze, and update project folders.
- **Pattern Exploration**: Treat systematic theory exercises as 'Pillar' explorations (Scale/Chord subsets, Rhythm grids).
- **Templates**: See `templates/dashboards.md` for dark-themed visualization logic and HTML structures.

### Pitfalls
- **Environment Constraints**: Check for `numpy` before using math-heavy synthesis; fallback to standard library `struct` for raw pulse generation.
- **WAV on Telegram**: WAV files often fail to render playable bubbles; OGG/Opus is the mandatory format for "Instant Play".
- **Path Resolution**: The sandbox `/root/` is often restricted; use `/opt/data/` or `/tmp/` for volatile media assets.

ffmpeg -i /tmp/hermes/songs/melody.wav -codec:a libopus -application voip -b:a 48k /tmp/hermes/songs/melody.ogg -y -loglevel error 2>&1
```

### Send via send_message tool

```
target: "telegram:Axel (dm)"
message: "Your melody! 🎵\nMEDIA:/tmp/hermes/songs/melody.ogg"
```

Key: the `MEDIA:/absolute/path/to-file` prefix tells the platform to send the file natively. `.ogg` sends as a **voice bubble**. `.mp4` plays inline. `.png`/`.webp`/`.jpg` appear as photos.

### Send Workflow — DO NOT RETRY

1. Convert WAV → OGG via ffmpeg
2. Verify file exists: `ls -la /tmp/hermes/songs/melody.ogg`
3. **Play it first** via `ffplay -nodisp -autoexit /tmp/hermes/songs/melody.ogg` — confirm it works locally before sending
4. Send once with `MEDIA:/` prefix
5. **If it doesn't arrive — DO NOT RETRY.** Tell the user the file path directly and stop. Spamming is worse than not sending.

### Instant Playback & Synthesis Workflow
- **Multi-instrument Ensemble**: Balance volumes when mixing (e.g., Piano 0.3, Guitar 0.4, Violin 0.3).
- **Subtle Vibrato**: For natural violin sounds, use ~5.5Hz vibrato with <1% depth. High vibrato (>2%) sounds "unnatural" or "synthetic" to the user.
- **Instrument Envelopes**: Piano/Guitar use fast exponential decay; Violin requires a "bowing" attack (~200ms) and release (~300ms).
- **Harmonic Profiles**: Violin (Sawtooth 1/n), Piano (Discrete additive 1, 0.5, 0.2), Guitar (Karplus-Strong Noise).

### Instant Playback & Synthesis Workflow
1. **Mathematical Representation**: Treat all musical elements as **Subsets** (Pitch Class Subsets or Time Grid Subsets).
2. **Low-Level Synthesis**: Use the specialized engines developed in Pillar 2:
   - **Piano**: Additive synthesis with fast decay.
   - **Guitar**: Karplus-Strong string modeling (filtered noise).
   - **Violin**: Sawtooth summation with FM vibrato (5.5Hz).
3. **Format Conversion**: Convert `.wav` -> `.ogg` (Opus) via `ffmpeg` with `-application voip -b:a 48k`.
4. **Delivery**: Use `MEDIA:/path/to/file.ogg` to deliver "voice bubbles" for instant user playback.
5. **Absolute Paths**: Always use absolute paths (e.g., `/opt/data/projects/...`) to avoid "Media not found" errors in Telegram blocks.
6. **Euclidean Rhythms**: Use the Euclidean algorithm to distribute pulses evenly across steps for grooves (e.g., Tresillo 3,8).

### Pillar 2: Low-Level Synthesis
- **Scripts**: See `scripts/pillar2_synthesis_engines.py` for standalone implementations of Guitar, Piano, and Violin.
- **Ensemble Setup**: Use `scripts/ensemble_synthesis.py` for mixing multiple synthesis sources.
- **Flat.io / MuseScore Integration**:
    - Use MusicXML as the bridge format. 
    - The `musicom.converters.music21_score` module in the core repository handles the `unit_to_stream` conversion.
    - **Note**: Ensure `PYTHONPATH` includes `/root/musicom` or relevant paths in `/opt/data/`.

### Composition Dashboarding (Project Hub)
For multi-session cooperation, maintain a centralized GitHub Pages dashboard:
1. **Project Index**: A root `index.html` linking to individual project folders.
2. **Project Workspace**: Each project in `projects/[id]-[name]/` containing its own `index.html` dashboard.
3. **Dashboard Standards**:
   - **Theme**: Dark, high-contrast (Slate-950 background, Cyan/Rose accents).
   - **Branding**: Credit "Musicom" as the composer; project name as title.
   - **Components**: Analytical Overview (Status/Mode/Meter), Advanced Analysis (Chroma Profile/Melodic Contour), Primary Visuals (Piano Roll/Volume Graph), and BandLab link.
4. **Pattern Exploration (Non-Compositional)**:
   - For theoretical exercises (Project 003+), organize by **Pillar 1 (Pitch)**: Catalog scales/modes/chords, and **Pillar 2 (Rhythm)**: Catalog meters/grooves/polyrhythms.

### External Platform Integration
- **Notion Hub**: Use a "Musicom Central Hub" parent page linked to the `Musicom Agent` integration.
- **Master Database**: Properties for Status, Genre, Key, Dashboard URL, and BandLab URL.
- **To-Do Sync**: Actively use the "To Do List DB" to track and update collaborative task status.
- **BandLab**: Always include direct track or revision URLs (e.g., `www.bandlab.com/axelwiertz/...`) in dashboards and Notion.

- **Project Management**: Organize assets into `projects/[id]-[name]/`. Create a Master Index (index.html) in root.
- **Notion Integration**: Sync project status, Genre, Key, and BandLab/Dashboard links to 'Musicom Project Master'.
- **Email Workflow**: Use `himalaya` to download MIDI attachments to `/tmp/`, analyze, and update project folders.
- **Pattern Exploration**: Treat systematic theory exercises as 'Pillar' explorations (Scale/Chord subsets, Rhythm grids).
- **Templates**: See `templates/dashboards.md` for dark-themed visualization logic and HTML structures.

### Pitfalls
- **Environment Constraints**: Check for `numpy` before using math-heavy synthesis; fallback to standard library `struct` for raw pulse generation.
- **WAV on Telegram**: WAV files often fail to render playable bubbles; OGG/Opus is the mandatory format for "Instant Play".
- **Path Resolution**: The sandbox `/root/` is often restricted; use `/opt/data/` or `/tmp/` for volatile media assets.

- **NEVER retry a send more than once.** One attempt, if it fails silently, fall back to telling the user the path. Sending the same message 5+ times is worse than not sending at all.
- Always use `-application voip` flag for best Telegram voice bubble quality
- Use `target: "telegram:Axel (dm)"` when available instead of bare chat IDs — it is the canonical handle
- **Always verify audio works via ffplay before attempting to send to user** — don't send broken audio
