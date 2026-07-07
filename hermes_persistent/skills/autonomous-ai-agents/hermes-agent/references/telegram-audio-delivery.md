# Telegram Audio Delivery: Voice Bubbles vs File Attachments

## How Telegram Handles Audio Files

Telegram's bot API **auto-converts** certain audio extensions to voice notes/audio messages:

| Extension | How Telegram delivers it |
|-----------|-------------------------|
| `.ogg` (Opus) | **Voice bubble** (round audio note) ✅ intended for voice |
| `.wav` | **Voice bubble** ⚠️ not intended for voice |
| `.mp3` | **Voice bubble** (audio message) |
| `.m4a` | **Voice bubble** (audio message) |
| `.mid`, `.midi` | **File attachment** (document) |
| `.bin`, `.audio` | **File attachment** (document) |

### Pattern: Telegram auto-detects by extension

If the file extension matches a known audio format, Telegram renders it as a voice bubble, regardless of actual content. To force it as a document file, use a **non-audio extension**.

## Force Audio as File Attachment

Rename the file to a non-audio extension before sending:

```bash
cp melody.wav /tmp/hermes/songs/melody.audio
# or
cp melody.wav /tmp/hermes/songs/melody.bin
```

Then send with the new extension — Telegram will deliver it as a downloadable document.

## Usage in send_message

```
# Voice bubble (intended):
message: "Here's a voice note! 🎵\nMEDIA:/tmp/hermes/songs/melody.ogg"

# File attachment (force):
message: "Composition file:\nMEDIA:/tmp/hermes/songs/melody.audio"
```

## Pitfalls

- **First send attempt may fail** — the file must exist on disk at the referenced path
- **Always verify with `ls -la`** after ffmpeg conversion before sending
- **Voice bubble quality** — use `ffmpeg -application voip -b:a 48k` for best Telegram voice bubble quality
- **MIDI files** (`.mid`) are always sent as documents, not audio — useful for structured compositions
