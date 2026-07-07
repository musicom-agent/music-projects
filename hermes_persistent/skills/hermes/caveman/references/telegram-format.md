# Telegram Formatting Rules for Caveman Mode

## Supported Markdown
- **Bold**: `**text**` → **text**
- *Italic*: `*text*` → *text*
- ~~Strikethrough~~: `~~text~~` → ~~text~~
- ||Spoiler||: `||text||` → ||text||
- `Inline code`: `` `text` `` → `text`
- ```Code blocks```: 
```
text
```
- [Links](url): `[text](url)` → [text](url)
- Headers: `## Header` → **Header** (Telegram renders as bold)

## Unsupported in Telegram
- Tables: Convert to bullet lists or key: value pairs.
- Nested formatting: Telegram ignores nesting (e.g., `**bold *italic***` → **bold *italic***).

## Media
- **Files**: Use `MEDIA:/absolute/path/to/file` in response. Telegram sends as native media.
  - Images: `.png`, `.jpg`, `.webp` → photo
  - Audio: `.ogg` → voice bubble
  - Video: `.mp4` → inline video
- **Image URLs**: `![alt](url)` → native photo.

## Caveman-Specific Rules
- **Brevity**: Drop filler. Use fragments. Example:
  - ❌ "I will now send the file."
  - ✅ "Sending file."
- **Media**: Always use absolute paths. Example:
  - ❌ "Here is the file."
  - ✅ `MEDIA:/opt/data/projects/001/audio.ogg`
- **Headers**: Use `##` for section breaks. Example:
  - ❌ "Here is the analysis:"
  - ✅ `## Analysis`
- **Lists**: Use `-` or `•` for bullets. Example:
  - ❌ "The issues are: 1. X, 2. Y."
  - ✅ `- X
  - Y`

## Pitfalls
- **Tables**: Telegram auto-converts pipe tables to bullet lists. Prefer bullets.
- **Code blocks**: Telegram renders as monospace. Use for CLI output, JSON, or MIDI dumps.
- **Media paths**: Must be absolute. Relative paths fail silently.