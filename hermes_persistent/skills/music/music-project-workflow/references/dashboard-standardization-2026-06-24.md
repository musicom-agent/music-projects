# Dashboard & Delivery Standardization

## Unified Project Dashboard (index.html)
Every musicom project MUST contain a root `index.html` as the primary human entry point.

### Minimal Dashboard Sections:
1. **Audio Player**: Native `<audio>` tag pointing to `Audio/*.ogg`.
2. **Matrix Visualization**: ASCII or SVG representation of the UnitMatrix.
3. **Harmony Report**: Summary of chord-tone accuracy (e.g., "Harmony: 100%, Lead: 40% CT").
4. **DNA Reference**: Pitch-class set and Euclidean parameters used.
5. **Score Links**: Download links for `.mid`, `.wav`, and `.musicxml`.

## Compact vs Full Reporting (User Preference 2026-06-24)

### Telegram (Compact)
Output should look like this:
- **Style**: [Style]
- **Key**: [Key]
- **Delta**: [Parameter Changes]
- **Status**: [Success/Fail]
MEDIA:/path/to/file.ogg
MEDIA:/path/to/file.mid

### File Logs (Full)
File: `/opt/data/projects/[Path]/logs/report-YYYY-MM-DD.md`
Content: 
- Full prompt/task description.
- Detailed DSP calculations.
- Reasoning for specific musical choices.
- Tracebacks or error resolution paths taken during the session.
