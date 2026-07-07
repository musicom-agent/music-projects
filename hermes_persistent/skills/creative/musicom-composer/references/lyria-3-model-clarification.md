# Lyria 3 & AI Music Model Clarification — 2026-05-17

## Context

User asked: "Can I use Lyria 3 as a composer skill, not a full generation from a prompt?"

## Finding

**Lyria 3 is Google's AI video generation model, NOT a music model.**

| Model ID | Type | Capability |
|----------|------|-----------|
| `google/lyria-3-clip-preview` | Video generation | Text/image → video clips |
| `google/lyria-3-pro-preview` | Video generation | Higher-quality professional video |

Lyria generates **video frames** from text or image prompts. It has:
- ❌ No music composition capability
- ❌ No MIDI generation
- ❌ No audio synthesis
- ❌ No melody/harmony/rhythm understanding

## Available Models That CAN Do Music

| Model / Skill | What It Does |
|---|---|
| `musicom-composer` skill | Pattern-based structured composition (MIDI/score) |
| `audiocraft-audio-generation` skill | Meta MusicGen — text-to-music audio |
| `heartmula` skill | Suno-like full song from lyrics + tags |
| `songwriting-and-ai-music` skill | Songwriting craft + Suno prompt engineering |

## Correction Embedded In

- `musicom-composer` SKILL.md — explicit "What Can & Can't Compose" table
- `musicom-theory-kb` SKILL.md — Known Implementation Gaps section
- `musicom-composer` references/ai-music-models-landscape.md — full model comparison

## Recommendation

For "composer, not full generation from a prompt" — use **Musicom's pattern-centric pipeline**:
1. Define pitch patterns (melodic DNA)
2. Define rhythm patterns (groove DNA)
3. Combine into MelodicPhrases
4. Apply harmony, structure, transformations
5. Export as MIDI/audio

This gives full creative control rather than black-box generation.