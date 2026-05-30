# AI Music Model Landscape — What Can & Can't Compose (2026-05-17)

## Models That CAN Generate Music

| Model / Skill | Type | How to Use |
|---|---|---|
| **MusicGen / AudioGen** (Meta) | Audio generation from text | `audiocraft-audio-generation` skill |
| **Suno AI** | Full song generation (text → vocals + music) | `songwriting-and-ai-music` skill |
| **HeartMuLa** | Suno-like song from lyrics + tags | `heartmula` skill |
| **Musicom** (local framework) | Pattern-based composition (MIDI/score) | `musicom-composer` skill |
| **NeuTTS** | Text-to-speech (local, with reference voice) | TTS config → `neutts` provider |

## Models That CANNOT Do Music Composition

| Model | Provider | What It Actually Does | Why It Can't Compose |
|---|---|---|---|
| **Lyria 3** (Pro/Clip Preview) | Google via OpenRouter | AI video generation from text/image | Generates video frames, no audio/music capability |
| **Ring-2.6-1T** | OpenRouter (`inclusionai/ring-2.6-1t`) | Reasoning language model | Text reasoning only, no multimodal output |
| **Qwen 3.6 35B** | OpenRouter | General-purpose LLM | Text-only, no audio/music generation |
| **TTS models** (Edge, ElevenLabs, etc.) | Various | Speech synthesis | Converts text → speech, cannot compose music |

## Key Takeaway

**Lyria 3 is a video model, not a music model.** Its full name on OpenRouter is
`google/lyria-3-pro-preview` and `google/lyria-3-clip-preview`. It generates
video from text or image prompts. It has zero capability for:
- Music composition or MIDI generation
- Audio synthesis or sound design
- Melody, harmony, or rhythm creation

If you need AI-generated music, use **Musicom** (pattern-based, full control)
for structured composition, or **AudioCraft/MusicGen** for text-to-music
generation. For full songs with vocals, use **Suno AI** or **HeartMuLa**.